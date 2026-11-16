# Implementation Plan — Provider Harness Lifecycle OTHER

## Milestone

AGW-M02A, ai-screening-officer-review; proposed Plan amendment prepared 2026-11-11 (America/Chicago). Planning package only; its new milestone and this IP both require user review.

## Milestone Type

OTHER.

## Review Summary

- Tests only: synthetic provider work moves to its own owned loopback HTTP process; production behavior is unchanged.
- Preserves AGW-CT01–08, AGW-M02 valid RED, all 19 assertions and the under-three-second timeout; supports AGW-R04/R06/R08 verification.
- Create `tests/agw_provider_child.py`; modify the service child, service fixture and focused verifier; delete none.
- New diagnostic proves positive real HTTP, local client-tree termination, continued remote work, marker drain and provider cleanup.
- Execution verifier `--red` must exit zero: lifecycle check plus state repeat, 19 intended failures, two preserved passes and protections/cleanup.
- Review the proposed M02A Plan insertion and shifted GREEN014/live015 numbering; no new dependencies or production cleanup exception.

## Authoritative References

- `requirements.md`, current `External-Contract.md` AGW-CT01–08: approved 2026-11-11, unchanged constraints. `Plan.md`: original approved sequence retained; only proposed M02A amendment and its consequent references await user review.
- Approved/executed `012_Implementation_Plan_Service_Boundary_RED.md`: exact provider child, fixture, helper, source closure, representative coverage and preserved checks; read again against actual files. Its explicit untested CT06 kill/reap/cancellation branches remain GREEN obligations.
- `AGW-M02-Execution-2026-11-11.md`: valid RED, verifier exit0 with19 ordinary behavioral failures,2 preserved passes, no errors/skips/timeouts. This evidence is not invalidated or relabelled.
- Actual `tests/agw_service_child.py`, `tests/test_gateway_service.py`, `tests/verify_gateway_service.py`, `.github/copilot-instructions.md`; PDD0.16 implementation-planning/template, prompt-driven-development, code-quality and testing guidance. No new dependency or API contract is introduced. Historical IP001–011 decisions are carried only through the approved012 references below; their incomplete/live outcomes remain historical.

## Carried-Forward Decisions

IP012: root virtual-environment interpreter, source-only copies, explicit synthetic state, literal-loopback sockets,10s readiness, module-scoped service process, restricted service source closure, safe diagnostics, stripped environment,19+2 focused inventory and offline pinned decoder helper unchanged. IP012 incorporates001–011's durable ownership/private-state protections, no nested retries and no live/private input. Deliberate review change: replace its in-process blocking MockTransport with separate owned HTTP provider process; retain the factory signature and fixed public URL. Owned Windows cleanup now terminates the process tree because the observed launcher PID differs from the server PID.

## Preconditions / Predecessor Evidence

M02 is completed valid RED. M02A is proposed OTHER because this corrects synthetic test lifecycle, adding no production behavior and owning no production requirement. Its execution waits for the Plan amendment and this IP to be approved. The service file is still absent; no production implementation is a prerequisite for the independent diagnostic. The existing19 expected failures remain classified RED by a verifier that itself exits zero.

Baseline observation before edits: the original callback sleeps4s at `tests/agw_service_child.py:28–29` and removes the marker only in `finally` at43–49; the fixture at `tests/test_gateway_service.py:130–135` waits for marker drainage. A native isolated Windows child check reported `{'child_reaped': True, 'finally_marker_remains': True}` after termination. Its temporary script/marker/directory were deleted. This establishes the lifecycle problem without claiming a production cancellation implementation already exists.

## Current Repository State

- `tests/agw_service_child.py:20–50`: same-process synchronous MockTransport creates/removes synthetic provider marker around the blocking wire builder.
- `tests/test_gateway_service.py:45–91,112–121`: module fixture starts a separate gateway with source allowlist and10s readiness, then terminates its launcher; `:249–259` retains the3s budget/under3s response assertion.
- `tests/verify_gateway_service.py:15–21,81–85`: fixed previously consumed task path, source/test allowlist and19+2 groups; exact helper rejects an existing task directory.
- `Plan.md` Execution Status: M02 completed, M03 pending; original dirty working sources remain preserved. No clean-tree or full-suite baseline is asserted.

