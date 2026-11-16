"""OpenAI Responses wire/media translation; shared policy remains authoritative."""
import base64
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import os
import shutil
import sqlite3
import struct
import subprocess
from time import monotonic
import time
from uuid import uuid4

import httpx
import durable as d
from assessment_policy import PROMPT, Failure, validate, output_schema, parse_json

MODEL = 'gpt-6.1-terra'
URL = 'https://api.openai.com/v1/responses'


def check_budget(deadline):
    remaining = deadline - monotonic()
    if remaining <= 0:
        raise Failure('ATTEMPT_TIMEOUT', True, diagnostic=(None, 'preparation', 'TIMEOUT'))
    return remaining


def decode(tool, arguments, deadline, source):
    try:
        result = subprocess.run([shutil.which(tool) or tool, '-v', 'error', *arguments],
                                input=source, capture_output=True, timeout=check_budget(deadline))
    except subprocess.TimeoutExpired:
        raise Failure('ATTEMPT_TIMEOUT', True, diagnostic=(None, 'preparation', 'TIMEOUT')) from None
    check_budget(deadline)
    if result.returncode:
        raise Failure('EVIDENCE_UNAVAILABLE')
    return result.stdout


def png_frames(data):
    frames = []
    position = 0
    while position < len(data):
        start = position
        if data[position:position + 8] != b'\x89PNG\r\n\x1a\n':
            raise ValueError('Invalid decoded frame')
        position += 8
        while True:
            if position + 12 > len(data):
                raise ValueError('Incomplete decoded frame')
            size = struct.unpack('>I', data[position:position + 4])[0]
            kind = data[position + 4:position + 8]
            position += size + 12
            if position > len(data):
                raise ValueError('Incomplete decoded chunk')
            if kind == b'IEND':
                break
        frames.append(data[start:position])
    return frames


