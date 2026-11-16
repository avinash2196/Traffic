"""Pure Gemini Files/GenerateContent translation; live verification remains deferred."""
import json
import re
import time
from urllib.parse import urlsplit
from assessment_policy import PROMPT, output_schema, parse_json
from agw_protocol import BoundaryError, usage
from agw_transport import deadline_remaining, request
from openai_adapter import check_status, validate_output

MODEL = 'gemini-3.8-flash'
BASE = 'https://generativelanguage.googleapis.com'


def normalize_usage(raw):
    raw = raw if type(raw) is dict else {}
    candidate, thinking = raw.get('candidatesTokenCount'), raw.get('thoughtsTokenCount')
    output = candidate + thinking if all(type(n) is int and n >= 0 for n in (candidate, thinking)) else None
    return usage(dict(input_tokens=raw.get('promptTokenCount'), cached_input_tokens=raw.get('cachedContentTokenCount'),
        output_tokens=output, thinking_tokens=raw.get('thoughtsTokenCount'),
        total_tokens=raw.get('totalTokenCount')))


def checked(client, key, deadline, method, url, **options):
    parsed = urlsplit(url)
    if parsed.scheme != 'https' or parsed.netloc != 'generativelanguage.googleapis.com' or parsed.fragment:
        raise BoundaryError('PROCESSING_ERROR', 'provider')
    response = request(client, (method, url, options), deadline, key)
    check_status(response)
    return response


def assess(value, media, parts, state, client, key, deadline):
    names, content = [], []
    started = time.monotonic()
    try:
        for item in media:
            start = checked(client, key, deadline, 'POST', BASE + '/upload/v1beta/files',
                headers={'X-Goog-Upload-Protocol': 'resumable', 'X-Goog-Upload-Command': 'start',
                'X-Goog-Upload-Header-Content-Length': str(len(item['bytes'])),
                'X-Goog-Upload-Header-Content-Type': item['mime_type']}, json={'file': {'display_name': item['id']}})
            upload = start.headers.get('x-goog-upload-url', '')
            if not urlsplit(upload).path.startswith('/upload/'):
                raise BoundaryError('PROCESSING_ERROR', 'provider')
            record = checked(client, key, deadline, 'POST', upload, headers={
                'X-Goog-Upload-Command': 'upload, finalize', 'X-Goog-Upload-Offset': '0',
                'Content-Type': item['mime_type']}, content=item['bytes']).json()['file']
            if not re.fullmatch(r'files/[A-Za-z0-9_-]+', record['name']):
                raise BoundaryError('PROCESSING_ERROR', 'provider')
            names.append(record['name'])
            expected = BASE + '/v1beta/' + record['name']
            while True:
                if record.get('uri') != expected or record.get('name') != names[-1]:
                    raise BoundaryError('PROCESSING_ERROR', 'provider')
                if record.get('state') != 'PROCESSING':
                    break
                time.sleep(min(.05, deadline_remaining(deadline, 'provider')))
                record = checked(client, key, deadline, 'GET', expected).json()
            if record.get('state') != 'ACTIVE':
                raise BoundaryError('EVIDENCE_UNAVAILABLE', 'provider')
            content.extend([{'text': 'Untrusted media handle: ' + item['id']},
                            {'fileData': {'mimeType': item['mime_type'], 'fileUri': expected}}])
        content.append({'text': 'Untrusted context and coverage: ' + json.dumps(
            dict(context=value['context'], media_coverage=state['media_coverage']))})
        body = dict(systemInstruction={'parts': [{'text': PROMPT}]}, contents=[{'role': 'user', 'parts': content}],
            generationConfig={'responseMimeType': 'application/json',
                'responseJsonSchema': output_schema([item['id'] for item in media], value['context']['reported_category'])})
        state['billing_state'] = 'unknown'
        response = request(client, ('POST', BASE + '/v1beta/models/' + MODEL + ':generateContent', {'json': body}), deadline, key)
        try:
            result = parse_json(response.content.decode('utf-8'))
        except (ValueError, UnicodeError):
            check_status(response)
            raise BoundaryError('INVALID_MODEL_OUTPUT', 'normalization', response.status_code) from None
        if type(result) is dict:
            state['usage'] = normalize_usage(result.get('usageMetadata'))
            state['model_version'] = result.get('modelVersion') if type(result.get('modelVersion')) is str else None
            if state['usage']['source'] != 'unavailable':
                state['billing_state'] = 'reported'
        state['timings_ms']['provider'] = int((time.monotonic() - started) * 1000)
        check_status(response)
        started = time.monotonic()
        if result.get('promptFeedback', {}).get('blockReason'):
            raise BoundaryError('MODEL_REFUSAL', 'normalization', response.status_code)
        candidates = result.get('candidates', [])
        if not candidates or candidates[0].get('finishReason') != 'STOP':
            raise BoundaryError('MODEL_OUTPUT_UNAVAILABLE', 'normalization', response.status_code)
        texts = [part['text'] for part in candidates[0]['content']['parts'] if
                 type(part) is dict and not part.get('thought') and type(part.get('text')) is str]
        if not texts:
            raise BoundaryError('MODEL_OUTPUT_UNAVAILABLE', 'normalization', response.status_code)
        state['assessment'] = validate_output(parse_json(''.join(texts)), media,
            value['context']['reported_category'], state['media_coverage'])
        state['timings_ms']['normalization'] = int((time.monotonic() - started) * 1000)
    except (ValueError, KeyError, TypeError, IndexError):
        raise BoundaryError('INVALID_MODEL_OUTPUT', 'normalization') from None
    finally:
        # Best effort only; local cancellation may prevent remote file deletion.
        for name in names:
            try:
                checked(client, key, deadline, 'DELETE', BASE + '/v1beta/' + name)
            except BoundaryError:
                pass
