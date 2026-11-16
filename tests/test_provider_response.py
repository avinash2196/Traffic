"""ASOR-M08A: actual bounded HTTP child, synthetic owned loopback only."""
import base64
from contextlib import contextmanager
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import socket
import subprocess
import threading
import time
from urllib.parse import urlsplit

import httpx
import pytest

from tests.test_gemini_assessment import assessment_runtime, submit, output, positive, HOST, KEY

SENTINELS = ('PRIVATE_BODY_SENTINEL', 'PRIVATE_TOKEN_SENTINEL',
             'C:/synthetic-private/evidence.jpg', 'PRIVATE_MEDIA_SENTINEL',
             'PRIVATE_PROMPT_SENTINEL', KEY)
STAGES = {'upload-start', 'upload-finalize', 'file-poll', 'generate', 'file-delete'}
CLASSES = {'HTTP_STATUS', 'NETWORK_ERROR', 'TIMEOUT', 'PROCESSING_ERROR'}


def run(runtime, report_id):
    # Real process startup consumes the configured budget; observe up to that
    # budget plus five seconds for scheduler/test bookkeeping, without extending it.
    from tests.test_durable_processing import OFFICER
    worker = runtime[4][-1]
    worker.start()
    try:
        assert worker.wait_idle(runtime[0].app.state.ai_settings['AI_ATTEMPT_TIMEOUT_SECONDS'] + 5), 'Owned worker did not become idle'
    finally:
        worker.stop()
    response = runtime[0].get('/api/authority/reports/' + report_id, headers=OFFICER)
    assert response.status_code == 200
    return response.json()

@contextmanager
def endpoint():
    state = dict(calls=[], mode='plain', fail_stage=None, status=400, value=None)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def handle_call(self):
            body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            path = urlsplit(self.path).path
            stage = ('file-delete' if self.command == 'DELETE' else
                     'upload-start' if path == '/upload/v1beta/files' else
                     'upload-finalize' if path.startswith('/upload/session/') else
                     'file-poll' if path.startswith('/v1beta/files/') else 'generate')
            state['calls'].append((stage, body, self.headers.get('x-goog-api-key')))
            if stage == state['fail_stage'] and state['status'] == 'reset':
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
                return
            headers = {}
            status = 200
            if stage == state['fail_stage']:
                status = state['status']
                payload = {'error': {'message': ' '.join(SENTINELS)}}
                headers['Retry-After'] = '17'
            elif stage == 'upload-start':
                payload = {}
                headers['x-goog-upload-url'] = 'https://' + HOST + '/upload/session/PRIVATE_TOKEN_SENTINEL'
            elif stage in ('upload-finalize', 'file-poll'):
                value = {'name': 'files/synthetic', 'uri': 'https://' + HOST + '/v1beta/files/synthetic',
                         'state': 'PROCESSING' if stage == 'upload-finalize' else 'ACTIVE'}
                payload = {'file': value} if stage == 'upload-finalize' else value
            elif stage == 'generate':
                state['prompt'] = json.loads(body) if body else {}
                payload = {'candidates': [{'finishReason': 'STOP', 'content': {'parts': [
                    {'text': json.dumps(state['value'])}]}}]}
            else:
                payload = {}
            raw = json.dumps(payload).encode()
            if state['mode'] == 'gzip':
                raw = gzip.compress(raw)
                headers['Content-Encoding'] = 'gzip'
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            for key, value in headers.items(): self.send_header(key, value)
            # Exercise chunk framing as well as compressed Content-Length.
            if state['mode'] == 'chunked':
                self.send_header('Transfer-Encoding', 'chunked')
                self.end_headers()
                self.wfile.write(('%x\r\n' % len(raw)).encode() + raw + b'\r\n0\r\n\r\n')
            else:
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
        do_GET = do_POST = do_DELETE = handle_call
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    state['base'] = 'http://127.0.0.1:' + str(server.server_port)
    try:
        yield state
    finally:
        server.shutdown(); server.server_close(); thread.join(5)
        assert not thread.is_alive()


