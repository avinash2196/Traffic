"""Owned process lifetime and fixed-host, no-retry provider transport."""
import asyncio
from contextlib import contextmanager, nullcontext
import ctypes
import json
import multiprocessing
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit

import httpx
from agw_protocol import BoundaryError


def stop_process(process):
    if process.poll() is None:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                           capture_output=True, timeout=5, check=False)
        else:
            process.kill()
    process.wait(timeout=5)


def deadline_remaining(deadline, stage):
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise BoundaryError('ATTEMPT_TIMEOUT', stage)
    return remaining


def decoder_memory_limit():
    import resource
    ctypes.CDLL(None).prctl(1, signal.SIGKILL)
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))


def windows_process_job(process, memory_limit):
    # Assign the suspended decoder before it can allocate/decode untrusted input.
    from ctypes import wintypes
    class Basic(ctypes.Structure):
        _fields_ = [('per_process', ctypes.c_int64), ('per_job', ctypes.c_int64),
                    ('flags', wintypes.DWORD), ('minimum', ctypes.c_size_t),
                    ('maximum', ctypes.c_size_t), ('active', wintypes.DWORD),
                    ('affinity', ctypes.c_size_t), ('priority', wintypes.DWORD),
                    ('scheduling', wintypes.DWORD)]
    class Io(ctypes.Structure):
        _fields_ = [(name, ctypes.c_uint64) for name in
                    ('read_operations', 'write_operations', 'other_operations', 'read_bytes', 'write_bytes', 'other_bytes')]
    class Extended(ctypes.Structure):
        _fields_ = [('basic', Basic), ('io', Io), ('process_memory', ctypes.c_size_t),
                    ('job_memory', ctypes.c_size_t), ('peak_process', ctypes.c_size_t),
                    ('peak_job', ctypes.c_size_t)]
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateJobObjectW.restype = wintypes.HANDLE
    kernel.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    kernel.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.CreateJobObjectW(None, None)
    limits = Extended()
    limits.basic.flags = 0x2000 | (0x100 | 0x200 if memory_limit is not None else 0)
    limits.process_memory = memory_limit or 0
    limits.job_memory = memory_limit or 0
    if not handle or not kernel.SetInformationJobObject(handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
        raise OSError('Decoder isolation unavailable')
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    target = kernel.OpenProcess(0x0101, False, process.pid)
    assigned = bool(target) and kernel.AssignProcessToJobObject(handle, target)
    if target:
        kernel.CloseHandle(target)
    if not assigned:
        kernel.CloseHandle(handle)
        raise OSError('Decoder isolation unavailable')
    return handle, kernel, limits


_IMAGE_JOB = None


@contextmanager
def image_memory_guard():
    global _IMAGE_JOB
    if os.name == 'nt':
        class CurrentProcess:
            pid = os.getpid()
        if _IMAGE_JOB is None:
            _IMAGE_JOB = windows_process_job(CurrentProcess(), 512 * 1024 * 1024)
        handle, kernel, limits = _IMAGE_JOB
        limits.basic.flags = 0x100 | 0x200
        if not kernel.SetInformationJobObject(handle, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            raise BoundaryError('EVIDENCE_LIMIT', 'preparation')
        try:
            yield
        finally:
            limits.basic.flags = 0
            kernel.SetInformationJobObject(handle, 9, ctypes.byref(limits), ctypes.sizeof(limits))
    else:
        import resource
        previous = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, previous[1]))
        try:
            yield
        finally:
            resource.setrlimit(resource.RLIMIT_AS, previous)


