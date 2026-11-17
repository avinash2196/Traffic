"""CITIZEN API for RoadWatch Traffic MVP (port 8001).

Provides citizen-facing endpoints:
- POST /api/media/upload - Upload evidence media
- POST /api/reports - Submit report
- GET /api/reports - Fetch citizen's reports
- GET /api/reports/{report_id} - Fetch report details
- GET /api/media/{media_id}/{filename} - Download media
- POST /api/reports/{report_id}/clarification - Submit clarification
"""

import os
from pathlib import Path
from contextlib import asynccontextmanager
import logging
from datetime import datetime, timezone
from uuid import uuid4
import json
import hashlib
import time
import sqlite3

from fastapi import FastAPI, Request, UploadFile, File
from starlette.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import io

# Add parent directory to Python path so we can import shared modules
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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

# Import utilities
from shared.bootstrap import init_database, get_db
from shared.auth_utils import validate_session_token
from shared.intake import (IntakeError, fail, parse_upload, validate_media, FORMATS, PRIVATE,
                    resource_name, media_path, media_view)
from shared.shared_utils import get_utc_now_iso, POINTS_BY_VIOLATION, VALID_VIOLATIONS
from shared.durable import JobStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown for citizen API."""
    logger.info("🚀 CITIZEN API STARTUP: Initializing citizen-api (port 9002)...")
    try:
        db_path = os.getenv("DATABASE_URL", "../roadwatch.db")
        db = init_database(db_path)
        logger.info(f"✓ Database initialized: {db_path}")
        app.state.db = db
        # Initialize AI settings (empty for MVP)
        app.state.ai_settings = {
            "ai_enabled": False,
            "model": "gpt-4o-mini",
            "screening_enabled": False
        }
        logger.info("✓ Citizen API initialized")
    except Exception as e:
        logger.error(f"✗ Startup failed: {e}", exc_info=True)
        raise
    
    yield  # App runs here
    
    # Shutdown
    logger.info("🛑 CITIZEN API SHUTDOWN: Closing citizen-api...")
    try:
        db = get_db()
        db.close()
        logger.info("✓ Database connection closed")
    except Exception as e:
        logger.warning(f"Shutdown error: {e}")


# Create FastAPI app
app = FastAPI(
    title="RoadWatch Citizen API",
    description="Citizen-facing API for traffic evidence reporting",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url=None,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for citizen authentication
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Authenticate citizen from Bearer token or X-Citizen-Id header."""
    # Allow public endpoints and CORS preflight
    public_paths = ["/health", "/api/docs", "/openapi.json"]
    if (request.url.path in public_paths or 
        request.url.path.startswith("/static/") or
        request.method == "OPTIONS"):
        return await call_next(request)
    
    # MVP DEMO MODE: Allow GET requests without auth (read-only access)
    if request.method == "GET":
        # For demo, generate a temporary citizen ID if none provided
        citizen_id = request.headers.get("X-Citizen-Id")
        if not citizen_id:
            citizen_id = "demo-" + request.client.host.replace(".", "-")
        request.scope["citizen_id"] = citizen_id
        return await call_next(request)
    
    # For POST/PUT/DELETE, require authentication
    # Try Bearer token
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        citizen_id = validate_session_token(token)
        if citizen_id:
            request.scope["citizen_id"] = citizen_id
            return await call_next(request)
    
    # Try X-Citizen-Id header (demo mode)
    citizen_id = request.headers.get("X-Citizen-Id")
    if citizen_id:
        request.scope["citizen_id"] = citizen_id
        return await call_next(request)
    
    # No auth found
    return JSONResponse(
        status_code=401,
        content={"error": "X-Citizen-Id header or Bearer token required"}
    )


@app.exception_handler(IntakeError)
async def intake_error_handler(request: Request, exc: IntakeError):
    return JSONResponse(
        status_code=exc.status,
        content={'error': exc.message, 'detail': exc.message, 'code': exc.code}
    )


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "citizen-api"
    }


# ============ MEDIA UPLOAD ============

def upload_result(row, duplicate: bool):
    """Format media upload response."""
    result = {
        'media_id': row['id'],
        'filename': row['filename'],
        'resource_name': resource_name(row),
        'file_size': row['file_size_bytes'],
        'sha256_hash': row['sha256_hash'],
        'uploaded_at': row['uploaded_at'],
        'is_duplicate': duplicate
    }
    if duplicate:
        result['duplicate_reason'] = 'Previously uploaded by you'
    return result


