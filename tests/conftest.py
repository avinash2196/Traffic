"""Current-demo fixtures use the real lifespan and production SQLite schema."""
from contextlib import contextmanager
from pathlib import Path
import shutil
import sqlite3
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

REPOSITORY = Path(__file__).resolve().parents[1]


@pytest.fixture
def runtime_factory(tmp_path):
    """Create independent lifespans without touching the checkout's data."""
    @contextmanager
    def start():
        runtime = tmp_path / uuid4().hex
        runtime.mkdir()
        assert not runtime.resolve().is_relative_to(REPOSITORY)
        assert runtime.resolve().is_relative_to(tmp_path.resolve())
        for name in ("static", "templates"):
            shutil.copytree(REPOSITORY / name, runtime / name)
        with pytest.MonkeyPatch.context() as patch:
            patch.chdir(runtime)
            import bootstrap
            import app as application
            patch.setattr(bootstrap, "db_connection", None)
            with TestClient(application.app) as active:
                db = bootstrap.get_db()
                assert db is application.app.state.db
                expected = (runtime / "roadwatch.db").resolve()
                assert db.db_path.resolve() == expected
                actual = Path(db.execute("PRAGMA database_list").fetchone()[2]).resolve()
                assert actual == expected
                assert (Path.cwd() / "media_store").resolve() == runtime / "media_store"
                yield active, db.connection, runtime
            with pytest.raises(sqlite3.ProgrammingError, match="closed"):
                db.execute("SELECT 1")
    return start


@pytest.fixture
def demo_runtime(runtime_factory):
    with runtime_factory() as runtime:
        yield runtime


@pytest.fixture
def test_db(demo_runtime):
    return demo_runtime[1]


@pytest.fixture
def client(demo_runtime):
    return demo_runtime[0]


@pytest.fixture
def sample_report(test_db):
    """Create a sample report for testing.
    
    Returns dict with report_id, citizen_id, violation_type, location, status.
    Report is in 'submitted' status, created now.
    """
    report_id = uuid4().hex[:16]
    citizen_id = "citizen-" + uuid4().hex[:8]
    now = datetime.now(timezone.utc).isoformat() + "Z"
    
    test_db.execute("""
        INSERT INTO reports (id, citizen_id, violation_type, location, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (report_id, citizen_id, "helmet", "MG Road, Bangalore", "submitted", now, now))
    
    test_db.commit()
    
    return {
        "id": report_id,
        "citizen_id": citizen_id,
        "violation_type": "helmet",
        "location": "MG Road, Bangalore",
        "status": "submitted"
    }


@pytest.fixture
def sample_media(test_db, sample_report):
    """Create sample media for a report.
    
    Depends on sample_report fixture.
    Returns dict with id, report_id, filename, sha256_hash.
    """
    media_id = uuid4().hex[:16]
    uploaded_at = datetime.now(timezone.utc).isoformat() + "Z"
    sha256_hash = uuid4().hex + uuid4().hex  # 64-char hex
    
    try:
        test_db.execute("""
            INSERT INTO media (id, report_id, filename, file_size_bytes, mime_type, sha256_hash, storage_path, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            media_id,
            sample_report["id"],
            "helmet.jpg",
            1024000,
            "image/jpeg",
            sha256_hash,
            "./media_store/report_abc/media_def.jpg",
            uploaded_at
        ))
        
        test_db.commit()
    except Exception as e:
        test_db.rollback()
        # If insert fails (e.g., duplicate hash), create with a unique hash
        sha256_hash = uuid4().hex + uuid4().hex
        test_db.execute("""
            INSERT INTO media (id, report_id, filename, file_size_bytes, mime_type, sha256_hash, storage_path, uploaded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            media_id,
            sample_report["id"],
            "helmet.jpg",
            1024000,
            "image/jpeg",
            sha256_hash,
            "./media_store/report_abc/media_def.jpg",
            uploaded_at
        ))
        test_db.commit()
    
    return {
        "id": media_id,
        "report_id": sample_report["id"],
        "filename": "helmet.jpg",
        "sha256_hash": sha256_hash
    }


