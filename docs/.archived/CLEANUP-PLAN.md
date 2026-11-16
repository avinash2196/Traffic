# CLEANUP MILESTONE - Implementation Plan
**Branch:** cleanup  
**Status:** PENDING APPROVAL  
**Author:** Copilot CLI  
**Date:** 2026-11-16

---

## 📋 Milestone Objective

Remove unnecessary files and reorganize documentation to follow PDD structure, reducing noise and improving project clarity.

---

## 🎯 Scope (What Will Change)

### FILES TO REMOVE (13 items)

**Legacy/Duplicate Batch Scripts (Already removed from main, keeping for audit):**
- ✗ No action - already removed

**Legacy Backend Folders (Assess for removal):**
- [ ] `backend/` - Check if duplicate of citizen+officer+auth
- [ ] `frontend/` - Check if duplicate of citizen-app+officer-app  
- [ ] `gateway/` - Check if unused
- [ ] `api-gateway/` - Check if duplicate of ai-gateway

**Legacy Documentation (Move to docs/):**
- [ ] Root level markdown files (50+) → Organize into `docs/`
- [ ] Session summaries → Archive to `docs/.archived/`
- [ ] Execution logs → Archive to `docs/.archived/`

**Other Unnecessary Files:**
- [ ] `check_*.py` - Debug scripts
- [ ] `test*.json` - Test output artifacts
- [ ] `report*.json` - Report artifacts
- [ ] `*.bak` - Backup files
- [ ] `r.json` - Stray config
- [ ] `gw_test.json` - Gateway test output
- [ ] `controls_*.py` - Legacy runtime controls (if not in use)
- [ ] `agw_*.py` - Legacy gateway files (if not in use)

---

## 📂 Documentation Reorganization

### Current Structure (Messy)
```
Traffic/
├── README.md
├── QUICK-START.md
├── STARTUP_GUIDE.md
├── ARCHITECTURE-*.md (5 files)
├── PHASE-*.md (5 files)
├── MVP_*.md (3 files)
├── STATUS-*.md (5 files)
├── TESTING-*.md (5 files)
├── SESSION_SUMMARY*.md (3 files)
├── [50+ more markdown files in root]
└── docs/
    └── [some docs already here]
```

### Target Structure (Clean)
```
Traffic/
├── README.md ..................... Main project overview
├── QUICK-START.md ................ 5-minute setup
├── CONTRIBUTING.md ............... Contribution guidelines
├── docs/
│   ├── ARCHITECTURE.md ........... Architecture decisions
│   ├── API-SPECIFICATION.md ...... API contracts
│   ├── TESTING.md ................ Testing guide
│   ├── DEPLOYMENT.md ............ Deployment guide
│   ├── TROUBLESHOOTING.md ....... Troubleshooting
│   ├── .archived/
│   │   ├── SESSION_SUMMARY_*.md .. Session notes
│   │   ├── PHASE_1_*.md .......... Phase 1 planning
│   │   ├── MVP_*.md ............ MVP status updates
│   │   └── STATUS_*.md .......... Old status files
│   └── .ai/
│       └── [existing AI planning docs]
└── [Only essential root files]
```

---

## 🗂️ Folder Assessment (Duplicate Detection)

### Decision Required - Review These

#### 1. `backend/` Folder
**Current Size:** Unknown  
**Purpose:** Needs clarification  
**Question:** Is this duplicate of auth/ + citizen/ + officer/?

**Action Options:**
- [ ] DELETE if confirmed duplicate
- [ ] KEEP if serves different purpose (document why)
- [ ] MOVE to docs/.archived/ if legacy reference

#### 2. `frontend/` Folder
**Current Size:** Unknown  
**Purpose:** Needs clarification  
**Question:** Is this duplicate of citizen-app/ + officer-app/?

**Action Options:**
- [ ] DELETE if confirmed duplicate
- [ ] KEEP if serves different purpose (document why)
- [ ] MOVE to docs/.archived/ if legacy reference

#### 3. `gateway/` Folder
**Current Size:** Unknown  
**Purpose:** Needs clarification  
**Question:** Is this active or legacy?

**Action Options:**
- [ ] DELETE if unused
- [ ] KEEP if it's the main API gateway
- [ ] MOVE to docs/.archived/ if reference implementation

#### 4. `api-gateway/` Folder
**Current Size:** Unknown  
**Purpose:** Needs clarification  
**Question:** Is this duplicate of ai-gateway/?

**Action Options:**
- [ ] DELETE if confirmed duplicate
- [ ] KEEP if different from ai-gateway/
- [ ] MOVE to docs/.archived/ if legacy

---

## 📝 Root-Level Files to Remove

**Category: Debug/Test Artifacts**
```
check_ai.py
check_env.py
check_env_in_app.py
check_env_now.py
check_failure.py
check_job_settings.py
check_jobs.py
check_login_page.py
check_media.py
check_report.py

test*.json (all test output files)
report*.json (all report output files)
r.json
gw_test.json

*.bak (backup files)
test.json
test-auth-fix.py
test-services-simple.py
test-services.py
test-gateway.py
test-gateway-response.py
test-token-validation.py
test_ai_e2e.py
test_ai_integration.py
test_auth_fixed.py
test_e2e.py
test_end_to_end.py
test_env_loading.py
test_new_report.py
test_openai.py
```

