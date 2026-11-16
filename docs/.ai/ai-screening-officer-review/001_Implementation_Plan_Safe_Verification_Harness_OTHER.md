# Implementation Plan — Safe Verification Harness

## Milestone

ASOR-M02 — Safe current-demo verification harness. Prepared 2026-11-08; final planning verification 2026-11-09, America/Chicago. This is a proposal for review, not authorization or execution evidence.

## Milestone Type

OTHER. The approved Plan assigns ASOR-C02 only: safe repeatable verification. No owned requirement adds or changes production behavior. The user-approved Q15 correction changes a stale test to the existing approved contract. Missing upload, ownership, AI, officer-action and recovery behavior stays in its recorded RED/GREEN milestones.

## Authoritative References

- `requirements.md`: approved by the user 2026-11-08; all nineteen requirements, acceptance criteria and clarification log read; R01/Q2 select the current local demo.
- `Plan.md`: approved 2026-11-08, including user-confirmed Q15 recorded by the main workflow; M01 Completed, M02 Pending, no earlier current-work-item Implementation Plan. M02 supplies scope, preservation, failure-disposition gate and completion criteria. The verification section explicitly requires inspecting unrelated infrastructure prerequisites rather than adopting the historical redesign.
- `External-Contract.md`: Contract Review Status Approved by user 2026-11-08; M01 predecessor. Baseline and CT04 preserve required vehicle number and `awaiting-review`; Compatibility Notes identify stale submission fixtures/assertion, twelve skipped media placeholders and commented officer assertions.
- `.github/copilot-instructions.md`: inspected repository guidance; its own footer says Awaiting approval. Follow its applicable no-executable-change-before-review boundaries, but use actual runtime/dependency files and this work item's approved artifacts rather than its stale contextual claims.
- Current-state evidence, not approval artifacts: `app.py`, `bootstrap.py`, `auth_utils.py`, all six active test modules and `tests/conftest.py`, `pytest.ini`, `requirements.txt`, `.venv/pyvenv.cfg`, installed `starlette/testclient.py` lifecycle implementation; source/fixture excerpts and runtime package metadata inspected. `docs/API-REQUEST-RESPONSE-REFERENCE.md` is identified by the approved contract as stale, not adopted as authority. Historical initial-build artifacts are explicitly excluded by R01 and do not contribute carried-forward decisions. No product-level `docs/requirements.md` exists.
- Planning rules/templates read: production-engineering-standards 0.15.0 `commands/create-implementation-plan.md`, `skills/implementation-planning/SKILL.md`, `skills/prompt-driven-development/SKILL.md` and its `templates/Implementation-Plan.md`, `skills/testing/SKILL.md`, `skills/requirements-analysis/SKILL.md`, `skills/security/SKILL.md`. These govern planning, not product requirements.

## Carried-Forward Decisions

There is no previously approved Implementation Plan in this work item. Carry the approved current-demo FastAPI/SQLite baseline, unchanged authentication and points, existing Python dependency pins, and M01 contract/Q15 test disposition forward. Do not adopt historical service scaffolding, PostgreSQL, Docker, providers or SDKs as M02 prerequisites.

## Preconditions / Predecessor Evidence

M01's completed execution row points to the approved complete External-Contract. M02 remains Pending. User decision Q15 explicitly permits only the required `vehicle_number` input and `awaiting-review` status correction, retaining every other submission assertion. The schema/lifecycle/isolation repairs below are submitted for human review in this plan. There is no accepted nonblocking failing test. Every proposed verification command must pass; a different failure stops execution and returns to planning.

## Current Repository State

The working tree reports an untracked current-work-item document folder; it is not claimed clean. No root test or application lifespan was run during this planning task. A private path/length/SHA-256 baseline was captured before scratch writes for existing source, tests, configuration, database/sidecars, media and private local files; values and private contents are not reproduced here.

Installed native runtime is Python 3.14.3, FastAPI 0.162.0, Starlette 1.10.0, httpx 0.28.1, pytest 9.1.1, pytest-asyncio 1.4.0, AnyIO 4.15.1, bcrypt 4.1.2 and Pillow 13.0.0. Existing requirements pins remain unchanged. Existing Starlette emits an httpx deprecation warning; this is recorded, not used to introduce httpx2 or any upgrade.

`tests/test_auth.py` deletes the cwd database/sidecars, removes modules, and manually starts a separate event loop/lifespan. `conftest.py` globally substitutes raw SQLite and handwritten schema without vehicle_number/citizen/officer tables; its client omits a managed lifespan. The real `bootstrap.DatabaseConnection` provides the schema, wrapper/transaction API and close; existing SQL seeding fixtures still receive its raw `.connection` so their `commit()` calls remain valid. Production handlers use the actual wrapper via unpatched `get_db`/`init_database`.

### Observed baseline and exact failure dispositions

All baseline executions used copied source and synthetic state; no historical database/media/private-local content was copied. Results below are planning observations, never milestone completion or RED evidence.

