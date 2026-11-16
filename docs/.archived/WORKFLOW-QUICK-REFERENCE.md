# RoadWatch MVP — Quick Reference Card
**Print this or bookmark it!**

---

## 🎯 THE COMPLETE FLOW (In 60 Seconds)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CITIZEN → SYSTEM → AI → OFFICER                  │
└─────────────────────────────────────────────────────────────────────┘

CITIZEN:
  1. Signup/Login (JWT token issued)
  2. Upload media (image/video validated, SHA-256 hashed)
  3. Submit report (traffic violation details)
       ↓
SYSTEM:
  4. Create report + Enqueue AI screening job
       ↓
AI (ASYNC - happens in background):
  5. Pull job → Assess evidence → Store result
       ↓
CITIZEN (meanwhile):
  6. Check status every 30s → Sees report moving through pipeline
       ↓
OFFICER:
  7. Login → View queue → Click report → Review evidence + AI result
  8. Make decision (Approve/Reject/Request More Info)
       ↓
CITIZEN:
  9. Status changes → Sees decision + provisional points
```

---

## 🔑 KEY ENDPOINTS AT A GLANCE

### Citizen Endpoints (JWT Authorization)
```
POST   /api/auth/signup              Create citizen account
POST   /api/auth/login               Get JWT session token

POST   /api/media/upload             Upload image/video (returns media_id)
POST   /api/reports                  Submit traffic report (uses media_id)
GET    /api/reports                  List own reports
GET    /api/reports/{report_id}      Get single report detail

POST   /api/reports/{id}/clarification   Respond to officer's "request-info"
```

### Officer Endpoints (Bearer Token Authorization)
```
GET    /api/authority/reports        List queue (awaiting-review)
GET    /api/authority/reports/{id}   Get full case details
POST   /api/authority/reports/{id}/decision   Make approval/rejection decision
```

### Media Access (Both)
```
GET    /api/media/{media_id}/{filename}  Download image/video
```

### Health Check
```
GET    /health                       Server status
```

---

## 🗂️ DATABASE ENTITIES

### reports (Mutable - Status Changes)
```
report_id          | UUID (PK)
citizen_id         | String (FK)
status             | "submitted" → "awaiting-review" → "approved|rejected|awaiting-citizen-info"
violation_type     | "helmet" | "triple-riding" | "red-light"
vehicle_number     | String (e.g., "DL01AB1234")
location           | String (e.g., "Delhi, Connaught Place")
media_id           | UUID (FK)
provisional_points | Integer (0 until approved, then 2/3 based on violation_type)
created_at         | ISO-8601 timestamp
updated_at         | ISO-8601 timestamp
```

### media (Immutable - Write Once)
```
media_id       | UUID (PK)
file_hash      | SHA-256 (for deduplication)
file_type      | "jpeg" | "png" | "mp4" | "mov"
file_size      | Integer (bytes)
citizen_id     | String (FK - who uploaded)
storage_path   | String (on-disk location)
upload_time    | ISO-8601 timestamp
```

### events (Immutable - Append Only - Never Updated)
```
event_id      | UUID (PK)
report_id     | UUID (FK)
event_type    | "report_submitted" | "ai_screening_started" | "ai_screening_completed" 
              | "officer_decision" | "clarification_submitted"
actor_type    | "citizen" | "system" | "officer"
actor_id      | String (citizen_id or officer_id)
data          | JSON (event-specific details)
timestamp     | ISO-8601 timestamp (immutable)
```

### ai_jobs (Async Processing Tracking)
```
job_id        | UUID (PK)
report_id     | UUID (FK)
status        | "pending" → "processing" → "completed"
outcome       | JSON (assessment result)
attempt_count | Integer (for retry tracking)
created_at    | ISO-8601 timestamp
completed_at  | ISO-8601 timestamp (NULL while pending/processing)
```

---

## 📊 STATUS FLOW DIAGRAM

```
              CITIZEN              │         SYSTEM/AI         │       OFFICER
                                   │                           │
Signup/Login ────→ JWT Token       │                           │
                                   │                           │
Upload Media ─────→ media_id       │                           │
                                   │                           │
Submit Report ─────→ report_id + status="submitted"           │
                                   │                           │
                                   ├─→ AI Job Queued          │
                                   │   (async)                │
                                   │                           │
Poll Status: "submitted" ──────────┼─→ AI: processing...      │
                                   │                           │
Poll Status: "submitted" ──────────┼─→ AI: completed          │
             status→"awaiting-review"                         │
                                   │                           │
                                   │                  ← Officer Sees in Queue
                                   │                           │
Poll Status: "awaiting-review"     │                  Officer Reviews Details
                                   │                  + Views Media
                                   │                  + Sees AI Result
                                   │                           │
                                   │              Officer Decides:
                                   │              Approve/Reject/Request-Info
                                   │                           │
                                   │              status → "approved" +
Poll Status: "approved" ←──────────┼────────────   provisional_points=2
Sees Decision ✅                    │

OR

Poll Status: "awaiting-citizen-info" ← Officer Request-Info
Citizen Resubmit + Clarification     ← Back to "awaiting-review"
```

---

## 🔐 AUTHENTICATION

### JWT (Citizen)
```
Header: Authorization: Bearer {session_token}

Payload (decoded):
{
  "citizen_id": "DL123ABC",
  "type": "citizen",
  "exp": 1700000000,              // 24 hours from login
  "iat": 1699913600
}

Validated on:
  - Media upload
  - Report submission
  - Report queries
  - Clarification submission