@contextmanager
def remap_child(monkeypatch, state):
    """Keep fixed child code/real transport; redirect only stdin URL to our socket."""
    import durable
    real = subprocess.Popen
    children = []
    class Owned:
        def __init__(self, args, **kwargs):
            assert args[-1] == durable._GEMINI_HTTP_CHILD
            assert args[1:4] == ['-I', '-B', '-c']
            self.child = real(args, **kwargs)
            children.append(self.child)
        def communicate(self, payload=None, **kwargs):
            if payload is not None:
                value = json.loads(payload)
                url = urlsplit(value['url'])
                assert url.scheme == 'https' and url.netloc == HOST
                value['url'] = state['base'] + url.path
                if url.query: value['url'] += '?' + url.query
                payload = json.dumps(value).encode()
            return self.child.communicate(payload, **kwargs)
        def __getattr__(self, name):
            return getattr(self.child, name)
    monkeypatch.setattr(subprocess, 'Popen', Owned)
    try:
        yield children
    finally:
        for child in children:
            if child.poll() is None:
                child.kill(); child.communicate()
            assert child.poll() is not None


@pytest.mark.parametrize('mode', ['plain', 'gzip', 'chunked'])
def test_real_child_response_framing(monkeypatch, mode):
    import durable
    with endpoint() as state, remap_child(monkeypatch, state) as children:
        state['mode'] = mode
        state['value'] = {'synthetic': True}
        with durable.gemini_client_factory() as client:
            try:
                response = client.post('https://' + HOST + '/generate',
                    extensions={'asor_deadline': time.monotonic() + 8})
            except httpx.DecodingError:
                pytest.fail('RESPONSE_FRAMING_MISSING: decoded bytes were decoded again')
        assert response.status_code == 200 and response.json()['candidates']
        assert len(state['calls']) == len(children) == 1
        assert response.headers.get('Content-Encoding', 'identity') == 'identity', 'RESPONSE_FRAMING_MISSING'
        assert 'Transfer-Encoding' not in response.headers, 'RESPONSE_FRAMING_MISSING'
        assert ('Content-Length' not in response.headers or
                int(response.headers['Content-Length']) == len(response.content)), 'RESPONSE_FRAMING_MISSING'


@pytest.mark.parametrize('stage,status,code,kind', [
    ('upload-start', 400, 'PROVIDER_REQUEST_REJECTED', 'HTTP_STATUS'),
    ('upload-finalize', 403, 'PROVIDER_CONFIGURATION', 'HTTP_STATUS'),
    ('file-poll', 429, 'PROVIDER_TRANSIENT', 'HTTP_STATUS'),
    ('generate', 503, 'PROVIDER_TRANSIENT', 'HTTP_STATUS'),
    ('generate', 'reset', 'PROVIDER_TRANSIENT', 'NETWORK_ERROR'),
])
def test_attempt_diagnostic_capture(assessment_runtime, monkeypatch, caplog, stage, status, code, kind):
    import durable
    import gemini
    runtime = assessment_runtime
    monkeypatch.setattr(durable, 'gemini_client_factory', DEFAULT_FACTORY)
    monkeypatch.setattr(durable, 'gemini_monotonic', time.monotonic)
    monkeypatch.setitem(runtime[0].app.state.ai_settings, 'AI_ATTEMPT_TIMEOUT_SECONDS', 30)
    caplog.set_level(logging.DEBUG)
    with endpoint() as state, remap_child(monkeypatch, state) as children:
        report_id, job_id, ids, _ = submit(runtime, key='positive-boundary')
        state['value'] = output(ids)
        positive = run(runtime, report_id)
        assert positive['ai']['state'] == 'completed', (
            positive['ai']['failure_code'], [call[0] for call in state['calls']])
        assert [x[0] for x in state['calls']] == ['upload-start', 'upload-finalize', 'file-poll', 'generate', 'file-delete']
        state['calls'].clear()
        runtime[4].append(runtime[5](runtime[2] / 'roadwatch.db'))
        state.update(fail_stage=stage, status=status)
        report_id, job_id, ids, _ = submit(runtime, key='failed-boundary')
        state['value'] = output(ids)
        body = run(runtime, report_id)
        assert body['ai']['attempt_count'] == 1
        assert body['ai']['state'] == ('retry-wait' if code == 'PROVIDER_TRANSIENT' else 'failed')
        assert body['ai']['failure_code'] == code
        assert body['status'] == 'awaiting-review'
        db = runtime[1]
        assert db.execute('SELECT provisional_points FROM reports WHERE id=?', (report_id,)).fetchone()[0] == 0
        assert sum(x[0] == 'generate' for x in state['calls']) <= 1
        assert all(x[2] == KEY for x in state['calls'])
        assert all(child.poll() is not None for child in children)
        # Guard before querying absent schema: intentional RED, never SQL setup error.
        assert db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='ai_provider_diagnostics'").fetchone(), 'SAFE_DIAGNOSTIC_MISSING'
        rows = db.execute('SELECT provider_status,request_stage,diagnostic_class FROM ai_provider_diagnostics WHERE job_id=? AND number=1', (job_id,)).fetchall()
        assert len(rows) == 1, 'SAFE_DIAGNOSTIC_MISSING'
        assert tuple(rows[0]) == (None if status == 'reset' else status, stage, kind), 'SAFE_DIAGNOSTIC_MISSING'
        assert rows[0][1] in STAGES and rows[0][2] in CLASSES
        # Only synthetic DB; inspect persisted diagnostic content and captured logs.
        text = json.dumps([tuple(row) for row in db.execute('SELECT * FROM ai_provider_diagnostics')]) + caplog.text
        for secret in (*SENTINELS, gemini.PROMPT, str(runtime[2])):
            assert secret not in text, 'UNSAFE_DIAGNOSTIC_DETAIL'


