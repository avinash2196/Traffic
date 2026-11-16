# RoadWatch Documentation Index

Complete navigation guide for all project documentation, code, and deployment resources.

---

## 🎯 Getting Started (Start Here!)

### For First-Time Users (5–15 minutes)
1. **README.md** — Overview of what RoadWatch is and does
2. **QUICK_REFERENCE.md** — Copy-paste commands to get running in 5 minutes
3. **LOCAL_DEPLOYMENT.md** → Section "Quick Start" — Three startup options

### For Project Managers/Stakeholders (30 minutes)
1. **COMPLETION.md** — Comprehensive status of all 9 milestones
2. **Plan.md** — Architecture decisions and design trade-offs
3. **STATUS.md** — Current state and progress

### For Developers (1–2 hours)
1. **Plan.md** → "Architecture" section — System overview
2. **QUICK_REFERENCE.md** → API Endpoints table — All 7 endpoints
3. **LOCAL_DEPLOYMENT.md** → Full guide — Database, testing, troubleshooting
4. **app.py** source code — Implementation details

### For DevOps/Cloud Engineers (1 hour)
1. **GCP_DEPLOYMENT.md** — Complete production deployment guide
2. **LOCAL_DEPLOYMENT.md** → Docker section — Container build
3. **.env.example** — Environment variable reference
4. **Dockerfile** source code — Build configuration

---

## 📋 Documentation Files

### Quick Reference
| File | Purpose | Read Time | Audience |
|------|---------|-----------|----------|
| **QUICK_REFERENCE.md** | One-page cheat sheet | 5 min | Everyone |
| **README.md** | Project overview | 10 min | Public |
| **INDEX.md** | Documentation guide (this file) | 5 min | Everyone |

### Deployment & Setup
| File | Purpose | Read Time | Audience |
|------|---------|-----------|----------|
| **LOCAL_DEPLOYMENT.md** | Run locally (Windows/macOS/Linux) | 15 min | Developers |
| **GCP_DEPLOYMENT.md** | Deploy to Google Cloud | 20 min | DevOps/Cloud Eng |
| **.env.example** | Environment variable template | 5 min | Everyone |

### Project Status & Planning
| File | Purpose | Read Time | Audience |
|------|---------|-----------|----------|
| **COMPLETION.md** | MVP status: all 9 milestones | 20 min | Project Manager |
| **Plan.md** | Architecture, decisions, ambiguities | 25 min | Tech Lead |
| **STATUS.md** | Real-time progress tracker | 5 min | Everyone |

### Code & Architecture
| File | Purpose | Read Time | Audience |
|------|---------|-----------|----------|
| **app.py** | FastAPI server (650+ lines) | 30 min | Backend Dev |
| **bootstrap.py** | Database schema (200+ lines) | 10 min | Backend Dev |
| **media.py** | Media validation (150+ lines) | 10 min | Backend Dev |

### Testing & Verification
| File | Purpose | Read Time | Audience |
|------|---------|-----------|----------|
| **verify_integration.py** | Standalone integration check | 2 min | DevOps/QA |
| **tests/test_api.py** | Unit & integration tests (600+ lines) | 20 min | QA Engineer |

### Configuration
| File | Purpose | Read Time | Audience |
|------|---------|-----------|----------|
| **requirements.txt** | Python dependencies (15) | 2 min | Developer |
| **Dockerfile** | Docker build configuration | 5 min | DevOps |
| **.dockerignore** | Docker build exclusions | 2 min | DevOps |

### Startup Scripts
| File | Purpose | OS | Audience |
|------|---------|-----|----------|
| **start-windows.ps1** | Windows startup script | Windows | Windows Dev |
| **start.sh** | macOS/Linux startup script | macOS/Linux | Mac/Linux Dev |