| Check | Observed baseline | Disposition for review |
| --- | --- | --- |
| Entire `tests/test_auth.py` | 23 passed, 1 existing deprecation warning; 20.58 s | Preserve all 23 assertions/test bodies; remove only unsafe local client fixture/imports and use shared managed fixture. |
| `TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id` | 400 versus expected 201, line 57; reproduced twice as the sole selected node | Test payload omits current required vehicle_number; later `submitted` expectation contradicts approved baseline/CT04. Q15 authorizes the exact correction shown, no production change. |
| `TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports` | 500 versus expected 200, line 96; captured `Error in fetch_reports: no such column: vehicle_number`; reproduced twice separately | Harness schema defect. Use real startup/schema; retain every existing history assertion. |
| `TestCitizenReportDetails::test_citizen_fetch_report_details_with_timeline` | Passed | Preserve exact legacy timeline assertions; historical submitted/screening events remain readable per CT01. |
| Seven remaining active API tests listed below | Passed after fixture/SQL setup; HTTP calls and all assertions are commented | Keep unchanged, report as setup-only. They do not prove officer/clarification workflow behavior. M03/M09/M13 RED scopes supply real contract checks later. |
| Entire `tests/test_api_endpoints.py` | 2 failed, 8 passed, 1 warning; 1.02 s | Both failures are explicitly owned harness/stale-test subjects, not accepted nonblocking failures. |
| Entire `tests/test_media.py` | 12 skipped, 1 warning; 1.10 s | Preserve unchanged and disclose all skips. No valid media/access/upload coverage, no RED evidence. M03 owns real intake tests. |
| Entire `tests/test_identity.py` | 6 passed, 1 warning; 1.90 s | Native synthetic transport safety net; retain unchanged and include in both verification runs. |
| `tests/test_controls.py`, `tests/test_identity_oidc.py` | Not executed; fixture inspection requires absent `/private/configuration.dsn`, `/private/gateway.dsn` and/or real CA/Keycloak/service/browser infrastructure | Not selected as current-demo acceptance commands, not counted as passing/skipped tests. No private content read, external service started or historical infrastructure introduced. Files and existing workflow preserved by hash comparison. Plan expressly excludes requiring that redesign for this demo. |

Initial restricted baseline commands for auth and API timed out at 50 s each. A fixed one-node 8 s faulthandler run recorded the main thread in `socket._fallback_socketpair` → asyncio Proactor `_make_self_pipe` → `asyncio.new_event_loop`, before app startup. Expanded local execution of the same node passed (1.82 s), then the bounded full baseline produced the real outcomes above. An earlier diagnostic helper omitted its scratch import path and failed `import bootstrap`; it was corrected before diagnosis, without changing tests. Neither helper error nor environment timeout is business failure, RED, or successful verification. The 45-node restricted diagnostic used four 15 s bounded children at a time: 26 timed out, seven setup-only nodes passed and twelve skipped; all results remain private and inconclusive for the timed-out nodes. The later sequential expanded runs are not retries until a test happens to pass; they remove the demonstrated local socket prerequisite and retain the two genuine failures.

The first independent harness probe deliberately kept the stale submission unchanged: both runs were 34 passed, 12 skipped, exactly that one failure. This established history/lifecycle repair without silently changing the business expectation. Only after Q15 was recorded was the exact approved correction added.

### Named preservation inventory

All nodes below run, unchanged except the narrowly approved Q15 payload/status correction. Coverage is described by executed assertions, not class names. In particular, the authentication tests with ownership names mostly verify authenticated list access, not cross-owner media protection.
- `tests/test_auth.py::TestSignup::test_signup_with_valid_data_returns_201`
- `tests/test_auth.py::TestSignup::test_signup_with_duplicate_citizen_id_returns_409`
- `tests/test_auth.py::TestSignup::test_signup_with_duplicate_email_returns_409`
- `tests/test_auth.py::TestSignup::test_signup_with_invalid_email_returns_400`
- `tests/test_auth.py::TestSignup::test_signup_with_missing_email_returns_400`
- `tests/test_auth.py::TestSignup::test_signup_with_missing_password_returns_400`
- `tests/test_auth.py::TestSignup::test_signup_with_short_password_returns_400`
- `tests/test_auth.py::TestSignup::test_signup_password_is_hashed_not_plaintext`
- `tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200`
- `tests/test_auth.py::TestLogin::test_login_with_invalid_password_returns_401`
- `tests/test_auth.py::TestLogin::test_login_with_nonexistent_citizen_returns_401`
- `tests/test_auth.py::TestLogin::test_login_returns_session_token`
- `tests/test_auth.py::TestLogin::test_login_updates_last_login_timestamp`
- `tests/test_auth.py::TestLogout::test_logout_returns_204_no_content`
- `tests/test_auth.py::TestLogout::test_logout_without_token_returns_401`
- `tests/test_auth.py::TestAccessControl::test_accessing_reports_without_token_returns_401`
- `tests/test_auth.py::TestAccessControl::test_accessing_reports_with_invalid_token_returns_401`
- `tests/test_auth.py::TestAccessControl::test_citizen_can_see_own_reports`
- `tests/test_auth.py::TestAccessControl::test_citizen_cannot_see_other_citizens_reports`
- `tests/test_auth.py::TestAccessControl::test_citizen_id_from_token_used_for_reports`
- `tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_returns_profile`
- `tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_without_token_returns_401`
- `tests/test_auth.py::TestIntegration::test_complete_citizen_workflow`

Active API assertion preservation/correction set:

- `tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id`
- `tests/test_api_endpoints.py::TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports`
- `tests/test_api_endpoints.py::TestCitizenReportDetails::test_citizen_fetch_report_details_with_timeline`

Unchanged setup-only API nodes, not behavioral coverage:

- `tests/test_api_endpoints.py::TestOfficerReviewQueue::test_officer_query_review_queue_returns_paginated_list`
- `tests/test_api_endpoints.py::TestOfficerCaseDetail::test_officer_view_case_detail_shows_evidence`
- `tests/test_api_endpoints.py::TestOfficerApproval::test_officer_approve_report_awards_points`
- `tests/test_api_endpoints.py::TestOfficerRejection::test_officer_reject_with_reason_stores_reason`
- `tests/test_api_endpoints.py::TestOfficerClarificationRequest::test_officer_request_clarification_requeues_case`
- `tests/test_api_endpoints.py::TestCitizenClarification::test_citizen_clarification_response_resubmits_case`
- `tests/test_api_endpoints.py::TestOfficerQueueUpdate::test_officer_queue_reflects_requeued_cases`

Unchanged native synthetic identity preservation set:

- `tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source`
- `tests/test_identity.py::test_claim_validation_and_error_contract`
- `tests/test_identity.py::test_human_permission_boundary_without_business_handlers`
- `tests/test_identity.py::test_fixed_service_client_audience_scope_matrix`
- `tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache`
- `tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers`

Existing media skip inventory, retained and never counted as coverage:

- `tests/test_media.py::TestMediaUploadValidation::test_upload_valid_jpeg_returns_media_id_and_hash`
- `tests/test_media.py::TestMediaUploadValidation::test_upload_valid_mp4_video_returns_media_id`
- `tests/test_media.py::TestMediaUploadValidation::test_duplicate_file_returns_409_conflict`
- `tests/test_media.py::TestMediaUploadValidation::test_file_too_large_returns_413_payload_too_large`
- `tests/test_media.py::TestMediaUploadValidation::test_video_too_long_returns_413`
- `tests/test_media.py::TestMediaUploadValidation::test_unsupported_file_format_returns_422`
- `tests/test_media.py::TestMediaUploadValidation::test_corrupted_jpeg_returns_422`
- `tests/test_media.py::TestTechnicalScreening::test_low_resolution_image_flags_warning`
- `tests/test_media.py::TestTechnicalScreening::test_high_blur_video_flags_warning`
- `tests/test_media.py::TestMediaAccessControl::test_citizen_can_download_own_media`
- `tests/test_media.py::TestMediaAccessControl::test_citizen_cannot_download_other_citizens_media`
- `tests/test_media.py::TestMediaAccessControl::test_officer_can_download_any_media`

The preserved `sample_media` fixture remains legacy metadata attached to a sample report and uses synthetic names/hash; this plan does not turn it into a valid future CT04 owned-unattached positive intake fixture. M03/M04 must supply that fixture for their approved ownership/attachment checks. No valid-upload/codec claim is made from its fake bytes or metadata.

## Files in Scope

### Files to Create

- `tests/test_verification_harness.py`
- `tests/verify_current_demo.py`

### Files to Modify

- `tests/conftest.py`
- `tests/test_auth.py`
- `tests/test_api_endpoints.py`

### Files to Delete

None. The Implementation Plan artifact itself is the only repository write during planning. These five executable changes are proposed only.

## Proposed Changes

1. Replace conftest's handwritten/global/autouse database patch/cleanup and unmanaged client with function-scoped `runtime_factory`, `demo_runtime`, `test_db`, and `client`. `runtime_factory()` returns a context manager yielding `(TestClient, sqlite3.Connection, Path)` from real production startup. Each invocation creates its own tmp_path child, copies only public static/templates, changes cwd within a restoring monkeypatch context, resets/restores only the bootstrap database global, enters/exits `with TestClient(application.app)`, and asserts real database identity/file path, effective media root and closed connection. Retain the existing sample-report/media fixture content without changed business semantics.
2. Remove test_auth's destructive client fixture and its now-unused imports. Use the common fixture. Do not change any test body/assertion.
3. Apply only Q15 in the submission test: add synthetic `vehicle_number: KA01AB1234`, replace `submitted` with `awaiting-review` in the status assertion and matching docstring. Keep HTTP201/id/category/citizen/created_at checks, all other API tests and assertions unchanged.
4. Add two harness-only tests: real schema and effective database/media containment, with a synthetic sentinel file; two independently started lifespans do not reuse DB state and close the prior SQLite connection. Positive health requests prove a running app before closure/isolation checks; no future feature behavior is supplied by a mock.
5. Add `tests/verify_current_demo.py`, a standard-library-only safe entry point. It hashes protected root/state/source/test/config paths in memory, creates one unique disposable repository under the actual OS temp root, allowlists only root Python/pytest.ini and tests/templates/static (not database/media/.local/.env), verifies excluded data absent, and launches the exact five selected test modules twice in that one copy. Each child has a 90 s bound and is waited/reaped; no cleanup occurs between runs apart from fixture lifecycle. It sets all three temp variables to an owned scratch subdirectory so pytest fixtures cannot leak state to the global temp directory. It prints real synthetic test output/status, verifies unchanged protected hashes, deletes the owned disposable tree via TemporaryDirectory and asserts deletion. Any nonzero child/timeout stops the loop after its log/wait, then still performs the protected-state guard/owned cleanup and returns failure. A second run is made only after the first passes. No failing test is ignored or accepted.

### Explicit tool/configuration decisions for review

| Decision introduced by test code | Trace / reason |
| --- | --- |
| Existing pytest/TestClient/pytest-asyncio with real app lifespan and production schema | Plan M02 lifecycle/schema repair; no package or version change. Alternative of another handwritten schema or mocked bootstrap would preserve the demonstrated drift and is not proposed. |
| Function-scoped UUID runtime below pytest tmp_path, cwd restoration, static/templates copy | M02 isolation while app hardcodes relative database/media/template/static paths. No production path setting is added. |
| `pytest.MonkeyPatch` for cwd/bootstrap-global restoration only | M02 process-state isolation; no substituted database functions, endpoint handlers or authentication outputs. |
| `-v`, explicit five module paths, `-p pytest_asyncio.plugin` | Reviewable exact node results; existing pytest-asyncio required by six unchanged identity tests. No selection by failed-test exclusion. A first unexpected failed/timeout child stops verification rather than being retried. |
| `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` | Explicitly control unrelated installed pytest plugins; load the existing required asyncio plugin explicitly. No dependencies added. |
| `PYTHONUTF8=1`, `PYTHONDONTWRITEBYTECODE=1` | UTF-8 evidence on Windows and no copied-source bytecode side effects. |
| `TMP`, `TEMP`, `TMPDIR` all point to owned scratch/temporary | Contain existing pytest/tempfile state; effective DB/media paths are additionally asserted by fixtures. |
| Remove inherited environment entries whose names contain GEMINI, GOOGLE, OPENAI, ANTHROPIC, OTEL_, ROADWATCH, DATABASE_URL, JWT_SECRET or OIDC_; and exact names CONTROLS_RUNTIME, SERVICE_ROLE, DATABASE_DSN_FILE, TRUST_CA_FILE, APP_PROFILE, AI_ADAPTER from the child only | Provider-free synthetic verification without using/logging credentials or accidental inherited live configuration; JWT_SECRET removal uses the existing built-in demo signing default. Removing inherited bootstrap role/OIDC/controls/profile/DSN/CA settings prevents accidental historical service activation or private-file access; bootstrap.py:464–483 is the import-time boundary. Parent environment is unchanged. No provider/app setting is created. |
| 90 s per child, two runs, one disposable repository | Plan M02 bounded repeatability; observed native full run approximately 31–33 s, no performance target imposed. TIMEOUT is failure/inconclusive, never valid RED. |
| Protected-path SHA-256 snapshot and allowlisted disposable copy | Plan C02 and preservation constraints; no private file contents or hash values printed, no live data reused. |