```

### Bearer Token (Officer)
```
Header: Authorization: Bearer {token}

Token = Environment Variable: ROADWATCH_REVIEWER_TOKEN
Default: "local-reviewer-only" (for local testing)

NO JWT decoding - just string comparison
Shared across all officers in MVP (no per-officer tracking)

Validated on:
  - Authority queue access
  - Report detail access (any report)
  - Decision making
```

---

## 🎯 VIOLATION POINTS TABLE

```
Violation Type    │ Provisional Points
─────────────────┼──────────────────
helmet            │ 2
triple-riding     │ 3
red-light         │ 3
```

Awarded by officer when clicking "Approve" (Step 6E).

---

## 🚀 STARTING THE APP

### Local (Development)
```bash
# Terminal 1: Start FastAPI Server
export ROADWATCH_REVIEWER_TOKEN='local-reviewer-only'
python -m venv .venv
source .venv/bin/activate         # Mac/Linux
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
uvicorn app:app --reload

# Terminal 2 (Optional): Start AI Gateway Service
python ai_gateway_service.py
```

### Browser
```
Citizen Portal:  http://127.0.0.1:8000/
Officer Portal:  http://127.0.0.1:8000/officer-dashboard.html
API Docs:        http://127.0.0.1:8000/api/docs
Health Check:    http://127.0.0.1:8000/health
```

### Docker
```bash
docker build -t roadwatch:1.0 .
docker run -p 8000:8000 \
  -e ROADWATCH_REVIEWER_TOKEN='local-reviewer-only' \
  roadwatch:1.0
```

---

## 🧪 TESTING MANUALLY

### Test Full Flow (Script)
```bash
python manual_test.py
# Runs complete 8-step workflow
# - Citizen signup/login
# - Media upload
# - Report submit
# - Officer queue review
# - Officer decision
# - Citizen status tracking
```

### Test Specific Endpoint
```bash
# Citizen signup
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "citizen_id": "DL123ABC",
    "email": "test@example.com",
    "password": "Test1234!",
    "full_name": "Test User"
  }'

# Officer queue
curl -X GET http://127.0.0.1:8000/api/authority/reports \
  -H "Authorization: Bearer local-reviewer-only"
```

---

## ⚠️ COMMON SCENARIOS

### Scenario 1: Media Upload Fails (400)
```
Reason: File too large, wrong format, or corrupted
Response: {"error": "File validation failed", "reason": "..."}
Action: Check file size (<25MB images, <45s video), format (JPEG/PNG/MP4/MOV)
```

### Scenario 2: Duplicate Media (409)
```
Reason: Same file already uploaded
Response: {"media_id": "existing-id", "status": "duplicate"}
Action: This is OK - system deduplicates. Use returned media_id.
```

### Scenario 3: AI Screening Fails (But Officer Can Still Decide)
```
Reason: No API keys configured, network issue, or demo mode
Response: ai_state="failed", outcome={"status": "failed"}
Action: Officer can still manually review and approve/reject
```

### Scenario 4: Officer Token Invalid (401)
```
Reason: Token doesn't match ROADWATCH_REVIEWER_TOKEN
Response: {"error": "Unauthorized"}
Action: Check environment variable is set correctly
```

### Scenario 5: Citizen Sees "Awaiting Officer Review" Forever
```
Reason: Officer hasn't reviewed the report yet
Action: Officer needs to login and click "Approve/Reject"
Note: Status polling shows "awaiting-review" until officer decides
```

---

## 📈 DATA FLOW TRACKING

### From Report Submit to Final Decision
```
1. Citizen submits report
   → reports table gets: status="submitted"
   → events table logs: "report_submitted"
   → ai_jobs table gets: status="pending"

2. AI Worker picks up job
   → ai_jobs: status="processing"
   → events logs: "ai_screening_started"

3. AI Completes
   → ai_jobs: status="completed", outcome={...}
   → reports: status="awaiting-review"
   → events logs: "ai_screening_completed"

4. Officer Reviews & Approves
   → reports: status="approved", provisional_points=2
   → events logs: "officer_decision"

5. Citizen Polls & Sees Result
   → GET /api/reports/{id} returns status="approved"
   → Citizen sees decision + provisional points
```

---

## 🔍 DEBUGGING TIPS

### Check App Logs
```bash
# Terminal running uvicorn shows real-time logs
# Look for:
# - "POST /api/reports" - report submission
# - "ai_worker" - AI processing logs
# - "officer_decision" - officer actions
```

### Check Database
```bash
sqlite3 roadwatch.db
> SELECT report_id, status, created_at FROM reports;
> SELECT event_type, timestamp FROM events ORDER BY timestamp DESC LIMIT 10;
> SELECT job_id, status, outcome FROM ai_jobs;
```

### Check Media Files
```bash
ls -la media_store/
# Each media_id folder contains the original file
```

### Test API with Swagger
```
http://127.0.0.1:8000/api/docs
# Interactive API testing - no curl needed
```

---

## 📞 SUPPORT QUICK LINKS

- **Workflow Details:** See WORKFLOW-PRECISE-SUMMARY.md
- **Architecture:** See docs/ARCHITECTURE-FLOW-DIAGRAMS.md
- **API Reference:** See docs/API-REQUEST-RESPONSE-REFERENCE.md
- **Quick Start:** See docs/QUICK_START.md
- **Full Plan:** See docs/Plan.md

---

**Last Updated:** 2026-11-13  
**Status:** ✅ Production Ready
