# Implementation Plan — Bounded Provider Response Correction RED

## Milestone and authorization boundary

ASOR-M08A, **RED**, work item `ai-screening-officer-review`. Prepared 2026-11-09–10, America/Chicago by the fresh-context implementation planner. Plan Status records user approval of the correction revision on 2026-11-09. M08A remains Blocked following the 2026-11-10 intake timeout and subsequent RED positive-control failure. The diagnostic fixture revision was applied and verified in the stopped execution. This checkpoint revision proposes only the remaining verification procedure. This artifact proposes tests/checks only. Planning-time observations are not execution evidence, approval, M08B implementation or permission for another live request.

## Authoritative references

- `requirements.md`: approved by user 2026-11-08. R01/current FastAPI/SQLite demo, R03/live provider, R05/officer referral on technical failure, R15/R16 durable background work and three total attempts; C05 correction does not replace the live acceptance criteria.
- `Plan.md`: correction revision approved in Status 2026-11-09; M08A RED/M08B GREEN order, scopes, traceability and execution table. Its retained revision-preparation prose/old “awaiting revised Plan approval” table text is historical; the main workflow's explicit Status approval is authority. No Plan text/status is changed here.
- `External-Contract.md`: user-approved M01 2026-11-08; CT15 consumed attempts, classification, one inference per attempt, recovery/no nested retries; CT16 absolute budget and key protection; CT17 safe observed HTTP status and sanitized private failure information. CT11–14 output/model policy remains unchanged. Full CT17/18 operational presentation/accounting remains M15/M16.
- Approved predecessor Implementation Plans `001_Implementation_Plan_Safe_Verification_Harness_OTHER.md`, `002_Implementation_Plan_Evidence_Intake_RED.md`, `003_Implementation_Plan_Evidence_Intake_GREEN.md`, `004_Implementation_Plan_Durable_Processing_RED.md`, `005_Implementation_Plan_Durable_Processing_GREEN.md`, `006_Implementation_Plan_Gemini_Assessment_RED.md`; M02–M07 executed and recorded in their 2026-11-09 execution reports. Their historical Pending introductions do not supersede actual execution evidence.
- `007_Implementation_Plan_Gemini_Assessment_GREEN.md`: approved/executed offline, live execution stopped; default factory/clock seams, fixed child process, stdin secret boundary, absolute deadline, HTTP mapping, raw usage/version capture and unchanged output validation are approved inputs. Its earlier scratch checks did not test real compressed HTTP framing.
- `ASOR-M08-Execution-2026-11-09.md`: actual unchanged offline pairs passed (47 Gemini, 14 durable, 94 intake with 12 existing skips); first authorized image failed `PROVIDER_REQUEST_REJECTED`, one consumed attempt, no assessment, awaiting-review/zero points. Remaining live images/video NOT RUN.
- `ASOR-M08-Live-Diagnosis-2026-11-09.md`: actual bounded metadata GET raised DecodingError; ordinary HTTPX metadata GETs returned 200. Child serialized decoded bytes with original gzip headers, independently reproducing double decoding. Metadata access proves neither upload/inference acceptance nor the original rejection cause, which is unknown.
- `Live-Verification-Setup.md`: user-requested input-preparation guide, not authorization for this milestone or a live retry. No designated key, supplied photos, private backup or old live scratch is inspected here.
- `.github/copilot-instructions.md`: inspected PDD guidance; its footer remains Awaiting approval and its stale stack facts are not runtime authority. No applicable AGENTS.md or product-level `docs/requirements.md` found. Current source/tests/configuration are factual inputs: durable.py, gemini.py, app.py, bootstrap.py, intake.py, requirements.txt, pytest.ini, Dockerfile, tests/conftest.py, the three unchanged launchers and their selected tests.
- Current production-engineering-standards **0.15.1** implementation-planning, prompt-driven-development, testing, security, resilience-and-degradation and its local-adapters reference, distributed-systems and llm-engineering instructions govern this preparation; they add no product requirements.

## Current repository and predecessor evidence

The checkout is dirty. Existing app.py/bootstrap.py and three prior harness tests are modified; durable.py/gemini.py/intake.py, predecessor tests/launchers and this work-item folder are untracked. Preserve current bytes; Git HEAD cannot reconstruct this baseline. No root pytest, checkout lifespan, real database connection/migration, private backup fixture or Google call is used.

durable.py `_GEMINI_HTTP_CHILD` uses the real HTTPX HTTPTransport(retries=0), redirects disabled/trust_env false, serializes response.content and all headers. BoundedTransport then reconstructs HTTPX Response from those already-decoded bytes and original encoding/framing headers. This code and the recorded diagnosis establish the gzip defect. There is no post-reconstruction deadline check. Gemini Worker records only generic failure codes; ai_attempts has no observed provider status/stage/class capture. Existing M07 Provider.client substitutes MockTransport and bypasses this child/parent path; its passing47 checks cannot establish framing integrity.

Carry 001–007 source-only copies, genuine managed schema/lifespan, effective DB/media cwd checks and closed-connection assertions; fixed dependency pins; explicit pytest-asyncio and disabled plugin autoload; provider/bootstrap environment stripping; UTF-8/no bytecode; dynamic Windows loopback ports; real synthetic photo fixture; fixed three consumed attempts; source-state hashes and owned cleanup forward. Native FFmpeg/ffprobe still use the approved003 verification-only forwarding through the existing network-none real decoder image for the unchanged synthetic preservation suites, never production configuration. Existing47/14 launcher90-second and intake180-second bounds remain byte-identical. Twelve old media skips provide no coverage, seven old API passes are setup-only, unrelated controls/OIDC infrastructure suites are unrun.

## Exact file scope and ordered proposed changes

The two M08A files are already applied. After approval, apply the exact fixture correction below to `tests/test_provider_response.py` only. Verify `tests/verify_provider_response.py` and the original approved production and preservation inputs against their recorded baselines. This 008 is the sole checkout write during planning. After approved verified RED execution, only the normal M08A execution evidence/status documentation is additionally permitted by PDD; this planning task does not write it.

1. Add actual-child framing tests for plain, gzip and chunked synthetic HTTP responses. Call the real unchanged default factory. A narrowly scoped Popen proxy validates the fixed child arguments and changes only the stdin URL from the fixed Google authority to an owned dynamically bound127.0.0.1 endpoint. The child code, HTTPTransport, real HTTPX decoding, serialized body/headers and parent reconstruction remain real. It cannot contact Google through this seam. Assert positive HTTP200/JSON, one real request/child, no retained encoding/transfer framing and content-length absent or equal to decoded body length.
2. Add five end-to-end consumed-attempt failures after a successful real-child assessment. Exercise upload-start400, upload-finalize403, file-poll429, generate503 and generate connection reset. Assert existing class/retry/referral/zero-point behavior, one attempt, at most one inference, keyed per-attempt safe metadata and no secret/body/prompt/private-path/token disclosure in persisted diagnostic rows or captured logs. Fresh workers are used after stopping the positive worker. An independent unknown-dispatch failure first proves the existing successful workflow, then requires explicit unknown status/stage with safe PROCESSING_ERROR.
3. Add parent-work deadline checks for serialization, process startup and response reconstruction, and real kill/reap checks with two sequential owned fixed sleeping children. Successful real HTTP checks cover the network path; the sleep check covers parent cancellation and lack of overlapping live children. It does **not** claim to test a real slow HTTP stream. No network timeout feature matrix is introduced.
4. Add a narrow standard-library launcher using the carried source-only/stripped-environment/cwd/lifespan infrastructure. Run exactly13 named nodes twice without cleaning between runs, inspect full JUnit inventory, reject setup/errors/skips/xfails and unexpected failures/passes, compare repeated inventories and protected snapshots, reap children and remove owned state. `--red` accepts only the nine specified business-failure markers with four preserved passes; `--green` requires all13 pass and is used only for scratch soundness now and a separately approved future GREEN.

## Explicit decisions for human review

- Retain `durable.gemini_client_factory() -> httpx.Client`, `gemini_monotonic() -> float` and all runtime settings/defaults. The new Popen proxy is a test-local fixture, not a new production seam or endpoint. It checks Google URL authority before remapping, carries headers/body privately over stdin, performs no inference outside loopback, and never replaces response construction with a corrected mock. The endpoint is controlled synthetic HTTP rather than TLS; existing HTTPS/host/resource validation remains protected by47 unchanged tests.
- Select **decoded bytes with normalized framing** as the expected private boundary invariant: remove Content-Encoding and Transfer-Encoding and remove or recompute Content-Length when transferring decoded bytes. A raw-byte transfer redesign is unnecessary for this cohesive correction. Gzip/chunked nodes are RED; plain is explicitly preserved. No broad HTTP feature matrix, dependency/configuration/operator setting is added.
- Select a **private nullable per-attempt capture table**, `ai_provider_diagnostics`, keyed `(job_id,number)`, with `provider_status`, `request_stage`, `diagnostic_class` as the minimum test-visible storage seam for later M08B. A separate table preserves existing positional ai_attempts inserts and all public serializers. Alternative additive attempt columns would touch those inserts and is not selected. M08B will separately review its exact additive migration/foreign-key/allowlist implementation; no schema/source scaffold enters RED. Retain old jobs/attempts and unknown historical values; never infer the original rejection's status/stage/cause.
- Exact internal vocabulary: stages `upload-start|upload-finalize|file-poll|generate|file-delete`, or null when unobserved; classes `HTTP_STATUS|NETWORK_ERROR|TIMEOUT|PROCESSING_ERROR`. Provider status integer actually observed or null. Only the primary unsuccessful request may determine this attempt's diagnostic: best-effort cleanup must not overwrite it. A generic unobserved dispatch exception stores `(null,null,PROCESSING_ERROR)`; a connection reset before HTTP headers stores `(null,generate,NETWORK_ERROR)`. Provider reason/message text is never a diagnostic class. Concurrent primary and cleanup failure is not a separate node. TIMEOUT vocabulary is reserved consistently with the existing mapping; this suite directly tests network reset and generic processing capture, while timeout capture itself is not separately parameterized.
- Use a 30-second synthetic attempt budget only for the five diagnostic cases that exercise consecutive real subprocesses. Set it on the test app's lifespan settings before either report is submitted, so both jobs snapshot the test value. Read the observation bound from those same app settings and add five seconds. The shared 10-second fixture, the standalone deadline and kill/reap tests, the absolute deadline logic and production settings stay unchanged. The worker still stops in finally.
- Diagnostics/log tests plant synthetic body, API-key, token URI, private-path, media and prompt sentinels. They require a positive assessment and classified failed consumed attempt before the negative privacy assertions. Only synthetic diagnostic rows are serialized for inspection; ordinary report descriptions/authorized assessment storage are outside the forbidden diagnostic/log channels. No raw real input is copied/read.

- **Verification-only intake decoder carrier on this Windows host:** preserve the same approved FFmpeg/ffprobe image, programs, synthetic stdin bytes, decoder flags and original `--intake` selection. The stopped attempt used the original 180-second bound. Start one unique, owned, automatically removed network-none/no-mount carrier and use `docker exec -i` for each decoder invocation, rather than launching a fresh container per decoder command. This measured startup optimization is limited to the external verification scripts below. `ASOR_DECODER_CARRIER` exists only in their child environment and is not an app/operator setting. Use only the known existing image with pull disabled; unexpected runtime/carrier failure stops verification. No production/container dependency or new fixture is introduced.

