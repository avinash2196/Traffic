# Implementation Plan — Service Boundary RED

## Milestone

AGW-M02, ai-screening-officer-review; prepared 2026-11-11 (America/Chicago).

## Milestone Type

RED.

## Review Summary

- Tests only: separate authenticated gateway HTTP plus real application durable-worker dispatch.
- Requirements: AGW-R01–04/R06–09; deterministic prerequisites only for R05, whose real acceptance remains M04.
- Create three test/harness files; modify/delete none; production/configuration/dependencies remain untouched.
- Add 19 outcomes: image, VFR video, 12 rejection partitions, 2 output/usage failures, budget, worker success and restart/retry ownership.
- Verify `tests/verify_gateway_service.py --red`: predict 19 ordinary behavioral failures and 2 focused preserved passes.
- Review factory/source-isolation seams and representative limits below; untested CT03/06 resource/disconnect branches are explicit GREEN review obligations.
- Planning dry run: corrected exact fixture 19 intended RED; final probe evidence recorded below. This is not milestone execution.

## Authoritative References

- Current `requirements.md` and `Plan.md`: approved 2026-11-11; AGW-M01 complete, M02 Pending. `External-Contract.md`: user approved 2026-11-11, AGW-CT01–08. Their approvals authorize planning, not applying these tests.
- Earlier approved IP001–011: Review Summary/Carried-Forward Decisions and review status read; 010/011 relevant harness, worker, provider and media mechanisms inspected. Historical execution authority/status remains as recorded: 001–006/008–010 executed; 007 live blocker and 011 incomplete continuation are not completed here.
- `ASOR-M08D-Continuation-2026-11-11.md`, `MP4-Diagnosis-2026-11-11.md` and archived diagnostic `decoder_carrier.py` read as evidence/source. The original MP4 rejection has no established root cause; isolated single and 15-node diagnostic successes do not erase it.
- Current app/gateway/durable/intake/assessment/OpenAI source; named test modules and existing verifier; `.github/copilot-instructions.md` (historical v0.14 context superseded by approved focused artifacts); installed PDD0.16 implementation-planning/template, testing, API, security and LLM guidance. No applicable AGENTS.md found; product `docs/requirements.md` absent.

## Carried-Forward Decisions

001–005: real lifespan/schema, function-owned synthetic DB/media, explicit effective-path/closed-connection checks, source-only copies, existing interpreter/dependencies, disabled pytest autoload and explicit asyncio plugin, UTF-8/no-bytecode, stripped configuration, native Windows loopback and owned cleanup. 005: real JobStore claims/recovery/revision ownership and three attempts. 006/007: reuse common immutable prompt/catalog/schema and qualitative advisory policy. 008–011: no nested retries; allowlisted safe diagnostics; pinned offline decoder with stdin, network none and zero mounts; existing private backups/dirty work preserved. CT02/03/05/07 deliberately supersede historical terra/v1 and all-or-nothing usage conventions; no silent reopening.

## Preconditions / Predecessor Evidence

Approved M01 contract is recorded in the current Plan. Existing Python/FastAPI/httpx/pytest/subprocess infrastructure supports RED; absent service is the behavior under test. No dependency or bootstrap prerequisite is introduced. The default child serves ordinary HTTP404 only when the service file is absent; a broken present service import is never swallowed. Each service-negative case first proves authenticated positive HTTP and controlled provider dispatch; worker cases exercise actual accepted reports and durable state. No checkout source/test/config was applied during planning.

## Current Repository State

- `gateway.py:124` is in-process worker orchestration; `:138` constructs DB-coupled adapters; `:19` retains terra/v1. Current source has no service entry point.
- `durable.py:108` claims consumed attempts; `:147` recovers interrupted attempts; `:153` guards accepted results; `:250` delegates worker construction. Tests call this real factory/JobStore, never a mocked durable result.
- `openai_adapter.py:17,64,191` imports durable/loads media/prepares provider wire; existing adapter cannot be imported unchanged in a DB-free service source closure.
- `tests/conftest.py:16` gives a real isolated runtime; `tests/test_gateway_openai.py:371` makes a synthetic 40-frame VFR fixture; existing output builder returns provider JSON, not application results.
- Dirty baseline: modified app.py/bootstrap.py/tests/conftest.py/tests/test_api_endpoints.py/tests/test_auth.py; untracked assessment_policy.py/durable.py/gateway.py/gemini.py/intake.py/openai_adapter.py, existing ASOR docs and delivered tests/verifiers. Preserve all of it. No clean-working-tree or current full-suite claim.

## Files in Scope

### Files to Create

`tests/agw_service_child.py`, `tests/test_gateway_service.py`, `tests/verify_gateway_service.py`.

### Files to Modify

None. Exact modified-test diffs: none.

### Files to Delete

None.

## Proposed Changes

1. Controlled child executes separately with only service/policy/adapter source, no app/database modules, no provider socket egress. It supplies raw Responses wire via an injected httpx client and records synthetic provider calls; it does not supply gateway DTOs or application state.
2. Proposed technical seams for human review: `ai_gateway_service.create_app(*, provider_client_factory, scratch_root)` and public `app`; existing `durable.ai_worker_factory(path).assess_job(job_id)` stays the application entry. These are testability/implementation choices for later013, not changes to the approved HTTP contract. Service source closure permits ai_gateway_service, assessment_policy, openai_adapter, retained gemini and explicitly service-owned agw_*.py; no application path/database/control module imports allowed. New service-owned transport helpers may use the agw_ prefix. This additive source allowlist is an internal review choice, not a public contract. Module-scoped child avoids repeated process starts; provider test-control files are parent-owned synthetic harness state, never service endpoints. Reset occurs only after the previous controlled invocation drains.
3. Add seven named scenario functions plus parameterized cases, totaling19 outcomes. Representative partitions are deliberate: valid JPEG and ordered JPEG+40frame VFR MP4; malformed auth/duplicate/unknown/bool/base64/query;17attachments; exact prompt/model incompatibility; unsupported method/encoding; invalid decode; refusal and invalid-output with one invalid counter among valid neighbors;3s provider timeout; real HTTP worker success and3consumed transient attempts. No application deadline defaults change.
4. Source-only verifier hashes only explicit source/public-asset allowlists; all other root entries are metadata-only. It strips provider/bootstrap configuration, asserts effective temporary paths via reused fixtures, compiles all copied Python, selects19new+2affected nodes in bounded groups, classifies ordinary failures, and cleans owned state. Native decoder if present, otherwise pinned carrier through the archived canonical stdin helper; both wrapper resolutions checked as WindowsPath and direct `docker exec ... -version` preflight.

