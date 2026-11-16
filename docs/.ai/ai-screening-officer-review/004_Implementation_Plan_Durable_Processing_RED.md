# Implementation Plan — Durable Processing RED

## Milestone and boundary

ASOR-M05 — Durable processing RED, work item `ai-screening-officer-review`. Prepared 2026-11-09, America/Chicago. Type **RED**, predecessor **ASOR-M04 completed**. M05 remains Pending. This artifact proposes tests/checks only. Planning-time scratch executions below are not milestone execution or approval, and do not authorize M06.

## Authoritative References

- [requirements.md](requirements.md), approved by user 2026-11-08: R15/R16 and AC09, with C04 compatibility/duplicate concerns delegated by Plan. R17 human-final policy remains M09/M10.
- [Plan.md](Plan.md), approved 2026-11-08: M05 scope/type/Pending row; M06 delivery owner; requirement/concern traceability, verification, exclusions and current execution evidence. No prior approved unexecuted M05 plan exists.
- [External-Contract.md](External-Contract.md), approved M01 by user 2026-11-08: CT02/04 pending acceptance and atomic durable job, CT15 recovery/attempt/technical/duplicate/stale semantics, relevant CT16 scheduling defaults and Contract-Wide Rules. Public formatting, provider classification and human-final mutation policies retain their assigned later milestones.
- [001 approved M02 plan](001_Implementation_Plan_Safe_Verification_Harness_OTHER.md), [002 approved M03 plan](002_Implementation_Plan_Evidence_Intake_RED.md), [003 approved M04 plan](003_Implementation_Plan_Evidence_Intake_GREEN.md): all predecessor decisions retained. Their Human Review sections record user approval/execution on 2026-11-09.
- [M02 evidence](ASOR-M02-Execution-2026-11-09.md), [M03 evidence](ASOR-M03-Execution-2026-11-09.md), [M04 evidence](ASOR-M04-Execution-2026-11-09.md): M04 exact three production files, unchanged M03 checks and94/12 matching inventories twice; synthetic legacy migration twice; retained private coherent recovery backup; real DB was not migrated.
- `.github/copilot-instructions.md` inspected; its footer is Awaiting approval and historical dependency/context claims are not factual authority. Its relevant PDD no-executable-change-before-approval boundary is consistent with this plan. No AGENTS.md was found in the repository; product-level `docs/requirements.md` remains absent.
- Current-state evidence inspected: app.py intake/lifespan/officer-read paths; bootstrap.py schema/transactions/M04 migration; intake.py; tests/conftest.py, test_evidence_intake.py, verify_current_demo.py and selected preserved tests; pytest.ini/requirements.txt. Planning rules read: PDD, implementation-planning, testing, distributed-systems, resilience-and-degradation skills. These are process guidance, not new requirements.

## Actual baseline and predecessor preservation

The working tree is **dirty**, as expected: modified app.py/bootstrap.py/tests/conftest.py/tests/test_api_endpoints.py/tests/test_auth.py; untracked intake.py, current work-item docs, test_evidence_intake.py/test_verification_harness.py/verify_current_demo.py. Preserve all of it. No checkout test/lifespan, live Gemini request, real data migration, or backup modification occurred. A private full path/length/SHA inventory was captured before scratch work and independently matched after verification. No real database/media/.local/.env/.git/.venv content was copied into verification inputs.

`submit_report` currently atomically commits report, ordered media attachment and initial event, then returns201 awaiting-review without an AI summary or job. Lifespan initializes SQLite only; there is no durable module, worker scheduling, jobs, attempts or recovery. Missing production Python imports are not used as RED: every node first proves real accepted intake, then asserts the required pending AI snapshot in its test body. On this actual baseline all14 nodes fail that behavior assertion before any future module import. After that gate, the scratch-only probe reached and passed every downstream assertion.

Frozen preservation verification:94 passed/12 existing skips twice, identical106-node inventories, unchanged guards, using M04's exact existing180-second intake child bound and offline real-decoder forwarding. Seven old API bodies remain setup-only;12 old media skips provide no coverage. Historical controls/OIDC infrastructure tests remain unrun, unchanged. The Starlette/httpx deprecation warning persists. This is the selected current-demo suite, not an all-repository pass.

## Carried-Forward Decisions

1. M02's actual production schema/lifespan fixture; function-scoped UUID runtime under owned pytest temporary state; asserted effective database/media paths and connection closure. No handwritten substitute app/schema or global fixture rewrite.
2. M02/M03's existing pytest/pytest-asyncio, explicit `-p pytest_asyncio.plugin`, `-v`, plugin autoload disabled, UTF-8/no-bytecode, provider/bootstrap environment stripping, owned TMP/TEMP/TMPDIR and allowlisted source-only nested copies. No dependency/configuration version change.
3. M03 real HTTP transport for status/error contracts, real JPEG bytes, owned attachment flow and source guards. No live provider/model-quality test.
4. M04's unchanged full six-module preservation selection and180-second intake bound. Native Windows FFmpeg/FFprobe remain absent; use only the approved scratch forwarding through existing `traffic-60e6e567315a-runner:latest`, actual bytes through stdin, `--network none --rm`. This installs nothing, mocks no decoder and adds no production Docker requirement. The native deployment prerequisite remains outstanding.
5. Keep M04's retained private recovery backup/preimages intact. Source-copy verification never uses them or real data. Do not reset/clean/stage/commit/publish.

## Exact scope and proposed changes

Files to create after approval only:

- `tests/test_durable_processing.py`:14 runnable behavioral nodes and local helpers, using the existing unchanged runtime_factory.
- `tests/verify_durable_processing.py`: standard-library safe launcher and exact JUnit/node/failure classifier, with separate `--red` and future verification `--green` modes.

Files to modify/delete: **none**. Existing tests/verify_current_demo.py and its historical --intake-red classification stay byte-identical. No app/bootstrap/durable module, schema/config/dependency or other test file is authorized in M05. The milestone's eventual status/evidence update is the ordinary PDD exception after actual approved execution, never performed by this planning task.