@app.post("/api/media/upload", tags=["Media"], status_code=201)
async def upload_media(request: Request):
    """Validate and store uploaded media (image/video)."""
    try:
        filename, mime, data = await run_in_threadpool(
            parse_upload,
            request.headers.get('content-type', ''),
            await request.body()
        )
        await run_in_threadpool(validate_media, data, mime)
        
        owner = request.scope['citizen_id']
        digest = hashlib.sha256(data).hexdigest()
        db = get_db()
        
        # Check for duplicates
        existing = db.execute(
            "SELECT * FROM media WHERE owner_citizen_id=? AND sha256_hash=? AND report_id IS NULL ORDER BY uploaded_at,id LIMIT 1",
            (owner, digest)
        ).fetchone()
        
        if existing:
            return JSONResponse(status_code=200, content=upload_result(existing, True))
        
        # Create new media record
        media_id = uuid4().hex[:16]
        name = media_id + FORMATS[mime]
        filename = filename or name
        path = Path('media_store').resolve() / name
        now = get_utc_now_iso()
        
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as output:
                output.write(data)
            
            with db.transaction() as conn:
                conn.execute(
                    'INSERT INTO media(id,filename,file_size_bytes,mime_type,sha256_hash,storage_path,uploaded_at,owner_citizen_id,resource_name) VALUES(?,?,?,?,?,?,?,?,?)',
                    (media_id, filename, len(data), mime, digest, str(path), now, owner, name)
                )
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


# ============ REPORT SUBMISSION ============

@app.post("/api/reports", tags=["Reports"], status_code=201)
async def submit_report(request: Request):
    """Submit a new traffic violation report with evidence media."""
    if request.headers.get('content-type', '').split(';')[0].strip().lower() != 'application/json':
        fail(415, 'UNSUPPORTED_CONTENT_TYPE', 'Expected JSON')
    
    try:
        body = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        fail(400, 'INVALID_INPUT', 'Invalid JSON')
    
    if not isinstance(body, dict):
        fail(400, 'INVALID_INPUT', 'Expected JSON object')
    
    logger.info(f"Report request body: {body}")
    
    # Validate required fields
    for key in ('violation_type', 'vehicle_number', 'location'):
        if not isinstance(body.get(key), str) or not body[key].strip():
            logger.error(f"Validation failed for {key}: value={body.get(key)}, type={type(body.get(key))}")
            fail(400, 'INVALID_INPUT', 'Required nonblank string')
    
    if body['violation_type'] not in VALID_VIOLATIONS:
        fail(400, 'INVALID_INPUT', 'Unknown violation category')
    
    # Accept either media_id (single) or media_ids (multiple)
    if ('media_id' in body) == ('media_ids' in body):
        fail(400, 'INVALID_INPUT', 'Supply exactly one media alias')
    
    ids = body.get('media_ids') if 'media_ids' in body else [body['media_id']]
    
    if not isinstance(ids, list) or not ids or any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
        fail(400, 'INVALID_INPUT', 'Expected distinct media handles')
    
    citizen = request.scope['citizen_id']
    key = request.headers.get('Idempotency-Key')
    
    if key is not None and (not 1 <= len(key) <= 128 or any(ord(c) < 32 or ord(c) > 126 for c in key) or not key.strip()):
        fail(400, 'INVALID_INPUT', 'Invalid idempotency key')
    
    # Create report
    fingerprint = json.dumps(
        [body['violation_type'], body['vehicle_number'], body['location'], ids],
        separators=(',', ':'),
        ensure_ascii=True
    )
    
    report_id = uuid4().hex[:16]
    now = get_utc_now_iso()
    job_id = uuid4().hex[:16]
    
    response = {
        'report_id': report_id,
        'status': 'awaiting-review',
        'violation_type': body['violation_type'],
        'created_at': now,
        'citizen_id': citizen,
        'ai': {
            'job_id': job_id,
            'state': 'pending',
            'outcome': None,
            'recommendation': None,
            'attempt_count': 0,
            'max_attempts': 3,
            'failure_code': None,
            'failure_reason': None,
            'next_attempt_at': None,
            'started_at': None,
            'completed_at': None,
            'processing_ms': None,
            'assessment_id': None,
            'evidence_revision': 1,
            'late_result': False
        }
    }
    
    db = get_db()
    
    try:
        with db.transaction() as conn:
            conn.execute('BEGIN IMMEDIATE')
            
            # Check idempotency
            if key is not None:
                replay = conn.execute(
                    'SELECT fingerprint,response FROM ai_jobs WHERE principal=? AND idempotency_key=?',
                    (citizen, key)
                ).fetchone()
                if replay is not None:
                    if replay['fingerprint'] != fingerprint:
                        fail(409, 'IDEMPOTENCY_CONFLICT', 'Idempotency key was already used')
                    return JSONResponse(status_code=201, content=json.loads(replay['response']))
            
            # Verify media ownership and availability
            for media_id in ids:
                media = conn.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
                if not media:
                    fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
                
                owner = media['owner_citizen_id']
                if owner is None and media['report_id']:
                    report = conn.execute('SELECT citizen_id FROM reports WHERE id=?', (media['report_id'],)).fetchone()
                    owner = report['citizen_id'] if report else None
                
                if owner is None:
                    fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
                if owner != citizen:
                    fail(403, 'FORBIDDEN', 'Media belongs to another citizen')
                if media['report_id']:
                    fail(409, 'MEDIA_ALREADY_ATTACHED', 'Media already attached')
            
            # Insert report
            conn.execute(
                'INSERT INTO reports(id,citizen_id,violation_type,vehicle_number,location,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)',
                (report_id, citizen, body['violation_type'], body['vehicle_number'], body['location'], 'awaiting-review', now, now)
            )
            
            # Attach media
            for position, media_id in enumerate(ids):
                conn.execute(
                    'UPDATE media SET report_id=?,attachment_position=? WHERE id=?',
                    (report_id, position, media_id)
                )
            
            # Create event
            conn.execute(
                'INSERT INTO events(id,report_id,event_type,actor,old_status,new_status,created_at,reason) VALUES(?,?,?,?,?,?,?,?)',
                (uuid4().hex[:16], report_id, 'status_change', 'citizen', None, 'awaiting-review', now, None)
            )
            
            # Create AI job
            conn.execute(
                "INSERT INTO ai_jobs(id,report_id,evidence_revision,state,created_at,principal,idempotency_key,fingerprint,response,settings_snapshot) VALUES(?,?,1,'pending',?,?,?,?,?,?)",
                (job_id, report_id, time.time(), citizen, key, fingerprint, json.dumps(response), json.dumps(app.state.ai_settings))
            )
    
    except IntakeError:
        raise
    except sqlite3.Error:
        fail(503, 'STORAGE_UNAVAILABLE', 'Report storage unavailable')
    except Exception:
        fail(500, 'INTERNAL_ERROR', 'Unable to submit report')
    
    return JSONResponse(status_code=201, content=response)


