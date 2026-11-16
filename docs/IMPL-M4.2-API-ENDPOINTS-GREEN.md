# IMPL-M4.2-API-ENDPOINTS-GREEN.md

**Milestone:** M4.2 (API ENDPOINTS GREEN)  
**Type:** GREEN (Implementation to pass RED tests)  
**Duration:** 2 days  
**Dependency:** M4.1 ✅ (10 RED test cases defined), M2 ✅ (app.py structure)  
**Approval Status:** ⏳ Pending  

---

## 📋 Objective

Implement 6 API endpoint handlers to pass all 10 RED test cases from M4.1 (`tests/test_api_endpoints.py`).

---

## 🎯 Deliverables

### Add Endpoints to `app.py`

**File:** `C:\Users\avina\Downloads\avinash-repo\v11\Traffic\app.py` (modify existing)

**Add 6 endpoints:**

#### 1. POST /api/reports — Citizen Submit Report

**Signature:**
```python
@app.post("/api/reports", tags=["Citizen"], status_code=201)
async def submit_report(request: Request, body: dict) -> dict:
```

**Request:**
```json
{
  "violation_type": "helmet",
  "location": "MG Road, Bangalore",
  "media_id": "media-abc123"
}
```

**Response (201):**
```json
{
  "report_id": "report-xyz789",
  "status": "submitted",
  "violation_type": "helmet",
  "created_at": "2026-11-01T19:20:00Z",
  "citizen_id": "citizen-001"
}
```

**Logic:**
- Extract citizen_id from request.scope["citizen_id"] (set by identity middleware)
- Validate violation_type (helmet, triple-riding, red-light)
- Verify media_id exists and belongs to citizen_id
- Create report record in database with status=submitted
- Create "report_submitted" event in events table
- Return 201 with report_id

**Error Cases:**
- 400: Missing required fields
- 401: Missing X-Citizen-Id header
- 403: Media belongs to different citizen
- 404: Media not found

---

#### 2. GET /api/reports — Citizen Report History

**Signature:**
```python
@app.get("/api/reports", tags=["Citizen"])
async def fetch_reports(request: Request) -> dict:
```

**Query Parameters:**
- `page` (optional, default=1)
- `page_size` (optional, default=20)

**Response (200):**
```json
{
  "reports": [
    {
      "id": "report-xyz789",
      "status": "submitted",
      "violation_type": "helmet",
      "location": "MG Road, Bangalore",
      "created_at": "2026-11-01T19:20:00Z",
      "updated_at": "2026-11-01T19:20:00Z"
    }
  ],
  "total_count": 5,
  "page": 1,
  "page_size": 20
}
```

**Logic:**
- Extract citizen_id from request.scope["citizen_id"]
- Query reports table WHERE citizen_id=X, ordered by created_at DESC
- Apply pagination (page, page_size)
- Return list of own reports only (access control)

**Error Cases:**
- 401: Missing X-Citizen-Id header
- 400: Invalid pagination params

---

#### 3. GET /api/reports/{id} — Report Details + Timeline

**Signature:**
```python
@app.get("/api/reports/{report_id}", tags=["Citizen"])
async def fetch_report_detail(request: Request, report_id: str) -> dict:
```

**Response (200):**
```json
{
  "id": "report-xyz789",
  "citizen_id": "citizen-001",
  "status": "awaiting-review",
  "violation_type": "helmet",
  "location": "MG Road, Bangalore",
  "provisional_points": null,
  "created_at": "2026-11-01T19:20:00Z",
  "updated_at": "2026-11-01T19:25:00Z",
  "timeline": [
    {
      "id": "event-001",
      "event_type": "status_change",
      "actor": "citizen",
      "old_status": null,
      "new_status": "submitted",
      "created_at": "2026-11-01T19:20:00Z",
      "reason": null
    },
    {
      "id": "event-002",
      "event_type": "status_change",
      "actor": "system",
      "old_status": "submitted",
      "new_status": "screening",
      "created_at": "2026-11-01T19:21:00Z",
      "reason": null
    },
    {
      "id": "event-003",
      "event_type": "status_change",
      "actor": "system",
      "old_status": "screening",
      "new_status": "awaiting-review",
      "created_at": "2026-11-01T19:22:00Z",
      "reason": null
    }
  ]
}
```

