# ASOR-M08 Gemini assessment GREEN offline execution — 2026-11-09

Executed only the approved offline portion of ASOR-M08 for `ai-screening-officer-review`, by a fresh-context implementation-engineer role. Authority:007 Human Review user approval2026-11-09, approved requirements/Plan/External Contract,001–006 approved predecessor plans and actual M02–M07 evidence. The exact production changes are applied and offline verification passed. At this original offline snapshot, M08 was Waiting for live inputs. The live follow-up below supersedes that status: actual first-image provider rejection stopped execution; M08 is now Blocked and not Completed. R03 is not closed by substitutes. M09 remains Pending; no next-milestone work occurred.

## Live image follow-up — actual provider rejection; execution stopped

Following the offline snapshot below, the user supplied a private key and photos, confirmed the two suspected-category test cases/qualitative officer-referral expectations and requested image-first testing, with video to be tested manually later. Google transmission of those supplied photos was authorized. All unprovided plate/location/statutory context was explicitly unknown. A read-only SHA-256 comparison found the second helmet-named copy byte-identical, so it was excluded. No new source/test/configuration or provider substitution occurred.

Prepared a separately owned host-visible disposable source-only application area, exact007 external live runner and private `live-inputs.json` with two confirmed image cases. The key remained in its original private file; only the live runner read its value into its child environment, never stdout/arguments or a disk copy. Full original checkout/key/sample absolute-path/length/hash metadata was privately captured twice and matched. Original images stayed read-only; uploaded copies existed only in the disposable application. No real checkout startup/DB connection/migration occurred.

Actual command from the disposable repository cwd, with common owned TMP/TEMP/TMPDIR, PYTHONUTF8=1/PYTHONDONTWRITEBYTECODE=1 and expanded network capability:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m08-live-20261109-734b10f3'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\live_m08.py" "$taskRoot\live-inputs.json" *> "$taskRoot\live.log"
$result=$LASTEXITCODE
```

The exact real-default application/adapter runner exited1 on its **first** case, before the second case or its final coverage checks. Actual sanitized result:

```text
case: photo-triple-riding-01
category: triple-riding
media_types: image
ai.state: failed
ai.failure_code: PROVIDER_REQUEST_REJECTED
ai.attempt_count: 1
workflow_status: awaiting-review
points: 0
assessment: null
returned model/modelVersion: unavailable
runner finding: Live provider case did not complete; actual failure recorded
```

This is a genuine terminal provider-request failure, not the anticipated incomplete image/video-coverage exit. The approved persistence seam does not retain HTTP status, request stage or provider rejection body; none is inferred. Actual selected-model inference/grounding was not demonstrated. The original first image was visually reviewed as road/motorcycle evidence with multiple visible riders; exact carried count cannot be established merely from its filename. With no assessment, semantic/citation/routing review of a model response is NOT RUN. The technical failure correctly left the claim officer-reviewable with no award/final decision; this does not make the live criterion pass.

Stopped the entire live batch immediately. No manual retry, repair call, fallback, alternative model, diagnostic inference or source patch occurred. The confirmed helmet case and later proposed unrelated-photo, unclear-road/red-light and mixed-image cases were NOT RUN after this failure. Video remains NOT RUN, user-manual testing deferred; that request does not waive the approved photo/video acceptance criterion. Account tier and current applicable pricing are unknown/unverified and were not a call gate.

The exact runner's TestClient context unwound and stopped/joined the worker on failure. Expanded final inspection found0owned live/Traffic Python processes. The full original checkout/key/sample metadata inventory matched exactly before evidence updates. Sanitized result, sanitized exit/failure metadata, exact runner and private input context are retained privately outside checkout; raw provider responses/prompts/token URLs were not archived. Only the adapter's best-effort deletion of valid attempt-owned returned Files was permitted; remote absence is unverified and no bulk deletion/listing occurred. Removed only the resolved literal owned live source/application/DB/media/log directory after exact Temp-parent/no-reparse guards, independently confirmed absent. Original key/photos, dirty source and existing private recovery backups remain intact.

```text
Exact live runner exit: 1
Owned live/Traffic Python processes: 0
Full checkout/key/original sample path-length-hash inventory unchanged
Owned disposable live app/source/media/DB/key-free inputs/log removed and independently absent
```

**Current status:** ASOR-M08 Blocked — actual live PROVIDER_REQUEST_REJECTED on first image, count1; cause pending separate read-only diagnosis/review.007 preserves its original approval/offline execution history and records live execution stopped; review is required before retrying the failed live criterion. M09 remains Pending. Remaining unperformed image/video/grounding cases are NOT RUN; R03/M08 are not complete.

## Exact application and stopped-data safeguards

Expanded read-only `Get-CimInstance Win32_Process` found no Python/uvicorn/decoder process; `Get-NetTCPConnection -State Listen` found no8000/8001 listener; `docker ps --no-trunc` returned an empty inventory. No demo instance needed stopping and no unknown process/container was stopped.

Before source changes, twice captured equal private185-file full absolute-path/length/SHA-256 inventories, excluding only .git/.venv/transient Python/pytest/deepeval caches. Saved exact current dirty app.py/durable.py preimages and confirmed gemini.py absent. Retained a new coherent stopped SQLite backup and corresponding media tree in a stable host-visible private location outside checkout, separate from predecessor recovery backups. The source connection used SQLite read-only mode; backup integrity_check was ok; both connections closed. Original main-DB length/hash stayed equal. Recovery data was never a verification fixture. Private paths, data values and hashes are not published here.

```python
source=sqlite3.connect((root/'roadwatch.db').as_uri()+'?mode=ro',uri=True)
dest=sqlite3.connect(private/'roadwatch.db')
try:
    source.backup(dest)
    assert dest.execute('pragma integrity_check').fetchone()[0]=='ok'
