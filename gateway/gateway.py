"""Application-owned evidence authorization, one durable queue and gateway HTTP dispatch."""
import base64
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import time
from uuid import uuid4

import httpx
import durable as d
from assessment_policy import PROMPT, Failure, parse_json
from agw_protocol import (BoundaryError, COUNTERS, ERRORS, PROFILES, VERSIONS, local_url,
                          safe_id, token_valid, usage as normalize_counters)
from intake import media_path

RANGES = {'AI_ATTEMPT_TIMEOUT_SECONDS': (10, 600), 'AI_RETRY_BASE_SECONDS': (1, 60),
          'AI_RETRY_MAX_DELAY_SECONDS': (2, 3600)}
LOG = logging.getLogger('ai.application')


def settings(provider=None):
    provider = os.getenv('AI_PROVIDER', 'openai') if provider is None else provider
    profile = PROFILES.get(provider)
    value = dict(VERSIONS, provider=provider, valid=False)
    if profile is None:
        return value
    model, request_profile, media_profile = profile
    value.update(model=os.getenv(provider.upper() + '_MODEL', model),
                 request_profile_version=request_profile, media_profile_version=media_profile)
    for key, default in (('AI_ATTEMPT_TIMEOUT_SECONDS', '120'), ('AI_RETRY_BASE_SECONDS', '5'),
                         ('AI_RETRY_MAX_DELAY_SECONDS', '300')):
        raw = os.getenv(key, default)
        if not re.fullmatch(r'[0-9]+', raw):
            return value
        value[key] = int(raw)
    value['valid'] = True
    value['valid'] = valid_snapshot(value)
    return value


def snapshot_provider(value):
    if type(value) is not dict:
        return None
    if 'provider' in value:
        return value['provider']
    legacy = set(VERSIONS) | set(RANGES) | {'model', 'valid'}
    return 'gemini' if set(value) == legacy and value.get('model') == PROFILES['gemini'][0] else None


def valid_snapshot(value):
    if type(value) is not dict or value.get('valid') is not True:
        return False
    provider = snapshot_provider(value)
    if type(provider) is not str or provider not in PROFILES:
        return False
    model, request_profile, media_profile = PROFILES[provider]
    if value.get('model') != model or any(value.get(k) != v for k, v in VERSIONS.items()):
        return False
    if 'provider' in value and (value.get('request_profile_version') != request_profile
                               or value.get('media_profile_version') != media_profile):
        return False
    if any(type(value.get(key)) is not int or not low <= value[key] <= high
           for key, (low, high) in RANGES.items()):
        return False
    return value['AI_RETRY_MAX_DELAY_SECONDS'] >= 2 * value['AI_RETRY_BASE_SECONDS']


def remaining(deadline):
    value = deadline - time.monotonic()
    if value <= 0:
        raise Failure('ATTEMPT_TIMEOUT', True)
    return value


def read_authorized_evidence(path, job, deadline):
    with sqlite3.connect(path, timeout=min(2, remaining(deadline))) as conn:
        conn.row_factory = sqlite3.Row
        report = dict(conn.execute('SELECT * FROM reports WHERE id=?', (job['report_id'],)).fetchone())
        media = [dict(row) for row in conn.execute(
            'SELECT * FROM media WHERE report_id=? ORDER BY attachment_position', (report['id'],))]
    if not media or len(media) > 16 or report['evidence_revision'] != job['evidence_revision']:
        raise Failure('EVIDENCE_UNAVAILABLE')
    for item in media:
        remaining(deadline)
        if item['owner_citizen_id'] != report['citizen_id']:
            raise Failure('EVIDENCE_UNAVAILABLE')
        with media_path(item).open('rb') as stream:
            data = stream.read(10 * 1024 * 1024 + 1)
        if not data or len(data) > 10 * 1024 * 1024 or hashlib.sha256(data).hexdigest() != item['sha256_hash']:
            raise Failure('EVIDENCE_UNAVAILABLE')
        item['bytes'] = data
        remaining(deadline)
    return report, media