Ordered changes: create the exact test file below; create the exact helper below; parse the two files; run the unchanged preservation entry point, then the new `--red` entry point in owned source copies; require both repeated inventories and all guards; archive evidence; remove only owned verification state. Stop after M05 execution; M06 needs its own reviewed plan.

## Explicit implementation/test decisions for review

These internal seams are proposed for approval here because M06 must satisfy the RED tests. They are not production changes in M05, public HTTP additions beyond M01, or claims of existing symbols.

| Decision | Exact proposed boundary and alternative |
| --- | --- |
| Durable local state | SQLite in the same database as accepted reports; reviewed names `ai_jobs`, `ai_attempts`, `ai_history`, and `reports.evidence_revision`. Tests directly require `ai_jobs.id/attempt_count`; other fields are accessed through the seam. Three table names also identify the synthetic pre-durable fixture. Alternative external broker/new service is unnecessary for the approved single local instance and would add dependencies. |
| Worker scheduling seam | `app.ai_worker_factory(database_path)` produces an object with `start()` and `stop()`; production lifespan owns both. Tests override/restore this factory before lifespan. PausedWorker suspends scheduling only for deterministic storage tests; it never supplies job/result behavior. The background node supplies the real durable.Worker and a blocked controlled adapter, proving lifespan scheduling and acceptance independent of dispatch completion. Alternative environment test-disable flags would add production config and are not proposed. |
| Store seam | `durable.JobStore(database_path: Path)` with `summary(report_id)`, `claim(job_id, owner, now) -> token|None`, `recover(now)`, `fail(token, code, retryable, now) -> bool`, `complete(token, assessment, now) -> accepted|superseded`, `history(job_id) -> records`. `summary` is an internal projection containing tested lifecycle/attempt fields, not the complete HTTP serializer. `next_attempt_at` in this internal seam is numeric seconds on the supplied clock; M01 HTTP UTC timestamp formatting remains unchanged. Tokens expose job_id, number and revision-bound ownership. Store methods commit before returning. |
| Adapter/worker seam | `durable.Worker(store, dispatch, clock)` with start/stop and `wait_idle(timeout) -> bool`. dispatch(token) is an already validated advisory-result adapter boundary; the controlled test returns uncertain/needs-human-judgment. It is not Gemini output validation. Tests do not request a provider SDK, prompt, law catalog or automatic rejection policy. |
| Failure boundary | fail receives an already classified technical code and retryable flag. The matrix checks durable handling, not future Gemini HTTP-to-code classification. Default retry delays5/10 seconds are supplied by CT16; deterministic numeric clock values avoid wall-clock waiting. Interrupted consumed attempts and unknown billing are tested across actual fresh Python processes. |
| Duplicate/stale outcomes | history records at least `kind=accepted|superseded` for completion publication attempts; no second effective result. Synthetic evidence-revision advancement isolates C04 without implementing citizen resubmit or workflow-final policy. Evidence revision is distinct from user workflow expected_revision. |
| Atomic failure | Synthetic SQLite trigger rejects an ai_jobs insert. A positive accepted report first proves work active, then real HTTP must return503 STORAGE_UNAVAILABLE with no report/event commit or consumed upload. No database function, handler, auth or response is mocked. |
| Runner/error policy | New helper requires14 exact nodes, no setup/teardown error/skip/xfail. RED accepts exit1 only when every failure contains the observed pending-behavior assertion and expected None-versus-pending comparison; GREEN requires exit0 and14 passes. Child bound90 seconds is inherited M02 non-intake containment, not a latency requirement or independent absolute watchdog. Unexpected results stop; no retry-until-pass or broadened deadlines. |

The lazy import follows a genuine observable behavior assertion, not an `importorskip`, missing-symbol assertion, fake passing stub or production scaffolding. It keeps RED runnable in Python while the full soundness probe demonstrates the later assertions execute.

## Normative traceability and ownership

| Approved rule | Verifying new node(s) and positive-before-negative proof |
| --- | --- |
| R15/CT02/04/15 durable acceptance; pending restart unchanged | pending_commit... creates real HTTP report/media/event, observes pending/count0/job ID; same-key create replays same claim/job; fresh child recovers and sees same pending count0. No provider wait. |
| C04 compatibility/idempotent migration | pending_commit... derives synthetic pre-durable schema, seeds historical AI payload/legacy approved17-point row, opens through production bootstrap twice in fresh processes, compares every old reports/media/events column and media bytes, integrity/foreign keys; legacy not-requested. |
| R15/CT15 in-flight recovery consumes interrupted attempts | interrupted_attempts... claims each attempt, independently reads persisted count before recovery, child marks INTERRUPTED/unknown billing; attempts1–3 persist, no fourth/reset. |
| R16/CT15 transient/timeout three-total bound | technical_outcomes...[PROVIDER_TRANSIENT-True], [...ATTEMPT_TIMEOUT-True], plus interrupted node: real accepted work/claimed attempt first, fail/recover/retry; early claim blocked, default5/10 schedule, exhausted after3. |
| R16/CT15 terminal technical outcomes never reject, immediate officer reads | six terminal parameter nodes and both transient nodes: active job/claim/failure first, officer detail/queue remain200 and contain report; exact report/media/events rows unchanged, points0, no fabricated success. |
| C04 concurrent duplicate/stale worker ownership | concurrent_claims... two independently connected threads race; exactly one claim wins, recovery consumes it, replacement attempt2 runs; obsolete and duplicate completions recorded superseded; exactly one accepted history publication. Positive accepted completion precedes duplicate-negative assertion. |
| C04 obsolete evidence completion | obsolete_evidence... first completes a current job successfully, creates another real job, advances synthetic evidence revision, then rejects obsolete screen-out completion as superseded without effective assessment or report/media/event mutation. |
| C04/CT04/15 atomic acceptance failure | atomic_job_failure... positive accepted job then failing insert trigger through real HTTP;503, no report/event changes, upload remains unattached. |
| R15/R16 background/nonblocking dispatch/pre-dispatch accounting | acceptance_returns... production lifespan starts real worker with controlled blocked adapter; report request returns while dispatch blocked, independent SQLite sees attempt_count1 before adapter proceeds; officer reads work immediately; released advisory completion leaves awaiting-review/points0. |

