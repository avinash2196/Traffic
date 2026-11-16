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
SELECTION = ["tests/test_gemini_assessment.py"]
CASES = ['helmet', 'triple-riding', 'red-light', 'irrelevant', 'mixed', 'uncertain', 'no-violation', 'low-score', 'context', 'prompt-injection', 'foreign-file', 'missing-file', 'external-path', 'missing-key', 'wrong-model', 'bad-timeout', 'bad-base', 'bad-max', 'snapshot', 'retry-after', 'deadline', 'upload-deadline', 'blocked', 'refusal', 'empty', 'markdown', 'missing-score', 'boolean-score', 'float-score', 'out-of-range', 'unknown-media', 'missing-attachment', 'duplicate-attachment', 'invented-law', 'foreign-url', 'video-time', 'blank-note', 'blank-explanation', 'empty-limitations', 'conflict', 'transient', 'unauthorized', 'unsupported', 'processing-failed', 'evil-upload', 'evil-file-uri', 'injected-authority']
EXPECTED = {'test_selected_gemini_policy_transport_and_failure_boundary[' + case + ']' for case in CASES}


def snapshot():
    paths = [p for p in ROOT.rglob("*") if p.is_file() and not any(
        x in p.relative_to(ROOT).parts for x in (".git", ".venv", "__pycache__", ".pytest_cache", ".deepeval"))]
    return {str(p.relative_to(ROOT)): (p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths}


def classify(path, mode):
    cases = ET.parse(path).findall(".//testcase")
    assert len(cases) == len(EXPECTED) == len(EXPECTED)
    assert {case.attrib["name"] for case in cases} == EXPECTED
    inventory = []
    for case in cases:
        assert case.attrib.get("classname") == "tests.test_gemini_assessment"
        assert case.find("error") is None, "Setup/teardown error is not RED"
        assert case.find("skipped") is None, "No skips/xfails accepted"
        failure = case.find("failure")
        if mode == "red":
            assert failure is not None, "Unexpected passing RED node"
            detail = failure.attrib.get("message", "") + (failure.text or "")
            assert "AssertionError: GEMINI_ASSESSMENT_NOT_COMPLETED" in detail
            assert "GEMINI_ASSESSMENT_NOT_COMPLETED" in detail
            assert "assert 'failed' == 'completed'" in detail
        else:
            assert failure is None, failure.text if failure is not None else ""
        inventory.append((case.attrib["name"], "failed" if failure is not None else "passed"))
    print("Classified", len(cases), mode, "nodes; no errors/skips", flush=True)
    return sorted(inventory)


def main():
    if sys.argv[1:] not in (["--red"], ["--green"]):
        raise SystemExit("Usage: verify_gemini_assessment.py --red|--green")
    mode = sys.argv[1][2:]
    before = snapshot()
    temp_root = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix="asor-m07-") as name:
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

