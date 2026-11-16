"""Local stateless advisory gateway; one admitted invocation, no durable queue."""
import asyncio
from contextlib import asynccontextmanager
import hmac
import json
import logging
import os
from pathlib import Path
import shutil
import time
from uuid import uuid4

from fastapi import FastAPI
from starlette.requests import ClientDisconnect, Request
from starlette.responses import JSONResponse

from agw_protocol import (BODY_LIMIT, BoundaryError, ERRORS, PROFILES, VERSIONS, require,
                          token_valid, usage, utc, validate_request)
from agw_transport import provider_client_factory as default_client_factory, run_pipeline, Pipeline

LOG = logging.getLogger('ai.gateway')


class Invocation:
    def __init__(self):
        self.started = time.monotonic()
        self.evidence_metadata = []
        self.value = dict(contract_version='agw-v1', correlation_id=None, attempt_id=None,
            attempt_number=None, evidence_revision=None, gateway_request_id=uuid4().hex,
            provider=None, model=None, model_version=None, prompt_version=None, policy_version=None,
            legal_reference_version=None, request_profile_version=None, media_profile_version=None,
            received_at=utc(), completed_at=None,
            timings_ms=dict.fromkeys(('receive', 'validation', 'preparation', 'provider', 'normalization', 'total')),
            provider_request_id=None, media_coverage=[], usage=usage(), billing_state='not-invoked',
            assessment=None, error=None)

    def trace(self, stage, outcome=None):
        safe = {key: self.value[key] for key in ('correlation_id', 'attempt_id', 'attempt_number',
                'gateway_request_id', 'provider', 'model', 'prompt_version', 'policy_version',
                'legal_reference_version', 'request_profile_version', 'media_profile_version',
                'provider_request_id', 'usage')}
        LOG.warning(json.dumps(dict(safe, utc=utc(), severity='INFO', stage=stage,
            elapsed_ms=max(0, int((time.monotonic() - self.started) * 1000)), outcome=outcome,
            evidence=self.evidence_metadata, sampled_frame_count=sum(len(entry['sampled_timestamps_ms']) for entry in self.value['media_coverage']),
            coverage_complete=[entry['complete'] for entry in self.value['media_coverage']],
            provider_status=self.value['error']['provider_status'] if self.value['error'] else None)))

    def respond(self, error=None):
        if error is not None:
            self.value['assessment'] = None
            self.value['error'] = error.envelope()
        self.value['completed_at'] = utc()
        self.value['timings_ms']['total'] = max(0, int((time.monotonic() - self.started) * 1000))
        self.trace('response', self.value['error']['code'] if self.value['error'] else 'completed')
        status = ERRORS[self.value['error']['code']][0] if self.value['error'] else 200
        return JSONResponse(self.value, status_code=status)


async def receive_body(request, invocation):
    encoding = request.headers.get('content-encoding', 'identity')
    require(encoding == 'identity', 'UNSUPPORTED_MEDIA_TYPE', 'admission')
    content_type = request.headers.get('content-type', 'application/json').lower().replace(' ', '')
    require(content_type in ('application/json', 'application/json;charset=utf-8'),
            'UNSUPPORTED_MEDIA_TYPE', 'admission')
    length = request.headers.get('content-length')
    if length is not None:
        require(length.isascii() and length.isdecimal(), 'INVALID_REQUEST', 'admission')
        require(int(length) <= BODY_LIMIT, 'REQUEST_TOO_LARGE', 'admission')
    body = bytearray()
    try:
        async with asyncio.timeout_at(invocation.started + 15):
            async for chunk in request.stream():
                require(len(body) + len(chunk) <= BODY_LIMIT, 'REQUEST_TOO_LARGE', 'admission')
                body.extend(chunk)
    except TimeoutError:
        raise BoundaryError('REQUEST_TIMEOUT', 'admission') from None
    invocation.value['timings_ms']['receive'] = int((time.monotonic() - invocation.started) * 1000)
    return bytes(body)


async def monitor_disconnect(request, disconnected):
    while not disconnected.is_set():
        if await request.is_disconnected():
            disconnected.set()
            return
        await asyncio.sleep(.02)


def service_settings():
    provider = os.getenv('AI_PROVIDER', 'openai')
    token = os.getenv('AI_GATEWAY_TOKEN', '')
    require(provider in PROFILES and token_valid(token), 'PROVIDER_CONFIGURATION', 'admission')
    model = os.getenv(provider.upper() + '_MODEL', PROFILES[provider][0])
    key = os.getenv(provider.upper() + '_API_KEY', '')
    require(model == PROFILES[provider][0] and bool(key.strip()) and
            bool(shutil.which('ffmpeg')) and bool(shutil.which('ffprobe')),
            'PROVIDER_CONFIGURATION', 'admission')
    return provider, token, key


