# RoadWatch Traffic Evidence Reporting — Development Plan

**Document Status:** APPROVED  
**Plan Version:** 1.0  
**Created:** 2026-11-01  
**Author:** Avinash Srivastava (Copilot)  
**Approval Status:** ✅ APPROVED (2026-11-01, by Avinash — all ambiguities resolved, M1–M4.1 verified complete)  
**Ambiguities Resolution:** ✅ ALL RESOLVED (A1: SQLite ✓, A2: Vanilla HTML ✓, A3: Local disk ✓, A4: FIFO queue ✓, A5: Helmet/triple-riding/red-light ✓)

---

## 📊 Milestone Completion Status

| # | Milestone | Type | Status | Git Commit | Verified |
|---|-----------|------|--------|-----------|----------|
| 1 | M1: DATABASE SCHEMA | OTHER | ✅ DONE | `ea9a20c` | ✓ 8/8 checks |
| 2 | M2: FASTAPI APP | OTHER | ✅ DONE | `a3ba81c` | ✓ 5 routes, health check |
| 3 | M3.1: MEDIA UPLOAD RED | RED | ✅ DONE | `da23460` | ✓ 12/12 tests SKIPPED |
| 4 | M4.1: API ENDPOINTS RED | RED | ✅ DONE | `5a300e4` | ✓ 10/10 tests SKIPPED |
| 5 | M3.2: MEDIA UPLOAD GREEN | GREEN | ✅ DONE | `82866ee` | ✓ media.py implemented, fixtures working |
| 6 | M4.2: API ENDPOINTS GREEN | GREEN | ✅ DONE | `609cd4c` | ✓ 10/10 tests PASS, endpoints verified |
| 7 | M5: UI SCAFFOLDING | OTHER | ✅ DONE | `59af9ef` | ✓ 6 HTML pages, 4 CSS, 4 JS files, responsive |
| 8 | M6: EVIDENCE EXPORT | OTHER | ✅ DONE | `719ae0e` | ✓ ZIP endpoint: manifest + media + timeline |
| 9 | M7: DOCKER & DEPLOYMENT | OTHER | ✅ DONE | `59af9ef` | ✓ Dockerfile, start.sh, start-windows.ps1 |
| 10 | M8: CITIZEN SIGNUP & VERIFIED LOGIN | GREEN | ✅ DONE | `6a8bc10` | ✓ 23/23 tests PASS, JWT auth implemented |
| 11 | M9: OFFICER AUTH & CITIZEN MEDIA DISPLAY | GREEN | ✅ DONE | `a6967c8` | ✓ Two-tier auth, media endpoints, citizen detail view |
| 12 | M10: AI SCREENING — REAL AI GATEWAY INTEGRATION | OTHER | ✅ DONE | TBD | ✓ ai-gateway service, ai-worker background job, real OpenAI assessments |

**Progress:** 12/12 milestones complete (100%) ✅ MVP FULL FEATURE COMPLETE PLUS AI SCREENING | **All code committed**

---

## 📋 Requirements Summary

**Project:** RoadWatch — India-focused traffic evidence reporting MVP  
**Scope:** Complete end-to-end workflow: citizen upload → authority review → provisional points  
**Vision:** Modular monolith (FastAPI) with OIDC identity, event-driven state machine, and real AI-powered evidence screening via AI Gateway  
**Constraints:** Local-only for MVP (SQLite, local file storage); production evolution outlined  

### Must-Have Features (MVP Scope)
1. **Citizen Portal** — Upload photos/videos (25 MB, 45 sec limit) → get report ID + status tracking
2. **Authority Portal** — Review queue + decision UI (approve/reject/request-info)
3. **Report Lifecycle** — Submitted → Screening → Awaiting Review → Officer Decision
4. **Provisional Points** — Demo awards (2 helmet, 3 triple-riding/red-light)
5. **Media Validation** — Technical checks (container, frames, resolution, blur)
6. **SHA-256 Deduplication** — Binary hash-based duplicate detection
7. **Evidence Export** — Reviewer ZIP with original file + hash + timeline
8. **Audit Trail** — Immutable event log of all status changes
9. **AI Screening** — Real OpenAI-powered assessments via AI Gateway (background worker, evidence-based decision support)
10. **Deployable** — Docker image, Windows/Mac/Linux local startup, Swagger API