_EVIDENCE_CHILD = r"""
import base64,json,sys
value=json.loads(sys.stdin.buffer.read())
sys.path.insert(0,value['source'])
from gateway import read_authorized_evidence
try:
    report,media=read_authorized_evidence(value['database'],value['job'],value['deadline'])
    for item in media:
        item['bytes']=base64.b64encode(item['bytes']).decode('ascii')
    result={'report':report,'media':media}
except Exception:
    result={'failure':'EVIDENCE_UNAVAILABLE'}
sys.stdout.write(json.dumps(result))
"""


def load_evidence(path, job, deadline):
    payload=json.dumps(dict(source=str(Path(__file__).resolve().parent), database=str(path),
                            job=job, deadline=deadline)).encode('utf-8')
    process=None
    try:
        environment={key:value for key,value in os.environ.items() if not any(word in key.upper()
                     for word in ('KEY','TOKEN','OPENAI','GEMINI','GOOGLE','DATABASE','ROADWATCH','AI_'))}
        process=subprocess.Popen([sys.executable,'-I','-B','-c',_EVIDENCE_CHILD], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=environment)
        output,_=process.communicate(payload, timeout=remaining(deadline))
        remaining(deadline)
        value=parse_json(output.decode('utf-8'))
        if process.returncode or 'failure' in value:
            raise Failure('EVIDENCE_UNAVAILABLE')
        for item in value['media']:
            item['bytes']=base64.b64decode(item['bytes'])
        return value['report'],value['media']
    except subprocess.TimeoutExpired:
        raise Failure('ATTEMPT_TIMEOUT',True) from None
    finally:
        if process is not None:
            if process.poll() is None:
                if os.name=='nt':
                    subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,timeout=5,check=False)
                else:
                    process.kill()
            process.communicate()


def request_body(job, token, config, report, media, deadline):
    provider = snapshot_provider(config)
    model, request_profile, media_profile = PROFILES[provider]
    budget = min(110000, int(remaining(deadline) * 1000) - 5000)
    if budget < 1000:
        raise Failure('ATTEMPT_TIMEOUT', True)
    return dict(contract_version='agw-v1', correlation_id=hashlib.sha256(('agw:' + job['id']).encode('ascii')).hexdigest()[:32], attempt_id=token['owner'],
        attempt_number=token['number'], evidence_revision=token['evidence_revision'],
        selection=dict(provider=provider, model=model, request_profile_version=request_profile,
                       media_profile_version=media_profile),
        prompt=dict(version=VERSIONS['prompt_version'], text=PROMPT,
                    policy_version=VERSIONS['policy_version'], legal_reference_version=VERSIONS['legal_reference_version']),
        context=dict(reported_category=report['violation_type'], location=report['location'],
                     vehicle_number=report['vehicle_number'], description=report.get('screening_notes')),
        evidence=[dict(media_id=item['id'], mime_type='image/jpeg' if item['mime_type'] == 'image/jpg' else item['mime_type'],
                       data_base64=base64.b64encode(item['bytes']).decode('ascii')) for item in media], budget_ms=budget)


def response_requires(condition):
    if not condition:
        raise Failure('INVALID_MODEL_OUTPUT')


def validate_response_error(value, status):
    error = value['error']
    response_requires((value['assessment'] is None) != (error is None))
    if error is None:
        response_requires(status == 200)
        return
    fields = set('code message retryable stage provider_status retry_after_ms'.split())
    response_requires(type(error) is dict and set(error) == fields)
    response_requires(type(error['code']) is str and error['code'] in ERRORS)
    response_requires(type(error['retryable']) is bool)
    response_requires(ERRORS[error['code']] == (status, error['retryable']))
    response_requires(type(error['message']) is str and bool(error['message'].strip())
                      and len(error['message']) <= 256)
    response_requires(error['stage'] in ('admission', 'validation', 'preparation', 'provider',
                                       'normalization', 'transport'))
    for field, low, high in (('provider_status', 100, 599), ('retry_after_ms', 0, 300000)):
        item = error[field]
        response_requires(item is None or type(item) is int and low <= item <= high)


