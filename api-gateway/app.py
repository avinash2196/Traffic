"""API GATEWAY for RoadWatch Traffic MVP (port 8000).

Routes requests to appropriate microservices:
- /health → all services
- / → welcome
- /{filename}.html → serve frontend templates
- /api/auth/* → auth-service:8003
- /api/officer/* → auth-service:8003
- /api/media/* → citizen-api:8001
- /api/reports → citizen-api:8001
- /api/authority/* → officer-api:8002
"""

import os
from pathlib import Path
from contextlib import asynccontextmanager
import logging
from datetime import datetime, timezone
import httpx

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

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

os.environ.setdefault('APP_PROFILE', 'local')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service URLs
AUTH_SERVICE_URL = "http://127.0.0.1:9001"
CITIZEN_API_URL = "http://127.0.0.1:9002"
OFFICER_API_URL = "http://127.0.0.1:9003"


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown for API gateway."""
    logger.info("API GATEWAY STARTUP: Initializing api-gateway (port 8000)...")
    
    # Check if backend services are available
    try:
        async with httpx.AsyncClient() as client:
            for name, url in [
                ("auth-service", AUTH_SERVICE_URL),
                ("citizen-api", CITIZEN_API_URL),
                ("officer-api", OFFICER_API_URL)
            ]:
                try:
                    response = await client.get(f"{url}/health", timeout=5)
                    if response.status_code == 200:
                        logger.info(f"Backend {name} is healthy: {url}")
                    else:
                        logger.warning(f"Backend {name} returned status {response.status_code}")
                except Exception as e:
                    logger.warning(f"Backend {name} not ready yet: {e}")
    except Exception as e:
        logger.warning(f"Could not check backend services: {e}")
    
    yield  # App runs here
    
    # Shutdown
    logger.info("API GATEWAY SHUTDOWN: Closing api-gateway...")


# Create FastAPI app
app = FastAPI(
    title="RoadWatch API Gateway",
    description="API Gateway for microservices routing",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
    lifespan=lifespan
)

# Add CORS middleware to allow frontend apps to call API Gateway
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3001",  # Citizen frontend
        "http://127.0.0.1:3002",  # Officer frontend
        "http://localhost:3001",
        "http://localhost:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS)
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    logger.info(f"Static files mounted: {static_dir}")
else:
    logger.warning(f"Static directory not found: {static_dir}")

# Setup template rendering
templates_dir = Path("templates")
if templates_dir.exists():
    templates = Jinja2Templates(directory=str(templates_dir))
    logger.info(f"Templates loaded: {templates_dir}")
else:
    templates = None
    logger.warning(f"Templates directory not found: {templates_dir}")


# ============ UTILITY FUNCTIONS ============

async def proxy_request(
    url: str,
    method: str,
    headers: dict,
    body: bytes = None,
    params: dict = None
):
    """Proxy request to backend service."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Remove host header to avoid issues
            proxy_headers = dict(headers)
            proxy_headers.pop("host", None)
            proxy_headers.pop("connection", None)
            
            if method == "GET":
                response = await client.get(url, headers=proxy_headers, params=params)
            elif method == "POST":
                response = await client.post(url, headers=proxy_headers, content=body, params=params)
            elif method == "PUT":
                response = await client.put(url, headers=proxy_headers, content=body, params=params)
            elif method == "DELETE":
                response = await client.delete(url, headers=proxy_headers, params=params)
            else:
                return JSONResponse(
                    status_code=405,
                    content={"error": "Method not allowed"}
                )
            
            # Return response with appropriate content
            if response.status_code in [204, 304]:  # No content
                return JSONResponse(status_code=response.status_code, content={})
            
            content_type = response.headers.get("content-type", "")
            
            # Return binary content as-is (ZIP files, media)
            if "application/zip" in content_type or "image" in content_type or "video" in content_type:
                return response
            
            # Return JSON
            try:
                json_content = response.json()
                return JSONResponse(
                    status_code=response.status_code,
                    content=json_content,
                    headers=dict(response.headers)
                )
            except:
                return JSONResponse(
                    status_code=response.status_code,
                    content={"data": response.text}
                )
    
    except httpx.TimeoutException:
        logger.error(f"Request to {url} timed out")
        return JSONResponse(
            status_code=503,
            content={"error": "Backend service timeout"}
        )
    except Exception as e:
        logger.error(f"Error proxying request to {url}: {e}")
        return JSONResponse(
            status_code=502,
            content={"error": "Bad gateway"}
        )