**Logic:**
- Extract citizen_id from request.scope["citizen_id"]
- Query reports table WHERE id=report_id
- Verify citizen_id matches (access control)
- Query events table WHERE report_id=report_id, ordered by created_at ASC
- Return report + timeline

**Error Cases:**
- 401: Missing X-Citizen-Id header
- 403: Report belongs to different citizen
- 404: Report not found

---

#### 4. POST /api/reports/{id}/clarification — Citizen Clarification Response

**Signature:**
```python
@app.post("/api/reports/{report_id}/clarification", tags=["Citizen"])
async def submit_clarification(request: Request, report_id: str, body: dict) -> dict:
```

**Request:**
```json
{
  "clarification_text": "Here is better photo of the violation",
  "new_media_id": "media-def456"
}
```

**Response (200):**
```json
{
  "report_id": "report-xyz789",
  "status": "resubmitted",
  "new_media_id": "media-def456",
  "clarification_event": {
    "id": "event-004",
    "old_status": "awaiting-citizen-info",
    "new_status": "resubmitted",
    "created_at": "2026-11-01T19:30:00Z"
  }
}
```

**Logic:**
- Extract citizen_id from request.scope["citizen_id"]
- Query reports table WHERE id=report_id
- Verify citizen_id matches (access control)
- Verify report status is "awaiting-citizen-info"
- Verify new_media_id exists and belongs to citizen
- Update report status to "resubmitted"
- Create "clarification" event in events table
- Return 200 with updated status

**Error Cases:**
- 401: Missing X-Citizen-Id header
- 403: Report belongs to different citizen or citizen not authorized
- 404: Report or media not found
- 409: Report status not awaiting-citizen-info

---

#### 5. GET /api/authority/reports — Officer Review Queue

**Signature:**
```python
@app.get("/api/authority/reports", tags=["Officer"])
async def fetch_queue(request: Request) -> dict:
```

**Headers Required:**
- Authorization: "Bearer {officer_token}" OR X-Reviewer-Token

**Query Parameters:**
- `page` (optional, default=1)
- `page_size` (optional, default=10)
- `status` (optional, filter by status)

