# Implementation Plan — Durable Processing GREEN

## Milestone and boundary

ASOR-M06 — Durable processing GREEN, work item `ai-screening-officer-review`, type **GREEN**, predecessor ASOR-M05. Prepared 2026-11-09, America/Chicago. Plan records M05 Completed and M06 Pending. This proposal delivers only ASOR-R15/R16 and ASOR-C04 verified by the approved M05 checks. Planning observations below do not execute M06 or authorize later milestones.

## Authoritative References

- `requirements.md`, user-approved 2026-11-08: R15/R16, AC09, Q6 and current-demo boundaries.
- `Plan.md`, user-approved 2026-11-08: M06 scope/type, current execution rows, R15/R16/C04 ownership; M08 owns provider/policy integration, M10 human-final safety, M14 evidence-changing actions and M16 complete operational presentation.
- `External-Contract.md`, user-approved M01 2026-11-08: CT02/04 atomic pending acceptance, CT15 persistence/consumed attempts/duplicate and obsolete output, CT16 default retry schedule, contract-wide identity/errors/idempotency. CT17/18 full operational accounting stays M16; no provider or legal choices are reopened.
- `001_Implementation_Plan_Safe_Verification_Harness_OTHER.md`, `002_Implementation_Plan_Evidence_Intake_RED.md`, `003_Implementation_Plan_Evidence_Intake_GREEN.md`, `004_Implementation_Plan_Durable_Processing_RED.md`: all approved/executed predecessor artifacts; Human Review sections establish authority. Their lifecycle, isolation, source-only copy, test selection, decoder forwarding and approved004 internal seams carry forward unchanged.
- `ASOR-M02-Execution-2026-11-09.md`, `ASOR-M03-Execution-2026-11-09.md`, `ASOR-M04-Execution-2026-11-09.md`, `ASOR-M05-Execution-2026-11-09.md`: completed evidence. M05 has two identical14-node behavioral RED inventories, ordinary test-body `DURABLE_PENDING_NOT_COMMITTED` assertions, no setup errors/skips; its common earliest gate does not independently prove downstream behaviors. Its approved scratch soundness probe is distinct from execution evidence.
- `.github/copilot-instructions.md` inspected: footer Awaiting approval; use its consistent PDD boundary, not stale runtime/dependency claims. No applicable AGENTS.md or product-level `docs/requirements.md` exists.
- Current-state evidence: app.py/bootstrap.py/intake.py/auth_utils.py, tests/conftest.py, durable and intake tests, both unchanged safe launchers, relevant auth/API/media/identity/harness tests, requirements.txt and pytest.ini. These are repository evidence, not approval artifacts.
- Process guidance: PDD, implementation-planning, python-fastapi, distributed-systems, resilience-and-degradation (including local-adapter guidance), security. No new product requirements derive from these skills.

## Current state and predecessor preservation

The checkout is dirty: app.py/bootstrap.py/tests/conftest.py/tests/test_api_endpoints.py/tests/test_auth.py modified; intake.py, work-item docs, durable/intake/harness checks and both launchers untracked. Preserve these exact baseline bytes. Existing intake commits report, attachment positions and event in one immediate transaction. It has no durable jobs/attempts/recovery or AI summary. Bootstrap initializes the actual SQLite schema and M04 intake migration. Lifespan currently owns only the database. Existing officer queue includes awaiting-review claims; durable technical failure must leave them there.

M05 completed unchanged preservation twice (94 passes/12 existing skips) and classified14 RED nodes twice. Seven historical API bodies remain setup-only;12 legacy media skips supply no coverage. Historical infrastructure/OIDC/control suites are unchanged and unrun. Existing Starlette/httpx warning remains. No all-repository, model-quality or native decoder/deployment-readiness claim is made.

Private full absolute-path/length/SHA-256 preimages were captured before checkout document creation; non-Markdown protection was independently captured by the carried setup. Real DB/media/.local content never entered scratch. M04's coherent private recovery backup is retained, untouched and never used as a verification fixture. Planning does not open, migrate, checkpoint, copy or start the real database/application.

## Carried-forward decisions

1. 001/002/003: actual production lifespan/schema, UUID-owned runtime with asserted effective DB/media paths and closed connections; unchanged dependency pins, pytest plugin selection, no autoload, UTF-8/no-bytecode, environment stripping and allowlisted source-only copies.
2. 003/004: native Windows loopback capability and real-decoder forwarding through existing `traffic-60e6e567315a-runner:latest`, actual temporary bytes on stdin, `--network none --rm`, no installation/mock/production Docker dependency. Native Windows decoder installation remains outstanding.
3. 004: same local SQLite database; `ai_jobs`, `ai_attempts`, `ai_history`, `reports.evidence_revision`; exact JobStore/Worker/factory method seams, numeric internal scheduling clock, ascending attempts, committed-before-return store writes, revision-bound ownership, accepted/superseded history. Public summary timestamps are UTC strings.
4. 004: `app.ai_worker_factory(path)` start/stop owned by lifespan; injected dispatch returns an already validated advisory result. No provider validation is inferred from this seam. Paused test worker changes scheduling only; storage remains production.
5. 004: classified failure handling; fixed three consumed attempts, interrupted unknown billing, default5/10 scheduling; unchanged90-second durable child bound and180-second intake bound. Test assertions, configurations and runner code remain byte-identical.
6. 003/004: preserve existing data, dirty work and private recovery backup; no commits/staging/publication/reset/clean or unrequested infrastructure.