Contract/assertion map (representative coverage, not exhaustive):

| Contract / requirements | Assertions / preserved evidence | Explicitly untested here |
| --- | --- | --- |
| CT01;R01/R02/R03 | Separate child PID/source closure; auth-before-invalid-body401; query400/method405/encoding415; success via actual HTTP | startup token entropy/constant-time comparison, no CORS/docs, busy admission and nonloopback URL rejection require013 code review |
| CT02;R02 | exact terminal key set; known valid request; duplicate/unknown/bool/noncanonical base64,17items,prompt/model mismatch | exhaustive field/string/byte boundaries,224MiB counting/chunked/slow-body and128KiB metadata limits require013 code review; count16/17 is representative count partition |
| CT03;R02/R05/R09 | actual VFR PTS→32rational targets→31deduplicated actual frames,ordered image+video,disclosed omissions/audio and human referral | pixel/memory/downscale/external-reference/orphan/reap limits,sub-ms tie/dedup edge partitions; no native Gemini execution |
| CT04;R07/R09 | reused real policy/schema/catalog and common provider output; mixed-video uncertainty; illegal extra points output fails; application status/points unchanged | full unchanged legal/confidence/policy matrix remains existing coverage, not rerun; no real model-quality claim |
| CT05;R02/R06 | exact envelope; provider snapshot/request ID;timings;valid zeros/partial counters survive refusal/invalid output;fixed safe failure;no repair inference | full error-status/Retry-After date matrix; app durable failure-usage persistence is a013 review obligation, not asserted by direct-service usage cases |
| CT06;R04/R07 | one3s budget with2s reserve timeout; terminal scratch empty;3app-owned429 attempts across new worker instances and store recovery;4thdispatch absent | physical worker-process kill/restart,ambiguous connection loss,disconnect cancellation,reap/release and late-envelope mismatch; existing durable interrupted/stale guards are preserved mechanisms, not HTTP proof |
| CT07;R03 | GPT5.4snapshot/v2 profile,medium/8192/storefalse/strictschema,retained app snapshot passed through worker | historical terra fail-closed/legacyGemini read compatibility code review; no model access/live claim |
| CT08;R06/R08 | positive correlated safe log plus forbidden token/key/context/prompt checks; service source has no DB | full every-stage trace and hostile raw decoder/model disclosure matrix; synthetic diagnostics only |

Every CT01–08 normative rule above is either assigned an assertion/preserved mechanism or explicitly untested. Important untested invariants must be reviewed against exact013 source and reported as limitations; this plan does not claim runtime proof of them or authorize adding tests during GREEN. If review needs executable evidence beyond this inventory, revise/reapprove012 before execution rather than silently expand013.

## Proposed Code / Tests

Complete new contents follow. No existing file is modified.

### `tests/agw_service_child.py`

```python
"""Synthetic provider wire only; executable in the isolated service process."""
import time
import os
print('child-start '+str(time.monotonic())+' pid='+str(os.getpid()),flush=True)
import json
from pathlib import Path
import socket
import sys
import time

import httpx
import uvicorn
from fastapi import FastAPI

ROOT = Path(sys.argv[1])
MODE = ROOT / 'mode.json'
CALLS = ROOT / 'provider.jsonl'


def provider_client_factory():
    def respond(request):
        assert str(request.url) == 'https://api.openai.com/v1/responses'
        assert request.headers['authorization'] == 'Bearer synthetic-provider-key'
        body = json.loads(request.content)
        with CALLS.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(body) + '\n')
        mode = json.loads(MODE.read_text(encoding='utf-8'))
        if mode.get('delay'):
            time.sleep(mode['delay'])
        status = mode.get('status', 200)
        if status != 200:
            return httpx.Response(status, headers={'Retry-After': '7'}, json={
                'error': {'message': 'PRIVATE_PROVIDER_BODY C:/private/media.jpg'}})
        payload = {'status': 'completed', 'model': 'provider-reported-snapshot',
                   'usage': mode.get('usage', {'input_tokens': 23,
                       'input_tokens_details': {'cached_tokens': 0}, 'output_tokens': 11,
                       'output_tokens_details': {'reasoning_tokens': 3}, 'total_tokens': 34}),
                   'output': [{'type': 'message', 'role': 'assistant', 'content': [
                       {'type': 'output_text', 'text': json.dumps(mode['assessment'])}]}]}
        if mode.get('refusal'):
            payload['output'][0]['content'] = [{'type': 'refusal', 'refusal': 'PRIVATE_REFUSAL'}]
        return httpx.Response(200, headers={'x-request-id': 'req_synthetic'}, json=payload)
    def observed(request):
        active=ROOT/'provider-active'
        active.touch()
        try:
            return respond(request)
        finally:
            active.unlink(missing_ok=True)
    return httpx.Client(transport=httpx.MockTransport(observed), follow_redirects=False)


if __name__ == '__main__':
    print(json.dumps(dict(event='imports-complete',monotonic=time.monotonic(),pid=os.getpid())),flush=True)
    # The missing service is represented by ordinary HTTP 404, not import failure.
    # An existing but broken service import is never hidden by this fallback.
    if not (Path.cwd() / 'ai_gateway_service.py').is_file():
        app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
    else:
        from ai_gateway_service import create_app
        app = create_app(provider_client_factory=provider_client_factory,
                         scratch_root=ROOT / 'scratch')
    # No public-provider socket can be opened; the substitute returns wire bytes.
    original = socket.socket.connect
    def local_only(self, address):
        assert address[0] in ('127.0.0.1', '::1'), 'External network forbidden'
        return original(self, address)
    socket.socket.connect = local_only
    print(json.dumps(dict(event='starting-http',monotonic=time.monotonic(),pid=os.getpid())),flush=True)
    uvicorn.run(app, host='127.0.0.1', port=int(sys.argv[2]),
                access_log=False, log_level='warning')
```