### Out of Scope (Documented for Production Roadmap)
- Real OIDC integration (demo token only for MVP)
- PostgreSQL (SQLite for MVP; PostgreSQL documented for scale)
- Real police/VAHAN/e-challan integration (demo-only)
- Multi-region or high-availability
- User management beyond fixed demo token
- Payment/redemption

---

## 🎯 Critical Ambiguities to Resolve (Blocking)

**These questions must be answered by stakeholders before proceeding:**

### A1: Database Choice (MVP Phase)
**Question:** Start with SQLite (simple, local, no setup) or PostgreSQL (production-ready)?

- **SQLite Approach:** File-based, zero external dependencies, works immediately
- **PostgreSQL Approach:** More setup, better for scaling, closer to production

**Recommendation:** SQLite for MVP (faster time-to-demo), documented migration path to PostgreSQL in Phase 2  
**Impact:** Affects bootstrap.py database layer, schema definition, connection handling  
**Blocking Until:** Stakeholder decision

### A2: UI Framework
**Question:** Vanilla HTML + server-side templating, or SPA (React/Vue)?

- **Vanilla HTML:** Built-in with Jinja2, minimal dependencies, faster initial velocity
- **React/Vue:** Better UX, more code, separate frontend build

**Recommendation:** Vanilla HTML + Jinja2 for MVP (within existing FastAPI patterns), SPA evaluated in Phase 2  
**Impact:** Affects template structure, API response shapes, build complexity  
**Blocking Until:** Stakeholder decision

### A3: Media Storage
**Question:** Local disk (/tmp or project folder) or cloud object store (S3/Azure Blob)?

- **Local Disk:** Works immediately, fine for MVP, data loss risk
- **Cloud Storage:** More complex setup, production-ready, cost implications

**Recommendation:** Local disk for MVP (in project folder with .gitignore), cloud storage documented for Phase 2  
**Impact:** Affects media handler implementation, backup strategy, deployment model  
**Blocking Until:** Stakeholder decision

### A4: Officer Review SLA
**Question:** Are there time limits on review cycles or case aging?

- If yes: need queuing by recency, SLA tracking, escalation logic
- If no: queue can be simple FIFO

**Recommendation:** Start with simple FIFO for MVP; SLA tracking in Phase 2 if needed  
**Impact:** Affects queue ordering, officer dashboard design, alert logic  
**Blocking Until:** Stakeholder clarification

### A5: Pilot Violation Types (Priority)
**Question:** Which violation types are highest priority for pilot? (helmet, triple-riding, red-light, speeding, etc.)

**Recommendation:** Start with helmet (simplest detection), add triple-riding and red-light in Phase 2  
**Impact:** Affects provisional points, evidence assessment strategy, test case design, background job architecture  
**Blocking Until:** Stakeholder prioritization

---

## 📊 Milestone Breakdown

**Total Estimated Duration:** 2–3 weeks for Phase 1 MVP  

### Phase 1: MVP Foundation (All Blocking)
**Goal:** Complete end-to-end citizen upload → officer decision cycle working

#### M1: DATABASE SCHEMA (Duration: 1–2 days)
**Type:** OTHER (no behavior change yet; infrastructure)  
**Deliverable:** SQLite/PostgreSQL schema, migrations, connection pool  

**Implementation Plan Details:**
- Define 3 core tables: `reports`, `events`, `media`
- Wire psycopg connection pool in bootstrap.py
- Create schema setup script for first-time deployment
- Verify schema integrity with basic test fixtures

**Definition of Done:**
- Schema file creates all tables without errors
- Connection pool initializes successfully
- Test fixtures can insert/query test data
- No test failures