**Response (200):**
```json
{
  "reports": [
    {
      "id": "report-xyz789",
      "citizen_id": "citizen-001",
      "status": "awaiting-review",
      "violation_type": "helmet",
      "location": "MG Road, Bangalore",
      "created_at": "2026-11-01T19:20:00Z",
      "media_count": 1,
      "submission_age_seconds": 300
    }
  ],
  "total_count": 42,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

**Logic:**
- Verify officer authorization (demo token or OIDC)
- Query reports table WHERE status IN (awaiting-review, resubmitted)
- Order by created_at ASC (FIFO)
- Apply pagination
- Include media_count from media table
- Return queue

**Error Cases:**
- 401: Missing/invalid authorization
- 400: Invalid pagination params

---

#### 6. POST /api/authority/reports/{id}/decision — Officer Decision

**Signature:**
```python
@app.post("/api/authority/reports/{report_id}/decision", tags=["Officer"])
async def make_decision(request: Request, report_id: str, body: dict) -> dict:
```

**Request (Approve):**
```json
{
  "action": "approve"
}
```

**Request (Reject):**
```json
{
  "action": "reject",
  "reason": "blurry"
}
```

**Request (Request Info):**
```json
{
  "action": "request-info"
}
```

**Response (200) — Approve:**
```json
{
  "report_id": "report-xyz789",
  "status": "approved",
  "violation_type": "helmet",
  "provisional_points": 2,
  "decision_event": {
    "id": "event-005",
    "actor": "officer",
    "old_status": "awaiting-review",
    "new_status": "approved",
    "created_at": "2026-11-01T19:35:00Z",
    "provisional_points": 2
  }
}
```

**Response (200) — Reject:**
```json
{
  "report_id": "report-xyz789",
  "status": "rejected",
  "reason": "blurry",
  "decision_event": {
    "id": "event-005",
    "actor": "officer",
    "old_status": "awaiting-review",
    "new_status": "rejected",
    "reason": "blurry",
    "created_at": "2026-11-01T19:35:00Z"
  }
}
```

**Response (200) — Request Info:**
```json
{
  "report_id": "report-xyz789",
  "status": "awaiting-citizen-info",
  "decision_event": {
    "id": "event-005",
    "actor": "officer",
    "old_status": "awaiting-review",
    "new_status": "awaiting-citizen-info",
    "created_at": "2026-11-01T19:35:00Z"
  }
}
```

**Logic:**
- Verify officer authorization
- Query reports table WHERE id=report_id
- Verify report status is "awaiting-review"
- Based on action:
  - **approve:** 
    - Set status="approved"
    - Calculate provisional_points based on violation_type (helmet=2, triple-riding=3, red-light=3)
    - Create decision event with points
  - **reject:**
    - Set status="rejected"
    - Store reason in event
    - Create decision event with reason
  - **request-info:**
    - Set status="awaiting-citizen-info"
    - Create decision event
- Update report record
- Create event in events table
- Return 200 with updated status

**Error Cases:**
- 401: Missing/invalid authorization
- 404: Report not found
- 409: Report status not awaiting-review

---

## 📊 RED Test Coverage (M4.1)

All 10 tests in `tests/test_api_endpoints.py` must PASS:

1. test_citizen_submit_report_returns_201_with_report_id ← POST /api/reports
2. test_citizen_fetch_history_returns_own_reports ← GET /api/reports
3. test_citizen_fetch_report_details_with_timeline ← GET /api/reports/{id}
4. test_officer_query_review_queue_returns_paginated_list ← GET /api/authority/reports
5. test_officer_view_case_detail_shows_evidence ← GET /api/reports/{id} (officer access)
6. test_officer_approve_report_awards_points ← POST /api/authority/reports/{id}/decision (approve)
7. test_officer_reject_with_reason_stores_reason ← POST /api/authority/reports/{id}/decision (reject)
8. test_officer_request_clarification_requeues_case ← POST /api/authority/reports/{id}/decision (request-info)
9. test_citizen_clarification_response_resubmits_case ← POST /api/reports/{id}/clarification
10. test_officer_queue_reflects_requeued_cases ← GET /api/authority/reports (status=resubmitted)

---

## 🔧 Implementation Details

### HTTP Status Codes

| Status | When |
|--------|------|
| 200 | Successful read or update |
| 201 | Report created successfully |
| 400 | Bad request (missing fields, invalid params) |
| 401 | Missing/invalid authorization |
| 403 | Access denied (citizen sees other's report, etc.) |
| 404 | Resource not found |
| 409 | Conflict (wrong status for operation) |

### Points Calculation

```python
POINTS_BY_VIOLATION = {
    "helmet": 2,
    "triple-riding": 3,
    "red-light": 3
}
```

### Access Control

**Citizen endpoints:**
- Can access own reports only
- Cannot see other citizens' reports
- Cannot download others' media

**Officer endpoints:**
- Can see all reports
- Can see all media
- Requires authorization header (demo token: "local-reviewer-only" or real token)

### Database Integration

**Tables used:**
- reports — Main report record
- events — Immutable audit trail
- media — Media records (for media_count)
- operators — Officer records (optional, for future officer-specific logic)

**Transactions:**
- Each endpoint operation must be atomic
- On error: rollback all changes
- On success: commit event + report update together

---

## ✅ Definition of Done

- [ ] All 6 endpoints added to app.py
- [ ] All 10 M4.1 RED tests PASS (not SKIPPED)
- [ ] HTTP status codes correct (201 for create, 200 for read/update, 4xx for errors)
- [ ] Access control working (citizen isolation, officer override)
- [ ] Authorization enforcement (X-Citizen-Id for citizen endpoints, Authorization for officer)
- [ ] Points calculation correct (helmet=2, triple-riding=3, red-light=3)
- [ ] Events logged for all state changes (immutable audit trail)
- [ ] Pagination working (page, page_size, total_count)
- [ ] Error handling explicit (400, 401, 403, 404, 409)
- [ ] Transactions atomic (no partial updates)
- [ ] Code passes production code review
- [ ] Commit traceable to this Implementation Plan

---

## 🔍 Verification Steps

### Step 1: Run M4.1 tests
```bash
cd C:\Users\avina\Downloads\avinash-repo\v11\Traffic
python -m pytest tests/test_api_endpoints.py -v
```

**Expected:** All 10 tests PASS (not SKIPPED)

### Step 2: Test each endpoint manually
```bash
# Start app
uvicorn app:app --reload

