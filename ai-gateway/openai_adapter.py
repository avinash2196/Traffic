"""Pure OpenAI Responses translation; no application or durable-state imports."""
import json
import time
from assessment_policy import PROMPT, Failure, output_schema, parse_json, validate
from agw_protocol import BoundaryError, retry_after, safe_id, usage
from agw_transport import request

MODEL = 'gpt-5.4-2026-03-05'
URL = 'https://api.openai.com/v1/responses'


def normalize_usage(raw):
    raw = raw if type(raw) is dict else {}
    cached = raw.get('input_tokens_details')
    reasoning = raw.get('output_tokens_details')
    return usage(dict(input_tokens=raw.get('input_tokens'), output_tokens=raw.get('output_tokens'),
        cached_input_tokens=cached.get('cached_tokens') if type(cached) is dict else None,
        thinking_tokens=reasoning.get('reasoning_tokens') if type(reasoning) is dict else None,
        total_tokens=raw.get('total_tokens')))


def check_status(response):
    status = response.status_code
    if status in (408, 429, 500, 502, 503, 504):
        raise BoundaryError('PROVIDER_TRANSIENT', 'provider', status, retry_after(response.headers.get('Retry-After', '')))
    if status in (401, 403):
        raise BoundaryError('PROVIDER_CONFIGURATION', 'provider', status)
    if status >= 300:
        raise BoundaryError('PROVIDER_REQUEST_REJECTED', 'provider', status)


def validate_output(value, media, category, coverage):
    try:
        assessment = validate(value, media, category)
        for entry, attachment in zip(coverage, assessment['attachment_relevance']):
            if entry['mode'] != 'sampled-video':
                continue
            for observation in assessment['observations']:
                if observation['media_id'] == entry['media_id']:
                    start, end = observation['start_ms'], observation['end_ms']
                    if (start, end) != (None, None) and (start != end or start not in entry['sampled_timestamps_ms']):
                        raise Failure('INVALID_MODEL_OUTPUT')
            if not entry['complete'] and (attachment['relevance'] != 'uncertain'
                    or assessment['recommendation'] != 'needs-human-judgment'):
                raise Failure('INVALID_MODEL_OUTPUT')
        return assessment
    except Failure:
        raise BoundaryError('INVALID_MODEL_OUTPUT', 'normalization', 200) from None


def assess(value, media, parts, state, client, key, deadline):
    started = time.monotonic()
    category = value['context']['reported_category']
    parts.append(dict(type='input_text', text='Untrusted citizen context: ' + json.dumps(value['context'])))
    body = dict(model=MODEL, store=False, reasoning={'effort': 'medium'}, max_output_tokens=8192,
        instructions=PROMPT + '\nFor sampled video cite only supplied frame times with start_ms=end_ms. '
        'Incomplete video requires uncertain attachment relevance and needs-human-judgment; '
        'never assert complete coverage or irrelevance for omitted frames.',
        input=[dict(role='user', content=parts)], text={'format': dict(type='json_schema',
        name='traffic_assessment', strict=True, schema=output_schema([item['id'] for item in media], category))})
    state['billing_state'] = 'unknown'
    response = request(client, ('POST', URL, {'json': body}), deadline, key)
    state['provider_request_id'] = safe_id(response.headers.get('x-request-id'))
    try:
        result = parse_json(response.content.decode('utf-8'))
    except (ValueError, UnicodeError):
        check_status(response)
        raise BoundaryError('INVALID_MODEL_OUTPUT', 'normalization', response.status_code) from None
    if type(result) is dict:
        state['usage'] = normalize_usage(result.get('usage'))
        state['model_version'] = result.get('model') if type(result.get('model')) is str else None
        if state['usage']['source'] != 'unavailable':
            state['billing_state'] = 'reported'
    state['timings_ms']['provider'] = int((time.monotonic() - started) * 1000)
    check_status(response)
    started = time.monotonic()
    try:
        if type(result) is not dict:
            raise BoundaryError('INVALID_MODEL_OUTPUT', 'normalization', response.status_code)
        if result.get('status') != 'completed':
            raise BoundaryError('MODEL_OUTPUT_UNAVAILABLE', 'normalization', response.status_code)
        texts = []
        for item in result.get('output', []):
            if item.get('type') == 'message':
                for part in item.get('content', []):
                    if part.get('type') == 'refusal':
                        raise BoundaryError('MODEL_REFUSAL', 'normalization', response.status_code)
                    if part.get('type') == 'output_text' and type(part.get('text')) is str:
                        texts.append(part['text'])
        if not texts:
            raise BoundaryError('MODEL_OUTPUT_UNAVAILABLE', 'normalization', response.status_code)
        state['assessment'] = validate_output(parse_json(''.join(texts)), media, category, state['media_coverage'])
    except (ValueError, TypeError, KeyError, AttributeError):
        raise BoundaryError('INVALID_MODEL_OUTPUT', 'normalization', response.status_code) from None
    finally:
        state['timings_ms']['normalization'] = int((time.monotonic() - started) * 1000)