## Files and ordered proposed changes

Create `durable.py` only. Modify `bootstrap.py` and `app.py` only. Delete nothing. Tests/dependencies/configuration remain unchanged. Normal M06 execution documentation/status updates are permitted only after approved execution and verification, not by this planning task.

1. Add idempotent additive durable migration after M04 migration: revision default1, three tables/index, foreign keys without cascading deletion (SQLite default NO ACTION); no historical enqueue, payload rewrite, dropped old column or media operation. Execute durable DDL/revision addition in one immediate transaction; failures roll back.
2. Add independent short-lived SQLite connections/transactions for job reads and writes. Persist pending job in intake's same report/media/event transaction. Store original201 pending response with the job and principal-scoped key/fingerprint; canonical singular/plural evidence aliases and ordered IDs share fingerprint, unknown fields ignored. Replay authenticates first via existing middleware and returns the exact original response without attachment reuse/new job. Blank/nonprintable/oversize key400; changed normalized request409. Unkeyed requests retain attachment conflicts. This scope introduces create-only replay, not later route replay policies.
3. Claim atomically under `BEGIN IMMEDIATE`; increment count and persist unique ownership/attempt before dispatch. Check current evidence revision, readiness and count<3. Finish only matching running ownership/number; history records obsolete/duplicate completions. Accepted advisory projection changes only durable rows, never report/media/events/points. Store only outcome/recommendation from the trusted validated seam; full assessment/provider/policy implementation remains M08.
4. Recover running attempts once at startup for the single local instance, mark INTERRUPTED/unknown billing and consume the existing count. Keep pending jobs unchanged. Classified transient/timeout/interruption schedules5/10 seconds; terminal classes fail immediately; third retryable failure becomes ATTEMPTS_EXHAUSTED with cause preserved in attempts. No fourth claim/reset. Evidence-obsolete completion is superseded/cancelled, without an effective assessment.
5. Internal implementation choices for review: SQLite connection busy timeout5 seconds, polling/wait interval0.05 seconds and one non-daemon owned worker thread; these are local scheduling mechanics, not new operator settings or latency promises. New job IDs follow contract-wide16 lowercase hex; ownership tokens and assessment IDs remain internal UUID hex values. Lifespan starts/stops the real polling worker, with independent durable connection usage and stop/join before database closure. Factory/start/yield are inside a guarded ownership scope; the DB closes even if worker construction/recovery/thread-start fails, and stop joins only a started owned thread. Queued acceptance returns its own committed pending snapshot while controlled dispatch runs on another thread. Unhandled storage failure halts the worker and is surfaced on lifecycle stop rather than forging a result. Recovery assumes the prior local process is stopped; no multi-process lease or multi-instance guarantee.
6. **Explicit M06 integration decision for review:** no provider adapter exists yet. Default factory supplies no dispatch callable. Worker records terminal PROVIDER_CONFIGURATION before claiming/dispatch, count0/no attempt/no assessment; immediate officer review remains available. This is deliberate unavailable integration, not a successful screening/default model adapter. M08 must replace this with bounded real provider integration; currently accepted configured or unconfigured work has the same truthful unavailable-adapter result. The injected004 dispatch seam is unchanged and demonstrates background execution. No key/model is read or snapshotted in M06; provider/settings/prompt/legal snapshot and Retry-After/deadline implementation stay M08 as approved004 explicitly states.
7. Add safe public summary to citizen and officer detail after existing authorization, plus pending summary on acceptance/replay. Expose generic technical failure and lifecycle/count/revision/timing, not raw exception, credentials or internal ownership token. Complete list/dashboard/attempt/usage/cost serializers and UI remain M16; this is minimum consumer technical visibility.

## Acceptance / completion criteria — Expected / Predicted, Not Yet Verified as M06

- Exactly durable.py created and app.py/bootstrap.py modified to the exact code below, with prior dirty source/tests/config/private data preserved.
- Same successful acceptance atomically commits report, ordered evidence, event and one pending job; keyed replay returns original201/job with no duplicate effects; insertion failure returns503 and consumes no upload.
- Pending recovery remains pending/count0; interrupted attempts1–3 stay consumed across fresh processes; no fourth attempt. Only eligible transient classes retry at the reviewed schedule. All technical outcomes preserve officer access/status/points/evidence/events.
- Concurrent claims have one winner; stale ownership, duplicate completion and obsolete evidence cannot publish an effective second assessment; history records superseded attempts.
- Production lifespan starts/stops the worker; adapter call observes committed count before dispatch, acceptance/officer reads finish while dispatch is blocked. Default unavailable integration produces failed/configuration/count0 with no fabricated result.
- Synthetic old-schema migration opens twice, retaining every old reports/media/events column value and media bytes, approved status/points/legacy AI payload; integrity/foreign keys pass. Historical no-job claims remain not-requested.
- Unchanged durable --green launcher: two equal14-node all-pass inventories, no errors/skips/xfails, unchanged90s bound. Unchanged preservation --intake: two equal106-node inventories,94 passes/12 existing skips, unchanged180s bound, no failure/error/new skip/timeout. No root pytest or live-provider call.
- Private full protected inventory matches originals except this plan; all owned children/containers/temp state removed after evidence archiving, prior private recovery backup retained.

