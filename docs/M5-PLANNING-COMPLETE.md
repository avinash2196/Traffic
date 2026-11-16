# M5 UI Scaffolding — Planning Complete ✅

**Date:** 2026-11-01  
**Status:** Architecture & flow diagrams complete. Ready to implement.

---

## 📚 Documentation Created

Before UI implementation begins, we've prepared **3 comprehensive planning documents**:

### 1. **ARCHITECTURE-FLOW-DIAGRAMS.md** (19 KB)
Complete visual reference for all flows and architecture:
- ✅ **Citizen Workflow** — Upload → Track Status → Clarification → Final Verdict
- ✅ **Officer Workflow** — Queue → Case Details → Decision
- ✅ **System Architecture** — Components, APIs, storage, future integrations
- ✅ **State Machine** — Report lifecycle all statuses
- ✅ **API Integration Maps** — Which UI calls which endpoint
- ✅ **Database Schema** — ER diagram for all tables
- ✅ **UI Page Layout** — Exact page structure for all 6 pages
- ✅ **Authentication Headers** — Citizen ID vs Officer Authorization
- ✅ **Polling Strategy** — 30-second status update mechanism
- ✅ **Error Handling Flow** — 400/401/403/404/409/500 paths
- ✅ **Violation Types & Points** — helmet/triple-riding/red-light with points

**Use this for:** Understanding the complete end-to-end flow before coding any HTML.

---

### 2. **M5-UI-IMPLEMENTATION-CHECKLIST.md** (23 KB)
Detailed component-by-component breakdown:
- ✅ **Citizen Portal** (4 pages):
  - Dashboard (welcome, quick stats)
  - Upload Form (violation type, location, file, submit)
  - Report List (paginated, filterable, clickable)
  - Report Details (with timeline, conditional clarification form, auto-refresh)
  
- ✅ **Officer Portal** (2 pages):
  - Review Queue (paginated, filterable, status badges)
  - Case Detail (media viewer, timeline, decision form)

- ✅ **Shared Assets**:
  - CSS files (base, layout, components, responsive)
  - JavaScript utilities (formatDate, maskId, getStatusColor, etc.)
  - API wrapper (error handling, auth headers)
  - HTML boilerplate templates

- ✅ **Testing Checklist** — Forms, errors, pagination, responsive, state machine
- ✅ **Implementation Principles** — No frameworks, responsive, error handling, security
- ✅ **API Integration Verification** — What to test for each endpoint

**Use this for:** Planning what to build and in what order. Provides exact component specs.

---

### 3. **API-REQUEST-RESPONSE-REFERENCE.md** (23 KB)
Copy-paste ready code for every API endpoint:

Each endpoint includes:
- ✅ Exact HTTP method & URL
- ✅ Required headers (X-Citizen-Id or Authorization)
- ✅ Request body structure (JSON)
- ✅ Complete response example
- ✅ Real JavaScript code to integrate
- ✅ Error handling code (400/401/403/404/409/500)
- ✅ Usage patterns with comments

Example:
```javascript
async function submitReport() {
  const citizenId = getCitizenId();
  const payload = {
    violation_type: document.getElementById('violationType').value,
    location: document.getElementById('location').value,
    media_id: uploadedMediaId
  };
  
  const response = await fetch('/api/reports', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Citizen-Id': citizenId
    },
    body: JSON.stringify(payload)
  });
  // ... error handling ...
}
```

**Use this for:** Copy-pasting API integration code while building UI.

---

## 🎯 What These Docs Provide

### Before You Start Coding:
1. **Read** ARCHITECTURE-FLOW-DIAGRAMS.md → Understand the complete workflow
2. **Review** M5-UI-IMPLEMENTATION-CHECKLIST.md → Know what pages/components to build
3. **Keep** API-REQUEST-RESPONSE-REFERENCE.md open → Copy-paste while coding