No new library, SDK, dependency pin, app configuration, CI workflow, Docker or service infrastructure is introduced.

## Proposed Code / Tests

The following diffs and complete new files are exact. They are review-only; they were applied only to disposable synthetic copies for planning.

### `tests/conftest.py` — complete unified diff

```diff
--- a/tests/conftest.py
+++ b/tests/conftest.py
@@ -1,135 +1,61 @@
-"""Test fixtures for M3+ milestones (database, reports, media).
+"""Current-demo fixtures use the real lifespan and production SQLite schema."""
+from contextlib import contextmanager
+from pathlib import Path
+import shutil
+import sqlite3
+from datetime import datetime, timezone
+from uuid import uuid4
 
-M1 (DATABASE SCHEMA) deliverable.
-Provides sample_report, sample_media, and test_db fixtures.
-"""
 import pytest
-import sqlite3
-import tempfile
-from pathlib import Path
-from uuid import uuid4
-from datetime import datetime, timezone
 from fastapi.testclient import TestClient
 
-# Global test database - persists for entire test session
-_TEST_DB = None
-_TEST_DB_PATH = None
-
-def _create_test_db():
-    """Create a fresh test database connection."""
-    global _TEST_DB, _TEST_DB_PATH
-    
-    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
-        _TEST_DB_PATH = f.name
-    
-    conn = sqlite3.connect(_TEST_DB_PATH, check_same_thread=False)
-    conn.row_factory = sqlite3.Row
-    conn.execute("PRAGMA foreign_keys=ON")
-    
-    # Initialize schema
-    conn.executescript("""
-        CREATE TABLE reports (
-            id TEXT PRIMARY KEY,
-            citizen_id TEXT NOT NULL,
-            violation_type TEXT NOT NULL,
-            location TEXT,
-            status TEXT NOT NULL DEFAULT 'submitted',
-            provisional_points INTEGER DEFAULT 0,
-            created_at TEXT NOT NULL,
-            updated_at TEXT NOT NULL,
-            screening_notes TEXT,
-            officer_notes TEXT
-        );
-        
-        CREATE TABLE events (
-            id TEXT PRIMARY KEY,
-            report_id TEXT NOT NULL,
-            event_type TEXT NOT NULL,
-            actor TEXT NOT NULL,
-            reason TEXT,
-            created_at TEXT NOT NULL,
-            old_status TEXT,
-            new_status TEXT NOT NULL,
-            provisional_points INTEGER,
-            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
-        );
-        
-        CREATE TABLE media (
-            id TEXT PRIMARY KEY,
-            report_id TEXT NOT NULL,
-            filename TEXT NOT NULL,
-            file_size_bytes INTEGER NOT NULL,
-            mime_type TEXT NOT NULL,
-            sha256_hash TEXT NOT NULL UNIQUE,
-            storage_path TEXT NOT NULL,
-            screening_status TEXT DEFAULT 'pending',
-            screen_blur_score REAL,
-            screen_blur_flagged BOOLEAN DEFAULT FALSE,
-            screen_resolution_width INTEGER,
-            screen_resolution_height INTEGER,
-            screen_resolution_flagged BOOLEAN DEFAULT FALSE,
-            screen_frame_count INTEGER,
-            screen_frame_sampled_count INTEGER,
-            ai_screening_status TEXT,
-            ai_screening_result TEXT,
-            ai_screened_at TEXT,
-            uploaded_at TEXT NOT NULL,
-            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
-        );
-        
-        CREATE TABLE operators (
-            id TEXT PRIMARY KEY,
-            report_id TEXT NOT NULL,
-            control_type TEXT NOT NULL,
-            control_state TEXT NOT NULL,
-            requested_by TEXT NOT NULL,
-            requested_at TEXT NOT NULL,
-            completed_at TEXT,
-            result_json TEXT,
-            FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
-        );
-    """)
-    
-    _TEST_DB = conn
-    return conn
-
-
-@pytest.fixture(scope="session", autouse=True)
-def _setup_test_db():
-    """Session-level setup to create and patch the test database."""
-    # Create test database
-    test_db = _create_test_db()
-    
-    # Patch bootstrap module to use test database
-    import bootstrap
-    bootstrap.get_db = lambda: test_db
-    bootstrap.init_database = lambda *args, **kwargs: test_db
-    
-    yield test_db
-    
-    test_db.close()
-    if _TEST_DB_PATH:
-        Path(_TEST_DB_PATH).unlink()
+REPOSITORY = Path(__file__).resolve().parents[1]
 
 
 @pytest.fixture
-def test_db():
-    """Provide the session-level test database connection.
-    
-    Returns the global test database that's shared across all tests.
-    Each test should clear its own data or use unique IDs to avoid conflicts.
-    """
-    global _TEST_DB
-    return _TEST_DB
+def runtime_factory(tmp_path):
+    """Create independent lifespans without touching the checkout's data."""
+    @contextmanager
+    def start():
+        runtime = tmp_path / uuid4().hex
+        runtime.mkdir()
+        assert not runtime.resolve().is_relative_to(REPOSITORY)
+        assert runtime.resolve().is_relative_to(tmp_path.resolve())
+        for name in ("static", "templates"):
+            shutil.copytree(REPOSITORY / name, runtime / name)
+        with pytest.MonkeyPatch.context() as patch:
+            patch.chdir(runtime)
+            import bootstrap
+            import app as application
+            patch.setattr(bootstrap, "db_connection", None)
+            with TestClient(application.app) as active:
+                db = bootstrap.get_db()
+                assert db is application.app.state.db
+                expected = (runtime / "roadwatch.db").resolve()
+                assert db.db_path.resolve() == expected
+                actual = Path(db.execute("PRAGMA database_list").fetchone()[2]).resolve()
+                assert actual == expected
+                assert (Path.cwd() / "media_store").resolve() == runtime / "media_store"
+                yield active, db.connection, runtime
+            with pytest.raises(sqlite3.ProgrammingError, match="closed"):
+                db.execute("SELECT 1")
+    return start
 
 
-@pytest.fixture(autouse=True)
-def _clear_test_db_per_test(test_db):
-    """Clear database before each test to avoid cross-test contamination."""
-    test_db.execute("DELETE FROM events")
-    test_db.execute("DELETE FROM reports")
-    test_db.commit()
-    yield
+@pytest.fixture
+def demo_runtime(runtime_factory):
+    with runtime_factory() as runtime:
+        yield runtime
+
+
+@pytest.fixture
+def test_db(demo_runtime):
+    return demo_runtime[1]
+
+
+@pytest.fixture
+def client(demo_runtime):
+    return demo_runtime[0]
 
 
 @pytest.fixture
@@ -213,11 +139,3 @@
     }
 
 
-@pytest.fixture
-def client(test_db):
-    """FastAPI TestClient with test database.
-    
-    Uses the session-level test database that's already patched into bootstrap.
-    """
-    from app import app as fastapi_app
-    return TestClient(fastapi_app)
```

