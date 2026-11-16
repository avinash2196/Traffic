# ASOR-M08A provider response correction RED resume — 2026-11-10

**Blocked.** The first RED child completed, but the launcher rejected an unexpected failure in the `generate-503` case. Its positive assessment stopped at `tests/test_provider_response.py:176` with `assert 'retry-wait' == 'completed'` before the case could exercise its intended diagnostic assertion. The visible HTTP log lines recorded successful test-app requests. The output establishes the unexpected state and does not identify the provider-boundary cause. The numerical RED total alone does not verify the milestone.

The [stopped execution](ASOR-M08A-Execution-2026-11-10.md) retained two valid historical RED runs plus Gemini and durable pairs. Its published baseline includes exact hashes for the two applied files and aggregate integrity results, but the prior disposable source copies were removed and individual remaining input hashes were unavailable. The revised 008 procedure therefore required rerunning the three original pairs before intake. A setup extraction guard initially expected 11 code blocks and found 10. That invocation created only the approved empty root. After verifying it was still empty and owned, corrected the count guard and extracted the exact approved blocks. Both Python test files matched the prior SHA-256 values and the source-only baseline and probe copies.

## Observed run

Used the existing Traffic venv interpreter with explicit cwd `repository` under the approved literal resume root, that root's `temporary` for TMP/TEMP/TMPDIR, the forwarding bin path, UTF-8, and bytecode disabled. Executed the archived `setup.py`, `probe.py`, and `prepare_intake_resume.py` as specified by 008. The variant and probe were prepared in the disposable tree. Verification began with `tests/verify_provider_response.py --red` using the unchanged 90-second child bound. The child exited 1 at 76.30 seconds with 9 failures, 4 passes and 1 warning. The launcher exited 1 after classifying the first child's assertion messages. The remaining RED repetition, fresh Gemini and durable pairs, both intake repetitions, and both scratch soundness repetitions were not started.

```text
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-resume-20261110-8c13b0a6\\temporary\\asor-m08a-mrz4ty4l\\red-1.xml', 'tests/test_provider_response.py']
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
```

## Integrity and cleanup

The independent original absolute-path/length/SHA-256 inventory matched all 192 entries after the run, excluding 008 and repository/virtual-environment/transient caches as prescribed. A separate hash check confirmed 008 itself was unchanged during verification. All 91 frozen files across the disposable baseline and probe matched their pre-run path/SHA-256 inventory. Both new test files parsed and matched between checkout, baseline and probe. The original production files, tests, configuration and 90/180-second launchers matched the frozen baseline byte for byte. Private inventory data stays unpublished. Process inspection found zero owned verification processes, the named decoder carrier was absent, and the owned launcher temporary directory was empty. After checking the literal resolved root, direct Temp parent and absence of reparse points, removed only the owned resume root and confirmed it was absent.

M08A requires a reviewed verification procedure that can account for the failed positive control and then establish both valid RED runs, the unchanged preservation pairs, and both scratch soundness runs. M08B remains Pending. No live request or production edit occurred.
