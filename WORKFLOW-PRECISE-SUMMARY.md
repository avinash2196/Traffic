# RoadWatch MVP — Precise Workflow Summary
**Date:** 2026-11-13  
**Status:** ✅ Fully Operational  

---

## 🎯 EXECUTIVE FLOW (60 seconds)

1. **Citizen uploads image** → System validates & stores
2. **Citizen submits report** → AI screening job queued (async)
3. **System processes AI screening** → Results stored (pass/fail/flags)
4. **Officer sees report in queue** → Status = "awaiting-review"
5. **Officer reviews evidence + AI results** → Makes decision (approve/reject/request-info)
6. **Decision recorded** → Provisional points awarded → Citizen notified

---

## 📋 DETAILED FLOW — WHO DOES WHAT AT EACH STEP

### **PHASE 1: CITIZEN AUTHENTICATION**

#### Step 1A: Citizen Opens Browser
```
User opens: http://127.0.0.1:8000/
│
├─ Frontend checks: Is there a valid JWT token in localStorage?
│
├─ If NO token → Redirect to /citizen-login.html
│                  (Signup or login form)
│
└─ If YES token → Load citizen dashboard (/citizen-dashboard.html)
```

#### Step 1B: Citizen Signs Up (First Time)
```
POST /api/auth/signup
Content-Type: application/json

Request Body:
{
  "citizen_id": "DL123ABC",           ← User enters (license plate)
  "email": "user@example.com",        ← User enters
  "password": "SecurePass123",        ← User enters (bcrypt hashed)
  "full_name": "Test User"            ← User enters
}

Backend Processing:
  1. auth_utils.validate_citizen_id() → Check format (DL123ABC)
  2. auth_utils.is_valid_email() → Check email format
  3. auth_utils.is_valid_password() → Check complexity
  4. database.insert_citizen() → Save with hashed password
  5. Response → 201 Created (user saved)
     OR 409 Conflict (user already exists)

Frontend:
  - Save citizen_id to localStorage
  - Redirect to login page (or dashboard if auto-login)
```

#### Step 1C: Citizen Logs In
```
POST /api/auth/login
Content-Type: application/json

Request Body:
{
  "citizen_id": "DL123ABC",
  "password": "SecurePass123"
}

Backend Processing:
  1. database.get_citizen(citizen_id) → Fetch from DB
  2. auth_utils.verify_password() → Compare hashed password
  3. If valid:
     - auth_utils.generate_session_token() → Create JWT
       {
         "citizen_id": "DL123ABC",
         "type": "citizen",
         "exp": (24 hours from now)
       }
     - Response → 200 OK + session_token
     - Log: event_type = "citizen_login"
  4. If invalid:
     - Response → 401 Unauthorized

Frontend:
  - Extract session_token from response
  - Save to localStorage: { citizen_id, session_token }
  - Redirect to citizen dashboard
```

---

### **PHASE 2: MEDIA UPLOAD & VALIDATION**

#### Step 2A: Citizen Selects Media File
```
Frontend (citizen-dashboard.html):
  1. User clicks "Upload Evidence"
  2. File picker opens
  3. User selects JPG/PNG (image) OR MP4/MOV (video)
  4. Frontend validates:
     - File type → Must be: JPEG, PNG, MP4, MOV
     - File size → Max 25 MB (images), 45 seconds (video duration)
     - If invalid → Show error, ask to retry
  5. If valid → Move to Step 2B
```

#### Step 2B: Upload Media File
```
POST /api/media/upload
Content-Type: multipart/form-data
Authorization: Bearer {session_token}  ← JWT from Step 1C

Request:
  - media_file: <binary file data>

Backend Processing (media.py):
  1. auth_utils.validate_session_token(session_token) → Verify JWT
     - If invalid → Response 401 Unauthorized, stop
  2. intake.parse_upload() → Extract file from multipart
  3. intake.validate_media() → Check:
     - File format (JPEG/PNG/MP4/MOV)
     - File size (≤25 MB for images, ≤45s for video)
     - If validation fails → Response 400 Bad Request + error message
  4. Calculate SHA-256 hash of file content
  5. Check deduplication:
     - Does hash already exist in database?
     - If yes → Response 409 Conflict + existing_media_id (don't store duplicate)
     - If no → Proceed
  6. Store file:
     - Create unique media_id (UUID)
     - Save file to disk: media_store/{media_id}/{media_id}.{ext}
     - Insert record into database:
       {
         media_id: (UUID),
         file_hash: (SHA-256),
         file_type: (jpeg/png/mp4/mov),
         file_size: (bytes),
         upload_timestamp: (ISO-8601),
         citizen_id: (from token),
         storage_path: (disk path)
       }
  7. Response → 201 Created
     {
       "media_id": "abc123def456",
       "file_hash": "sha256...",
       "status": "verified",
       "message": "Media stored successfully"
     }

Frontend:
  - Extract media_id from response
  - Store in memory (for use in Step 3B)
  - Display "Upload successful"
```