### `tests/test_auth.py` — complete unified diff

```diff
--- a/tests/test_auth.py
+++ b/tests/test_auth.py
@@ -5,62 +5,6 @@
 """
 
 import pytest
-import asyncio
-import sys
-import os
-from fastapi.testclient import TestClient
-
-
-@pytest.fixture
-def client():
-    """Fixture: FastAPI test client with lifespan support."""
-    # Clean up database files
-    db_path = "./roadwatch.db"
-    for suffix in ['', '-shm', '-wal']:
-        try:
-            os.remove(db_path + suffix)
-        except:
-            pass
-    
-    # Delete cached modules to force reimport
-    for mod_name in ['bootstrap', 'app']:
-        if mod_name in sys.modules:
-            del sys.modules[mod_name]
-    
-    # Reimport to get fresh instances
-    from app import app
-    
-    # Manually run the lifespan startup since TestClient doesn't do it reliably
-    # in FastAPI 0.162.0
-    async def run_lifespan_startup():
-        """Run lifespan startup code."""
-        lifespan_cm = app.router.lifespan_context(app)
-        stack = lifespan_cm.__aenter__()
-        await stack
-        return lifespan_cm
-    
-    # Get or create event loop
-    try:
-        loop = asyncio.get_running_loop()
-    except RuntimeError:
-        loop = asyncio.new_event_loop()
-        asyncio.set_event_loop(loop)
-    
-    # Run startup
-    lifespan_context = loop.run_until_complete(run_lifespan_startup())
-    
-    # Create test client
-    test_client = TestClient(app)
-    
-    # Yield the client to the test
-    yield test_client
-    
-    # Cleanup: run lifespan shutdown
-    async def run_lifespan_shutdown():
-        """Run lifespan shutdown code."""
-        await lifespan_context.__aexit__(None, None, None)
-    
-    loop.run_until_complete(run_lifespan_shutdown())
 
 
 @pytest.fixture
```

### `tests/test_api_endpoints.py` — complete unified diff

```diff
--- a/tests/test_api_endpoints.py
+++ b/tests/test_api_endpoints.py
@@ -36,12 +36,13 @@
         """
         GIVEN: Valid report submission with JPG, helmet violation, location
         WHEN: POST /api/reports with citizen identity
-        THEN: 201 status, report_id in response, status=submitted
+        THEN: 201 status, report_id in response, status=awaiting-review
         """
         # Arrange
         citizen_id = "citizen-test-001"
         request_payload = {
             "violation_type": "helmet",
+            "vehicle_number": "KA01AB1234",
             "location": "MG Road, Bangalore",
             "media_id": sample_media["id"]
         }
@@ -57,7 +58,7 @@
         assert response.status_code == 201
         body = response.json()
         assert "report_id" in body
-        assert body["status"] == "submitted"
+        assert body["status"] == "awaiting-review"
         assert body["violation_type"] == "helmet"
         assert body["citizen_id"] == citizen_id
         assert "created_at" in body
```

### `tests/test_verification_harness.py` — complete final content

