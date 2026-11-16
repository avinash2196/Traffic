# ASOR-M07 Gemini assessment RED execution — 2026-11-09

Executed only ASOR-M07 for `ai-screening-officer-review` by a fresh-context test-engineer role. Authority:006 Human Review user approval2026-11-09; approved requirements/Plan/External Contract,001–005 approved predecessor plans and M02–M06 evidence. No production/configuration/dependency/other test change, provider call, live account/model/key access, soundness-probe repeat, M08 planning/implementation, staging, commit or publication.

## Exact files and data protection

Mechanically extracted006's two `~~~~python` blocks into tests/test_gemini_assessment.py and tests/verify_gemini_assessment.py, using UTF-8 bytes with the block's terminating newline. Both parse and equal the approved blocks exactly before and after verification. These are the only executable additions; every pre-existing dirty source/test/configuration byte is preserved.

Before either addition, captured a stable host-visible private full absolute-path/length/SHA-256 inventory twice, with equal180-file results. Inventory includes Markdown, source/tests/configuration, real database/sidecars/media/.local and excludes only .git/.venv/transient Python/pytest/deepeval caches. Independent post-verification comparison found all180 original paths/lengths/hashes equal, no deleted original, and exactly the two authorized additions. The carried setup also independently protects non-Markdown originals. Every file in the frozen source-only outer repository matched checkout after all checks. Detailed private inventories and actual log/setup/decoder copies remain retained outside checkout; private paths/data values/hashes are not published. Prior private recovery folders were left entirely untouched, never inspected or used as fixtures; no independent hash claim is made about external backup folders.

No root pytest, real checkout lifespan/migration, real DB connection, media copying into fixtures or recovery-backup use occurred. Source-only allowlist copied root Python/pytest.ini/tests/templates/static, excluding real DB/media/.local/.env/.git/.venv. Existing host venv and dependencies unchanged. Genuine temporary media bytes were decoded through existing carrier traffic-60e6e567315a-runner:latest using stdin and --network none --rm. No fake decoder, dependency installation or production Docker requirement.

## Actual sequential verification commands

The setup was extracted and executed with only003's literal task directory replaced:

```powershell
$document=Get-Content -Raw -LiteralPath 'docs/.ai/ai-screening-officer-review/003_Implementation_Plan_Evidence_Intake_GREEN.md'
$blocks=[regex]::Matches($document,'(?s)~~~powershell\r?\n(.*?)\r?\n~~~')
if($blocks.Count -ne 3){throw 'Approved setup block inventory changed'}
$setup=$blocks[0].Groups[1].Value.Replace('asor-m04-execution-20261109-b4e82c10','asor-m07-execution-20261109-c67e91ab')
Invoke-Expression $setup
```