def prepare_media(media, deadline):
    from gateway import decoder_options
    parts, coverage = [], []
    for item in media:
        check_budget(deadline)
        if item['mime_type'].startswith('image/'):
            images = [(None, item['mime_type'], item['bytes'])]
            entry = {'media_id': item['id'], 'mode': 'image', 'duration_ms': None,
                     'sampled_timestamps_ms': [], 'complete': True,
                     'limitations': ['High-detail visual input does not guarantee perception of every fact.']}
        else:
            source = item['bytes']
            options = decoder_options(item['mime_type'])
            raw = decode('ffprobe', [*options, '-select_streams', 'v:0', '-show_frames',
                '-show_entries', 'frame=best_effort_timestamp_time:format=duration', '-of', 'json', 'pipe:0'], deadline, source)
            value = parse_json(raw.decode('utf-8'))
            duration = Decimal(value['format']['duration']) * 1000
            times = [Decimal(frame['best_effort_timestamp_time']) * 1000 for frame in value['frames']]
            if not times or not duration.is_finite() or duration < 0:
                raise ValueError('Unavailable source timing')
            if any(not point.is_finite() or point < 0 or point > duration for point in times):
                raise ValueError('Invalid source timing')
            if any(right < left for left, right in zip(times, times[1:])):
                raise ValueError('Unordered source timing')
            stamps = [round(point) for point in times]
            count = min(32, len(stamps))
            targets = ([stamps[0]] if count == 1 else
                       [stamps[0] + (stamps[-1] - stamps[0]) * index / (count - 1)
                        for index in range(count)])
            chosen = sorted({min(stamps, key=lambda point: (abs(point - target), point)) for target in targets})
            indices = [stamps.index(point) for point in chosen]
            selection = '+'.join('eq(n\\,' + str(index) + ')' for index in indices)
            encoded = decode('ffmpeg', [*options, '-i', 'pipe:0', '-map', '0:v:0', '-an',
                '-vf', 'select=' + selection, '-vsync', '0', '-f', 'image2pipe', '-vcodec', 'png', 'pipe:1'], deadline, source)
            frames = png_frames(encoded)
            if len(frames) != len(chosen):
                raise ValueError('Incomplete frame extraction')
            item['duration_ms'] = int(duration)
            images = [(stamp, 'image/png', frame) for stamp, frame in zip(chosen, frames)]
            entry = {'media_id': item['id'], 'mode': 'sampled-video', 'duration_ms': int(duration),
                     'sampled_timestamps_ms': chosen, 'complete': len(indices) == len(stamps),
                     'limitations': ['High-detail PNG source frames; audio is not analyzed.',
                                     'Sampled frames cannot establish facts in omitted intervals.']}
        coverage.append(entry)
        parts.append({'type': 'input_text', 'text': 'Untrusted media coverage: ' + json.dumps(entry)})
        for stamp, mime, data in images:
            parts.append({'type': 'input_text', 'text': 'Untrusted media handle: ' + item['id']
                          + ('; source frame timestamp_ms=' + str(stamp) if stamp is not None else '')})
            parts.append({'type': 'input_image', 'detail': 'high',
                          'image_url': 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii')})
        check_budget(deadline)
    return parts, coverage


def normalize_usage(raw):
    from gateway import normalize_counters
    if type(raw) is not dict:
        return normalize_counters(None)
    try:
        cached = raw.get('input_tokens_details')
        reasoning = raw.get('output_tokens_details')
        if cached is not None and type(cached) is not dict:
            raise ValueError()
        if reasoning is not None and type(reasoning) is not dict:
            raise ValueError()
        return normalize_counters({'input_tokens': raw.get('input_tokens'),
            'cached_input_tokens': cached.get('cached_tokens') if cached is not None else None,
            'output_tokens': raw.get('output_tokens'),
            'thinking_tokens': reasoning.get('reasoning_tokens') if reasoning is not None else None,
            'total_tokens': raw.get('total_tokens')})
    except ValueError:
        return normalize_counters(None)


class Adapter:
    normalize_usage = staticmethod(normalize_usage)

    def __init__(self, path, config):
        self.path, self.config = Path(path), config

    def preflight(self, job):
        from gateway import valid_snapshot, snapshot_provider, load_evidence
        self.key = os.getenv('OPENAI_API_KEY', '').strip()
        if not valid_snapshot(self.config) or snapshot_provider(self.config) != 'openai' or not self.key:
            raise Failure('PROVIDER_CONFIGURATION')
        self.deadline = monotonic() + self.config['AI_ATTEMPT_TIMEOUT_SECONDS']
        return load_evidence(self.path, job, self.deadline, monotonic)

    def request(self, client, body):
        remaining = check_budget(self.deadline)
        try:
            response = client.post(URL, headers={'Authorization': 'Bearer ' + self.key}, json=body,
                                   timeout=min(10, remaining), extensions={'asor_deadline': self.deadline})
        except httpx.TimeoutException:
            raise Failure('ATTEMPT_TIMEOUT', True, diagnostic=(None, 'inference', 'TIMEOUT')) from None
        except (httpx.NetworkError, httpx.RemoteProtocolError):
            raise Failure('PROVIDER_TRANSIENT', True, diagnostic=(None, 'inference', 'NETWORK_ERROR')) from None
        except httpx.HTTPError:
            raise Failure('PROCESSING_ERROR', diagnostic=(None, 'inference', 'PROCESSING_ERROR')) from None
        check_budget(self.deadline)
        status = response.status_code
        diagnostic = (status, 'inference', 'HTTP_STATUS')
        if status in (408, 429, 500, 502, 503, 504):
            from gateway import retry_after
            retry = retry_after(response.headers.get('Retry-After', ''), time.time())
            raise Failure('PROVIDER_TRANSIENT', True, retry, diagnostic=diagnostic)
        if status in (401, 403):
            raise Failure('PROVIDER_CONFIGURATION', diagnostic=diagnostic)
        if status >= 300:
            raise Failure('PROVIDER_REQUEST_REJECTED', diagnostic=diagnostic)
        return response

    def dispatch(self, prepared):
        report, media = prepared
        client = None
        try:
            try:
                parts, coverage = prepare_media(media, self.deadline)
            except Failure:
                raise
            except (ValueError, KeyError, TypeError, InvalidOperation, OSError):
                raise Failure('EVIDENCE_UNAVAILABLE') from None
            check_budget(self.deadline)
            context = {'untrusted_citizen_context': {'location': report['location'],
                       'vehicle_number': report['vehicle_number'], 'description': report.get('screening_notes')},
                       'reported_category': report['violation_type'], 'media_coverage': coverage}
            parts.append({'type': 'input_text', 'text': 'Untrusted: ' + json.dumps(context)})
            body = {'model': self.config['model'], 'store': False, 'reasoning': {'effort': 'medium'},
                    'max_output_tokens': 8192, 'instructions': PROMPT + '\nFor sampled video cite only supplied frame times '
                    'with start_ms=end_ms. Incomplete video requires uncertain attachment relevance and '
                    'needs-human-judgment; never assert complete coverage or irrelevance for omitted frames.',
                    'input': [{'role': 'user', 'content': parts}],
                    'text': {'format': {'type': 'json_schema', 'name': 'traffic_assessment', 'strict': True,
                             'schema': output_schema([item['id'] for item in media], report['violation_type'])}}}
            client = d.provider_client_factory()
            result = parse_json(self.request(client, body).content.decode('utf-8'))
            if type(result) is not dict:
                raise Failure('INVALID_MODEL_OUTPUT')
            version = result.get('model')
            with sqlite3.connect(self.path) as conn:
                conn.execute('INSERT OR REPLACE INTO ai_provider_usage(job_id,number,usage,model_version) VALUES(?,?,?,?)',
                             (*self.current_job, json.dumps(result.get('usage')),
                              version if isinstance(version, str) else None))
            check_budget(self.deadline)
            if result.get('status') != 'completed':
                raise Failure('MODEL_OUTPUT_UNAVAILABLE')
            texts = []
            for item in result.get('output', []):
                if item.get('type') != 'message':
                    continue
                for part in item.get('content', []):
                    if part.get('type') == 'refusal':
                        raise Failure('MODEL_OUTPUT_UNAVAILABLE')
                    if part.get('type') == 'output_text' and isinstance(part.get('text'), str):
                        texts.append(part['text'])
            if not texts:
                raise Failure('MODEL_OUTPUT_UNAVAILABLE')
            if version is not None and not isinstance(version, str):
                raise Failure('INVALID_MODEL_OUTPUT')
            try:
                value = parse_json(''.join(texts))
            except ValueError:
                raise Failure('INVALID_MODEL_OUTPUT') from None
            assessment = validate(value, media, report['violation_type'])
            for entry, attachment in zip(coverage, assessment['attachment_relevance']):
                if entry['mode'] != 'sampled-video':
                    continue
                times = entry['sampled_timestamps_ms']
                for observation in assessment['observations']:
                    if observation['media_id'] == entry['media_id']:
                        start, end = observation['start_ms'], observation['end_ms']
                        if (start, end) != (None, None) and (start != end or start not in times):
                            raise Failure('INVALID_MODEL_OUTPUT')
                if not entry['complete'] and (attachment['relevance'] != 'uncertain'
                        or assessment['recommendation'] != 'needs-human-judgment'):
                    raise Failure('INVALID_MODEL_OUTPUT')
            assessment.update(id=uuid4().hex, job_id=None, evidence_revision=report['evidence_revision'],
                              provider='openai', model=self.config['model'], model_version=version,
                              prompt_version=self.config['prompt_version'], policy_version=self.config['policy_version'],
                              legal_reference_version=self.config['legal_reference_version'], media_coverage=coverage,
                              completed_at=d.timestamp(time.time()), late_result=False)
            check_budget(self.deadline)
            return {'outcome': assessment['relevance'], 'recommendation': assessment['recommendation'],
                    'assessment': assessment}
        except Failure:
            raise
        except (ValueError, KeyError, TypeError, IndexError, InvalidOperation, AttributeError):
            raise Failure('INVALID_MODEL_OUTPUT') from None
        finally:
            self.key = None
            if client is not None:
                client.close()
            check_budget(self.deadline)