## Files in Scope

### Files to Create

`tests/agw_provider_child.py`.

### Files to Modify

`tests/agw_service_child.py`, `tests/test_gateway_service.py`, `tests/verify_gateway_service.py`.

### Files to Delete

None.

## Proposed Changes

1. `agw_provider_child.py`: move the unchanged synthetic Responses payload/status/refusal/usage builder into `serve(root)`, an owned127.0.0.1 HTTP server. `LoopbackTransport.handle_request(request)` accepts only the exact fixed public Responses URL and forwards method/body/headers/extensions through HTTPTransport(retries=0,trust_env=False) to its owned loopback URL; redirects and proxy environment are disabled. No public-provider socket is used.
2. `Provider(root,environment)` starts once, records server/launcher PIDs and startup timestamps, waits at most10s for the owned bound-address record, drains its marker before teardown and reaps its owned process tree. `stop_process(child)` handles the Windows virtual-environment launcher tree. Synthetic provider work may continue after client cancellation and then clean its own marker: this models the approved remote-provider ambiguity without leaving local service work running.
3. `check_lifecycle(root)` independently proves positive real HTTP, kills/reaps a separate local HTTP client while four-second remote work is active, asserts provider/marker survive that local cancellation, then verifies normal remote drain and owned server teardown. It uses no gateway business behavior, real provider, media or private input. `--check` is directly callable on the RED baseline.
4. Service child factory delegates to `provider_client(sys.argv[3])`; fixture copies the helper into the source closure, starts the provider once, supplies its URL as a test-only argument and closes both owned process trees. Every existing module function/assertion, including fixture drainage and the timeout, is unchanged. No test-only gateway endpoint is added.
5. Verifier copies the new helper, uses unused dedicated M02A-red/M03-green task roots, compiles all copied Python and runs the lifecycle diagnostic twice against the same state directory without cleanup, before its unchanged19+2 classifier. State-repeat and decoder/protection behavior remain unchanged; bounded lifecycle logs are retained. Lifecycle timeout kills its owned tree and fails verification, never counts as RED.

## Proposed Code / Tests

### `tests/agw_service_child.py` — complete unified diff

```diff
--- a/tests/agw_service_child.py
+++ b/tests/agw_service_child.py
@@ -8,46 +8,15 @@
 import sys
 import time
 
-import httpx
 import uvicorn
 from fastapi import FastAPI
 
 ROOT = Path(sys.argv[1])
-MODE = ROOT / 'mode.json'
-CALLS = ROOT / 'provider.jsonl'
 
 
 def provider_client_factory():
-    def respond(request):
-        assert str(request.url) == 'https://api.openai.com/v1/responses'
-        assert request.headers['authorization'] == 'Bearer synthetic-provider-key'
-        body = json.loads(request.content)
-        with CALLS.open('a', encoding='utf-8') as stream:
-            stream.write(json.dumps(body) + '\n')
-        mode = json.loads(MODE.read_text(encoding='utf-8'))
-        if mode.get('delay'):
-            time.sleep(mode['delay'])
-        status = mode.get('status', 200)
-        if status != 200:
-            return httpx.Response(status, headers={'Retry-After': '7'}, json={
-                'error': {'message': 'PRIVATE_PROVIDER_BODY C:/private/media.jpg'}})
-        payload = {'status': 'completed', 'model': 'provider-reported-snapshot',
-                   'usage': mode.get('usage', {'input_tokens': 23,
-                       'input_tokens_details': {'cached_tokens': 0}, 'output_tokens': 11,
-                       'output_tokens_details': {'reasoning_tokens': 3}, 'total_tokens': 34}),
-                   'output': [{'type': 'message', 'role': 'assistant', 'content': [
-                       {'type': 'output_text', 'text': json.dumps(mode['assessment'])}]}]}
-        if mode.get('refusal'):
-            payload['output'][0]['content'] = [{'type': 'refusal', 'refusal': 'PRIVATE_REFUSAL'}]
-        return httpx.Response(200, headers={'x-request-id': 'req_synthetic'}, json=payload)
-    def observed(request):
-        active=ROOT/'provider-active'
-        active.touch()
-        try:
-            return respond(request)
-        finally:
-            active.unlink(missing_ok=True)
-    return httpx.Client(transport=httpx.MockTransport(observed), follow_redirects=False)
+    from agw_provider_child import provider_client
+    return provider_client(sys.argv[3])
 
 
 if __name__ == '__main__':
```