---

### **PHASE 3: REPORT SUBMISSION**

#### Step 3A: Citizen Fills Report Form
```
Frontend (citizen-dashboard.html):
  1. User clicks "Submit Report"
  2. Form displays:
     ├─ Violation Type (dropdown):
     │    ├─ "helmet" → 2 points
     │    ├─ "triple-riding" → 3 points
     │    └─ "red-light" → 3 points
     ├─ Vehicle Number (text input)
     │    Example: "DL01AB1234"
     ├─ Location (text input)
     │    Example: "Delhi, Connaught Place"
     └─ Media Preview (from Step 2B)
  3. User clicks "Submit"
  4. Frontend validates all fields filled
  5. Proceed to Step 3B
```

#### Step 3B: Submit Report to Backend
```
POST /api/reports
Content-Type: application/json
Authorization: Bearer {session_token}

Request Body:
{
  "violation_type": "helmet",          ← From dropdown
  "vehicle_number": "DL01AB1234",     ← From text input
  "location": "Delhi, Connaught Place", ← From text input
  "media_id": "abc123def456"           ← From Step 2B upload
}

Backend Processing (app.py):
  1. auth_utils.validate_session_token(session_token) → Verify JWT
     - If invalid → Response 401 Unauthorized
  2. database.get_media(media_id) → Verify media exists
     - If not found → Response 404 Not Found
  3. Validate violation_type:
     - Must be one of: "helmet", "triple-riding", "red-light"
     - If invalid → Response 400 Bad Request
  4. Create report record:
     {
       report_id: (UUID),
       citizen_id: (from JWT token),
       violation_type: (from request),
       vehicle_number: (from request),
       location: (from request),
       media_id: (from request),
       status: "submitted",              ← Initial state
       provisional_points: 0,            ← Will be filled by officer
       created_at: (ISO-8601 timestamp),
       updated_at: (ISO-8601 timestamp)
     }
  5. IMMEDIATELY enqueue AI screening job:
     - job_id = uuid4()
     - ai_job_record:
       {
         job_id: (UUID),
         report_id: (from step 4),
         status: "pending",              ← Initial state
         created_at: (ISO-8601),
         updated_at: (ISO-8601),
         attempt_count: 0
       }
  6. Insert event into immutable events table:
     {
       event_id: (UUID),
       report_id: (from step 4),
       event_type: "report_submitted",
       timestamp: (ISO-8601),
       actor_id: (citizen_id),
       actor_type: "citizen",
       data: {details of submission}
     }
  7. Response → 201 Created
     {
       "report_id": "abc456def789",
       "status": "submitted",
       "ai_job_id": "job123abc",
       "created_at": "2026-11-13T16:16:21Z",
       "message": "Report submitted; AI screening queued"
     }

Frontend:
  - Save report_id
  - Redirect to report status tracker
  - Display "Report submitted! Waiting for system screening..."
```

---

### **PHASE 4: AI SCREENING (ASYNCHRONOUS)**

#### Step 4A: AI Job Picks Up Report
```
System (background worker):
  1. gateway.py:ai_worker_factory() spawns worker thread
  2. Worker polls job queue every 5 seconds
  3. Finds job from Step 3B with status="pending"
  4. Updates job status → "processing"
  5. Insert event:
     {
       event_type: "ai_screening_started",
       report_id: (from job),
       timestamp: (now)
     }
```