# ============ HEALTH CHECK ============

@app.get("/health", tags=["Health"])
async def health_check():
    """Gateway health check - check all backend services."""
    status = {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "api-gateway",
        "backend_services": {}
    }
    
    async with httpx.AsyncClient() as client:
        for name, url in [
            ("auth-service", AUTH_SERVICE_URL),
            ("citizen-api", CITIZEN_API_URL),
            ("officer-api", OFFICER_API_URL)
        ]:
            try:
                response = await client.get(f"{url}/health", timeout=5)
                status["backend_services"][name] = {
                    "status": "healthy" if response.status_code == 200 else "degraded",
                    "status_code": response.status_code
                }
            except Exception as e:
                status["backend_services"][name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
    
    return JSONResponse(content=status)


# ============ PUBLIC ENDPOINTS ============

@app.get("/", tags=["Public"])
async def welcome():
    """Welcome endpoint with service info."""
    return {
        "service": "RoadWatch Traffic MVP - API Gateway",
        "version": "1.0.0",
        "documentation": "http://127.0.0.1:8000/api/docs",
        "citizen_portal": "http://127.0.0.1:8000/citizen",
        "authority_portal": "http://127.0.0.1:8000/authority"
    }


@app.get("/favicon.ico", tags=["Static"])
async def favicon():
    """Serve favicon (returns 204 No Content)."""
    return JSONResponse(status_code=204, content={})


@app.get("/{filename}.html", tags=["Static"])
async def serve_html(filename: str):
    """Serve HTML template files without authentication."""
    file_path = Path("templates") / f"{filename}.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return JSONResponse(status_code=404, content={"error": "Page not found"})


# ============ AUTH SERVICE ROUTES ============

@app.post("/api/auth/signup", tags=["Auth"])
async def proxy_auth_signup(request: Request):
    """Proxy to auth-service."""
    body = await request.body()
    return await proxy_request(
        f"{AUTH_SERVICE_URL}/api/auth/signup",
        "POST",
        dict(request.headers),
        body=body
    )


@app.post("/api/auth/login", tags=["Auth"])
async def proxy_auth_login(request: Request):
    """Proxy to auth-service."""
    body = await request.body()
    return await proxy_request(
        f"{AUTH_SERVICE_URL}/api/auth/login",
        "POST",
        dict(request.headers),
        body=body
    )


@app.post("/api/auth/logout", tags=["Auth"])
async def proxy_auth_logout(request: Request):
    """Proxy to auth-service."""
    return await proxy_request(
        f"{AUTH_SERVICE_URL}/api/auth/logout",
        "POST",
        dict(request.headers)
    )


@app.get("/api/auth/me", tags=["Auth"])
async def proxy_auth_me(request: Request):
    """Proxy to auth-service."""
    return await proxy_request(
        f"{AUTH_SERVICE_URL}/api/auth/me",
        "GET",
        dict(request.headers)
    )


# ============ OFFICER AUTH ROUTES ============

@app.post("/api/officer/register", tags=["Officer"])
async def proxy_officer_register(request: Request):
    """Proxy to auth-service."""
    body = await request.body()
    return await proxy_request(
        f"{AUTH_SERVICE_URL}/api/officer/register",
        "POST",
        dict(request.headers),
        body=body
    )


@app.post("/api/officer/login", tags=["Officer"])
async def proxy_officer_login(request: Request):
    """Proxy to auth-service."""
    body = await request.body()
    return await proxy_request(
        f"{AUTH_SERVICE_URL}/api/officer/login",
        "POST",
        dict(request.headers),
        body=body
    )


# ============ MEDIA ROUTES ============

@app.post("/api/media/upload", tags=["Media"])
async def proxy_media_upload(request: Request):
    """Proxy to citizen-api."""
    body = await request.body()
    return await proxy_request(
        f"{CITIZEN_API_URL}/api/media/upload",
        "POST",
        dict(request.headers),
        body=body
    )


@app.get("/api/media/{media_id}/{filename}", tags=["Media"])
async def proxy_media_download(request: Request, media_id: str, filename: str):
    """Proxy to citizen-api."""
    return await proxy_request(
        f"{CITIZEN_API_URL}/api/media/{media_id}/{filename}",
        "GET",
        dict(request.headers),
        params=dict(request.query_params)
    )


# ============ CITIZEN REPORT ROUTES ============

@app.post("/api/reports", tags=["Reports"])
async def proxy_submit_report(request: Request):
    """Proxy to citizen-api."""
    body = await request.body()
    return await proxy_request(
        f"{CITIZEN_API_URL}/api/reports",
        "POST",
        dict(request.headers),
        body=body
    )


@app.get("/api/reports", tags=["Reports"])
async def proxy_fetch_reports(request: Request, page: int = 1, page_size: int = 20):
    """Proxy to citizen-api."""
    return await proxy_request(
        f"{CITIZEN_API_URL}/api/reports",
        "GET",
        dict(request.headers),
        params={"page": page, "page_size": page_size}
    )


@app.get("/api/reports/{report_id}", tags=["Reports"])
async def proxy_fetch_report(request: Request, report_id: str):
    """Proxy to citizen-api."""
    return await proxy_request(
        f"{CITIZEN_API_URL}/api/reports/{report_id}",
        "GET",
        dict(request.headers)
    )


@app.post("/api/reports/{report_id}/clarification", tags=["Reports"])
async def proxy_submit_clarification(request: Request, report_id: str):
    """Proxy to citizen-api."""
    body = await request.body()
    return await proxy_request(
        f"{CITIZEN_API_URL}/api/reports/{report_id}/clarification",
        "POST",
        dict(request.headers),
        body=body
    )


# ============ OFFICER AUTHORITY ROUTES ============

@app.get("/api/authority/reports", tags=["Authority"])
async def proxy_fetch_queue(request: Request, page: int = 1, page_size: int = 10, status: str = None):
    """Proxy to officer-api."""
    params = {"page": page, "page_size": page_size}
    if status:
        params["status"] = status
    
    return await proxy_request(
        f"{OFFICER_API_URL}/api/authority/reports",
        "GET",
        dict(request.headers),
        params=params
    )


@app.get("/api/authority/reports/{report_id}", tags=["Authority"])
async def proxy_get_report_detail(request: Request, report_id: str):
    """Proxy to officer-api."""
    return await proxy_request(
        f"{OFFICER_API_URL}/api/authority/reports/{report_id}",
        "GET",
        dict(request.headers)
    )


@app.get("/api/authority/reports/{report_id}/media/{filename}", tags=["Authority"])
async def proxy_serve_media(request: Request, report_id: str, filename: str):
    """Proxy to officer-api."""
    return await proxy_request(
        f"{OFFICER_API_URL}/api/authority/reports/{report_id}/media/{filename}",
        "GET",
        dict(request.headers),
        params=dict(request.query_params)
    )


@app.post("/api/authority/reports/{report_id}/decision", tags=["Authority"])
async def proxy_make_decision(request: Request, report_id: str):
    """Proxy to officer-api."""
    body = await request.body()
    return await proxy_request(
        f"{OFFICER_API_URL}/api/authority/reports/{report_id}/decision",
        "POST",
        dict(request.headers),
        body=body
    )


@app.get("/api/authority/reports/{report_id}/evidence.zip", tags=["Authority"])
async def proxy_download_zip(request: Request, report_id: str):
    """Proxy to officer-api."""
    return await proxy_request(
        f"{OFFICER_API_URL}/api/authority/reports/{report_id}/evidence.zip",
        "GET",
        dict(request.headers)
    )


# ============ CORS PREFLIGHT ============

@app.options("/{full_path:path}", tags=["CORS"])
async def preflight_handler(full_path: str):
    """Handle CORS preflight requests."""
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=9000,
        reload=False,
        log_level="info"
    )
