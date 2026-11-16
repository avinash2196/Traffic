# ASOR-M03 execution evidence — 2026-11-09

Executed only the approved Evidence Intake RED milestone in work item `ai-screening-officer-review`, by a fresh-context test-engineer role. Authority: [002 approved Implementation Plan](002_Implementation_Plan_Evidence_Intake_RED.md), Human Review user approval 2026-11-09; approved requirements, Plan, External Contract and completed M02 evidence. M04 remains Pending. No production implementation, provider call, staging, commit or publication occurred.

## Applied scope and exactness

Applied the exact complete new `tests/test_evidence_intake.py`, exact complete `tests/verify_current_demo.py`, and exact unified diff for `tests/test_api_endpoints.py` extracted from 002. Mechanical `git apply --check --ignore-whitespace` passed before application. New contents matched the proposal, all three parsed, and reverse API patch check passed. Preserved submission success assertions; its valid owned JPEG upload precondition now fails in the test body, not setup. No configuration, dependency, schema source, production or global fixture change.

A private preapplication path/length/SHA-256 inventory covered 167 repository files, excluding `.git`, `.venv`, node_modules and caches; real database/media/private-local values were hashed only, never copied as input. In that same invocation, final comparison verified exactly two modified files (API/runner), exactly one new intake test and no other path/length/hash change. M02's dirty baseline was retained. Independent reconstruction of approved M02 diffs from HEAD in an owned source-only folder verified unchanged conftest/auth/harness, and API equal to M02 plus the exact M03 diff (normalized text).

The first private baseline/preimages were placed in the restricted execution environment's per-invocation Temp. That area was inaccessible in later invocations (different sandbox Temp identity); it cannot support a claimed independent final 167-file comparison or independent cleanup certification. No user state was copied there. A stable host-visible post-application private 168-file inventory was then captured and verified identical after successful verification, before status/evidence edits. The approved runner independently held its protected root/source/test/config/database/media/private-local path/hash snapshot through the successful repeated checks and verified equality. This limitation is disclosed rather than inventing retained preimages or a broader end-to-end private comparison.

## Actual verification and deviations

Only the standard-library isolated launcher was run from the checkout. No root pytest/app startup, real DB/media/private-local copy, Docker, fixture regeneration or provider call occurred. Existing Python/dependency versions were used unchanged. Windows socket support required expanded local execution, as documented in M02/002; no event-loop change.

An initial output-redirection attempt pointed to the restricted Temp path from expanded execution and failed before Python launched (`Could not find a part of the path`). A fresh owned host-visible evidence directory was created at `C:\Users\avina\AppData\Local\Temp\asor-m03-execution-20261109-6e92b57c`.

The first actual launcher invocation was the verification shorthand with output capture:

```powershell
& .\.venv\Scripts\python.exe .\tests\verify_current_demo.py --intake-red *> 'C:\Users\avina\AppData\Local\Temp\asor-m03-execution-20261109-6e92b57c\execution.log'
```

It completed both preservation runs. Its first RED child returned 1 and was reaped; printing its Unicode filename failure log raised Windows cp1252 UnicodeEncodeError in the parent launcher, before classification/second RED/final hash guard. This invocation exited 1 and is not accepted RED evidence. Its owned `asor-m02-4rxj05xf` scratch directory was independently absent afterward and no owned Python process remained. Actual trimmed output:

```text
preservation run 1 result: 0
========== 40 passed, 12 skipped, 1 deselected, 1 warning in 35.86s ===========
preservation passed 40 failed 0 errors 0 skipped 12
preservation run 2 result: 0
========== 40 passed, 12 skipped, 1 deselected, 1 warning in 35.62s ===========
preservation passed 40 failed 0 errors 0 skipped 12
red run 1 result: 1
UnicodeEncodeError: 'charmap' codec can't encode character '\u96ea' in position 64158: character maps to <undefined>
```