#### Step 4B: AI Assessment
```
System (gateway.py):
  1. Fetch report data + media from database
  2. Load media file from disk
  3. Select AI provider:
     - If OPENAI_API_KEY set → Use OpenAI adapter (openai_adapter.py)
     - Else if GEMINI_API_KEY set → Use Gemini adapter (gemini.py)
     - Else → Return demo/mock result
  
  CASE 1: Real OpenAI Integration
    ├─ openai_adapter.assess_evidence()
    ├─ Call: OpenAI GPT-4V API
    │   {
    │     model: "gpt-4-vision-preview",
    │     messages: [
    │       {
    │         role: "user",
    │         content: [
    │           {text: "Assess if this violates helmet law..."},
    │           {type: "image_url", image_url: {url: (base64 encoded)}}
    │         ]
    │       }
    │     ]
    │   }
    ├─ Response: JSON with:
    │   {
    │     violation_detected: true/false,
    │     confidence: 0.95,
    │     flags: [description of issues],
    │     assessment: "text explanation",
    │     recommendation: "approve" / "reject" / "flag-for-review"
    │   }
    └─ Store result in database
  
  CASE 2: Real Gemini Integration
    ├─ gemini.py:assess_evidence()
    ├─ Call: Google Gemini API
    │   Similar payload to OpenAI
    └─ Store result in database
  
  CASE 3: Demo Mode (No API keys)
    ├─ Return simulated result
    ├─ Status: "failed" (demo cannot validate real evidence)
    ├─ Message: "AI processing unavailable; officer can still review"
    └─ Store demo result in database
```

#### Step 4C: AI Job Completes
```
System (gateway.py + app.py):
  1. Assessment result from Step 4B → Store in ai_job record
     {
       job_id: (from Step 4A),
       status: "completed",
       outcome: (violation_detected, confidence, flags),
       completed_at: (ISO-8601)
     }
  2. Update report status → "awaiting-review"
     (Citizen can now see report in their history)
  3. Insert event:
     {
       event_type: "ai_screening_completed",
       report_id: (from job),
       ai_outcome: (result from Step 4B),
       timestamp: (now)
     }
  4. Report is NOW READY for officer review (Step 5)
```

---

### **PHASE 5: CITIZEN STATUS TRACKING (While AI Runs)**

#### Step 5A: Citizen Polls Status
```
Frontend (citizen-dashboard.html):
  - Timer: Check every 30 seconds

GET /api/reports/{report_id}
Authorization: Bearer {session_token}

Response states (loop until status != "submitted"):
  {
    "report_id": "abc456def789",
    "status": "submitted",              ← Waiting for AI (Step 3B)
    "ai_job_id": "job123abc",
    "ai_state": "pending"
  }
  ↓ (wait 30s, check again)
  
  {
    "report_id": "abc456def789",
    "status": "submitted",              ← Still waiting
    "ai_job_id": "job123abc",
    "ai_state": "processing"            ← AI is working
  }
  ↓ (wait 30s, check again)
  
  {
    "report_id": "abc456def789",
    "status": "awaiting-review",        ← AI DONE (Step 4C)
    "ai_job_id": "job123abc",
    "ai_state": "failed",               ← Demo mode shows "failed"
    "ai_outcome": {
      "message": "AI processing unavailable; officer can still review",
      "status": "failed"
    }
  }
  
Frontend displays:
  - "Status: Awaiting Officer Review"
  - "AI Assessment: Failed (officer can still review)"
  - "Report submitted at: 2026-11-13 11:30:12 AM"
```

---

### **PHASE 6: OFFICER REVIEW & DECISION**

#### Step 6A: Officer Logs In
```
Officer opens: http://127.0.0.1:8000/officer-dashboard.html

Frontend checks:
  ├─ Is there a valid officer session token?
  │   (Sent via Authorization header, not localStorage)
  ├─ If NO → Redirect to /officer-login.html
  └─ If YES → Load officer queue
```

