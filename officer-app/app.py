from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from starlette.staticfiles import StaticFiles
from pathlib import Path
import os
import json

app = FastAPI(title="RoadWatch Officer App")

@app.get("/favicon.ico")
async def favicon():
    """Return favicon (empty response to avoid 404)"""
    return Response(status_code=204)

# Config endpoint - frontend can fetch this to get API URLs
@app.get("/config")
async def get_config():
    """Get frontend configuration including API URLs"""
    officer_api_port = os.getenv("OFFICER_API_PORT", "9002")
    auth_service_port = os.getenv("AUTH_SERVICE_PORT", "9003")
    return {
        "api": {
            "officer": f"http://127.0.0.1:{officer_api_port}",
            "auth": f"http://127.0.0.1:{auth_service_port}"
        }
    }

# Mount static files
static_path = Path(__file__).resolve().parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Serve templates
templates_path = Path(__file__).resolve().parent / "templates"

@app.get("/")
async def root():
    return FileResponse(templates_path / "officer-login.html")

@app.get("/login")
async def login():
    return FileResponse(templates_path / "officer-login.html")

@app.get("/signup")
async def signup():
    return FileResponse(templates_path / "officer-signup.html")

@app.get("/queue")
async def queue():
    return FileResponse(templates_path / "officer-queue.html")

@app.get("/detail")
async def detail():
    return FileResponse(templates_path / "officer-detail.html")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "officer-app"}

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("OFFICER_APP_PORT", "3002"))
    uvicorn.run(app, host="127.0.0.1", port=port)