### `tests/test_gateway_service.py`

```python
"""AGW-M02: public wire and real durable-worker ownership, synthetic inputs only."""
import base64
from contextlib import contextmanager
from copy import deepcopy
from fractions import Fraction
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time

import httpx
import pytest

from assessment_policy import PROMPT
from tests.test_durable_processing import PausedWorker, OWNER, OFFICER
from tests.test_evidence_intake import photo
from tests.test_gemini_assessment import output

MODEL = 'gpt-5.4-2026-03-05'
TOKEN = 'c3ludGhldGljLXNlcnZpY2UtdG9rZW4tMzItYnl0ZXM'
SELECTION = dict(provider='openai', model=MODEL,
                 request_profile_version='agw-openai-responses-v2',
                 media_profile_version='agw-openai-frames-v2')
ENVELOPE = set('contract_version correlation_id attempt_id attempt_number evidence_revision '
    'gateway_request_id provider model model_version prompt_version policy_version '
    'legal_reference_version request_profile_version media_profile_version received_at '
    'completed_at timings_ms provider_request_id media_coverage usage billing_state assessment error'.split())


def request_body():
    return dict(contract_version='agw-v1', correlation_id='1'*32, attempt_id='2'*32,
        attempt_number=1, evidence_revision=1, selection=deepcopy(SELECTION),
        prompt=dict(version='asor-prompt-v1', text=PROMPT, policy_version='asor-relevance-v1',
                    legal_reference_version='asor-in-national-2026-11-08-v1'),
        context=dict(reported_category='helmet', location='PRIVATE_CONTEXT',
                     vehicle_number='TEST01', description=None),
        evidence=[dict(media_id='synthetic', mime_type='image/jpeg',
                       data_base64=base64.b64encode(photo()).decode())], budget_ms=10000)


class Service:
    def __init__(self, root):
        self.root = root
        self.mode(assessment=output(['synthetic']))
        service = root / 'source'
        service.mkdir()
        repository = Path(__file__).resolve().parents[1]
        # Deliberate service-source allowlist: application state modules absent.
        names={'ai_gateway_service.py','assessment_policy.py','openai_adapter.py','gemini.py'}
        names.update(path.name for path in repository.glob('agw_*.py'))
        for name in sorted(names):
            if (repository/name).exists():
                shutil.copy2(repository/name, service/name)
        shutil.copy2(Path(__file__).with_name('agw_service_child.py'), service/'child.py')
        assert not any((service/name).exists() for name in
                       ('app.py', 'bootstrap.py', 'durable.py', 'intake.py', 'roadwatch.db'))
        with socket.socket() as reservation:
            reservation.bind(('127.0.0.1', 0))
            port = reservation.getsockname()[1]
        self.url = f'http://127.0.0.1:{port}'
        environment = {k:v for k,v in os.environ.items() if not any(word in k.upper()
            for word in ('KEY','TOKEN','OPENAI','GEMINI','GOOGLE','DATABASE','ROADWATCH','AI_'))}
        environment.update(AI_GATEWAY_TOKEN=TOKEN, AI_PROVIDER='openai', OPENAI_MODEL=MODEL,
                           OPENAI_API_KEY='synthetic-provider-key', PYTHONDONTWRITEBYTECODE='1')
        self.log = (root/'service.log').open('w', encoding='utf-8')
        self.child = subprocess.Popen([sys.executable, '-B', 'child.py', str(root), str(port)],
            cwd=service, env=environment, stdout=self.log, stderr=subprocess.STDOUT)
        self.client = httpx.Client(base_url=self.url, timeout=15, follow_redirects=False,
                                   headers={'Authorization': 'Bearer '+TOKEN}, trust_env=False)
        deadline = time.monotonic()+10
        while time.monotonic()<deadline and self.child.poll() is None:
            try:
                self.client.get('/__readiness__')
                self.log.write(json.dumps(dict(event='parent-ready',monotonic=time.monotonic(),
                    child_pid=self.child.pid,parent_pid=os.getpid()))+'\n'); self.log.flush()
                return
            except httpx.ConnectError:
                time.sleep(.02)
        self.close()
        raise AssertionError('Service harness did not bind; pid='+str(self.child.pid)+
            ' returncode='+str(self.child.returncode)+': '+(root/'service.log').read_text())

    def mode(self, **value):
        (self.root/'mode.json').write_text(json.dumps(value), encoding='utf-8')

    def calls(self):
        file = self.root/'provider.jsonl'
        return [json.loads(line) for line in file.read_text().splitlines()] if file.exists() else []

    def post(self, body=None, **kwargs):
        return self.client.post('/v1/assessments', json=body or request_body(), **kwargs)

    def positive(self):
        response = self.post()
        assert response.status_code == 200, 'SEPARATE_HTTP_ASSESSMENT_MISSING'
        value = response.json()
        assert set(value) == ENVELOPE
        assert value['assessment'] and value['error'] is None
        assert value['model'] == MODEL and value['model_version'] == 'provider-reported-snapshot'
        assert value['request_profile_version'] == SELECTION['request_profile_version']
        assert value['provider_request_id'] == 'req_synthetic'
        assert self.calls(), 'HTTP traversal did not invoke controlled provider'
        return value

    def close(self):
        self.client.close()
        self.child.terminate()
        try:
            self.child.wait(8)
        except subprocess.TimeoutExpired:
            self.child.kill(); self.child.wait(5)
        self.log.close()
        assert self.child.poll() is not None


@pytest.fixture(scope='module')
def service_process(tmp_path_factory):
    root=tmp_path_factory.mktemp('service')
    current=Service(root)
    try:
        yield current
    finally:
        current.close()


@pytest.fixture
def service(service_process):
    current=service_process
    deadline=time.monotonic()+10
    while (current.root/'provider-active').exists() and time.monotonic()<deadline:
        time.sleep(.01)
    assert not (current.root/'provider-active').exists(),'Previous controlled provider did not drain'
    current.mode(assessment=output(['synthetic']))
    calls=current.root/'provider.jsonl'
    if calls.exists(): calls.unlink()
    yield current


def test_separate_image_wire_and_safe_trace(service):
    value=service.positive()
    wire=service.calls()[0]
    assert wire['model']==MODEL and wire['store'] is False
    assert wire['reasoning']=={'effort':'medium'} and wire['max_output_tokens']==8192
    assert wire['text']['format']['strict'] is True
    assert not set(wire)&{'tools','background','stream'}
    assert PROMPT in wire['instructions']
    assert value['media_coverage'][0]['complete'] is True
    assert value['media_coverage'][0]['sampled_timestamps_ms']==[]
    assert value['usage']==dict(input_tokens=23,cached_input_tokens=0,output_tokens=11,
                                thinking_tokens=3,total_tokens=34,source='provider')
    assert set(value['timings_ms'])==set('receive validation preparation provider normalization total'.split())
    assert all(type(v) is int and v>=0 for v in value['timings_ms'].values())
    assert value['received_at'].endswith('Z') and value['completed_at']>=value['received_at']
    logs=(service.root/'service.log').read_text()
    assert value['gateway_request_id'] in logs and value['correlation_id'] in logs
    assert all(secret not in logs for secret in (TOKEN,'synthetic-provider-key','PRIVATE_CONTEXT',PROMPT))
    assert not list(service.root.glob('**/*.db'))


@pytest.mark.parametrize('case,status,code',[
    ('auth',401,'UNAUTHORIZED'),('query',400,'INVALID_REQUEST'),
    ('unknown',400,'INVALID_REQUEST'),('boolean',400,'INVALID_REQUEST'),
    ('duplicate',400,'INVALID_REQUEST'),('base64',400,'INVALID_REQUEST'),
    ('count',413,'REQUEST_TOO_LARGE'),('prompt',409,'PROMPT_INCOMPATIBLE'),
    ('selection',409,'SELECTION_INCOMPATIBLE'),('method',405,'METHOD_NOT_ALLOWED'),
    ('encoding',415,'UNSUPPORTED_MEDIA_TYPE'),('decode',422,'EVIDENCE_UNAVAILABLE')])
def test_rejection_partitions(service,case,status,code):
    service.positive()  # Proves the negative assertions below are not vacuous.
    body=request_body(); kwargs={}; method='POST'; path='/v1/assessments'
    if case=='auth':
        kwargs=dict(content=b'PRIVATE_INVALID_JSON',headers={'Authorization':'Bearer wrong'})
    elif case=='query': path+='?forbidden=1'
    elif case=='unknown': body['points']=100
    elif case=='boolean': body['attempt_number']=True
    elif case=='duplicate': kwargs['content']=json.dumps(body)[:-1]+',"budget_ms":10000}'
    elif case=='base64': body['evidence'][0]['data_base64']='YQ'
    elif case=='count': body['evidence']=[dict(body['evidence'][0],media_id=f'x{i}') for i in range(17)]
    elif case=='prompt': body['prompt']['text']+=' altered'
    elif case=='selection': body['selection']['model']='gpt-6.1-terra'
    elif case=='method': method='GET'
    elif case=='encoding': kwargs['headers']={'Content-Encoding':'gzip'}
    elif case=='decode': body['evidence'][0]['data_base64']=base64.b64encode(b'not-image').decode()
    if 'content' not in kwargs: kwargs['json']=body
    response=service.client.request(method,path,**kwargs)
    assert response.status_code==status
    value=response.json(); assert set(value)==ENVELOPE
    assert value['error']['code']==code and value['assessment'] is None
    assert value['billing_state']=='not-invoked' and len(service.calls())==1
    assert 'PRIVATE_INVALID_JSON' not in response.text


@pytest.mark.parametrize('mode,code', [('refusal','MODEL_REFUSAL'),('invalid','INVALID_MODEL_OUTPUT')])
def test_output_failure_retains_independent_usage(service,mode,code):
    service.positive()
    assessment=output(['synthetic'])
    if mode=='invalid': assessment['points']=100
    service.mode(assessment=assessment,refusal=mode=='refusal',usage={
        'input_tokens':23,'input_tokens_details':{'cached_tokens':True},
        'output_tokens':11,'output_tokens_details':{},'total_tokens':34})
    response=service.post(); assert response.status_code==502
    value=response.json(); assert value['error']['code']==code
    assert value['usage']==dict(input_tokens=23,cached_input_tokens=None,output_tokens=11,
                               thinking_tokens=None,total_tokens=34,source='partial')
    assert value['billing_state']=='reported' and value['assessment'] is None
    assert len(service.calls())==2  # No repair inference.
    assert 'PRIVATE_REFUSAL' not in response.text


def test_v2_video_actual_pts_and_incomplete_referral(service,tmp_path):
    service.positive()
    from tests.test_gateway_openai import video_fixture
    video,times=video_fixture(tmp_path)
    # Fixture PTS are exact milliseconds; target arithmetic remains rational.
    targets=[Fraction(times[0])+Fraction(times[-1]-times[0])*i/31 for i in range(32)]
    chosen=sorted({min(times,key=lambda stamp:(abs(Fraction(stamp)-target),stamp)) for target in targets})
    assert len(times)==40 and len(chosen)==31  # 32 targets deduplicate one source index.
    body=request_body()
    body['evidence'].append(dict(media_id='video',mime_type='video/mp4',
        data_base64=base64.b64encode(video).decode()))
    assessment=output(['synthetic','video'],kinds=['image','video'])
    assessment['observations'][1].update(start_ms=chosen[0],end_ms=chosen[0])
    assessment['attachment_relevance'][1]['relevance']='uncertain'
    assessment['recommendation']='needs-human-judgment'
    service.mode(assessment=assessment)
    response=service.post(body); assert response.status_code==200
    coverage=response.json()['media_coverage']
    assert [entry['media_id'] for entry in coverage]==['synthetic','video']
    assert coverage[1]['mode']=='sampled-video' and coverage[1]['complete'] is False
    assert coverage[1]['sampled_timestamps_ms']==chosen
    assert coverage[1]['duration_ms']>=chosen[-1]
    assert 'audio' in ' '.join(coverage[1]['limitations']).lower()
    images=[part for item in service.calls()[-1]['input'] for part in item['content']
            if part['type']=='input_image']
    assert len(images)==32 and all(part['detail']=='high' for part in images)


def test_absolute_budget_and_terminal_scratch_cleanup(service):
    service.positive()
    service.mode(assessment=output(['synthetic']),delay=4)
    body=request_body(); body['budget_ms']=3000
    started=time.monotonic(); response=service.post(body)
    assert response.status_code==504
    assert time.monotonic()-started<3
    value=response.json()
    assert value['error']['code']=='ATTEMPT_TIMEOUT' and value['error']['retryable'] is True
    assert value['assessment'] is None and value['billing_state']=='unknown'
    assert not list((service.root/'scratch').rglob('*'))
    assert len(service.calls())==2  # One dispatch, no nested retries.


@contextmanager
def application_runtime(runtime_factory,monkeypatch,service):
    import app as application
    monkeypatch.setattr(application,'ai_worker_factory',lambda path:PausedWorker())
    for key,value in dict(AI_GATEWAY_URL=service.url,AI_GATEWAY_TOKEN=TOKEN,
        AI_PROVIDER='openai',OPENAI_MODEL=MODEL,AI_ATTEMPT_TIMEOUT_SECONDS='30',
        AI_RETRY_BASE_SECONDS='1',AI_RETRY_MAX_DELAY_SECONDS='2',
        ROADWATCH_REVIEWER_TOKEN='durable-reviewer').items():
        monkeypatch.setenv(key,value)
    monkeypatch.delenv('OPENAI_API_KEY',raising=False)
    monkeypatch.delenv('GEMINI_API_KEY',raising=False)
    with runtime_factory() as runtime:
        yield runtime


def submit(runtime):
    client,db,root=runtime
    upload=client.post('/api/media/upload',headers=OWNER,
        files={'media_file':('synthetic.jpg',photo(),'image/jpeg')})
    assert upload.status_code==201
    media=upload.json()['media_id']
    response=client.post('/api/reports',headers=OWNER,json=dict(violation_type='helmet',
        vehicle_number='TEST01',location='PRIVATE_CONTEXT',media_ids=[media]))
    assert response.status_code==201
    return response.json(),media


def run_attempt(runtime,job):
    import durable
    worker=durable.ai_worker_factory(runtime[2]/'roadwatch.db')
    worker.assess_job(job)  # Real worker, claim, bytes authorization, HTTP and persistence.
    return worker


def assert_authority(runtime,report):
    row=runtime[1].execute('SELECT status,provisional_points FROM reports WHERE id=?',(report,)).fetchone()
    assert tuple(row)==('awaiting-review',0)


def test_application_worker_owns_wire_and_persistence(service,runtime_factory,monkeypatch):
    with application_runtime(runtime_factory,monkeypatch,service) as runtime:
        body,media=submit(runtime); job=body['ai']['job_id']
        service.mode(assessment=output([media]))
        run_attempt(runtime,job)
        assert len(service.calls())==1,'APPLICATION_WORKER_DID_NOT_TRAVERSE_GATEWAY_HTTP'
        row=runtime[1].execute('SELECT state,attempt_count,assessment FROM ai_jobs WHERE id=?',(job,)).fetchone()
        assert row[0:2]==('completed',1)
        result=json.loads(row[2])['assessment']
        assert result['model']==MODEL and result['job_id']==job
        assert result['media_coverage'][0]['media_id']==media
        assert_authority(runtime,body['report_id'])


def test_restart_transients_consume_three_attempts_without_fallback(service,runtime_factory,monkeypatch):
    with application_runtime(runtime_factory,monkeypatch,service) as runtime:
        body,media=submit(runtime); job=body['ai']['job_id']
        service.mode(status=429)
        for number in range(1,4):
            worker=run_attempt(runtime,job)
            assert len(service.calls())==number,'APPLICATION_HTTP_RETRY_OWNERSHIP_MISSING'
            attempt=runtime[1].execute('SELECT state,failure_code FROM ai_attempts WHERE job_id=? AND number=?',(job,number)).fetchone()
            assert tuple(attempt)==('failed','PROVIDER_TRANSIENT')
            with worker.store.transaction() as conn:
                conn.execute('UPDATE ai_jobs SET next_attempt_at=0 WHERE id=?',(job,))
            worker.store.recover(worker.clock())
        run_attempt(runtime,job)
        row=runtime[1].execute('SELECT state,attempt_count,failure_code FROM ai_jobs WHERE id=?',(job,)).fetchone()
        assert tuple(row)==('failed',3,'ATTEMPTS_EXHAUSTED') and len(service.calls())==3
        assert_authority(runtime,body['report_id'])
```