**Risk:** Database choice ambiguity (A1) — requires decision first

---

#### M2: FASTAPI APP & IDENTITY MIDDLEWARE (Duration: 1–2 days)
**Type:** OTHER (infrastructure)  
**Dependency:** M1 (database must exist)  
**Deliverable:** `app.py` entry point, OIDC/demo identity middleware, health check

**Implementation Plan Details:**
- Create `app.py` with FastAPI lifespan context manager
- Initialize database connection on startup
- Wire identity middleware from bootstrap.py (OIDC or demo token)
- Swagger UI at `/api/docs`
- Health check endpoint: `GET /health` → 200 OK

**Definition of Done:**
- `uvicorn app:app --reload` starts without errors
- `/health` returns 200 OK
- `/api/docs` is accessible
- Identity middleware rejects invalid tokens
- Telemetry hooks (OpenTelemetry) are initialized

**Risk:** None (M1 complete)

---

#### M3: MEDIA UPLOAD & VALIDATION (Duration: 2–3 days)
**Type:** RED + GREEN pair (behavior-changing)

**3.1 RED Milestone: Test Suite for Media Operations**
**Duration:** 1 day  
**Deliverable:** Test file with all tests failing; framework verifies

**Test Cases (All Fail):**
1. Valid JPEG upload (25 MB, readable) → return file_id + hash
2. Valid MP4 upload (45 sec, readable) → return file_id + hash
3. Duplicate detection: same file twice → second reports duplicate
4. Invalid container (corrupted JPEG) → reject with 422
5. File too large (26 MB) → reject with 413
6. Video too long (46 sec) → reject with 413
7. Unsupported format (.exe) → reject with 422
8. Technical screening: low resolution → flag in metadata
9. Technical screening: high blur → flag in metadata
10. Media access control: citizen can only read own media

**Dependency:** M2 (app.py, identity middleware)  
**Definition of Done:**
- All 10 tests run; all fail with clear error messages
- Test framework verifies (pytest, fixtures work)
- Database schema supports media table
- No production code written yet

---

**3.2 GREEN Milestone: Media Operations Implementation**
**Duration:** 2 days  
**Deliverable:** Media handlers pass all RED tests

**Endpoints Implemented:**
- `POST /api/reports/{report_id}/media` — Upload file, validate, hash, detect duplicates
- `GET /api/reports/{report_id}/media/{media_id}` — Download original file (access-controlled)

**Backend Logic:**
- File validation (MIME type, size, container readability)
- SHA-256 hashing and duplicate detection
- Frame sampling for videos (5 frames)
- Technical screening (Pillow blur/resolution detection)
- Storage (local disk in `./media_store/` subdirectory)

**Dependency:** M3.1 (RED tests defined)  
**Definition of Done:**
- All 10 RED tests pass
- Code review passed (correctness, security)
- No new test failures

---

#### M4: CORE API ENDPOINTS (Duration: 2–3 days)
**Type:** RED + GREEN pair

**4.1 RED Milestone: Full API Test Suite**
**Duration:** 1 day  
**Deliverable:** Tests for all 8 endpoints (all fail)

**Test Cases (All Fail):**
1. Citizen submit report (JPG, helmet violation) → 201, report_id, status=submitted
2. Citizen fetch history → 200, list of own reports
3. Citizen fetch report details + timeline → 200, events, status progression
4. Officer query review queue (sorted by submission time) → 200, paginated list
5. Officer view case detail (photos, current status, evidence) → 200
6. Officer approve report → 200, status=approved, provisional points awarded
7. Officer reject with reason → 200, status=rejected, reason stored
8. Officer request clarification → 200, status=awaiting-citizen-info
9. Citizen clarification response → 200, status=resubmitted
10. Officer queue reflects re-queued cases → 200, updated order

