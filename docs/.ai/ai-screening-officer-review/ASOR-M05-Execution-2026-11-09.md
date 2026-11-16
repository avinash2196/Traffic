# ASOR-M05 Durable processing RED execution — 2026-11-09

Executed only ASOR-M05 for `ai-screening-officer-review` by a fresh-context test-engineer. Authority:004 Human Review approval by user2026-11-09, approved requirements/Plan/External Contract, and completed M02/M03/M04 evidence. No M06 planning or implementation, production/configuration/dependency change, live provider call, staging, commit or publication.

Applied exactly the two complete approved new files `tests/test_durable_processing.py` and `tests/verify_durable_processing.py` mechanically extracted from004. Both parsed and matched approved code after verification. No existing executable file changed. Before application, a stable host-visible private inventory captured 173 protected paths with length/SHA-256; repeated capture matched. Independent final comparison before documentation updates found exactly the two approved additions and no changed/deleted original paths, including original dirty M02/M03/M04 baseline, real DB/media/private-local and retained recovery backup. Private contents/hashes were never copied into verification inputs or published.

## Actual isolated commands and output

Setup extracted003's exact first PowerShell block with only the literal owned directory changed. Verification used its frozen allowlisted source-only copy as working directory, expanded Windows loopback, UTF-8/no-bytecode, stripped provider/bootstrap environment and owned temporary paths. Actual-byte offline FFmpeg/FFprobe forwarding used the existing carrier image with `--network none --rm`; no native decoder installation or readiness claim. Operations were sequential. No root pytest/real checkout lifespan/database migration or extra soundness probe.

```powershell
$document=Get-Content -Raw -LiteralPath 'docs/.ai/ai-screening-officer-review/003_Implementation_Plan_Evidence_Intake_GREEN.md'
$blocks=[regex]::Matches($document,'(?s)~~~powershell\r?\n(.*?)\r?\n~~~')
if($blocks.Count -ne 3){throw 'Approved setup block inventory changed'}
$setup=$blocks[0].Groups[1].Value.Replace('asor-m04-execution-20261109-b4e82c10','asor-m05-execution-20261109-c80be291')
Invoke-Expression $setup
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m05-execution-20261109-c80be291'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary";$env:TEMP=$env:TMP;$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1';$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\preservation.log"
if($LASTEXITCODE -ne 0){throw 'Preservation failed; stop and preserve evidence'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_durable_processing.py" --red *> "$taskRoot\red.log"
if($LASTEXITCODE -ne 0){throw 'RED classification failed; stop and preserve evidence'}
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\check_integrity.py"
if($LASTEXITCODE -ne 0){throw 'Independent protected inventory mismatch'}
```

Both helpers and independent integrity command exited0. Preservation retained its180-second child bound and unchanged six-module selection. RED retained90 seconds and exact new-file selection. Actual trimmed output:

```text
intake run 1 result: 0
============ 94 passed, 12 skipped, 1 warning in 158.49s (0:02:38) ============
intake run 2 result: 0
============ 94 passed, 12 skipped, 1 warning in 153.51s (0:02:33) ============
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
red run 1 exit 1
======================= 14 failed, 1 warning in 18.14s ========================
Classified 14 red nodes; no errors/skips
red run 2 exit 1
======================= 14 failed, 1 warning in 23.02s ========================
Classified 14 red nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
Independent protected inventory unchanged
Independent inventories:106 equal preservation nodes94/12;14 equal ordinary RED nodes; original path/length/SHA values unchanged
```

Every RED node failed in its test body with `AssertionError: DURABLE_PENDING_NOT_COMMITTED` and `assert None == 'pending'`; both children exited1 and classifier required exact14 membership, no errors/skips/xfails. This common earliest gate is not14 independently observed downstream failures; the approved planning-time soundness probe remains separate evidence, not repeated or claimed as M05 implementation.

Independent parsing of verbose node/status lines confirmed identical106-node preservation inventories (94 passes/12 preexisting skips) and identical14-node RED inventories. An initial private parsing assertion excluded spaces in a parameter name and variable alignment whitespace; corrected only the independent parser and re-read the same logs. No test, runner, bound or assertion changed and no verification was rerun. No other deviation or material mismatch occurred.

Existing Starlette/httpx deprecation warning remains. Seven old API bodies are setup-only;12 old media skips supply no coverage. Historical controls/OIDC tests remain unchanged/unrun. This is selected demo preservation, not an all-repository pass; no live model-quality evidence or full later contract coverage.

## Complete independent node/status inventories

Both runs matched each inventory below exactly.

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

```text
tests/test_durable_processing.py::test_pending_commit_survives_fresh_process_and_legacy_is_not_enqueued FAILED
tests/test_durable_processing.py::test_interrupted_attempts_are_consumed_across_process_recovery FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROVIDER_TRANSIENT-True] FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[ATTEMPT_TIMEOUT-True] FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROVIDER_CONFIGURATION-False] FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROVIDER_REQUEST_REJECTED-False] FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[INVALID_MODEL_OUTPUT-False] FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[MODEL_OUTPUT_UNAVAILABLE-False] FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[EVIDENCE_UNAVAILABLE-False] FAILED
tests/test_durable_processing.py::test_technical_outcomes_never_reject_and_retry_bound_is_durable[PROCESSING_ERROR-False] FAILED
tests/test_durable_processing.py::test_concurrent_claims_and_recovered_stale_completion_publish_once FAILED
tests/test_durable_processing.py::test_atomic_job_failure_does_not_accept_report_or_consume_upload FAILED
tests/test_durable_processing.py::test_acceptance_returns_during_background_dispatch_and_attempt_precedes_call FAILED
tests/test_durable_processing.py::test_obsolete_evidence_completion_is_superseded FAILED
```

## Owned cleanup and execution status

After archiving actual commands/output and complete inventories, expanded process inspection found0 Python processes matching the literal owned execution directory; `docker ps --format '{{.Names}}'` returned empty. Each helper had reaped its children/HTTP servers and removed nested test state. From checkout, exact resolved-path equality was asserted before `Remove-Item -LiteralPath ... -Recurse -Force` for only `C:\Users\avina\AppData\Local\Temp\asor-m05-execution-20261109-c80be291` and the separately owned preinventory area `C:\Users\avina\AppData\Local\Temp\asor-m05-pre-20261109-c80be291`. Both absence checks passed. Retained M04 private recovery backup was not removed or modified.

Actual cleanup output:

```text
Owned Python processes: 0
Owned execution and preinventory areas absent: True
```

Only after successful verification/inventory/cleanup, Plan's M05 execution row and004 Human Review were updated to Executed. M06 and later remain Pending and unauthorized. No future planning or implementation occurred.