CT15 clauses outside this M05 verification slice are explicit, not silently covered: officer-finalized cancellation/no further retries/late human-final safety and workflow expected_revision race/idempotent decisions are R17/C06 M09/M10; manual-review/resubmit HTTP scheduling/revision changes are R13/R14/C08 M13/M14; Gemini dispatch/preparation deadlines, HTTP failure classification, SDK retry disabling, model/output validation and credentials/config snapshots are provider/policy M07/M08 (this plan tests only classified durable outcomes and default scheduling); full attempts/time/usage/cost serialization/sanitized logs/dashboard cards are R18/C09 M15/M16. No-job legacy and interrupted billing uncertainty are minimally asserted here without claiming accounting completion. Live Gemini and representative photo/video model quality remain M17. One effective accepted result per current job/revision and no extra job for same-key create are within C04; this plan does not implement or test all route idempotency rules.

## Acceptance / completion criteria — Expected / Predicted, not M05 evidence

- Only the two exact new test/helper files are created after approval; all earlier dirty files, dependencies/configuration, real DB/media/private-local state and recovery backup remain preserved.
- The unchanged six-module preservation launcher completes two identical106-node inventories,94 passes/12 existing skips each, no failures/errors/new skips/xfails/timeouts, under its unchanged bound.
- New launcher --red completes two identical14-node inventories: every node fails in the test body for missing committed pending AI behavior; no import/setup/teardown/transport/environment failure, skip or xfail. The helper itself exits0 only after exact classification and guards. A different missing-behavior RED class requires planning review, not casually accepting any exit1.
- Effective isolated database/media paths and closed lifecycle assertions remain active; fresh child processes read the same synthetic on-disk DB, never live state. Repeated commands run without cleaning between each pair.
- All owned children/HTTP workers/decoder containers finish, independently protected path/length/hash inventory matches except the two approved new files and normal milestone documentation, owned source/test state is removed. Archive actual commands/output and coverage limits; M05 remains separate from M06.

## Exact code — proposed repository files

### tests/test_durable_processing.py