### `tests/verify_gateway_service.py`

```python
"""Bounded source-only AGW-M02 verification. No live/private inputs."""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

SOURCE=Path(__file__).resolve().parents[1]
TASK=Path(r'C:\Users\avina\AppData\Local\Temp\asor-agw-m02-verify-20261111')
ROOT_FILES=('ai_gateway_service.py','app.py','assessment_policy.py','auth_utils.py','bootstrap.py','controls_http.py',
    'controls_operator.py','durable.py','gateway.py','gemini.py','intake.py','media.py',
    'openai_adapter.py','runtime_controls.py','pytest.ini')
TEST_FILES=('conftest.py','__init__.py','agw_service_child.py','test_gateway_service.py',
    'test_durable_processing.py','test_evidence_intake.py','test_gemini_assessment.py',
    'test_gateway_openai.py','verify_gateway_service.py')
PRESERVED=('tests/test_durable_processing.py::test_concurrent_claims_and_recovered_stale_completion_publish_once',
           'tests/test_durable_processing.py::test_obsolete_evidence_completion_is_superseded')


def files():
    selected=[SOURCE/name for name in ROOT_FILES]+[SOURCE/'tests'/name for name in TEST_FILES]
    selected.extend(SOURCE.glob('agw_*.py'))
    selected.append(SOURCE/'docs/.ai/ai-screening-officer-review/MP4-Diagnostics-2026-11-11/decoder_carrier.py')
    for directory in ('static','templates'):
        selected.extend(p for p in (SOURCE/directory).rglob('*') if p.is_file() and
                        p.suffix in ('.html','.css','.js','.json','.txt','.svg'))
    return sorted(p for p in selected if p.is_file())


def manifest(selected):
    return {str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in selected}


def main():
    assert sys.argv[1:] in (['--red'],['--green'])
    mode=sys.argv[1][2:]
    assert not TASK.exists(),'Refuse to reuse or erase an existing task folder'
    assert TASK.parent.resolve()==Path(r'C:\Users\avina\AppData\Local\Temp').resolve()
    TASK.mkdir(); copy=TASK/'repository'; copy.mkdir(); temporary=TASK/'temporary'; temporary.mkdir()
    selected=files(); before=manifest(selected)
    # Other root entries, including private files/directories: metadata only.
    metadata={p.name:(p.is_dir(),p.stat().st_size,p.stat().st_mtime_ns) for p in SOURCE.iterdir() if p not in selected}
    (TASK/'protected-before.json').write_text(json.dumps(dict(source=before,other_metadata=metadata)))
    carrier=None
    try:
        for source in selected:
            target=copy/source.relative_to(SOURCE); target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)
        assert not any((copy/name).exists() for name in ('.env','.local','.git','roadwatch.db','media_store'))
        for source in copy.rglob('*.py'):
            compile(source.read_text(encoding='utf-8-sig'),str(source),'exec')
        env={k:v for k,v in os.environ.items() if not any(word in k.upper() for word in
            ('OPENAI','GEMINI','GOOGLE','ANTHROPIC','KEY','TOKEN','AI_','ROADWATCH','DATABASE','OTEL','OIDC'))}
        env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
                   TEMP=str(temporary),TMP=str(temporary),TMPDIR=str(temporary))
        if not (shutil.which('ffmpeg') and shutil.which('ffprobe')):
            image='sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de'
            carrier=subprocess.check_output(['docker','run','-d','--rm','--network','none','--pull','never',
                '--entrypoint','/bin/sleep',image,'600'],text=True,timeout=30).strip()
            info=json.loads(subprocess.check_output(['docker','inspect',carrier],text=True,timeout=10))[0]
            assert info['Mounts']==[] and info['HostConfig']['NetworkMode']=='none'
            helper=SOURCE/'docs/.ai/ai-screening-officer-review/MP4-Diagnostics-2026-11-11/decoder_carrier.py'
            shutil.copy2(helper,TASK/'decoder_carrier.py')
            binary=TASK/'bin'; binary.mkdir()
            for tool in ('ffmpeg','ffprobe'):
                subprocess.run(['docker','exec',carrier,'/usr/bin/'+tool,'-version'],check=True,
                               capture_output=True,timeout=10)
                wrapper=binary/(tool+'.cmd')
                wrapper.write_text('@"'+sys.executable+'" "'+str(TASK/'decoder_carrier.py')+'" '+tool+' %*\n')
                assert Path(shutil.which(tool,path=str(binary))).resolve()==wrapper.resolve()
            env.update(ASOR_DECODER_CARRIER=carrier,PATH=str(binary)+os.pathsep+env['PATH'])
        groups=[('new',['tests/test_gateway_service.py'],mode),('preserved',list(PRESERVED),'green')]
        if mode=='green':
            groups.append(('state-repeat',['tests/test_gateway_service.py::test_application_worker_owns_wire_and_persistence',
                'tests/test_gateway_service.py::test_restart_transients_consume_three_attempts_without_fallback'],'green'))
        for label,nodes,expected in groups:
            log=TASK/(label+'.log'); xml=TASK/(label+'.xml')
            command=[sys.executable,'-B','-m','pytest','-p','pytest_asyncio.plugin','-vv','--tb=short',
                     '--junitxml='+str(xml),'--basetemp='+str(temporary/label),*nodes]
            with log.open('w',encoding='utf-8') as output:
                child=subprocess.Popen(command,cwd=copy,env=env,stdout=output,stderr=subprocess.STDOUT)
                try:
                    returncode=child.wait(timeout=180)
                except subprocess.TimeoutExpired:
                    subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],check=True,
                                   capture_output=True,timeout=15)
                    child.wait(timeout=5)
                    raise AssertionError('Verification timeout is not RED')
            cases=ET.parse(xml).findall('.//testcase')
            assert len(cases)==(19 if label=='new' else 2),(label,len(cases))
            assert not any(case.find('error') is not None or case.find('skipped') is not None for case in cases)
            failures=[case for case in cases if case.find('failure') is not None]
            if expected=='red':
                assert returncode==1 and len(failures)==19
                for case in failures:
                    detail=case.find('failure').text or ''
                    assert any(marker in detail for marker in ('SEPARATE_HTTP_ASSESSMENT_MISSING',
                        'APPLICATION_WORKER_DID_NOT_TRAVERSE_GATEWAY_HTTP','APPLICATION_HTTP_RETRY_OWNERSHIP_MISSING')),detail
            else:
                assert returncode==0 and not failures,log.read_text()
            print(label,len(cases),'intended failures' if expected=='red' else 'passes',flush=True)
        assert manifest(selected)==before,'Protected source changed'
        after_metadata={p.name:(p.is_dir(),p.stat().st_size,p.stat().st_mtime_ns) for p in SOURCE.iterdir() if p not in selected}
        assert after_metadata==metadata,'Other root metadata changed'
    finally:
        if carrier:
            subprocess.run(['docker','rm','-f',carrier],check=True,capture_output=True,timeout=15)
        # Retain only safe logs/XML/manifests and bounded synthetic decoder diagnostics.
        for owned in (copy,temporary,TASK/'bin'):
            if owned.exists():
                assert owned.resolve().is_relative_to(TASK.resolve())
                shutil.rmtree(owned)
    print('Owned processes/carrier removed; copied source and synthetic state deleted',flush=True)


if __name__=='__main__':
    main()
```