# In another terminal:

# Test 1: Submit report (citizen)
curl -X POST http://127.0.0.1:8000/api/reports \
  -H "X-Citizen-Id: citizen-001" \
  -H "Content-Type: application/json" \
  -d '{"violation_type": "helmet", "location": "MG Road", "media_id": "media-001"}'

# Test 2: Fetch history (citizen)
curl http://127.0.0.1:8000/api/reports \
  -H "X-Citizen-Id: citizen-001"

# Test 3: Fetch detail (citizen)
curl http://127.0.0.1:8000/api/reports/report-001 \
  -H "X-Citizen-Id: citizen-001"

# Test 4: Officer queue
curl http://127.0.0.1:8000/api/authority/reports \
  -H "Authorization: Bearer local-reviewer-only"

# Test 5: Officer decision
curl -X POST http://127.0.0.1:8000/api/authority/reports/report-001/decision \
  -H "Authorization: Bearer local-reviewer-only" \
  -H "Content-Type: application/json" \
  -d '{"action": "approve"}'
```

### Step 3: Verify access control
```bash
# Try to access another citizen's report (should fail with 403)
curl http://127.0.0.1:8000/api/reports/report-from-citizen-002 \
  -H "X-Citizen-Id: citizen-001"
# Expected: 403 Forbidden
```

### Step 4: Verify events logged
```bash
python -c "
from bootstrap import get_db
db = get_db()
events = db.execute('SELECT * FROM events WHERE report_id=?', ('report-001',)).fetchall()
print(f'[OK] Events logged: {len(events)}')
for evt in events:
    print(f'  - {evt[\"event_type\"]}: {evt[\"old_status\"]} → {evt[\"new_status\"]}')
"
```

---

## 📝 Implementation Checklist

**Before starting:**
- [ ] M4.1 RED tests reviewed and understood
- [ ] app.py structure reviewed (lifespan, middleware, imports)
- [ ] Database schema (reports, events, media tables) reviewed
- [ ] Points calculation approved

**During implementation:**
- [ ] POST /api/reports implemented (citizen submit)
- [ ] GET /api/reports implemented (citizen history, paginated)
- [ ] GET /api/reports/{id} implemented (report detail + timeline)
- [ ] POST /api/reports/{id}/clarification implemented (citizen response)
- [ ] GET /api/authority/reports implemented (officer queue, paginated)
- [ ] POST /api/authority/reports/{id}/decision implemented (approve/reject/request-info)
- [ ] Access control verified (citizen isolation, officer override)
- [ ] Authorization enforcement verified
- [ ] Points calculation verified
- [ ] Events logged for all changes

**After implementation:**
- [ ] All 10 tests PASS
- [ ] No test failures or errors
- [ ] Manual endpoint testing works (curl commands)
- [ ] Access control bypass attempts fail
- [ ] Events audit trail complete
- [ ] Commit with proper traceability

---

## 🚨 Common Pitfalls to Avoid

1. **Access control bypass** — Always verify citizen_id from request.scope; don't trust request body
2. **Silent data loss** — If event insert fails, rollback entire operation
3. **Wrong status codes** — Use 201 for create, 200 for read/update, 4xx for errors
4. **Points not awarded** — Must include provisional_points in response AND in event
5. **Missing events** — Every state change must create event (no silent updates)
6. **Race conditions** — Status transitions must be atomic (check status + update in one transaction)
7. **Pagination off-by-one** — Test page=1, page=2, last page carefully

---

## 🔗 Related Documents

- **Plan.md** — M4.2 milestone definition
- **IMPL-M4.1-API-ENDPOINTS-RED.md** — RED test specifications (10 test cases)
- **tests/test_api_endpoints.py** — Actual test code to pass
- **app.py** — FastAPI entry point (M2)
- **bootstrap.py** — Database functions

---

**Approved By:** [Awaiting approval]  
**Approved Date:** [Awaiting approval]  
**Implementation Status:** ⏹️ NOT STARTED