- **Clock seam exception limited to parent timing tests:** 006's assessment fixtures use only `gemini_monotonic`, never global time. That seam remains unchanged for assessment. The existing parent transport calls `time.monotonic()` directly, so the isolated no-lifespan parent-work nodes temporarily patch that clock in the pytest process to simulate elapsed serialization, startup or reconstruction; the separate fixed-protocol child and its actual subprocess handle stay real. `monkeypatch` restores the clock per node. No worker or loopback handler runs in those nodes. The alternatives are introducing a production seam before RED or relying on real sleeps for phase attribution, neither needed here. This is an explicit test-only review choice, not a change to the approved runtime seam or the original47 tests.

## Traceability and expected failure classes

| Approved rule / concern | Concrete nodes / evidence | Ownership |
| --- | --- | --- |
| C05, M08A framing integrity | framing[gzip], framing[chunked]: RESPONSE_FRAMING_MISSING from real child decoded-body/headers mismatch | Genuine RED; M08B owns correction |
| C05/CT17 minimal safe failure capture | five diagnostic_capture parameters + unobserved_diagnostic_stays_unknown: SAFE_DIAGNOSTIC_MISSING after real dispatch/classification | Genuine RED; private table choice above |
| C05/CT15–16 overall bound includes reconstruction | absolute_deadline[reconstruct]: ABSOLUTE_DEADLINE_MISSING | Genuine RED; no accepted late result |
| CT15–16 serialization/startup/kill/reap bounds | absolute_deadline[serialize/startup], real_timeout_kills_and_reaps_before_return | none — preserved; verifying M08A |
| C05 uncompressed consistency | framing[plain] | none — preserved; verifying M08A |
| CT15 classifications/no retry amplification/referral | diagnostic nodes assert original classification/retry-wait/count1/no more than1 generate, zero points, awaiting-review; unchanged47 and14 retain total3/recovery/late-result checks | none — preserved; verifying M08A |
| C05/CT17 body/key/token/path/media/prompt privacy | diagnostic nodes after positive dispatch and safe row assertions; unknown row exact null/null/class | Within capture correction; downstream reached by soundness probe |
| CT11–14 assessment/policy, CT15 durable total attempts, CT16 settings, CT03–05 intake | unchanged47/14/94+12 preservation pairs | Existing owning milestones preserved; no new normative behavior |
| CT17 full officer presentation/log schema; CT18 accounting, R18/C09 | Not implemented/tested here beyond minimal private capture/privacy; M15/M16 own full delivery | Explicit scope boundary |
| R03 live grounding, R05–R09 semantic policy/photo/video live criteria | Not tested by offline loopback; resumed M08 owns actual live evidence | No substitute closure or retry permission |

RED evidence is a **class of missing framing/capture/budget behavior**, not a predicted arbitrary failed SQL/import or one exact implementation return value. Table-presence assertions deliberately guard absent schema before querying it, yielding an intended assertion rather than a setup SQL exception. Downstream privacy checks cannot be claimed from RED alone; the separate scratch-only probe must pass them without weakening assertions.

## Acceptance / completion criteria — Expected / Predicted, not execution evidence

1. Verify both applied M08A files against the archived blocks, then apply and verify the exact diagnostic test revision below. The classifier stays byte-identical. No other test/source/config/dependency changes or status changes beyond PDD's verified execution documentation. No source scaffold, model substitute, real key/media/backup fixture, live retry or request-format guess.
2. The archived disposable launcher’s --red pair exits0 after each pytest child exits1 with precisely nine intended ordinary failures and four preserved passes, no errors/skips/xfails/timeouts, equal13-node inventories and all guards. Carry it forward only under the active checkpoint procedure. Every unexpected result stops; no assertion relaxation or rerun-until-pass.
3. Unchanged Gemini --green pair each47passes; durable --green pair each14passes; intake --intake pair each94passes/12pre-existing skips. Full repeated named inventories equal, effective fixture-path/closed-resource and source guards active, The archived Gemini pass used 90 seconds. The disposable Gemini checkpoint launcher and durable preservation launcher use a 180-second verification limit per child. The disposable provider RED and soundness launchers use 180 seconds per child. The intake verification copy uses 300 seconds per child under the procedure below. No new skip or accepted unrelated failure.
4. A separate scratch-only minimal production probe demonstrates all13 new nodes passing twice, including downstream metadata/privacy and failure classification after successful owned cleanup. That probe is soundness evidence only and never authorizes/checks in M08B implementation.
5. Exact revised test code derived, parsed and frozen in both verification copies. Compare the full original absolute-path/length/SHA-256 inventory, allowing only the documented 008 and test-file changes. Every owned child/server/decoder finishes; only owned contained scratch state is removed after archiving exact code/commands/output/inventories here. Real DB/media/private recovery remain untouched.

## Positive-control diagnosis and exact test revision

The [resume execution report](ASOR-M08A-Resume-Execution-2026-11-10.md) records the positive control returning `retry-wait` before the planned 503 was configured. The captured report omits the failure code and observed stages. `gemini.py` maps both attempt timeout and transient provider failures to retryable outcomes. The historical state alone leaves the specific cause unresolved.

A source-only diagnostic copy ran `python -m pytest -p pytest_asyncio.plugin -s -q tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS]` against the owned synthetic endpoint in three configurations. Exit 1 was expected in each case for the assertion indicated below. The scratch instrumentation printed only the failure code, known stage names and elapsed startup times. It injected 2.7 seconds immediately before each positive-control child spawn in the two delayed runs.

| Synthetic attempt budget | Injected startup delay | Positive control and pytest outcome |
| --- | --- | --- |
| 10 seconds | None | `completed`, no failure code, all five stages. Reached `SAFE_DIAGNOSTIC_MISSING`. |
| 10 seconds | 2.7 seconds per positive child | `retry-wait / ATTEMPT_TIMEOUT` after upload start and finalize. Failed at the positive assertion. |
| 30 seconds | Same 2.7 seconds | `completed`, no failure code, all five stages. Reached `SAFE_DIAGNOSTIC_MISSING` after the intended 503 classification and preservation assertions. |

The experiment reproduces the observed failure state through a startup-driven deadline exhaustion and shows that the revised test budget tolerates the same startup delay. The delay and timing instrumentation were confined to the disposable copy, which was removed. The proposed test revision retains real clocks, transport, subprocesses, all positive and negative assertions and the full 13-node inventory. Its positive assertion adds only the safe failure code and known stage names on failure.

Treat the two complete file blocks below as the byte-exact pre-revision baseline. After approval, confirm byte equality first. Save the following transformer in the owned verification root and pass the verified `tests/test_provider_response.py` path. First derive the proposed bytes in the disposable baseline and record the hashes. Apply the same transformation to the checkout test after confirming its original hash. The original test SHA-256 is `ff7776c163833b0b278d12475703e4849f79a27b1260988ceba3f64d9e888e73`. The revised test SHA-256 is `f614ff22f868dc6853f7b4320d00a5fe379845c9f241135d1287c1554ffbd9f4`. The unchanged classifier SHA-256 is `285278df42c8d7696f329acc00464dedec70751d58d4cc1ca9e35eeed6dea9a3`. Freeze and verify identical revised test bytes in both RED and scratch soundness copies. An unexpected byte mismatch stops verification.

~~~python
from hashlib import sha256
from pathlib import Path
import sys

path = Path(sys.argv[1])
original = path.read_bytes()
revised = original
for before, after in (
    (b"worker.adapter.config['AI_ATTEMPT_TIMEOUT_SECONDS']",
     b"runtime[0].app.state.ai_settings['AI_ATTEMPT_TIMEOUT_SECONDS']"),
    (b"    caplog.set_level(logging.DEBUG)",
     b"    monkeypatch.setitem(runtime[0].app.state.ai_settings, 'AI_ATTEMPT_TIMEOUT_SECONDS', 30)\n"
     b"    caplog.set_level(logging.DEBUG)"),
    (b"        assert positive['ai']['state'] == 'completed'",
     b"        assert positive['ai']['state'] == 'completed', (\n"
     b"            positive['ai']['failure_code'], [call[0] for call in state['calls']])"),
):
    assert revised.count(before) == 1
    revised = revised.replace(before, after)
compile(revised, str(path), "exec")
print(sha256(original).hexdigest(), sha256(revised).hexdigest())
path.write_bytes(revised)
~~~

Planning dry run with the exact revised fixture and the disposable 180-second provider launcher. `python tests/verify_provider_response_resume.py --red` exited 0. Its pytest children each exited 1, with nine intended failures and four preserved passes in 66.55 and 62.02 seconds. The classifier reported both complete 13-node inventories equal, with no errors or skips and the protected source/state unchanged. It reported both children reaped and its owned tree removed. The outer synthetic scratch tree was also removed. The archived pre-revision file blocks still match the checkout byte for byte. The test transformation reproduced the stated hash and the verification preparation code compiled. The intake carrier and soundness pair remain for approved execution.

## Active verification procedure — resume from the revised execution checkpoint

The [revised execution report](ASOR-M08A-Revised-Execution-2026-11-10.md) is the evidence source for both complete RED repetitions and Gemini repetition 1. Gemini repetition 2 supplied no inventory. Durable, intake and soundness have no matched checkpoint pairs. The sections below this active procedure retain the prior commands and exact support scripts as provenance.

1. From the checkout use its existing .venv interpreter and the literal direct Temp child C:\Users\avina\AppData\Local\Temp\asor-m08a-verify-20261110-8c13f901. Reject a pre-existing target, confirm its resolved parent is the intended Temp directory and reject reparse points. Create the empty root and extract the archived setup.py, decoder.py, decoder_carrier.py, run_intake_carrier.py, probe.py, prepare_intake_resume.py and check.py blocks as UTF-8 without BOM with LF line endings and a final newline. The setup commands below capture the private checkout inventory, build the source-only copy and forwarding wrappers, then reproduce the isolated probe and the existing provider/intake limits. The already-applied fixture must have the revised archived hash. Keep environment, checkout inventory, source-only setup and cleanup controls from the archived procedure.
2. Save the following block as checkpoint.py in the owned root. Run it with the report path as its only argument, before any test or decoder launch. It checks the full published manifest against the staged source files and temporary helper bytes, checks the actual forwarding wrappers and derives the exact launchers. Verify the report contains both classified RED inventories and the complete named Gemini pass before carrying either forward. Any missing or mismatched archived input stops checkpoint reuse and requires review of the verification baseline. The historical Gemini timeout and earlier missing-decoder invocation remain recorded failures of the verification setup.

~~~python
from hashlib import sha256
from pathlib import Path
import re
import sys

task = Path(__file__).resolve().parent
repo = task / "repository"
report = Path(sys.argv[1]).read_text(encoding="utf-8-sig")
manifest = report.split("## Frozen source inputs", 1)[1].split("```text", 1)[1].split("```", 1)[0]
rows = re.findall(r"^([0-9a-f]{64})  ([0-9]+)  (.+)$", manifest, re.MULTILINE)
assert len(rows) == len(manifest.strip().splitlines()) == 52
assert len({name for _, _, name in rows}) == len(rows)
for expected, length, name in rows:
    relative = name.removesuffix(" [disposable]")
    path = (task if "/" not in relative and name.endswith(" [disposable]") else repo) / relative
    data = path.read_bytes()
    assert len(data) == int(length) and sha256(data).hexdigest() == expected, relative