#### Step 6B: Officer Sees Queue
```
GET /api/authority/reports?limit=10
Authorization: Bearer {ROADWATCH_REVIEWER_TOKEN}

Backend:
  1. validate_officer_token(token) → Check token is valid
     - Token = environment variable ROADWATCH_REVIEWER_TOKEN
     - If invalid → Response 401 Unauthorized
  2. database.get_reports_queue(limit=10) → Fetch from "awaiting-review"
  3. Response → 200 OK
     {
       "reports": [
         {
           "report_id": "abc456def789",
           "citizen_id": "DL123ABC",
           "violation_type": "helmet",
           "vehicle_number": "DL01AB1234",
           "location": "Delhi, Connaught Place",
           "status": "awaiting-review",
           "created_at": "2026-11-13T11:30:12Z",
           "media_count": 1,
           "ai_state": "failed"
         },
         ... (more reports)
       ],
       "total": 8,
       "page": 1,
       "page_size": 10
     }

Frontend displays:
  - Table of 10 reports in queue
  - Each row clickable to view details (Step 6C)
```

#### Step 6C: Officer Views Report Details
```
GET /api/authority/reports/{report_id}
Authorization: Bearer {ROADWATCH_REVIEWER_TOKEN}

Response → 200 OK
{
  "report_id": "abc456def789",
  "citizen_id": "DL123ABC",
  "violation_type": "helmet",
  "vehicle_number": "DL01AB1234",
  "location": "Delhi, Connaught Place",
  "created_at": "2026-11-13T11:30:12Z",
  "status": "awaiting-review",
  "provisional_points": 0,
  
  "media": [
    {
      "media_id": "abc123def456",
      "file_type": "jpeg",
      "file_size": 2048000,
      "url": "/api/media/abc123def456/abc123def456.jpg"
    }
  ],
  
  "ai_assessment": {
    "job_id": "job123abc",
    "state": "failed",
    "outcome": {
      "message": "AI processing unavailable; officer can still review",
      "status": "failed"
    },
    "completed_at": "2026-11-13T11:31:45Z"
  },
  
  "events": [
    {
      "event_id": "evt1",
      "event_type": "report_submitted",
      "timestamp": "2026-11-13T11:30:12Z",
      "actor_type": "citizen"
    },
    {
      "event_id": "evt2",
      "event_type": "ai_screening_started",
      "timestamp": "2026-11-13T11:30:13Z"
    },
    {
      "event_id": "evt3",
      "event_type": "ai_screening_completed",
      "timestamp": "2026-11-13T11:31:45Z"
    }
  ]
}

Frontend displays:
  ├─ Report Header:
  │   └─ Violation: helmet | Points: 2 | Status: Awaiting Review
  ├─ Citizen Info:
  │   └─ ID: DL123ABC | Location: Delhi, Connaught Place
  ├─ Media Preview:
  │   └─ [Image thumbnail with click-to-view]
  ├─ AI Assessment:
  │   └─ "Assessment failed (AI processing unavailable; officer can still review)"
  └─ Timeline:
      └─ Submitted 11:30:12 AM → Screening started → Screening completed
```

#### Step 6D: Officer Views Media
```
GET /api/media/{media_id}/{filename}
Authorization: Bearer {ROADWATCH_REVIEWER_TOKEN}

Backend:
  1. validate_officer_token(token) → Officer access OK
  2. database.get_media(media_id) → Fetch metadata
  3. verify file exists on disk
  4. Response → 200 OK
     └─ File content (image/jpeg or video/mp4)

Frontend:
  - Display image or video player
  - Officer examines evidence
  - "This clearly shows someone without helmet"
```

#### Step 6E: Officer Makes Decision (APPROVE)
```
POST /api/authority/reports/{report_id}/decision
Authorization: Bearer {ROADWATCH_REVIEWER_TOKEN}
Content-Type: application/json

Request Body:
{
  "action": "approve",               ← OR "reject" OR "request-info"
  "comments": "Clear helmet violation. Provisional 2 points awarded."
}

Backend Processing:
  1. validate_officer_token(token) → Officer access OK
  2. database.get_report(report_id) → Fetch report
  3. Validate action ∈ ["approve", "reject", "request-info"]
  4. CASE: action = "approve"
     ├─ Get violation_type from report
     ├─ Lookup POINTS_BY_VIOLATION["helmet"] → 2 points
     ├─ Update report record:
     │   {
     │     status: "approved",
     │     provisional_points: 2,
     │     updated_at: (now)
     │   }
     ├─ Insert event:
     │   {
     │     event_type: "officer_decision",
     │     decision: "approve",
     │     points_awarded: 2,
     │     officer_comments: (from request),
     │     timestamp: (now),
     │     actor_type: "officer",
     │     actor_id: "officer_user"
     │   }
     └─ Response → 200 OK
        {
          "report_id": "abc456def789",
          "status": "approved",
          "provisional_points": 2,
          "decision_timestamp": "2026-11-13T16:16:21Z",
          "message": "Decision recorded successfully"
        }

Frontend:
  - Display success message
  - "Report approved! Provisional points: 2"
  - Auto-return to queue (Step 6B)
```