## Exact code

### durable.py — complete new file

```python
"""Local durable scheduling; provider integration is deliberately deferred."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import threading
import time
from uuid import uuid4

SCHEMA = (
    "CREATE TABLE IF NOT EXISTS ai_jobs (id TEXT PRIMARY KEY, report_id TEXT NOT NULL REFERENCES reports(id), evidence_revision INTEGER NOT NULL, state TEXT NOT NULL, attempt_count INTEGER NOT NULL DEFAULT 0 CHECK(attempt_count BETWEEN 0 AND 3), next_attempt_at REAL, owner TEXT, created_at REAL NOT NULL, started_at REAL, completed_at REAL, failure_code TEXT, assessment_id TEXT, assessment TEXT, principal TEXT, idempotency_key TEXT, fingerprint TEXT, response TEXT, UNIQUE(report_id,evidence_revision), UNIQUE(principal,idempotency_key))",
    "CREATE TABLE IF NOT EXISTS ai_attempts (job_id TEXT NOT NULL REFERENCES ai_jobs(id), number INTEGER NOT NULL CHECK(number BETWEEN 1 AND 3), owner TEXT NOT NULL, state TEXT NOT NULL, started_at REAL NOT NULL, completed_at REAL, failure_code TEXT, billing_state TEXT NOT NULL, PRIMARY KEY(job_id,number))",
    "CREATE TABLE IF NOT EXISTS ai_history (sequence INTEGER PRIMARY KEY AUTOINCREMENT, job_id TEXT NOT NULL REFERENCES ai_jobs(id), kind TEXT NOT NULL, number INTEGER NOT NULL, created_at REAL NOT NULL)",
    "CREATE INDEX IF NOT EXISTS ai_jobs_ready ON ai_jobs(state,next_attempt_at)",
)
RETRYABLE = frozenset({'PROVIDER_TRANSIENT', 'ATTEMPT_TIMEOUT', 'INTERRUPTED'})
FAILURES = RETRYABLE | {'PROVIDER_CONFIGURATION', 'PROVIDER_REQUEST_REJECTED', 'INVALID_MODEL_OUTPUT', 'MODEL_OUTPUT_UNAVAILABLE', 'EVIDENCE_UNAVAILABLE', 'PROCESSING_ERROR'}


def migrate(conn: sqlite3.Connection) -> None:
    """Add only durable state; never enqueue historical reports or alter AI payloads."""
    try:
        conn.execute('BEGIN IMMEDIATE')
        if 'evidence_revision' not in {r[1] for r in conn.execute('PRAGMA table_info(reports)')}:
            conn.execute('ALTER TABLE reports ADD COLUMN evidence_revision INTEGER NOT NULL DEFAULT 1')
        for statement in SCHEMA:
            conn.execute(statement)
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def timestamp(value: float | None) -> str | None:
    return datetime.fromtimestamp(value, timezone.utc).isoformat().replace('+00:00', 'Z') if value is not None else None


class JobStore:
    def __init__(self, database_path: Path):
        self.path = Path(database_path).resolve()

    @contextmanager
    def transaction(self):
        conn = sqlite3.connect(self.path, timeout=5)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys=ON')
        try:
            conn.execute('BEGIN IMMEDIATE')
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def summary(self, report_id: str) -> dict:
        with self.transaction() as conn:
            row = conn.execute('SELECT * FROM ai_jobs WHERE report_id=? ORDER BY evidence_revision DESC LIMIT 1', (report_id,)).fetchone()
            result = dict(job_id=None, state='not-requested', outcome=None, recommendation=None, attempt_count=0, max_attempts=3, failure_code=None, failure_reason=None, next_attempt_at=None, started_at=None, completed_at=None, processing_ms=None, assessment_id=None, evidence_revision=None, late_result=False, attempts=[])
            if row is None:
                return result
            attempts = [dict(a) for a in conn.execute('SELECT number,state,started_at,completed_at,failure_code,billing_state FROM ai_attempts WHERE job_id=? ORDER BY number', (row['id'],))]
            result.update({key: row[key] for key in ('state','attempt_count','failure_code','next_attempt_at','started_at','completed_at','assessment_id','evidence_revision')})
            result['job_id'] = row['id']
            result['attempts'] = attempts
            if row['failure_code']:
                result['failure_reason'] = 'AI processing unavailable; an officer can still review'
            finished = [a for a in attempts if a['completed_at'] is not None]
            if finished:
                result['processing_ms'] = sum(max(0, int((a['completed_at'] - a['started_at']) * 1000)) for a in finished)
            if row['assessment']:
                result.update(json.loads(row['assessment']))
            return result

    def public_summary(self, report_id: str) -> dict:
        result = self.summary(report_id)
        result.pop('attempts')
        for key in ('started_at', 'completed_at', 'next_attempt_at'):
            result[key] = timestamp(result[key])
        return result

    def claim(self, job_id: str, owner: str, now: float) -> dict | None:
        with self.transaction() as conn:
            row = conn.execute('SELECT j.*,r.evidence_revision AS current_revision FROM ai_jobs j JOIN reports r ON r.id=j.report_id WHERE j.id=?', (job_id,)).fetchone()
            if row is None or row['state'] not in ('pending','retry-wait') or row['attempt_count'] >= 3 or row['evidence_revision'] != row['current_revision'] or (row['next_attempt_at'] is not None and row['next_attempt_at'] > now):
                return None
            number, identity = row['attempt_count'] + 1, uuid4().hex
            conn.execute("UPDATE ai_jobs SET state='running',attempt_count=?,owner=?,next_attempt_at=NULL,started_at=COALESCE(started_at,?) WHERE id=?", (number,identity,now,job_id))
            conn.execute("INSERT INTO ai_attempts VALUES(?,?,?,'running',?,NULL,NULL,'unknown')", (job_id,number,identity,now))
            return dict(job_id=job_id,number=number,owner=identity,evidence_revision=row['evidence_revision'])

    @staticmethod
    def owns(conn, token: dict):
        return conn.execute("SELECT j.*,r.evidence_revision AS current_revision FROM ai_jobs j JOIN reports r ON r.id=j.report_id WHERE j.id=? AND j.owner=? AND j.attempt_count=? AND j.state='running'", (token['job_id'],token['owner'],token['number'])).fetchone()

    @staticmethod
    def finish_failure(conn, row, code: str, retryable: bool, now: float, billing: str) -> None:
        retry = retryable and code in RETRYABLE and row['attempt_count'] < 3
        exhausted = retryable and code in RETRYABLE and row['attempt_count'] == 3
        conn.execute('UPDATE ai_attempts SET state=?,completed_at=?,failure_code=?,billing_state=? WHERE job_id=? AND number=?', ('interrupted' if code == 'INTERRUPTED' else 'failed',now,code,billing,row['id'],row['attempt_count']))
        conn.execute('UPDATE ai_jobs SET state=?,owner=NULL,next_attempt_at=?,completed_at=?,failure_code=? WHERE id=?', ('retry-wait' if retry else 'failed',now + 5 * 2 ** (row['attempt_count'] - 1) if retry else None,None if retry else now,'ATTEMPTS_EXHAUSTED' if exhausted else code,row['id']))

    def fail(self, token: dict, code: str, retryable: bool, now: float) -> bool:
        if code not in FAILURES:
            code, retryable = 'PROCESSING_ERROR', False
        with self.transaction() as conn:
            row = self.owns(conn,token)
            if row is None:
                return False
            self.finish_failure(conn,row,code,retryable,now,'unknown')
            return True

    def recover(self, now: float) -> None:
        """Startup-only recovery for the approved single local instance."""
        with self.transaction() as conn:
            for row in conn.execute("SELECT * FROM ai_jobs WHERE state='running'").fetchall():
                self.finish_failure(conn,row,'INTERRUPTED',True,now,'unknown')

    def complete(self, token: dict, assessment: dict, now: float) -> str:
        with self.transaction() as conn:
            row = self.owns(conn,token)
            accepted = row is not None and row['current_revision'] == token['evidence_revision'] == row['evidence_revision']
            kind = 'accepted' if accepted else 'superseded'
            conn.execute('INSERT INTO ai_history(job_id,kind,number,created_at) VALUES(?,?,?,?)', (token['job_id'],kind,token['number'],now))
            if accepted:
                # Only an already validated advisory projection enters this seam.
                advisory = {key: assessment[key] for key in ('outcome','recommendation')}
                conn.execute("UPDATE ai_attempts SET state='succeeded',completed_at=? WHERE job_id=? AND number=?", (now,token['job_id'],token['number']))
                conn.execute("UPDATE ai_jobs SET state='completed',owner=NULL,completed_at=?,failure_code=NULL,assessment_id=?,assessment=? WHERE id=?", (now,uuid4().hex,json.dumps(advisory),token['job_id']))
            elif row is not None:
                conn.execute("UPDATE ai_attempts SET state='superseded',completed_at=? WHERE job_id=? AND number=?", (now,token['job_id'],token['number']))
                conn.execute("UPDATE ai_jobs SET state='cancelled',owner=NULL,completed_at=? WHERE id=?", (now,token['job_id']))
            return kind

    def history(self, job_id: str) -> list:
        with self.transaction() as conn:
            return [dict(row) for row in conn.execute('SELECT * FROM ai_history WHERE job_id=? ORDER BY sequence', (job_id,))]

    def ready(self, now: float) -> list:
        with self.transaction() as conn:
            return [row[0] for row in conn.execute("SELECT id FROM ai_jobs WHERE state IN ('pending','retry-wait') AND (next_attempt_at IS NULL OR next_attempt_at<=?) ORDER BY created_at,id", (now,))]

    def unavailable(self, job_id: str, now: float) -> None:
        """No adapter yet: terminal, truthful pre-dispatch configuration failure."""
        with self.transaction() as conn:
            conn.execute("UPDATE ai_jobs SET state='failed',failure_code='PROVIDER_CONFIGURATION',completed_at=?,next_attempt_at=NULL WHERE id=? AND state IN ('pending','retry-wait')", (now,job_id))


class Worker:
    def __init__(self, store: JobStore, dispatch=None, clock=time.time):
        self.store, self.dispatch, self.clock = store, dispatch, clock
        self.stopping = threading.Event()
        self.condition = threading.Condition()
        self.active = False
        self.thread = None
        self.error = None

    def start(self) -> None:
        self.store.recover(self.clock())
        self.thread = threading.Thread(target=self.run, name='roadwatch-ai-worker', daemon=False)
        self.thread.start()

    def run(self) -> None:
        try:
            while not self.stopping.is_set():
                for job_id in self.store.ready(self.clock()):
                    if self.stopping.is_set():
                        break
                    with self.condition:
                        self.active = True
                    try:
                        if self.dispatch is None:
                            self.store.unavailable(job_id,self.clock())
                            continue
                        token = self.store.claim(job_id,'local-worker',self.clock())
                        if token is None:
                            continue
                        try:
                            assessment = self.dispatch(token)
                        except Exception:
                            self.store.fail(token,'PROCESSING_ERROR',False,self.clock())
                        else:
                            self.store.complete(token,assessment,self.clock())
                    finally:
                        with self.condition:
                            self.active = False
                            self.condition.notify_all()
                self.stopping.wait(0.05)
        except Exception as error:
            self.error = error
        finally:
            with self.condition:
                self.condition.notify_all()

    def wait_idle(self, timeout: float) -> bool:
        deadline = time.monotonic() + timeout
        with self.condition:
            while self.active or self.store.ready(self.clock()):
                remaining = deadline - time.monotonic()
                if remaining <= 0 or self.error is not None:
                    return False
                self.condition.wait(min(remaining,0.05))
            return self.error is None

    def stop(self) -> None:
        self.stopping.set()
        if self.thread is not None and self.thread.ident is not None:
            self.thread.join()
        if self.error is not None:
            raise RuntimeError('AI worker storage unavailable') from self.error


def ai_worker_factory(database_path: Path) -> Worker:
    return Worker(JobStore(database_path))
```