helper = task / "decoder.py"
assert helper.is_file() and sha256(helper.read_bytes()).hexdigest() == "c59f927dd2991f44173e6bff34a7dd53a37cfb33298819c31736207a4d1a08ce"
for tool in ("ffprobe", "ffmpeg"):
    expected = f'@"{sys.executable}" "{helper}" {tool} %*\n'
    assert (task / "bin" / (tool + ".cmd")).read_text() == expected, tool

for name in ("test_provider_response.py", "verify_provider_response.py", "verify_provider_response_resume.py"):
    assert (repo / "tests" / name).read_bytes() == (task / "probe-repository" / "tests" / name).read_bytes(), name

for suite in ("gemini_assessment", "durable_processing"):
    source = repo / "tests" / f"verify_{suite}.py"
    data = source.read_bytes()
    old_wait = b"child.wait(timeout=90)"
    assert data.count(old_wait) == 1
    data = data.replace(old_wait, b"child.wait(timeout=180)")
    if suite == "gemini_assessment":
        old_repeat = b"for repeat in (1, 2):"
        assert data.count(old_repeat) == 1
        data = data.replace(old_repeat, b"for repeat in (2,):")
        guard = b"Protected source/state unchanged; repeated inventories equal"
        assert data.count(guard) == 1
        data = data.replace(guard, b"Protected source/state unchanged; compare checkpoint inventory with archived run 1")
    target = source.with_stem(source.stem + "_checkpoint")
    compile(data, str(target), "exec")
    with target.open("xb") as output:
        output.write(data)
    print(target.name, len(data), sha256(data).hexdigest())
print("Frozen archived input hashes, decoder wrappers and identical provider test/classifier inputs verified")
~~~

3. Run these commands in order with the archived Windows loopback capability, existing interpreter and owned temporary environment. Use the same forwarding wrappers for Gemini, including the exact verified decoder.py. Record the explicit working directories and capture full output and child commands. Stop on an unexpected exit, outcome, skip, timeout, inventory or integrity difference.

