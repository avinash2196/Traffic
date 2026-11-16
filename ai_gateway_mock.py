"""Minimal local AI gateway mock for MVP testing.

When the AI worker calls POST /v1/assessments, this service returns a mock assessment
that satisfies the gateway protocol, allowing local testing without Docker.
"""
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-gateway-mock")

app = FastAPI(title="AI Gateway Mock")

@app.post("/v1/assessments")
async def mock_assessment(request: Request):
    """Mock AI assessment endpoint.
    
    Receives a request from the AI worker and returns a mock assessment
    that indicates processing is unavailable (graceful fallback).
    """
    try:
        body = await request.json()
        correlation_id = body.get("correlation_id", "unknown")
        logger.info(f"Received assessment request: {correlation_id}")
        
        # Return a mock response that indicates AI processing is unavailable
        # This allows the system to gracefully degrade - officers can still review
        response = {
            "status": "failed",
            "error": {
                "code": "PROVIDER_CONFIGURATION",
                "message": "AI gateway mock - local testing only",
                "retryable": False,
                "retry_after_ms": None,
                "provider_status": None,
                "stage": "request"
            },
            "gateway_request_id": f"mock-{correlation_id[:16]}",
            "billing_state": "not-invoked",
            "provider": "mock",
            "model": None,
            "model_version": None,
            "usage": {
                "input_tokens": None,
                "output_tokens": None,
                "cached_input_tokens": None,
                "thinking_tokens": None,
                "total_tokens": None,
                "source": "unavailable"
            }
        }
        
        logger.info(f"Returning mock assessment for {correlation_id}")
        return JSONResponse(status_code=400, content=response)
        
    except Exception as e:
        logger.error(f"Error in mock assessment: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal mock server error", "detail": str(e)}
        )

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-gateway-mock"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Gateway Mock on http://127.0.0.1:9999")
    uvicorn.run(app, host="127.0.0.1", port=9999, log_level="info")