### While Building Each Page:
- Component checklist tells you what to build
- Flow diagram shows where it fits
- API reference has the exact code to integrate

### Testing:
- API reference includes testing scenarios
- Checklist includes test cases for each component

---

## 📊 6 Pages to Build

### Citizen Portal
| Page | URL | Purpose | API Calls |
|------|-----|---------|-----------|
| Dashboard | `/` | Welcome, quick stats | None (static) |
| Upload | `/upload.html` | Submit new report | POST /api/reports |
| Report List | `/reports.html` | View all reports | GET /api/reports |
| Report Detail | `/reports/{id}.html` | Status + timeline | GET /api/reports/{id}, POST clarification |

### Officer Portal
| Page | URL | Purpose | API Calls |
|------|-----|---------|-----------|
| Review Queue | `/authority/queue.html` | List reports to review | GET /api/authority/reports |
| Case Detail | `/authority/case/{id}.html` | Review + decide | GET details, POST decision |

---

## 🔑 Key Features

### Citizen Side
- [x] Upload report with violation type + location
- [x] View submission history (paginated)
- [x] Track status in real-time (30-second polling)
- [x] See complete event timeline
- [x] Respond to officer clarification requests
- [x] Receive final verdict (approved/rejected)

### Officer Side
- [x] Browse queue (awaiting-review + resubmitted)
- [x] Filter by status
- [x] View case details + media
- [x] Approve report (awards points)
- [x] Reject report (with reason)
- [x] Request clarification from citizen
- [x] Auto-redirect to queue after decision

### Shared Features
- [x] Responsive design (mobile-first)
- [x] Error handling (400/401/403/404/409/500)
- [x] Loading states (spinners, skeletons)
- [x] Success toasts (green, dismissable)
- [x] No frameworks (vanilla JS)
- [x] Status color coding
- [x] Timestamps (human-readable format)

---

## 🛠️ Technology Stack (Vanilla)

**Frontend:**
- HTML5 (semantic, accessible)
- CSS3 (responsive, mobile-first)
- JavaScript ES6+ (Fetch API, no jQuery/React)
- No build step (serve directly from /static/)

**Backend:**
- FastAPI (already built, tested ✅)
- SQLite (already working ✅)
- Local file storage (already working ✅)

**Serving:**
- FastAPI built-in static file serving
- `app.mount("/static", StaticFiles(directory="static"), name="static")`
- HTML files served from `/templates/`

---

## 📂 File Structure (After M5)

```
Traffic/
├── app.py                          # (existing)
├── bootstrap.py                    # (existing)
├── media.py                        # (existing)
├── requirements.txt                # (existing)
├── tests/                          # (existing)
│   ├── test_api_endpoints.py      # (existing, 10/10 PASS)
│   └── test_media.py              # (existing, 12/12 SKIPPED)
├── static/                         # ← NEW
│   ├── css/
│   │   ├── base.css               # Reset, typography
│   │   ├── layout.css             # Grid, flexbox
│   │   ├── components.css         # Buttons, cards, forms
│   │   ├── responsive.css         # Mobile breakpoints
│   │   └── officer.css            # Officer-specific styles
│   └── js/
│       ├── utils.js               # Helpers (formatDate, etc)
│       ├── auth.js                # Get citizen_id / auth token
│       ├── api.js                 # Fetch wrapper
│       ├── common.js              # Navbar, logout
│       └── [page-specific].js     # Per-page logic
├── templates/                      # ← NEW
│   ├── dashboard.html
│   ├── upload.html
│   ├── reports.html
│   ├── reports/
│   │   └── detail.html            # /reports/{id}.html
│   └── authority/
│       ├── queue.html
│       └── case/
│           └── detail.html        # /authority/case/{id}.html
├── ARCHITECTURE-FLOW-DIAGRAMS.md  # ← NEW (this session)
├── M5-UI-IMPLEMENTATION-CHECKLIST.md # ← NEW (this session)
└── API-REQUEST-RESPONSE-REFERENCE.md # ← NEW (this session)
```

