# RoadWatch Traffic Evidence Reporting — Copilot Development Instructions

**Project:** Traffic evidence reporting MVP for India-focused citizen + authority workflow  
**Repository:** avinash-repo/v11/Traffic  
**Plugin:** Production Engineering Standards v0.14.0  

---

## 🎯 Project Context

RoadWatch is a modular monolith (FastAPI) where citizens report traffic violations (photos/videos) and officers review evidence to award provisional points. This repository uses **Prompt-Driven Development (PDD)** with structured planning, milestone separation, and human approval gates.

**Key Project Constraints:**
- Modular monolith: FastAPI + SQLite (MVP) / PostgreSQL (future)
- Local-only: file storage, demo identity, no external integrations in MVP
- Event-driven: immutable append-only audit trail
- Stateful: report lifecycle with citizen/officer interactions
- Deployable: Docker, Windows/Mac/Linux startup scripts

---

## 🚀 Development Workflow (Prompt-Driven Development)

### Approval Gates (Non-Negotiable)

Every code change must be authorized by an approved, milestone-specific **Implementation Plan**. This applies to:
- Production source code
- Test code
- Configuration files and dependencies
- Database schemas and migrations
- Deployment scripts

**Do not:**
- Write code from free-form requests, failing tests, or "obvious improvements" without an approved Implementation Plan
- Create dependencies, modify schemas, or change infrastructure without a written plan
- Bypass human review, even for small changes
- Mix RED (test) and GREEN (implementation) work in one milestone

**Do:**
- Create detailed Implementation Plans for each milestone
- Wait for human approval before coding
- Update Plan.md with verified progress after each milestone
- Include approved plan references in git commits

---

## 📋 Artifact Authority

**These are the source of truth; no other decisions override them:**

1. **Plan.md** — Master breakdown of all milestones, dependencies, and risks
   - Updated only after human approval
   - Never modified mid-milestone
   - Tracks completion status

2. **Implementation Plans** — Detailed scope for one milestone
   - Approved separately for each milestone
   - Authorizes only the specified work
   - Blocks the next milestone until completion

3. **Decision Records** — Architecture and design decisions
   - Approval required for material trade-offs
   - Document trade-offs, not universal truths

4. **Code Changes** — Traceable to approved Implementation Plan
   - Commit message includes: "As per [Plan.md Milestone X, Implementation Plan Y]"
   - Code reviewers verify traceability

---

## 🛑 Control Boundaries (Copilot Enforcement)

### Material Ambiguity → Ask, Don't Assume
**Rule:** If a requirement is unclear, unclear, or contradictory, ask for clarification. Do not:
- Choose between material alternatives on behalf of the user
- Convert ambiguity into a default
- Treat reasonable defaults as authorization
- Silently resolve ambiguity in an Open Questions section

**Apply to RoadWatch:**
- Database choice unclear? Ask before database schema is written
- UI framework unclear? Ask before templates are created
- Media storage approach unclear? Ask before media handler is coded
- Officer SLA requirements unclear? Ask before queue is designed

### No Code Change Without Approval
**Rule:** Do not write production code, tests, config, dependencies, schemas, migrations, or deployment scripts without an approved Implementation Plan.

**Apply to RoadWatch:**
- Do not create `app.py` until DATABASE SCHEMA and FASTAPI APP Implementation Plans are approved
- Do not write test files until RED milestone Implementation Plan is approved
- Do not modify requirements.txt until dependency addition is approved
- Do not write migrations until schema is approved

### Milestone Separation
**Rule:** RED (failing tests), GREEN (implementation), and REFACTOR (restructuring) are separate milestones, reviewed separately. Never merge them.

**Apply to RoadWatch:**
- M3.1 (MEDIA UPLOAD RED) — Only test code, all tests fail, no production media.py code
- M3.2 (MEDIA UPLOAD GREEN) — Only implementation to pass M3.1 tests, separate code review
- M4.1 (API RED) — Only endpoint test code, all tests fail, no handler implementation
- M4.2 (API GREEN) — Only handler implementation to pass M4.1 tests, separate code review

---

## 🔍 Code Review Standards

### For Production Code Changes
**Review checklist:**
- [ ] Change is traceable to approved Implementation Plan
- [ ] Scope matches the plan (no creep)
- [ ] All RED tests pass (if GREEN milestone)
- [ ] Error handling is explicit (no silent failures)
- [ ] Secrets/credentials are never logged
- [ ] Database transactions have clear boundaries
- [ ] Concurrent access is safe (especially important for SQLite)
- [ ] No blocking I/O in async code paths