```python
"""ASOR-M05: durable background execution, independent of model quality."""
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
import socket
import time

import httpx
import uvicorn

from PIL import Image
import pytest

OWNER = {"X-Citizen-Id": "durable-owner"}
OFFICER = {"Authorization": "Bearer durable-reviewer"}


def accepted(client, color="red", key="durable-create"):
    content = BytesIO()
    Image.new("RGB", (16, 16), color).save(content, "JPEG")
    upload = client.post("/api/media/upload", headers=OWNER,
                         files={"media_file": ("proof.jpg", content.getvalue(), "image/jpeg")})
    assert upload.status_code == 201, upload.text
    media_id = upload.json()["media_id"]
    response = client.post("/api/reports", headers={**OWNER, "Idempotency-Key": key}, json={
        "violation_type": "helmet", "vehicle_number": "KA01AB1234",
        "location": "MG Road", "media_ids": [media_id]})
    assert response.status_code == 201, response.text
    body = response.json()
    assert body.get("ai", {}).get("state") == "pending", "DURABLE_PENDING_NOT_COMMITTED"
    assert body["ai"]["attempt_count"] == 0
    assert body["ai"]["max_attempts"] == 3
    return body["report_id"], body["ai"]["job_id"], media_id


class PausedWorker:
    def start(self):
        return None

    def stop(self):
        return None


@pytest.fixture
def durable_runtime(runtime_factory, monkeypatch):
    import app as application
    monkeypatch.setenv("ROADWATCH_REVIEWER_TOKEN", "durable-reviewer")
    # Reviewed scheduling seam; store/worker behavior is never substituted.
    monkeypatch.setattr(application, "ai_worker_factory", lambda path: PausedWorker(), raising=False)
    with runtime_factory() as runtime:
        yield runtime


@pytest.fixture
def wire_runtime(durable_runtime):
    _, database, root = durable_runtime
    import app as application
    sock = socket.socket()
    sock.bind(("127.0.0.1", 0))
    sock.listen(64)
    server = uvicorn.Server(uvicorn.Config(application.app, lifespan="off", log_level="error"))
    thread = threading.Thread(target=server.run, kwargs={"sockets": [sock]}, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started and thread.is_alive() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert server.started, "Owned HTTP server did not start"
        with httpx.Client(base_url=f"http://127.0.0.1:{sock.getsockname()[1]}", timeout=20) as client:
            assert client.get("/health").status_code == 200
            yield client, database, root
    finally:
        server.should_exit = True
        thread.join(10)
        sock.close()
        assert not thread.is_alive(), "Owned HTTP server did not stop"


def store(root):
    # Deliberately after the positive HTTP behavior assertion: absence of a
    # Python production module is not the intended behavioral RED evidence.
    from durable import JobStore
    return JobStore(root / "roadwatch.db")


def child(root, operation, database_name="roadwatch.db"):
    code = ("import json; from durable import JobStore; "
            "s=JobStore(__import__('pathlib').Path(__import__('sys').argv[1])); " + operation)
    result = subprocess.run([sys.executable, "-c", code, str(root / database_name)],
                            cwd=Path(__file__).resolve().parents[1], env=os.environ.copy(),
                            text=True, capture_output=True, timeout=20)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def rows(database):
    return {name: [dict(row) for row in database.execute("SELECT * FROM " + name + " ORDER BY id")]
            for name in ("reports", "media", "events")}


def accessible(client, report_id):
    response = client.get(f"/api/authority/reports/{report_id}", headers=OFFICER)
    assert response.status_code == 200, response.text
    queue = client.get("/api/authority/reports", headers=OFFICER)
    assert queue.status_code == 200, queue.text
    assert report_id in {row["id"] for row in queue.json()["reports"]}


def test_pending_commit_survives_fresh_process_and_legacy_is_not_enqueued(durable_runtime):
    client, database, root = durable_runtime
    report_id, job_id, media_id = accepted(client)
    replay = client.post("/api/reports", headers={**OWNER, "Idempotency-Key": "durable-create"}, json={"violation_type": "helmet", "vehicle_number": "KA01AB1234", "location": "MG Road", "media_ids": [media_id]})
    assert replay.status_code == 201, replay.text
    assert (replay.json()["report_id"], replay.json()["ai"]["job_id"]) == (report_id, job_id)
    before = rows(database)
    database.execute("INSERT INTO reports(id,citizen_id,violation_type,status,created_at,updated_at,provisional_points) VALUES('legacy','old','helmet','approved','2020','2020',17)")
    database.commit()
    snapshot = child(root, f"s.recover(1000); print(json.dumps(s.summary({report_id!r})))")
    assert (snapshot["job_id"], snapshot["state"], snapshot["attempt_count"]) == (job_id, "pending", 0)
    assert child(root, "s.recover(1000); print(json.dumps(s.summary('legacy')))" )["state"] == "not-requested"
    for name, values in before.items():
        current = rows(database)[name]
        assert all(value in current for value in values)
    assert tuple(database.execute("SELECT status,provisional_points FROM reports WHERE id='legacy'").fetchone()) == ("approved", 17)
    assert database.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert not database.execute("PRAGMA foreign_key_check").fetchall()
    accessible(client, report_id)
    # Build the exact pre-durable schema from synthetic state, never live data.
    legacy_path = root / "legacy.db"
    with sqlite3.connect(legacy_path) as legacy:
        database.backup(legacy)
        for name in ("ai_history", "ai_attempts", "ai_jobs"):
            legacy.execute("DROP TABLE " + name)
        legacy.execute("ALTER TABLE reports DROP COLUMN evidence_revision")
        legacy.execute("UPDATE media SET ai_screening_result='historical AI',ai_screening_status='completed'")
        legacy.commit()
        legacy.row_factory = sqlite3.Row
        original = rows(legacy)
    media_bytes = {str(path.relative_to(root)): path.read_bytes()
                   for path in (root / "media_store").rglob("*") if path.is_file()}
    for _ in (1, 2):
        summary = child(root, "from bootstrap import DatabaseConnection; d=DatabaseConnection(s.path); d.connect(); d.close(); print(json.dumps(s.summary('legacy')))", "legacy.db")
        assert summary["state"] == "not-requested"
        with sqlite3.connect(legacy_path) as legacy:
            legacy.row_factory = sqlite3.Row
            current = rows(legacy)
            for name, old_rows in original.items():
                assert len(current[name]) == len(old_rows)
                for old, new in zip(old_rows, current[name]):
                    assert {key: new[key] for key in old} == old
            assert legacy.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            assert not legacy.execute("PRAGMA foreign_key_check").fetchall()
        assert {str(path.relative_to(root)): path.read_bytes()
                for path in (root / "media_store").rglob("*") if path.is_file()} == media_bytes


def test_interrupted_attempts_are_consumed_across_process_recovery(durable_runtime):
    client, database, root = durable_runtime
    report_id, job_id, _ = accepted(client)
    s = store(root)
    for number in (1, 2, 3):
        token = s.claim(job_id, "old-worker", 1000 + number * 100)
        assert token["number"] == number
        assert child(root, f"print(json.dumps(s.summary({report_id!r})))")["attempt_count"] == number
        snapshot = child(root, f"s.recover({1010 + number * 100}); print(json.dumps(s.summary({report_id!r})))")
        assert snapshot["attempt_count"] == number
        assert snapshot["attempts"][-1]["failure_code"] == "INTERRUPTED"
        assert snapshot["attempts"][-1]["billing_state"] == "unknown"
    final = s.summary(report_id)
    assert (final["state"], final["failure_code"], final["attempt_count"]) == ("failed", "ATTEMPTS_EXHAUSTED", 3)
    assert s.claim(job_id, "fourth", 9999) is None
    assert [a["number"] for a in final["attempts"]] == [1, 2, 3]
    assert database.execute("SELECT status,provisional_points FROM reports WHERE id=?", (report_id,)).fetchone()[:] == ("awaiting-review", 0)
    accessible(client, report_id)


@pytest.mark.parametrize("code,retryable", [
    ("PROVIDER_TRANSIENT", True), ("ATTEMPT_TIMEOUT", True),
    ("PROVIDER_CONFIGURATION", False), ("PROVIDER_REQUEST_REJECTED", False),
    ("INVALID_MODEL_OUTPUT", False), ("MODEL_OUTPUT_UNAVAILABLE", False),
    ("EVIDENCE_UNAVAILABLE", False), ("PROCESSING_ERROR", False),
])
def test_technical_outcomes_never_reject_and_retry_bound_is_durable(durable_runtime, code, retryable):
    client, database, root = durable_runtime
    report_id, job_id, media_id = accepted(client)
    replay = client.post("/api/reports", headers={**OWNER, "Idempotency-Key": "durable-create"}, json={"violation_type": "helmet", "vehicle_number": "KA01AB1234", "location": "MG Road", "media_ids": [media_id]})
    assert replay.status_code == 201, replay.text
    assert (replay.json()["report_id"], replay.json()["ai"]["job_id"]) == (report_id, job_id)
    before = rows(database)
    s = store(root)
    count = 3 if retryable else 1
    for number in range(1, count + 1):
        token = s.claim(job_id, "worker", 1000 + number * 100)
        assert token["number"] == number
        assert s.fail(token, code, retryable, 1001 + number * 100)
        snapshot = child(root, f"s.recover({1002 + number * 100}); print(json.dumps(s.summary({report_id!r})))")
        assert snapshot["attempt_count"] == number
        assert snapshot["attempts"][-1]["failure_code"] == code
        if retryable and number < 3:
            assert snapshot["state"] == "retry-wait"
            assert snapshot["next_attempt_at"] == 1001 + number * 100 + 5 * (2 ** (number - 1))
            assert s.claim(job_id, "early", 1001 + number * 100) is None
        accessible(client, report_id)
    final = s.summary(report_id)
    assert final["state"] == "failed"
    assert final["failure_code"] == ("ATTEMPTS_EXHAUSTED" if retryable else code)
    assert s.claim(job_id, "extra", 9999) is None
    assert rows(database) == before


def test_concurrent_claims_and_recovered_stale_completion_publish_once(durable_runtime):
    client, database, root = durable_runtime
    report_id, job_id, _ = accepted(client)
    s = store(root)
    before = rows(database)
    with ThreadPoolExecutor(max_workers=2) as pool:
        tokens = list(pool.map(lambda owner: store(root).claim(job_id, owner, 1000), ("a", "b")))
    winners = [token for token in tokens if token is not None]
    assert len(winners) == 1
    stale = winners[0]
    child(root, "s.recover(1001); print(json.dumps(True))")
    fresh = s.claim(job_id, "replacement", 1100)
    assert fresh["number"] == 2
    advisory = {"outcome": "uncertain", "recommendation": "needs-human-judgment"}
    assert s.complete(stale, advisory, 1101) == "superseded"
    assert s.summary(report_id)["state"] == "running"
    assert s.complete(fresh, advisory, 1102) == "accepted"
    assert s.complete(fresh, advisory, 1103) == "superseded"
    summary = child(root, f"print(json.dumps(s.summary({report_id!r})))")
    assert (summary["state"], summary["attempt_count"], summary["outcome"]) == ("completed", 2, "uncertain")
    assert len([item for item in s.history(job_id) if item["kind"] == "accepted"]) == 1
    assert len([item for item in s.history(job_id) if item["kind"] == "superseded"]) == 2
    assert rows(database) == before


def test_atomic_job_failure_does_not_accept_report_or_consume_upload(wire_runtime):
    client, database, root = wire_runtime
    accepted(client)
    s = store(root)
    before = rows(database)
    database.execute("CREATE TRIGGER reject_job BEFORE INSERT ON ai_jobs BEGIN SELECT RAISE(ABORT,'synthetic storage failure'); END")
    database.commit()
    content = BytesIO()
    Image.new("RGB", (16, 16), "blue").save(content, "JPEG")
    upload = client.post("/api/media/upload", headers=OWNER, files={"media_file": ("other.jpg", content.getvalue(), "image/jpeg")})
    assert upload.status_code == 201
    media_id = upload.json()["media_id"]
    response = client.post("/api/reports", headers={**OWNER, "Idempotency-Key": "storage-failure"}, json={"violation_type": "helmet", "vehicle_number": "KA01AB1234", "location": "MG Road", "media_ids": [media_id]})
    assert response.status_code == 503, response.text
    assert response.json()["code"] == "STORAGE_UNAVAILABLE"
    assert rows(database)["reports"] == before["reports"]
    assert rows(database)["events"] == before["events"]
    assert database.execute("SELECT report_id FROM media WHERE id=?", (media_id,)).fetchone()[0] is None


def test_acceptance_returns_during_background_dispatch_and_attempt_precedes_call(runtime_factory, monkeypatch):
    import app as application
    entered, release = threading.Event(), threading.Event()
    observations = []
    workers = []
    def factory(path):
        from durable import JobStore, Worker
        s = JobStore(path)
        def dispatch(token):
            with sqlite3.connect(path) as independent:
                observations.append(independent.execute("SELECT attempt_count FROM ai_jobs WHERE id=?", (token["job_id"],)).fetchone()[0])
            entered.set()
            assert release.wait(10), "Test did not release owned adapter"
            return {"outcome": "uncertain", "recommendation": "needs-human-judgment"}
        worker = Worker(s, dispatch, lambda: 1000)
        workers.append(worker)
        return worker
    monkeypatch.setenv("ROADWATCH_REVIEWER_TOKEN", "durable-reviewer")
    # Factory is invoked by production lifespan, not by the test.
    monkeypatch.setattr(application, "ai_worker_factory", factory, raising=False)
    try:
        with runtime_factory() as (client, database, root):
            report_id, job_id, _ = accepted(client)
            assert entered.wait(5), "BACKGROUND_DISPATCH_DID_NOT_START"
            assert observations == [1]
            assert store(root).summary(report_id)["state"] == "running"
            accessible(client, report_id)
            release.set()
            assert workers[0].wait_idle(5), "Owned worker did not finish"
            assert store(root).summary(report_id)["state"] == "completed"
            assert database.execute("SELECT status,provisional_points FROM reports WHERE id=?", (report_id,)).fetchone()[:] == ("awaiting-review", 0)
    finally:
        release.set()
        for worker in workers:
            worker.stop()


def test_obsolete_evidence_completion_is_superseded(durable_runtime):
    client, database, root = durable_runtime
    report_id, job_id, _ = accepted(client)
    s = store(root)
    positive = s.claim(job_id, "current-evidence", 900)
    assert s.complete(positive, {"outcome": "uncertain", "recommendation": "needs-human-judgment"}, 901) == "accepted"
    assert s.summary(report_id)["state"] == "completed"
    report_id, job_id, _ = accepted(client, "blue", "obsolete-evidence")
    token = s.claim(job_id, "old-evidence", 1000)
    assert token["number"] == 1
    # Synthetic revision advance isolates C04; resubmit HTTP/UI belongs to M13/M14.
    database.execute("UPDATE reports SET evidence_revision=2 WHERE id=?", (report_id,))
    database.commit()
    before = rows(database)
    assert s.complete(token, {"outcome": "irrelevant", "recommendation": "screen-out-irrelevant"}, 1001) == "superseded"
    assert s.summary(report_id)["assessment_id"] is None
    assert s.history(job_id)[-1]["kind"] == "superseded"
    assert rows(database) == before
```

