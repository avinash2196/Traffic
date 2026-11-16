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