### For Test Code (RED Milestone)
**Review checklist:**
- [ ] Tests are independent and can run in any order
- [ ] Test names describe the behavior being tested
- [ ] Fixtures properly set up and tear down state
- [ ] All tests fail (RED phase requirement)
- [ ] Test framework works (pytest runs without import errors)
- [ ] Access control is tested (citizen sees only own data, officer sees queue)

### For API Endpoints
**Review checklist:**
- [ ] HTTP status codes are correct (201 on create, 400 on validation error, 401 on auth failure, 403 on permission denial)
- [ ] Request/response shapes match OpenAPI spec
- [ ] Authorization is enforced (not just on UI side)
- [ ] Input validation catches invalid data before database operations
- [ ] Database errors are caught and return appropriate HTTP status

---

## 🛠️ Python Files (`**/*.py`)

### Style & Structure
- Explicit types at public boundaries (function signatures)
- Constructor injection for dependencies (not globals)
- Async functions for I/O-bound work (FastAPI context)
- Immutable request/response models (Pydantic)
- Clear error handling (no `except: pass`)

### Database Interactions
- Use prepared statements (parameterized queries via psycopg)
- Never build SQL strings from user input
- Transactions have clear scope (start, commit, rollback explicit)
- SQLite: WAL mode for better concurrency
- Connection pooling is initialized at app startup

### Testing
- Use pytest + pytest-asyncio for async tests
- Fixtures for database setup/teardown
- Mocking external services (OpenAI, if integrated)
- Test files in `tests/` directory with `test_*.py` naming
- No test files imported as modules; use pytest discovery

---

## 📦 Dependencies (`requirements.txt`)

**Current approved stack:**
- FastAPI 0.162.0
- uvicorn 0.54.0
- psycopg 3.3.6 (PostgreSQL driver; works with SQLite via adapters)
- Pillow 13.0.0 (image validation)
- pytest 9.1.1 + pytest-asyncio 1.4.0 (testing)
- OpenTelemetry 1.45.1 (observability)
- PyJWT 2.15.1 (identity validation)

**Adding dependencies requires:**
- Approved Implementation Plan justifying the addition
- Minimal version constraints (no over-locking)
- Security scanning (no high/critical vulnerabilities)
- Documentation of what the dependency does

---

## 🗄️ Database Files (`**/*migration*`, schema files)

### Schema Rules
- Tables are named snake_case (plural: `reports`, `events`, `media`)
- Columns are snake_case (lowercase, no spaces)
- Primary keys are explicit (not auto-guessed)
- Foreign keys have `ON DELETE` behavior documented
- Timestamps are UTC ISO-8601 strings or UNIX integers (be consistent)
- No nullable columns without a documented reason

### Migration Path
- SQLite for MVP (file-based, zero setup)
- PostgreSQL schema for Phase 2 (documented, not required for MVP)
- Never drop columns (archive them)
- Always test migration on fresh database

### Schema Review
- [ ] All tables match Plan.md data model
- [ ] Event table is append-only (no UPDATE on events)
- [ ] Media table has SHA-256 hash column
- [ ] Reports table tracks status and provisional points
- [ ] Indexes are added for query performance (especially report status, citizen ID)

---

## 📝 Configuration Files & Environment

### Environment Variables
**Supported (for MVP):**
- `ROADWATCH_REVIEWER_TOKEN` — Demo officer token (default: "local-reviewer-only")
- `OPENAI_API_KEY` — Optional; enables AI screening (Phase 2)
- `OPENAI_MODEL` — Model override (default: "gpt-4o-mini")
- `DATABASE_URL` — Optional; for PostgreSQL in future
- `OTEL_EXPORTER_OTLP_PROTO_HTTP_ENDPOINT` — Optional; for telemetry export

**Never commit secrets.**

### Dockerfile
- Multi-stage: dependencies, app, migrations
- Non-root user for runtime
- Health check endpoint
- Media storage volume (if needed for deployment)

---

## 🧪 Testing (`tests/**/*.py`)

### RED Phase (Test Design)
- All tests must fail initially (before production code is written)
- Test framework must work (pytest discovery, fixtures, assertions)
- No production code should be touched

### GREEN Phase (Implementation)
- Production code is written to pass RED tests
- No new tests are added in GREEN (tests come from RED)
- Code review verifies correctness

