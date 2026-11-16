"""Versioned gateway boundary; no application state or provider credentials."""
import base64
import binascii
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import json
import re
import time
from urllib.parse import urlsplit

from assessment_policy import PROMPT, parse_json

VERSIONS = dict(prompt_version='asor-prompt-v1', policy_version='asor-relevance-v1',
                legal_reference_version='asor-in-national-2026-11-08-v1')
PROFILES = {'openai': ('gpt-4o-mini', 'agw-openai-responses-v2', 'agw-openai-frames-v2'),
            'gemini': ('gemini-2.0-flash', 'asor-gemini-files-v1', 'asor-gemini-native-v1')}
MIMES = {'image/jpeg', 'image/png', 'video/mp4', 'video/quicktime', 'video/x-msvideo'}
COUNTERS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'thinking_tokens', 'total_tokens')
BODY_LIMIT = 224 * 1024 * 1024
FILE_LIMIT = 10 * 1024 * 1024
ERRORS = {
    'INVALID_REQUEST': (400, False), 'UNAUTHORIZED': (401, False),
    'NOT_FOUND': (404, False), 'METHOD_NOT_ALLOWED': (405, False),
    'UNSUPPORTED_MEDIA_TYPE': (415, False), 'REQUEST_TIMEOUT': (408, True),
    'SELECTION_INCOMPATIBLE': (409, False), 'PROMPT_INCOMPATIBLE': (409, False),
    'REQUEST_TOO_LARGE': (413, False), 'EVIDENCE_UNAVAILABLE': (422, False),
    'EVIDENCE_LIMIT': (422, False), 'PROVIDER_CONFIGURATION': (502, False),
    'PROVIDER_REQUEST_REJECTED': (502, False), 'MODEL_REFUSAL': (502, False),
    'MODEL_OUTPUT_UNAVAILABLE': (502, False), 'INVALID_MODEL_OUTPUT': (502, False),
    'GATEWAY_BUSY': (503, True), 'PROVIDER_TRANSIENT': (503, True),
    'ATTEMPT_TIMEOUT': (504, True), 'PROCESSING_ERROR': (500, False),
}


class BoundaryError(Exception):
    def __init__(self, code, stage, status=None, retry_after=None):
        self.code, self.stage = code, stage
        self.provider_status, self.retry_after = status, retry_after

    def envelope(self):
        return dict(code=self.code, message='AI assessment unavailable: ' + self.code + '.',
                    retryable=ERRORS[self.code][1], stage=self.stage,
                    provider_status=self.provider_status, retry_after_ms=self.retry_after)


def require(condition, code='INVALID_REQUEST', stage='validation'):
    if not condition:
        raise BoundaryError(code, stage)


def exact(value, fields):
    require(type(value) is dict and set(value) == set(fields.split()))


def text(value, maximum, *, empty=False):
    return type(value) is str and len(value) <= maximum and (empty or bool(value.strip()))


def token_valid(token):
    if type(token) is not str or not re.fullmatch(r'[A-Za-z0-9_-]{43,}', token):
        return False
    try:
        raw = base64.urlsafe_b64decode(token + '=' * (-len(token) % 4))
        return len(raw) >= 32 and base64.urlsafe_b64encode(raw).decode().rstrip('=') == token
    except (ValueError, binascii.Error):
        return False


def local_url(value):
    parsed = urlsplit(value)
    require(parsed.scheme == 'http' and parsed.hostname in ('127.0.0.1', '::1')
            and parsed.port is not None and parsed.path in ('', '/') and not parsed.query
            and not parsed.fragment and not parsed.username and not parsed.password,
            'PROVIDER_CONFIGURATION', 'transport')
    return value.rstrip('/')


def utc():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def usage(counters=None):
    counters = counters if type(counters) is dict else {}
    result = {key: value if type(value := counters.get(key)) is int and value >= 0 else None
              for key in COUNTERS}
    for subset, total in (('cached_input_tokens', 'input_tokens'), ('thinking_tokens', 'output_tokens')):
        if result[subset] is not None and result[total] is not None and result[subset] > result[total]:
            result[subset] = None
    count = sum(value is not None for value in result.values())
    result['source'] = 'provider' if count == len(COUNTERS) else 'partial' if count else 'unavailable'
    return result