```python
"""Regression evidence for ASOR-M02 fixture safety only."""
from pathlib import Path
import sqlite3

import pytest


def test_real_schema_and_effective_paths(demo_runtime):
    client, db, runtime = demo_runtime
    assert client.get("/health").status_code == 200
    columns = {row[1] for row in db.execute("PRAGMA table_info(reports)")}
    assert "vehicle_number" in columns
    tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"citizens", "officers", "reports", "events", "media", "operators"} <= tables
    media = Path("media_store")
    media.mkdir()
    (media / "synthetic.bin").write_bytes(b"ASOR-M02 synthetic fixture")
    assert (media / "synthetic.bin").resolve().is_relative_to(runtime)
    assert (runtime / "media_store/synthetic.bin").read_bytes() == b"ASOR-M02 synthetic fixture"


def test_independent_lifespans_close_and_do_not_reuse_state(runtime_factory):
    with runtime_factory() as (first, first_db, first_root):
        assert first.get("/health").status_code == 200
        first_db.execute("CREATE TABLE harness_sentinel (value TEXT)")
        first_db.execute("INSERT INTO harness_sentinel VALUES ('synthetic')")
        first_db.commit()
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        first_db.execute("SELECT 1")
    with runtime_factory() as (second, second_db, second_root):
        assert second.get("/health").status_code == 200
        assert first_root != second_root
        assert not second_db.execute("SELECT name FROM sqlite_master WHERE name='harness_sentinel'").fetchall()
        assert Path(second_db.execute("PRAGMA database_list").fetchone()[2]).resolve() == second_root / "roadwatch.db"
```

### `tests/verify_current_demo.py` — complete final content

```python
"""Run only the current-demo preservation set in a disposable repository copy."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "test_auth.py", "test_api_endpoints.py", "test_media.py",
    "test_verification_harness.py", "test_identity.py",
)


def snapshot():
    paths = [path for path in ROOT.iterdir() if path.is_file()]
    for name in ("media_store", ".local", "tests", "templates", "static", "tools", ".github"):
        directory = ROOT / name
        if directory.exists():
            paths.extend(path for path in directory.rglob("*") if path.is_file()
                         and "__pycache__" not in path.parts)
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


def main():
    before = snapshot()
    temp_root = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix="asor-m02-") as name:
        scratch = Path(name).resolve()
        assert scratch.parent == temp_root
        assert not scratch.is_relative_to(ROOT)
        copy = scratch / "repository"
        copy.mkdir()
        for source in ROOT.glob("*.py"):
            shutil.copy2(source, copy / source.name)
        shutil.copy2(ROOT / "pytest.ini", copy / "pytest.ini")
        for directory in ("tests", "templates", "static"):
            shutil.copytree(ROOT / directory, copy / directory,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak"))
        assert not (copy / "roadwatch.db").exists()
        assert not (copy / "media_store").exists()
        assert not (copy / ".local").exists()
        temporary = scratch / "temporary"
        temporary.mkdir()
        env = os.environ.copy()
        for key in list(env):
            if (any(word in key.upper() for word in
                    ("GEMINI", "GOOGLE", "OPENAI", "ANTHROPIC", "OTEL_", "ROADWATCH", "DATABASE_URL", "JWT_SECRET", "OIDC_"))
                    or key.upper() in {"CONTROLS_RUNTIME", "SERVICE_ROLE", "DATABASE_DSN_FILE",
                                       "TRUST_CA_FILE", "APP_PROFILE", "AI_ADAPTER"}):
                env.pop(key)
        env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
                   PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", TMP=str(temporary),
                   TEMP=str(temporary), TMPDIR=str(temporary))
        command = [sys.executable, "-m", "pytest", "-p", "pytest_asyncio.plugin", "-v"]
        command.extend("tests/" + filename for filename in FILES)
        failed = False
        for repeat in (1, 2):
            log_path = scratch / ("run-" + str(repeat) + ".log")
            with log_path.open("w", encoding="utf-8") as log:
                child = subprocess.Popen(command, cwd=copy, env=env,
                                         stdout=log, stderr=subprocess.STDOUT)
                try:
                    result = child.wait(timeout=90)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
                    result = "TIMEOUT"
            assert child.poll() is not None
            print("Run", repeat, "result:", result, flush=True)
            print(log_path.read_text(encoding="utf-8"), flush=True)
            failed = result != 0
            if failed:
                break
        assert snapshot() == before, "Protected checkout files changed"
        print("Protected checkout paths and SHA-256 values unchanged", flush=True)
    assert not scratch.exists()
    print("Disposable repository and test state removed; child processes finished", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## Execution Steps

1. Require human approval of this exact Implementation Plan. Confirm M01 still completed, M02 Pending, Q15 unchanged and executable baseline unchanged. If a material new failure/contract conflict exists, stop rather than choosing a disposition.
2. Apply exactly the three complete diffs and two complete new files above. No production/config/dependency file changes.
3. Invoke the safe runner below with the existing virtual-environment interpreter. The runner performs both repeated runs internally in disposable synthetic state; never invoke the old destructive baseline tests from the working directory.
4. Inspect both complete results and hash/cleanup statements. Require the exact expected node inventory and no new skip/xfail/failure/timeout. Seven setup-only passes and twelve existing media skips remain disclosed, not coverage.
5. Only after verified approved execution may the normal workflow record M02 execution evidence/status; planning has not updated that row and this plan does not approve subsequent milestones.

## Acceptance / Completion Criteria

- Only the five listed test files change; no production behavior/data/schema source/config/dependency/workflow change. Q15 is the sole changed business assertion and is corrected to the already approved contract with same coverage. The existing auth, history, timeline and six synthetic identity assertions all pass unchanged.
- No fixture deletes/reuses the user's cwd database/media; no module deletion/reload or handwritten schema substitution remains in current-demo fixtures. Real app startup/shutdown initializes the production schema and closes the real connection.
- The two new harness checks pass, and every shared fixture invocation asserts actual SQLite filename, DB identity, isolated cwd/media containment and connection closure. Two sequential lifespans prove no sentinel state leaks.
- Both full selected runs complete within their bounds with all 41 executable nodes passing and only the same twelve pre-existing media skips. Of the 41 passes, seven API setup-only nodes are expressly not behavioral coverage. No accepted pre-existing failure, blanket subset success, new skip, xfail, or weakening.
- Disposable input excludes real database/media/private-local content and provider credentials; fixture temp state is contained within owned scratch. Protected source/config/data path/hash snapshots compare equal and the owned tree is removed after both children have finished.
- Report the absent historical controls/OIDC prerequisites as unrun, and do not claim the entire repository test suite passed. A new failure or needed production change stops M02 and returns for planning/review.

## Verification

### Commands

From the repository root, after approval/application only:

```powershell
& .\.venv\Scripts\python.exe .\tests\verify_current_demo.py
```

This entry point itself imports only the standard library, then moves all pytest/app/lifespan work into its allowlisted disposable copy. It runs the following exact command twice in the same disposable repository, without cleanup between runs:

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe -m pytest -p pytest_asyncio.plugin -v tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py
```