### Test Structure
```python
# tests/test_reports.py
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    from app import app
    return TestClient(app)

def test_citizen_submit_report(client):
    """Citizen submits a new report with JPG."""
    # Arrange
    report_data = {...}
    
    # Act
    response = client.post("/api/reports", json=report_data)
    
    # Assert
    assert response.status_code == 201
    assert "report_id" in response.json()
```

---

## 🔐 Security & Secrets

### Secret Management
- Never log secrets, tokens, or credentials
- Use `X-Citizen-Id` header for demo identity (explain it's forged in MVP)
- OIDC token validation in bootstrap.py (mock for MVP)
- Reviewer token is shared and configurable (not hardcoded)

### Access Control
- Citizen can only see their own reports
- Officer can see all reports in queue (no per-officer filtering in MVP)
- Media download is access-checked (citizen: own media, officer: any media)
- No SQL injection (use parameterized queries)

---

## 🚀 Deployment & Operations

### Docker Build
- `docker build -t roadwatch .`
- Verify image size (should be < 500 MB)
- Health check: `docker run roadwatch curl http://localhost:8000/health`

### Local Startup (Windows)
```powershell
# start-windows.ps1
$ErrorActionPreference = "Stop"
if (-Not (Test-Path .venv)) {
    python -m venv .venv
}
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### Local Startup (macOS/Linux)
```bash
#!/bin/bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

---

## 📊 Status Tracking

### Plan.md Status Column
Update after each milestone is verified:

```markdown
| Milestone | Status | Implementation Plan | Verified |
|-----------|--------|---------------------|----------|
| M1: DATABASE SCHEMA | ✅ Done | Yes | Yes |
| M2: FASTAPI APP | ⏳ In Progress | Yes | No |
| M3.1: MEDIA UPLOAD RED | ⏹️ Pending | No | No |
| M3.2: MEDIA UPLOAD GREEN | ⏹️ Pending | No | No |
```

### Git Commit Format
```
[MILESTONE] Brief description

Longer description explaining what changed and why.

As per Plan.md M1 (DATABASE SCHEMA), approved by <reviewer>.
Implementation Plan: <link or date>.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

---

## ⚠️ Common Mistakes to Avoid

1. **Writing code before Implementation Plan approval**
   - ❌ "Let me just create app.py, it's obvious"
   - ✅ Wait for Implementation Plan approval

2. **Mixing RED and GREEN milestones**
   - ❌ "I'll write tests and implement in one PR"
   - ✅ RED tests in M3.1, implementation in M3.2 (separate PRs, separate reviews)

3. **Silently resolving ambiguity**
   - ❌ "The plan doesn't specify, so I'll use SQLite"
   - ✅ Ask stakeholder and wait for clarification

4. **Scope creep in Implementation Plan**
   - ❌ "M3.2 includes AI screening too"
   - ✅ Stick to the approved scope; AI is Phase 2

5. **No authorization in code**
   - ❌ "It's obvious we need admin role checking"
   - ✅ Only implement what Implementation Plan specifies; code review catches missing checks

---

## 🔗 Related Documents

- **Plan.md** — Master milestone breakdown (requires approval before coding)
- **STATUS.md** — Current state overview (informational)
- **PLUGIN-REVIEW.md** — Production Engineering Standards plugin review
- **CONTRIBUTING.md** — To be created; contributor guidelines
- **README.md** — Project overview for users
- **.github/workflows/** — CI/CD pipelines (to be created)

---

## 📞 Questions & Escalation

**Material ambiguity encountered?**
1. Check Plan.md Ambiguities section (A1–A5)
2. If not addressed, post in GitHub Issues with "AMBIGUITY:" prefix
3. Do not proceed with coding until clarified

**Approval needed?**
1. Prepare detailed Implementation Plan (see plugin docs)
2. Request review from technical lead / project owner
3. Post GitHub Issue with "REVIEW:" prefix
4. Wait for approval before writing code

**Disagreement with control boundary?**
1. Explain your concern in writing
2. Reference the specific rule in this document
3. Propose exception with justification
4. Get written approval from project owner before proceeding

---

## 🎓 Learning Resources

- **Production Engineering Standards Repository:** `avinash2196-production-engineering-standards`
- **Prompt-Driven Development (PDD):** See `.claude/skills/` in plugin
- **Implementation Planning:** See `.claude/agents/planner.md`
- **Code Review Standards:** See `.claude/agents/code-reviewer.md`

---

**Last Updated:** 2026-11-01  
**Approved By:** [Awaiting approval]  
**Version:** 1.0
