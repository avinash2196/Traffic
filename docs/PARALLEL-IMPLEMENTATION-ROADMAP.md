# Parallel Implementation Roadmap: M5 + M6 + M7

**Execution Strategy:** Parallel  
**Start Date:** 2026-11-01  
**Status:** Ready for implementation  
**Estimated Duration:** 18 hours (vs. 28 hours sequential)

---

## 🚀 Three Parallel Tracks

### Track 1: M5 — UI SCAFFOLDING (10–15 hours)
**Dependency:** M4.2 (✅ complete)  
**Reference:** M5-DOCUMENTATION-INDEX.md, M5-UI-IMPLEMENTATION-CHECKLIST.md  
**Phases:**
1. Setup (1 hour) — Create directories, shared CSS/JS
2. Citizen portal (4–5 hours) — 4 pages, all APIs
3. Officer portal (3–4 hours) — 2 pages, decision form
4. Testing (2–3 hours) — Forms, errors, responsive

**Start immediately:** Follow M5-UI-IMPLEMENTATION-CHECKLIST.md Phase 1

---

### Track 2: M6 — EVIDENCE EXPORT (3 hours)
**Dependency:** M4.2 (✅ complete) — can run in parallel with M5  
**Reference:** IMPLEMENTATION-PLANS-M5-M6-M7.md → M6 section  
**Tasks:**
1. ZIP export function (1.5 hours)
2. UI integration (0.5 hours)
3. Testing (1 hour)

**Can start:** Immediately (no M5 dependency)  
**Integrates with:** M5 Phase 4 (add button to officer-detail.html)

---

### Track 3: M7 — DOCKER & DEPLOYMENT (1 day)
**Dependency:** None — M1–M4.2 complete  
**Reference:** IMPLEMENTATION-PLANS-M5-M6-M7.md → M7 section  
**Tasks:**
1. Dockerfile (multi-stage, 3–4 hours)
2. Startup scripts (Windows/Mac/Linux, 2–3 hours)
3. Verification (1 hour)

**Can start:** Immediately (fully independent)

---

## 📊 Parallelization Benefits

| Approach | Duration | Notes |
|----------|----------|-------|
| Sequential (M5→M6→M7) | ~28 hours | Safe, no conflicts |
| Staggered (M5+M6, then M7) | ~22 hours | M7 independent, run last |
| **Parallel (M5+M6+M7)** | **~18 hours** | **3 parallel streams, fastest** |

**Why Parallel is Safe:**
- ✅ M5 (UI) has no dependencies on M6/M7
- ✅ M6 (ZIP) has no dependencies on M5 (but M5 UI adds button for UX)
- ✅ M7 (Docker) has zero dependencies (M1–M4.2 already done)
- ✅ Can integrate M6 into M5 Phase 4 without blocking

---

## 🎯 Integration Points

### M5 + M6 Integration
**When:** M5 Phase 4 (Testing & Validation)  
**How:** Add "Download Evidence" button to `templates/authority/case/detail.html`  
**Link:** Button calls `GET /api/authority/reports/{id}/evidence.zip` (from M6)  
**Timing:** M6 implementation doesn't block M5 phases 1-3

### M5 + M7 Integration
**When:** After M5 complete  
**How:** Docker image includes all templates/ and static/ files  
**Timing:** M7 can be finalized once M5 complete (no blocking)

### M6 + M7 Integration
**When:** Docker build includes media ZIP endpoint  
**How:** Dockerfile includes all M6 code automatically  
**Timing:** Independent, no blocking

---

## 📋 Implementation Checklist

### Before Starting All Three
- [x] M5-M7 Implementation Plans approved (IMPLEMENTATION-PLANS-M5-M6-M7.md)
- [x] M5 documentation ready (M5-DOCUMENTATION-INDEX.md, etc.)
- [x] M4.2 fully verified (all 10 tests PASS)
- [x] Parallel strategy confirmed (this document)

### Track 1: M5 UI Scaffolding
- [ ] Phase 1: Setup (static/, CSS, JS shared assets)
- [ ] Phase 2: Citizen portal (4 pages)
- [ ] Phase 3: Officer portal (2 pages)
- [ ] Phase 4: Testing (responsive, all APIs, errors)
- [ ] Integration point: Add M6 ZIP button (in Phase 4)

### Track 2: M6 Evidence Export
- [ ] Implement ZIP export function (app.py endpoint)
- [ ] Add to officers-detail.html (M5 Phase 4 integration)
- [ ] Test all scenarios (approved, rejected, missing auth)

### Track 3: M7 Docker & Deployment
- [ ] Create Dockerfile (multi-stage)
- [ ] Create start-windows.ps1 (PowerShell)
- [ ] Create start.sh (Bash)
- [ ] Test build & run

---

## 🔄 Synchronization Points

**No hard blocking dependencies, but:**

1. **After M5 Phase 2–3 complete:**
   - M6 can finish and be tested independently
   - M7 can finish and be tested independently

2. **M5 Phase 4 (Testing):**
   - Integrate M6 ZIP button if M6 complete
   - Integrate M7 verification checks if needed

3. **Final Sync (Before M5 completion):**
   - M5 includes M6 button (if M6 done)
   - M7 ready for M5 artifacts

**Expected Timeline:**
- Start all 3: 2026-11-01 (now)
- M6 complete: ~2026-11-02 (after 3 hours)
- M7 complete: ~2026-11-02 (after 1 day)
- M5 complete: ~2026-11-03 (after 10-15 hours)

---

## ✅ Definition of Done (All Milestones)

### M5 Done When:
- ✅ All 6 pages load without errors
- ✅ All 6 APIs integrated
- ✅ Responsive design verified (375px, 1024px, 1280px)
- ✅ Error handling works (all status codes)
- ✅ Status polling works (30-second updates)
- ✅ Clarification loop works
- ✅ ZIP download button integrated (if M6 done)
- ✅ All 10 endpoint tests still PASS
- ✅ No console errors

### M6 Done When:
- ✅ POST /api/authority/reports/{id}/evidence.zip endpoint works
- ✅ ZIP downloads successfully
- ✅ ZIP contains all required files (media + manifest + timeline + README)
- ✅ Access control verified (401/403/404/409)
- ✅ UI button added to officer-detail.html
- ✅ All test scenarios passing

### M7 Done When:
- ✅ `docker build -t roadwatch .` succeeds
- ✅ `docker run -p 8000:8000 roadwatch` runs
- ✅ start-windows.ps1 works (creates venv, installs, runs)
- ✅ start.sh works (macOS/Linux)
- ✅ Health check returns 200 OK
- ✅ API endpoints respond

---

## 📞 Communication Protocol

**If a track gets blocked:**
1. Document blocking issue
2. Note which other tracks are affected
3. Escalate to team lead
4. Continue on unblocked tracks

**If an integration point conflicts:**
1. M5 is priority (primary user-facing)
2. M6 integrates into M5 (add button after M6 done)
3. M7 independent (verify after M5+M6 done)

---

## 🎯 Success Criteria

**Parallel implementation successful when:**
- ✅ M5: All 6 UI pages working, all APIs integrated, responsive
- ✅ M6: ZIP export working, button in UI, all tests passing
- ✅ M7: Docker image builds, app runs, scripts work
- ✅ All 10 endpoint tests still PASS
- ✅ Zero integration conflicts
- ✅ Estimated 18-hour duration maintained

---

**Execution Status:** 🟢 **READY TO LAUNCH**  
**Date:** 2026-11-01  
**Strategy:** Parallel (3 simultaneous tracks)  
**Estimated Completion:** 2026-11-03 (~18 hours)