def retry_after(raw):
    try:
        seconds = int(raw) if re.fullmatch(r'[0-9]+', raw) else (
            parsedate_to_datetime(raw).timestamp() - time.time())
        return min(300000, max(0, int(seconds * 1000)))
    except (ValueError, TypeError, OverflowError):
        return None


def safe_id(value):
    return value if type(value) is str and re.fullmatch(r'[A-Za-z0-9_-]{1,128}', value) else None


def validate_request(raw, provider):
    try:
        value = parse_json(raw.decode('utf-8'))
    except (ValueError, UnicodeError, RecursionError):
        raise BoundaryError('INVALID_REQUEST', 'validation') from None
    exact(value, 'contract_version correlation_id attempt_id attempt_number evidence_revision selection prompt context evidence budget_ms')
    require(value['contract_version'] == 'agw-v1')
    for name in ('correlation_id', 'attempt_id'):
        require(type(value[name]) is str and re.fullmatch('[0-9a-f]{32}', value[name]))
    for name, low, high in (('attempt_number', 1, 3), ('evidence_revision', 1, None), ('budget_ms', 1000, 110000)):
        number = value[name]
        require(type(number) is int and number >= low and (high is None or number <= high))
    selection = value['selection']
    exact(selection, 'provider model request_profile_version media_profile_version')
    expected = PROFILES.get(provider)
    require(selection == dict(provider=provider, model=expected[0], request_profile_version=expected[1],
                              media_profile_version=expected[2]), 'SELECTION_INCOMPATIBLE')
    prompt = value['prompt']
    exact(prompt, 'version text policy_version legal_reference_version')
    require(prompt == dict(version=VERSIONS['prompt_version'], text=PROMPT,
                          policy_version=VERSIONS['policy_version'], legal_reference_version=VERSIONS['legal_reference_version']),
            'PROMPT_INCOMPATIBLE')
    require(len(PROMPT.encode('utf-8')) <= 32768, 'PROMPT_INCOMPATIBLE')
    context = value['context']
    exact(context, 'reported_category location vehicle_number description')
    require(context['reported_category'] in ('helmet', 'triple-riding', 'red-light'))
    require(text(context['location'], 1024) and text(context['vehicle_number'], 64))
    require(context['description'] is None or text(context['description'], 8192, empty=True))
    evidence = value['evidence']
    require(type(evidence) is list and bool(evidence))
    require(len(evidence) <= 16, 'REQUEST_TOO_LARGE')
    identifiers, media, total = set(), [], 0
    metadata = dict(value, evidence=[])
    for item in evidence:
        exact(item, 'media_id mime_type data_base64')
        identifier, mime, encoded = item['media_id'], item['mime_type'], item['data_base64']
        require(type(identifier) is str and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', identifier)
                and identifier not in identifiers and type(mime) is str and mime in MIMES)
        identifiers.add(identifier)
        require(type(encoded) is str and bool(encoded))
        require(len(encoded) <= ((FILE_LIMIT + 2) // 3) * 4, 'REQUEST_TOO_LARGE')
        decoded = bytearray()
        try:
            for offset in range(0, len(encoded), 65536):
                chunk = encoded[offset:offset + 65536]
                block = base64.b64decode(chunk, validate=True)
                require(base64.b64encode(block).decode('ascii') == chunk)
                require(offset + len(chunk) == len(encoded) or '=' not in chunk)
                decoded.extend(block)
                require(len(decoded) <= FILE_LIMIT, 'REQUEST_TOO_LARGE')
        except (ValueError, UnicodeError, binascii.Error):
            raise BoundaryError('INVALID_REQUEST', 'validation') from None
        require(bool(decoded))
        total += len(decoded)
        require(total <= 160 * 1024 * 1024, 'REQUEST_TOO_LARGE')
        metadata['evidence'].append(dict(media_id=identifier, mime_type=mime))
        media.append(dict(id=identifier, mime_type=mime, bytes=bytes(decoded)))
    require(len(raw) - sum(len(item['data_base64']) for item in evidence) <= 128 * 1024, 'REQUEST_TOO_LARGE')
    return value, media