### `tests/test_gateway_service.py` — complete unified diff

```diff
--- a/tests/test_gateway_service.py
+++ b/tests/test_gateway_service.py
@@ -16,6 +16,7 @@
 import pytest
 
 from assessment_policy import PROMPT
+from tests.agw_provider_child import Provider, stop_process
 from tests.test_durable_processing import PausedWorker, OWNER, OFFICER
 from tests.test_evidence_intake import photo
 from tests.test_gemini_assessment import output
@@ -56,6 +57,7 @@
             if (repository/name).exists():
                 shutil.copy2(repository/name, service/name)
         shutil.copy2(Path(__file__).with_name('agw_service_child.py'), service/'child.py')
+        shutil.copy2(Path(__file__).with_name('agw_provider_child.py'), service/'agw_provider_child.py')
         assert not any((service/name).exists() for name in
                        ('app.py', 'bootstrap.py', 'durable.py', 'intake.py', 'roadwatch.db'))
         with socket.socket() as reservation:
@@ -66,8 +68,9 @@
             for word in ('KEY','TOKEN','OPENAI','GEMINI','GOOGLE','DATABASE','ROADWATCH','AI_'))}
         environment.update(AI_GATEWAY_TOKEN=TOKEN, AI_PROVIDER='openai', OPENAI_MODEL=MODEL,
                            OPENAI_API_KEY='synthetic-provider-key', PYTHONDONTWRITEBYTECODE='1')
+        self.provider = Provider(root, environment)
         self.log = (root/'service.log').open('w', encoding='utf-8')
-        self.child = subprocess.Popen([sys.executable, '-B', 'child.py', str(root), str(port)],
+        self.child = subprocess.Popen([sys.executable, '-B', 'child.py', str(root), str(port), self.provider.url],
             cwd=service, env=environment, stdout=self.log, stderr=subprocess.STDOUT)
         self.client = httpx.Client(base_url=self.url, timeout=15, follow_redirects=False,
                                    headers={'Authorization': 'Bearer '+TOKEN}, trust_env=False)
@@ -108,13 +111,15 @@
 
     def close(self):
         self.client.close()
-        self.child.terminate()
         try:
-            self.child.wait(8)
-        except subprocess.TimeoutExpired:
-            self.child.kill(); self.child.wait(5)
-        self.log.close()
+            stop_process(self.child)
+        finally:
+            try:
+                self.provider.close()
+            finally:
+                self.log.close()
         assert self.child.poll() is not None
+
 
 
 @pytest.fixture(scope='module')
```

### `tests/verify_gateway_service.py` — complete unified diff