~~~powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m08a-verify-20261110-8c13f901'
$python='C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe'
$report='C:\Users\avina\Downloads\avinash-repo\v11\Traffic\docs\.ai\ai-screening-officer-review\ASOR-M08A-Revised-Execution-2026-11-10.md'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& $python "$taskRoot\setup.py"
if($LASTEXITCODE -ne 0){throw 'Source-only setup failed'}
Set-Location -LiteralPath "$taskRoot\repository"
& $python "$taskRoot\probe.py"
if($LASTEXITCODE -ne 0){throw 'Soundness probe preparation failed'}
& $python "$taskRoot\prepare_intake_resume.py"
if($LASTEXITCODE -ne 0){throw 'Intake and provider launcher preparation failed'}
& $python "$taskRoot\checkpoint.py" $report
if($LASTEXITCODE -ne 0){throw 'Checkpoint input verification failed'}
function Get-FrozenSourceInventory {
    foreach ($copy in @('repository', 'probe-repository')) {
        Get-ChildItem -LiteralPath (Join-Path $taskRoot $copy) -File -Recurse -Force |
            Sort-Object FullName |
            ForEach-Object { '{0} {1} {2}' -f $_.FullName, $_.Length, (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
    }
}
$frozenBefore = @(Get-FrozenSourceInventory)
& $python tests\verify_gemini_assessment_checkpoint.py --green *> "$taskRoot\gemini-2.log"
if($LASTEXITCODE -ne 0){throw 'Gemini checkpoint repetition failed'}
~~~

Compare Gemini's 47 named passing outcomes against the archived Gemini repetition 1 before continuing. The archived launcher still validates the exact pytest selection, complete JUnit classification, source guard and child cleanup. The 180-second outer verification limit is twice the observed 90-second cutoff and provides headroom over the completed 67.98-second run. Give durable the same finite limit because it runs in the same Windows subprocess environment and its current pair has no recorded timing. The provider soundness limit remains 180 seconds, intake remains 300 seconds and its carrier lifetime remains 720 seconds. These limits govern disposable verification processes only. The approved test-local 30-second positive-control budget and production/runtime deadlines retain their existing values.

~~~powershell
& $python tests\verify_durable_processing_checkpoint.py --green *> "$taskRoot\durable.log"
if($LASTEXITCODE -ne 0){throw 'Durable preservation failed'}
& $python "$taskRoot\run_intake_resume.py" *> "$taskRoot\intake-carrier-driver.log"
if($LASTEXITCODE -ne 0){throw 'Intake preservation failed'}
Set-Location -LiteralPath "$taskRoot\probe-repository"
& $python tests\verify_provider_response_resume.py --green *> "$taskRoot\soundness.log"
if($LASTEXITCODE -ne 0){throw 'Scratch soundness verification failed'}
& $python "$taskRoot\check.py"
if($LASTEXITCODE -ne 0){throw 'Original checkout integrity verification failed'}
$frozenAfter = @(Get-FrozenSourceInventory)
if (Compare-Object -ReferenceObject $frozenBefore -DifferenceObject $frozenAfter) {
    throw 'Frozen source inventory changed'
}
~~~

4. Require two complete matching durable inventories with 14 passes each, two complete matching intake inventories with 94 passes and the same 12 archived skips, and two complete matching soundness inventories with all 13 passing. Check the named outcomes against the inventories archived below. Run the archived check.py from the owned root to compare the independent original checkout inventory and baseline/probe inputs before writing milestone records. Independently compare the complete frozen scratch inventory captured after checkpoint preparation against the post-run inventory. Archive the matched provenance, actual commands, results, named inventories, source guards, deviations and cleanup evidence. Confirm all owned processes and the intake carrier are absent and remove only the verified literal disposable root. Keep all original launchers and production files byte-identical. The checkout fixture requires no further change.

Planning mechanical check. Extracted and compiled the exact Python blocks in a disposable copy, ran setup.py, probe.py, prepare_intake_resume.py and checkpoint.py, and parsed the PowerShell blocks. All 52 published input rows, decoder wrappers and the matched provider fixture and classifier bytes passed. Gemini's derived launcher SHA-256 is `196dcf1dde5b5c324a7b448757be918c5d1f20c757fb2a61c3ebad1d07ac4598`. Durable's is `b3b0a43c6712fb83df8d69e787af086250533f494edfdf3cea13e90edf5c0182`. The mechanical check launched no pytest, decoder, app or carrier process.

## Historical verification commands and isolation

See [the stopped execution record](ASOR-M08A-Execution-2026-11-10.md). Both correction RED runs and both Gemini and durable runs passed their respective verification criteria. Intake run 1 passed 94 with 12 existing skips in 149.64 seconds. Run 2 timed out at 180 seconds after 100 of 106 outcomes. The scratch soundness launcher was not started. The 300-second intake child limit adds 120 seconds of headroom over the observed timeout. An unexpected result still stops verification.

Use the approved 003 source-only setup and real-decoder forwarding from the literal direct Temp child `C:\Users\avina\AppData\Local\Temp\asor-m08a-verify-20261110-8c13f901`. Reject a pre-existing target, verify the direct Temp parent and absence of reparse points, and capture the original absolute path/length/SHA-256 inventory. Exclude only .git, .venv and transient caches and keep private metadata unpublished. Copy only root Python files, pytest.ini, tests, templates and static. Verify the archived original test and launcher bytes before applying the exact test revision. The previous RED pair covered a different fixture. Rerun the provider RED pair from the revised disposable repository with the 180-second variant below and require both full inventories to classify. The exact revised test reached the fifth diagnostic parameter in a planning dry run before the original 90-second child limit stopped it. The owned directory was initially held open after timeout on Windows. A follow-up process check found no remaining matching Python process and verified removal of the owned directory. This timed-out run supplies no RED inventory. Carry forward the successful Gemini and durable pairs only if the recorded evidence and protected inputs establish the same baseline for those unchanged selections. Otherwise rerun the affected unchanged pair with its original launcher, arguments and 90-second child bound before intake.

Extract the archived `decoder_carrier.py`, `run_intake_carrier.py`, and `probe.py` as specified below. Before freezing, use the following exact preparation script as `prepare_intake_resume.py` in the owned root. It derives the one-line intake variant beside the original launcher in the disposable repository so its repository-root and snapshot logic still applies. It also derives an identical 180-second provider variant in both disposable repositories. The provider variant changes only the launcher wait, preserving the exact selection, classifier and test deadlines. The driver uses the same carrier image and restrictions. Its fixed lifetime is 720 seconds to cover two 300-second children and setup and cleanup overhead. The prior driver block remains the historical record of the 180-second run.

~~~python
from pathlib import Path

task = Path(__file__).resolve().parent
tests = task / "repository" / "tests"
original = tests / "verify_current_demo.py"
data = original.read_bytes()
old = b'child.wait(timeout=180 if phase == "intake" else 90)'
new = b'child.wait(timeout=300 if phase == "intake" else 90)'
assert data.count(old) == 1
variant = data.replace(old, new)
assert variant.count(new) == 1 and variant.replace(new, old) == data
compile(variant, str(original), "exec")
with (tests / "verify_current_demo_resume.py").open("xb") as output:
    output.write(variant)

for repository in ("repository", "probe-repository"):
    tests = task / repository / "tests"
    original = tests / "verify_provider_response.py"
    data = original.read_bytes()
    old = b"child.wait(timeout=90)"
    new = b"child.wait(timeout=180)"
    assert data.count(old) == 1
    variant = data.replace(old, new)
    assert variant.count(new) == 1 and variant.replace(new, old) == data
    compile(variant, str(original), "exec")
    with (tests / "verify_provider_response_resume.py").open("xb") as output:
        output.write(variant)

driver = (task / "run_intake_carrier.py").read_bytes()
for before, after in (
    (b"asor-m08a-intake-8c13b0a4", b"asor-m08a-intake-8c13f901"),
    (b"'480']", b"'720']"),
    (b"tests/verify_current_demo.py", b"tests/verify_current_demo_resume.py"),
    (b"Unchanged intake launcher exit", b"Intake verification copy exit"),
):
    assert driver.count(before) == 1
    driver = driver.replace(before, after)
compile(driver, "run_intake_resume.py", "exec")
with (task / "run_intake_resume.py").open("xb") as output:
    output.write(driver)
~~~

Use expanded native Windows loopback capability with explicit disposable working directories. Build the soundness copy from the source-only baseline before adding the intake launcher variant. The archived `probe.py` creates the separate `probe-repository` from the source-only baseline and applies its minimal transformation there. Verify that the revised test and original classifier match the frozen baseline in the probe copy.

~~~powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m08a-verify-20261110-8c13f901'
$python='C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
Set-Location -LiteralPath "$taskRoot\repository"
& $python "$taskRoot\probe.py"
if($LASTEXITCODE -ne 0){throw 'Soundness probe preparation failed'}
& $python "$taskRoot\prepare_intake_resume.py"
if($LASTEXITCODE -ne 0){throw 'Intake verification preparation failed'}
# Freeze and record input hashes here, including the revised test and all launcher variants.
& $python tests\verify_provider_response_resume.py --red *> "$taskRoot\red.log"
if($LASTEXITCODE -ne 0){throw 'Revised RED verification failed'}
& $python "$taskRoot\run_intake_resume.py" *> "$taskRoot\intake-carrier-driver.log"
if($LASTEXITCODE -ne 0){throw 'Intake preservation failed'}
Set-Location -LiteralPath "$taskRoot\probe-repository"
& $python tests\verify_provider_response_resume.py --green *> "$taskRoot\soundness.log"
if($LASTEXITCODE -ne 0){throw 'Scratch soundness verification failed'}
~~~

Run the intake pair from its first repetition in one invocation with no intervening cleanup. Both children must exit 0 with the same complete 106-node inventory (94 passes and exactly the 12 existing skips). Verify full named outcomes against the recorded complete intake inventory, launcher source guards, and independent original checkout inventory. The separate soundness pair must exit 0 with both complete 13-node inventories passing and its guards intact. Archive actual commands, deviations, results, named inventories, source-integrity comparisons and cleanup evidence in a linked execution report. Verify the carrier and owned child processes are absent and remove only the verified disposable root after archiving. No root pytest/lifespan, environment installation, live provider, supplied media or backup access.

## Risks, rollback and exclusions

No pre-authorized contingency. Missing owned-loopback/decoder capability, unexpected failure/flakiness, absent source seam or conflicting contract stops execution for review; The disposable variants use 180 seconds per provider child and 300 seconds per intake child. Every assertion and selection is retained. The test-local URL remap covers real HTTP/content decoding/process transfer, not TLS certificate behavior or arbitrary protocol permutations. Fixed-child cancellation is a real process test, not proof of remote billing cancellation or a slow-stream integration test. Existing original live rejection remains unknown; gzip diagnosis is distinct. Minimal capture does not deliver full CT17/18 operational UI/logging/accounting.

If rolling back this fixture revision, compare the test to the frozen revised bytes and restore only its archived pre-revision bytes. If rolling back the original RED milestone too, remove the two M08A files only after comparing them to the archived approved originals. Preserve all other dirty work. RED creates no production schema or real data requiring downgrade. No Git reset/clean, global Temp cleanup, private recovery deletion, retry/model/output policy change or new SDK/configuration/dependency is proposed. M08B and resumed M08 each still require a separate reviewed Implementation Plan.

## Archived exact pre-revision code
### tests/test_provider_response.py — original complete file

~~~python
"""ASOR-M08A: actual bounded HTTP child, synthetic owned loopback only."""
import base64
from contextlib import contextmanager
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
import socket
import subprocess
import threading
import time
from urllib.parse import urlsplit

import httpx
import pytest

from tests.test_gemini_assessment import assessment_runtime, submit, output, positive, HOST, KEY

SENTINELS = ('PRIVATE_BODY_SENTINEL', 'PRIVATE_TOKEN_SENTINEL',
             'C:/synthetic-private/evidence.jpg', 'PRIVATE_MEDIA_SENTINEL',
             'PRIVATE_PROMPT_SENTINEL', KEY)
STAGES = {'upload-start', 'upload-finalize', 'file-poll', 'generate', 'file-delete'}
CLASSES = {'HTTP_STATUS', 'NETWORK_ERROR', 'TIMEOUT', 'PROCESSING_ERROR'}


def run(runtime, report_id):
    # Real process startup consumes the configured budget; observe up to that
    # budget plus five seconds for scheduler/test bookkeeping, without extending it.
    from tests.test_durable_processing import OFFICER
    worker = runtime[4][-1]
    worker.start()
    try:
        assert worker.wait_idle(worker.adapter.config['AI_ATTEMPT_TIMEOUT_SECONDS'] + 5), 'Owned worker did not become idle'
    finally:
        worker.stop()
    response = runtime[0].get('/api/authority/reports/' + report_id, headers=OFFICER)
    assert response.status_code == 200
    return response.json()

@contextmanager
def endpoint():
    state = dict(calls=[], mode='plain', fail_stage=None, status=400, value=None)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def handle_call(self):
            body = self.rfile.read(int(self.headers.get('Content-Length', '0')))
            path = urlsplit(self.path).path
            stage = ('file-delete' if self.command == 'DELETE' else
                     'upload-start' if path == '/upload/v1beta/files' else
                     'upload-finalize' if path.startswith('/upload/session/') else
                     'file-poll' if path.startswith('/v1beta/files/') else 'generate')
            state['calls'].append((stage, body, self.headers.get('x-goog-api-key')))
            if stage == state['fail_stage'] and state['status'] == 'reset':
                self.connection.shutdown(socket.SHUT_RDWR)
                self.connection.close()
                return
            headers = {}
            status = 200
            if stage == state['fail_stage']:
                status = state['status']
                payload = {'error': {'message': ' '.join(SENTINELS)}}
                headers['Retry-After'] = '17'
            elif stage == 'upload-start':
                payload = {}
                headers['x-goog-upload-url'] = 'https://' + HOST + '/upload/session/PRIVATE_TOKEN_SENTINEL'
            elif stage in ('upload-finalize', 'file-poll'):
                value = {'name': 'files/synthetic', 'uri': 'https://' + HOST + '/v1beta/files/synthetic',
                         'state': 'PROCESSING' if stage == 'upload-finalize' else 'ACTIVE'}
                payload = {'file': value} if stage == 'upload-finalize' else value
            elif stage == 'generate':
                state['prompt'] = json.loads(body) if body else {}
                payload = {'candidates': [{'finishReason': 'STOP', 'content': {'parts': [
                    {'text': json.dumps(state['value'])}]}}]}
            else:
                payload = {}
            raw = json.dumps(payload).encode()
            if state['mode'] == 'gzip':
                raw = gzip.compress(raw)
                headers['Content-Encoding'] = 'gzip'
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            for key, value in headers.items(): self.send_header(key, value)
            # Exercise chunk framing as well as compressed Content-Length.
            if state['mode'] == 'chunked':
                self.send_header('Transfer-Encoding', 'chunked')
                self.end_headers()
                self.wfile.write(('%x\r\n' % len(raw)).encode() + raw + b'\r\n0\r\n\r\n')
            else:
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
        do_GET = do_POST = do_DELETE = handle_call
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    state['base'] = 'http://127.0.0.1:' + str(server.server_port)
    try:
        yield state
    finally:
        server.shutdown(); server.server_close(); thread.join(5)
        assert not thread.is_alive()


@contextmanager
def remap_child(monkeypatch, state):
    """Keep fixed child code/real transport; redirect only stdin URL to our socket."""
    import durable
    real = subprocess.Popen
    children = []
    class Owned:
        def __init__(self, args, **kwargs):
            assert args[-1] == durable._GEMINI_HTTP_CHILD
            assert args[1:4] == ['-I', '-B', '-c']
            self.child = real(args, **kwargs)
            children.append(self.child)
        def communicate(self, payload=None, **kwargs):
            if payload is not None:
                value = json.loads(payload)
                url = urlsplit(value['url'])
                assert url.scheme == 'https' and url.netloc == HOST
                value['url'] = state['base'] + url.path
                if url.query: value['url'] += '?' + url.query
                payload = json.dumps(value).encode()
            return self.child.communicate(payload, **kwargs)
        def __getattr__(self, name):
            return getattr(self.child, name)
    monkeypatch.setattr(subprocess, 'Popen', Owned)
    try:
        yield children
    finally:
        for child in children:
            if child.poll() is None:
                child.kill(); child.communicate()
            assert child.poll() is not None


@pytest.mark.parametrize('mode', ['plain', 'gzip', 'chunked'])
def test_real_child_response_framing(monkeypatch, mode):
    import durable
    with endpoint() as state, remap_child(monkeypatch, state) as children:
        state['mode'] = mode
        state['value'] = {'synthetic': True}
        with durable.gemini_client_factory() as client:
            try:
                response = client.post('https://' + HOST + '/generate',
                    extensions={'asor_deadline': time.monotonic() + 8})
            except httpx.DecodingError:
                pytest.fail('RESPONSE_FRAMING_MISSING: decoded bytes were decoded again')
        assert response.status_code == 200 and response.json()['candidates']
        assert len(state['calls']) == len(children) == 1
        assert response.headers.get('Content-Encoding', 'identity') == 'identity', 'RESPONSE_FRAMING_MISSING'
        assert 'Transfer-Encoding' not in response.headers, 'RESPONSE_FRAMING_MISSING'
        assert ('Content-Length' not in response.headers or
                int(response.headers['Content-Length']) == len(response.content)), 'RESPONSE_FRAMING_MISSING'


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
    caplog.set_level(logging.DEBUG)
    with endpoint() as state, remap_child(monkeypatch, state) as children:
        report_id, job_id, ids, _ = submit(runtime, key='positive-boundary')
        state['value'] = output(ids)
        positive = run(runtime, report_id)
        assert positive['ai']['state'] == 'completed'
        assert [x[0] for x in state['calls']] == ['upload-start', 'upload-finalize', 'file-poll', 'generate', 'file-delete']
        state['calls'].clear()
        runtime[4].append(runtime[5](runtime[2] / 'roadwatch.db'))
        state.update(fail_stage=stage, status=status)
        report_id, job_id, ids, _ = submit(runtime, key='failed-boundary')
        state['value'] = output(ids)
        body = run(runtime, report_id)
        assert body['ai']['attempt_count'] == 1
        assert body['ai']['state'] == ('retry-wait' if code == 'PROVIDER_TRANSIENT' else 'failed')
        assert body['ai']['failure_code'] == code
        assert body['status'] == 'awaiting-review'
        db = runtime[1]
        assert db.execute('SELECT provisional_points FROM reports WHERE id=?', (report_id,)).fetchone()[0] == 0
        assert sum(x[0] == 'generate' for x in state['calls']) <= 1
        assert all(x[2] == KEY for x in state['calls'])
        assert all(child.poll() is not None for child in children)
        # Guard before querying absent schema: intentional RED, never SQL setup error.
        assert db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='ai_provider_diagnostics'").fetchone(), 'SAFE_DIAGNOSTIC_MISSING'
        rows = db.execute('SELECT provider_status,request_stage,diagnostic_class FROM ai_provider_diagnostics WHERE job_id=? AND number=1', (job_id,)).fetchall()
        assert len(rows) == 1, 'SAFE_DIAGNOSTIC_MISSING'
        assert tuple(rows[0]) == (None if status == 'reset' else status, stage, kind), 'SAFE_DIAGNOSTIC_MISSING'
        assert rows[0][1] in STAGES and rows[0][2] in CLASSES
        # Only synthetic DB; inspect persisted diagnostic content and captured logs.
        text = json.dumps([tuple(row) for row in db.execute('SELECT * FROM ai_provider_diagnostics')]) + caplog.text
        for secret in (*SENTINELS, gemini.PROMPT, str(runtime[2])):
            assert secret not in text, 'UNSAFE_DIAGNOSTIC_DETAIL'


def test_unobserved_diagnostic_stays_unknown(assessment_runtime, monkeypatch):
    import gemini
    runtime = assessment_runtime
    positive(runtime)
    runtime[4].append(runtime[5](runtime[2] / 'roadwatch.db'))
    report_id, job_id, _, _ = submit(runtime, key='unknown-boundary')
    def fail(prepared):
        raise RuntimeError(' '.join(SENTINELS))
    monkeypatch.setattr(runtime[4][-1].adapter, 'dispatch', fail)
    body = run(runtime, report_id)
    assert body['ai']['failure_code'] == 'PROCESSING_ERROR' and body['ai']['attempt_count'] == 1
    db = runtime[1]
    assert db.execute("SELECT 1 FROM sqlite_master WHERE name='ai_provider_diagnostics'").fetchone(), 'SAFE_DIAGNOSTIC_MISSING'
    rows = db.execute('SELECT provider_status,request_stage,diagnostic_class FROM ai_provider_diagnostics WHERE job_id=? AND number=1', (job_id,)).fetchall()
    assert [tuple(x) for x in rows] == [(None, None, 'PROCESSING_ERROR')], 'SAFE_DIAGNOSTIC_MISSING'


@pytest.mark.parametrize('phase', ['serialize', 'startup', 'reconstruct'])
def test_absolute_deadline_covers_parent_work(monkeypatch, phase):
    import durable
    real_dumps, real_loads = json.dumps, json.loads
    real_popen = subprocess.Popen
    now = time.monotonic()
    clock = [now]
    monkeypatch.setattr(time, 'monotonic', lambda: clock[0])
    children = []
    def dumps(value, *args, **kwargs):
        result = real_dumps(value, *args, **kwargs)
        if phase == 'serialize': clock[0] += 2
        return result
    def loads(value, *args, **kwargs):
        result = real_loads(value, *args, **kwargs)
        if phase == 'reconstruct': clock[0] += 2
        return result
    def popen(args, **kwargs):
        child = real_popen(args, **kwargs); children.append(child)
        if phase == 'startup': clock[0] += 2
        return child
    monkeypatch.setattr(json, 'dumps', dumps)
    monkeypatch.setattr(json, 'loads', loads)
    monkeypatch.setattr(subprocess, 'Popen', popen)
    # Faithful child output, only for parent timing; framing uses real HTTP above.
    monkeypatch.setattr(durable, '_GEMINI_HTTP_CHILD', "import sys; sys.stdin.buffer.read(); sys.stdout.write('{\"status\":200,\"headers\":[],\"content\":\"e30=\"}')")
    with durable.gemini_client_factory() as client:
        try:
            client.post('https://' + HOST + '/timing', extensions={'asor_deadline': now + 1})
        except httpx.TimeoutException:
            pass
        else:
            pytest.fail('ABSOLUTE_DEADLINE_MISSING')
    assert len(children) == (0 if phase == 'serialize' else 1)
    assert all(p.poll() is not None for p in children)


def test_real_timeout_kills_and_reaps_before_return(monkeypatch):
    import durable
    real = subprocess.Popen
    children = []
    def popen(args, **kwargs):
        child = real(args, **kwargs); children.append(child); return child
    monkeypatch.setattr(subprocess, 'Popen', popen)
    monkeypatch.setattr(durable, '_GEMINI_HTTP_CHILD', 'import time; time.sleep(20)')
    with durable.gemini_client_factory() as client:
        for _ in range(2):
            with pytest.raises(httpx.TimeoutException):
                client.post('https://' + HOST + '/owned-no-network',
                    extensions={'asor_deadline': time.monotonic() + .25})
            assert children and all(p.poll() is not None for p in children)
    assert len(children) == 2


import durable as _durable
DEFAULT_FACTORY = _durable.gemini_client_factory
~~~

### tests/verify_provider_response.py — complete new file

~~~python
"""ASOR-M08A: classify intended correction RED and preserved nodes separately."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ["tests/test_provider_response.py"]
PRESERVED = {"test_real_child_response_framing[plain]",
    "test_absolute_deadline_covers_parent_work[serialize]",
    "test_absolute_deadline_covers_parent_work[startup]",
    "test_real_timeout_kills_and_reaps_before_return"}
RED = {"test_real_child_response_framing[gzip]": "RESPONSE_FRAMING_MISSING",
    "test_real_child_response_framing[chunked]": "RESPONSE_FRAMING_MISSING",
    "test_attempt_diagnostic_capture[upload-start-400-PROVIDER_REQUEST_REJECTED-HTTP_STATUS]": "SAFE_DIAGNOSTIC_MISSING",
    "test_attempt_diagnostic_capture[upload-finalize-403-PROVIDER_CONFIGURATION-HTTP_STATUS]": "SAFE_DIAGNOSTIC_MISSING",
    "test_attempt_diagnostic_capture[file-poll-429-PROVIDER_TRANSIENT-HTTP_STATUS]": "SAFE_DIAGNOSTIC_MISSING",
    "test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS]": "SAFE_DIAGNOSTIC_MISSING",
    "test_attempt_diagnostic_capture[generate-reset-PROVIDER_TRANSIENT-NETWORK_ERROR]": "SAFE_DIAGNOSTIC_MISSING",
    "test_unobserved_diagnostic_stays_unknown": "SAFE_DIAGNOSTIC_MISSING",
    "test_absolute_deadline_covers_parent_work[reconstruct]": "ABSOLUTE_DEADLINE_MISSING"}
EXPECTED = PRESERVED | set(RED)


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
        assert case.attrib.get("classname") == "tests.test_provider_response"
        assert case.find("error") is None, "Setup/teardown error is not RED"
        assert case.find("skipped") is None, "No skips/xfails accepted"
        failure = case.find("failure")
        name = case.attrib["name"]
        if mode == "red" and name in RED:
            assert failure is not None, "Unexpected passing RED node"
            detail = failure.attrib.get("message", "") + (failure.text or "")
            assert RED[name] in detail, detail
            assert "AssertionError" in detail or "Failed:" in detail, detail
        else:
            assert failure is None, failure.text if failure is not None else ""
        inventory.append((case.attrib["name"], "failed" if failure is not None else "passed"))
    print("Classified", len(cases), mode, "nodes; no errors/skips", flush=True)
    return sorted(inventory)


def main():
    if sys.argv[1:] not in (["--red"], ["--green"]):
        raise SystemExit("Usage: verify_provider_response.py --red|--green")
    mode = sys.argv[1][2:]
    before = snapshot()
    temp_root = Path(tempfile.gettempdir()).resolve()
    with tempfile.TemporaryDirectory(prefix="asor-m08a-") as name:
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

~~~

## Planning-time dry run — actual observations, not milestone execution

Created the owned stable host-visible area `C:\Users\avina\AppData\Local\Temp\asor-m08a-plan-20261109-8c13b0a4`, source-only baseline/probe copies, scripts/bin/temporary state and synthetic verification logs, self-cleaning launcher trees, and one separately identified one-node diagnostic pytest tree. No real DB/media/.local/.env/.git/.venv or recovery backup entered fixtures. Native interpreter/dependencies unchanged. The final new files and production baseline were frozen before final pairs; no source/test/config edits occurred during any final verification child. The document was prepared separately while verification ran.

Actual setup: `& .\.venv\Scripts\python.exe C:\Users\avina\AppData\Local\Temp\asor-m08a-plan-20261109-8c13b0a4\setup.py` with PYTHONUTF8=1/PYTHONDONTWRITEBYTECODE=1. Actual final commands below used the explicit disposable repository cwd and expanded Windows loopback capability. The probe uses its separate probe-repository cwd. Each launcher internally repeats; the preservation driver invokes unchanged launchers sequentially with the carried real-decoder PATH and owned TMP/TEMP/TMPDIR.

~~~powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m08a-plan-20261109-8c13b0a4'
$python='C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe'
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
# source-only probe setup, separate from the frozen baseline
& $python "$taskRoot\probe.py"
# cwd: $taskRoot\repository; expanded native Windows loopback
& $python tests\verify_provider_response.py --red *> "$taskRoot\red-reviewed.log"
# cwd: $taskRoot\probe-repository; expanded native Windows loopback
& $python tests\verify_provider_response.py --green *> "$taskRoot\probe-reviewed.log"
# cwd: $taskRoot\repository; expanded loopback / approved synthetic decoders
& $python "$taskRoot\preserve.py"
# only the affected unchanged intake pair, after measured decoder startup correction
& $python "$taskRoot\run_intake_carrier.py"
# independent original checkout / frozen-code checks
& $python "$taskRoot\check.py"
~~~

Both final correction launcher invocations captured `$result=$LASTEXITCODE`, displayed their trimmed tails and exited with that result. The preservation driver records actual commands, working directories and return codes, stopping on any nonzero exit. The probe was constructed before the final RED/probe pairs and its final identical new helper copied while all test processes were stopped; `probe.py` archives the original minimal production transformation, and the complete current exact two-file blocks are the final test/helper inputs to both copies. Setup was not rerun on an existing target. Final RED/probe/Gemini/durable and the environment-corrected intake launcher exited0. The initial intake invocation failed at its unchanged timeout, recorded below. Actual trimmed output:

~~~text
Correction RED13
red run 1 exit 1
=================== 9 failed, 4 passed, 1 warning in 57.17s ===================
Classified 13 red nodes; no errors/skips
red run 2 exit 1
=================== 9 failed, 4 passed, 1 warning in 57.72s ===================
Classified 13 red nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
Correction scratch soundness13
green run 1 exit 0
======================= 13 passed, 1 warning in 56.30s ========================
Classified 13 green nodes; no errors/skips
green run 2 exit 0
======================= 13 passed, 1 warning in 55.59s ========================
Classified 13 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
Unchanged Gemini47
green run 1 exit 0
================== 47 passed, 1 warning in 62.33s (0:01:02) ===================
Classified 47 green nodes; no errors/skips
green run 2 exit 0
======================= 47 passed, 1 warning in 53.91s ========================
Classified 47 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
Unchanged durable14
green run 1 exit 0
======================= 14 passed, 1 warning in 21.89s ========================
Classified 14 green nodes; no errors/skips
green run 2 exit 0
======================= 14 passed, 1 warning in 22.59s ========================
Classified 14 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
Unchanged intake106, decoder carrier
intake run 1 result: 0
============ 94 passed, 12 skipped, 1 warning in 130.99s (0:02:10) ============
intake run 2 result: 0
============ 94 passed, 12 skipped, 1 warning in 158.37s (0:02:38) ============
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
~~~

No unexpected failure/error/skip/xfail/timeout was accepted in final evidence. Existing Starlette/httpx deprecation warning remains; it is not a dependency-upgrade request. Full repeated inventories follow, with twelve unchanged legacy skips visibly distinguished. All positive/negative diagnostic and privacy assertions passed in the scratch probe without modification. The minimal probe normalizes decoded framing, checks reconstruction deadline and captures only fixed status/stage/class in a private table; it changes no validation, classification, retry policy or public representation.

### Initial failed invocations and corrections — retained honestly

1. Initial restricted `python -m pytest -p pytest_asyncio.plugin -v tests/test_provider_response.py --junitxml=...\initial.xml` used the owned repository/TMP and stalled after three failed framing nodes. It was interrupted and its owned processes reaped. This was not accepted as RED or proof of environment behavior. Expanded Windows loopback was used for all conclusive verification, as required by001's recorded socket prerequisite.
2. First expanded draft launcher `tests\verify_provider_response.py --red` exited1: **10 failed/3 passed,57.47s**. The classifier correctly rejected plain framing and worker-idle failures. A standalone owned-loopback child probe showed RemoteProtocolError because the synthetic handler tried JSON-decoding an empty POST. Corrected the handler to accept the empty direct framing POST. No production change.
3. An expanded one-node diagnostic invocation `python -m pytest -p pytest_asyncio.plugin -x -vv -s tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-start-400-PROVIDER_REQUEST_REJECTED-HTTP_STATUS]` failed the inherited5second idle assertion (**1failed,11.26s**). Its positive real child workflow had completed, then the target reused a stopped worker. Source evidence: Worker.stop sets stopping, Worker.start does not reset it; predecessor check_target explicitly appends a fresh factory worker. Added that fresh-worker step before the target. One generated `pytest-of-avina/pytest-766/test_attempt_diagnostic_captur0` tree was positively identified as this exact one-node invocation and was independently absent at final inspection; no shared pytest root or older run was deleted.
4. With fresh workers, the first13-node RED pair classified9intended failures/4preserved passes (49.21s/46.66s). A first scratch probe then produced **11passed/2failed,43.46s**, both at positive real-workflow wait_idle(5). Five real subprocess startups consumed more than that observation allowance. This is a test-harness defect, not a product failure or acceptable flake. Corrected only the new test helper to wait the effective configured10second attempt plus5seconds observation/bookkeeping, always stop in finally. Original47 helper, production deadline and90/180bounds stay unchanged. The final exact RED/probe pairs above supersede these draft checks; product assertions remain unchanged.
5. One combined probe setup/run tool call failed before dispatch with Windows error267 because its requested probe cwd did not exist yet. Created the separate source copy first, then invoked from its existing cwd. No test ran in that failed invocation.
6. The first unchanged intake command under the inherited standalone-container forwarding returned `intake run 1 result: TIMEOUT` at its original180second limit. It had completed **84passed/12existing skips** out of106, with `test_report_validation_does_not_consume_upload[duplicate]` in progress and ten node outcomes unverified. The second child did not run. No failing business assertion was captured; child reaped, source integrity guard passed, nested disposable state removed. Original M08 recorded127.59s/142.95s; the current host slowdown's sole cause is unproven. Measured a concrete independent decoder-startup cost before changing environment: three standalone FFprobe invocations took1103/1107/973ms vs715/633/537ms for `docker exec` in an owned network-none carrier with identical `-version` output (`7.1.5-0+deb13u1`). The command was `docker run --rm --network none --pull never --entrypoint /usr/bin/ffprobe traffic-60e6e567315a-runner:latest -version` versus `docker exec <owned carrier id> /usr/bin/ffprobe -version`; the temporary timing carrier was stopped and absent. The measured difference justified a narrower verification-only change to the per-command startup mechanics, not an asserted root cause or relaxed budget. Ran only the affected intake pair once with the exact owned carrier scripts below; original selection/source/flags/bytes,90/180bounds and acceptance counts remained intact. The final carrier reported `network none; mounts 0`, then stopped and was independently absent. No other pair was repeated for this environment correction.

No automatic approval rejection occurred. None of these failures was suppressed or mislabelled intended business RED. No Google request, use or inspection of a key value, user-photo access, private backup access, checkout source fix or live retry occurred. The private integrity comparison uses only path/length/one-way hashes and publishes none of those private records.

## Full repeated named inventories

Each complete list below was independently captured twice with identical node/status order. Counts are verified against the actual verbose log, not inferred from the test definitions. Preserved nodes are intentionally passing at RED; they are never counted as RED evidence.

### Correction RED13 — complete inventory, identical in both runs

~~~text
tests/test_provider_response.py::test_real_child_response_framing[plain] PASSED
tests/test_provider_response.py::test_real_child_response_framing[gzip] FAILED
tests/test_provider_response.py::test_real_child_response_framing[chunked] FAILED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-start-400-PROVIDER_REQUEST_REJECTED-HTTP_STATUS] FAILED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-finalize-403-PROVIDER_CONFIGURATION-HTTP_STATUS] FAILED
tests/test_provider_response.py::test_attempt_diagnostic_capture[file-poll-429-PROVIDER_TRANSIENT-HTTP_STATUS] FAILED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS] FAILED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-reset-PROVIDER_TRANSIENT-NETWORK_ERROR] FAILED
tests/test_provider_response.py::test_unobserved_diagnostic_stays_unknown FAILED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[serialize] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[startup] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[reconstruct] FAILED
tests/test_provider_response.py::test_real_timeout_kills_and_reaps_before_return PASSED
~~~

### Correction scratch soundness13 — complete inventory, identical in both runs

~~~text
tests/test_provider_response.py::test_real_child_response_framing[plain] PASSED
tests/test_provider_response.py::test_real_child_response_framing[gzip] PASSED
tests/test_provider_response.py::test_real_child_response_framing[chunked] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-start-400-PROVIDER_REQUEST_REJECTED-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-finalize-403-PROVIDER_CONFIGURATION-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[file-poll-429-PROVIDER_TRANSIENT-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-reset-PROVIDER_TRANSIENT-NETWORK_ERROR] PASSED
tests/test_provider_response.py::test_unobserved_diagnostic_stays_unknown PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[serialize] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[startup] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[reconstruct] PASSED
tests/test_provider_response.py::test_real_timeout_kills_and_reaps_before_return PASSED
~~~

### Unchanged Gemini47 — complete inventory, identical in both runs

~~~text
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[helmet] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[triple-riding] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[red-light] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[irrelevant] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[mixed] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[uncertain] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[no-violation] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[low-score] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[context] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[prompt-injection] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[foreign-file] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-file] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[external-path] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-key] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[wrong-model] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[bad-timeout] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[bad-base] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[bad-max] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[snapshot] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[retry-after] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[deadline] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[upload-deadline] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[blocked] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[refusal] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[empty] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[markdown] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-score] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[boolean-score] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[float-score] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[out-of-range] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[unknown-media] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-attachment] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[duplicate-attachment] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[invented-law] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[foreign-url] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[video-time] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[blank-note] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[blank-explanation] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[empty-limitations] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[conflict] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[transient] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[unauthorized] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[unsupported] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[processing-failed] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[evil-upload] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[evil-file-uri] PASSED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[injected-authority] PASSED
~~~

### Unchanged durable14 — complete inventory, identical in both runs

~~~text
tests/test_durable_processing.py::test_pending_commit_survives_fresh_process_and_legacy_is_not_enqueued PASSED
tests/test_durable_processing.py::test_interrupted_attempts_are_consumed_across_process_recovery PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROVIDER_TRANSIENT-True] PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[ATTEMPT_TIMEOUT-True] PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROVIDER_CONFIGURATION-False] PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROVIDER_REQUEST_REJECTED-False] PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[INVALID_MODEL_OUTPUT-False] PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[MODEL_OUTPUT_UNAVAILABLE-False] PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[EVIDENCE_UNAVAILABLE-False] PASSED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROCESSING_ERROR-False] PASSED
tests/test_durable_processing.py::test_concurrent_claims_and_recovered_stale_completion_publish_once PASSED
tests/test_durable_processing.py::test_atomic_job_failure_does_not_accept_report_or_consume_upload PASSED
tests/test_durable_processing.py::test_acceptance_returns_during_background_dispatch_and_attempt_precedes_call PASSED
tests/test_durable_processing.py::test_obsolete_evidence_completion_is_superseded PASSED
~~~

### Unchanged intake106, decoder carrier — complete inventory, identical in both runs

~~~text
tests/test_auth.py::TestSignup::test_signup_with_valid_data_returns_201 PASSED
tests/test_auth.py::TestSignup::test_signup_with_duplicate_citizen_id_returns_409 PASSED
tests/test_auth.py::TestSignup::test_signup_with_duplicate_email_returns_409 PASSED
tests/test_auth.py::TestSignup::test_signup_with_invalid_email_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_with_missing_email_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_with_missing_password_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_with_short_password_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_password_is_hashed_not_plaintext PASSED
tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200 PASSED
tests/test_auth.py::TestLogin::test_login_with_invalid_password_returns_401 PASSED
tests/test_auth.py::TestLogin::test_login_with_nonexistent_citizen_returns_401 PASSED
tests/test_auth.py::TestLogin::test_login_returns_session_token PASSED
tests/test_auth.py::TestLogin::test_login_updates_last_login_timestamp PASSED
tests/test_auth.py::TestLogout::test_logout_returns_204_no_content PASSED
tests/test_auth.py::TestLogout::test_logout_without_token_returns_401 PASSED
tests/test_auth.py::TestAccessControl::test_accessing_reports_without_token_returns_401 PASSED
tests/test_auth.py::TestAccessControl::test_accessing_reports_with_invalid_token_returns_401 PASSED
tests/test_auth.py::TestAccessControl::test_citizen_can_see_own_reports PASSED
tests/test_auth.py::TestAccessControl::test_citizen_cannot_see_other_citizens_reports PASSED
tests/test_auth.py::TestAccessControl::test_citizen_id_from_token_used_for_reports PASSED
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_returns_profile PASSED
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_without_token_returns_401 PASSED
tests/test_auth.py::TestIntegration::test_complete_citizen_workflow PASSED
tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id PASSED
tests/test_api_endpoints.py::TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports PASSED
tests/test_api_endpoints.py::TestCitizenReportDetails::test_citizen_fetch_report_details_with_timeline PASSED
tests/test_api_endpoints.py::TestOfficerReviewQueue::test_officer_query_review_queue_returns_paginated_list PASSED
tests/test_api_endpoints.py::TestOfficerCaseDetail::test_officer_view_case_detail_shows_evidence PASSED
tests/test_api_endpoints.py::TestOfficerApproval::test_officer_approve_report_awards_points PASSED
tests/test_api_endpoints.py::TestOfficerRejection::test_officer_reject_with_reason_stores_reason PASSED
tests/test_api_endpoints.py::TestOfficerClarificationRequest::test_officer_request_clarification_requeues_case PASSED
tests/test_api_endpoints.py::TestCitizenClarification::test_citizen_clarification_response_resubmits_case PASSED
tests/test_api_endpoints.py::TestOfficerQueueUpdate::test_officer_queue_reflects_requeued_cases PASSED
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_jpeg_returns_media_id_and_hash SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_mp4_video_returns_media_id SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_duplicate_file_returns_409_conflict SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_file_too_large_returns_413_payload_too_large SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_video_too_long_returns_413 SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_unsupported_file_format_returns_422 SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_corrupted_jpeg_returns_422 SKIPPED
tests/test_media.py::TestTechnicalScreening::test_low_resolution_image_flags_warning SKIPPED
tests/test_media.py::TestTechnicalScreening::test_high_blur_video_flags_warning SKIPPED
tests/test_media.py::TestMediaAccessControl::test_citizen_can_download_own_media SKIPPED
tests/test_media.py::TestMediaAccessControl::test_citizen_cannot_download_other_citizens_media SKIPPED
tests/test_media.py::TestMediaAccessControl::test_officer_can_download_any_media SKIPPED
tests/test_verification_harness.py::test_real_schema_and_effective_paths PASSED
tests/test_verification_harness.py::test_independent_lifespans_close_and_do_not_reuse_state PASSED
tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source PASSED
tests/test_identity.py::test_claim_validation_and_error_contract PASSED
tests/test_identity.py::test_human_permission_boundary_without_business_handlers PASSED
tests/test_identity.py::test_fixed_service_client_audience_scope_matrix PASSED
tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache PASSED
tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpeg-a.jpg] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpg-a.jpg] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[png-image/png-a.png] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mov-video/quicktime-a.mov] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[avi-video/x-msvideo-a.avi] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[long-video/mp4-a.mp4] PASSED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485759] PASSED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485760] PASSED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485761] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[not an image-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[\xff\xd8\xffbroken-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[GIF89a-image/gif-UNSUPPORTED_MEDIA_TYPE] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[\x1aE\xdf\xa3webm-video/webm-UNSUPPORTED_MEDIA_TYPE] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[https://example.invalid/evidence.jpg-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[C:\outside\evidence.jpg-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[png_as_jpeg] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[video_as_image] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[image_as_video] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[audio_only] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[truncated_video] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[mp4_as_mov] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[mov_as_mp4] PASSED
tests/test_evidence_intake.py::test_multipart_contract[missing] PASSED
tests/test_evidence_intake.py::test_multipart_contract[wrong] PASSED
tests/test_evidence_intake.py::test_multipart_contract[multiple] PASSED
tests/test_evidence_intake.py::test_multipart_contract[malformed] PASSED
tests/test_evidence_intake.py::test_unknown_multipart_fields_and_generated_display_filename PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[../escaped.jpg] PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[C:\\temp\\escaped.jpg] PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[https://example.invalid/a.jpg] PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[unicode-\u96ea.jpg] PASSED
tests/test_evidence_intake.py::test_citizen_authentication_and_invalid_bearer_precedence PASSED
tests/test_evidence_intake.py::test_duplicate_privacy_unattached_replay_and_attached_new_handle PASSED
tests/test_evidence_intake.py::test_mixed_ordered_owned_unattached_evidence_and_singular_compatibility PASSED
tests/test_evidence_intake.py::test_changed_json_boundary_rejects_malformed_nonobject_and_content_type PASSED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[missing-MEDIA_NOT_FOUND-404] PASSED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[foreign-FORBIDDEN-403] PASSED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[attached-MEDIA_ALREADY_ATTACHED-409] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[both] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[empty] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[null] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[duplicate] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[blank] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[wrong_type] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[category] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[number] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[location] PASSED
tests/test_evidence_intake.py::test_competing_creates_cannot_reassociate_same_attachment PASSED
tests/test_evidence_intake.py::test_private_returned_officer_url_credentials_and_exact_basename PASSED
tests/test_evidence_intake.py::test_legacy_metadata_paths_are_contained_and_owner_is_not_guessed PASSED
tests/test_evidence_intake.py::test_safe_zip_names_preserve_display_metadata PASSED
~~~

### Initial timed-out intake run — complete observed partial inventory

~~~text
intake run 1 result: TIMEOUT
tests/test_auth.py::TestSignup::test_signup_with_valid_data_returns_201 PASSED
tests/test_auth.py::TestSignup::test_signup_with_duplicate_citizen_id_returns_409 PASSED
tests/test_auth.py::TestSignup::test_signup_with_duplicate_email_returns_409 PASSED
tests/test_auth.py::TestSignup::test_signup_with_invalid_email_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_with_missing_email_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_with_missing_password_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_with_short_password_returns_400 PASSED
tests/test_auth.py::TestSignup::test_signup_password_is_hashed_not_plaintext PASSED
tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200 PASSED
tests/test_auth.py::TestLogin::test_login_with_invalid_password_returns_401 PASSED
tests/test_auth.py::TestLogin::test_login_with_nonexistent_citizen_returns_401 PASSED
tests/test_auth.py::TestLogin::test_login_returns_session_token PASSED
tests/test_auth.py::TestLogin::test_login_updates_last_login_timestamp PASSED
tests/test_auth.py::TestLogout::test_logout_returns_204_no_content PASSED
tests/test_auth.py::TestLogout::test_logout_without_token_returns_401 PASSED
tests/test_auth.py::TestAccessControl::test_accessing_reports_without_token_returns_401 PASSED
tests/test_auth.py::TestAccessControl::test_accessing_reports_with_invalid_token_returns_401 PASSED
tests/test_auth.py::TestAccessControl::test_citizen_can_see_own_reports PASSED
tests/test_auth.py::TestAccessControl::test_citizen_cannot_see_other_citizens_reports PASSED
tests/test_auth.py::TestAccessControl::test_citizen_id_from_token_used_for_reports PASSED
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_returns_profile PASSED
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_without_token_returns_401 PASSED
tests/test_auth.py::TestIntegration::test_complete_citizen_workflow PASSED
tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id PASSED
tests/test_api_endpoints.py::TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports PASSED
tests/test_api_endpoints.py::TestCitizenReportDetails::test_citizen_fetch_report_details_with_timeline PASSED
tests/test_api_endpoints.py::TestOfficerReviewQueue::test_officer_query_review_queue_returns_paginated_list PASSED
tests/test_api_endpoints.py::TestOfficerCaseDetail::test_officer_view_case_detail_shows_evidence PASSED
tests/test_api_endpoints.py::TestOfficerApproval::test_officer_approve_report_awards_points PASSED
tests/test_api_endpoints.py::TestOfficerRejection::test_officer_reject_with_reason_stores_reason PASSED
tests/test_api_endpoints.py::TestOfficerClarificationRequest::test_officer_request_clarification_requeues_case PASSED
tests/test_api_endpoints.py::TestCitizenClarification::test_citizen_clarification_response_resubmits_case PASSED
tests/test_api_endpoints.py::TestOfficerQueueUpdate::test_officer_queue_reflects_requeued_cases PASSED
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_jpeg_returns_media_id_and_hash SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_mp4_video_returns_media_id SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_duplicate_file_returns_409_conflict SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_file_too_large_returns_413_payload_too_large SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_video_too_long_returns_413 SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_unsupported_file_format_returns_422 SKIPPED
tests/test_media.py::TestMediaUploadValidation::test_corrupted_jpeg_returns_422 SKIPPED
tests/test_media.py::TestTechnicalScreening::test_low_resolution_image_flags_warning SKIPPED
tests/test_media.py::TestTechnicalScreening::test_high_blur_video_flags_warning SKIPPED
tests/test_media.py::TestMediaAccessControl::test_citizen_can_download_own_media SKIPPED
tests/test_media.py::TestMediaAccessControl::test_citizen_cannot_download_other_citizens_media SKIPPED
tests/test_media.py::TestMediaAccessControl::test_officer_can_download_any_media SKIPPED
tests/test_verification_harness.py::test_real_schema_and_effective_paths PASSED
tests/test_verification_harness.py::test_independent_lifespans_close_and_do_not_reuse_state PASSED
tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source PASSED
tests/test_identity.py::test_claim_validation_and_error_contract PASSED
tests/test_identity.py::test_human_permission_boundary_without_business_handlers PASSED
tests/test_identity.py::test_fixed_service_client_audience_scope_matrix PASSED
tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache PASSED
tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpeg-a.jpg] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpg-a.jpg] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[png-image/png-a.png] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mov-video/quicktime-a.mov] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[avi-video/x-msvideo-a.avi] PASSED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[long-video/mp4-a.mp4] PASSED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485759] PASSED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485760] PASSED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485761] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[not an image-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[\xff\xd8\xffbroken-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[GIF89a-image/gif-UNSUPPORTED_MEDIA_TYPE] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[\x1aE\xdf\xa3webm-video/webm-UNSUPPORTED_MEDIA_TYPE] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[https://example.invalid/evidence.jpg-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[C:\outside\evidence.jpg-image/jpeg-INVALID_MEDIA] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[png_as_jpeg] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[video_as_image] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[image_as_video] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[audio_only] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[truncated_video] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[mp4_as_mov] PASSED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[mov_as_mp4] PASSED
tests/test_evidence_intake.py::test_multipart_contract[missing] PASSED
tests/test_evidence_intake.py::test_multipart_contract[wrong] PASSED
tests/test_evidence_intake.py::test_multipart_contract[multiple] PASSED
tests/test_evidence_intake.py::test_multipart_contract[malformed] PASSED
tests/test_evidence_intake.py::test_unknown_multipart_fields_and_generated_display_filename PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[../escaped.jpg] PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[C:\\temp\\escaped.jpg] PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[https://example.invalid/a.jpg] PASSED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[unicode-\u96ea.jpg] PASSED
tests/test_evidence_intake.py::test_citizen_authentication_and_invalid_bearer_precedence PASSED
tests/test_evidence_intake.py::test_duplicate_privacy_unattached_replay_and_attached_new_handle PASSED
tests/test_evidence_intake.py::test_mixed_ordered_owned_unattached_evidence_and_singular_compatibility PASSED
tests/test_evidence_intake.py::test_changed_json_boundary_rejects_malformed_nonobject_and_content_type PASSED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[missing-MEDIA_NOT_FOUND-404] PASSED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[foreign-FORBIDDEN-403] PASSED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[attached-MEDIA_ALREADY_ATTACHED-409] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[both] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[empty] PASSED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[null] PASSED
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
~~~



### Exact planning-only setup.py

~~~python
from pathlib import Path
import hashlib,json,shutil
ROOT=Path(r'C:\Users\avina\Downloads\avinash-repo\v11\Traffic')
TASK=Path(__file__).resolve().parent
def snapshot():
    return {str(p.resolve()):[p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()] for p in ROOT.rglob('*') if p.is_file() and not any(x in p.relative_to(ROOT).parts for x in ('.git','.venv','__pycache__','.pytest_cache','.deepeval')) and p.name!='008_Implementation_Plan_Provider_Response_Correction_RED.md'}
(TASK/'before.json').write_text(json.dumps(snapshot()),encoding='utf-8')
copy=TASK/'repository'; copy.mkdir()
for p in ROOT.glob('*.py'): shutil.copy2(p,copy/p.name)
shutil.copy2(ROOT/'pytest.ini',copy/'pytest.ini')
for name in ('tests','templates','static'):
    shutil.copytree(ROOT/name,copy/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.bak'))
assert not any((copy/n).exists() for n in ('roadwatch.db','media_store','.local','.env','.git'))
(TASK/'temporary').mkdir(); (TASK/'bin').mkdir()
for tool in ('ffprobe','ffmpeg'):
    (TASK/'bin'/(tool+'.cmd')).write_text('@"'+str(ROOT/'.venv/Scripts/python.exe')+'" "'+str(TASK/'decoder.py')+'" '+tool+' %*\n')
~~~

### Exact planning-only decoder.py

~~~python
from pathlib import Path
import subprocess,sys
name,args=sys.argv[1],sys.argv[2:]
index=len(args)-1 if name=='ffprobe' else args.index('-i')+1
path=Path(args[index]); args[index]='pipe:0'
result=subprocess.run(['docker','run','--rm','-i','--network','none','--entrypoint','/usr/bin/'+name,'traffic-60e6e567315a-runner:latest',*args],input=path.read_bytes(),capture_output=True)
sys.stdout.buffer.write(result.stdout); sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
~~~

### Exact planning-only preserve.py

~~~python
from pathlib import Path
import os,subprocess,sys
task=Path(__file__).parent
env=os.environ.copy()
env.update(PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',TMP=str(task/'temporary'),TEMP=str(task/'temporary'),TMPDIR=str(task/'temporary'))
env['PATH']=str(task/'bin')+os.pathsep+env['PATH']
for name,argument in [('gemini_assessment','--green'),('durable_processing','--green'),('current_demo','--intake')]:
    command=[sys.executable,'tests/verify_'+name+'.py',argument]
    print('Command:',repr(command),'cwd=',str(task/'repository'),flush=True)
    with (task/(name+'.log')).open('w',encoding='utf-8') as log:
        result=subprocess.run(command,cwd=task/'repository',env=env,stdout=log,stderr=subprocess.STDOUT)
    print(name,'exit',result.returncode,flush=True)
    assert result.returncode==0
print('All unchanged preservation pairs completed',flush=True)
~~~

### Exact planning-only decoder_carrier.py

~~~python
from pathlib import Path
import os,re,subprocess,sys
name,args=sys.argv[1],sys.argv[2:]
assert name in ('ffprobe','ffmpeg')
carrier=os.environ['ASOR_DECODER_CARRIER']
assert re.fullmatch(r'[0-9a-f]{64}',carrier)
index=len(args)-1 if name=='ffprobe' else args.index('-i')+1
path=Path(args[index]).resolve(); args[index]='pipe:0'
assert path.is_relative_to((Path(__file__).parent/'temporary').resolve())
result=subprocess.run(['docker','exec','-i',carrier,'/usr/bin/'+name,*args],input=path.read_bytes(),capture_output=True)
sys.stdout.buffer.write(result.stdout); sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
~~~

### Exact planning-only run_intake_carrier.py

~~~python
from pathlib import Path
import os,re,subprocess,sys
task=Path(__file__).resolve().parent
bin_dir=task/'bin-carrier'; bin_dir.mkdir()
for tool in ('ffprobe','ffmpeg'):
    (bin_dir/(tool+'.cmd')).write_text('@"'+sys.executable+'" "'+str(task/'decoder_carrier.py')+'" '+tool+' %*\n')
command=['docker','run','-d','--rm','--network','none','--pull','never','--name','asor-m08a-intake-8c13b0a4','--entrypoint','/bin/sleep','traffic-60e6e567315a-runner:latest','480']
print('Carrier:',repr(command),flush=True)
carrier=subprocess.check_output(command,text=True,timeout=30).strip()
assert re.fullmatch(r'[0-9a-f]{64}',carrier)
try:
    geometry=subprocess.check_output(['docker','inspect','--format','{{.HostConfig.NetworkMode}} {{len .Mounts}}',carrier],text=True,timeout=15).strip()
    assert geometry=='none 0',geometry
    print('Owned decoder carrier: network none; mounts 0',flush=True)
    env=os.environ.copy()
    env.update(ASOR_DECODER_CARRIER=carrier,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',TMP=str(task/'temporary'),TEMP=str(task/'temporary'),TMPDIR=str(task/'temporary'))
    env['PATH']=str(bin_dir)+os.pathsep+env['PATH']
    command=[sys.executable,'tests/verify_current_demo.py','--intake']
    print('Command:',repr(command),'cwd=',str(task/'repository'),flush=True)
    with (task/'current_demo-carrier.log').open('w',encoding='utf-8') as log:
        result=subprocess.run(command,cwd=task/'repository',env=env,stdout=log,stderr=subprocess.STDOUT)
    print('Unchanged intake launcher exit',result.returncode,flush=True)
    assert result.returncode==0
finally:
    subprocess.run(['docker','stop','--time','1',carrier],check=True,capture_output=True,timeout=20)
    remain=subprocess.check_output(['docker','ps','-aq','--filter','id='+carrier],text=True,timeout=15)
    assert not remain.strip()
    print('Owned decoder carrier stopped and absent',flush=True)
~~~

### Exact planning-only check.py

~~~python
from pathlib import Path
import ast,hashlib,json,re
task=Path(__file__).parent
root=Path(r'C:\Users\avina\Downloads\avinash-repo\v11\Traffic')
def snapshot():
    return {str(p.resolve()):[p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()] for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ('.git','.venv','__pycache__','.pytest_cache','.deepeval')) and p.name!='008_Implementation_Plan_Provider_Response_Correction_RED.md'}
before=json.loads((task/'before.json').read_text())
assert snapshot()==before,'Protected original checkout changed'
print('Full original absolute-path/length/SHA-256 inventory unchanged:',len(before),'files; only008 excluded')
for name in ('tests/verify_gemini_assessment.py','tests/verify_durable_processing.py','tests/verify_current_demo.py','tests/test_gemini_assessment.py','tests/test_durable_processing.py','tests/test_evidence_intake.py','tests/conftest.py','durable.py','gemini.py','app.py','bootstrap.py','intake.py','pytest.ini'):
    assert (root/name).read_bytes()==(task/'repository'/name).read_bytes(),name
print('Original source/config/tests and90/180-second launchers byte-identical to frozen baseline')
for name in ('tests/test_provider_response.py','tests/verify_provider_response.py'):
    assert (task/'repository'/name).read_bytes()==(task/'probe-repository'/name).read_bytes()
    ast.parse((task/'repository'/name).read_text(encoding='utf-8-sig'))
print('Both exact new files parse and baseline/probe bytes match')
~~~

## Scratch-only soundness probe archive

The following exact external script creates a separate source-only copy and changes only its durable.py/gemini.py. It is archived to make the fail/pass proof reproducible; it is not a proposed repository file, approved production implementation or M08B plan. Test assertions/classifiers are identical in baseline/probe copies.

~~~python
"""Planning-only smallest behavior probe; never apply to checkout."""
from pathlib import Path
import shutil,ast
task=Path(__file__).parent
source=task/'repository'; target=task/'probe-repository'
shutil.copytree(source,target,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
p=target/'durable.py'; s=p.read_text(encoding='utf-8-sig')
s=s.replace('    "CREATE INDEX IF NOT EXISTS ai_jobs_ready', '''    "CREATE TABLE IF NOT EXISTS ai_provider_diagnostics(job_id TEXT NOT NULL,number INTEGER NOT NULL,provider_status INTEGER,request_stage TEXT,diagnostic_class TEXT NOT NULL,PRIMARY KEY(job_id,number),FOREIGN KEY(job_id,number) REFERENCES ai_attempts(job_id,number))",
    "CREATE INDEX IF NOT EXISTS ai_jobs_ready''')
s=s.replace("'headers':list(response.headers.multi_items())", "'headers':[(k,v) for k,v in response.headers.multi_items() if k.lower() not in ('content-encoding','content-length','transfer-encoding')]")
s=s.replace("                return httpx.Response(result['status'],headers=result['headers'],content=base64.b64decode(result['content']))", "                response=httpx.Response(result['status'],headers=result['headers'],content=base64.b64decode(result['content']))\n                if time.monotonic()>=deadline: raise httpx.TimeoutException('Provider deadline expired')\n                return response")
p.write_text(s,encoding='utf-8')
p=target/'gemini.py'; s=p.read_text(encoding='utf-8-sig')
s=s.replace('        report,media=prepared\n', '        report,media=prepared\n        self.diagnostic=None\n')
s=s.replace('        def request(method,url,**kwargs):\n', '''        def request(method,url,**kwargs):
            path=urlsplit(url).path
            stage=('file-delete' if method=='DELETE' else 'upload-start' if path=='/upload/v1beta/files' else 'upload-finalize' if path.startswith('/upload/') else 'file-poll' if path.startswith('/v1beta/files/') else 'generate' if path.startswith('/v1beta/models/') else None)
            def record(status,kind):
                if self.diagnostic is None: self.diagnostic=(status,stage,kind)
''')
s=s.replace("            except httpx.TimeoutException: raise Failure('ATTEMPT_TIMEOUT',True)", "            except httpx.TimeoutException:\n                record(None,'TIMEOUT')\n                raise Failure('ATTEMPT_TIMEOUT',True)")
s=s.replace("            except (httpx.NetworkError,httpx.RemoteProtocolError): raise Failure('PROVIDER_TRANSIENT',True)", "            except (httpx.NetworkError,httpx.RemoteProtocolError):\n                record(None,'NETWORK_ERROR')\n                raise Failure('PROVIDER_TRANSIENT',True)")
s=s.replace("            except httpx.HTTPError: raise Failure('PROCESSING_ERROR')", "            except httpx.HTTPError:\n                record(None,'PROCESSING_ERROR')\n                raise Failure('PROCESSING_ERROR')")
s=s.replace("            if response.status_code in (408", "            if response.status_code>=300: record(response.status_code,'HTTP_STATUS')\n            if response.status_code in (408")
s=s.replace('class Worker(d.Worker):', '''def save_diagnostic(path, token, value):
    status,stage,kind=value or (None,None,'PROCESSING_ERROR')
    if type(status) is not int or not 100<=status<=599: status=None
    if stage not in {'upload-start','upload-finalize','file-poll','generate','file-delete'}: stage=None
    if kind not in {'HTTP_STATUS','NETWORK_ERROR','TIMEOUT','PROCESSING_ERROR'}: kind='PROCESSING_ERROR'
    with sqlite3.connect(path) as conn:
        conn.execute('INSERT OR REPLACE INTO ai_provider_diagnostics VALUES(?,?,?,?,?)',(token['job_id'],token['number'],status,stage,kind))

class Worker(d.Worker):''')
s=s.replace('                        except Failure as failure:\n                            now=self.clock()', "                        except Failure as failure:\n                            save_diagnostic(self.adapter.path,token,getattr(self.adapter,'diagnostic',None))\n                            now=self.clock()")
s=s.replace("                        except Exception:\n                            self.store.fail(token,'PROCESSING_ERROR'", "                        except Exception:\n                            save_diagnostic(self.adapter.path,token,None)\n                            self.store.fail(token,'PROCESSING_ERROR'")
p.write_text(s,encoding='utf-8')
for p in (target/'durable.py',target/'gemini.py'): ast.parse(p.read_text())
print('Scratch-only minimal probe parsed; separate frozen source copy')
~~~

## Exact-code self-check and cleanup

Both complete proposed new files parse. The source-only baseline and soundness copies contain byte-identical final new test/helper content. Each exact block was independently extracted and reapplied to a separate owned mechanical directory; AST parsing and byte/hash equality to the frozen test input passed. The test block uses UTF-8/LF and the launcher UTF-8/CRLF, preserved verbatim in this document; no encoding/newline-only source mutation was needed during verification.

| Proposed file | Scope / actual check |
| --- | --- |
| tests/test_provider_response.py | Complete final content; framing/attempt capture/privacy/unknown/deadline/cancellation checks map to ordered changes1–3. Exact bytes extracted/reapplied, parsed, equal to both frozen copies. |
| tests/verify_provider_response.py | Complete final content; exact13-node classification and safe repeated source-only verification map to change4. Exact bytes extracted/reapplied, parsed and equal;90second limit retained. |

No new dependency, configuration, operator setting or production seam is hidden in the code. Every proposed change is named above and every exact code behavior traces to approved correction scope, a preserved row or an explicit review decision. The private capture-table assertion is a RED signature expectation, not production scaffolding. Scratch probe code is evidence only.

Independent full original metadata comparison: **189 absolute-path/length/SHA-256 records unchanged**, excluding only this008 and .git/.venv/transient caches. This includes all prior dirty source/tests/configuration/docs, real database/sidecars/media/private-local bytes. Protected private metadata values are not published. No other checkout addition/modification was made. Actual private recovery backups and designated key/photos were not fixtures or inspected.

Expanded read-only process inspection found **0 owned verification processes** and both named decoder carriers independently absent. All launcher children/owned HTTP threads were reaped by their guards. The separately identified one-node diagnostic tree was already absent at final inspection; the shared pytest parent and older trees were untouched. Verified the exact planning directory resolved to its intended direct Temp parent and contained no reparse points, then removed only that literal directory. Actual cleanup output: `Owned literal source/probe/synthetic state area removed and independently absent; known launcher/diagnostic trees absent`. No additional external archive, running helper, scratch source copy or container remains. No unrelated process, container, recovery backup or workspace file was stopped, removed or changed.


Historical intake-resume revision self-check. Both proposed code blocks still match the applied checkout files byte for byte. Executing the exact preparation block in disposable scratch confirmed the original launcher stayed byte-identical and the sibling differed only in the intake timeout expression. The derived carrier driver compiled. This check started no carrier or test child.

## Human Review

Status: Checkpoint verification procedure approved by user on 2026-11-10.
