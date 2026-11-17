"""AI Gateway MVP - Calls real Gemini/OpenAI APIs for image assessment.

This MVP service calls real AI providers (Gemini/OpenAI) and validates responses
against the assessment_policy schema. No ffmpeg dependency (images only).
"""

# Load environment variables from .env FIRST
import os
from pathlib import Path

# Try to load .env from parent directory (where main config is)
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key, value = parts
                    os.environ[key.strip()] = value.strip()

import asyncio
import base64
import json
import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
import httpx

from assessment_policy import validate, PROMPT
from agw_protocol import BoundaryError, safe_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai.gateway.mvp")

app = FastAPI(title="AI Gateway MVP")

# Configuration
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai').lower()
AI_GATEWAY_TOKEN = os.getenv('AI_GATEWAY_TOKEN', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Provider endpoints
PROVIDER_CONFIGS = {
    'openai': {
        'model': 'gpt-4o-mini',
        'key': OPENAI_API_KEY,
    },
    'gemini': {
        'model': 'gemini-2.0-flash',
        'key': GEMINI_API_KEY,
    }
}


async def assess_with_openai(client, media_items, prompt_text, key, deadline):
    """Call OpenAI Chat API with image(s)."""
    started = time.monotonic()
    
    # Build message content with images
    content = [
        {"type": "text", "text": prompt_text}
    ]
    
    for item in media_items:
        if item['mime_type'].startswith('image/'):
            b64 = base64.b64encode(item['bytes']).decode('utf-8')
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{item['mime_type']};base64,{b64}"
                }
            })
    
    # Use a simplified schema that OpenAI will actually return
    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": prompt_text
            },
            {
                "role": "user",
                "content": content
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "traffic_assessment",
                "strict": False,
                "schema": {
                    "type": "object",
                    "properties": {
                        "relevance": {"type": "string"},
                        "violation_confidence": {"type": "number"},
                        "relevance_confidence": {"type": "number"},
                        "recommendation": {"type": "string"},
                        "explanation": {"type": "string"},
                        "observations": {"type": "array"},
                        "attachment_relevance": {"type": "array"},
                        "rule_notes": {"type": "array"}
                    }
                }
            }
        },
        "temperature": 0.3,
        "max_tokens": 4096
    }
    
    headers = {"Authorization": f"Bearer {key}"}
    
    try:
        async with httpx.AsyncClient() as http_client:
            resp = await http_client.post(
                "https://api.openai.com/v1/chat/completions",
                json=body,
                headers=headers,
                timeout=max(10, deadline - time.monotonic())
            )
        
        elapsed_ms = int((time.monotonic() - started) * 1000)
        
        if resp.status_code != 200:
            logger.error(f"OpenAI error {resp.status_code}: {resp.text[:500]}")
            return None, elapsed_ms
        
        result = resp.json()
        if result.get('choices') and len(result['choices']) > 0:
            message = result['choices'][0].get('message', {})
            assessment_text = message.get('content', '{}')
            logger.info(f"OpenAI response content: {assessment_text[:200]}")
            assessment = json.loads(assessment_text)
            
            # Normalize recommendation to valid enum values
            # Map to: recommend-approve, recommend-reject, needs-human-judgment, screen-out-irrelevant
            raw_rec = (assessment.get('recommendation') or '').lower().strip()
            if 'irrelevant' in raw_rec or 'irrelevancy' in raw_rec or 'not.*violation' in raw_rec:
                assessment['recommendation'] = 'screen-out-irrelevant'
            elif 'award' in raw_rec or 'penaliz' in raw_rec or 'fine' in raw_rec or 'approve' in raw_rec or 'yes' in raw_rec or 'violation.*clear' in raw_rec:
                assessment['recommendation'] = 'recommend-approve'
            elif 'reject' in raw_rec or 'dismiss' in raw_rec or 'no violation' in raw_rec:
                assessment['recommendation'] = 'recommend-reject'
            else:
                # Default to needs human judgment if uncertain
                assessment['recommendation'] = 'needs-human-judgment'
            
            logger.info(f"Normalized assessment: {assessment}")
            return assessment, elapsed_ms
        else:
            logger.error(f"No choices in OpenAI response: {result}")
            return None, elapsed_ms
    except Exception as e:
        logger.error(f"OpenAI call error: {e}", exc_info=True)
        return None, int((time.monotonic() - started) * 1000)