### bootstrap.py — complete unified diff

```diff
--- a/bootstrap.py
+++ b/bootstrap.py
@@ -37,6 +37,8 @@
         # Create schema if not exists
         self._init_schema()
         self._migrate_intake()
+        from durable import migrate
+        migrate(self.connection)
     
     def _init_schema(self):
         """Create all tables if they don't exist."""
```

### app.py — complete unified diff

```diff
--- a/app.py
+++ b/app.py
@@ -9,6 +9,9 @@
 - Swagger UI at /api/docs
 """
 
+from durable import JobStore, ai_worker_factory
+import time
+import sqlite3
 from contextlib import asynccontextmanager
 from datetime import datetime, timezone
 import hashlib
@@ -130,7 +133,17 @@
     except Exception as e:
         logger.warning(f"OpenTelemetry initialization skipped: {e}")
     
-    yield  # App runs here
+    worker = None
+    try:
+        worker = ai_worker_factory(db.db_path.resolve())
+        worker.start()
+        yield  # App runs here
+    finally:
+        try:
+            if worker is not None:
+                worker.stop()
+        finally:
+            db.close()
     
     # Shutdown
     logger.info("🛑 LIFESPAN SHUTDOWN: Shutting down RoadWatch Traffic MVP...")
@@ -699,11 +712,24 @@
     if not isinstance(ids, list) or not ids or any(not isinstance(i, str) or not i.strip() for i in ids) or len(set(ids)) != len(ids):
         fail(400, 'INVALID_INPUT', 'Expected distinct media handles')
     citizen = request.scope['citizen_id']
+    key = request.headers.get('Idempotency-Key')
+    if key is not None and (not 1 <= len(key) <= 128 or any(ord(c) < 32 or ord(c) > 126 for c in key) or not key.strip()):
+        fail(400, 'INVALID_INPUT', 'Invalid idempotency key')
+    fingerprint = json.dumps([body['violation_type'],body['vehicle_number'],body['location'],ids], separators=(',',':'), ensure_ascii=True)
     report_id, now = uuid4().hex[:16], get_utc_now_iso()
+    job_id = uuid4().hex[:16]
+    response = {'report_id':report_id,'status':'awaiting-review','violation_type':body['violation_type'],'created_at':now,'citizen_id':citizen,
+                'ai':dict(job_id=job_id,state='pending',outcome=None,recommendation=None,attempt_count=0,max_attempts=3,failure_code=None,failure_reason=None,next_attempt_at=None,started_at=None,completed_at=None,processing_ms=None,assessment_id=None,evidence_revision=1,late_result=False)}
     db = get_db()
     try:
         with db.transaction() as conn:
             conn.execute('BEGIN IMMEDIATE')
+            if key is not None:
+                replay = conn.execute('SELECT fingerprint,response FROM ai_jobs WHERE principal=? AND idempotency_key=?', (citizen,key)).fetchone()
+                if replay is not None:
+                    if replay['fingerprint'] != fingerprint:
+                        fail(409, 'IDEMPOTENCY_CONFLICT', 'Idempotency key was already used')
+                    return JSONResponse(status_code=201,content=json.loads(replay['response']))
             for media_id in ids:
                 media = conn.execute('SELECT * FROM media WHERE id=?', (media_id,)).fetchone()
                 if not media: fail(404, 'MEDIA_NOT_FOUND', 'Media not found')
@@ -720,12 +746,15 @@
                 conn.execute('UPDATE media SET report_id=?,attachment_position=? WHERE id=?', (report_id,position,media_id))
             conn.execute('INSERT INTO events(id,report_id,event_type,actor,old_status,new_status,created_at,reason) VALUES(?,?,?,?,?,?,?,?)',
                          (uuid4().hex[:16],report_id,'status_change','citizen',None,'awaiting-review',now,None))
+            conn.execute("INSERT INTO ai_jobs(id,report_id,evidence_revision,state,created_at,principal,idempotency_key,fingerprint,response) VALUES(?,?,1,'pending',?,?,?,?,?)",
+                         (job_id,report_id,time.time(),citizen,key,fingerprint,json.dumps(response)))
     except IntakeError:
         raise
+    except sqlite3.Error:
+        fail(503, 'STORAGE_UNAVAILABLE', 'Report storage unavailable')
     except Exception:
         fail(500, 'INTERNAL_ERROR', 'Unable to submit report')
-    return JSONResponse(status_code=201, content={'report_id':report_id,'status':'awaiting-review',
-                        'violation_type':body['violation_type'],'created_at':now,'citizen_id':citizen})
+    return JSONResponse(status_code=201, content=response)
 
 @app.get("/api/reports", tags=["Citizen"])
 async def fetch_reports(request: Request, page: int = 1, page_size: int = 20):
@@ -814,6 +843,7 @@
         result = dict(report)
         result["timeline"] = timeline
         result["media"] = media_urls
+        result["ai"] = JobStore(db.db_path).public_summary(report_id)
         
         return JSONResponse(content=result)
     except Exception as e:
@@ -1012,6 +1042,7 @@
         media = [media_view(m, report_id, token_for_media) for m in media_list]
 
         report_dict['media'] = media
+        report_dict['ai'] = JobStore(db.db_path).public_summary(report_id)
         
         return JSONResponse(content=report_dict)
     except Exception as e:
```

