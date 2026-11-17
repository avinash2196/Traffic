import sys
from pathlib import Path

# Add parent directory to path to find shared modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging

# Load environment
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import AI gateway assessment functions
try:
    from ai_gateway_mvp import assess_violation
    logger.info("✓ AI Gateway MVP loaded successfully")
    AI_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Could not import AI modules: {e}")
    AI_AVAILABLE = False
    assess_violation = None

app = FastAPI(title="RoadWatch AI Gateway")

class AnalyzeRequest(BaseModel):
    report_id: str
    media_items: list = None
    settings: dict = None

@app.post("/api/ai/analyze")
async def analyze_report(body: AnalyzeRequest):
    """Analyze report with AI assessment"""
    if not AI_AVAILABLE:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    
    try:
        # Simple AI assessment - just return a mock assessment for MVP
        # TODO: Convert to real assess_violation when request format is aligned
        result = {
            "report_id": body.report_id,
            "status": "assessed",
            "assessment": {
                "relevance": "relevant",
                "violation_confidence": 0.85,
                "recommendation": "award-points",
                "explanation": "Evidence appears to support the violation claim",
                "observations": []
            },
            "timestamp": str(__import__('datetime').datetime.utcnow().isoformat())
        }
        return result
    except Exception as e:
        logger.error(f"AI analysis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/status")
async def ai_status():
    """Get AI gateway status"""
    return {
        "status": "ready" if AI_AVAILABLE else "unavailable",
        "providers": {
            "openai": os.getenv("OPENAI_API_KEY") is not None,
            "gemini": os.getenv("GEMINI_API_KEY") is not None
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "ai-gateway",
        "ai_available": AI_AVAILABLE
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("AI_GATEWAY_PORT", "9004"))
    uvicorn.run(app, host="127.0.0.1", port=port)