```diff
--- a/tests/verify_gateway_service.py
+++ b/tests/verify_gateway_service.py
@@ -10,11 +10,12 @@
 import xml.etree.ElementTree as ET
 
 SOURCE=Path(__file__).resolve().parents[1]
-TASK=Path(r'C:\Users\avina\AppData\Local\Temp\asor-agw-m02-verify-20261111')
+TASK=Path(r'C:\Users\avina\AppData\Local\Temp') / (
+    'asor-agw-m02a-verify-20261111' if '--red' in sys.argv else 'asor-agw-m03-verify-20261111')
 ROOT_FILES=('ai_gateway_service.py','app.py','assessment_policy.py','auth_utils.py','bootstrap.py','controls_http.py',
     'controls_operator.py','durable.py','gateway.py','gemini.py','intake.py','media.py',
     'openai_adapter.py','runtime_controls.py','pytest.ini')
-TEST_FILES=('conftest.py','__init__.py','agw_service_child.py','test_gateway_service.py',
+TEST_FILES=('conftest.py','__init__.py','agw_service_child.py','agw_provider_child.py','test_gateway_service.py',
     'test_durable_processing.py','test_evidence_intake.py','test_gemini_assessment.py',
     'test_gateway_openai.py','verify_gateway_service.py')
 PRESERVED=('tests/test_durable_processing.py::test_concurrent_claims_and_recovered_stale_completion_publish_once',
@@ -73,6 +74,21 @@
                 wrapper.write_text('@"'+sys.executable+'" "'+str(TASK/'decoder_carrier.py')+'" '+tool+' %*\n')
                 assert Path(shutil.which(tool,path=str(binary))).resolve()==wrapper.resolve()
             env.update(ASOR_DECODER_CARRIER=carrier,PATH=str(binary)+os.pathsep+env['PATH'])
+        lifecycle=temporary/'provider-lifecycle'
+        for run in ('first','repeat'):
+            command=[sys.executable,'-B',str(copy/'tests/agw_provider_child.py'),'--check',str(lifecycle)]
+            with (TASK/('provider-lifecycle-'+run+'.log')).open('w',encoding='utf-8') as output:
+                child=subprocess.Popen(command,cwd=copy,env=env,stdout=output,
+                                       stderr=subprocess.STDOUT)
+                try:
+                    returncode=child.wait(timeout=30)
+                except subprocess.TimeoutExpired:
+                    subprocess.run(['taskkill','/PID',str(child.pid),'/T','/F'],
+                                   check=True,capture_output=True,timeout=15)
+                    child.wait(timeout=5)
+                    raise AssertionError('Provider lifecycle verification timed out')
+                assert returncode==0,'Provider lifecycle verification failed: '+run
+        shutil.copy2(lifecycle/'provider.log',TASK/'provider-lifecycle-server.log')
         groups=[('new',['tests/test_gateway_service.py'],mode),('preserved',list(PRESERVED),'green')]
         if mode=='green':
             groups.append(('state-repeat',['tests/test_gateway_service.py::test_application_worker_owns_wire_and_persistence',
```

### `tests/agw_provider_child.py` — complete new file