## Verification and deployment/recovery ordering

After human approval, preserve current source preimages and a coherent SQLite backup plus corresponding media tree while the local instance is stopped, following M04's approved read-only-source SQLite backup procedure. Do not use a raw copy of only the main WAL database. Retain the prior private recovery backup. Stop if another active local instance or materially different schema is found. Apply only the exact three production changes; parse and mechanically compare them with this artifact. Verification uses source-only disposable copies and synthetic state; it never exercises the live DB. Startup migration is additive and repeatable, but real migration waits for deliberate local startup after these checks. No deployment or startup is authorized merely by approval to execute source changes.

Run the carried003 setup block with literal owned area changed to `asor-m06-execution-20261109-d9f18a71`, absent-before-create. It copies root Python, pytest.ini, tests/templates/static only and creates real-decoder forwarding wrappers. Use that disposable repository as the explicit tool working directory, expanded native Windows loopback execution, unchanged installed venv, and this exact run sequence (each launcher internally repeats without cleaning between its runs):

```powershell
$document=Get-Content -Raw -LiteralPath 'docs/.ai/ai-screening-officer-review/003_Implementation_Plan_Evidence_Intake_GREEN.md'
$blocks=[regex]::Matches($document,'(?s)~~~powershell\r?\n(.*?)\r?\n~~~')
if($blocks.Count -ne 3){throw 'Approved setup block inventory changed'}
$setup=$blocks[0].Groups[1].Value.Replace('asor-m04-execution-20261109-b4e82c10','asor-m06-execution-20261109-d9f18a71')
Invoke-Expression $setup
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m06-execution-20261109-d9f18a71'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_durable_processing.py" --green *> "$taskRoot\green.log"
if($LASTEXITCODE -ne 0){throw 'Durable verification failed; preserve evidence and stop'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\intake.log"
if($LASTEXITCODE -ne 0){throw 'Preservation failed; preserve evidence and stop'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\check_integrity.py"
if($LASTEXITCODE -ne 0){throw 'Protected inventory differs'}
```