def validate_response_identity(value, body):
    error = value['error']
    unidentified = error is not None and error['stage'] in ('admission', 'validation', 'transport')
    unidentified = unidentified and value['billing_state'] == 'not-invoked'
    expected = {name: body[name] for name in
                ('correlation_id', 'attempt_id', 'attempt_number', 'evidence_revision')}
    expected.update(body['selection'], **VERSIONS)
    for name, wanted in expected.items():
        actual = value[name]
        if unidentified and actual is None:
            continue
        response_requires(type(actual) is type(wanted) and actual == wanted)
    response_requires(type(value['gateway_request_id']) is str and
                      re.fullmatch('[0-9a-f]{32}', value['gateway_request_id']))
    response_requires(value['model_version'] is None or type(value['model_version']) is str)
    response_requires(value['provider_request_id'] is None or
                      safe_id(value['provider_request_id']) is not None)


def validate_response_times(value):
    from datetime import datetime
    stamps = []
    for name in ('received_at', 'completed_at'):
        stamp = value[name]
        response_requires(type(stamp) is str and re.fullmatch(
            r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z', stamp))
        stamps.append(datetime.fromisoformat(stamp[:-1] + '+00:00'))
    response_requires(stamps[1] >= stamps[0])
    timings = value['timings_ms']
    response_requires(type(timings) is dict and set(timings) ==
                      set('receive validation preparation provider normalization total'.split()))
    response_requires(type(timings['total']) is int and timings['total'] >= 0)
    for duration in timings.values():
        response_requires(duration is None or type(duration) is int and
                          0 <= duration <= timings['total'])


def validate_response_usage(value):
    observed = value['usage']
    response_requires(type(observed) is dict and set(observed) == set(COUNTERS) | {'source'})
    response_requires(normalize_counters(observed) == observed)
    response_requires(value['billing_state'] in ('not-invoked', 'reported', 'unknown'))
    if observed['source'] == 'unavailable':
        response_requires(value['billing_state'] != 'reported')
    else:
        response_requires(value['billing_state'] == 'reported')


def validate_video_coverage(entry, provider):
    response_requires(type(entry['duration_ms']) is int and entry['duration_ms'] >= 0)
    stamps = entry['sampled_timestamps_ms']
    response_requires(type(stamps) is list)
    if provider == 'gemini':
        response_requires(entry['mode'] == 'native-video' and stamps == [] and
                          entry['complete'] is False)
        return
    response_requires(entry['mode'] == 'sampled-video' and 1 <= len(stamps) <= 32)
    response_requires(all(type(stamp) is int and 0 <= stamp <= entry['duration_ms']
                          for stamp in stamps))
    response_requires(all(left < right for left, right in zip(stamps, stamps[1:])))


def validate_response_coverage(value, body):
    coverage = value['media_coverage']
    evidence = body['evidence']
    response_requires(type(coverage) is list and len(coverage) <= len(evidence))
    if value['error'] is None:
        response_requires(len(coverage) == len(evidence))
    fields = set('media_id mode duration_ms sampled_timestamps_ms complete limitations'.split())
    media = []
    for entry, original in zip(coverage, evidence):
        response_requires(type(entry) is dict and set(entry) == fields)
        response_requires(entry['media_id'] == original['media_id'])
        response_requires(type(entry['complete']) is bool)
        limits = entry['limitations']
        response_requires(type(limits) is list and bool(limits) and
                          all(type(text) is str and bool(text.strip()) for text in limits))
        if original['mime_type'].startswith('image/'):
            response_requires(entry['mode'] == 'image' and entry['duration_ms'] is None and
                              entry['sampled_timestamps_ms'] == [] and entry['complete'] is True)
        else:
            validate_video_coverage(entry, body['selection']['provider'])
        media.append(dict(id=original['media_id'], mime_type=original['mime_type'],
                          duration_ms=entry['duration_ms']))
    return media


def validate_response_assessment(value, body, media):
    from assessment_policy import validate
    assessment = value['assessment']
    response_requires(type(assessment) is dict)
    raw = dict(assessment)
    notes = raw['rule_notes']
    fields = set('reference_id applicability note title section url'.split())
    response_requires(type(notes) is list and all(type(note) is dict and set(note) == fields
                                                for note in notes))
    raw['rule_notes'] = [{key: note[key] for key in ('reference_id', 'applicability', 'note')}
                         for note in notes]
    response_requires(validate(raw, media, body['context']['reported_category']) == assessment)
    for entry, attachment in zip(value['media_coverage'], assessment['attachment_relevance']):
        if entry['mode'] != 'sampled-video':
            continue
        if not entry['complete']:
            response_requires(attachment['relevance'] == 'uncertain' and
                              assessment['recommendation'] == 'needs-human-judgment')
        for observation in assessment['observations']:
            if observation['media_id'] == entry['media_id']:
                start, end = observation['start_ms'], observation['end_ms']
                response_requires((start is None and end is None) or
                                  start == end and start in entry['sampled_timestamps_ms'])


def validate_envelope(value, body, status):
    fields = set(('contract_version correlation_id attempt_id attempt_number evidence_revision gateway_request_id '
        'provider model model_version prompt_version policy_version legal_reference_version request_profile_version '
        'media_profile_version received_at completed_at timings_ms provider_request_id media_coverage usage '
        'billing_state assessment error').split())
    try:
        response_requires(type(value) is dict and set(value) == fields)
        response_requires(type(value['contract_version']) is str and value['contract_version'] == 'agw-v1')
        validate_response_error(value, status)
        validate_response_usage(value)
        validate_response_identity(value, body)
        validate_response_times(value)
        media = validate_response_coverage(value, body)
        if value['assessment'] is not None:
            validate_response_assessment(value, body, media)
        return value
    except (KeyError, TypeError, ValueError, IndexError, OverflowError, RecursionError):
        raise Failure('INVALID_MODEL_OUTPUT') from None


class Worker(d.Worker):
    def __init__(self, path):
        super().__init__(d.JobStore(path), dispatch=True)
        self.path = Path(path)

    def assess_job(self, job_id):
        started = time.monotonic()
        token = self.store.claim(job_id, 'gateway-http-worker', self.clock())
        if token is None:
            return
        billing = 'not-invoked'
        correlation = hashlib.sha256(('agw:' + job_id).encode('ascii')).hexdigest()[:32]
        trace = dict(correlation_id=correlation, attempt_id=token['owner'], attempt_number=token['number'],
                     gateway_request_id=None, http_status=None, outcome='technical', stage='attempt', started_at=d.timestamp(self.clock()))
        LOG.warning(json.dumps(trace))
        try:
            with self.store.transaction() as conn:
                job = dict(conn.execute('SELECT * FROM ai_jobs WHERE id=?', (job_id,)).fetchone())
            config = json.loads(job['settings_snapshot'])
            if not valid_snapshot(config):
                raise Failure('PROVIDER_CONFIGURATION')
            deadline = started + config['AI_ATTEMPT_TIMEOUT_SECONDS']
            self.store.deadline = deadline
            url = local_url(os.getenv('AI_GATEWAY_URL', ''))
            service_token = os.getenv('AI_GATEWAY_TOKEN', '')
            if not token_valid(service_token):
                raise Failure('PROVIDER_CONFIGURATION')
            report, media = load_evidence(self.path, job, deadline)
            body = request_body(job, token, config, report, media, deadline)
            http_deadline = deadline - 5
            billing = 'unknown'
            with d.gemini_client_factory() as client:
                response = client.post(url + '/v1/assessments', json=body,
                    headers={'Authorization': 'Bearer ' + service_token},
                    extensions={'asor_deadline': http_deadline}, timeout=httpx.Timeout(remaining(http_deadline), connect=min(2, remaining(http_deadline)), pool=0))
            trace['http_status'] = response.status_code
            value = validate_envelope(parse_json(response.content.decode('utf-8')), body, response.status_code)
            remaining(deadline)
            if not self.store.record_gateway(token, value, self.clock()):
                return
            billing = value['billing_state']
            trace['gateway_request_id'] = value['gateway_request_id']
            if value['error'] is not None:
                error = value['error']
                raise Failure(error['code'], error['retryable'],
                    error['retry_after_ms'] / 1000 if error['retry_after_ms'] is not None else None,
                    diagnostic=(error['provider_status'], error['stage'], 'HTTP_STATUS'))
            assessment = value['assessment']
            assessment.update(id=uuid4().hex, job_id=job_id, evidence_revision=token['evidence_revision'],
                provider=value['provider'], model=value['model'], model_version=value['model_version'],
                **VERSIONS, completed_at=value['completed_at'], media_coverage=value['media_coverage'], late_result=False)
            trace['outcome'] = self.store.complete(token, dict(outcome=assessment['relevance'], recommendation=assessment['recommendation'],
                                            assessment=assessment), self.clock())
            LOG.warning(json.dumps(dict(correlation_id=body['correlation_id'], attempt_id=token['owner'],
                gateway_request_id=value['gateway_request_id'], stage='persistence', outcome='completed')))
        except BoundaryError:
            trace['outcome'] = 'PROVIDER_CONFIGURATION'
            self.record_failure(token, Failure('PROVIDER_CONFIGURATION'), billing)
        except (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError):
            trace['outcome'] = 'PROVIDER_TRANSIENT'
            self.record_failure(token, Failure('PROVIDER_TRANSIENT', True), billing)
        except Failure as error:
            trace['outcome'] = error.code
            self.record_failure(token, error, billing)
        except (sqlite3.Error, TimeoutError):
            trace['outcome'] = 'APP_PERSISTENCE_FAILED'
        except (OSError, ValueError, TypeError, KeyError):
            self.record_failure(token, Failure('PROCESSING_ERROR'), billing)
        finally:
            trace.update(stage='persistence', completed_at=d.timestamp(self.clock()), elapsed_ms=max(0, int((time.monotonic() - started) * 1000)), billing_state=billing)
            try:
                self.store.record_trace(token, trace)
            except (sqlite3.Error, TimeoutError):
                trace['outcome'] = 'APP_PERSISTENCE_FAILED'
            finally:
                self.store.deadline = None
            LOG.warning(json.dumps(trace))

    def record_failure(self, token, failure, billing):
        try:
            self.store.fail(token, failure.code, failure.retry, self.clock(), failure.retry_after,
                            provider_diagnostic=failure.diagnostic, billing_state=billing)
        except (sqlite3.Error, TimeoutError):
            LOG.warning(json.dumps(dict(correlation_id=hashlib.sha256(('agw:' + token['job_id']).encode('ascii')).hexdigest()[:32],
                attempt_id=token['owner'], attempt_number=token['number'], stage='persistence',
                outcome='APP_PERSISTENCE_FAILED')))

    def run(self):
        try:
            while not self.stopping.is_set():
                for job_id in self.store.ready(self.clock()):
                    if self.stopping.is_set():
                        break
                    with self.condition:
                        self.active = True
                    try:
                        self.assess_job(job_id)
                    finally:
                        with self.condition:
                            self.active = False
                            self.condition.notify_all()
                self.stopping.wait(.01)
        except Exception as error:
            self.error = error
        finally:
            with self.condition:
                self.condition.notify_all()


def factory(path):
    return Worker(Path(path).resolve())


def usage_record(path, job_id, number):
    with sqlite3.connect(path) as conn:
        snapshot = conn.execute('SELECT settings_snapshot FROM ai_jobs WHERE id=?', (job_id,)).fetchone()
        row = conn.execute('SELECT usage,model_version FROM ai_provider_usage WHERE job_id=? AND number=?',
                           (job_id, number)).fetchone()
    config = json.loads(snapshot[0]) if snapshot and snapshot[0] else None
    provider = snapshot_provider(config) if valid_snapshot(config) else None
    raw = json.loads(row[0]) if row and row[0] is not None else None
    if type(raw) is dict and 'agw_envelope' in raw:
        normalized = raw['agw_envelope']['usage']
    elif provider == 'openai':
        from openai_adapter import normalize_usage
        normalized = normalize_usage(raw)
    elif provider == 'gemini':
        from gemini import normalize_usage
        normalized = normalize_usage(raw)
    else:
        normalized = normalize_counters()
    return dict(provider=provider, model=config.get('model') if provider else None,
                model_version=row[1] if row else None, usage=normalized, raw_usage=raw)