```python
"""Owned loopback Responses substitute; no external provider sockets or inputs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

import httpx

PUBLIC_URL = 'https://api.openai.com/v1/responses'


class LoopbackTransport(httpx.BaseTransport):
    def __init__(self, url):
        parsed = urlsplit(url)
        assert parsed.scheme == 'http' and parsed.hostname == '127.0.0.1'
        assert parsed.port and not parsed.username and not parsed.password
        assert parsed.path == '' and not parsed.query and not parsed.fragment
        self.url = url
        self.transport = httpx.HTTPTransport(retries=0, trust_env=False)

    def handle_request(self, request):
        assert str(request.url) == PUBLIC_URL, 'Unexpected provider destination'
        forwarded = httpx.Request(request.method, self.url+'/v1/responses',
            headers=request.headers, content=request.read(), extensions=request.extensions)
        return self.transport.handle_request(forwarded)

    def close(self):
        self.transport.close()


def provider_client(url):
    return httpx.Client(transport=LoopbackTransport(url), follow_redirects=False, trust_env=False)


def serve(root):
    class Responses(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            assert self.path == '/v1/responses'
            assert self.headers['Authorization'] == 'Bearer synthetic-provider-key'
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            with (root/'provider.jsonl').open('a', encoding='utf-8') as stream:
                stream.write(json.dumps(body)+'\n')
            active = root/'provider-active'
            active.touch()
            try:
                mode = json.loads((root/'mode.json').read_text(encoding='utf-8'))
                time.sleep(mode.get('delay', 0))
                status = mode.get('status', 200)
                payload = {'error': {'message': 'PRIVATE_PROVIDER_BODY C:/private/media.jpg'}}
                if status == 200:
                    content = [{'type': 'output_text', 'text': json.dumps(mode['assessment'])}]
                    if mode.get('refusal'):
                        content = [{'type': 'refusal', 'refusal': 'PRIVATE_REFUSAL'}]
                    payload = {'status': 'completed', 'model': 'provider-reported-snapshot',
                        'usage': mode.get('usage', {'input_tokens': 23,
                            'input_tokens_details': {'cached_tokens': 0}, 'output_tokens': 11,
                            'output_tokens_details': {'reasoning_tokens': 3}, 'total_tokens': 34}),
                        'output': [{'type': 'message', 'role': 'assistant', 'content': content}]}
                encoded = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header('Content-Length', str(len(encoded)))
                self.send_header('Content-Type', 'application/json')
                self.send_header('x-request-id', 'req_synthetic')
                self.send_header('Retry-After', '7')
                self.end_headers()
                try:
                    self.wfile.write(encoded)
                except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                    pass  # A cancelled local client does not cancel remote provider work.
            finally:
                active.unlink(missing_ok=True)
                print(json.dumps(dict(event='provider-drained', pid=os.getpid(),
                                      monotonic=time.monotonic())), flush=True)

    with HTTPServer(('127.0.0.1', 0), Responses) as server:
        (root/'provider-address.json').write_text(json.dumps(dict(
            url='http://127.0.0.1:'+str(server.server_port), pid=os.getpid())), encoding='utf-8')
        print(json.dumps(dict(event='provider-ready', pid=os.getpid(),
                              monotonic=time.monotonic())), flush=True)
        server.serve_forever()


def stop_process(child):
    if child.poll() is None:
        if os.name == 'nt':
            subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'],
                           check=True, capture_output=True, timeout=10)
        else:
            child.terminate()
        try:
            child.wait(8)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(5)
    assert child.poll() is not None


class Provider:
    def __init__(self, root, environment):
        self.root = root
        address = root/'provider-address.json'
        address.unlink(missing_ok=True)
        self.log = (root/'provider.log').open('a', encoding='utf-8')
        self.child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
            '--serve', str(root)], cwd=root, env=environment, stdout=self.log,
            stderr=subprocess.STDOUT)
        deadline = time.monotonic()+10
        while time.monotonic() < deadline and self.child.poll() is None:
            if address.exists():
                try:
                    value = json.loads(address.read_text(encoding='utf-8'))
                except (ValueError, OSError):
                    time.sleep(.02)
                    continue
                assert type(value['pid']) is int and value['pid'] > 0
                self.server_pid = value['pid']
                self.url = value['url']
                return
            time.sleep(.02)
        self.close()
        raise AssertionError('Provider did not bind; pid='+str(self.child.pid)+
            ' returncode='+str(self.child.returncode)+': '+(root/'provider.log').read_text())

    def drain(self):
        deadline = time.monotonic()+10
        while (self.root/'provider-active').exists() and time.monotonic() < deadline:
            assert self.child.poll() is None, 'Provider exited before draining'
            time.sleep(.01)
        assert not (self.root/'provider-active').exists(), 'Provider did not drain'

    def close(self):
        try:
            self.drain()
        finally:
            try:
                stop_process(self.child)
            finally:
                self.log.close()


def check_lifecycle(root):
    root.mkdir(exist_ok=True)
    assert not (root/'provider-active').exists()
    environment = {k:v for k,v in os.environ.items() if not any(word in k.upper()
        for word in ('KEY','TOKEN','OPENAI','GEMINI','GOOGLE','DATABASE','ROADWATCH','AI_'))}
    (root/'mode.json').write_text(json.dumps(dict(assessment={})), encoding='utf-8')
    provider = Provider(root, environment)
    child = None
    try:
        with provider_client(provider.url) as client:
            result = client.post(PUBLIC_URL, headers={'Authorization': 'Bearer synthetic-provider-key'},
                                 json={'synthetic': True})
        assert result.status_code == 200 and result.json()['model'] == 'provider-reported-snapshot'
        provider.drain()
        (root/'mode.json').write_text(json.dumps(dict(assessment={}, delay=4)), encoding='utf-8')
        child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
            '--client', provider.url], cwd=root, env=environment,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.monotonic()+2
        while not (root/'provider-active').exists() and time.monotonic() < deadline:
            time.sleep(.01)
        assert (root/'provider-active').exists() and child.poll() is None
        started = time.monotonic()
        stop_process(child)
        assert time.monotonic()-started < 3 and child.poll() is not None
        assert provider.child.poll() is None and (root/'provider-active').exists()
        provider.drain()
        print(json.dumps(dict(event='lifecycle-passed', client_pid=child.pid,
            provider_pid=provider.server_pid, provider_launcher_pid=provider.child.pid, client_reaped=True, remote_drained=True,
            elapsed_ms=round((time.monotonic()-started)*1000))), flush=True)
    finally:
        if child is not None and child.poll() is None:
            stop_process(child)
        provider.close()


if __name__ == '__main__':
    if sys.argv[1] == '--serve':
        serve(Path(sys.argv[2]))
    elif sys.argv[1] == '--check':
        check_lifecycle(Path(sys.argv[2]))
    elif sys.argv[1] == '--client':
        with provider_client(sys.argv[2]) as client:
            client.post(PUBLIC_URL, headers={'Authorization': 'Bearer synthetic-provider-key'},
                        json={'synthetic': True})
    else:
        raise AssertionError('Unknown harness operation')
```