The interpreter above is the existing virtual-environment path observed on this host; the exact runner obtains that same interpreter from `sys.executable`, rather than selecting a new version. On this Windows host restricted local sockets stalled Python event-loop creation; run the safe command with expanded local execution if needed. This is an execution capability for loopback/self-pipe sockets, not permission to call Gemini or start external services. Do not alter event-loop policy or tests to mask that environment problem.

### Expected Evidence

Latest final frozen-code planning observation (2026-11-09): 41 passed, 12 skipped on each of two runs, 17.37 s and 22.24 s; exit 0, protected hashes equal and owned cleanup confirmed. This is not milestone execution.

Expected / Predicted — Not Yet Verified as milestone evidence: both child results 0; each summary 41 passed, 12 skipped, existing deprecation warning; protected checkout paths/SHA-256 unchanged; disposable repository/test state removed; child processes finished. The planning-time observations below do not execute M02 or authorize its file changes.

### Planning-Time Dry Run

Private host-visible planning area: unique `asor-m02-20261108-12609b9b1c234633b56cb5f857ea4930` under `C:\Users\avina\AppData\Local\Temp`. Only copied source/public assets and own synthetic input were used. Existing virtual-environment interpreter was used without package installation. Logs are UTF-8. All subprocess calls had explicit 15/30/45/50/60/90 s bounds according to the recorded diagnostic stage; timed-out children were killed and waited. Each retained private log/result identifies its exact command and outcome.

Baseline command argument sequences, run separately in the unmodified disposable `baseline` directory:

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe -m pytest -p pytest_asyncio.plugin -v tests/test_auth.py
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe -m pytest -p pytest_asyncio.plugin -v tests/test_api_endpoints.py
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe -m pytest -p pytest_asyncio.plugin -v tests/test_media.py
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe -m pytest -p pytest_asyncio.plugin -v tests/test_identity.py
```

Trimmed actual expanded baseline output:

```text
23 passed, 1 warning in 20.58s
FAILED tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id
assert 400 == 201
FAILED tests/test_api_endpoints.py::TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports
assert 500 == 200
ERROR app:app.py:837 Error in fetch_reports: no such column: vehicle_number
2 failed, 8 passed, 1 warning in 1.02s
12 skipped, 1 warning in 1.10s
6 passed, 1 warning in 1.90s
```

Both failed nodes were each selected alone twice, unchanged, with the same interpreter/plugin/-v arguments and exact full selectors above; all four returned 1 with the same respective failures. No failure was hidden by a rerun. Restricted runs, stack trace and the corrected-helper import error remain separately recorded as described in Current Repository State.

The complete proposed exact code was applied to the disposable `proposal` only. Standard-library `ast.parse` on every proposed Python test file returned `All proposed test files parse`. The full suite itself imports/executes the changed fixtures/helpers, so this parse check is supplementary. The independent pre-Q15 two-run command was:

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe -m pytest -p pytest_asyncio.plugin -v tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py
```

Both runs returned 1, `1 failed, 34 passed, 12 skipped`, sole stale submission node; one trimmed recorded duration was 39.05 s. After Q15 was recorded/read, the initial complete proposed runner was invoked (before the final explicit signing/bootstrap-environment removal and fail-fast corrections):

```powershell
$env:PYTHONUTF8='1'
& C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\asor-m02-20261108-12609b9b1c234633b56cb5f857ea4930\proposal\tests\verify_current_demo.py *> C:\Users\avina\AppData\Local\Temp\asor-m02-20261108-12609b9b1c234633b56cb5f857ea4930\exact-runner.log
```

The invocation returned 0. Its exact-code runner repeated the stated five-module command internally, with no cleanup between its runs. Trimmed real output:

```text
Run 1 result: 0
41 passed, 12 skipped, 1 warning in 32.19s
Run 2 result: 0
41 passed, 12 skipped, 1 warning in 30.60s
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
```

The final frozen revision adds the explicitly reviewed JWT/bootstrap-environment isolation and stops on a first unexpected failure instead of making a second attempt. Its complete code is the code shown above. On 2026-11-09 the following exact invocation returned 0:

```powershell
$env:PYTHONUTF8='1'
& C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\asor-m02-20261108-12609b9b1c234633b56cb5f857ea4930\proposal\tests\verify_current_demo.py *> C:\Users\avina\AppData\Local\Temp\asor-m02-20261108-12609b9b1c234633b56cb5f857ea4930\frozen-runner-nov09.log
```

Trimmed real final frozen-code output:

```text
Run 1 result: 0
41 passed, 12 skipped, 1 warning in 17.37s
Run 2 result: 0
41 passed, 12 skipped, 1 warning in 22.24s
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
```

No other executable changes followed this frozen-code run. All three extracted plan diffs passed `git apply --check` and applied in another disposable baseline; their resulting files and the two extracted complete-file blocks matched all five frozen proposal files, and all parsed with `ast.parse`. This verifies the reviewed code's planning feasibility only. The difference from baseline command selection is explicit: two new harness checks and six already-baselined synthetic identity checks are included; the Q15 correction and schema/lifecycle repairs are proposed test changes. No tests were dropped from the three demo files.

