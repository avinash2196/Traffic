"""OFFICER API for RoadWatch Traffic MVP (port 8002).

Provides officer/authority-facing endpoints:
- GET /api/authority/reports - Fetch review queue
- GET /api/authority/reports/{report_id} - Fetch report details
- GET /api/authority/reports/{report_id}/media/{filename} - Download media
- POST /api/authority/reports/{report_id}/decision - Make approval/rejection decision
- GET /api/authority/reports/{report_id}/evidence.zip - Download evidence ZIP
"""

import os
from pathlib import Path
from contextlib import asynccontextmanager
import logging
from datetime import datetime, timezone
from uuid import uuid4
import json
import io
from zipfile import ZipFile

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

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
from shared.auth_utils import validate_officer_token
from shared.intake import resource_name, media_path, PRIVATE, fail
from shared.shared_utils import get_utc_now_iso, validate_officer_token_for_middleware, POINTS_BY_VIOLATION
from shared.durable import JobStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown for officer API."""
    logger.info("🚀 OFFICER API STARTUP: Initializing officer-api (port 8002)...")
    try:
        db = init_database("./roadwatch.db")
        logger.info(f"✓ Database initialized: ./roadwatch.db")
        app.state.db = db
    except Exception as e:
        logger.error(f"✗ Startup failed: {e}", exc_info=True)
        raise
    
    yield  # App runs here
    
    # Shutdown
    logger.info("🛑 OFFICER API SHUTDOWN: Closing officer-api...")
    try:
        db = get_db()
        db.close()
        logger.info("✓ Database connection closed")
    except Exception as e:
        logger.warning(f"Shutdown error: {e}")


# Create FastAPI app
app = FastAPI(
    title="RoadWatch Officer API",
    description="Officer-facing API for reviewing and approving reports",
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


# Middleware for officer authentication
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Authenticate officer from Bearer token."""
    # Allow public endpoints and CORS preflight
    public_paths = ["/health", "/api/docs", "/openapi.json"]
    if (request.url.path in public_paths or 
        request.url.path.startswith("/static/") or
        request.method == "OPTIONS"):
        return await call_next(request)
    
    # Check Authorization header
    auth_header = request.headers.get("Authorization", "")
    officer_info = validate_officer_token_for_middleware(auth_header)
    
    if not officer_info:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid or missing officer token"}
        )
    
    request.scope["officer_id"] = officer_info.get("officer_id", "unknown")
    return await call_next(request)


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "officer-api"
    }


# ============ QUEUE & REVIEW ============

@app.get("/api/authority/reports", tags=["Officer"])
async def fetch_queue(request: Request, page: int = 1, page_size: int = 10, status: str = None):
    """Fetch review queue with pagination."""
    try:
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
    """Fetch report details for officer review."""
    try:
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
        
        # Get media URLs
        media_list = db.execute("""
            SELECT *
            FROM media
            WHERE report_id = ?
            ORDER BY COALESCE(attachment_position, 2147483647), uploaded_at, id
        """, (report_id,)).fetchall()
        
        # Extract token from Authorization header for media URLs
        auth_header = request.headers.get("Authorization", "")
        token_for_media = auth_header.replace("Bearer ", "").strip()
        if not token_for_media:
            token_for_media = os.getenv("ROADWATCH_REVIEWER_TOKEN", "")
        
        media = [_media_view_with_token(m, report_id, token_for_media) for m in media_list]
        
        report_dict['media'] = media
        report_dict['ai'] = JobStore(db.db_path).public_summary(report_id)
        report_dict['assessment'] = report_dict['ai'].pop('assessment', None)
        
        return JSONResponse(content=report_dict)
    except Exception as e:
        logger.error(f"Error in get_report_detail: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": f"Internal server error"})


def _media_view_with_token(row, report_id, token):
    """Format media view URL with token."""
    from intake import resource_name
    name = resource_name(row)
    return {
        'media_id': row['id'],
        'filename': name,
        'url': f'/api/authority/reports/{report_id}/media/{name}?token={token}' if token else f'/api/authority/reports/{report_id}/media/{name}',
        'mime_type': row['mime_type'],
        'file_size': row['file_size_bytes'],
        'uploaded_at': row['uploaded_at']
    }


# ============ MEDIA DOWNLOAD ============

@app.get("/api/authority/reports/{report_id}/media/{filename}", tags=["Officer"])
async def serve_media(request: Request, report_id: str, filename: str, token: str = None):
    """Download media from a report."""
    credential = request.headers.get('Authorization', '')
    if not credential and token:
        credential = 'Bearer ' + token
    
    if not validate_officer_token_for_middleware(credential):
        fail(401, 'UNAUTHENTICATED', 'Invalid or missing officer token')
    
    db = get_db()
    media = next(
        (row for row in db.execute('SELECT * FROM media WHERE report_id=?', (report_id,)).fetchall()
         if resource_name(row) == filename),
        None
    )
    
    if media is None:
        fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
    
    return FileResponse(str(media_path(media)), media_type=media['mime_type'], headers=PRIVATE)


# ============ DECISION MAKING ============

@app.post("/api/authority/reports/{report_id}/decision", tags=["Officer"])
async def make_decision(request: Request, report_id: str):
    """Officer makes approval/rejection decision on a report."""
    try:
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
        
        if report["status"] != "awaiting-review" and report["status"] != "resubmitted":
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
                """, (uuid4().hex[:16], report_id, "decision", "officer", report["status"], new_status, now, comments))
            
            return JSONResponse(content={
                "report_id": report_id,
                "status": new_status,
                "violation_type": report["violation_type"],
                "provisional_points": provisional_points,
                "decision_event": {
                    "old_status": report["status"],
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
                """, (uuid4().hex[:16], report_id, "decision", "officer", report["status"], new_status, now, comments))
            
            return JSONResponse(content={
                "report_id": report_id,
                "status": new_status,
                "reason": comments,
                "decision_event": {
                    "old_status": report["status"],
                    "new_status": new_status,
                    "reason": comments,
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
                """, (uuid4().hex[:16], report_id, "decision", "officer", report["status"], new_status, now, None))
            
            return JSONResponse(content={
                "report_id": report_id,
                "status": new_status,
                "decision_event": {
                    "old_status": report["status"],
                    "new_status": new_status,
                    "created_at": now
                }
            })
    
    except Exception as e:
        logger.error(f"Error in make_decision: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})


# ============ EVIDENCE EXPORT ============

@app.get("/api/authority/reports/{report_id}/evidence.zip", tags=["Officer"])
async def download_evidence_zip(report_id: str, request: Request):
    """Download evidence ZIP for a report."""
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("OFFICER_API_PORT", "9002"))
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=port,
        reload=False,
        log_level="info"
    )
