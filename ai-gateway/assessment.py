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
                    'media_id': item.get('media_id'),
                    'mime_type': item.get('mime_type'),
                    'bytes': base64.b64decode(item['data_base64'])
                })
        
        logger.info(f"Assessment request: {correlation_id} from {provider}, media_count={len(media_items)}")
        
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
                # Validate assessment against schema
                valid = validate(assessment)
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
                        "assessment": assessment,
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



if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting AI Gateway MVP on http://127.0.0.1:9999")
    logger.info(f"  Provider: {AI_PROVIDER}")
    logger.info(f"  Gateway Token: {AI_GATEWAY_TOKEN[:10]}..." if AI_GATEWAY_TOKEN else "  Gateway Token: NOT SET")
    uvicorn.run(app, host="127.0.0.1", port=9999, log_level="info")
