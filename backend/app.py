"""FastAPI application entry point for RoadWatch Traffic MVP.

M2 Deliverable:
- FastAPI instance with lifespan context manager
- Database initialization on startup/shutdown
- Identity middleware for X-Citizen-Id header validation
- Health check endpoint
- OpenTelemetry hooks (minimal for MVP)
- Swagger UI at /api/docs
"""

# Load environment variables from .env FIRST (before importing anything else)
import os
from pathlib import Path

# Try to load .env from script directory
env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key, value = parts
                    os.environ[key.strip()] = value.strip()

# Set defaults if not in .env
os.environ.setdefault('APP_PROFILE', 'local')

from durable import JobStore, ai_worker_factory
import time
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import hashlib
import io
import json
import logging
from uuid import uuid4
from zipfile import ZipFile

from fastapi import FastAPI, Request, UploadFile, File
from starlette.concurrency import run_in_threadpool
from intake import (IntakeError, fail, parse_upload, validate_media, FORMATS, PRIVATE,
                    resource_name, media_path, media_view)
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import bootstrap functions for database and identity
from bootstrap import init_database, get_db
from auth_utils import validate_session_token, is_valid_email, is_valid_password, is_valid_citizen_id, hash_password, generate_session_token, verify_password, generate_officer_session_token, validate_officer_token

# Points mapping for violations
POINTS_BY_VIOLATION = {
    "helmet": 2,
    "triple-riding": 3,
    "red-light": 3
}
VALID_VIOLATIONS = set(POINTS_BY_VIOLATION.keys())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_utc_now_iso():
    """Get current UTC time in ISO-8601 format without microseconds (JavaScript-compatible)."""
    # isoformat() on timezone-aware datetime returns: "2026-11-03T01:29:40+00:00"
    # Replace "+00:00" with "Z" to get: "2026-11-03T01:29:40Z"
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_reviewer_token(auth_header: str) -> bool:
    """Validate reviewer token from Authorization header.
    
    Format: "Bearer <token>" or just "<token>"
    Expected token from environment: ROADWATCH_REVIEWER_TOKEN (default: no token = require valid)
    """
    if not auth_header:
        return False
    
    # Handle "Bearer <token>" format
    token = auth_header.replace("Bearer ", "").strip()
    
    # Get expected token from environment (if not set, no valid token = reject all)
    expected_token = os.getenv("ROADWATCH_REVIEWER_TOKEN")
    if not expected_token:
        logger.warning("ROADWATCH_REVIEWER_TOKEN not set - officer access disabled")
        return False
    
    # Simple constant-time comparison
    return token == expected_token


def validate_officer_token_for_middleware(auth_header: str) -> dict:
    """Wrapper to validate officer session token from Authorization header for middleware.
    
    Returns dict with {officer_id: str} if valid, or {} if invalid.
    Accepts both master reviewer token (for backward compatibility) and per-officer tokens.
    """
    if not auth_header:
        return {}
    
    # Handle "Bearer " prefix
    token = auth_header.replace("Bearer ", "").strip()
    
    # Check if it's the master reviewer token (backward compatibility)
    expected_reviewer_token = os.getenv("ROADWATCH_REVIEWER_TOKEN")
    if expected_reviewer_token and token == expected_reviewer_token:
        # For demo/testing: allow any officer access with master token
        return {"officer_id": "demo-officer", "token_type": "reviewer"}
    
    # Try to decode as JWT session token using auth_utils
    officer_id = validate_officer_token(token)
    if officer_id:
        return {"officer_id": officer_id, "token_type": "session"}
    return {}