#### Step 6F: Officer Makes Decision (REJECT)
```
POST /api/authority/reports/{report_id}/decision

Request Body:
{
  "action": "reject",
  "comments": "Image too blurry; cannot confirm violation."
}

Backend:
  ├─ Update report:
  │   {
  │     status: "rejected",
  │     provisional_points: 0,
  │     rejection_reason: (from comments)
  │   }
  └─ Insert event: event_type="officer_decision", decision="reject"

Frontend:
  - Display: "Report rejected"
  - Auto-return to queue
```

#### Step 6G: Officer Makes Decision (REQUEST INFO)
```
POST /api/authority/reports/{report_id}/decision

Request Body:
{
  "action": "request-info",
  "comments": "Can you provide vehicle registration? Hard to read in photo."
}

Backend:
  ├─ Update report:
  │   {
  │     status: "awaiting-citizen-info",
  │     provisional_points: 0
  │   }
  ├─ Insert event: event_type="officer_decision", decision="request-info"
  └─ Citizen can now see this in Step 5A and resubmit evidence

Frontend:
  - Display: "Clarification requested"
  - Auto-return to queue
```

---

### **PHASE 7: CITIZEN RESPONDS TO CLARIFICATION REQUEST**

#### Step 7A: Citizen Sees Request in Dashboard
```
GET /api/reports/{report_id}

Report status changed to "awaiting-citizen-info" (from Step 6G)

Frontend displays:
  - "⚠️ Officer is requesting clarification"
  - "Message: Can you provide vehicle registration? Hard to read in photo."
  - "Clarification Form" button
```

#### Step 7B: Citizen Resubmits with Clarification
```
POST /api/reports/{report_id}/clarification
Authorization: Bearer {session_token}

Request Body:
{
  "clarification_text": "Here is a clearer photo showing the vehicle registration.",
  "media_id": "new_media_id_from_Step2B"  ← New upload from citizen
}

Backend:
  1. database.get_report(report_id) → Verify report exists & status="awaiting-citizen-info"
  2. Insert event:
     {
       event_type: "clarification_submitted",
       report_id: (from request),
       clarification_text: (from request),
       new_media_id: (from request),
       timestamp: (now)
     }
  3. Update report status → "resubmitted"
  4. Re-enqueue AI screening (Step 4A-C)
  5. Response → 200 OK

Frontend:
  - Display success: "Clarification submitted!"
  - Return to status tracker (Step 5A)
  - Begin polling again (status should transition from "resubmitted" → "awaiting-review")
```

---

### **PHASE 8: CITIZEN SEES FINAL DECISION**

#### Step 8A: Citizen Polling Completes (From Step 5A)
```
After officer decision is made (Step 6E, 6F, 6G):

GET /api/reports/{report_id}

Response changes to:
{
  "report_id": "abc456def789",
  "status": "approved",                ← Final status
  "provisional_points": 2,
  "decision_timestamp": "2026-11-13T16:16:21Z",
  "officer_comments": "Clear helmet violation. Provisional 2 points awarded.",
  ...
}

Frontend displays:
  ├─ Status: ✅ APPROVED
  ├─ Provisional Points: 2
  ├─ Officer Decision: "Clear helmet violation. Provisional 2 points awarded."
  ├─ Timeline:
  │   ├─ Submitted: 11:30:12 AM
  │   ├─ AI Screening: Started → Completed (Failed/Demo)
  │   └─ Officer Decision: 16:16:21 (Approved)
  └─ Next Steps: "Your points will be finalized by transport authority"
```

---

## 🔐 AUTHENTICATION SUMMARY

