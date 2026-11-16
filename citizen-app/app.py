from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from starlette.staticfiles import StaticFiles
from pathlib import Path
import os
import json

app = FastAPI(title="RoadWatch Citizen App")

@app.get("/favicon.ico")
async def favicon():
    """Return favicon (empty response to avoid 404)"""
    return Response(status_code=204)

# Config endpoint - frontend can fetch this to get API URLs
@app.get("/config")
async def get_config():
    """Get frontend configuration including API URLs"""
    citizen_api_port = os.getenv("CITIZEN_API_PORT", "9001")
    auth_service_port = os.getenv("AUTH_SERVICE_PORT", "9003")
    return {
        "api": {
            "citizen": f"http://127.0.0.1:{citizen_api_port}",
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
    return FileResponse(templates_path / "citizen-login.html")

@app.get("/login")
async def login():
    return FileResponse(templates_path / "citizen-login.html")

@app.get("/signup")
async def signup():
    return FileResponse(templates_path / "citizen-signup.html")

@app.get("/dashboard")
async def dashboard():
    return FileResponse(templates_path / "citizen-dashboard.html")

@app.get("/reports")
async def reports():
    return FileResponse(templates_path / "citizen-reports.html")

@app.get("/report")
async def report():
    return FileResponse(templates_path / "citizen-report.html")

@app.get("/report-detail")
async def report_detail():
    return FileResponse(templates_path / "citizen-report-detail.html")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "citizen-app"}

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.getenv("CITIZEN_APP_PORT", "3001"))
    uvicorn.run(app, host="127.0.0.1", port=port)