finally:
    dest.close();source.close()
shutil.copytree(root/'media_store',private/'media_store')
```

Mechanically extracted007's complete gemini.py block and both complete unified diffs. Both `git apply --check --ignore-whitespace` checks passed; both `git apply --ignore-whitespace` applications passed. Created only gemini.py; modified only app.py/durable.py. Three files parse; both reverse checks passed. Independent reapplication of the two diffs to saved dirty preimages produced byte-identical checkout files; complete Gemini block equals UTF-8 source. No test/dependency/config/bootstrap/future-milestone change. The patch tool reported the reviewed durable diff's final blank-line whitespace warning; no patch/code correction was made.

## Actual sequential offline verification

Executed003's exact approved source-only/real-decoder setup, replacing only its literal task-directory name:

```powershell
$document=Get-Content -Raw docs/.ai/ai-screening-officer-review/003_Implementation_Plan_Evidence_Intake_GREEN.md
$blocks=[regex]::Matches($document,'(?s)~~~powershell\r?\n(.*?)\r?\n~~~')
Invoke-Expression ($blocks[0].Groups[1].Value.Replace('asor-m04-execution-20261109-b4e82c10','asor-m08-execution-20261109-734b10f2'))
```

Only root Python/pytest.ini/tests/templates/static entered the frozen copy. No real DB/media/.local/.env/.git/.venv or recovery backup was copied into fixtures. Existing interpreter/dependencies/configuration unchanged. Genuine temporary media bytes were forwarded on stdin through existing `traffic-60e6e567315a-runner:latest` FFmpeg/ffprobe using `--network none --rm`. No fake decoder, installation or production Docker dependency.

Each next call used explicit disposable repository cwd `C:\Users\avina\AppData\Local\Temp\asor-m08-execution-20261109-734b10f2\repository` and expanded native Windows local socket capability. Common environment and actual commands below were executed sequentially; each launcher internally repeated without cleanup between repetitions. Each invocation captured `$LASTEXITCODE`, displayed its trimmed tail and threw on nonzero. No edits to frozen source while children ran.

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m08-execution-20261109-734b10f2'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_gemini_assessment.py" --green *> "$taskRoot\gemini.log"
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_durable_processing.py" --green *> "$taskRoot\durable.log"
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\intake.log"
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\probes.py" *> "$taskRoot\probes.log"
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\mechanical_check.py" *> "$taskRoot\mechanical.log"
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\check_integrity.py"
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\archive_checks.py"
```

