# ASOR-M08D execution evidence — stopped 2026-11-11

Approved011 six source artifacts were applied mechanically. All three exact diffs passed `git -c core.autocrlf=false apply --check --ignore-space-change`; all six normalized outputs matched independently reconstructed approved content. Root/test Python parsed without bytecode. No test, dependency or configuration change; no live provider call or private content read.

Verification stopped on a new execution failure. M08D is not complete; no unchanged retry occurred. The accepted historical aggregate F does not waive this failure.

## Actual commands and outcomes

All commands used cwd `C:\Users\avina\AppData\Local\Temp\asor-m08d-exec-20261111-70d6c2\repository`, absolute existing .venv Python, explicit pytest-asyncio, disabled plugin autoload, UTF-8/no bytecode, approved environment filter, and the same owned temporary fixture parent. Source-only copy excluded .local/.env/.git/real DB/media/backups.

| Partition | Limit | Actual result |
| --- | ---: | --- |
| full-new-nonvideo | 180s | exit0; 23 passed, 6 deselected, 1 warning in 89.44s (0:01:29) |
| full-new-video | 180s | exit0; 6 passed, 23 deselected, 1 warning in 142.40s (0:02:22) |
| full-gemini | 180s | exit0; 47 passed, 1 warning in 71.71s (0:01:11) |
| full-durable | 180s | exit0; 14 passed, 1 warning in 34.32s |
| full-provider-state | 180s | exit1; 1 failed, 3 passed, 7 deselected, 1 warning in 105.85s (0:01:45) |

Full provider-transport and intake partitions and every state/configuration repeat were NOT RUN after failure. No complete209 or repeat96 claim. All completed children returned/reaped, and the owned decoder carrier was stopped and independently confirmed absent.

Exact actual argument arrays:

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\full-new-nonvideo.xml', 'tests/test_gateway_openai.py', '-k', 'not sampled_video']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\full-new-video.xml', 'tests/test_gateway_openai.py', '-k', 'sampled_video']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\full-gemini.xml', 'tests/test_gemini_assessment.py']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\full-durable.xml', 'tests/test_durable_processing.py']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\full-provider-state.xml', 'tests/test_provider_response.py', '-k', 'attempt_diagnostic_capture or unobserved_diagnostic', '-x']
```

## New failure traceback

```text
...F
================================== FAILURES ===================================
_ test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS] _

assessment_runtime = (<starlette.testclient.TestClient object at 0x000002B1A233FCE0>, <sqlite3.Connection object at 0x000002B1A26FE3E0>, Wi...2B1A233D5B0>, [<gateway.Worker object at 0x000002B1A2340AF0>], <function ai_worker_factory at 0x000002B1A1990A90>, ...)
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002B1A22F6250>
caplog = <_pytest.logging.LogCaptureFixture object at 0x000002B1A26B4C30>
stage = 'generate', status = 503, code = 'PROVIDER_TRANSIENT'
kind = 'HTTP_STATUS'

    @pytest.mark.parametrize('stage,status,code,kind', [
        ('upload-start', 400, 'PROVIDER_REQUEST_REJECTED', 'HTTP_STATUS'),
        ('upload-finalize', 403, 'PROVIDER_CONFIGURATION', 'HTTP_STATUS'),
        ('file-poll', 429, 'PROVIDER_TRANSIENT', 'HTTP_STATUS'),
        ('generate', 503, 'PROVIDER_TRANSIENT', 'HTTP_STATUS'),
        ('generate', 'reset', 'PROVIDER_TRANSIENT', 'NETWORK_ERROR'),
    ])
    def test_attempt_diagnostic_capture(assessment_runtime, monkeypatch, caplog, stage, status, code, kind):
        import durable
        import gemini
        runtime = assessment_runtime
        monkeypatch.setattr(durable, 'gemini_client_factory', DEFAULT_FACTORY)
        monkeypatch.setattr(durable, 'gemini_monotonic', time.monotonic)
        monkeypatch.setitem(runtime[0].app.state.ai_settings, 'AI_ATTEMPT_TIMEOUT_SECONDS', 30)
        caplog.set_level(logging.DEBUG)
        with endpoint() as state, remap_child(monkeypatch, state) as children:
            report_id, job_id, ids, _ = submit(runtime, key='positive-boundary')
            state['value'] = output(ids)
            positive = run(runtime, report_id)