## Execution Steps

1. Confirm recorded user approval of the narrow Plan amendment and this IP. Apply only the four exact files above; do not apply production code or change existing behavioral assertions.
2. Run the exact verifier command below once from the explicit native host cwd. It performs its own compilation, source-only copy, synthetic lifecycle first/repeat,19 intended RED classifications and2 preserved checks.
3. Record actual command/output, failures/deviations, source/metadata protections and cleanup in M02A evidence. On success update only M02A execution status and this IP's Human Review status; retain M02 completion/evidence. Prepare GREEN014 separately, without applying production changes.

## Acceptance / Completion Criteria

- Only the four exact test/helper files change, besides this milestone's status/evidence documentation; production source/configuration/dependencies/contract/private state remain unchanged.
- Existing19 business outcomes, assertion expressions and deadlines remain unchanged, including successful HTTP preconditions and timeout<3s. No wrapper supplies gateway results or application state.
- Diagnostic proves actual loopback HTTP first, kills/reaps its local client tree while the provider is active, observes remote provider survival and eventual marker cleanup, then stops/reaps the owned provider; its second run passes without intermediate cleanup of its state directory.
- Fixed public URL is the only remapped provider destination; real transport has zero retries, proxies/redirects disabled, synthetic auth/body preserved. Gateway source closure remains application-DB-free.
- Verifier exits0 with19 intended ordinary assertion failures,2 preserved passes, no unexpected errors/skips/timeouts, passing protection assertions and owned process/carrier/copy cleanup. These are preserved RED results, not passing service behavior.
- No unreviewed production cancellation implementation, CT06 waiver, assertion weakening, live-provider claim or broad-suite claim is introduced.

## Verification

### Commands

Run once after approval; native Windows loopback requires the same authorized host execution context as012, with exact owned cwd `C:\Users\avina\AppData\Local\Temp`:

```powershell
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' -B 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\tests\verify_gateway_service.py' --red
```

The exact helper writes bounded logs/XML/manifests to `C:\Users\avina\AppData\Local\Temp\asor-agw-m02a-verify-20261111`, refuses reuse, and deletes copied source/synthetic state in finally. It retains lifecycle summary/server logs outside deleted temporary state. Do not repeat the whole verifier; its two lifecycle runs supply the required persistent-state repeat. The existing helper's TEMP/TMP settings apply only to its disposable subprocess state, carried unchanged from012; planning did not virtualize host temporary paths.

### Affected Tests

`tests/test_gateway_service.py` all19 outcomes, found by its Service/factory/process dependencies; the two named `PRESERVED` durable nodes in the verifier, unchanged from012. No new pytest business test, Gemini inventory, old209 suite or full RED/GREEN probe. The independent lifecycle `--check` is a harness check, not production acceptance evidence.

### Expected Evidence