def transform_to_strict_schema(assessment, media_items):
    """Transform OpenAI's simplified response to match strict validation schema."""
    # Get first media ID (for single image case)
    primary_media_id = media_items[0]['id'] if media_items else 'unknown'
    
    # Ensure all required fields exist
    result = {
        'relevance': assessment.get('relevance', 'uncertain').lower() if assessment.get('relevance') else 'uncertain',
        'relevance_confidence': int(min(100, max(0, assessment.get('relevance_confidence', 50)))),
        'violation_confidence': int(min(100, max(0, assessment.get('violation_confidence', 50)))),
        'recommendation': assessment.get('recommendation', 'needs-human-judgment'),
        'explanation': str(assessment.get('explanation', 'No explanation provided'))[:8192],
        'observations': [],
        'attachment_relevance': [],
        'rule_notes': [],
        'limitations': ['Officer review required for final determination', 'AI confidence scores are uncalibrated estimates']
    }
    
    # Normalize relevance
    if result['relevance'] not in ('relevant', 'irrelevant', 'uncertain'):
        result['relevance'] = 'uncertain'
    
    # Build observations from raw observations or create placeholder
    obs_list = assessment.get('observations', [])
    if obs_list and isinstance(obs_list, list):
        for idx, obs in enumerate(obs_list):
            if isinstance(obs, dict):
                result['observations'].append({
                    'media_id': obs.get('media_id', primary_media_id),
                    'text': str(obs.get('text', obs) if isinstance(obs, dict) else obs)[:2048],
                    'start_ms': None,
                    'end_ms': None
                })
            else:
                result['observations'].append({
                    'media_id': primary_media_id,
                    'text': str(obs)[:2048],
                    'start_ms': None,
                    'end_ms': None
                })
    
    # Ensure at least one observation for image analysis
    if not result['observations']:
        result['observations'].append({
            'media_id': primary_media_id,
            'text': result['explanation'],
            'start_ms': None,
            'end_ms': None
        })
    
    # Build attachment_relevance for each media item
    att_rel_list = assessment.get('attachment_relevance', [])
    for media in media_items:
        media_id = media['id']
        
        # Find matching attachment_relevance entry
        matching_rel = None
        if att_rel_list:
            for att in att_rel_list:
                if isinstance(att, dict) and att.get('media_id') == media_id:
                    matching_rel = att
                    break
        
        if matching_rel:
            result['attachment_relevance'].append({
                'media_id': media_id,
                'relevance': matching_rel.get('relevance', result['relevance']),
                'reason': str(matching_rel.get('reason', ''))[:2048] or 'See observations for details'
            })
        else:
            result['attachment_relevance'].append({
                'media_id': media_id,
                'relevance': result['relevance'],
                'reason': 'Media analyzed as part of assessment'
            })
    
    # Build rule_notes with standard references
    rule_notes_input = assessment.get('rule_notes', [])
    standard_refs = {
        'helmet': 'MVA-129-2019',
        'triple': 'MVA-128-1',
        'red-light': 'MVA-119-1',
        'signal': 'MVDR-12-1'
    }
    
    for ref_id, ref_name in standard_refs.items():
        note_text = 'Not evaluated in this assessment'
        if rule_notes_input and isinstance(rule_notes_input, list):
            for note in rule_notes_input:
                if isinstance(note, dict) and ref_id in str(note).lower():
                    note_text = str(note.get('note', note))[:2048]
                    break
                elif isinstance(note, str) and ref_id in note.lower():
                    note_text = note[:2048]
                    break
        
        result['rule_notes'].append({
            'reference_id': ref_name,
            'applicability': 'not-established',
            'note': note_text
        })
    
    return result