### tests/verify_durable_processing.py

```python
"""ASOR-M05 safe launcher: classify exact behavioral RED, never swallow exit 1."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ["tests/test_durable_processing.py"]
EXPECTED = {
    "test_pending_commit_survives_fresh_process_and_legacy_is_not_enqueued",
    "test_interrupted_attempts_are_consumed_across_process_recovery",
    "test_concurrent_claims_and_recovered_stale_completion_publish_once",
    "test_atomic_job_failure_does_not_accept_report_or_consume_upload",
    "test_acceptance_returns_during_background_dispatch_and_attempt_precedes_call",
    "test_obsolete_evidence_completion_is_superseded",
} | {"test_technical_outcomes_never_reject_and_retry_bound_is_durable[" + code + "-" + str(retryable) + "]"
     for code, retryable in (("PROVIDER_TRANSIENT", True), ("ATTEMPT_TIMEOUT", True),
       ("PROVIDER_CONFIGURATION", False), ("PROVIDER_REQUEST_REJECTED", False),
       ("INVALID_MODEL_OUTPUT", False), ("MODEL_OUTPUT_UNAVAILABLE", False),
       ("EVIDENCE_UNAVAILABLE", False), ("PROCESSING_ERROR", False))}


def snapshot():
    paths = [p for p in ROOT.rglob("*") if p.is_file() and not any(
        x in p.relative_to(ROOT).parts for x in (".git", ".venv", "__pycache__", ".pytest_cache", ".deepeval"))]
    return {str(p.relative_to(ROOT)): (p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths}


def classify(path, mode):
    cases = ET.parse(path).findall(".//testcase")
    assert len(cases) == len(EXPECTED) == 14
    assert {case.attrib["name"] for case in cases} == EXPECTED
    inventory = []
    for case in cases:
        assert case.attrib.get("classname") == "tests.test_durable_processing"
        assert case.find("error") is None, "Setup/teardown error is not RED"
        assert case.find("skipped") is None, "No skips/xfails accepted"
        failure = case.find("failure")
        if mode == "red":
            assert failure is not None, "Unexpected passing RED node"
            detail = failure.attrib.get("message", "") + (failure.text or "")
            assert "AssertionError: DURABLE_PENDING_NOT_COMMITTED" in detail
            assert "DURABLE_PENDING_NOT_COMMITTED" in detail
            assert "assert None == 'pending'" in detail
        else:
            assert failure is None, failure.text if failure is not None else ""
        inventory.append((case.attrib["name"], "failed" if failure is not None else "passed"))
    print("Classified", len(cases), mode, "nodes; no errors/skips", flush=True)
    return sorted(inventory)


def main():
    if sys.argv[1:] not in (["--red"], ["--green"]):
        raise SystemExit("Usage: verify_durable_processing.py --red|--green")
    mode = sys.argv[1][2:]
    before = snapshot()
    temp_root = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix="asor-m05-") as name:
        scratch = Path(name).resolve()
        assert scratch.parent == temp_root and not scratch.is_relative_to(ROOT)
        copy = scratch / "repository"
        copy.mkdir()
        for source in ROOT.glob("*.py"):
            shutil.copy2(source, copy / source.name)
        shutil.copy2(ROOT / "pytest.ini", copy / "pytest.ini")
        for directory in ("tests", "templates", "static"):
            shutil.copytree(ROOT / directory, copy / directory,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.bak"))
        assert not any((copy / name).exists() for name in ("roadwatch.db", "media_store", ".local", ".env"))
        temporary = scratch / "temporary"
        temporary.mkdir()
        env = os.environ.copy()
        for key in list(env):
            if (any(word in key.upper() for word in ("GEMINI", "GOOGLE", "OPENAI", "ANTHROPIC", "OTEL_", "ROADWATCH", "DATABASE_URL", "JWT_SECRET", "OIDC_"))
                    or key.upper() in {"CONTROLS_RUNTIME", "SERVICE_ROLE", "DATABASE_DSN_FILE", "TRUST_CA_FILE", "APP_PROFILE", "AI_ADAPTER"}):
                env.pop(key)
        env.update(PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
                   TMP=str(temporary), TEMP=str(temporary), TMPDIR=str(temporary))
        previous = None
        for repeat in (1, 2):
            log = scratch / f"{mode}-{repeat}.log"
            xml = scratch / f"{mode}-{repeat}.xml"
            command = [sys.executable, "-m", "pytest", "-p", "pytest_asyncio.plugin", "-v", "--junitxml=" + str(xml), *SELECTION]
            print("Command:", repr(command), flush=True)
            with log.open("w", encoding="utf-8") as output:
                child = subprocess.Popen(command, cwd=copy, env=env, stdout=output, stderr=subprocess.STDOUT)
                try:
                    result = child.wait(timeout=90)
                except subprocess.TimeoutExpired:
                    child.kill()
                    child.wait()
                    raise AssertionError("TIMEOUT is infrastructure failure, not RED")
            assert child.poll() is not None
            print(mode, "run", repeat, "exit", result, flush=True)
            print(log.read_text(encoding="utf-8"), flush=True)
            assert result == (1 if mode == "red" else 0), "Unexpected pytest exit"
            inventory = classify(xml, mode)
            assert previous is None or inventory == previous, "Repeat inventory differs"
            previous = inventory
        assert snapshot() == before, "Protected source/state changed"
        print("Protected source/state unchanged; repeated inventories equal", flush=True)
    assert not scratch.exists()
    print("Owned disposable tree removed; children reaped", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```