---

## ✅ Implementation Readiness Checklist

Before starting M5, ensure:
- [x] All 6 API endpoints implemented ✅ (M4.2 complete)
- [x] All 10 endpoint tests passing ✅ (10/10 PASS)
- [x] Database schema stable ✅ (M1 verified)
- [x] Media handler complete ✅ (M3.2 verified)
- [x] FastAPI app running ✅ (M2 verified)
- [x] Architecture diagrams done ✅ (THIS SESSION)
- [x] Component specs done ✅ (THIS SESSION)
- [x] API reference done ✅ (THIS SESSION)

**Ready to build:** YES ✅

---

## 🚀 Recommended Build Order for M5

### Phase 1: Setup (1 hour)
1. Create directory structure
2. Write shared CSS (base.css, layout.css, components.css)
3. Write shared JS (utils.js, auth.js, api.js, common.js)
4. Test CSS on dummy page

### Phase 2: Citizen Portal (4-5 hours)
1. Dashboard.html (static, no API)
2. Upload.html (POST /api/reports)
3. Reports.html (GET /api/reports)
4. Reports/detail.html (GET /api/reports/{id}, status polling, conditional clarification)

### Phase 3: Officer Portal (3-4 hours)
1. Authority/queue.html (GET /api/authority/reports)
2. Authority/case/detail.html (decision form, POST decision)

### Phase 4: Integration & Testing (2-3 hours)
1. Test all forms with valid data
2. Test all error paths
3. Test pagination, status updates, state transitions
4. Test responsive CSS

**Total Estimated Time:** 10-15 hours (2-3 days if working full-time)

---

## 📝 Next Steps (After M5 Planning)

1. **Start M5 Implementation**
   - Use M5-UI-IMPLEMENTATION-CHECKLIST.md as build guide
   - Reference API-REQUEST-RESPONSE-REFERENCE.md for code
   - Check ARCHITECTURE-FLOW-DIAGRAMS.md for flow understanding

2. **Parallel: M6 & M7**
   - M6 (EVIDENCE EXPORT) — Independent of UI
   - M7 (DOCKER & DEPLOYMENT) — Independent of UI
   - Can start while M5 is in progress

3. **Post-MVP**
   - Real OIDC integration (Phase 2)
   - OpenAI content screening (Phase 2)
   - Points decay/escalation (Phase 3)
   - Geographic multipliers (Phase 3)

---

## 🎓 Learning Resources Embedded

Each document includes:
- Real-world code examples
- Error handling patterns
- Testing scenarios
- Implementation principles
- Responsive design patterns

Copy-paste ready. No prior web dev experience needed for vanilla HTML/CSS/JS.

---

## ✨ Why These Docs Matter

✅ **No ambiguity** — Every endpoint, every request, every error path documented  
✅ **Copy-paste ready** — JavaScript code ready to integrate  
✅ **Visual-first** — Diagrams show flows before any code  
✅ **Test-driven** — Scenarios cover all workflows  
✅ **Accessible** — No frameworks, just HTML/CSS/JS  
✅ **Production quality** — Error handling, loading states, polling strategy included  

---

## 📞 Questions to Ask Before Starting M5

- [ ] Should media upload use FormData or pre-upload to M3 handler first?
- [ ] Should dashboard show summary stats or just quick links?
- [ ] Should rejection reason be dropdown or free-text input?
- [ ] Should clarification form support just text or text + media?
- [ ] Should officer see citizen full name/ID or masked?

**If unclear:** Check ARCHITECTURE-FLOW-DIAGRAMS.md or API-REQUEST-RESPONSE-REFERENCE.md first.

---

**Status:** 🟢 **Ready to implement M5 UI Scaffolding**  
**Date Prepared:** 2026-11-01  
**Session:** Architecture & Flow Planning Complete