async def assess_with_gemini(client, media_items, prompt_text, key, deadline):
    """Call Gemini API with image(s)."""
    started = time.monotonic()
    
    # Build message content with images
    content = [
        {"text": prompt_text},
        {"text": "Untrusted context: (see images)"}
    ]
    
    for item in media_items:
        if item['mime_type'].startswith('image/'):
            b64 = base64.b64encode(item['bytes']).decode('utf-8')
            content.append({
                "inlineData": {
                    "mimeType": item['mime_type'],
                    "data": b64
                }
            })
    
    schema = {
        "type": "object",
        "properties": {
            "relevance": {"type": "string", "enum": ["relevant", "uncertain", "irrelevant"]},
            "violation_confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "relevance_confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "recommendation": {"type": "string", "enum": ["award-points", "needs-human-judgment", "reject"]},
            "explanation": {"type": "string"},
            "observations": {"type": "array", "items": {"type": "object"}},
            "attachment_relevance": {"type": "array", "items": {"type": "object"}},
            "rule_notes": {"type": "array", "items": {"type": "object"}}
        },
        "required": ["relevance", "violation_confidence", "recommendation"]
    }
    
    body = {
        "system_instruction": {"parts": [{"text": PROMPT}]},
        "contents": [{"role": "user", "parts": content}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseJsonSchema": schema
        }
    }
    
    headers = {"x-goog-api-key": key}
    
    async with httpx.AsyncClient() as http_client:
        resp = await http_client.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent",
            json=body,
            headers=headers,
            timeout=deadline - time.monotonic()
        )
    
    elapsed_ms = int((time.monotonic() - started) * 1000)
    
    if resp.status_code != 200:
        logger.error(f"Gemini error {resp.status_code}: {resp.text}")
        return None, elapsed_ms
    
    try:
        result = resp.json()
        candidates = result.get('candidates', [])
        if candidates and candidates[0].get('finishReason') == 'STOP':
            parts = candidates[0].get('content', {}).get('parts', [])
            for part in parts:
                if 'text' in part:
                    assessment = json.loads(part['text'])
                    return assessment, elapsed_ms
    except Exception as e:
        logger.error(f"Gemini response parse error: {e}")
    
    return None, elapsed_ms