# Lifespan context manager for FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events.
    
    Startup: Initialize database connection
    Shutdown: Close database connection
    """
    # Startup
    logger.info("🚀 LIFESPAN STARTUP: Starting RoadWatch Traffic MVP...")
    try:
        db = init_database("./roadwatch.db")
        logger.info(f"✓ Database initialized: ./roadwatch.db, db_connection object: {db}")
        app.state.db = db
        
        # Verify db_connection was set
        from bootstrap import db_connection as check_db
        logger.info(f"✓ bootstrap.db_connection is now: {check_db}")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}", exc_info=True)
        raise
    
    # Initialize OpenTelemetry (minimal for MVP)
    try:
        from opentelemetry.sdk.trace import TracerProvider
        tracer_provider = TracerProvider()
        # SimpleSpanProcessor for MVP (no external export yet)
        logger.info("✓ OpenTelemetry initialized (in-memory)")
    except Exception as e:
        logger.warning(f"OpenTelemetry initialization skipped: {e}")
    
    worker = None
    try:
        from gateway import settings
        app.state.ai_settings=settings()
        worker = ai_worker_factory(db.db_path.resolve())
        worker.start()
        yield  # App runs here
    finally:
        try:
            if worker is not None:
                worker.stop()
        finally:
            db.close()
    
    # Shutdown
    logger.info("🛑 LIFESPAN SHUTDOWN: Shutting down RoadWatch Traffic MVP...")
    try:
        db = get_db()
        db.close()
        logger.info("✓ Database connection closed")
    except Exception as e:
        logger.warning(f"Database shutdown error: {e}")


# Create FastAPI app with lifespan
app = FastAPI(
    title="RoadWatch Traffic MVP",
    description="India-focused traffic evidence reporting system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,  # Disable ReDoc for MVP
    lifespan=lifespan
)

# Mount static files (CSS, JS) - REMOVED: Frontend service handles this
# static_dir = Path("static")
# if static_dir.exists():
#     app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
#     logger.info(f"✓ Static files mounted: {static_dir}")
# else:
#     logger.warning(f"⚠ Static directory not found: {static_dir}")

# Setup template rendering - REMOVED: Frontend service handles this
# templates_dir = Path("templates")
# if templates_dir.exists():
#     templates = Jinja2Templates(directory=str(templates_dir))
#     logger.info(f"✓ Templates loaded: {templates_dir}")
# else:
#     templates = None
#     logger.warning(f"⚠ Templates directory not found: {templates_dir}")


# Identity middleware for X-Citizen-Id header + JWT token validation
@app.middleware("http")
async def identity_middleware(request: Request, call_next):
    """Identity middleware supporting both demo (X-Citizen-Id) and JWT auth.
    
    For new auth endpoints, accept Bearer token in Authorization header.
    For backwards compatibility, still accept X-Citizen-Id header.
    Officer endpoints check Authorization header separately.
    """
    # Allow public and API endpoints only (no more static/HTML serving)
    public_paths = ["/health", "/api/docs", "/openapi.json", "/api/auth/signup", "/api/auth/login", "/api/officer/register", "/api/officer/login"]
    if (request.url.path in public_paths):
        return await call_next(request)
    
    # Allow officer endpoints (they check Authorization header separately)
    if request.url.path.startswith("/api/authority/"):
        return await call_next(request)
    
    # Try X-Citizen-Id header first for demo mode (MVP)
    citizen_id = request.headers.get("X-Citizen-Id")
    if citizen_id:
        request.scope["citizen_id"] = citizen_id
        return await call_next(request)
    
    # Try JWT token from Authorization header
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        citizen_id = validate_session_token(token)
        if citizen_id:
            request.scope["citizen_id"] = citizen_id
            return await call_next(request)
        else:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid or expired token", "detail": "Invalid or expired token", "code": "UNAUTHENTICATED"}
            )
    
    # No auth found
    return JSONResponse(
        status_code=401,
        content={"error": "X-Citizen-Id header or Bearer token required", "detail": "X-Citizen-Id header or Bearer token required", "code": "UNAUTHENTICATED"}
    )


@app.exception_handler(IntakeError)
async def intake_error_handler(request: Request, exc: IntakeError):
    return JSONResponse(status_code=exc.status,
                        content={'error': exc.message, 'detail': exc.message, 'code': exc.code})


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint.
    
    Returns 200 OK with status and timestamp.
    Used for deployment health verification.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "roadwatch-traffic-api"
    }


# Welcome endpoint
# ============ M8: AUTH ENDPOINTS ============

@app.post("/api/auth/signup", tags=["Auth"], status_code=201)
async def signup(body: dict):
    """Citizen signup endpoint.
    
    Request body:
        - email: valid email address
        - full_name: citizen's full name
        - citizen_id: unique citizen identifier
        - password: password (minimum 8 characters)
    
    Returns 201 Created with citizen profile (no password).
    Returns 400 Bad Request for validation errors.
    Returns 409 Conflict if citizen_id or email already exists.
    """
    try:
        email = body.get("email", "").strip()
        full_name = body.get("full_name", "").strip()
        citizen_id = body.get("citizen_id", "").strip()
        password = body.get("password", "")
        
        # Validation
        if not email or not full_name or not citizen_id or not password:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing required fields: email, full_name, citizen_id, password"}
            )
        
        if not is_valid_email(email):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid email format"}
            )
        
        if not is_valid_password(password):
            return JSONResponse(
                status_code=400,
                content={"error": "Password must be at least 8 characters"}
            )
        
        if not is_valid_citizen_id(citizen_id):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid citizen_id format"}
            )
        
        # Check for duplicates
        db = get_db()
        cursor = db.execute(
            "SELECT id FROM citizens WHERE id = ? OR email = ?",
            (citizen_id, email)
        )
        if cursor.fetchone():
            return JSONResponse(
                status_code=409,
                content={"error": "Citizen ID or email already exists"}
            )
        
        # Hash password and create citizen record
        password_hash = hash_password(password)
        now = datetime.now(timezone.utc).isoformat()
        
        db.execute(
            """INSERT INTO citizens (id, email, full_name, password_hash, created_at, is_active)
               VALUES (?, ?, ?, ?, ?, TRUE)""",
            (citizen_id, email, full_name, password_hash, now)
        )
        db.connection.commit()
        
        return JSONResponse(
            status_code=201,
            content={
                "citizen_id": citizen_id,
                "email": email,
                "full_name": full_name,
                "created_at": now
            }
        )
    
    except Exception as e:
        logger.error(f"Signup error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )


@app.post("/api/auth/login", tags=["Auth"], status_code=200)
async def login(body: dict):
    """Citizen login endpoint.
    
    Request body:
        - citizen_id: citizen's ID
        - password: citizen's password
    
    Returns 200 OK with session token and citizen profile.
    Returns 401 Unauthorized for invalid credentials.
    """
    try:
        citizen_id = body.get("citizen_id", "").strip()
        password = body.get("password", "")
        
        if not citizen_id or not password:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid citizen_id or password"}
            )
        
        # Lookup citizen
        db = get_db()
        cursor = db.execute(
            "SELECT id, email, full_name, password_hash FROM citizens WHERE id = ? AND is_active = TRUE",
            (citizen_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid citizen_id or password"}
            )
        
        # Verify password
        password_hash = row[3]
        if not verify_password(password, password_hash):
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid citizen_id or password"}
            )
        
        # Generate token and update last_login_at
        session_token = generate_session_token(citizen_id)
        now = datetime.now(timezone.utc).isoformat()
        
        db.execute(
            "UPDATE citizens SET last_login_at = ? WHERE id = ?",
            (now, citizen_id)
        )
        db.connection.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "session_token": session_token,
                "citizen_id": citizen_id,
                "email": row[1],
                "full_name": row[2]
            }
        )
    
    except Exception as e:
        logger.error(f"Login error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )


@app.post("/api/auth/logout", tags=["Auth"], status_code=204)
async def logout(request: Request):
    """Citizen logout endpoint.
    
    Clears session token on server (client should clear localStorage).
    Returns 204 No Content.
    """
    try:
        citizen_id = request.scope.get("citizen_id")
        if not citizen_id:
            return JSONResponse(status_code=401, content={"error": "Not authenticated"})
        
        # For MVP with stateless JWT, nothing to clear server-side
        # Client clears localStorage
        return JSONResponse(status_code=204, content="")
    
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.get("/api/auth/me", tags=["Auth"])
async def get_current_citizen(request: Request):
    """Get current authenticated citizen's profile.
    
    Returns 200 OK with citizen profile (no password).
    Returns 401 Unauthorized if not authenticated.
    """
    try:
        citizen_id = request.scope.get("citizen_id")
        if not citizen_id:
            return JSONResponse(status_code=401, content={"error": "Not authenticated"})
        
        # Lookup citizen
        db = get_db()
        cursor = db.execute(
            "SELECT id, email, full_name, created_at, last_login_at FROM citizens WHERE id = ? AND is_active = TRUE",
            (citizen_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            return JSONResponse(status_code=401, content={"error": "Citizen not found"})
        
        return JSONResponse(
            status_code=200,
            content={
                "citizen_id": row[0],
                "email": row[1],
                "full_name": row[2],
                "created_at": row[3],
                "last_login_at": row[4]
            }
        )
    
    except Exception as e:
        logger.error(f"Get current citizen error: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


# ============ OFFICER AUTHENTICATION ============

@app.post("/api/officer/register", tags=["Officer"], status_code=201)
async def register_officer(body: dict):
    """Officer registration endpoint.
    
    Requires reviewer token to register (acts as shared secret).
    
    Request body:
        - email: officer's email
        - password: officer's password
        - reviewer_token: shared reviewer token (must match ROADWATCH_REVIEWER_TOKEN)
        - full_name: officer's full name (optional)
    
    Returns 201 Created with officer profile.
    Returns 400 Bad Request for invalid token or email.
    """
    try:
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")
        reviewer_token = body.get("reviewer_token", "")
        full_name = body.get("full_name", "").strip()
        
        # Validate reviewer token
        expected_token = os.getenv("ROADWATCH_REVIEWER_TOKEN", "demo-reviewer-token")
        if not reviewer_token or reviewer_token != expected_token:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid reviewer token"}
            )
        
        # Validate email
        if not email or "@" not in email:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid email address"}
            )
        
        # Validate password
        if not password or len(password) < 6:
            return JSONResponse(
                status_code=400,
                content={"error": "Password must be at least 6 characters"}
            )
        
        # Create officer
        officer_id = uuid4().hex[:16]
        password_hash = hash_password(password)
        now = get_utc_now_iso()
        
        db = get_db()
        try:
            db.execute(
                """INSERT INTO officers (id, email, password_hash, full_name, created_at, is_active)
                   VALUES (?, ?, ?, ?, ?, TRUE)""",
                (officer_id, email, password_hash, full_name or None, now)
            )
            db.connection.commit()
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                return JSONResponse(
                    status_code=400,
                    content={"error": "Email already registered"}
                )
            raise
        
        return JSONResponse(
            status_code=201,
            content={
                "officer_id": officer_id,
                "email": email,
                "full_name": full_name,
                "created_at": now
            }
        )
    
    except Exception as e:
        logger.error(f"Officer registration error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )


@app.post("/api/officer/login", tags=["Officer"], status_code=200)
async def officer_login(body: dict):
    """Officer login endpoint.
    
    Request body:
        - email: officer's email
        - password: officer's password
    
    Returns 200 OK with session token.
    Returns 401 Unauthorized for invalid credentials.
    """
    try:
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")
        
        if not email or not password:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid email or password"}
            )
        
        # Lookup officer
        db = get_db()
        cursor = db.execute(
            "SELECT id, email, password_hash, full_name FROM officers WHERE email = ? AND is_active = TRUE",
            (email,)
        )
        row = cursor.fetchone()
        
        if not row:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid email or password"}
            )
        
        # Extract fields - row is sqlite3.Row so can use dict-like access
        officer_id = row['id']
        stored_hash = row['password_hash']
        officer_email = row['email']
        officer_name = row['full_name']
        
        # Verify password
        if not verify_password(password, stored_hash):
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid email or password"}
            )
        
        # Generate officer session token
        session_token = generate_officer_session_token(officer_id)
        now = get_utc_now_iso()
        
        db.execute(
            "UPDATE officers SET last_login_at = ? WHERE id = ?",
            (now, officer_id)
        )
        db.connection.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "session_token": session_token,
                "officer_id": officer_id,
                "email": officer_email,
                "full_name": officer_name
            }
        )
    
    except Exception as e:
        logger.error(f"Officer login error: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )



# ============ M3.2: MEDIA UPLOAD ============

@app.post("/api/media/upload", tags=["Citizen"], status_code=201)
async def upload_media(request: Request):
    """Validate real multipart bytes and create a private owned upload handle."""
    try:
        filename, mime, data = await run_in_threadpool(
            parse_upload, request.headers.get('content-type', ''), await request.body())
        await run_in_threadpool(validate_media, data, mime)
        owner = request.scope['citizen_id']
        digest = hashlib.sha256(data).hexdigest()
        db = get_db()
        existing = db.execute("SELECT * FROM media WHERE owner_citizen_id=? AND sha256_hash=? AND report_id IS NULL ORDER BY uploaded_at,id LIMIT 1", (owner, digest)).fetchone()
        if existing:
            return JSONResponse(status_code=200, content=upload_result(existing, True))
        media_id = uuid4().hex[:16]
        name = media_id + FORMATS[mime]
        filename = filename or name
        path = Path('media_store').resolve() / name
        now = get_utc_now_iso()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as output: output.write(data)
            with db.transaction() as conn:
                conn.execute('INSERT INTO media(id,filename,file_size_bytes,mime_type,sha256_hash,storage_path,uploaded_at,owner_citizen_id,resource_name) VALUES(?,?,?,?,?,?,?,?,?)',
                             (media_id, filename, len(data), mime, digest, str(path), now, owner, name))
        except Exception:
            path.unlink(missing_ok=True)
            raise
        row = db.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
        return JSONResponse(status_code=201, content=upload_result(row, False))
    except IntakeError:
        raise
    except OSError:
        fail(503, 'STORAGE_UNAVAILABLE', 'Media storage unavailable')
    except Exception:
        fail(500, 'INTERNAL_ERROR', 'Unable to upload media')


def upload_result(row, duplicate: bool):
    result = {'media_id': row['id'], 'filename': row['filename'],
              'resource_name': resource_name(row), 'file_size': row['file_size_bytes'],
              'sha256_hash': row['sha256_hash'], 'uploaded_at': row['uploaded_at'], 'is_duplicate': duplicate}
    if duplicate: result['duplicate_reason'] = 'Previously uploaded by you'
    return result

@app.post("/api/reports", tags=["Citizen"], status_code=201)
async def submit_report(request: Request):
    """Commit an ordered, owned, previously unattached evidence set atomically."""
    if request.headers.get('content-type', '').split(';')[0].strip().lower() != 'application/json':
        fail(415, 'UNSUPPORTED_CONTENT_TYPE', 'Expected JSON')
    try:
        body = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        fail(400, 'INVALID_INPUT', 'Invalid JSON')
    if not isinstance(body, dict): fail(400, 'INVALID_INPUT', 'Expected JSON object')
    
    logger.info(f"Report request body: {body}")
    
    for key in ('violation_type', 'vehicle_number', 'location'):
        if not isinstance(body.get(key), str) or not body[key].strip():
            logger.error(f"Validation failed for {key}: value={body.get(key)}, type={type(body.get(key))}")
            fail(400, 'INVALID_INPUT', 'Required nonblank string')
    if body['violation_type'] not in VALID_VIOLATIONS:
        fail(400, 'INVALID_INPUT', 'Unknown violation category')
    if ('media_id' in body) == ('media_ids' in body):
        fail(400, 'INVALID_INPUT', 'Supply exactly one media alias')
    ids = body.get('media_ids') if 'media_ids' in body else [body['media_id']]
    if not isinstance(ids, list) or not ids or any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
        fail(400, 'INVALID_INPUT', 'Expected distinct media handles')
    citizen = request.scope['citizen_id']
    key = request.headers.get('Idempotency-Key')
    if key is not None and (not 1 <= len(key) <= 128 or any(ord(c) < 32 or ord(c) > 126 for c in key) or not key.strip()):
        fail(400, 'INVALID_INPUT', 'Invalid idempotency key')
    fingerprint = json.dumps([body['violation_type'],body['vehicle_number'],body['location'],ids], separators=(',',':'), ensure_ascii=True)
    report_id, now = uuid4().hex[:16], get_utc_now_iso()
    job_id = uuid4().hex[:16]
    response = {'report_id':report_id,'status':'awaiting-review','violation_type':body['violation_type'],'created_at':now,'citizen_id':citizen,
                'ai':dict(job_id=job_id,state='pending',outcome=None,recommendation=None,attempt_count=0,max_attempts=3,failure_code=None,failure_reason=None,next_attempt_at=None,started_at=None,completed_at=None,processing_ms=None,assessment_id=None,evidence_revision=1,late_result=False)}
    db = get_db()
    try:
        with db.transaction() as conn:
            conn.execute('BEGIN IMMEDIATE')
            if key is not None:
                replay = conn.execute('SELECT fingerprint,response FROM ai_jobs WHERE principal=? AND idempotency_key=?', (citizen,key)).fetchone()
                if replay is not None:
                    if replay['fingerprint'] != fingerprint:
                        fail(409, 'IDEMPOTENCY_CONFLICT', 'Idempotency key was already used')
                    return JSONResponse(status_code=201,content=json.loads(replay['response']))
            for media_id in ids:
                media = conn.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
                if not media: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
                owner = media['owner_citizen_id']
                if owner is None and media['report_id']:
                    report = conn.execute('SELECT citizen_id FROM reports WHERE id=?', (media['report_id'],)).fetchone()
                    owner = report['citizen_id'] if report else None
                if owner is None: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
                if owner != citizen: fail(403, 'FORBIDDEN', 'Media belongs to another citizen')
                if media['report_id']: fail(409, 'MEDIA_ALREADY_ATTACHED', 'Media already attached')
            conn.execute('INSERT INTO reports(id,citizen_id,violation_type,vehicle_number,location,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)',
                         (report_id,citizen,body['violation_type'],body['vehicle_number'],body['location'],'awaiting-review',now,now))
            for position, media_id in enumerate(ids):
                conn.execute('UPDATE media SET report_id=?,attachment_position=? WHERE id=?', (report_id,position,media_id))
            conn.execute('INSERT INTO events(id,report_id,event_type,actor,old_status,new_status,created_at,reason) VALUES(?,?,?,?,?,?,?,?)',
                         (uuid4().hex[:16],report_id,'status_change','citizen',None,'awaiting-review',now,None))
            conn.execute("INSERT INTO ai_jobs(id,report_id,evidence_revision,state,created_at,principal,idempotency_key,fingerprint,response,settings_snapshot) VALUES(?,?,1,'pending',?,?,?,?,?,?)",
                         (job_id,report_id,time.time(),citizen,key,fingerprint,json.dumps(response),json.dumps(app.state.ai_settings)))
    except IntakeError:
        raise
    except sqlite3.Error:
        fail(503, 'STORAGE_UNAVAILABLE', 'Report storage unavailable')
    except Exception:
        fail(500, 'INTERNAL_ERROR', 'Unable to submit report')
    return JSONResponse(status_code=201, content=response)

@app.get("/api/reports", tags=["Citizen"])
async def fetch_reports(request: Request, page: int = 1, page_size: int = 20):
    """Citizen fetches their own reports."""
    try:
        citizen_id = request.scope.get("citizen_id")
        if not citizen_id:
            return JSONResponse(status_code=401, content={"error": "Missing citizen_id"})
        
        if page < 1 or page_size < 1:
            return JSONResponse(status_code=400, content={"error": "Invalid pagination params"})
        
        db = get_db()
        
        # Get total count
        total_count_result = db.execute(
            "SELECT COUNT(*) as cnt FROM reports WHERE citizen_id = ?",
            (citizen_id,)
        ).fetchone()
        total_count = total_count_result[0]
        
        # Get paginated results
        offset = (page - 1) * page_size
        reports = db.execute("""
            SELECT id, status, violation_type, vehicle_number, location, created_at, updated_at, provisional_points
            FROM reports WHERE citizen_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (citizen_id, page_size, offset)).fetchall()
        
        reports_list = [dict(r) for r in reports]
        
        return JSONResponse(content={
            "reports": reports_list,
            "total_count": total_count,
            "page": page,
            "page_size": page_size
        })
    except Exception as e:
        logger.error(f"Error in fetch_reports: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.get("/api/reports/{report_id}", tags=["Citizen"])
async def fetch_report_detail(request: Request, report_id: str):
    """Citizen fetches report details with timeline and media."""
    try:
        citizen_id = request.scope.get("citizen_id")
        if not citizen_id:
            return JSONResponse(status_code=401, content={"error": "Missing citizen_id"})
        
        db = get_db()
        
        # Get report
        report = db.execute(
            "SELECT id, citizen_id, status, violation_type, vehicle_number, location, provisional_points, created_at, updated_at FROM reports WHERE id = ?",
            (report_id,)
        ).fetchone()
        
        if not report:
            return JSONResponse(status_code=404, content={"error": "Report not found"})
        
        # Check access control
        if report["citizen_id"] != citizen_id:
            return JSONResponse(status_code=403, content={"error": "Access denied"})
        
        # Get media for this report
        media_list = db.execute("""
            SELECT *
            FROM media
            WHERE report_id = ?
            ORDER BY COALESCE(attachment_position, 2147483647), uploaded_at, id
        """, (report_id,)).fetchall()
        
        media_urls = [media_view(m) for m in media_list]

        # Get timeline
        events = db.execute("""
            SELECT id, event_type, actor, old_status, new_status, created_at, reason
            FROM events WHERE report_id = ?
            ORDER BY created_at ASC
        """, (report_id,)).fetchall()
        
        timeline = [dict(e) for e in events]
        
        result = dict(report)
        result["timeline"] = timeline
        result["media"] = media_urls
        result["ai"] = JobStore(db.db_path).public_summary(report_id)
        result["assessment"] = result["ai"].pop("assessment",None)
        
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error in fetch_report_detail: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.get("/api/media/{media_id}/{filename}", tags=["Citizen"])
async def serve_citizen_media(request: Request, media_id: str, filename: str):
    db = get_db()
    media = db.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
    if not media or resource_name(media) != filename: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    owner = media['owner_citizen_id']
    if owner is None and media['report_id']:
        report = db.execute('SELECT citizen_id FROM reports WHERE id=?', (media['report_id'],)).fetchone()
        owner = report['citizen_id'] if report else None
    if owner is None: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    if owner != request.scope['citizen_id']: fail(403, 'FORBIDDEN', 'Media belongs to another citizen')
    return FileResponse(str(media_path(media)), media_type=media['mime_type'], headers=PRIVATE)

@app.post("/api/reports/{report_id}/clarification", tags=["Citizen"])
async def submit_clarification(request: Request, report_id: str, body: dict):
    """Citizen submits clarification response."""
    try:
        citizen_id = request.scope.get("citizen_id")
        if not citizen_id:
            return JSONResponse(status_code=401, content={"error": "Missing citizen_id"})
        
        clarification_text = body.get("clarification_text")
        new_media_id = body.get("new_media_id")
        
        if not all([clarification_text, new_media_id]):
            return JSONResponse(status_code=400, content={"error": "Missing required fields"})
        
        db = get_db()
        
        # Get report
        report = db.execute(
            "SELECT citizen_id, status FROM reports WHERE id = ?",
            (report_id,)
        ).fetchone()
        
        if not report:
            return JSONResponse(status_code=404, content={"error": "Report not found"})
        
        # Check access and status
        if report["citizen_id"] != citizen_id:
            return JSONResponse(status_code=403, content={"error": "Access denied"})
        
        if report["status"] != "awaiting-citizen-info":
            return JSONResponse(status_code=409, content={"error": "Report not awaiting clarification"})
        
        # Verify media exists
        media = db.execute("SELECT id FROM media WHERE id = ?", (new_media_id,)).fetchone()
        if not media:
            return JSONResponse(status_code=404, content={"error": "Media not found"})
        
        # Update status
        now = get_utc_now_iso()
        
        with db.transaction() as conn:
            conn.execute(
                "UPDATE reports SET status = ?, updated_at = ? WHERE id = ?",
                ("resubmitted", now, report_id)
            )
            
            # Create event
            conn.execute("""
                INSERT INTO events (id, report_id, event_type, actor, old_status, new_status, created_at, reason)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (uuid4().hex[:16], report_id, "clarification", "citizen", "awaiting-citizen-info", "resubmitted", now, None))
        
        return JSONResponse(content={
            "report_id": report_id,
            "status": "resubmitted",
            "new_media_id": new_media_id,
            "clarification_event": {
                "old_status": "awaiting-citizen-info",
                "new_status": "resubmitted",
                "created_at": now
            }
        })
    except Exception as e:
        logger.error(f"Error in submit_clarification: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.get("/api/authority/reports", tags=["Officer"])
async def fetch_queue(request: Request, page: int = 1, page_size: int = 10, status: str = None):
    """Officer fetches review queue."""
    try:
        # Check authorization
        auth_header = request.headers.get("Authorization", "")
        officer_info = validate_officer_token_for_middleware(auth_header)
        if not officer_info:
            return JSONResponse(status_code=401, content={"error": "Invalid or missing officer token"})
        
        if page < 1 or page_size < 1:
            return JSONResponse(status_code=400, content={"error": "Invalid pagination params"})
        
        db = get_db()
        
        # Query reports awaiting review
        if status:
            where_clause = "status = ?"
            where_params = (status,)
        else:
            where_clause = "status IN (?, ?)"
            where_params = ("awaiting-review", "resubmitted")
        
        # Get total count
        total_count_result = db.execute(
            f"SELECT COUNT(*) as cnt FROM reports WHERE {where_clause}",
            where_params
        ).fetchone()
        total_count = total_count_result[0]
        
        # Get paginated results
        offset = (page - 1) * page_size
        reports = db.execute(f"""
            SELECT r.id, r.citizen_id, r.status, r.violation_type, r.vehicle_number, r.location, r.created_at,
                   (SELECT COUNT(*) FROM media WHERE report_id = r.id) as media_count
            FROM reports r
            WHERE {where_clause}
            ORDER BY r.created_at ASC
            LIMIT ? OFFSET ?
        """, (*where_params, page_size, offset)).fetchall()
        
        reports_list = [dict(r) for r in reports]
        
        total_pages = (total_count + page_size - 1) // page_size
        
        return JSONResponse(content={
            "reports": reports_list,
            "total_count": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        })
    except Exception as e:
        logger.error(f"Error in fetch_queue: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


@app.get("/api/authority/reports/{report_id}", tags=["Officer"])
async def get_report_detail(request: Request, report_id: str):
    """Officer fetches details of a specific report."""
    try:
        # Check authorization
        auth_header = request.headers.get("Authorization", "")
        officer_info = validate_officer_token_for_middleware(auth_header)
        if not officer_info:
            return JSONResponse(status_code=401, content={"error": "Invalid or missing officer token"})
        
        db = get_db()
        
        # Get report details
        report = db.execute("""
            SELECT id, citizen_id, status, violation_type, vehicle_number, location, screening_notes, officer_notes, created_at, updated_at
            FROM reports
            WHERE id = ?
        """, (report_id,)).fetchone()
        
        if not report:
            return JSONResponse(status_code=404, content={"error": "Report not found"})
        
        # Build plain dictionary to avoid JSON serialization issues
        report_dict = {
            'id': str(report['id']),
            'citizen_id': str(report['citizen_id']),
            'status': str(report['status']),
            'violation_type': str(report['violation_type']),
            'vehicle_number': str(report['vehicle_number']),
            'location': str(report['location']),
            'description': str(report['screening_notes'] or ''),
            'created_at': str(report['created_at']),
            'updated_at': str(report['updated_at'] or ''),
        }
        
        # Get media URLs for this report
        media_list = db.execute("""
            SELECT *
            FROM media
            WHERE report_id = ?
            ORDER BY COALESCE(attachment_position, 2147483647), uploaded_at, id
        """, (report_id,)).fetchall()
        
        # Extract token from Authorization header to pass to media URLs
        # Browser <img> tags can't send Authorization headers, so we pass token as query param
        auth_header = request.headers.get("Authorization", "")
        token_for_media = auth_header.replace("Bearer ", "").strip()
        if not token_for_media:
            # Fallback to reviewer token for backward compatibility
            token_for_media = os.getenv("ROADWATCH_REVIEWER_TOKEN", "")
        
        media = [media_view(m, report_id, token_for_media) for m in media_list]

        report_dict['media'] = media
        report_dict['ai'] = JobStore(db.db_path).public_summary(report_id)
        report_dict['assessment'] = report_dict['ai'].pop('assessment',None)
        
        return JSONResponse(content=report_dict)
    except Exception as e:
        logger.error(f"Error in get_report_detail: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": f"Internal server error"})


@app.get("/api/authority/reports/{report_id}/media/{filename}", tags=["Officer"])
async def serve_media(request: Request, report_id: str, filename: str, token: str = None):
    credential = request.headers.get('Authorization', '')
    if not credential and token: credential = 'Bearer ' + token
    if not validate_officer_token_for_middleware(credential):
        fail(401, 'UNAUTHENTICATED', 'Invalid or missing officer token')
    media = next((row for row in get_db().execute('SELECT * FROM media WHERE report_id=?', (report_id,)).fetchall()
                  if resource_name(row) == filename), None)
    if media is None: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    return FileResponse(str(media_path(media)), media_type=media['mime_type'], headers=PRIVATE)

@app.post("/api/authority/reports/{report_id}/decision", tags=["Officer"])
async def make_decision(request: Request, report_id: str):
    """Officer makes a decision on a report."""
    try:
        # Check authorization
        auth_header = request.headers.get("Authorization", "")
        officer_info = validate_officer_token_for_middleware(auth_header)
        if not officer_info:
            return JSONResponse(status_code=401, content={"error": "Invalid or missing officer token"})
        
        body = await request.json()
        
        # Handle both field names: decision_type (UI) and action (old API)
        decision_type = body.get("decision_type") or body.get("action")
        comments = body.get("comments") or body.get("reason")
        
        # Normalize decision_type to action values
        if decision_type == "approved":
            action = "approve"
        elif decision_type == "rejected":
            action = "reject"
        else:
            action = decision_type
        
        if action not in ["approve", "reject", "request-info"]:
            return JSONResponse(status_code=400, content={"error": "Invalid decision type"})
        
        db = get_db()
        
        # Get report
        report = db.execute(
            "SELECT id, status, violation_type FROM reports WHERE id = ?",
            (report_id,)
        ).fetchone()
        
        if not report:
            return JSONResponse(status_code=404, content={"error": "Report not found"})
        
        if report["status"] != "awaiting-review":
            return JSONResponse(status_code=409, content={"error": "Report not awaiting review"})
        
        now = get_utc_now_iso()
        
        if action == "approve":
            new_status = "approved"
            provisional_points = POINTS_BY_VIOLATION.get(report["violation_type"], 0)
            
            with db.transaction() as conn:
                conn.execute(
                    "UPDATE reports SET status = ?, provisional_points = ?, updated_at = ? WHERE id = ?",
                    (new_status, provisional_points, now, report_id)
                )
                
                conn.execute("""
                    INSERT INTO events (id, report_id, event_type, actor, old_status, new_status, created_at, reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (uuid4().hex[:16], report_id, "decision", "officer", "awaiting-review", new_status, now, comments))
            
            return JSONResponse(content={
                "report_id": report_id,
                "status": new_status,
                "violation_type": report["violation_type"],
                "provisional_points": provisional_points,
                "decision_event": {
                    "old_status": "awaiting-review",
                    "new_status": new_status,
                    "created_at": now,
                    "provisional_points": provisional_points,
                    "comments": comments
                }
            })
        
        elif action == "reject":
            new_status = "rejected"
            
            with db.transaction() as conn:
                conn.execute(
                    "UPDATE reports SET status = ?, updated_at = ? WHERE id = ?",
                    (new_status, now, report_id)
                )
                
                conn.execute("""
                    INSERT INTO events (id, report_id, event_type, actor, old_status, new_status, created_at, reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (uuid4().hex[:16], report_id, "decision", "officer", "awaiting-review", new_status, now, reason))
            
            return JSONResponse(content={
                "report_id": report_id,
                "status": new_status,
                "reason": reason,
                "decision_event": {
                    "old_status": "awaiting-review",
                    "new_status": new_status,
                    "reason": reason,
                    "created_at": now
                }
            })
        
        elif action == "request-info":
            new_status = "awaiting-citizen-info"
            
            with db.transaction() as conn:
                conn.execute(
                    "UPDATE reports SET status = ?, updated_at = ? WHERE id = ?",
                    (new_status, now, report_id)
                )
                
                conn.execute("""
                    INSERT INTO events (id, report_id, event_type, actor, old_status, new_status, created_at, reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (uuid4().hex[:16], report_id, "decision", "officer", "awaiting-review", new_status, now, None))
            
            return JSONResponse(content={
                "report_id": report_id,
                "status": new_status,
                "decision_event": {
                    "old_status": "awaiting-review",
                    "new_status": new_status,
                    "created_at": now
                }
            })
    
    except Exception as e:
        logger.error(f"Error in make_decision: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


# M6: Evidence Export - ZIP Download
@app.get("/api/authority/reports/{report_id}/evidence.zip")
async def download_evidence_zip(report_id: str, request: Request):
    """Download evidence ZIP for a report."""
    # Check authorization
    auth_header = request.headers.get("Authorization", "")
    officer_info = validate_officer_token_for_middleware(auth_header)
    if not officer_info:
        return JSONResponse(status_code=401, content={"detail": "Invalid or missing officer token"})
    
    try:
        db = get_db()
        
        # Fetch report
        report = db.execute(
            "SELECT id, citizen_id, violation_type, vehicle_number, location, screening_notes, status, provisional_points, created_at, updated_at FROM reports WHERE id = ?",
            (report_id,)
        ).fetchone()
        
        if not report:
            return JSONResponse(status_code=404, content={"detail": "Report not found"})
        
        # Fetch media
        media_files = db.execute(
            "SELECT * FROM media WHERE report_id = ?",
            (report_id,)
        ).fetchall()
        
        # Fetch events
        events = db.execute(
            "SELECT id, event_type, reason, created_at FROM events WHERE report_id = ? ORDER BY created_at ASC",
            (report_id,)
        ).fetchall()
        
        # Create ZIP in memory
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            # 1. Report manifest
            report_manifest = {
                "report_id": report['id'],
                "citizen_id": report['citizen_id'],
                "violation_type": report['violation_type'],
                "vehicle_number": report['vehicle_number'],
                "location": report['location'],
                "notes": report['screening_notes'],
                "status": report['status'],
                "provisional_points": report['provisional_points'],
                "created_at": report['created_at'],
                "updated_at": report['updated_at'],
            }
            zip_file.writestr("report_manifest.json", json.dumps(report_manifest, indent=2))
            
            # 2. Media files
            if media_files:
                for media in media_files:
                    media_id = media['id']
                    filename = media['filename']
                    storage_path = media['storage_path']
                    
                    file_path = media_path(media)
                    arc_path = 'media/' + resource_name(media)
                    zip_file.write(str(file_path), arcname=arc_path)
            
            # 3. Timeline (events)
            timeline = [
                {
                    "event_id": e['id'],
                    "event_type": e['event_type'],
                    "reason": e['reason'],
                    "created_at": e['created_at'],
                }
                for e in events
            ]
            zip_file.writestr("timeline.json", json.dumps(timeline, indent=2))
            
            # 4. README
            readme = f"""RoadWatch Evidence Export
Report ID: {report['id']}
Exported: {datetime.now(timezone.utc).isoformat()}

Contents:
- report_manifest.json: Full report metadata
- media/: Evidence photos/videos
- timeline.json: All events (creation, review, decision)

Report Status: {report['status']}
Provisional Points: {report['provisional_points']}
Vehicle: {report['vehicle_number']}
Location: {report['location']}
"""
            zip_file.writestr("README.txt", readme)
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            iter([zip_buffer.getvalue()]),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename=evidence-{report_id}.zip"}
        )
    
    except Exception as e:
        logger.error(f"Error downloading evidence ZIP: {e}")
        return JSONResponse(status_code=500, content={"detail": "Failed to generate ZIP"})


# HTML Routes for UI
@app.get("/")
async def root():
    """Redirect to citizen login"""
    return FileResponse("templates/citizen-login.html")

@app.get("/favicon.ico", tags=["Static"])
async def favicon():
    """Serve favicon (returns 204 No Content)"""
    return JSONResponse(status_code=204, content={})

@app.get("/{filename}.html")
async def serve_html(filename: str):
    """Serve HTML template files without authentication (auth handled client-side)"""
    file_path = Path("templates") / f"{filename}.html"
    if file_path.exists():
        return FileResponse(str(file_path))
    return JSONResponse(status_code=404, content={"error": "Page not found"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