Expected evidence is the exact criteria above, not simply launcher exit0. Archive trimmed real outputs, node/status inventory equality, effective path/closed lifecycle assertions, independent full protected source/data comparison and owned cleanup. Existing M05 first node contains the synthetic pre-durable-schema migration round-trip; no production data or added test is needed. Its migration assertions cover compatibility of inspected schema only, not arbitrary custom schemas. Default no-adapter behavior is additionally inspected/probed only in disposable synthetic state; this does not introduce a checkout test.

Rollback before live startup: restore only app.py/bootstrap.py exact preimages and remove only the newly added durable.py after verifying it still matches this artifact. Never overwrite unrelated later edits. After migration, stop the local instance before recovery. Additive tables/column can remain for older source because old queries name their columns; retain durable state to avoid resetting consumed attempts. If restoring data is necessary, use the coherent predeployment SQLite backup and corresponding media tree together, explicitly reconciling any subsequently accepted work first; do not discard newly committed reports or reset counters by restoring an older database casually. No rollback/migration-down deletion is proposed.

## Pre-authorized contingencies

None. Any additional executable file, dependency/configuration change, weakened assertion, timeout extension, provider adapter or materially different schema returns to planning. Routine shell quoting/path correction is permitted only outside source and must be recorded truthfully; no retry-until-pass.

