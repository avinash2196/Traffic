# RoadWatch Traffic — Execution Handoff

**Date:** 2026-11-01  
**Plan Status:** ✅ APPROVED  
**Ready for:** Implementation Phase  

---

## 📋 What You Have

### Planning Documents (Ready-to-Use)
1. **Plan.md** — Master milestone breakdown (APPROVED)
   - 7 sequential milestones (M1 → M7)
   - 5 critical ambiguities resolved (database: SQLite, UI: vanilla HTML, storage: local disk, SLA: simple FIFO, violations: helmet priority)
   - 9–13 working day estimate

2. **STATUS.md** — Current state overview
   - What exists (architecture, code skeleton, testing framework)
   - What's missing (FastAPI app, database schema, API endpoints, UI)
   - Next actions prioritized

### Implementation Plans (Detailed & Executable)
3. **IMPL-M1-DATABASE-SCHEMA.md** — M1 Implementation Plan
   - 4 SQLite tables defined with exact SQL
   - `DatabaseConnection` class code ready to implement
   - Test fixtures (conftest.py) provided
   - Definition of Done checklist
   - Verification steps

4. **IMPL-M3.1-MEDIA-UPLOAD-RED.md** — M3.1 Implementation Plan
   - 12 test cases with GIVEN-WHEN-THEN format
   - All tests SKIPPED (no implementation yet)
   - Mock helpers for file generation
   - Definition of Done checklist
   - Verification steps

---

## 🚀 How to Execute

### Phase 1: M1 (DATABASE SCHEMA)
**Owner:** Implementation Engineer  
**Duration:** 1–2 days  
**Deliverable:** Working SQLite schema + connection pool

```bash
# Steps
1. Read IMPL-M1-DATABASE-SCHEMA.md completely
2. Implement DatabaseConnection class in bootstrap.py
3. Create conftest.py with sample_report and sample_media fixtures
4. Run verification steps to confirm schema integrity
5. Commit with provided commit message
6. Request code review (focus: schema correctness, fixture quality)
```

**Blockers:** None (M1 is first)

**Exit Criteria:**
- ✅ `roadwatch.db` file creates without errors
- ✅ All 4 tables exist with correct indexes
- ✅ Foreign keys + WAL mode enabled
- ✅ Test fixtures work (can insert/query data)
- ✅ Code review passes

---

### Phase 2: M2 (FASTAPI APP & IDENTITY MIDDLEWARE)
**Owner:** Implementation Engineer  
**Duration:** 1–2 days  
**Dependency:** M1 complete  
**Deliverable:** `app.py`, health check, Swagger UI

**Note:** IMPL-M2 plan will be created after M1 is done. It will include:
- FastAPI lifespan context manager
- Database initialization on startup
- Identity middleware (OIDC/demo token validation)
- Health check endpoint
- OpenTelemetry hooks

---

### Phase 3: M3.1 (MEDIA UPLOAD RED)
**Owner:** Test Engineer  
**Duration:** 1 day  
**Dependency:** M1 complete (M2 not yet needed)  
**Deliverable:** 12 failing tests in `tests/test_media.py`

```bash
# Steps
1. Read IMPL-M3.1-MEDIA-UPLOAD-RED.md completely
2. Create tests/test_media.py with 12 test cases
3. All tests use pytest.skip() or assertion placeholders
4. Verify test discovery: pytest tests/test_media.py -v
5. Commit with provided commit message
6. Request code review (focus: test quality, naming, GIVEN-WHEN-THEN format)
```

