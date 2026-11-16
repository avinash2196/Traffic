"""Shared provider selection, evidence authority, and durable orchestration."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import time

import durable as d
from assessment_policy import Failure
from intake import media_path

VERSIONS = {'prompt_version': 'asor-prompt-v1', 'policy_version': 'asor-relevance-v1',
            'legal_reference_version': 'asor-in-national-2026-11-08-v1'}
PROFILES = {
    'gemini': ('gemini-3.8-flash', 'asor-gemini-files-v1', 'asor-gemini-native-v1'),
    'openai': ('gpt-6.1-terra', 'asor-openai-responses-v1', 'asor-openai-frames-v1'),
}
RANGES = {'AI_ATTEMPT_TIMEOUT_SECONDS': (10, 600), 'AI_RETRY_BASE_SECONDS': (1, 60),
          'AI_RETRY_MAX_DELAY_SECONDS': (2, 3600)}


def settings(provider=None):
    provider = os.getenv('AI_PROVIDER', 'gemini') if provider is None else provider
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
    legacy_keys = set(VERSIONS) | set(RANGES) | {'model', 'valid'}
    if set(value) == legacy_keys and value.get('model') == PROFILES['gemini'][0]:
        return 'gemini'
    return None


def valid_snapshot(value):
    if type(value) is not dict or value.get('valid') is not True:
        return False
    provider = snapshot_provider(value)
    if not isinstance(provider, str) or provider not in PROFILES:
        return False
    model, request_profile, media_profile = PROFILES[provider]
    if value.get('model') != model or any(value.get(k) != v for k, v in VERSIONS.items()):
        return False
    if 'provider' in value and (value.get('request_profile_version') != request_profile
                               or value.get('media_profile_version') != media_profile):
        return False
    for key, (low, high) in RANGES.items():
        if type(value.get(key)) is not int or not low <= value[key] <= high:
            return False
    return value['AI_RETRY_MAX_DELAY_SECONDS'] >= 2 * value['AI_RETRY_BASE_SECONDS']


def remaining(deadline, clock=time.monotonic):
    budget = deadline - clock()
    if budget <= 0:
        raise Failure('ATTEMPT_TIMEOUT', True, diagnostic=(None, 'preparation', 'TIMEOUT'))
    return budget


def decoder_options(mime):
    options = ['-protocol_whitelist', 'file,pipe', '-format_whitelist', 'mov,avi']
    if mime != 'video/x-msvideo':
        options += ['-enable_drefs', '0', '-use_absolute_path', '0']
    return options


def load_evidence(path, job, deadline, clock=time.monotonic, *, native_duration=False):
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        report = dict(conn.execute('SELECT * FROM reports WHERE id=?', (job['report_id'],)).fetchone())
        media = [dict(row) for row in conn.execute(
            'SELECT * FROM media WHERE report_id=? ORDER BY attachment_position', (report['id'],))]
    try:
        if not media:
            raise ValueError()
        for item in media:
            remaining(deadline, clock)
            if item['owner_citizen_id'] != report['citizen_id']:
                raise ValueError()
            owned = media_path(item)
            item['bytes'] = owned.read_bytes()
            if not item['bytes'] or hashlib.sha256(item['bytes']).hexdigest() != item['sha256_hash']:
                raise ValueError()
            if native_duration and item['mime_type'].startswith('video/'):
                result = subprocess.run([shutil.which('ffprobe') or 'ffprobe', '-v', 'error',
                    *decoder_options(item['mime_type']), '-show_entries', 'format=duration',
                    '-of', 'json', 'pipe:0'], input=item['bytes'], capture_output=True,
                    timeout=min(10, remaining(deadline, clock)))
                if result.returncode:
                    raise ValueError()
                item['duration_ms'] = int(float(json.loads(result.stdout)['format']['duration']) * 1000)
            remaining(deadline, clock)
        return report, media
    except Failure:
        raise
    except subprocess.TimeoutExpired:
        raise Failure('ATTEMPT_TIMEOUT', True, diagnostic=(None, 'preparation', 'TIMEOUT')) from None
    except Exception:
        raise Failure('EVIDENCE_UNAVAILABLE') from None


class Worker(d.Worker):
    def __init__(self, path):
        super().__init__(d.JobStore(path), dispatch=True)
        self.path = Path(path)

    def assess_job(self, job_id):
        with self.store.transaction() as conn:
            job = dict(conn.execute('SELECT * FROM ai_jobs WHERE id=?', (job_id,)).fetchone())
        try:
            config = json.loads(job['settings_snapshot'])
            if not valid_snapshot(config):
                raise Failure('PROVIDER_CONFIGURATION')
            adapter = ADAPTERS[snapshot_provider(config)](self.path, config)
            prepared = adapter.preflight(job)
        except (ValueError, TypeError, KeyError):
            failure = Failure('PROVIDER_CONFIGURATION')
        except Failure as error:
            failure = error
        else:
            failure = None
        if failure is not None and failure.code == 'ATTEMPT_TIMEOUT':
            token = self.store.claim(job_id, 'provider-worker', self.clock())
            if token is not None:
                self.store.fail(token, failure.code, True, self.clock(), provider_diagnostic=failure.diagnostic)
            return
        if failure is not None:
            with self.store.transaction() as conn:
                conn.execute("UPDATE ai_jobs SET state='failed',failure_code=?,completed_at=?,next_attempt_at=NULL "
                             "WHERE id=? AND state IN ('pending','retry-wait')",
                             (failure.code, self.clock(), job_id))
            return
        token = self.store.claim(job_id, 'provider-worker', self.clock())
        if token is None:
            return
        adapter.current_job = (job_id, token['number'])
        try:
            value = adapter.dispatch(prepared)
        except Failure as error:
            self.store.fail(token, error.code, error.retry, self.clock(), error.retry_after,
                            provider_diagnostic=error.diagnostic)
        except Exception:
            self.store.fail(token, 'PROCESSING_ERROR', False, self.clock(),
                            provider_diagnostic=(None, None, 'PROCESSING_ERROR'))
        else:
            value['assessment']['job_id'] = job_id
            self.store.complete(token, value, self.clock())

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




def retry_after(raw, now):
    from email.utils import parsedate_to_datetime
    from datetime import timezone
    if re.fullmatch(r'[0-9]+', raw.strip()):
        return int(raw.strip())
    try:
        value = parsedate_to_datetime(raw)
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return max(0, value.timestamp() - now)
    except (ValueError, TypeError, OverflowError):
        return None

def normalize_counters(counters):
    keys = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'thinking_tokens', 'total_tokens')
    unavailable = dict.fromkeys(keys)
    unavailable['source'] = 'unavailable'
    if counters is None:
        return unavailable
    if any(value is not None and (type(value) is not int or value < 0) for value in counters.values()):
        return unavailable
    for subset, total in (('cached_input_tokens', 'input_tokens'), ('thinking_tokens', 'output_tokens')):
        if counters[subset] is not None and counters[total] is not None and counters[subset] > counters[total]:
            return unavailable
    result = dict(counters)
    result['source'] = 'provider' if any(value is not None for value in counters.values()) else 'unavailable'
    return result

def usage_record(path, job_id, number):
    with sqlite3.connect(path) as conn:
        snapshot = conn.execute('SELECT settings_snapshot FROM ai_jobs WHERE id=?', (job_id,)).fetchone()
        row = conn.execute('SELECT usage,model_version FROM ai_provider_usage WHERE job_id=? AND number=?',
                           (job_id, number)).fetchone()
    try:
        config = json.loads(snapshot[0]) if snapshot else None
    except (ValueError, TypeError):
        config = None
    provider = snapshot_provider(config) if valid_snapshot(config) else None
    raw = json.loads(row[0]) if row and row[0] is not None else None
    usage = {key: None for key in ('input_tokens', 'cached_input_tokens', 'output_tokens',
                                   'thinking_tokens', 'total_tokens')}
    usage['source'] = 'unavailable'
    if provider in ADAPTERS:
        usage = ADAPTERS[provider].normalize_usage(raw)
    return {'provider': provider, 'model': config.get('model') if provider else None,
            'model_version': row[1] if row else None, 'usage': usage, 'raw_usage': raw}


from gemini import Adapter as GeminiAdapter
from openai_adapter import Adapter as OpenAIAdapter

ADAPTERS = {'gemini': GeminiAdapter, 'openai': OpenAIAdapter}