All exited0. Actual trimmed output:

```text
green run 1 exit 0
47 passed, 1 warning in 52.70s
Classified 47 green nodes; no errors/skips
green run 2 exit 0
47 passed, 1 warning in 53.56s
Classified 47 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
green run 1 exit 0
14 passed, 1 warning in 20.88s
Classified 14 green nodes; no errors/skips
green run 2 exit 0
14 passed, 1 warning in 22.05s
Classified 14 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
intake run 1 result: 0
94 passed, 12 skipped, 1 warning in 127.59s (0:02:07)
intake run 2 result: 0
94 passed, 12 skipped, 1 warning in 142.95s (0:02:22)
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
Absolute transport timeout killed/reaped owned child; no network request
Equivalent limitation wording accepted; synthetic provider URL log suppressed and local URL retained
Retry-After numeric/date/past/negative/invalid probes passed
Synthetic old-schema migration twice preserved pending row/null snapshot; default worker failed configuration/count0 before client
Exact approved block and diffs independently reapplied to saved dirty preimages; all parse/equal
Every frozen source/test/config file matches checkout; external live runner parses without running
Independent protected inventory unchanged
Independent gemini inventory: 47 equal named nodes; 47 PASSED/0 SKIPPED each
Independent durable inventory: 14 equal named nodes; 14 PASSED/0 SKIPPED each
Independent intake inventory: 106 equal named nodes; 94 PASSED/12 SKIPPED each
Required repeated inventories equal; actual logs/scripts/metadata archived privately; no synthetic database/media archived
```

Unchanged bounds:90seconds Gemini/durable,180seconds intake per child. Explicit pytest-asyncio/no plugin autoload, provider/bootstrap environment stripping, UTF-8/no-bytecode, dynamic sockets, effective DB/media path and closed-connection guards stayed active. No failure/error/new skip/xfail/timeout, rerun-until-pass or widened bound occurred. Existing Starlette/httpx warning remains. Inherited subprocess waits are not an independent suite watchdog.

Narrow external-only probe mechanics follow007's recorded conditions: replaced only fixed child source locally with five-second sleep, used0.25second absolute deadline, captured real Popen and asserted owned child exited before TimeoutException handling completed; no outbound request. Independent validation accepted equivalent limitation wording with null video timing without literal officer/uncertain/timing keywords. Direct filter rejected a synthetic Google token URL and retained localhost health. Pure Retry-After numeric/date/past/negative/invalid cases passed. A synthetic old-schema pending row was migrated twice with original fields/count/null snapshot intact, integrity/FK checks passed; default worker with a synthetic key failed PROVIDER_CONFIGURATION/count0 before forbidden client construction. Worker stopped. All Python/live-runner blocks parsed; live runner never executed. These scratch probes are not new committed tests or live acceptance.

## Preservation, cleanup and limitations

Read-only backup created baseline-absent roadwatch.db-wal0bytes and roadwatch.db-shm32768bytes; these were explicitly attributed, not hidden. After checks, expanded process inspection found0owned Traffic/verification processes and0active containers. Baseline absence, original main-DB length/hash, WAL0, stable sidecar hashes and exclusive FileShare.None read handles on DB/WAL/SHM proved the exact sidecars inert/unheld. Handles closed; final WAL0/main-hash guards passed immediately before removing only those two literal files. No checkpoint, migration or real application lifespan/startup occurred.