**Blockers:** None (tests don't require M2 FastAPI app)

**Exit Criteria:**
- ✅ 12 tests exist in test_media.py
- ✅ All tests SKIPPED or placeholders
- ✅ pytest discovers all tests without errors
- ✅ Test names follow pattern `test_<behavior>_<expected_outcome>`
- ✅ Code review passes

---

### Phase 4: M3.2 (MEDIA UPLOAD GREEN)
**Owner:** Implementation Engineer  
**Duration:** 2 days  
**Dependency:** M1 + M2 complete (app.py with identity middleware)  
**Deliverable:** Media handlers to pass all M3.1 tests

**Note:** IMPL-M3.2 plan will reference M3.1 tests and provide:
- `POST /api/reports/{id}/media` endpoint
- File validation (MIME type, size, duration)
- SHA-256 hashing + duplicate detection
- Technical screening (Pillow blur/resolution)
- Local file storage in `./media_store/`

---

## 📊 Dependency Graph

```
M1: DATABASE SCHEMA (1–2 days)
        ↓ (Dependency)
M2: FASTAPI APP (1–2 days)
        ↓ (Dependency)
    ┌───┴────────────────────┐
    ↓                        ↓
M3.1: MEDIA RED (1 day)  M4.1: API RED (1 day)
    ↓                        ↓
M3.2: MEDIA GREEN (2 days)  M4.2: API GREEN (2 days)
    ↓
M5: UI SCAFFOLDING (1–2 days)
    ↓
M6: EVIDENCE EXPORT (1 day)
    ↓
M7: DOCKER & DEPLOYMENT (1 day)

Critical Path: M1 → M2 → M3.1 → M3.2 → ... (7 sequential)
Parallel: M3.1 and M4.1 tests can be written in parallel after M2
Total Estimate: 9–13 days (2+ weeks)
```

---

## ✅ Review Checklist (Per Milestone)

### For M1 Code Review
- [ ] Schema matches IMPL-M1 exactly (table names, column types, indexes)
- [ ] Foreign keys are enabled (`PRAGMA foreign_keys=ON`)
- [ ] WAL mode is enabled for concurrency
- [ ] `DatabaseConnection` class initializes without errors
- [ ] Fixtures can insert and query test data
- [ ] Verification steps pass (schema integrity, foreign key constraints work)

### For M3.1 Code Review
- [ ] All 12 tests exist in `tests/test_media.py`
- [ ] Tests follow GIVEN-WHEN-THEN docstring format
- [ ] Test names describe behavior + expected outcome
- [ ] All tests are SKIPPED (no real HTTP requests, no production code)
- [ ] Fixtures are reused from conftest.py
- [ ] No new dependencies added (pytest + conftest.py only)

---

## 📞 Questions & Support

### If you get stuck:
1. **Schema question?** → Check IMPL-M1-DATABASE-SCHEMA.md (exact SQL provided)
2. **Test structure question?** → Check IMPL-M3.1-MEDIA-UPLOAD-RED.md (full test file provided)
3. **Fixture question?** → conftest.py is created in M1; fixtures are example code
4. **Next milestone?** → After each milestone completes, a new Implementation Plan will be created

### If you find ambiguity:
1. Post GitHub Issue with "AMBIGUITY:" prefix
2. Check if it's in Plan.md (A1–A5) and already resolved
3. Don't proceed until clarified

---

## 🎯 Success Metrics

**By end of this sprint (all milestones complete):**
- [ ] All 7 milestones executed (M1–M7)
- [ ] All tests passing (pytest -v returns 100% pass)
- [ ] Docker image builds and runs
- [ ] Citizen can submit report → officer approves → citizen sees points
- [ ] README promises match actual behavior
- [ ] No breaking changes to existing skeleton code

---

## 📎 Document Map

| Document | Purpose | Owner | Status |
|----------|---------|-------|--------|
| `Plan.md` | Master milestone breakdown | Stakeholder | ✅ APPROVED |
| `STATUS.md` | Current state overview | Documentation | 📖 Reference |
| `README.md` | Project scope + API spec | Documentation | 📖 Reference |
| `IMPL-M1-DATABASE-SCHEMA.md` | M1 executable plan | Implementation Engineer | ⏳ READY |
| `IMPL-M3.1-MEDIA-UPLOAD-RED.md` | M3.1 executable plan | Test Engineer | ⏳ READY |
| `IMPL-M2-FASTAPI-APP.md` | M2 executable plan | [To be created] | 📝 PENDING |
| `IMPL-M3.2-MEDIA-UPLOAD-GREEN.md` | M3.2 executable plan | [To be created] | 📝 PENDING |
| `IMPL-M4.1-API-RED.md` | M4.1 executable plan | [To be created] | 📝 PENDING |
| `IMPL-M4.2-API-GREEN.md` | M4.2 executable plan | [To be created] | 📝 PENDING |
| `IMPL-M5-UI-SCAFFOLDING.md` | M5 executable plan | [To be created] | 📝 PENDING |
| `IMPL-M6-EVIDENCE-EXPORT.md` | M6 executable plan | [To be created] | 📝 PENDING |
| `IMPL-M7-DOCKER-DEPLOYMENT.md` | M7 executable plan | [To be created] | 📝 PENDING |

---

## 🔄 Workflow After Each Milestone

1. **Milestone Implementation** — Developer executes per Implementation Plan
2. **Verification** — Developer runs Definition of Done checklist
3. **Code Review** — Reviewer checks against Review Checklist
4. **Approval** — Stakeholder approves or requests changes
5. **Git Commit** — Developer commits with provided commit message
6. **Next Plan** — Copilot creates Implementation Plan for next milestone

---

## 🚀 Start Now

**Recommended order:**

| Day | Milestone | Owner | Duration |
|-----|-----------|-------|----------|
| **Day 1** | M1 (DATABASE SCHEMA) | Implementation Engineer | 1–2 days |
| **Day 2–3** | M2 (FASTAPI APP) | Implementation Engineer | 1–2 days |
| **Day 3–4** | M3.1 (MEDIA RED) + M4.1 (API RED) | Test Engineer (parallel) | 1 day each |
| **Day 4–5** | M3.2 (MEDIA GREEN) | Implementation Engineer | 2 days |
| **Day 6–7** | M4.2 (API GREEN) | Implementation Engineer | 2 days |
| **Day 7–8** | M5 (UI SCAFFOLDING) | Frontend Developer | 1–2 days |
| **Day 8** | M6 (EVIDENCE EXPORT) | Implementation Engineer | 1 day |
| **Day 9** | M7 (DOCKER & DEPLOYMENT) | DevOps Engineer | 1 day |

**Total: 9–13 working days (2+ weeks)**

---

**Generated:** 2026-11-01  
**Status:** READY TO EXECUTE  
**Next Action:** Start M1 (DATABASE SCHEMA) with Implementation Engineer