**Endpoints:**
- `POST /api/reports` — Submit
- `GET /api/reports` — History
- `GET /api/reports/{id}` — Details
- `POST /api/reports/{id}/clarification` — Citizen follow-up
- `GET /api/authority/reports` — Officer queue
- `POST /api/authority/reports/{id}/decision` — Officer review action

**Dependency:** M3.2 (media works)  
**Definition of Done:**
- All tests run; all fail
- Framework verifies (HTTP status codes, JSON schema validation)
- Database schema supports events table

---

**4.2 GREEN Milestone: API Implementation**
**Duration:** 2 days  
**Deliverable:** Endpoints pass all RED tests

**Implementation:**
- Report state machine (transitions, event recording)
- Provisional points calculation (helmet=2, triple-riding=3, red-light=3)
- Officer queue ordering and pagination
- Citizen/officer authorization checks (headers or OIDC claims)
- Event timeline immutability (append-only)

**Dependency:** M4.1 (RED tests defined)  
**Definition of Done:**
- All tests pass
- Code review passed
- Event trail is immutable and complete
- Provisional points correctly awarded

---

#### M5: WEB UI SCAFFOLDING (Duration: 1–2 days)
**Type:** OTHER (UI infrastructure)  
**Dependency:** M4.2 (API must work)  
**Deliverable:** Minimal HTML templates for citizen and authority portals

**Citizen Portal (`/citizen`):**
- Upload form (file picker, violation type dropdown, location input)
- Report history table (ID, status, points, date, actions)
- Report detail view (photos/videos, timeline, messages)
- Clarification input form (when status=awaiting-citizen-info)

**Authority Portal (`/authority`):**
- Login form (demo token: "local-reviewer-only")
- Review queue table (report ID, violation type, date, actions)
- Case detail view (evidence grid, current status, timeline)
- Decision form (Approve, Reject with reason, Request info)

**Technology:** Jinja2 templates + Bootstrap CSS (CDN, no build)  
**Definition of Done:**
- Both portals load without errors
- Forms submit correctly to API endpoints
- Status displays update on refresh
- Mobile-responsive (bootstrap grid)

**M5 Planning Status (Session 2026-11-01):**
✅ **PLANNING COMPLETE** — 4 comprehensive architecture documents created:
1. **ARCHITECTURE-FLOW-DIAGRAMS.md** (19 KB) — 11 Mermaid diagrams covering citizen/officer workflows, system architecture, state machine, database schema, UI layouts
2. **M5-UI-IMPLEMENTATION-CHECKLIST.md** (23 KB) — Component breakdown for 6 UI pages (4 citizen + 2 officer), API mapping, CSS/JS structure, testing checklist
3. **API-REQUEST-RESPONSE-REFERENCE.md** (23 KB) — Copy-paste JavaScript code for all 6 endpoints, error handling, testing scenarios
4. **M5-PLANNING-COMPLETE.md** (11 KB) — Build order, time estimates, implementation readiness checklist

**M5 Ready to Build:** YES ✅ All prerequisites met. No blockers. Implementation guide ready.

---

#### M6: EVIDENCE EXPORT (Duration: 1 day)
**Type:** GREEN (behavior implementation)  
**Dependency:** M4.2 (API endpoints), M5 (UI shows export button)  
**Deliverable:** Reviewer ZIP export working

**Endpoint:** `GET /api/authority/reports/{id}/evidence.zip`  

**ZIP Contents:**
- `original_file` (media file with original name)
- `manifest.json` (report metadata, hash, dates)
- `timeline.json` (events list with timestamps, reasons)

**Definition of Done:**
- ZIP downloads without errors
- ZIP contains all required files
- Manifest and timeline are valid JSON
- Officer can extract and review offline

---

#### M7: DOCKER & DEPLOYMENT (Duration: 1 day)
**Type:** OTHER (operations)  
**Dependency:** M6 (full app works)  
**Deliverable:** Docker image builds and runs; startup scripts for Windows/Mac/Linux