# ============ REPORT RETRIEVAL ============

@app.get("/api/reports", tags=["Reports"])
async def fetch_reports(request: Request, page: int = 1, page_size: int = 20):
    """Fetch citizen's own reports with pagination."""
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


@app.get("/api/reports/{report_id}", tags=["Reports"])
async def fetch_report_detail(request: Request, report_id: str):
    """Fetch report details with timeline and media."""
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
        
        # Get media
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
        result["assessment"] = result["ai"].pop("assessment", None)
        
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error in fetch_report_detail: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


# ============ MEDIA DOWNLOAD ============

@app.get("/api/media/{media_id}/{filename}", tags=["Media"])
async def serve_citizen_media(request: Request, media_id: str, filename: str):
    """Download media (citizen can only download own media)."""
    db = get_db()
    media = db.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
    
    if not media or resource_name(media) != filename:
        fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    
    owner = media['owner_citizen_id']
    if owner is None and media['report_id']:
        report = db.execute('SELECT citizen_id FROM reports WHERE id=?', (media['report_id'],)).fetchone()
        owner = report['citizen_id'] if report else None
    
    if owner is None:
        fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    
    if owner != request.scope['citizen_id']:
        fail(403, 'FORBIDDEN', 'Media belongs to another citizen')
    
    return FileResponse(str(media_path(media)), media_type=media['mime_type'], headers=PRIVATE)


# ============ CLARIFICATION ============

@app.post("/api/reports/{report_id}/clarification", tags=["Reports"])
async def submit_clarification(request: Request, report_id: str):
    """Submit clarification response to officer request."""
    try:
        citizen_id = request.scope.get("citizen_id")
        if not citizen_id:
            return JSONResponse(status_code=401, content={"error": "Missing citizen_id"})
        
        body = await request.json()
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("CITIZEN_API_PORT", "9001"))
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=port,
        reload=False,
        log_level="info"
    )