def decode(command, source, deadline):
    process, job = None, None
    options = {}
    if os.name == 'nt':
        options['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP | 4
    else:
        options['preexec_fn'] = decoder_memory_limit
    with tempfile.TemporaryFile() as incoming, tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as diagnostic:
        incoming.write(source)
        incoming.seek(0)
        try:
            process = subprocess.Popen(command, stdin=incoming, stdout=output, stderr=diagnostic, **options)
            if os.name == 'nt':
                job = windows_process_job(process, 512 * 1024 * 1024)
                if ctypes.WinDLL('ntdll').NtResumeProcess(ctypes.c_void_p(int(process._handle))):
                    raise OSError('Decoder isolation unavailable')
            while process.poll() is None:
                deadline_remaining(deadline, 'preparation')
                if sum(os.fstat(stream.fileno()).st_size for stream in (incoming, output, diagnostic)) > 512 * 1024 * 1024:
                    raise BoundaryError('EVIDENCE_LIMIT', 'preparation')
                time.sleep(.01)
            deadline_remaining(deadline, 'preparation')
            if sum(os.fstat(stream.fileno()).st_size for stream in (incoming, output, diagnostic)) > 512 * 1024 * 1024:
                raise BoundaryError('EVIDENCE_LIMIT', 'preparation')
            output.seek(0)
            diagnostic.seek(0)
            error = diagnostic.read()
            if process.returncode:
                code = 'EVIDENCE_LIMIT' if process.returncode == 72 or any(word in error.lower() for word in
                        (b'cannot allocate memory', b'out of memory')) else 'EVIDENCE_UNAVAILABLE'
                raise BoundaryError(code, 'preparation')
            return output.read(), error
        except OSError:
            raise BoundaryError('EVIDENCE_UNAVAILABLE', 'preparation') from None
        finally:
            if process is not None:
                stop_process(process)
            if job:
                job[1].CloseHandle(job[0])


def provider_client_factory():
    return httpx.Client(transport=httpx.HTTPTransport(retries=0), follow_redirects=False,
                        trust_env=False, limits=httpx.Limits(max_connections=1, max_keepalive_connections=0))


def request(client, call, deadline, key):
    method, url, options = call
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.hostname not in (
            'api.openai.com', 'generativelanguage.googleapis.com') or parsed.port not in (None, 443) or (
            parsed.username or parsed.password or parsed.fragment):
        raise BoundaryError('PROCESSING_ERROR', 'provider')
    remaining = deadline_remaining(deadline, 'provider')
    headers = options.pop('headers', {})
    headers.update({'Authorization': 'Bearer ' + key} if parsed.hostname == 'api.openai.com'
                   else {'x-goog-api-key': key})
    try:
        response = client.request(method, url, headers=headers, timeout=httpx.Timeout(
            remaining, connect=min(2, remaining), pool=0), **options)
    except httpx.TimeoutException:
        raise BoundaryError('ATTEMPT_TIMEOUT', 'provider') from None
    except (httpx.NetworkError, httpx.RemoteProtocolError):
        raise BoundaryError('PROVIDER_TRANSIENT', 'provider') from None
    deadline_remaining(deadline, 'provider')
    return response


class Progress(dict):
    def __init__(self, path, **values):
        self.path = Path(path)
        super().__init__(values)
        self.save()

    def save(self):
        temporary = self.path.with_suffix('.pending')
        temporary.write_text(json.dumps(self), encoding='utf-8')
        temporary.replace(self.path)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.save()


def pipeline_child(source, result, deadline, provider, key, client_factory):
    from agw_media import prepare_media
    from agw_protocol import parse_json, usage
    import openai_adapter
    import gemini
    state = Progress(result, media_coverage=[], usage=usage(), model_version=None, provider_request_id=None,
                 billing_state='not-invoked', assessment=None, error=None,
                 timings_ms=dict(preparation=None, provider=None, normalization=None))
    started = time.monotonic()
    try:
        value = parse_json(Path(source).read_text(encoding='utf-8'))
        import base64
        media = [dict(id=item['media_id'], mime_type=item['mime_type'], bytes=base64.b64decode(item['data_base64']))
                 for item in value['evidence']]
        preparation = min(deadline, started + 30)
        parts = prepare_media(media, provider, preparation, state['media_coverage'], state.save)
        state['timings_ms']['preparation'] = int((time.monotonic() - started) * 1000)
        provider_deadline = min(time.monotonic() + 70, deadline - 2)
        deadline_remaining(provider_deadline, 'provider')
        adapter = openai_adapter if provider == 'openai' else gemini
        with client_factory() as client:
            adapter.assess(value, media, parts, state, client, key, provider_deadline)
        deadline_remaining(deadline, 'normalization')
    except BoundaryError as error:
        state['error'] = error.envelope()
    except Exception:
        state['error'] = BoundaryError('PROCESSING_ERROR', 'preparation').envelope()
    finally:
        if state['timings_ms']['preparation'] is None:
            state['timings_ms']['preparation'] = int((time.monotonic() - started) * 1000)
        state.save()


def pipeline_server(connection, provider, key, client_factory):
    if os.name != 'nt':
        parent = os.getppid()
        ctypes.CDLL(None).prctl(1, signal.SIGKILL)
        if os.getppid() != parent:
            os._exit(1)
        os.setsid()
    import agw_media
    import openai_adapter
    import gemini
    from PIL import Image
    with client_factory() as client:
        connection.send('ready')
        while True:
            value = connection.recv()
            if value is None:
                return
            source, result, deadline = value
            client.cookies.clear()
            try:
                pipeline_child(source, result, deadline, provider, key, lambda: nullcontext(client))
            finally:
                client.cookies.clear()
            connection.send('complete')


class Pipeline:
    def __init__(self, provider, key, factory):
        self.arguments = provider, key, factory
        self.process = self.connection = self.ownership = None

    async def start(self):
        context = multiprocessing.get_context('spawn')
        self.connection, child = context.Pipe()
        self.process = context.Process(target=pipeline_server, args=(child, *self.arguments))
        self.process.start()
        child.close()
        try:
            if os.name == 'nt':
                self.ownership = windows_process_job(self.process, None)
            deadline = time.monotonic() + 10
            while not self.connection.poll():
                if not self.process.is_alive() or time.monotonic() >= deadline:
                    raise RuntimeError('Gateway worker unavailable')
                await asyncio.sleep(.01)
            if self.connection.recv() != 'ready':
                raise RuntimeError('Gateway worker unavailable')
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.process is not None:
            if self.process.is_alive():
                if os.name == 'nt':
                    subprocess.run(['taskkill', '/PID', str(self.process.pid), '/T', '/F'],
                                   capture_output=True, timeout=5, check=False)
                else:
                    try:
                        os.killpg(self.process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        self.process.kill()
            self.process.join(timeout=5)
            if self.process.is_alive():
                self.process.kill()
                self.process.join(timeout=5)
            if self.process.is_alive():
                raise RuntimeError('Owned process not reaped')
            self.process.close()
            self.process = None
        if self.ownership:
            self.ownership[1].CloseHandle(self.ownership[0])
            self.ownership = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None


async def run_pipeline(paths, deadline, worker, disconnected):
    source, result = paths
    completed = False
    worker.connection.send((str(source), str(result), deadline))
    try:
        while not worker.connection.poll():
            if disconnected.is_set():
                raise asyncio.CancelledError()
            deadline_remaining(deadline - 1.5, 'provider')
            if not worker.process.is_alive():
                raise BoundaryError('PROCESSING_ERROR', 'transport')
            await asyncio.sleep(.01)
        if worker.connection.recv() != 'complete' or not result.is_file():
            raise BoundaryError('PROCESSING_ERROR', 'transport')
        completed = True
        return json.loads(result.read_text(encoding='utf-8'))
    except BoundaryError as error:
        error.progress = json.loads(result.read_text(encoding='utf-8')) if result.is_file() else None
        raise
    finally:
        if not completed:
            worker.close()