## Execution Steps

1. Read this sole Human Review status and the current Plan; stop unless this exact artifact records user approval. Confirm no in-scope filename already exists; preserve baseline dirt and all private metadata.
2. Create only the three exact files above; do not change production/config/dependencies. Run the verifier from explicit owned native Temp cwd with root-venv interpreter and loopback execution authorization; no root fixtures/live calls.
3. Record named JUnit failures/passes, any errors/skips/timeouts and exact commands. Only all19intended assertion failures with the two affected passes constitute RED. Infrastructure failures stop; never retry unchanged failures, raise limits, weaken assertions or repair unrelated tests.
4. After verified execution update M02 execution status/evidence only. No013 planning/source execution follows automatically.

## Acceptance / Completion Criteria

- Exactly the three authorized new test/harness files; no production/config/dependency or pre-existing test modification (except milestone execution status in Plan).
- All19new outcomes reach ordinary intended missing-service/worker-HTTP assertions on the actual applied baseline; no skip/import/collection/readiness timeout qualifies.
- Two named affected durable guard cases pass. Source allowlist hashes and other-root metadata remain equal; owned service/decoder children reaped and copied state removed.
- Report precise scope and untested limits above, historic MP4 unknown cause/deferred Gemini, and distinguish planning probe evidence from milestone evidence. Human approval never inferred.