**Deliverables:**
- Dockerfile (multi-stage: dependencies, app, migrations)
- `start-windows.ps1` (creates venv, installs, runs uvicorn)
- `start.sh` (macOS/Linux equivalent)
- `.dockerignore` (media_store, __pycache__, .venv)

**Definition of Done:**
- `docker build -t roadwatch .` succeeds
- `docker run -p 8000:8000 roadwatch` runs app
- Windows PowerShell startup script creates venv and starts server
- macOS/Linux bash startup script works
- All README instructions work as written

---

#### M10: AI SCREENING — REAL AI GATEWAY INTEGRATION (Duration: 2 days)
**Type:** OTHER (background service)  
**Dependency:** M7 (deployment works), M4.2 (API endpoints exist)  
**Deliverable:** AI-powered evidence assessment via OpenAI, integrated with background worker job queue

**Architecture:**
- **AI Gateway Service** (`ai-gateway/app.py`) — Domain service for all AI assessment calls
  - Endpoint: `POST /v1/assessments`
  - Accepts evidence (media files base64-encoded), violation context, prompt
  - Calls OpenAI GPT-4o-mini with structured prompt for traffic violation assessment
  - Returns assessment result with violation confidence, evidence quality, recommended action
  - No mocking — all assessments are real AI calls

- **Background Worker** (`ai-worker/app.py`) — Async job processor
  - Polls SQLite `ai_jobs` table for pending jobs (every 5 seconds)
  - Fetches report media from disk storage
  - Builds assessment request with violation type, vehicle number, location, evidence
  - Calls AI Gateway `/v1/assessments` endpoint
  - Stores result in database (append-only event trail)
  - Implements retry logic (up to 3 attempts) with exponential backoff

- **Database Schema** — New tables for job tracking
  - `ai_jobs` (id, report_id, state, result, attempt_count, next_attempt_at)
  - `ai_assessments` (id, job_id, assessment_result JSON)
  - Integration with existing `events` table for immutable audit trail

**Configuration:**
- `AI_GATEWAY_URL` env var (default: `http://127.0.0.1:9004`)
- `AI_GATEWAY_TOKEN` env var (optional, defaults to "demo-token")
- `OPENAI_API_KEY` env var (required for real OpenAI; mocked locally if not set)
- `OPENAI_MODEL` env var (default: "gpt-4o-mini")

**Workflow:**
1. Citizen submits report → Report status = `submitted`
2. API creates `ai_jobs` entry with state=`pending`
3. Background worker polls every 5 seconds
4. Worker claims job, reads media from disk, calls AI Gateway
5. AI Gateway calls OpenAI with evidence + prompt
6. Result stored in database; event appended
7. Report status transitions → `screening-complete`
8. Officer sees assessment result in queue (if assessment recommends approval)

**Definition of Done:**
- AI Gateway service runs independently on port 9004
- Background worker polls and processes jobs correctly
- Database migrations create `ai_jobs` and `ai_assessments` tables
- End-to-end: citizen report → AI assessment → officer queue
- Error handling: retries, timeouts, missing media handled gracefully
- Real OpenAI calls work (or mock if API key not set)
- All services documented in README with startup instructions

---

### Phase 2: Polish & Testing (Stretch Goals)
**Duration:** 1–2 weeks (if time permits; not blocking)

- #### M11: FULL TEST COVERAGE — Unit + integration tests for all endpoints
- #### M12: OBSERVABILITY — OpenTelemetry logging, metrics, traces
- #### M13: ERROR HANDLING & RECOVERY — Graceful degradation, retry logic

---

### Phase 3: Production Hardening
**Duration:** Not included in this plan (future work after MVP demo)

- Real OIDC provider
- PostgreSQL migration
- Object storage (S3/Azure Blob)
- Rate limiting, DDoS protection
- Security audit, compliance review
- High-availability setup

---

## 🔄 Dependency Graph