## Verification protocol after approval

Apply only the two exact new files above. Retain all earlier dirty preimages. Parse both without importing app or writing bytecode. Never invoke root pytest or the real checkout lifespan. Use the current-host setup already approved in003, mechanically extracting its exact first `~~~powershell` block and changing only the owned literal execution directory. This reuses its source-only copy, independent protected inventory/check_integrity.py, actual-byte offline decoder forwarding and temp containment; it adds no dependency/configuration.

```powershell
$document=Get-Content -Raw -LiteralPath 'docs/.ai/ai-screening-officer-review/003_Implementation_Plan_Evidence_Intake_GREEN.md'
$blocks=[regex]::Matches($document,'(?s)~~~powershell\r?\n(.*?)\r?\n~~~')
if($blocks.Count -ne 3){throw 'Approved setup block inventory changed'}
$setup=$blocks[0].Groups[1].Value.Replace('asor-m04-execution-20261109-b4e82c10','asor-m05-execution-20261109-c80be291')
Invoke-Expression $setup
if($LASTEXITCODE -ne 0){throw 'Approved source-only setup failed'}
```

Use literal `C:\Users\avina\AppData\Local\Temp\asor-m05-execution-20261109-c80be291\repository` as next tool working directory, with expanded local Windows sockets (`require_escalated`). Freeze source and run sequentially:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m05-execution-20261109-c80be291'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary";$env:TEMP=$env:TMP;$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1';$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\preservation.log"
if($LASTEXITCODE -ne 0){throw 'Preservation failed; stop and preserve evidence'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_durable_processing.py" --red *> "$taskRoot\red.log"
if($LASTEXITCODE -ne 0){throw 'RED classification failed; stop and preserve evidence'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\check_integrity.py"
if($LASTEXITCODE -ne 0){throw 'Independent protected inventory mismatch'}
```

The unchanged existing helper runs the six modules in003 twice with180-second containment. The new helper prints its exact child command, explicit tests/test_durable_processing.py selection and isolated JUnit path, runs twice with90-second containment, and compares the complete14-node inventory. Neither bound is an independent absolute watchdog or product latency target. Inspect/archive all node results, not merely exit0. Independently parse preservation verbose node/status lines: require106 identical nodes,94 passed/12 existing skips each. No tolerated nonblocking failure is introduced. Existing warning,12 skips,7 setup-only API bodies and unrun historical controls/OIDC suites retain their evidence limitations.

Archive actual commands/log summaries/inventories into M05 execution evidence before cleanup or status update. Require every owned child/server/decoder finished. Inspect only matching owned Python processes; wait/reap exact known children if any remain, never stop unrelated services. Cleanup from checkout or the area's parent:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m05-execution-20261109-c80be291'
$owned=@(Get-CimInstance Win32_Process | Where-Object {$_.Name -match '^python' -and $_.CommandLine -like "*$taskRoot*"})
if($owned.Count -ne 0){throw 'Owned child remains; do not remove state'}
$resolved=(Resolve-Path -LiteralPath $taskRoot).Path
if($resolved -cne 'C:\Users\avina\AppData\Local\Temp\asor-m05-execution-20261109-c80be291'){throw 'Ownership mismatch'}
Remove-Item -LiteralPath $resolved -Recurse -Force
if(Test-Path -LiteralPath $taskRoot){throw 'Owned area remains'}
```

## Planning-time dry run — observed, not milestone execution

Owned literal area: `C:\Users\avina\AppData\Local\Temp\asor-m05-plan-20261109-d274fe81`. Created setup.py/decoder.py, private before.json, allowlisted repository/baseline/probe copies, bin forwarding wrappers, owned temporary state, proposal/diagnostic scripts and synthetic logs. No real DB/media/private backup copied. Exact proposed files were applied only in disposable copies; all pytest/app activity used copied source. Local sockets required expanded execution.

Initial invalid preservation invocation: inherited180-second wait returned TIMEOUT while its log eventually printed94 passed/12 skipped in177.30s. Concurrently adding proposal files also tripped its source-copy guard. Neither is accepted preservation/RED. The cause of scheduling overhead is not established; direct source mutation explains the hash mismatch. No bound was widened or assertion skipped. Frozen independent copies and sequential verification removed the known mutation; the required final preservation pair completed under the unchanged bound.

Initial new classifier wrongly expected a literal JUnit type attribute; observed pytest XML represents the assertion in message/text. The final classifier requires the actual assertion text, None-versus-pending comparison, exact14-node membership, no errors/skips and exit1. Initial scratch soundness run reached13 passes/1 failure: a broad edit accidentally reused a create idempotency key for a different atomic-failure request. It now uses distinct storage-failure key. The proposal was further strengthened with real HTTP503, synthetic migration and a positive accepted completion before stale-evidence rejection. These corrections happened before the final frozen checks; no existing approved test was relaxed.

### Frozen baseline preservation

Actually executed from the owned `baseline` directory, expanded local sockets:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m05-plan-20261109-d274fe81'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary";$env:TEMP=$env:TMP;$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1';$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\baseline\tests\verify_current_demo.py" --intake *> "$taskRoot\baseline-final.log"
if($LASTEXITCODE -ne 0){Get-Content "$taskRoot\baseline-final.log" -Tail 10;throw 'Frozen preservation failed'}
Select-String -LiteralPath "$taskRoot\baseline-final.log" -Pattern 'run [12] result|passed,|Protected checkout|removed'
```

Actual exit0, trimmed output:

```text
intake run 1 result: 0
94 passed, 12 skipped, 1 warning in 88.42s
intake run 2 result: 0
94 passed, 12 skipped, 1 warning in 67.31s
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
```

### Exact final RED pair

Actually executed from the owned `repository` directory, expanded local sockets:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m05-plan-20261109-d274fe81'
$env:TMP="$taskRoot\temporary";$env:TEMP=$env:TMP;$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1';$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_durable_processing.py" --red *> "$taskRoot\red-frozen.log"
if($LASTEXITCODE -ne 0){Get-Content "$taskRoot\red-frozen.log" -Tail 30;throw 'Frozen RED classification failed'}
Select-String -LiteralPath "$taskRoot\red-frozen.log" -Pattern 'run [12] exit|Classified|failed,|unchanged|removed'
```

Actual helper exit0; pytest children exit1 exactly classified:

```text
red run 1 exit 1
14 failed, 1 warning in 2.48s
Classified 14 red nodes; no errors/skips
red run 2 exit 1
14 failed, 1 warning in 2.02s
Classified 14 red nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
```

Actual representative assertion, same missing-behavior class for all14 nodes:

```text
assert body.get("ai", {}).get("state") == "pending", "DURABLE_PENDING_NOT_COMMITTED"
E AssertionError: DURABLE_PENDING_NOT_COMMITTED
E assert None == 'pending'
```

### Soundness probe pair

The owned `probe` copy alone added a SQLite job/attempt/history store, worker and minimal app/bootstrap integration. The identical final tests/helper reached and passed all downstream assertions. The probe commits attempts before dispatch, serializes claims using separate connections/BEGIN IMMEDIATE, persists consumed recovery/failure state, fences completion by token/evidence revision, records accepted/superseded outcomes and runs an actual lifespan-owned background worker with a blocked controlled adapter. No provider call.

The probe is deliberately incomplete production code: no Gemini/policy, human-final safety, complete accounting or deployment. Its scratch create replay cache only reaches the duplicate-create assertion; it is not evidence of full durable HTTP idempotency. Actual jobs/attempts/recovery use on-disk state read by fresh processes. Passing the probe proves test soundness, not M06 implementation or complete future contract coverage.

Actually executed from the owned `probe` directory, expanded local sockets:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m05-plan-20261109-d274fe81'
$env:TMP="$taskRoot\temporary";$env:TEMP=$env:TMP;$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1';$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\probe\tests\verify_durable_processing.py" --green *> "$taskRoot\probe-frozen.log"
if($LASTEXITCODE -ne 0){Get-Content "$taskRoot\probe-frozen.log" -Tail 50;throw 'Frozen probe failed'}
Select-String -LiteralPath "$taskRoot\probe-frozen.log" -Pattern 'run [12] exit|Classified|passed,|unchanged|removed'
```

Actual helper/children exit0:

```text
green run 1 exit 0
14 passed, 1 warning in 9.47s
Classified 14 green nodes; no errors/skips
green run 2 exit 0
14 passed, 1 warning in 10.04s
Classified 14 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
```

Each14-node inventory is the complete EXPECTED set in the exact helper above. Preservation inventories independently parsed as106 equal nodes. Independent standard-library check actually run from checkout, with no lifespan:

```powershell
$env:PYTHONUTF8='1';$env:PYTHONDONTWRITEBYTECODE='1'
& .\.venv\Scripts\python.exe 'C:\Users\avina\AppData\Local\Temp\asor-m05-plan-20261109-d274fe81\verify_integrity.py'
```

Actual exit0:

```text
Independent preservation inventory:106 equal nodes;94 passed/12 skipped each
Independent checkout path/length/SHA inventory unchanged, including original dirty baseline, DB/media/private-local; no live startup
Exact proposed test/helper parse and match final RED/probe copies
```

## Risks, exclusions and recovery

A common pending gate reports the earliest missing behavior in all baseline nodes, not14 independently observed downstream failure classes. The identical-code probe compensates by executing every downstream assertion. Partial GREEN will expose later assertions; do not weaken them. Direct SQLite names/internal seams bind M06 and need review here. Any material alternative returns for amended approved RED planning, not silently adapted tests in GREEN.

CT15 permits pre-dispatch evidence/configuration failure with zero attempts; this plan's failure matrix intentionally exercises classified outcomes after a consumed claim. Pre-dispatch provider/file preparation, actual absolute deadlines, SDK retry disabling, credentials/settings snapshots and HTTP failure classification belong to M07/M08; they are not proven by the injected timeout/error codes. No omission is claimed as coverage. Officer-final cancellation/late decisions and workflow expected_revision remain M09/M10; synthetic evidence revision is C04 only. Full usage/time/log/dashboard presentation remains M15/M16; interrupted unknown billing is minimally protected here. Citizen recovery/resubmit UI remains M13/M14. No live Gemini/model-quality/legal implementation, production queue, dependency/configuration change or deployment is authorized.

No pre-authorized contingency changes files or weakens evidence. Missing carrier/socket capability, timeout, unexpected failure/pass/skip/node or guard mismatch stops execution. Never widen deadlines, swallow exit1, remove a check or retry until passing. Rollback removes only the two exact newly created files if their current content still matches this plan; otherwise preserve and review. Do not reset older dirty files, restore real data, or reverse a schema. M05 changes no production/data. Retained M04 private coherent recovery backup stays untouched.

## Exact-code audit

| File | Result |
| --- | --- |
| tests/test_durable_processing.py | Complete final content; parsed; identical final RED/probe copies;14 nodes/helpers match proposed changes and traceability. Only existing dependencies plus reviewed internal seams/schema names/settings used. |
| tests/verify_durable_processing.py | Complete final content; parsed; identical final copies; exact membership/classification,90-second bound, environment flags, copies/temp/hash decisions explicitly traced. No new dependency. |

No test or production change has been applied to the checkout. The final preservation/cleanup record below completes planning only.

## Final planning preservation and cleanup

Expanded read-only process inventory found0 Python processes matching the literal owned planning area; `docker ps --format '{{.Names}}'` returned empty. A standard-library final check extracted both exact proposal blocks from this artifact, parsed them, compared them byte-for-text to the frozen final test/helper, and compared every original protected checkout path/length/SHA against the captured preimage, excluding only this newly added004 document. No original checkout file changed. No real lifespan/data/backup operation occurred.

Actual cleanup used the exact literal target and ownership check from checkout:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m05-plan-20261109-d274fe81'
$resolved=(Resolve-Path -LiteralPath $taskRoot).Path
if($resolved -cne 'C:\Users\avina\AppData\Local\Temp\asor-m05-plan-20261109-d274fe81'){throw 'Ownership mismatch'}
Remove-Item -LiteralPath $resolved -Recurse -Force
if(Test-Path -LiteralPath $taskRoot){throw 'Owned area remains'}
Write-Output 'Owned planning area absent: True'
```

Actual final exit0/output:

```text
Owned Python processes: 0
Exact two proposal blocks parse and match frozen code; only004 added; all original checkout bytes unchanged
Owned planning area absent: True
```

A documentation-append command initially failed PowerShell parsing because nested here-string delimiters collided; it wrote nothing and was replaced with a plain append. It had no test/runtime effect. Original M02/M03/M04 dirty baseline, real DB/media/private-local content and retained private recovery backup remain intact. No stage/commit/publication, Plan status change or milestone approval occurred.

## Human Review

Status: Executed on 2026-11-09 from user approval recorded2026-11-09 for ASOR-M05 Durable processing RED only. Exact two test/helper files applied and specified isolated verification completed; see [Plan execution status](Plan.md#execution-status) and [actual execution evidence](ASOR-M05-Execution-2026-11-09.md). M06 and later remain Pending and unauthorized.