## Verification

### Commands

Use the root `.venv/Scripts/python.exe` interpreter. Explicit cwd: `C:\Users\avina\AppData\Local\Temp`; execution needs approved native loopback access. The verifier refuses existing owned target `C:\Users\avina\AppData\Local\Temp\asor-agw-m02-verify-20261111`; it never erases a pre-existing directory.

```powershell
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' -B 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\tests\verify_gateway_service.py' --red
```

Logs/XML/protection manifests stay only in the owned verification directory. Each pytest group has180s; each service readiness10s; no automatic broad-suite or repeat19planning run. GREEN execution may reuse `--green`, which repeats only its two state cases without cleaning between groups. No SDK/dependency installation/version selection.

### Affected Tests

Found by `rg` over factory/JobStore and current Plan named test modules: `test_concurrent_claims_and_recovered_stale_completion_publish_once` and `test_obsolete_evidence_completion_is_superseded` in `tests/test_durable_processing.py`. These protect claim/revision state accepted by the new HTTP result path. No Gemini suite, old209/96inventory or unchanged full policy matrix. Test helper imports are code reuse, not automatic selection.

### Expected Evidence

Expected / Predicted — Not Yet Verified milestone evidence: `new19intendedfailures`; `preserved2passes`; zero errors/skips/timeouts; source/metadata guard equality; cleanup. The new cases fail for absent HTTP200service or absent worker traversal, not arbitrary missing Python imports. Current Plan assigns affected state preservation to the boundary selection; preserved cases are never RED evidence for new behavior.

