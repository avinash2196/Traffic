"""AI Gateway Service - Routes assessment requests to real AI providers (Gemini/OpenAI).

This service:
1. Receives assessment requests at /v1/assessments
2. Routes them to Gemini or OpenAI APIs
3. Returns structured assessment results

No mocking - all assessments are real AI calls.
"""

import sys
from pathlib import Path

# Add parent directory to path to find shared modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
import os
from dotenv import load_dotenv
import logging

# Load environment
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import real AI gateway assessment
try:
    from assessment import app as assessment_app, assess_violation
    logger.info("✓ AI Gateway Assessment Service (real Gemini/OpenAI) loaded successfully")
    AI_AVAILABLE = True
except ImportError as e:
    logger.error(f"Could not import Assessment Service: {e}")
    AI_AVAILABLE = False
    assess_violation = None

# Create app - use the MVP app directly (which has /v1/assessments endpoint)
app = FastAPI(title="RoadWatch AI Gateway")

# Mount the real MVP assessment endpoint
@app.get("/health")
async def health():
    """Health check - confirms AI Gateway is running."""
    return {
        "status": "healthy",
        "service": "ai-gateway",
        "assessment_endpoint": "/v1/assessments",
        "ai_available": AI_AVAILABLE,
        "providers": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "gemini": bool(os.getenv("GEMINI_API_KEY"))
        }
    }

# Include the real MVP app routes
if AI_AVAILABLE:
    @app.post("/v1/assessments")
    async def forward_assessment_request(request):
        """Forward assessment requests to real AI providers.
        
        Expects:
        - Authorization: Bearer <token>
        - Body with:
          - correlation_id
          - attempt_id
          - attempt_number
          - evidence_revision
          - selection (provider: openai|gemini)
          - prompt (text, version)
          - evidence (array with media_id, mime_type, data_base64)
        
        Returns real AI assessment from Gemini or OpenAI.
        """
        return await assess_violation(request)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("AI_GATEWAY_PORT", "9004"))
    uvicorn.run(app, host="127.0.0.1", port=port)