Independent full185-file comparison before documentation updates found exactly app.py/durable.py changed, gemini.py alone added, no original deletion; every original test/config/other dirty source/document/real DB/media/.local byte equal. Private baseline/final inventories, source preimages, recovery SQLite/media and exact verification scripts/logs/metadata remain privately retained outside checkout. Predecessor private backups were untouched, never fixtures; no independent external-backup hash claim is made.

After archiving evidence, removed only the resolved literal owned execution tree, with exact path/Temp-parent/no-reparse guards and independent absence check:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m08-execution-20261109-734b10f2'
$resolved=(Resolve-Path -LiteralPath $taskRoot).Path
if($resolved -ne $taskRoot -or (Split-Path -Parent $resolved) -ne 'C:\Users\avina\AppData\Local\Temp' -or (Get-Item -LiteralPath $resolved).Attributes.HasFlag([IO.FileAttributes]::ReparsePoint)){throw 'Owned cleanup target guard failed'}
Remove-Item -LiteralPath $resolved -Recurse -Force
if(Test-Path -LiteralPath $taskRoot){throw 'Owned execution area remains'}
```

```text
Owned Traffic/verification processes: 0
Active containers: 0
Only two baseline-absent backup-created inert sidecars removed after WAL0/main-hash/exclusive-handle/process/hash guards; no checkpoint
Independent full 185-file baseline: exactly app.py/durable.py changed; gemini.py alone added; no original deletion
All original tests/configuration/other dirty source/docs/real DB/media/.local bytes equal; recovery backups retained and not fixtures
Owned literal disposable execution area removed and independently absent; private recovery/evidence retained
```

Command deviations are log redirection/trimmed tails, explicit stop checks and external-only probe/inventory helpers following007's described mechanics; setup source-only block, launcher order/arguments and90/180bounds unchanged. Initial absent root AGENTS.md lookup printed file-not-found; existing007 records no applicable AGENTS.md. One output-poll request was aborted before dispatch then read normally; no child was repeated. No auto-review rejection, provider failure or executable correction occurred. No stage/commit/publish/deployment, global Temp cleanup, unknown process stop, real media deletion or backup deletion.

Controlled provider wire bytes prove deterministic adapter/validation/persistence/routing behavior, not arbitrary semantic truth, visual accuracy, legal correctness or actual account/model availability. Native Windows decoder installation remains an outstanding deployment prerequisite. Twelve inherited media skips provide no coverage; seven historical API bodies remain setup-only; unrelated controls/OIDC infrastructure suites remain unchanged/unrun. No all-repository or deployment-readiness claim.

## Original offline snapshot — live NOT RUN then; superseded by follow-up above

No real private key or arbitrary representative media was discovered, read or used; no Google/provider/account/model call occurred. Only reviewed synthetic keys/media were used offline. The exact007 live protocol resumes on this same approved Implementation Plan after the user supplies private key-file path, ordered designated representative photo/video paths and Google transmission authorization, categories/context and qualitative expectations/limitations. Required genuine photo/video, three categories, irrelevance, mixed and unclear/no-apparent-violation coverage must be reviewed as specified; missing cases remain NOT RUN. Account free/paid/unknown tier and dated pricing basis are recorded; unknown tier/rates are allowed and do not block calls. No additional implementation reapproval is needed merely to supply inputs. Actual live defects would follow007's stop/replanning boundary.

Plan M08 is recorded Waiting,007 Human Review preserves approval and records offline execution/live waiting in one place, M09 stays Pending. No substitute-only closure of R03 or M08 completion.

## Complete equal named inventories

Each inventory below was independently extracted from both actual verbose logs and matched exactly, including full parametrized names.

### Gemini GREEN —47 nodes

```text
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
```

### Durable GREEN —14 nodes

```text
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
```

### Intake preservation —106 nodes

```text
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
```