### Planning-Time Dry Run

Disposable literal root from first setup: `C:\Users\avina\AppData\Local\Temp\asor-agw-m02-plan-20261111`; no `$env:TEMP` lookup was used to choose it. Source copy contained explicit root modules and synthetic test/public assets only. Real keys/media/DB contents not read.

Commands actually run (planning-only, not milestone evidence):

- Root-venv `-m compileall -q .` in initial disposable copy: successful; no checkout bytecode/source changed. Final selected Python compiled again by the final driver.
- `-m pytest -p pytest_asyncio.plugin tests/test_gateway_service.py -vv --tb=short --junitxml=../red.xml`:15intendedfailures+2infrastructure missing controls_operator/auth helpers; this was not RED completion. Corrected explicit source allowlist.
- Same command with `../red-final.xml`, frozen19inventory:19ordinary intendedfailures,37.88s; no errors/skips.
- Initial failfast probe `-vv -x --tb=short --basetemp=<owned>/probe --junitxml=<owned>/probe.xml`:3passes then child failed to bind in10s with empty log; no cause established; remaining cases NOT RUN. This prompted a specific harness correction, not timeout increase or unchanged retry: module-scoped child, per-test provider drain/reset and safe child/import/start/ready timestamps+PID/returncode diagnostics.
- Final corrected module fixture: `-B -m pytest -p pytest_asyncio.plugin -vv --tb=short --basetemp=C:\Users\avina\AppData\Local\Temp\asor-agw-m02-plan-20261111\temporary\red-corrected --junitxml=C:\Users\avina\AppData\Local\Temp\asor-agw-m02-plan-20261111\red-corrected.xml tests/test_gateway_service.py`:19intended assertion failures,6.15s,noerrors/skips.
- Corrected-fixture probe with `-x` and owned probe-corrected paths:15passes,then VFR test-design precondition failed (32rational targets deduplicated to31indices). Contract requires deduplication; corrected fixture assertion to31 and provider image count to32 (one still+31frames), retaining exact timestamp equality. No production behavior or decoder repair.
- Corrected video only, `-B -m pytest -p pytest_asyncio.plugin -vv --tb=short --basetemp=<literal-root>\temporary\red-video-corrected --junitxml=<literal-root>\red-video-corrected.xml tests/test_gateway_service.py::test_v2_video_actual_pts_and_incomplete_referral`:1intended404/200assertion failure. The15already-passing assertions were unchanged.
- Final probe `-B -m pytest -p pytest_asyncio.plugin -vv -x --tb=short --basetemp=<literal-root>\temporary\probe-remaining --junitxml=<literal-root>\probe-remaining.xml` selecting `test_v2_video_actual_pts_and_incomplete_referral`, `test_absolute_budget_and_terminal_scratch_cleanup`, `test_application_worker_owns_wire_and_persistence`, `test_restart_transients_consume_three_attempts_without_fallback` in the new module:4passes,15.58s. Thus all19final assertions have passing probe evidence; no full/repeat suite was run. `<literal-root>` means exactly the root named above, not environment TEMP.
- Pinned carrier direct preflight reported FFmpeg/FFprobe7.1.5-0+deb13u1; inspect asserted networknone/zero mounts. Video fixture decoded successfully before carrier lifetime600s; every driver removed its carrier in finally.
- The three exact proposed files compile. Integrated final verifier wrapper and its2affectedpreservation nodes were NOT RUN during planning; tests were exercised by equivalent bounded disposable drivers. Predicted wrapper/source-manifest and affected-pass evidence must be obtained at approved execution, not represented as already verified.

