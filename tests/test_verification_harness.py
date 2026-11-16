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