## Risks, verification gaps and explicit exclusions

The inherited request handlers still use synchronous local SQLite and one shared handler connection; M06 does not redesign that baseline. Durable independent transactions are serialized, bounded by existing SQLite timeout5s; a busy/unavailable intake storage operation returns503 rather than accepting memory-only work. Same local-instance restart recovery requires the prior worker process to be stopped. Worker shutdown joins an active injected dispatch; the004 seam assumes dispatch returns, and M08 must impose provider absolute deadlines/cancellation before real provider work is added. M06 does not claim provider exactly-once billing, multiple workers/processes safety, full execution-setting snapshots, configured Retry-After handling or enforced120-second provider timeout.

M05 directly proves the14 named storage/lifecycle behaviors, including synthetic legacy compatibility, default5/10 delays and consumed counts. It does not assert changed-key normalization/ASCII errors, default no-adapter count0, public timestamp formatting, all detail summary fields, unknown failure-code safety or arbitrary process shutdown during DDL. Those are exact code review/scratch observations, not retroactively claimed M05 coverage. Consumer summary uses no raw provider/exception data and does not invent usage/cost. Full provider failure classification/validated assessment/legal rules remain M07/M08; officer finalization cancellation/late-result policy remains M09/M10; refresh/counts/UI M11/M12; resubmission/manual review M13/M14; complete attempt/usage/cost presentation M15/M16; live validation M17.

Exclude tests, dependency/config/CI/Docker changes, Gemini/legal/AI decision integration, auto rejection/awards, officer-action policy fixes, browser changes, real migration/private-data reuse, broad refactor, commit/stage/publication and the next milestone.

## Planning-time dry run — not milestone execution evidence

The exact proposed code ran in the newly created owned host-visible source-only area `C:\Users\avina\AppData\Local\Temp\asor-m06-plan-20261109-d9f18a71`. The carried003 setup block was mechanically extracted, changing only that literal directory. All runs were sequential against frozen copied production bytes; no source/test/config edits occurred while a launcher ran. Provider/bootstrap environment stripping, real schema/runtime guards, UTF-8/no-bytecode and child bounds were unchanged. Decoder forwarding passes actual temporary media bytes to the existing carrier, `--network none --rm`, with no historical application import or native installation claim.

Before final freeze, main review found two code gaps outside M05 assertions: a32-character proposed job ID violated the explicit16-hex contract, and worker.start before the ownership try/finally leaked the initialized DB on startup failure. Corrected exact production proposals only; tests/bounds were not weakened. The earlier frozen draft passed14/14 twice (19.24s/18.44s) and94/12 twice (109.34s/150.76s), with guards, but those results are historical and do not verify this corrected revision. Both original launchers completed before any correction; the revised exact source is verified anew below.

Actual commands were the verification block above with `asor-m06-plan-20261109-d9f18a71` substituted for the execution area, explicit disposable repository cwd, and separate stdout/stderr logs. The historical durable command completed first. Historical pre-review output (superseded):

```text
green run 1 exit 0
14 passed, 1 warning in 19.24s
Classified 14 green nodes; no errors/skips
green run 2 exit 0
14 passed, 1 warning in 18.44s
Classified 14 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
```

Preservation results, exact-code mechanical reapplication, final private comparison and cleanup are recorded below after completion; they are not predicted or counted as passing prematurely.

Final corrected-revision launcher sequence exited0. Actual trimmed output:

```text
green run 1 exit 0
14 passed, 1 warning in 17.32s
Classified 14 green nodes; no errors/skips
green run 2 exit 0
14 passed, 1 warning in 15.74s
Classified 14 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
intake run 1 result: 0
94 passed, 12 skipped, 1 warning in 122.13s (0:02:02)
intake run 2 result: 0
94 passed, 12 skipped, 1 warning in 123.68s (0:02:03)
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
Independent inventories:14 equal durable nodes;106 equal preservation nodes94/12
```

The first unchanged durable node built the synthetic pre-durable schema (dropped only synthetic durable tables/revision), preserved historical AI text/status and approved17-point report, opened through proposed bootstrap twice in fresh processes, and checked old column values, media bytes, integrity and foreign keys. Both final runs passed this assertion. No real migration or backup-content reuse occurred.

The exact artifact was independently reapplied to a fresh owned `mechanical` source-only copy by extracting its complete new-file block and mechanically applying every unified-diff hunk against actual checkout source. All three resulting files matched the frozen verification proposal and parsed. No tests or configuration were modified. Actual auxiliary invocations (native copied working directory, UTF-8/no-bytecode; provider/bootstrap environment stripped for probe):