**Category: Legacy Control Scripts**
```
controls_http.py
controls_operator.py
runtime_controls.py

agw_media.py
agw_protocol.py
agw_transport.py
ai_gateway_mock.py
ai_gateway_service.py

manual_test.py
generate_token.py
media.py
```

**Category: Logs**
```
ai-gateway-debug.log
server.log
logs-*.txt
pytest_output.txt
```

---

## 🚀 Implementation Steps

### Step 1: Identify Duplicates (Need Approval)
Before deleting, verify:
- [ ] Check contents of `backend/` folder
- [ ] Check contents of `frontend/` folder
- [ ] Check contents of `gateway/` folder
- [ ] Check contents of `api-gateway/` folder
- [ ] Confirm which are truly duplicates vs. different purpose

### Step 2: Remove Test/Debug Artifacts
Once approved, delete:
- [ ] All `check_*.py` files
- [ ] All `test*.json` files
- [ ] All `report*.json` files
- [ ] All `.bak` files
- [ ] Stray config files (`r.json`, `gw_test.json`)

### Step 3: Remove Legacy Scripts (If Not in Use)
Once approved, delete:
- [ ] `controls_*.py` (if not referenced)
- [ ] `agw_*.py` (if not referenced)
- [ ] `manual_test.py`
- [ ] `media.py` (if duplicate of shared/media.py)

### Step 4: Reorganize Documentation
Once approved, move:
- [ ] Session summaries → `docs/.archived/`
- [ ] Phase planning → `docs/.archived/`
- [ ] MVP status → `docs/.archived/`
- [ ] Old status files → `docs/.archived/`
- [ ] Architecture decisions → `docs/ARCHITECTURE.md`
- [ ] Testing guides → `docs/TESTING.md`
- [ ] Deployment guides → `docs/DEPLOYMENT.md`

### Step 5: Create New Root Documentation
- [ ] `CONTRIBUTING.md` - Contribution guidelines
- [ ] Update `README.md` with cleaner structure
- [ ] Update `QUICK-START.md` if needed

### Step 6: Delete Duplicate Folders (If Confirmed)
- [ ] Delete `backend/` (if duplicate)
- [ ] Delete `frontend/` (if duplicate)
- [ ] Delete `gateway/` (if unused)
- [ ] Delete `api-gateway/` (if duplicate of ai-gateway)

---

## 📊 Expected Outcome

### Before Cleanup
- **Files:** 450
- **Root markdown files:** 50+
- **Duplicate folders:** 4 (possibly)
- **Clutter:** High

### After Cleanup (Estimated)
- **Files:** ~350
- **Root markdown files:** 3-4 essential ones
- **Duplicate folders:** Removed or consolidated
- **Clutter:** Low
- **Clarity:** High

---

## ⚠️ Open Questions (NEED APPROVAL)

**Q1: What is `backend/` folder used for?**
- Is it active code or legacy?
- Is it imported/used by any service?
- Should it be deleted or archived?

**Q2: What is `frontend/` folder used for?**
- Is it React/Vue/Angular or Python?
- How does it differ from citizen-app + officer-app?
- Should it be deleted or archived?

**Q3: What is `gateway/` folder used for?**
- Is it an HTTP API gateway?
- Is it actively used in deployment?
- Should it be deleted or archived?

**Q4: What is `api-gateway/` folder used for?**
- How does it differ from ai-gateway/?
- Is it actively used?
- Should it be deleted or archived?

**Q5: Should old test/debug scripts be kept for reference?**
- Delete all `check_*.py`, `test*.py` root files?
- Keep any for historical reference?

---

## 🔄 Git Workflow (PDD)

### Current Status
- ✅ Branch created: `cleanup`
- ⏳ Plan created: This document
- ⏹️ Awaiting approval: **NEED YOUR DECISION**

### Next Steps (After Approval)
1. Answer the 5 open questions above
2. Create detailed deletion list
3. Create IMPLEMENTATION PHASE 1 markdown
4. Execute deletions/reorganization
5. Verify no broken imports
6. Commit changes
7. Create PR for review

---

## 🎓 PDD Structure Followed

✅ Milestone objective clearly stated  
✅ Scope defined (what will change)  
✅ Implementation steps numbered  
✅ Expected outcomes documented  
✅ Open questions identified (need approval)  
✅ Git workflow tracked  
✅ No code changes yet (plan only)  

---

## 📌 Approval Checklist

Before proceeding, confirm:

- [ ] Do you approve removing all debug/test artifacts?
- [ ] Do you approve reorganizing documentation to `docs/`?
- [ ] Do you approve deleting `backend/` if confirmed duplicate?
- [ ] Do you approve deleting `frontend/` if confirmed duplicate?
- [ ] Do you approve deleting `gateway/` if unused?
- [ ] Do you approve deleting `api-gateway/` if confirmed duplicate?

---

**Status:** 🔴 PENDING APPROVAL  
**Next Action:** Answer the 5 open questions + approval checklist  
**Reviewer:** You (project owner)