Each next invocation used explicit disposable repository working directory `C:\Users\avina\AppData\Local\Temp\asor-m07-execution-20261109-c67e91ab\repository` and expanded Windows local socket capability from the start. Exact common environment and actual commands (separate sequential invocations):

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m07-execution-20261109-c67e91ab'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"; $env:TEMP=$env:TMP; $env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'; $env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_durable_processing.py" --green *> "$taskRoot\green.log"
if($LASTEXITCODE -ne 0){throw 'Durable preservation failed; stop'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\intake.log"
if($LASTEXITCODE -ne 0){throw 'Intake preservation failed; stop'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_gemini_assessment.py" --red *> "$taskRoot\red.log"
if($LASTEXITCODE -ne 0){throw 'Assessment RED classification failed; stop'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\check_integrity.py"
if($LASTEXITCODE -ne 0){throw 'Protected inventory changed'}
```

All launchers and integrity command exited0. Each launcher internally repeats its selection without cleanup between repetitions. Frozen source/test/configuration was never edited while any verification child ran. Child commands use existing interpreter, `-m pytest -p pytest_asyncio.plugin -v`; durable/Gemini include temporary JUnit paths. Plugin autoload disabled; inherited provider/bootstrap environment stripped; owned TMP/TEMP/TMPDIR; asserted real schema/effective DB/media paths and closed connections. Bounds unchanged90s durable/Gemini and180s intake. No failure/timeout or retry-until-pass occurred.

Actual trimmed output:

```text
green run 1 exit 0
======================= 14 passed, 1 warning in 16.85s ========================
Classified 14 green nodes; no errors/skips
green run 2 exit 0
======================= 14 passed, 1 warning in 20.92s ========================
Classified 14 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
intake run 1 result: 0
============ 94 passed, 12 skipped, 1 warning in 73.13s (0:01:13) =============
intake run 2 result: 0
============ 94 passed, 12 skipped, 1 warning in 104.94s (0:01:44) ============
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
red run 1 exit 1
======================= 47 failed, 1 warning in 17.99s ========================
Classified 47 red nodes; no errors/skips
red run 2 exit 1
======================= 47 failed, 1 warning in 17.52s ========================
Classified 47 red nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
Independent protected inventory unchanged
Independent green inventory:14 equal nodes;14 PASSED each
Independent intake inventory:106 equal nodes;94 PASSED/12 SKIPPED each
Independent red inventory:47 equal nodes;47 FAILED each
All180 original paths/lengths/hashes unchanged; exactly two approved additions
Every frozen source file matches checkout; exact approved blocks parse and match
Remaining owned nested temporary entries:0
```

The new launcher independently validates all47 exact JUnit names, no setup/teardown errors/skips/xfails/unexpected pass, and every failure contains the ordinary test-body `AssertionError: GEMINI_ASSESSMENT_NOT_COMPLETED` and `assert 'failed' == 'completed'`. Current default worker deliberately yields terminal PROVIDER_CONFIGURATION/count0/no assessment, so each node reaches the positive completed-assessment gate before future fields/imports. These are intended missing-integration failures, not missing-symbol/import/setup failures. This RED evidence does not independently exercise downstream negative assertions. The prior planning soundness probe was not repeated or represented as execution. Controlled transport bytes establish no live model availability or visual accuracy.

## Cleanup, deviations and limitations

After independent inventories/exact-block/source/whole-original hash checks, archived actual logs and metadata privately. Expanded Get-CimInstance inspection found0owned Traffic/verification Python/uvicorn; docker ps --no-trunc returned0active containers. All children returned/reaped; owned nested temporary directory empty. Resolved exact literal taskRoot, checked expected parent and no reparse point, removed only that tree, then independently checked absence:

```powershell
$resolved=(Resolve-Path -LiteralPath $taskRoot).Path
if($resolved -ne $taskRoot -or (Split-Path -Parent $resolved) -ne 'C:\Users\avina\AppData\Local\Temp' -or (Get-Item -LiteralPath $resolved).Attributes.HasFlag([IO.FileAttributes]::ReparsePoint)){throw 'Owned target guard failed'}
Remove-Item -LiteralPath $resolved -Recurse -Force
if(Test-Path -LiteralPath $taskRoot){throw 'Owned scratch remains'}
```

```text
Owned Traffic/verification processes:0
Active containers:0
Owned literal execution area removed and independently absent; private evidence/recovery preserved
```

No unknown process/container stopped, global Temp cleanup, real state deletion, checkpoint, backup deletion or real startup. Initial read-only lookup of absent root AGENTS.md and guessed003 filename printed file-not-found; corrected to actual003 filename. Read-only ancestor search completed and was reaped. One session-output poll was aborted before dispatch and then read successfully; no verification child was repeated or changed. Command deviations are only explicit log redirection, stop checks and trimmed-tail display for review; source-only setup and required runner order/arguments/bounds unchanged. No executable prerequisite workaround was introduced.

Native Windows decoder installation remains an unmet deployment prerequisite; offline real-decoder forwarding does not establish deployment readiness. Existing Starlette/httpx warning remains. Twelve inherited skipped media nodes provide no coverage, seven historical API passes remain setup-only, historical controls/OIDC infrastructure tests unchanged/unrun; no all-repository pass claim. Inherited subprocess.wait bounds are not independent absolute watchdogs. Real provider/account/model availability, semantic/visual quality and live M08/M17 obligations remain unverified. No provider credential or model call occurred; only synthetic provider key appears in reviewed test fixtures.

Only after verified checks and cleanup, M07's Plan execution row and006 Human Review were marked Executed. M08 remains Pending, with no next-milestone planning or implementation.

## Complete repeated node/status inventories

Both repetitions independently matched each full inventory below exactly.

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

### Gemini RED —47 nodes

```text
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[helmet] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[triple-riding] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[red-light] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[irrelevant] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[mixed] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[uncertain] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[no-violation] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[low-score] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[context] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[prompt-injection] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[foreign-file] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-file] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[external-path] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-key] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[wrong-model] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[bad-timeout] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[bad-base] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[bad-max] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[snapshot] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[retry-after] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[deadline] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[upload-deadline] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[blocked] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[refusal] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[empty] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[markdown] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-score] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[boolean-score] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[float-score] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[out-of-range] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[unknown-media] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[missing-attachment] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[duplicate-attachment] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[invented-law] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[foreign-url] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[video-time] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[blank-note] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[blank-explanation] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[empty-limitations] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[conflict] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[transient] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[unauthorized] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[unsupported] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[processing-failed] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[evil-upload] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[evil-file-uri] FAILED
tests/test_gemini_assessment.py::test_selected_gemini_policy_transport_and_failure_boundary[injected-authority] FAILED
```
