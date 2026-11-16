"""Run current-demo checks only in an owned disposable repository copy."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "test_auth.py", "test_api_endpoints.py", "test_media.py",
    "test_verification_harness.py", "test_identity.py",
)
SUBMISSION = "tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id"
RED_FILE = "tests/test_evidence_intake.py"


def snapshot():
    paths = [path for path in ROOT.iterdir() if path.is_file()]
    for name in ("media_store", ".local", "tests", "templates", "static", "tools", ".github"):
        directory = ROOT / name
        if directory.exists():
            paths.extend(path for path in directory.rglob("*") if path.is_file()
                         and "__pycache__" not in path.parts)
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths}


def classify(xml_path, phase):
    nodes = ET.parse(xml_path).findall(".//testcase")
    errors = [node for node in nodes if node.find("error") is not None]
    failures = [node for node in nodes if node.find("failure") is not None]
    skips = [node for node in nodes if node.find("skipped") is not None]
    passed = len(nodes) - len(errors) - len(failures) - len(skips)
    print(phase, "passed", passed, "failed", len(failures), "errors", len(errors), "skipped", len(skips), flush=True)
    if errors:
        return False
    if phase == "preservation":
        return (passed, len(failures), len(skips), len(nodes)) == (40, 0, 12, 52)
    if len(nodes) != 54 or len(failures) != 54 or skips:
        return False
    for node in failures:
        failure = node.find("failure")
        text = failure.attrib.get("message", "") + (failure.text or "")
        if "assert 401 == 201" not in text:
            return False
        if not (node.attrib.get("classname", "").startswith("tests.test_evidence_intake")
                or (node.attrib.get("classname") == "tests.test_api_endpoints.TestCitizenReportSubmission"
                    and node.attrib.get("name") == "test_citizen_submit_report_returns_201_with_report_id")):
            return False
    print("Classified 54 intended RED assertions: valid authenticated upload returned 401 instead of 201", flush=True)
    return True


def main():
    if sys.argv[1:] not in ([], ["--intake"], ["--intake-red"]):
        raise SystemExit("Usage: verify_current_demo.py [--intake|--intake-red]")
    intake_red = sys.argv[1:] == ["--intake-red"]
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
        selections = [("demo", ["tests/" + filename for filename in FILES])]
        if sys.argv[1:] == ["--intake"]:
            selections = [("intake", ["tests/" + filename for filename in FILES] + [RED_FILE])]
        if intake_red:
            selections = [("preservation", ["tests/" + filename for filename in FILES] + ["--deselect=" + SUBMISSION]),
                          ("red", [RED_FILE, SUBMISSION])]
        failed = False
        for phase, selection in selections:
            for repeat in (1, 2):
                log_path = scratch / (phase + "-" + str(repeat) + ".log")
                xml_path = scratch / (phase + "-" + str(repeat) + ".xml")
                command = [sys.executable, "-m", "pytest", "-p", "pytest_asyncio.plugin", "-v"]
                if intake_red:
                    command.append("--junitxml=" + str(xml_path))
                command.extend(selection)
                with log_path.open("w", encoding="utf-8") as log:
                    child = subprocess.Popen(command, cwd=copy, env=env,
                                             stdout=log, stderr=subprocess.STDOUT)
                    try:
                        result = child.wait(timeout=180 if phase == "intake" else 90)
                    except subprocess.TimeoutExpired:
                        child.kill()
                        child.wait()
                        result = "TIMEOUT"
                assert child.poll() is not None
                print(phase, "run", repeat, "result:", result, flush=True)
                print(log_path.read_text(encoding="utf-8"), flush=True)
                expected_exit = 1 if phase == "red" else 0
                failed = result != expected_exit
                if intake_red and not failed:
                    failed = not classify(xml_path, phase)
                if failed:
                    break
            if failed:
                break
        assert snapshot() == before, "Protected checkout files changed"
        print("Protected checkout paths and SHA-256 values unchanged", flush=True)
    assert not scratch.exists()
    print("Disposable repository and test state removed; child processes finished", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