def test_unobserved_diagnostic_stays_unknown(assessment_runtime, monkeypatch):
    import gemini
    runtime = assessment_runtime
    positive(runtime)
    runtime[4].append(runtime[5](runtime[2] / 'roadwatch.db'))
    report_id, job_id, _, _ = submit(runtime, key='unknown-boundary')
    def fail(self, prepared):
        raise RuntimeError(' '.join(SENTINELS))
    monkeypatch.setattr(gemini.Adapter, 'dispatch', fail)
    body = run(runtime, report_id)
    assert body['ai']['failure_code'] == 'PROCESSING_ERROR' and body['ai']['attempt_count'] == 1
    db = runtime[1]
    assert db.execute("SELECT 1 FROM sqlite_master WHERE name='ai_provider_diagnostics'").fetchone(), 'SAFE_DIAGNOSTIC_MISSING'
    rows = db.execute('SELECT provider_status,request_stage,diagnostic_class FROM ai_provider_diagnostics WHERE job_id=? AND number=1', (job_id,)).fetchall()
    assert [tuple(x) for x in rows] == [(None, None, 'PROCESSING_ERROR')], 'SAFE_DIAGNOSTIC_MISSING'


@pytest.mark.parametrize('phase', ['serialize', 'startup', 'reconstruct'])
def test_absolute_deadline_covers_parent_work(monkeypatch, phase):
    import durable
    real_dumps, real_loads = json.dumps, json.loads
    real_popen = subprocess.Popen
    now = time.monotonic()
    clock = [now]
    monkeypatch.setattr(time, 'monotonic', lambda: clock[0])
    children = []
    def dumps(value, *args, **kwargs):
        result = real_dumps(value, *args, **kwargs)
        if phase == 'serialize': clock[0] += 2
        return result
    def loads(value, *args, **kwargs):
        result = real_loads(value, *args, **kwargs)
        if phase == 'reconstruct': clock[0] += 2
        return result
    def popen(args, **kwargs):
        child = real_popen(args, **kwargs); children.append(child)
        if phase == 'startup': clock[0] += 2
        return child
    monkeypatch.setattr(json, 'dumps', dumps)
    monkeypatch.setattr(json, 'loads', loads)
    monkeypatch.setattr(subprocess, 'Popen', popen)
    # Faithful child output, only for parent timing; framing uses real HTTP above.
    monkeypatch.setattr(durable, '_GEMINI_HTTP_CHILD', "import sys; sys.stdin.buffer.read(); sys.stdout.write('{\"status\":200,\"headers\":[],\"content\":\"e30=\"}')")
    with durable.gemini_client_factory() as client:
        try:
            client.post('https://' + HOST + '/timing', extensions={'asor_deadline': now + 1})
        except httpx.TimeoutException:
            pass
        else:
            pytest.fail('ABSOLUTE_DEADLINE_MISSING')
    assert len(children) == (0 if phase == 'serialize' else 1)
    assert all(p.poll() is not None for p in children)


def test_real_timeout_kills_and_reaps_before_return(monkeypatch):
    import durable
    real = subprocess.Popen
    children = []
    def popen(args, **kwargs):
        child = real(args, **kwargs); children.append(child); return child
    monkeypatch.setattr(subprocess, 'Popen', popen)
    monkeypatch.setattr(durable, '_GEMINI_HTTP_CHILD', 'import time; time.sleep(20)')
    with durable.gemini_client_factory() as client:
        for _ in range(2):
            with pytest.raises(httpx.TimeoutException):
                client.post('https://' + HOST + '/owned-no-network',
                    extensions={'asor_deadline': time.monotonic() + .25})
            assert children and all(p.poll() is not None for p in children)
    assert len(children) == 2


import durable as _durable
DEFAULT_FACTORY = _durable.gemini_client_factory