### Web Interface
| Directory | Purpose | Files | Audience |
|-----------|---------|-------|----------|
| **templates/** | HTML pages (8) | See table below | Frontend Dev |
| **static/css/** | Stylesheets (4) | See table below | Frontend Dev |
| **static/js/** | JavaScript utilities (4) | See table below | Frontend Dev |

---

## 🌐 Web Interface

### HTML Pages (templates/)

| Page | Path | Role | Purpose |
|------|------|------|---------|
| **Citizen Login** | citizen-login.html | Citizen | Authentication |
| **Citizen Dashboard** | citizen-dashboard.html | Citizen | List own reports |
| **New Report** | citizen-report.html | Citizen | Create violation report |
| **Report List** | citizen-reports.html | Citizen | Search & filter reports |
| **Report Detail** | citizen-report-detail.html | Citizen | View timeline & status |
| **Officer Login** | officer-login.html | Officer | Authentication |
| **Review Queue** | officer-queue.html | Officer | Cases awaiting decision |
| **Case Detail** | officer-detail.html | Officer | Review evidence & decide |

### Stylesheets (static/css/)

| Stylesheet | Purpose | Lines | KB |
|-----------|---------|-------|-----|
| **base.css** | Typography, forms, colors | 150 | 4 |
| **layout.css** | Header, footer, grid, containers | 200 | 6 |
| **components.css** | Buttons, badges, modals, tables | 350 | 10 |
| **responsive.css** | Mobile (375px+), dark mode, print, a11y | 250 | 7 |

### JavaScript (static/js/)

| Script | Purpose | Functions | KB |
|--------|---------|-----------|-----|
| **api.js** | API client wrapper | 6 endpoint functions | 4 |
| **auth.js** | Demo identity management | localStorage, token | 2 |
| **common.js** | UI helpers | Toasts, badges, formatting | 3 |
| **utils.js** | General utilities | Debounce, polling, validation | 2 |

---

## 📊 API Reference

### All Endpoints

```
Citizen Endpoints:
  POST   /api/reports                    Create report
  GET    /api/reports                    List reports
  GET    /api/reports/{id}               Get report detail

Officer Endpoints:
  GET    /api/authority/queue            Review queue
  GET    /api/authority/reports/{id}     Case detail
  POST   /api/authority/reports/{id}/decision  Submit decision
  GET    /api/authority/reports/{id}/evidence.zip  Download ZIP (M6)

Admin/Health:
  GET    /health                         Health check
  GET    /api/docs                       Swagger UI
  GET    /api/redoc                      ReDoc (alternative)
```

**Full documentation:** Swagger UI at `http://127.0.0.1:8000/api/docs`

### Request/Response Formats

See:
- **app.py** lines 1–100 — Pydantic models (request/response shapes)
- **Plan.md** → "API Specification" — Request/response details

---

## 🗄️ Database Schema

### Tables

| Table | Columns | Purpose | Rows |
|-------|---------|---------|------|
| **reports** | id, citizen_id, violation_type, location, status, points, created_at | Violation reports | ~1000 (demo) |
| **media** | id, report_id, filename, sha256_hash, size, upload_time | Attached photos/videos | ~1000 (demo) |
| **events** | id, report_id, event_type, actor, description, timestamp | Audit trail (append-only) | ~3000 (demo) |

### Schema Definitions

See **bootstrap.py** lines 30–150 for full schema with:
- Column types and constraints
- Primary/foreign keys
- Indexes for performance
- SQLite optimizations (WAL mode, pragma settings)

---

## 🔧 Development Workflow

### Setting Up Local Environment

**5-minute path:**
```
1. Run startup script (start.sh or start-windows.ps1)
   └─ Creates venv, installs deps, initializes DB, starts server
```

**Manual path:**
```
1. Clone repo: git clone ...
2. Create venv: python -m venv .venv
3. Activate: source .venv/bin/activate (macOS/Linux) or .venv\Scripts\Activate.ps1 (Windows)
4. Install: pip install -r requirements.txt
5. Database: python bootstrap.py (creates roadwatch.db)
6. Start: uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Docker path:**
```
1. Build: docker build -t roadwatch .
2. Run: docker run -p 8000:8000 roadwatch
```

**Details:** See `LOCAL_DEPLOYMENT.md`

### Testing Locally

**Automated tests:**
```bash
pytest tests/
# Expected: 10/10 PASS
```

**Manual workflow (5 steps):**
1. Citizen Login → Create report
2. Note report ID
3. Officer Login → Review queue
4. Select report → Approve/Reject
5. Download evidence ZIP

**Details:** See `LOCAL_DEPLOYMENT.md` → "Testing Workflow"

### Code Changes & Commit

**Workflow:**
1. Create feature branch: `git checkout -b feature/my-feature`
2. Edit code: `vi app.py`
3. Test locally: `pytest tests/`
4. Commit: `git commit -m "[MILESTONE] Description"` (see Plan.md for milestone format)
5. Push: `git push origin feature/my-feature`
6. Create PR with reference to Implementation Plan

**Details:** See `Plan.md` → "Git Commit Format"

---

## ☁️ Deployment Options

### Option 1: Local (Fastest, Development)
```bash
./start.sh                    # macOS/Linux
.\start-windows.ps1          # Windows
# Access http://127.0.0.1:8000/citizen-login.html
```
**Time:** 2 minutes | **Cost:** Free | **Guide:** LOCAL_DEPLOYMENT.md

### Option 2: Docker (Portable, Testing)
```bash
docker build -t roadwatch .
docker run -p 8000:8000 roadwatch
# Access http://localhost:8000/citizen-login.html
```
**Time:** 3 minutes | **Cost:** Free | **Guide:** LOCAL_DEPLOYMENT.md → Docker

### Option 3: GCP (Production, Scalable)
```bash
gcloud run deploy roadwatch --source . --region us-central1
# Access https://roadwatch-XXXXXX.run.app/citizen-login.html
```
**Time:** 30 minutes | **Cost:** $0–50/month (Pay-as-you-go) | **Guide:** GCP_DEPLOYMENT.md

**Comparison table:** See `GCP_DEPLOYMENT.md` → "Deployment Options"

---

## 🔐 Security & Secrets

### Environment Variables

**Required:**
```bash
ROADWATCH_REVIEWER_TOKEN=your-secure-token
```

**Optional:**
```bash
DATABASE_URL=...
MEDIA_STORE_PATH=...
LOG_LEVEL=INFO
OPENAI_API_KEY=...
```

**Reference:** `.env.example` (comprehensive template)

### Best Practices

1. Never commit `.env` file (add to `.gitignore`)
2. Use `.env.example` for team sharing (no secrets)
3. Use `ROADWATCH_REVIEWER_TOKEN` env var to override default
4. For production: Use Secret Manager (GCP), Secrets (GitHub), or environment variables

**Details:** See `.env.example` comments and `GCP_DEPLOYMENT.md` → "Security Hardening"

---

## 🚨 Troubleshooting

### Common Issues

| Error | Cause | Solution | Guide |
|-------|-------|----------|-------|
| `ModuleNotFoundError: app` | venv not activated | Activate: `.venv\Scripts\Activate.ps1` | LOCAL_DEPLOYMENT.md |
| `Address already in use` | Port 8000 in use | Use different port: `--port 8001` | LOCAL_DEPLOYMENT.md |
| `sqlite3.OperationalError: database is locked` | Database locked | Kill Python: `pkill python` | LOCAL_DEPLOYMENT.md |
| `No module named 'jinja2'` | Missing dependency | Install: `pip install jinja2==3.1.2` | LOCAL_DEPLOYMENT.md |
| `Health check failed` | Container not ready | Wait 10s, check logs: `docker logs <ID>` | LOCAL_DEPLOYMENT.md |
| `Cloud SQL connection timeout` | Database unreachable | Check proxy, firewall, IP allowlist | GCP_DEPLOYMENT.md |

**Full troubleshooting:** See respective deployment guide

---

## 📈 Monitoring & Observability

### Local (Development)
- **Logs:** Console output from uvicorn
- **Health check:** `curl http://127.0.0.1:8000/health`
- **Metrics:** Swagger UI at `/api/docs`

### GCP (Production)
- **Logs:** Cloud Logging dashboard
- **Metrics:** Cloud Monitoring dashboard
- **Traces:** Cloud Trace (if OpenTelemetry enabled)
- **Errors:** Error Reporting dashboard

**Details:** See `GCP_DEPLOYMENT.md` → "Monitoring & Observability"

---

## 📞 FAQ & Support

### How do I...

| Question | Answer | Reference |
|----------|--------|-----------|
| Run locally? | `./start.sh` or `start-windows.ps1` | QUICK_REFERENCE.md |
| Deploy to GCP? | Follow 10-step guide | GCP_DEPLOYMENT.md |
| Change the reviewer token? | Set `ROADWATCH_REVIEWER_TOKEN` env var | .env.example |
| Add an API endpoint? | Edit `app.py`, add route, test with pytest | Plan.md |
| Reset the database? | `rm roadwatch.db && ./start.sh` | LOCAL_DEPLOYMENT.md |
| Download evidence as ZIP? | Officer Portal → View case → Download ZIP button | README.md |
| Enable AI screening? | Set `OPENAI_API_KEY` and `ENABLE_AI_SCREENING=true` | .env.example |
| Monitor in production? | Use Cloud Logging + Cloud Monitoring | GCP_DEPLOYMENT.md |

### Need Help?

1. **Quick lookup:** QUICK_REFERENCE.md (2 min)
2. **Setup issues:** LOCAL_DEPLOYMENT.md → Troubleshooting (5 min)
3. **Production issues:** GCP_DEPLOYMENT.md → Troubleshooting (10 min)
4. **Code questions:** Read app.py comments (15 min)
5. **Architecture:** Review Plan.md (30 min)

---

## 📚 Additional Resources

### Code Quality
- **Style:** Python 3.11+, type hints, docstrings
- **Testing:** pytest (10/10 tests passing)
- **Linting:** (Can be added with black, flake8, mypy)
- **Security:** No SQL injection, CORS configured, headers validated

### Compliance & Standards
- **PDD (Prompt-Driven Development):** See Plan.md → "Development Workflow"
- **Production Engineering Standards:** Plugin used for planning & review
- **Accessibility:** WCAG 2.1 AA (forms labeled, color contrast, keyboard nav)

### Dependencies
- **Framework:** FastAPI 0.162.0
- **Server:** uvicorn 0.54.0
- **Database:** SQLite (PostgreSQL schema documented)
- **ORM:** Direct SQL (no ORM for MVP)
- **Testing:** pytest 9.1.1 + pytest-asyncio 1.4.0
- **Media:** Pillow 13.0.0

**Full list:** requirements.txt

---

## 🎯 Project Status

### Current State
- ✅ All 9 milestones **COMPLETE**
- ✅ 10/10 tests **PASSING**
- ✅ Integration verified
- ✅ Deployment guides complete
- ✅ Documentation comprehensive

### Timeline
- M1–M4.2: Backend (Database, API, Media, Tests) — **DONE**
- M5–M7: Frontend + Deployment — **DONE**
- Phase 2: Real auth, PostgreSQL, AI screening — **PLANNED**

**Details:** See COMPLETION.md or STATUS.md

---

## 🔗 Navigation Quick Links

- **I want to run it locally** → QUICK_REFERENCE.md + LOCAL_DEPLOYMENT.md
- **I want to deploy to GCP** → GCP_DEPLOYMENT.md
- **I want to understand the code** → Plan.md + app.py
- **I want to see what was built** → COMPLETION.md
- **I need environment variables** → .env.example
- **I need API details** → Swagger at http://127.0.0.1:8000/api/docs
- **I want to troubleshoot** → LOCAL_DEPLOYMENT.md or GCP_DEPLOYMENT.md
- **I need a quick cheat sheet** → QUICK_REFERENCE.md

---

## 📝 Document Metadata

| Attribute | Value |
|-----------|-------|
| Project | RoadWatch |
| Status | MVP Complete |
| Version | 1.0 |
| Last Updated | 2026-11-02 |
| Total Documentation | ~80 KB |
| Total Code | ~3,500 LOC |
| Test Coverage | 10/10 PASS |

---

**Start with:** QUICK_REFERENCE.md (5 min)  
**Then read:** LOCAL_DEPLOYMENT.md or GCP_DEPLOYMENT.md (15 min)  
**Deep dive:** Plan.md + app.py (1 hour)

Happy deploying! 🚀
   - **Read if:** You want more detail on integration

### 7. **README-INTEGRATION.md**
   - **What it is:** Comprehensive integration guide with artifact map and workflow details
   - **Time to read:** 15 minutes
   - **Best for:** Understanding the complete integration in detail
   - **Read if:** You want thorough understanding of the system

### 8. **README.md** (Original)
   - **What it is:** User-facing project overview (not changed by this integration)
   - **Time to read:** 5-10 minutes (features overview)
   - **Best for:** Understanding what RoadWatch is and what it does
   - **Key sections:** Features, API spec, demo walkthrough, known limitations

---

## 📋 **Quick Reference Tables**

### By Question Type

**"What's the current project status?"**
→ Read: SUMMARY-CARD.txt (5 min) then STATUS.md (10 min)

**"What's blocking development?"**
→ Read: SUMMARY-CARD.txt → Look at "5 BLOCKING AMBIGUITIES" section

**"How do I unblock development?"**
→ Read: Plan.md → "Approval Checklist" section → "Answer A1–A5 Questions"

**"What can I change in code?"**
→ Read: .github/copilot-instructions.md → "Control Boundaries" section

**"What's the development timeline?"**
→ Read: Plan.md → "Milestone Breakdown" section

**"How does the plugin work?"**
→ Read: PLUGIN-REVIEW.md → "Plugin Overview" section

**"What's been created in this session?"**
→ Read: SUMMARY-CARD.txt → "WHAT WAS ACCOMPLISHED THIS SESSION" section

**"What's the approval workflow?"**
→ Read: Plan.md → "Approval Checklist" section

**"How will development proceed after approval?"**
→ Read: SUMMARY-CARD.txt → "DEVELOPMENT CYCLE (After Approval)" section

---

## 🎯 **By Role**

### **Project Manager / Stakeholder**
   1. SUMMARY-CARD.txt (5 min) — Understand the big picture
   2. Plan.md (20 min) — Understand milestones and timeline
   3. Approve Plan.md and answer A1–A5 (10 min) — Unblock development

### **Developer / Implementation Engineer**
   1. SUMMARY-CARD.txt (5 min) — Understand what's happening
   2. .github/copilot-instructions.md (15 min) — Know the rules
   3. Plan.md (20 min) — Know which milestones you'll execute
   4. Reference PLUGIN-REVIEW.md (10 min) — Understand plugin oversight

### **Technical Lead / Code Reviewer**
   1. Plan.md (20 min) — Understand milestones and approval gates
   2. .github/copilot-instructions.md (15 min) — Know the code review standards
   3. PLUGIN-REVIEW.md (10 min) — Understand plugin enforcement

### **Security / Compliance Reviewer**
   1. Plan.md (20 min) — Section: "Risks & Mitigation"
   2. .github/copilot-instructions.md (15 min) — Section: "Security & Secrets"
   3. INTEGRATION-SUMMARY.md (10 min) — Section: "Control Boundaries"

---

## 📊 **Document Statistics**

| Document | Lines | Size | Read Time | Purpose |
|----------|-------|------|-----------|---------|
| SUMMARY-CARD.txt | 320 | 12 KB | 5 min | Executive summary |
| Plan.md | 335 | 16.8 KB | 20 min | Master plan (CRITICAL) |
| .github/copilot-instructions.md | 400+ | 14.2 KB | 15 min | Development rules |
| PLUGIN-REVIEW.md | 250 | 11.5 KB | 10 min | Plugin review log |
| STATUS.md | 220 | 11.9 KB | 10 min | Current state |
| INTEGRATION-SUMMARY.md | 234 | 13.1 KB | 10 min | Integration summary |
| README-INTEGRATION.md | 324 | 13.7 KB | 15 min | Integration guide |
| README.md | 93 | 8.5 KB | 10 min | Project overview |

**Total Documentation:** 66.5 KB, 1,132 lines  
**Total Read Time (All):** ~95 minutes  
**Total Read Time (Core):** ~50 minutes  
**Total Read Time (Essential):** ~25 minutes

---

## 🚀 **Recommended Reading Path**

### **Path A: Quick Approval** (30 minutes total)
For stakeholders who need to approve Plan.md quickly:

1. SUMMARY-CARD.txt (5 min)
   └─ Get the big picture

2. Plan.md (20 min)
   └─ Understand milestones and blocking questions
   └─ Read "Blocking Ambiguities" section carefully (A1–A5)

3. Answer A1–A5 & Approve (5 min)
   └─ Unblock development

---

### **Path B: Thorough Understanding** (1.5 hours total)
For technical leads and implementers:

1. SUMMARY-CARD.txt (5 min)
   └─ Executive summary

2. Plan.md (20 min)
   └─ Full milestone breakdown

3. .github/copilot-instructions.md (15 min)
   └─ Development rules you'll follow

4. PLUGIN-REVIEW.md (10 min)
   └─ How plugin enforcement works

5. STATUS.md (10 min)
   └─ Current project state

6. INTEGRATION-SUMMARY.md (10 min)
   └─ PDD workflow details

**Total:** ~70 minutes

---

### **Path C: Everything** (2 hours total)
For comprehensive project understanding:

Read all documents in this order:
1. SUMMARY-CARD.txt (5 min)
2. Plan.md (20 min)
3. .github/copilot-instructions.md (15 min)
4. PLUGIN-REVIEW.md (10 min)
5. STATUS.md (10 min)
6. INTEGRATION-SUMMARY.md (10 min)
7. README-INTEGRATION.md (15 min)
8. README.md (10 min)

**Total:** ~95 minutes

---

## 🛑 **Blocking Gate**

**You cannot proceed with development until:**

1. ✅ You have read Plan.md
2. ✅ You have answered A1–A5 (5 ambiguities)
3. ✅ You have approved Plan.md
4. ✅ You have identified who approves Implementation Plans

**Estimated time to unblock:** 25–35 minutes

---

## 📍 **Key Sections to Bookmark**

### In **Plan.md**
- "5 Critical Ambiguities to Resolve (Blocking)" — Read this first
- "Milestone Breakdown" — Detailed scope for each milestone
- "Approval Checklist" — 8 items before coding begins

### In **.github/copilot-instructions.md**
- "Control Boundaries (Copilot Enforcement)" — Rules you must follow
- "Code Review Standards" — What reviewers will check

### In **PLUGIN-REVIEW.md**
- "Review Points (Updated Each Turn)" — Progress tracking
- "Plugin Findings" — Strengths, friction points, recommendations

---

## ✅ **How to Use This Index**

1. **First time?** Start with SUMMARY-CARD.txt
2. **Need to approve?** Read Plan.md + answer A1–A5
3. **Starting development?** Read .github/copilot-instructions.md
4. **Want details?** Use the "By Question Type" section
5. **Need reference?** Use the "By Role" section

---

## 🔄 **This Index Will Be Updated**

After each development turn:
- PLUGIN-REVIEW.md will be updated with new findings
- Plan.md will show progress on each milestone
- Other documents will be updated as needed

The index itself will be updated to reflect any changes in document structure or reading recommendations.

---

**Last Updated:** 2026-11-01  
**Status:** Complete ✅  
**Next:** See SUMMARY-CARD.txt for immediate next steps
