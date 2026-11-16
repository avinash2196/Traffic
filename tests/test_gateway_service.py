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
from tests.agw_provider_child import Provider, stop_process
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
        shutil.copy2(Path(__file__).with_name('agw_provider_child.py'), service/'agw_provider_child.py')
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
        self.provider = Provider(root, environment)
        self.log = (root/'service.log').open('w', encoding='utf-8')
        self.child = subprocess.Popen([sys.executable, '-B', 'child.py', str(root), str(port), self.provider.url],
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
        try:
            stop_process(self.child)
        finally:
            try:
                self.provider.close()
            finally:
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
