"""AI Gateway MVP - Simplified Single-Call Approach.

Single endpoint that returns boolean violations directly.
No complex schema validation - just what officer needs to decide.
"""

import os
from pathlib import Path

# Load environment variables
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai.gateway.mvp")

app = FastAPI(title="AI Gateway MVP - Simplified")

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
AI_GATEWAY_TOKEN = os.getenv('AI_GATEWAY_TOKEN', 'local-ai-gateway')


async def call_openai_simple(image_base64: str, violation_type: str) -> dict:
    """
    Single OpenAI call that returns boolean violations.
    
    Args:
        image_base64: Base64-encoded image
        violation_type: Type of violation (helmet, etc.)
    
    Returns:
        {
            "no_helmet": true/false,
            "triple_riding": true/false,
            "red_light": true/false,
            "recommendation": "Issue warning" or "No violation"
        }
    """
    prompt = f"""Analyze this traffic violation image for a {violation_type} violation.

Return ONLY the JSON in the exact format below (no markdown, no explanation, no extra text):
{{
  "no_helmet": true or false,
  "triple_riding": true or false,
  "red_light": true or false,
  "recommendation": "Issue warning" or "No violation"
}}

Rules:
- no_helmet: Are riders/drivers NOT wearing helmets? (true/false)
- triple_riding: Are there more than 2 people on a single two-wheeler? (true/false)
- red_light: Is vehicle crossing at a red traffic signal? (true/false)
- recommendation: If any violation is true, say "Issue warning". Otherwise "No violation".

Be confident in your assessment. Return JSON in provided format only."""

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": OPENAI_MODEL,
        "temperature": 0.2,
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    }
                ]
            }
        ]
    }
    
    async with httpx.AsyncClient(timeout=30) as client:
        logger.info(f"OpenAI request: {OPENAI_MODEL}")
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers
        )
        
        if response.status_code != 200:
            logger.error(f"OpenAI error: {response.status_code} {response.text}")
            raise Exception(f"OpenAI API error: {response.status_code}")
        
        result = response.json()
        logger.info(f"OpenAI response content: {result.get('choices', [{}])[0].get('message', {}).get('content', '')[:200]}")
        
        # Extract content
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        # Clean up markdown code blocks if present
        content = content.replace('```json', '').replace('```', '').strip()
        
        # Parse JSON
        try:
            assessment = json.loads(content)
            
            # Ensure all fields exist and are correct type
            assessment = {
                'no_helmet': bool(assessment.get('no_helmet', False)),
                'triple_riding': bool(assessment.get('triple_riding', False)),
                'red_light': bool(assessment.get('red_light', False)),
                'recommendation': str(assessment.get('recommendation', 'No violation'))
            }
            
            logger.info(f"Parsed assessment: {assessment}")
            return assessment
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}, content: {content}")
            raise Exception(f"Invalid JSON response: {content}")


@app.post("/v1/assessments")
async def assess_violation(request: Request):
    """
    Single-call assessment endpoint.
    Returns violations directly as booleans.
    """
    started = time.monotonic()
    correlation_id = str(uuid4())
    
    try:
        # Verify authorization
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.split(' ', 1)[1] if 'Bearer ' in auth_header else ''
        
        if token != AI_GATEWAY_TOKEN:
            return JSONResponse(status_code=401, content={
                "error": "Unauthorized"
            })
        
        # Parse request
        body = await request.json()
        correlation_id = body.get('correlation_id', correlation_id)
        
        # Extract media
        evidence_list = body.get('evidence', [])
        if not evidence_list:
            return JSONResponse(status_code=400, content={
                "error": "No evidence provided",
                "correlation_id": correlation_id
            })
        
        # Get first image
        image_base64 = evidence_list[0].get('data_base64', '')
        if not image_base64:
            return JSONResponse(status_code=400, content={
                "error": "No image data",
                "correlation_id": correlation_id
            })
        
        # Extract violation type from prompt
        prompt = body.get('prompt', {})
        prompt_text = prompt.get('text', '')
        
        violation_type = 'traffic'
        if 'violation:' in prompt_text.lower():
            parts = prompt_text.lower().split('violation:')
            if len(parts) > 1:
                violation_type = parts[1].strip().split(' by ')[0].strip()
        
        logger.info(f"Assessment: {correlation_id}, violation={violation_type}")
        
        # Call OpenAI
        try:
            assessment = await call_openai_simple(image_base64, violation_type)
            
            elapsed_ms = int((time.monotonic() - started) * 1000)
            logger.info(f"Assessment completed in {elapsed_ms}ms")
            
            return JSONResponse(status_code=200, content={
                "correlation_id": correlation_id,
                "assessment": assessment,
                "timings_ms": elapsed_ms
            })
            
        except Exception as e:
            logger.error(f"Assessment failed: {e}")
            elapsed_ms = int((time.monotonic() - started) * 1000)
            
            return JSONResponse(status_code=502, content={
                "error": str(e),
                "correlation_id": correlation_id,
                "timings_ms": elapsed_ms
            })
    
    except Exception as e:
        logger.error(f"Request error: {e}")
        elapsed_ms = int((time.monotonic() - started) * 1000)
        
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "correlation_id": correlation_id,
            "timings_ms": elapsed_ms
        })


@app.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse(status_code=200, content={"status": "ok"})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=9004)