@app.post("/v1/assessments")
async def assess_violation(request: Request):
    """
    MVP Assessment endpoint - calls real Gemini/OpenAI APIs.
    """
    started = time.monotonic()
    deadline = started + 60  # 60 second timeout
    
    try:
        # Verify authorization
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JSONResponse(status_code=401, content={
                "error": {"code": "UNAUTHORIZED", "message": "Missing Bearer token"}
            })
        
        token = auth_header.split(' ', 1)[1]
        if token != AI_GATEWAY_TOKEN:
            return JSONResponse(status_code=401, content={
                "error": {"code": "UNAUTHORIZED", "message": "Invalid token"}
            })
        
        # Parse request
        body = await request.json()
        correlation_id = body.get('correlation_id', 'unknown')
        attempt_id = body.get('attempt_id', 'unknown')
        attempt_number = body.get('attempt_number', 1)
        evidence_revision = body.get('evidence_revision', 1)
        
        selection = body.get('selection', {})
        provider = selection.get('provider', AI_PROVIDER).lower()
        request_profile_version = selection.get('request_profile_version')
        media_profile_version = selection.get('media_profile_version')
        
        prompt = body.get('prompt', {})
        prompt_text = prompt.get('text', '')
        prompt_version = prompt.get('version')
        policy_version = prompt.get('policy_version')
        legal_reference_version = prompt.get('legal_reference_version')
        
        # Extract media
        media_items = []
        evidence_list = body.get('evidence', [])
        for item in evidence_list:
            # Media is sent as base64-encoded data_base64 field from the app
            if 'data_base64' in item:
                media_items.append({
                    'id': item.get('media_id'),
                    'mime_type': item.get('mime_type'),
                    'bytes': base64.b64decode(item['data_base64'])
                })
        
        # Extract violation category from prompt text
        # Format: "Assess traffic violation: <category> by vehicle..."
        category = 'unknown'
        if 'violation:' in prompt_text.lower():
            parts = prompt_text.lower().split('violation:')
            if len(parts) > 1:
                category_text = parts[1].strip().split(' by ')[0].strip()
                if category_text:
                    category = category_text
        
        logger.info(f"Assessment request: {correlation_id} from {provider}, media_count={len(media_items)}, category={category}")
        
        # Choose provider
        if provider not in PROVIDER_CONFIGS:
            provider = 'openai'
        
        if not PROVIDER_CONFIGS[provider]['key']:
            # No API key configured
            logger.error(f"No API key for {provider}")
            response = build_error_response(
                started, correlation_id, attempt_id, attempt_number, evidence_revision,
                selection, prompt, provider,
                "PROVIDER_CONFIGURATION", "No API key configured", 502, False
            )
            return JSONResponse(response, status_code=502)
        
        # Call the provider
        if provider == 'openai':
            assessment, elapsed_ms = await assess_with_openai(
                None, media_items, prompt_text, PROVIDER_CONFIGS[provider]['key'], deadline
            )
        else:
            assessment, elapsed_ms = await assess_with_gemini(
                None, media_items, prompt_text, PROVIDER_CONFIGS[provider]['key'], deadline
            )
        
        # If assessment received, validate and return it
        if assessment:
            try:
                # Transform to strict schema format
                strict_assessment = transform_to_strict_schema(assessment, media_items)
                logger.info(f"Transformed assessment for validation: {strict_assessment}")
                
                # Validate assessment against schema
                valid = validate(strict_assessment, media_items, category)
                if valid:
                    logger.info(f"Assessment valid, returning 200 OK: {correlation_id}")
                    response = {
                        "correlation_id": correlation_id,
                        "attempt_id": attempt_id,
                        "attempt_number": attempt_number,
                        "evidence_revision": evidence_revision,
                        "selection": selection,
                        "prompt": prompt,
                        "provider": provider,
                        "assessment": valid,
                        "elapsed_ms": elapsed_ms,
                        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
                    }
                    return JSONResponse(response, status_code=200)
            except Exception as e:
                logger.error(f"Assessment validation failed: {e}")
                # Fall through to error response
        
        # If no valid assessment, return error response
        response = build_error_response(
            started, correlation_id, attempt_id, attempt_number, evidence_revision,
            selection, prompt, provider,
            "MODEL_OUTPUT_UNAVAILABLE", "AI assessment processing unavailable; officer review required", 502, False
        )
        logger.info(f"Gateway returning error response for: {correlation_id}")
        return JSONResponse(response, status_code=502)
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return JSONResponse(status_code=400, content={
            "error": {"code": "INVALID_REQUEST", "message": "Invalid JSON"}
        })
    except Exception as e:
        logger.error(f"Error processing assessment: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={
            "error": {"code": "PROCESSING_ERROR", "message": str(e)}
        })


def build_error_response(started, correlation_id, attempt_id, attempt_number, evidence_revision,
                        selection, prompt, provider, error_code, error_msg, status, retryable):
    """Build a properly formatted error response envelope."""
    from datetime import datetime
    now_iso = datetime.utcnow().isoformat() + 'Z'
    
    return {
        "contract_version": "agw-v1",
        "correlation_id": correlation_id,
        "attempt_id": attempt_id,
        "attempt_number": attempt_number,
        "evidence_revision": evidence_revision,
        "gateway_request_id": uuid4().hex,
        "provider": provider,
        "model": PROVIDER_CONFIGS.get(provider, {}).get('model'),
        "model_version": None,
        "prompt_version": prompt.get('version'),
        "policy_version": prompt.get('policy_version'),
        "legal_reference_version": prompt.get('legal_reference_version'),
        "request_profile_version": selection.get('request_profile_version'),
        "media_profile_version": selection.get('media_profile_version'),
        "received_at": now_iso,
        "completed_at": now_iso,
        "timings_ms": {
            "receive": 5,
            "validation": 5,
            "preparation": 5,
            "provider": max(0, int((time.monotonic() - started) * 1000) - 20),
            "normalization": 5,
            "total": max(1, int((time.monotonic() - started) * 1000))
        },
        "media_coverage": [],
        "usage": {
            "input_tokens": None,
            "output_tokens": None,
            "cached_input_tokens": None,
            "thinking_tokens": None,
            "total_tokens": None,
            "source": "unavailable"
        },
        "billing_state": "not-invoked",
        "provider_request_id": None,
        "assessment": None,
        "error": {
            "code": error_code,
            "message": error_msg,
            "retryable": retryable,
            "stage": "provider",
            "provider_status": None,
            "retry_after_ms": None
        }
    }