Corrected only the invocation encoding using the UTF-8/no-bytecode environment already documented in 002 planning verification; the exact reviewed runner/tests, selections, assertions, timeout bounds and classifier were unchanged. This rerun addresses a demonstrated output-encoding prerequisite, not a retry to hide a behavior failure:

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& .\.venv\Scripts\python.exe .\tests\verify_current_demo.py --intake-red *> 'C:\Users\avina\AppData\Local\Temp\asor-m03-execution-20261109-6e92b57c\execution-utf8.log'
```

Actual launcher exit 0. Its owned source-only copy ran each selection twice, without resetting between pairs, under owned TMP/TEMP/TMPDIR with provider/bootstrap environment stripped. Child executable was the existing checkout `.venv\Scripts\python.exe`; exact child argument patterns (the XML paths use the run's owned scratch, never checkout data):

```text
-m pytest -p pytest_asyncio.plugin -v --junitxml=C:\Users\avina\AppData\Local\Temp\asor-m02-qooga4yw\preservation-1.xml tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py --deselect=tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id
-m pytest -p pytest_asyncio.plugin -v --junitxml=C:\Users\avina\AppData\Local\Temp\asor-m02-qooga4yw\preservation-2.xml tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py --deselect=tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id
-m pytest -p pytest_asyncio.plugin -v --junitxml=C:\Users\avina\AppData\Local\Temp\asor-m02-qooga4yw\red-1.xml tests/test_evidence_intake.py tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id
-m pytest -p pytest_asyncio.plugin -v --junitxml=C:\Users\avina\AppData\Local\Temp\asor-m02-qooga4yw\red-2.xml tests/test_evidence_intake.py tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id
```

Actual trimmed successful output:

```text
preservation run 1 result: 0
========== 40 passed, 12 skipped, 1 deselected, 1 warning in 33.82s ===========
preservation passed 40 failed 0 errors 0 skipped 12
preservation run 2 result: 0
========== 40 passed, 12 skipped, 1 deselected, 1 warning in 33.44s ===========
preservation passed 40 failed 0 errors 0 skipped 12
red run 1 result: 1
======================= 54 failed, 1 warning in 55.78s ========================
red passed 0 failed 54 errors 0 skipped 0
Classified 54 intended RED assertions: valid authenticated upload returned 401 instead of 201
red run 2 result: 1
======================= 54 failed, 1 warning in 42.28s ========================
red passed 0 failed 54 errors 0 skipped 0
Classified 54 intended RED assertions: valid authenticated upload returned 401 instead of 201
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
```

JUnit classifier accepted exactly 54 ordinary assertion failures each time, no errors/skips/unexpected passes: valid authenticated upload returned 401 rather than 201. The 53 new native HTTP bodies plus corrected existing TestClient body all reached that intended positive gate. This is common-gate RED evidence, not independent proof of every downstream guard or GREEN behavior. Embedded validated synthetic fixtures required no external decoding tool during execution. M02's two lifecycle/isolation tests passed in both preservation runs; dynamic real HTTP server fixture shutdown assertions completed before each lifespan closed.

Independent log inspection confirmed both preservation node/status sequences identical and exactly the M02 53-node inventory minus the explicitly moved submission; both RED node/status sequences identical, exactly 53 new-file nodes plus that moved submission. Native exit 1 alone was never treated as sufficient. No new skip, xfail, setup/import error, timeout or assertion weakening was accepted. Existing Starlette/httpx deprecation warning remained; no dependency update.

## Preserved scope and coverage limits

The seven unchanged API nodes with commented HTTP/assertion bodies remain setup-only passes. Twelve existing media skips provide no media coverage. Historical controls/OIDC infrastructure tests remain unrun, not claimed passing; no historical services started. Current RED stops at the shared missing upload identity boundary, so downstream assertions and later AI/jobs/officer/recovery/provider behavior are not claimed executed to completion. Planning-only scratch soundness is prior evidence, not production GREEN or release evidence. Native subprocess.wait bounds remain 90 seconds for preservation/RED, not an independent wall-clock watchdog; the inherited scheduling caveat remains.

## Repeated preservation inventory

Both runs produced this exact 52-node inventory; the moved node ran separately in RED:

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
```

## Repeated intended RED inventory

Both runs produced this exact 54-node inventory, classified by actual JUnit assertions:

```text
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpeg-a.jpg] FAILED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpg-a.jpg] FAILED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[png-image/png-a.png] FAILED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4] FAILED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mov-video/quicktime-a.mov] FAILED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[avi-video/x-msvideo-a.avi] FAILED
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[long-video/mp4-a.mp4] FAILED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485759] FAILED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485760] FAILED
tests/test_evidence_intake.py::test_chunked_actual_byte_boundary[10485761] FAILED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[-image/jpeg-INVALID_MEDIA] FAILED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[not an image-image/jpeg-INVALID_MEDIA] FAILED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[\xff\xd8\xffbroken-image/jpeg-INVALID_MEDIA] FAILED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[GIF89a-image/gif-UNSUPPORTED_MEDIA_TYPE] FAILED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[\x1aE\xdf\xa3webm-video/webm-UNSUPPORTED_MEDIA_TYPE] FAILED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[https://example.invalid/evidence.jpg-image/jpeg-INVALID_MEDIA] FAILED
tests/test_evidence_intake.py::test_reject_invalid_upload_without_visible_handle[C:\outside\evidence.jpg-image/jpeg-INVALID_MEDIA] FAILED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[png_as_jpeg] FAILED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[video_as_image] FAILED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[image_as_video] FAILED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[audio_only] FAILED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[truncated_video] FAILED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[mp4_as_mov] FAILED
tests/test_evidence_intake.py::test_declared_mime_must_match_decodable_visual_container[mov_as_mp4] FAILED
tests/test_evidence_intake.py::test_multipart_contract[missing] FAILED
tests/test_evidence_intake.py::test_multipart_contract[wrong] FAILED
tests/test_evidence_intake.py::test_multipart_contract[multiple] FAILED
tests/test_evidence_intake.py::test_multipart_contract[malformed] FAILED
tests/test_evidence_intake.py::test_unknown_multipart_fields_and_generated_display_filename FAILED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[../escaped.jpg] FAILED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[C:\\temp\\escaped.jpg] FAILED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[https://example.invalid/a.jpg] FAILED
tests/test_evidence_intake.py::test_display_filename_cannot_select_storage_or_urls[unicode-\u96ea.jpg] FAILED
tests/test_evidence_intake.py::test_citizen_authentication_and_invalid_bearer_precedence FAILED
tests/test_evidence_intake.py::test_duplicate_privacy_unattached_replay_and_attached_new_handle FAILED
tests/test_evidence_intake.py::test_mixed_ordered_owned_unattached_evidence_and_singular_compatibility FAILED
tests/test_evidence_intake.py::test_changed_json_boundary_rejects_malformed_nonobject_and_content_type FAILED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[missing-MEDIA_NOT_FOUND-404] FAILED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[foreign-FORBIDDEN-403] FAILED
tests/test_evidence_intake.py::test_rejected_attachment_is_atomic_and_preserves_orphans[attached-MEDIA_ALREADY_ATTACHED-409] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[both] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[empty] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[null] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[duplicate] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[blank] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[wrong_type] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[category] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[number] FAILED
tests/test_evidence_intake.py::test_report_validation_does_not_consume_upload[location] FAILED
tests/test_evidence_intake.py::test_competing_creates_cannot_reassociate_same_attachment FAILED
tests/test_evidence_intake.py::test_private_returned_officer_url_credentials_and_exact_basename FAILED
tests/test_evidence_intake.py::test_legacy_metadata_paths_are_contained_and_owner_is_not_guessed FAILED
tests/test_evidence_intake.py::test_safe_zip_names_preserve_display_metadata FAILED
tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id FAILED
```

## Integrity and owned cleanup

The successful runner reported protected paths/SHA-256 equality, waited/reaped every child and removed its owned disposable repository/test state. Independent stable post-application inventory check matched all 168 path/length/hash entries before documentation status edits. Independent process/existence check:

```text
Successful owned scratch absent: True
Matching owned Python processes: 0
```

Only this task's literal host-visible evidence directory and its source-only mechanical reconstruction/log/inventory contents are removed after archiving the relevant trimmed real output and inventories here. No unknown Temp path, historical M02 state, existing service/container or user data is cleaned. The restricted per-invocation Temp retention limitation above and historical M02 synthetic-temp attribution caveat remain explicitly unresolved. No missing hash baseline or old uncertainty is relabelled verified cleanup.

Only Plan M03 execution status and 002 Human Review are updated after verification; all other Plan scope/status rows, including M04 Pending, and authoritative requirements/contract remain unchanged. Completing RED does not authorize GREEN.