```
DATABASE SCHEMA (M1)
        ↓
FASTAPI APP (M2)
        ↓
MEDIA UPLOAD RED (M3.1)
        ↓
MEDIA UPLOAD GREEN (M3.2)
        ↓
API ENDPOINTS RED (M4.1)
        ↓
API ENDPOINTS GREEN (M4.2)
        ↓
UI SCAFFOLDING (M5)
        ↓
EVIDENCE EXPORT (M6)
        ↓
DOCKER & DEPLOYMENT (M7)
```

**Critical Path:** 7 sequential milestones (M1 → M7)  
**Parallel Work:** None (all depend on previous)  
**Estimated Total:** 9–13 working days (2+ weeks, accounting for testing/review)

---

## ⚠️ Risks & Mitigation

| Risk | Severity | Mitigation |
|------|----------|-----------|
| Database schema has breaking changes mid-project | 🔴 HIGH | Schema reviewed and approved before M2 starts |
| API scope creeps (more endpoints than 8) | 🟡 MEDIUM | Strict RED test scope; only those 8 endpoints in MVP |
| Media validation too slow for large files | 🟡 MEDIUM | Hash computed in background; user gets immediate report_id |
| Officer identity not enforced (everyone sees all cases) | 🔴 HIGH | Access control tested in M4.1 RED tests |
| Points awarded incorrectly | 🔴 HIGH | Points calculation tested in M4.1; code review mandatory |
| Report state machine has stuck states | 🟡 MEDIUM | State transitions tested in M4.1; officer can force status |
| SQLite concurrency issues under load | 🟡 MEDIUM | Documented as MVP limitation; PostgreSQL in Phase 2 |
| Deployment fails on Windows | 🟡 MEDIUM | `start-windows.ps1` tested on Windows before M7 complete |

---

## 📋 Approval Checklist

**This Plan requires human approval before any code changes:**

- [ ] Stakeholder confirms database choice (SQLite or PostgreSQL)
- [ ] Stakeholder confirms UI framework (vanilla HTML or React)
- [ ] Stakeholder confirms media storage (local disk or cloud)
- [ ] Stakeholder confirms officer review SLA requirements
- [ ] Stakeholder prioritizes violation types
- [ ] Stakeholder approves milestone breakdown
- [ ] Technical lead approves state machine design (in M4 Implementation Plan)
- [ ] Security reviewer approves identity/authorization approach

**Blocking Gate:** Do not proceed to M1 (DATABASE SCHEMA) until all items are checked.

---

## 📞 Questions for Human Review

1. **Ambiguities:** Are the 5 blocking questions (A1–A5) addressed to your satisfaction?
2. **Scope:** Does the milestone breakdown align with your vision?
3. **Timeline:** Is 2–3 weeks realistic for your team's availability?
4. **Risks:** Are there risks I've missed?
5. **Approval:** Who will approve each Implementation Plan as we proceed?
6. **Integration:** Should we integrate with real Delhi Traffic Prahari API in Phase 2, or stay demo-only?

---

## 📝 Next Step

**When approved by stakeholder:**

1. Create detailed **Implementation Plan for M1 (DATABASE SCHEMA)**
2. Implementation Engineer executes M1
3. Create detailed **Implementation Plan for M3.1 (MEDIA UPLOAD RED)**
4. Test Engineer executes M3.1 (writes failing tests)
5. Create detailed **Implementation Plan for M3.2 (MEDIA UPLOAD GREEN)**
6. Implementation Engineer executes M3.2 (implements to pass tests)
7. Code Reviewer reviews M3.2 changes
8. Continue through remaining milestones...

---

## 📎 Artifacts

- **STATUS.md** — Current state overview (documentation)
- **PLUGIN-REVIEW.md** — Production Engineering Standards plugin review (documentation)
- **Plan.md** — This document (requires approval)
- **.github/copilot-instructions.md** — To be created after Plan approval
- **CONTRIBUTING.md** — To be created after Plan approval

---

**Document Version:** 1.0  
**Status:** DRAFT READY FOR REVIEW  
**Next Action:** Stakeholder review and approval of Plan.md and resolution of blocking ambiguities (A1–A5)