Probe scope: temporary stateless FastAPI behavior implemented auth/DTO/error/usage/media/provider mechanics and reused the real common validator; worker probe used actual JobStore claim/load_evidence/fail/complete/recover over the real isolated app schema and actual gateway HTTP. No mock returned application state. The probe is not a production design, executable013proposal, approval or full contract implementation; only assertions reached/passed are soundness evidence. Probe code is not included as production proposed code. No live provider execution occurred.

Exact proposed-file SHA256: `{"agw_service_child.py": "70576034ac1d0ff16d938d88c26aece5a58e426052fd2867f4cf8fe5ff988809", "test_gateway_service.py": "cfef04e1b6a01d4dc1ec7fdadd1fa35c5466bb6e197277f1a031c65d6254e8e5", "verify_gateway_service.py": "79e16b914e1ddefdc3b9ac02927918db330e0bb79335e0f2081454ad7afac6e7"}`.

Cleanup: owned service children reaped by fixtures; carriers removed in driver finally. Disposable repository, pytest synthetic DB/media roots and wrapper directory removed after recording this evidence. Safe logs/XML and diagnostic scripts remain only in the literal owned Temp root for review; no copied application or synthetic durable state remains.

## Risks

Representative tests cannot establish all resource/security/disconnect invariants; the table makes those gaps reviewable. The controlled blocking provider may continue after local timeout and drains before next case; scratch emptiness does not prove remote provider cancellation. Worker new-instance recovery proves durable attempts in one app process, not process-crash ambiguity. Historical MP4 rejection and Gemini402 remain unresolved/deferred; no full-suite success claim. Service factory/source-closure choices bind the later exact013proposal and need human review.

## Pre-authorized Contingencies

None. Different source seams/files, dependency changes, limits, inventory or assertions return to planning for review.

## Rollback / Recovery

Remove only the three newly created files after checking they contain this milestone's exact bytes; keep all baseline dirt/private backups. Never reset/clean/checkout the repository. Kill/reap only owned children and remove only resolved descendants of the explicitly named owned Temp directory.

## Explicitly Out of Scope

Production/source/config/dependency edits, keys/private media/DB reads, live providers, staging/commits/publication, unrelated repairs, broad/Gemini suites, migration and next-milestone execution. Real R05image/video acceptance belongs exclusively to M04.

## Human Review

Status: Executed — valid RED 2026-11-11. Approved by user on 2026-11-11 (America/Chicago), in response to the request to apply and execute this specific test plan. AGW-M02 only; no production implementation authorized. See [execution evidence](AGW-M02-Execution-2026-11-11.md): 19 intended failures and 2 preserved passes, exact verifier exit 0.