def create_app(provider_client_factory=None, scratch_root=None):
    factory = provider_client_factory or default_client_factory
    root = Path(scratch_root) if scratch_root is not None else Path(__file__).with_name('.agw-scratch')
    active = False
    config = None
    worker = None

    @asynccontextmanager
    async def lifespan(application):
        nonlocal config, worker
        try:
            config = service_settings()
            root.mkdir(parents=True, exist_ok=True)
            require(not root.is_symlink(), 'PROVIDER_CONFIGURATION', 'admission')
            for child in root.iterdir():
                if child.is_dir() and not child.is_symlink():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        except Exception:
            raise RuntimeError('GATEWAY_CONFIGURATION_INVALID') from None
        for name in ('httpx', 'httpcore'):
            logging.getLogger(name).setLevel(logging.CRITICAL)
        worker = Pipeline(config[0], config[2], factory)
        await worker.start()
        try:
            yield
        finally:
            worker.close()

    application = FastAPI(lifespan=lifespan, openapi_url=None, docs_url=None, redoc_url=None)

    @application.middleware('http')
    async def boundary(request: Request, call_next):
        nonlocal active
        invocation = Invocation()
        owned, watcher = None, None
        disconnected = asyncio.Event()
        admitted = False
        try:
            provider, token, key = config
            if not hmac.compare_digest(request.headers.get('authorization', '').encode(),
                                       ('Bearer ' + token).encode()):
                raise BoundaryError('UNAUTHORIZED', 'admission')
            require(request.url.path == '/v1/assessments', 'NOT_FOUND', 'admission')
            require(request.method == 'POST', 'METHOD_NOT_ALLOWED', 'admission')
            require(not request.url.query and not request.headers.get('cookie'), 'INVALID_REQUEST', 'admission')
            require(not active, 'GATEWAY_BUSY', 'admission')
            active, admitted = True, True
            invocation.trace('admission')
            raw = await receive_body(request, invocation)
            started = time.monotonic()
            try:
                value, media = validate_request(raw, provider)
            except (TypeError, KeyError, AttributeError, OverflowError):
                raise BoundaryError('INVALID_REQUEST', 'validation') from None
            invocation.evidence_metadata = [dict(mime_type=item['mime_type'], byte_count=len(item['bytes'])) for item in media]
            invocation.value.update({name: value[name] for name in
                                    ('correlation_id', 'attempt_id', 'attempt_number', 'evidence_revision')})
            invocation.value.update(value['selection'], **VERSIONS)
            invocation.value['timings_ms']['validation'] = int((time.monotonic() - started) * 1000)
            invocation.trace('validation')
            deadline = invocation.started + value['budget_ms'] / 1000
            require(time.monotonic() < deadline - 2, 'ATTEMPT_TIMEOUT', 'preparation')
            owned = root / invocation.value['gateway_request_id']
            owned.mkdir()
            source, result = owned / 'request.json', owned / 'result.json'
            source.write_bytes(raw)
            del raw, media
            watcher = asyncio.create_task(monitor_disconnect(request, disconnected))
            invocation.trace('preparation')
            state = await run_pipeline((source, result), deadline, worker, disconnected)
            invocation.value.update({name: state[name] for name in ('media_coverage', 'usage', 'model_version',
                'provider_request_id', 'billing_state', 'assessment', 'error')})
            invocation.value['timings_ms'].update(state['timings_ms'])
            invocation.trace('provider')
            invocation.trace('normalization')
            return invocation.respond()
        except BoundaryError as error:
            progress = getattr(error, 'progress', None)
            if progress is not None:
                invocation.value.update({name: progress[name] for name in ('media_coverage', 'usage', 'model_version',
                    'provider_request_id', 'billing_state')})
            return invocation.respond(error)
        except (ClientDisconnect, asyncio.CancelledError):
            disconnected.set()
            raise
        except Exception:
            return invocation.respond(BoundaryError('PROCESSING_ERROR', 'transport'))
        finally:
            disconnected.set()
            if watcher is not None:
                watcher.cancel()
                try:
                    await watcher
                except asyncio.CancelledError:
                    pass
            if owned is not None:
                shutil.rmtree(owned)
            if admitted:
                if worker.process is None:
                    await worker.start()
                active = False

    return application


app = create_app()
