# AGW-M02A execution — 2026-11-11

Approved IP013 applied exactly: complete new `tests/agw_provider_child.py` and three reviewed diffs, preserving existing mixed line endings and all original context. No production/configuration/dependency changes. Baseline dirty status and public source hashes are retained in the linked artifacts; all public sources outside the three approved modifications remained equal. Applied hashes also remained equal after verification.

Actual command, once, with native Windows loopback authorization and explicit cwd `C:\Users\avina\AppData\Local\Temp`:

```powershell
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' -B 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\tests\verify_gateway_service.py' --red
```

Actual exit: 0. Actual output:

```text
new 19 intended failures
preserved 2 passes
Owned processes/carrier removed; copied source and synthetic state deleted
```

[Safe execution artifacts](AGW-M02A-Execution-2026-11-11/) contain complete pytest logs/XML, per-outcome summary, lifecycle first/repeat/server logs including full tracebacks and event timestamps, protection manifests, and before/after dirty status. The verifier used the new fixed M02A task root, refused reuse by assertion, and left the predecessor M02 logs untouched.

Lifecycle first: client launcher3388, provider server25444, provider launcher30980; passed, client reaped and remote drained, elapsed3998ms. Repeat without state cleanup: client launcher32732, provider server25136, provider launcher35316; passed, client reaped and remote drained, elapsed3997ms. These elapsed values include the legitimate four-second remote drain; the diagnostic separately asserted local cancellation/reap under3s. Positive real HTTP preceded cancellation. Both owned client trees were stopped, the remote provider survived local cancellation, finally removed its active marker and was then stopped through its owned launcher tree. Subsequent host process lookup found none of those six recorded PIDs.

Both cancellation requests produced `ConnectionResetError: [WinError 10054]` at `do_POST` / `end_headers`, outside the narrower response-body-write catch. Python HTTPServer catches this per-request exception; the provider's finally emitted provider-drained, its process survived until owned shutdown, and all diagnostic assertions passed. Full safe tracebacks are preserved, not suppressed. This is a simulated remote-client-disconnect observation, not a pytest error or production cancellation failure; no noise fix or rerun was made.

JUnit:19 ordinary intended failures, zero errors/skips;17 missing-service404 / `SEPARATE_HTTP_ASSESSMENT_MISSING`, one `APPLICATION_WORKER_DID_NOT_TRAVERSE_GATEWAY_HTTP`, one `APPLICATION_HTTP_RETRY_OWNERSHIP_MISSING`. The unchanged two durable preservation cases passed. No command timeout. These remain valid RED evidence, not passing production service behavior. Source closure compilation, allowlisted source hashes and same-native-Python other-root metadata assertions passed in the exact verifier.

Private/non-allowlisted content was neither read nor hashed. The independent pre-application metadata comparison differed only in the tests directory modification time caused by adding the authorized helper. The verifier's own post-application before/after metadata comparison passed. Directory sizes are host/runtime-context observations; no cross-shell byte-size guarantee is claimed.

Native decoders were absent, so the unchanged approved pinned image carrier was used: network none, zero mounts, helper supplied through stdin, direct container FFmpeg/FFprobe version checks and both Windows wrapper resolution assertions passed. No live provider sockets or host decoder installation. Verifier finally removed the owned carrier and source/synthetic-state/bin directories; subsequent host Docker listing showed only the three pre-existing Scribe containers. Retained files were copied from the owned task root; no old logs deleted.

Routine bookkeeping deviations: the source-application bookkeeping assertion initially compared Windows backslash paths to forward-slash literals after the exact writes; normalization confirmed the approved delta without rewriting/retrying tests. An independent metadata check initially included the authorized tests-directory creation mtime change; it was recorded explicitly rather than treated as private-state mutation. A read-only Docker cleanup inventory from the restricted context was denied; the authorized host-context inventory succeeded. The one exact verifier execution was never retried.

NOT RUN: GREEN probe, broad historical suite, Gemini/live calls, private keys/media/database reads, staging or commit. Production CT06 and other previously deferred contract coverage remain GREEN obligations; this diagnostic proves test-harness lifecycle mechanics only. M02 evidence is preserved unchanged. M02A complete; IP014 remains a separate planning/review step.