### Planning evidence and cleanup limitation

Initial diagnostic runners did not override TMP/TEMP/TMPDIR. Therefore the existing baseline conftest's random `NamedTemporaryFile(delete=False)` databases could be created in global OS Temp; killed diagnostic children may bypass teardown. Those filenames were not captured, so their deletion cannot be proven and unknown Temp files must not be deleted by attribution guesswork. They contain only this task's synthetic fixture content if created by these runs; no real database/media/private content was copied. This is a planning cleanup limitation, not a passing isolation claim. Private baseline/log evidence is retained. The proposed exact runner explicitly corrects containment for future execution, and its own two-run owned-tree cleanup was observed passing. Only known-owned disposable trees may be removed; preserve evidence if any deletion cannot be proven. Final planning cleanup observed 2026-11-09: all 48 known-owned disposable directories (baseline, proposal, 45 per-node copies, mechanical-check) were removed after resolved absolute-path validation; the owned runner trees had already been removed by their runners. The retained private evidence directory contains only logs, baseline/root-integrity maps, helper source, exact patch and code-block hashes. All started test/runner sessions completed, and host process inspection found no Python process referring to the owned scratch directory. The complete root path-set/hash comparison found only this new Implementation Plan and the main workflow's expected Q15 Plan metadata change; source/tests/config/database/media/private-local paths and hashes were unchanged. The separately disclosed global Temp database attribution/cleanup uncertainty remains.

## Risks

- Process-global cwd/bootstrap state: fixtures are sequential within a process and restore state via MonkeyPatch. No parallel pytest plugin/processes are introduced by the runner. User data safety relies on invoking the provided safe entry point, which copies only public source/assets and asserts effective persistence paths.
- Authentication comparisons are untouched: citizen identity comes from existing token validation or existing demo header fallback, officer validator unchanged. Sample citizens/hashes are synthetic; no mock grants access. Neither these harness tests nor existing auth-list tests claim to establish cross-owner media isolation; that belongs to M03/M04. Points, category values and vehicle/location semantics are untouched.
- Existing legacy sample_media is already associated; no broadened attachment success is inferred. Future capability tests must exercise valid owned-unattached inputs and real photo/video decoding. The seven setup-only API tests and twelve skipped media placeholders give no workflow coverage.
- Connection closure uses production lifespan's `get_db().close()` and is checked with an actual closed-SQLite operation. Installed Starlette TestClient's context manager manages startup, shutdown, portal and stream/transport cleanup (`starlette/testclient.py:557–584`). No manual event-loop lifecycle remains in test_auth.
- The inherited private environment is removed only in subprocesses and never logged. The snapshot hashes file bytes privately without printing contents or values. No provider import/call or live Gemini test is part of M02.
- The guard is specifically subprocess.wait(timeout=90), not an independent strict wall-clock watchdog or application timing requirement. In an intermediate JWT-isolation-only run, the first child returned 0 with pytest elapsed 1187.10 s and the second returned 0 in 32.89 s; the wait did not interrupt the long reported interval. Host scheduling/suspension is a possible explanation, not established by the date/context update. That output is preserved and not claimed to prove a strict 90-second wall bound. No external watchdog or timing SLA is added. An actual timeout/nonzero result must fail visibly rather than be increased/retried until green without review. The final rerun is justified by the explicit fail-fast/bootstrap-environment code corrections, not a retry of an unchanged failing test.

## Pre-authorized Contingencies

None. A new file, dependency, changed assertion, production behavior change, new accepted failure or different acceptance selection returns for review. Routine correction of a command invocation error is reported as such; it does not grant scope to change code.

## Rollback / Recovery

Before approved application, preserve the three original test files privately. If execution fails, stop; retain evidence and undo only these five milestone file changes using those exact preserved originals, removing only the two newly created test helpers. Preserve unrelated work and all database/media/private files. No repository-wide reset/clean/checkout, SQL cleanup against user data or guessed global Temp deletion.

## Explicitly Out of Scope

Production source, database/schema migrations, .env/app settings/dependencies, live provider credentials/calls, Docker/infrastructure, CI changes, officer/clarification/media placeholder activation, new auth/points/reward behavior, current/future RED or GREEN implementation, approval recording and Plan status updates during planning. Existing unrelated controls/OIDC tests are preserved but unrun without their historical prerequisites.

## Per-File Exactness Review

| File | Review result |
| --- | --- |
| `tests/conftest.py` | Complete unified diff; imports/fixture removal and real-lifespan replacements all listed in Proposed Changes; sample fixtures preserved; no pseudocode or untraced new setting. |
| `tests/test_auth.py` | Complete unified diff; only destructive client fixture/unused imports removed, all test bodies/assertions preserved. |
| `tests/test_api_endpoints.py` | Complete unified diff; Q15 input/status/docstring correction only, all other checks retained. |
| `tests/test_verification_harness.py` | Complete final file; two harness-only checks match proposal and containment/closure criteria, no provider/dependency/production behavior added. |
| `tests/verify_current_demo.py` | Complete final file; all environment flags, timeout, selectors, temp paths and copy/hash mechanisms explicitly traced in decisions table; no new dependency. |

All introduced names are ordinary test/helper symbols, not reused ASOR requirement/contract/decision IDs. No template comments remain. Predicted milestone evidence and actual planning observations are distinguished throughout.

## Human Review

Executed on 2026-11-09 following user approval on 2026-11-09 for ASOR-M02 only. See [Plan.md execution status](Plan.md#execution-status) and [execution evidence](ASOR-M02-Execution-2026-11-09.md): both isolated runs passed, protected hashes unchanged and owned cleanup verified. Later milestones and production/provider changes remain unauthorized.
