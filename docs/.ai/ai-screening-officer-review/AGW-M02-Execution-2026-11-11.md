# AGW-M02 execution — 2026-11-11

Approved IP012 applied exactly three complete files; no production/configuration/dependency or pre-existing test edits. Each extracted file parsed and matched its recorded SHA256. The child uses LF; the other two files use CRLF, as required to reproduce the approved hashes.

Actual command, with native Windows loopback authorization and explicit cwd `C:\Users\avina\AppData\Local\Temp`:

```powershell
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' -B 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\tests\verify_gateway_service.py' --red
```

Actual exit: 0. Trimmed output:

```text
new 19 intended failures
preserved 2 passes
Owned processes/carrier removed; copied source and synthetic state deleted
```

JUnit: 19 ordinary assertion failures; zero errors/skips/timeouts. Seventeen fail with `SEPARATE_HTTP_ASSESSMENT_MISSING` (404 versus 200), one with `APPLICATION_WORKER_DID_NOT_TRAVERSE_GATEWAY_HTTP`, and one with `APPLICATION_HTTP_RETRY_OWNERSHIP_MISSING`. The separate child’s missing-service 404 and absent application HTTP traversal are the intended RED behavior. The two preserved cases passed separately and are not new RED evidence.

Detailed logs, JUnit and protection manifest: [execution artifacts](AGW-M02-Execution-2026-11-11/). Named outcomes:

- `test_separate_image_wire_and_safe_trace`: intended failure.
- `test_rejection_partitions[auth-401-UNAUTHORIZED]`: intended failure.
- `test_rejection_partitions[query-400-INVALID_REQUEST]`: intended failure.
- `test_rejection_partitions[unknown-400-INVALID_REQUEST]`: intended failure.
- `test_rejection_partitions[boolean-400-INVALID_REQUEST]`: intended failure.
- `test_rejection_partitions[duplicate-400-INVALID_REQUEST]`: intended failure.
- `test_rejection_partitions[base64-400-INVALID_REQUEST]`: intended failure.
- `test_rejection_partitions[count-413-REQUEST_TOO_LARGE]`: intended failure.
- `test_rejection_partitions[prompt-409-PROMPT_INCOMPATIBLE]`: intended failure.
- `test_rejection_partitions[selection-409-SELECTION_INCOMPATIBLE]`: intended failure.
- `test_rejection_partitions[method-405-METHOD_NOT_ALLOWED]`: intended failure.
- `test_rejection_partitions[encoding-415-UNSUPPORTED_MEDIA_TYPE]`: intended failure.
- `test_rejection_partitions[decode-422-EVIDENCE_UNAVAILABLE]`: intended failure.
- `test_output_failure_retains_independent_usage[refusal-MODEL_REFUSAL]`: intended failure.
- `test_output_failure_retains_independent_usage[invalid-INVALID_MODEL_OUTPUT]`: intended failure.
- `test_v2_video_actual_pts_and_incomplete_referral`: intended failure.
- `test_absolute_budget_and_terminal_scratch_cleanup`: intended failure.
- `test_application_worker_owns_wire_and_persistence`: intended failure.
- `test_restart_transients_consume_three_attempts_without_fallback`: intended failure.
- `test_concurrent_claims_and_recovered_stale_completion_publish_once`: preserved pass.
- `test_obsolete_evidence_completion_is_superseded`: preserved pass.

The exact verifier asserted source/public-asset allowlist hash equality and same-process other-root metadata equality. Private/non-allowlisted contents were not hashed/read. Directory st_size is shell/runtime-dependent; equality here is the verifier’s own Python before/after observation, not a cross-shell directory-size guarantee. File metadata and directory modification times were protected by that comparison.

Pinned offline decoder carrier passed direct FFmpeg/FFprobe preflight and network-none/zero-mount inspection. Windows wrapper path resolution and the stdin helper were exercised by the successful synthetic VFR case setup. No host decoder installation or live provider call. Owned service children were fixture-reaped; carrier and source/synthetic-state directories removed by verifier finally. Safe copied logs/XML/manifests retained above; no execution retry or probe was needed.

Limitations remain exactly IP012’s representative assertion inventory. Full CT03/CT06 resource/disconnect/reap and additional contract branches await exact GREEN source review; no additional runtime coverage claimed. Historical MP4 root cause remains unknown, Gemini deferred, and old historical failures remain preserved. No broad old inventory, real media/DB/key reads, staging or commit. No next milestone source implementation.