### Citizen Token (JWT)
```
Header: X-Citizen-Id (demo mode)
  OR
Authorization: Bearer {session_token} (real mode)

Token payload:
{
  "citizen_id": "DL123ABC",
  "type": "citizen",
  "exp": (24 hours from login time)
}

Used for:
  - POST /api/media/upload
  - POST /api/reports
  - GET /api/reports (own reports only)
  - GET /api/reports/{id} (own report only)
  - POST /api/reports/{id}/clarification
```

### Officer Token (Bearer)
```
Authorization: Bearer {ROADWATCH_REVIEWER_TOKEN}

Token = environment variable (simple string, no JWT)
  - Set via: export ROADWATCH_REVIEWER_TOKEN='local-reviewer-only'
  - Used in all /api/authority/* endpoints
  - Multiple officers share same token (no per-officer tracking in MVP)

Used for:
  - GET /api/authority/reports (full queue)
  - GET /api/authority/reports/{id} (any report details)
  - POST /api/authority/reports/{id}/decision
```

---

## 📊 DATABASE RECORDS CREATED

### When Citizen Submits Report (Step 3B):
1. **reports table** - 1 new row
   - report_id, citizen_id, violation_type, vehicle_number, location, media_id
   - status="submitted", provisional_points=0
   - created_at, updated_at timestamps

2. **ai_jobs table** - 1 new row
   - job_id, report_id, status="pending", created_at

3. **events table** - 1 new row (immutable)
   - event_type="report_submitted", report_id, citizen_id, timestamp

### When AI Completes (Step 4C):
4. **ai_jobs table** - Updated (same row as #2)
   - status="completed", outcome={...}, completed_at

5. **events table** - 1 new row
   - event_type="ai_screening_completed", report_id, outcome, timestamp

### When Officer Approves (Step 6E):
6. **reports table** - Updated (same row as #1)
   - status="approved", provisional_points=2, updated_at

7. **events table** - 1 new row
   - event_type="officer_decision", report_id, decision="approve", points=2, timestamp

---

## 🔄 STATUS TRANSITIONS

```
Citizen Submit (Step 3)
        ↓
   "submitted"  ← Waiting for AI
        ↓
[AI Screening Happens - Step 4]
        ↓
"awaiting-review"  ← Officer can see in queue
        ↓
[Officer Reviews - Step 6]
        ↓
  ┌─────┼─────┐
  ↓     ↓     ↓
"app" "rej" "aw-citizen"  ← Three possible outcomes
  ↓     ↓     ↓
[END] [END] Citizen Resubmit (Step 7)
              ↓
          "resubmitted"
              ↓
        [Go back to "awaiting-review"]
```

---

## ✅ COMPLETE FLOW CHECKLIST

- [ ] **Authentication:** Citizen JWT issued at login
- [ ] **Media Upload:** File validated, hashed, stored (Step 2)
- [ ] **Report Submit:** Report created + AI job queued (Step 3)
- [ ] **AI Processing:** Job picked up, assessment run, result stored (Step 4)
- [ ] **Status Poll:** Citizen checks every 30s (Step 5)
- [ ] **Officer Queue:** Officer sees report in queue (Step 6B)
- [ ] **Officer Review:** Officer views details + media (Step 6C, 6D)
- [ ] **Officer Decision:** Report marked approved/rejected/request-info (Step 6E/F/G)
- [ ] **Citizen Notification:** Citizen sees final decision via polling (Step 8)
- [ ] **Audit Trail:** Every action logged in immutable events table

---

## 🎯 KEY POINTS

1. **All citizen authentication** done via JWT bearer token (or X-Citizen-Id header in demo)
2. **All officer authentication** done via shared ROADWATCH_REVIEWER_TOKEN environment variable
3. **AI screening is fully asynchronous** - report submitted in ~100ms, AI runs in background
4. **Status polling** - citizen checks every 30s; no push notifications in MVP
5. **Immutable audit trail** - every action creates an event record that can never be modified
6. **No external APIs required for MVP** - works in demo mode with mock results
7. **Real Gemini/OpenAI integration ready** - if API keys provided, uses real AI
8. **Database is SQLite** - file-based, zero setup needed locally

---

**Last Updated:** 2026-11-13  
**Status:** ✅ Verified and operational