```powershell
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' 'C:\Users\avina\AppData\Local\Temp\asor-m06-plan-20261109-d9f18a71\verify_artifact.py'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' 'C:\Users\avina\AppData\Local\Temp\asor-m06-plan-20261109-d9f18a71\probe.py'
```

Both exited0. Actual trimmed output:

```text
app.py: artifact complete code mechanically applies, matches frozen source, parses
bootstrap.py: artifact complete code mechanically applies, matches frozen source, parses
durable.py: artifact complete code mechanically applies, matches frozen source, parses
All checkout and frozen test Python bytes match; no test changes
Synthetic default: terminal PROVIDER_CONFIGURATION, zero attempts, no assessment; UTC public completion
Synthetic factory/start failures close initialized DB; only created owned worker stopped
```

These two narrow probes are disposable review checks, not new repository tests or claimed M05 coverage. The default probe initialized synthetic schema/report/job through proposed production bootstrap, ran real default Worker, and asserted failed/configuration/count0/no attempts/no assessment. Startup probe ran copied real app/TestClient lifespan twice: factory failure and owned worker.start failure; both propagated the synthetic error and left the actual initialized shared DB closed, while only the created worker received stop. Real-time default uses `time.time`; numeric1000 clocks are injected only by approved004 deterministic tests.

No verification invocation failed or timed out. The initial read of absent root AGENTS.md printed file-not-found and had no mutation/runtime effect; ancestor/repository inspection confirmed no applicable AGENTS.md. The pre-review code gaps and superseded successful evidence above are retained truthfully, rather than implying the initial tests proved the missing ID/startup rules.

## Exact-code self-check

| File | Final check |
| --- | --- |
| durable.py | Complete new content extracted, parsed and byte-equivalent as text to frozen tested source; no pseudocode/placeholders. Schema/transactions/recovery/claims/outcomes/history/worker/default behavior map to proposed changes1/3/4/5/6. Internal timeout/polling/thread choices explicitly listed; no dependency or operator setting introduced. |
| bootstrap.py | Complete unified diff applied mechanically; sole change calls additive durable migration after preserved M04 migration. Parsed/matched frozen source, compatibility exercised by unchanged M05 node in both final runs. |
| app.py | Complete unified diff applied mechanically and parsed/matched frozen source; approved factory ownership,16-hex job IDs, atomic create/replay/storage503 and authorized detail summaries map to proposed changes2/5/7. Original auth/media/points/officer decisions preserved. |

No code-only dependency/configuration setting, test change or Proposed Changes item without exact code remains. No approval or Plan execution status was changed.

## Protected-state and owned cleanup evidence

Independent full private comparison matched all176 original absolute paths/lengths/SHA-256 values, including original dirty source/tests/configuration, real DB/media/private-local and existing work-item artifacts. The only added checkout path was005. The carried non-Markdown integrity helper also passed. Full private metadata was never published; no real content entered scratch. The previously retained coherent recovery backup remains untouched.

Created only the owned literal planning area, its `repository`, `temporary`, `bin`, `mechanical`, `probes` directories, synthetic DB/media, real-decoder wrappers, private metadata inventories, setup/proposal/correction/document-writing/mechanical-check/probe/final-comparison scripts and logs. Relevant exact source, commands and truthful trimmed evidence are archived in this artifact; disposable copies/metadata/log originals were removed. No recovery backup was deleted.

Expanded final inspection found0 owned verification Python/uvicorn/decoder processes and empty `docker ps --format '{{.ID}} {{.Image}}'` output. No process/container stop was needed. An initial cleanup guard compared the owned area's parent with `[IO.Path]::GetTempPath().TrimEnd('\')` and failed with `Ownership/path check failed`; it deleted nothing. The corrected guard used the explicitly intended literal parent, without changing the deletion target:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m06-plan-20261109-d9f18a71'
$expectedParent='C:\Users\avina\AppData\Local\Temp'
$resolved=(Resolve-Path -LiteralPath $taskRoot).Path
if($resolved -ne $taskRoot -or (Split-Path -Parent $resolved) -ne $expectedParent -or (Split-Path -Leaf $resolved) -ne 'asor-m06-plan-20261109-d9f18a71'){throw 'Literal ownership/path check failed'}
Remove-Item -LiteralPath $resolved -Recurse -Force
if(Test-Path -LiteralPath $taskRoot){throw 'Owned disposable area remains'}
```

Actual exit0: `Verified owned planning area removed and independently absent`. No global Temp cleanup, unknown service stop, live application start, data migration, Plan status/approval change, commit/staging/publication or next-milestone work occurred.

## Human Review

Executed on 2026-11-09 following user approval on 2026-11-09 for ASOR-M06 Durable processing GREEN only. See [Plan execution status](Plan.md#execution-status) and [execution evidence](ASOR-M06-Execution-2026-11-09.md): exact three production files, unchanged durable14-pass and preservation94-pass/12-existing-skip pairs with equal inventories, synthetic default/startup probes, original protected data/dirty work and owned cleanup verified. Real migration/startup is deferred; private recovery backups retained. M07 remains Pending and unauthorized.