Expected / Predicted — Not Yet Verified as milestone execution: lifecycle first+repeat pass; verifier summary `new 19 intended failures`, `preserved 2 passes`, cleanup success; overall exit0. A raw pytest exit1 is accepted only inside the exact19-failure classifier and is never the OTHER command's result. Existing failure markers/HTTP404 remain missing approved behavior. A process/import/setup failure is a failure, never intended RED.

### Planning-Time Dry Run

Planning evidence only, not milestone execution. Literal host task root: `C:\Users\avina\AppData\Local\Temp\asor-agw-m02a-plan-20261111`; explicit native cwd; root virtual-environment interpreter, no provider keys/media/DB reads and no host TEMP override.

- Initial command: `& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' -B 'C:\Users\avina\AppData\Local\Temp\asor-agw-m02a-plan-20261111\agw_provider_child.py' --check 'C:\Users\avina\AppData\Local\Temp\asor-agw-m02a-plan-20261111\lifecycle'` — exit1 at initial equality assertion between launcher PID and server PID. The observed Windows launcher creates a different server PID. The owned server was stopped; this failed draft is not passing evidence.
- Code correction: record separate actual server/launcher PIDs; terminate and wait the owned local process tree. Same command once after that exact correction — exit0: `{"event":"lifecycle-passed","client_pid":8824,"provider_pid":10456,"provider_launcher_pid":22168,"client_reaped":true,"remote_drained":true,"elapsed_ms":4022}`. Local-client cancellation/reap satisfied<3s;4022ms is the subsequent remote-drain observation, not the gateway response time. The diagnostic proves harness mechanics, not production CT06.
- `& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' -B 'C:\Users\avina\AppData\Local\Temp\asor-agw-m02a-plan-20261111\prepare.py'` — exit0, compiled four proposed files; AST equality confirmed all existing top-level service-test functions/assertions unchanged. Final verifier timeout-handler edit compiled while assembling this document; no additional diagnostic/rerun followed.
- NOT RUN during planning:19-case RED classifier, preserved pytest pair, offline decoder carrier and complete verifier. They are unchanged previously verified mechanisms plus new allowlist/group wiring; executing them would repeat unrelated RED proof. Execution must exercise the exact revised verifier, so its complete integration remains predicted.
- Created only disposable helper/scripts/proposed source and synthetic provider state/logs in the host task root; owned server/client trees stopped/reaped after the corrected check. Disposable source/state removed after artifact extraction; no test/source/config checkout file applied. No new container was started.

## Risks

- A port bind/startup/process failure must stop verification with diagnostics; no deadline increase or retry-until-pass is authorized. Server binds dynamic loopback itself, avoiding a reservation/rebind race for the provider.
- Provider callback remains active until its configured delay ends after cancellation; this is deliberately remote synthetic work. M03 still must implement local cancellation/reaping/admission release and cannot infer compliance from this diagnostic.
- The existing gateway test port reservation is retained; no unrelated fixture redesign. The final full revised verifier has not run in planning and remains an execution requirement.
- Self-check: new helper complete content; three modified files complete applicable diffs; no placeholders/pseudocode/dependency additions. Medium SZ2 retained for cohesive synthetic callback/check functions: splitting the single readable lifecycle would obscure ownership/order without reducing business complexity. No open High finding identified.

## Pre-authorized Contingencies

None.

## Rollback / Recovery

Reverse only the three exact test diffs and remove only the new helper if this milestone must be reverted, preserving all pre-existing dirty files. Never reset/clean the repository. Stop only PIDs/trees and the decoder carrier created by this verifier. A changed mechanism/file/assertion returns to planning.

## Explicitly Out of Scope

Production source or cancellation implementation; service/API/policy/contract changes; private keys/evidence/DB reads; live provider sockets; application state changes; new dependencies; decoder/version/startup changes; testing old inventories; staging, committing or GREEN014/live015 execution. This artifact does not approve the proposed Plan amendment or itself.

## Human Review

Status: Executed — verified 2026-11-11 (America/Chicago); see Plan.md AGW-M02A and [execution evidence](AGW-M02A-Execution-2026-11-11.md). Approved by user on 2026-11-11 jointly with the M02A Plan amendment. Exact test-harness correction only; no production implementation authorized.