>           assert positive['ai']['state'] == 'completed', (
                positive['ai']['failure_code'], [call[0] for call in state['calls']])
E           AssertionError: ('ATTEMPT_TIMEOUT', ['upload-start', 'upload-finalize', 'file-poll'])
E           assert 'retry-wait' == 'completed'
E             
E             - completed
E             + retry-wait

C:\Users\avina\AppData\Local\Temp\asor-m08d-exec-20261111-70d6c2\repository\tests\test_provider_response.py:177: AssertionError
------------------------------ Captured log call ------------------------------
INFO     httpx:_client.py:1025 HTTP Request: POST http://testserver/api/media/upload "HTTP/1.1 201 Created"
INFO     httpx:_client.py:1025 HTTP Request: POST http://testserver/api/reports "HTTP/1.1 201 Created"
INFO     httpx:_client.py:1025 HTTP Request: GET http://testserver/api/authority/reports/c2f0ddd28a9b4188 "HTTP/1.1 200 OK"
============================== warnings summary ===============================
..\..\..\..\..\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ===========================
FAILED tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 3 passed, 7 deselected, 1 warning in 105.85s (0:01:45)
```

## Setup deviation

Initial wrapper-only version preflight returned1 before any pytest: exact helper requires a source operand and `ffmpeg -version` has none. Exact helper/wrappers were preserved. Version preflight was corrected to `ffmpeg -i pipe:0 -version` and `ffprobe -version pipe:0` with empty stdin; both passed. Image identity `sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de`, network none, zero mounts and WindowsPath wrapper equality were verified before video/Gemini. No test limit changed.

## Protection and exact inventories

165 explicitly allowlisted preexisting source/document/config-example hashes were captured; every entry other than the three authorized modified modules remained equal. 30 private-local/media/database metadata entries (path/size/mtime only) remained equal; this is not byte identity evidence. No staging/commit/reset. Six approved source SHA-256 values:

```json
{
  "assessment_policy.py": "fe6cc7738b315aed82145619c797c14afc53474b411fd24192f65a2e3daa8904",
  "gateway.py": "0bb2a0e043ca5f5332d0ab9fb39e32f7b7bc449ef292dbd6c47516e3de1e08a9",
  "openai_adapter.py": "96bbb26bafecbfc6e2d623d1f3de9b322735099e29c7b53e73097c3459e3b54e",
  "app.py": "bf7aa09825c12ab5b908e719ae09b4b324974d7b57c9bcc35e9e74e9417e9184",
  "durable.py": "b4239ab5a1f2fa3fc992e59765fe738f37edcadecbf7bbd648b55db4687fe033",
  "gemini.py": "d6c6f8f5536d1b18e9c18dd57b9c5fc03a5d9b474ab1e8036a9a1ffbb68eacb0"
}
```

The adjacent JSON retains actual command arrays, full captured synthetic logs, and exact observed JUnit name/outcome inventories. Historical M08B inventories and new29 comparison cannot be completed for unrun nodes. Scratch cleanup is recorded separately below.

The failing test explicitly sets `AI_ATTEMPT_TIMEOUT_SECONDS` to30 and restores the real monotonic clock. Its positive control exhausted that budget after upload-start/upload-finalize/file-poll, before the intended503 fault request. This establishes the observed timeout location, not its root cause. The four preceding partitions completed90 passes; provider-state added3 passes and1 failure before fail-fast stop (93 observed passes total).

Cleanup: verified the literal native Temp target and its full tree had no links/junctions, removed only that owned tree, and confirmed absence. Owned carrier absent, every child reaped. Temporary checkout driver/state/result files removed after evidence capture; six approved sources retained.