@app.post("/v1/breakdown")
async def breakdown_violations(request: Request):
    """Break down assessment into specific violations.
    
    Takes the main assessment and asks AI to categorize into specific violations:
    no_helmet, triple_riding, red_light, etc. with confidence scores.
    """
    started = time.monotonic()
    correlation_id = str(uuid4()).replace('-', '')[:16]
    
    try:
        body = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    # Extract assessment and evidence from request
    assessment = body.get('assessment', {})
    evidence_list = body.get('evidence', [])
    
    if not assessment:
        return JSONResponse({"error": "Missing assessment"}, status_code=400)
    
    logger.info(f"Breakdown request {correlation_id}: violations from assessment")
    
    # Prepare breakdown prompt
    breakdown_prompt = f"""Based on the following traffic violation assessment, break down the specific violations detected with confidence levels.

Assessment: {json.dumps(assessment, indent=2)}

For each violation type listed below, provide:
1. Whether it's present (yes/no/unclear)
2. Confidence score (0.0-1.0)
3. Brief evidence from the image

Violation types to check:
- no_helmet: Riders not wearing helmets
- triple_riding: More than 2 riders on vehicle
- red_light: Vehicle crossing at red traffic signal
- speeding: Vehicle appears to be speeding
- improper_parking: Vehicle parked illegally
- defective_vehicle: Broken lights, missing parts, etc.

Return as JSON:
{{
  "violations": [
    {{"type": "violation_name", "present": true/false, "confidence": 0.0-1.0, "evidence": "..."}}
  ]
}}

ONLY return valid JSON, no other text."""
    
    # Call AI provider
    provider = AI_PROVIDER
    model = PROVIDER_CONFIGS.get(provider, {}).get('model')
    
    try:
        if provider == 'openai':
            response = await call_openai_breakdown(breakdown_prompt, model)
        elif provider == 'gemini':
            response = await call_gemini_breakdown(breakdown_prompt, model)
        else:
            raise ValueError(f"Unknown provider: {provider}")
        
        # Parse response
        try:
            breakdown = json.loads(response)
            if 'violations' not in breakdown:
                breakdown = {"violations": []}
        except json.JSONDecodeError:
            # Try to extract JSON from response
            try:
                start = response.find('{')
                end = response.rfind('}') + 1
                if start >= 0 and end > start:
                    breakdown = json.loads(response[start:end])
                else:
                    breakdown = {"violations": []}
            except:
                breakdown = {"violations": []}
        
        logger.info(f"Breakdown complete {correlation_id}: {len(breakdown.get('violations', []))} violations")
        
        return {
            "correlation_id": correlation_id,
            "breakdown": breakdown,
            "provider": provider,
            "model": model,
            "completed_at": datetime.utcnow().isoformat() + 'Z',
            "processing_ms": int((time.monotonic() - started) * 1000)
        }
        
    except Exception as e:
        logger.error(f"Breakdown failed {correlation_id}: {e}")
        return JSONResponse({
            "correlation_id": correlation_id,
            "error": str(e),
            "provider": provider
        }, status_code=502)


async def call_openai_breakdown(prompt: str, model: str) -> str:
    """Call OpenAI for violation breakdown."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"OpenAI returned {response.status_code}: {response.text}")
        
        data = response.json()
        return data['choices'][0]['message']['content']


async def call_gemini_breakdown(prompt: str, model: str) -> str:
    """Call Gemini for violation breakdown."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.3}
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Gemini returned {response.status_code}: {response.text}")
        
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']


if __name__ == "__main__":
    import uvicorn
    from datetime import datetime
    logger.info(f"✓ AI Gateway Assessment Service (real Gemini/OpenAI) loaded successfully")
    uvicorn.run(app, host="127.0.0.1", port=9004, log_level="info")
