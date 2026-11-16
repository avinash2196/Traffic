# ASOR-M02 execution evidence

Executed 2026-11-09, America/Chicago, from the recorded user-approved ASOR-M02 OTHER Implementation Plan. Its Human Review approval, approved requirements/Plan/External Contract, M01 Completed predecessor and M02 Pending row were confirmed before source writes. This executes M02 only; M03 and later remain Pending.

## Applied scope and preservation

Applied exactly the three approved unified diffs to tests/conftest.py, tests/test_auth.py and tests/test_api_endpoints.py, and extracted the two complete approved new files tests/test_verification_harness.py and tests/verify_current_demo.py. Mechanical git apply --check passed before source writes; reverse check passed afterward. All five files parsed. Q15 alone adds required synthetic vehicle_number and corrects the existing status assertion/docstring to awaiting-review. Authentication test bodies and remaining API assertions are preserved. No production, dependency, configuration, workflow or provider changes.

Before writes, independently captured a private 163-file path/length/SHA-256 inventory covering existing source/tests/configuration, database/sidecars, media and private local paths; preserved the three test preimages in a uniquely owned host-visible OS Temp folder. No real DB/media/private-local content was copied into test input. Final independent comparison found exactly the three approved modified tests and two approved new helpers; all other inventoried paths/bytes were unchanged. Hash values and private data are not published here. The launcher's separate protected-source/state hash guard also passed.

## Actual verification

The approved root entry point below imports only the standard library. No root pytest or app startup was invoked. Expanded local execution supplied Windows event-loop/self-pipe capability; no event-loop policy or test changes were made. Existing virtual-environment interpreter and dependencies were used.

```powershell
& .\.venv\Scripts\python.exe .\tests\verify_current_demo.py *> C:\Users\avina\AppData\Local\Temp\asor-m02-execution-20261109-0f59f8166055470fb48dda45be7a1728\execution.log
```

Launcher exit: 0. Its exact approved child command ran twice in the same allowlisted disposable repository with no reset between runs apart from fixtures:

```text
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe -m pytest -p pytest_asyncio.plugin -v tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py
```

Both runs collected the same 53 nodes: 41 passed, 12 existing skips, one existing Starlette/httpx deprecation warning; durations 34.46 s and 33.84 s. No failure, timeout, new skip or xfail. The two harness checks prove effective real schema/database/media containment and independently closed lifespans with no sentinel reuse. The six synthetic identity checks and 23 auth tests passed. The seven unchanged API nodes whose HTTP calls/assertions are commented are setup-only passes, not officer/clarification behavior coverage; the twelve media skips provide no upload/media/ownership coverage. This is the approved selected preservation set, not an all-repository pass or RED evidence.

Existing tests/test_controls.py and tests/test_identity_oidc.py remain unrun: their historical private DSN/CA/Keycloak/service/browser prerequisites are absent; no historical infrastructure was started. Their bytes were preserved. No live provider call was made. The timeout mechanism remains native subprocess.wait(timeout=90), not an independent strict wall-clock watchdog; this run does not resolve the planning-time clock/scheduling limitation.

## Cleanup and limitations

The runner reported both children finished/reaped, protected hashes unchanged, and owned disposable repository/test state removed. Independent existence check confirmed its exact root C:\Users\avina\AppData\Local\Temp\asor-m02-ul3r4m0s absent. Expanded process inspection after completion showed no Python process belonging to this launcher/test run (unrelated processes were left untouched). Restricted process inspection was denied by the host; expanded read-only inspection succeeded, without affecting tests.

All current execution synthetic outputs are archived below before removing only this execution's independently verified literal private temporary evidence directory. No unknown Temp paths were deleted. The original planning private evidence directory was left untouched. Its previously disclosed global Temp synthetic-database attribution/cleanup uncertainty remains unresolved; this successful owned-tree cleanup does not erase or cure that historical limitation. No pre-authorized contingency or scope deviation was used; output redirection and read-only integrity/process checks are execution evidence handling only.

## Complete synthetic launcher output

```text
Run 1 result: 0
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.7.0 -- C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\avina\AppData\Local\Temp\asor-m02-ul3r4m0s\repository
configfile: pytest.ini
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 53 items

tests/test_auth.py::TestSignup::test_signup_with_valid_data_returns_201 PASSED [  1%]
tests/test_auth.py::TestSignup::test_signup_with_duplicate_citizen_id_returns_409 PASSED [  3%]
tests/test_auth.py::TestSignup::test_signup_with_duplicate_email_returns_409 PASSED [  5%]
tests/test_auth.py::TestSignup::test_signup_with_invalid_email_returns_400 PASSED [  7%]
tests/test_auth.py::TestSignup::test_signup_with_missing_email_returns_400 PASSED [  9%]
tests/test_auth.py::TestSignup::test_signup_with_missing_password_returns_400 PASSED [ 11%]
tests/test_auth.py::TestSignup::test_signup_with_short_password_returns_400 PASSED [ 13%]
tests/test_auth.py::TestSignup::test_signup_password_is_hashed_not_plaintext PASSED [ 15%]
tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200 PASSED [ 16%]
tests/test_auth.py::TestLogin::test_login_with_invalid_password_returns_401 PASSED [ 18%]
tests/test_auth.py::TestLogin::test_login_with_nonexistent_citizen_returns_401 PASSED [ 20%]
tests/test_auth.py::TestLogin::test_login_returns_session_token PASSED   [ 22%]
tests/test_auth.py::TestLogin::test_login_updates_last_login_timestamp PASSED [ 24%]
tests/test_auth.py::TestLogout::test_logout_returns_204_no_content PASSED [ 26%]
tests/test_auth.py::TestLogout::test_logout_without_token_returns_401 PASSED [ 28%]
tests/test_auth.py::TestAccessControl::test_accessing_reports_without_token_returns_401 PASSED [ 30%]
tests/test_auth.py::TestAccessControl::test_accessing_reports_with_invalid_token_returns_401 PASSED [ 32%]
tests/test_auth.py::TestAccessControl::test_citizen_can_see_own_reports PASSED [ 33%]
tests/test_auth.py::TestAccessControl::test_citizen_cannot_see_other_citizens_reports PASSED [ 35%]
tests/test_auth.py::TestAccessControl::test_citizen_id_from_token_used_for_reports PASSED [ 37%]
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_returns_profile PASSED [ 39%]
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_without_token_returns_401 PASSED [ 41%]
tests/test_auth.py::TestIntegration::test_complete_citizen_workflow PASSED [ 43%]
tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id PASSED [ 45%]
tests/test_api_endpoints.py::TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports PASSED [ 47%]
tests/test_api_endpoints.py::TestCitizenReportDetails::test_citizen_fetch_report_details_with_timeline PASSED [ 49%]
tests/test_api_endpoints.py::TestOfficerReviewQueue::test_officer_query_review_queue_returns_paginated_list PASSED [ 50%]
tests/test_api_endpoints.py::TestOfficerCaseDetail::test_officer_view_case_detail_shows_evidence PASSED [ 52%]
tests/test_api_endpoints.py::TestOfficerApproval::test_officer_approve_report_awards_points PASSED [ 54%]
tests/test_api_endpoints.py::TestOfficerRejection::test_officer_reject_with_reason_stores_reason PASSED [ 56%]
tests/test_api_endpoints.py::TestOfficerClarificationRequest::test_officer_request_clarification_requeues_case PASSED [ 58%]
tests/test_api_endpoints.py::TestCitizenClarification::test_citizen_clarification_response_resubmits_case PASSED [ 60%]
tests/test_api_endpoints.py::TestOfficerQueueUpdate::test_officer_queue_reflects_requeued_cases PASSED [ 62%]
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_jpeg_returns_media_id_and_hash SKIPPED [ 64%]
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_mp4_video_returns_media_id SKIPPED [ 66%]
tests/test_media.py::TestMediaUploadValidation::test_duplicate_file_returns_409_conflict SKIPPED [ 67%]
tests/test_media.py::TestMediaUploadValidation::test_file_too_large_returns_413_payload_too_large SKIPPED [ 69%]
tests/test_media.py::TestMediaUploadValidation::test_video_too_long_returns_413 SKIPPED [ 71%]
tests/test_media.py::TestMediaUploadValidation::test_unsupported_file_format_returns_422 SKIPPED [ 73%]
tests/test_media.py::TestMediaUploadValidation::test_corrupted_jpeg_returns_422 SKIPPED [ 75%]
tests/test_media.py::TestTechnicalScreening::test_low_resolution_image_flags_warning SKIPPED [ 77%]
tests/test_media.py::TestTechnicalScreening::test_high_blur_video_flags_warning SKIPPED [ 79%]
tests/test_media.py::TestMediaAccessControl::test_citizen_can_download_own_media SKIPPED [ 81%]
tests/test_media.py::TestMediaAccessControl::test_citizen_cannot_download_other_citizens_media SKIPPED [ 83%]
tests/test_media.py::TestMediaAccessControl::test_officer_can_download_any_media SKIPPED [ 84%]
tests/test_verification_harness.py::test_real_schema_and_effective_paths PASSED [ 86%]
tests/test_verification_harness.py::test_independent_lifespans_close_and_do_not_reuse_state PASSED [ 88%]
tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source PASSED [ 90%]
tests/test_identity.py::test_claim_validation_and_error_contract PASSED  [ 92%]
tests/test_identity.py::test_human_permission_boundary_without_business_handlers PASSED [ 94%]
tests/test_identity.py::test_fixed_service_client_audience_scope_matrix PASSED [ 96%]
tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache PASSED [ 98%]
tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers PASSED [100%]

============================== warnings summary ===============================
..\..\..\..\..\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ===========================
SKIPPED [1] tests\test_media.py:50: M3.2 implementation required
SKIPPED [1] tests\test_media.py:72: M3.2 implementation required
SKIPPED [1] tests\test_media.py:95: M3.2 implementation required
SKIPPED [1] tests\test_media.py:117: M3.2 implementation required
SKIPPED [1] tests\test_media.py:139: M3.2 implementation required
SKIPPED [1] tests\test_media.py:161: M3.2 implementation required
SKIPPED [1] tests\test_media.py:183: M3.2 implementation required
SKIPPED [1] tests\test_media.py:219: M3.2 implementation required
SKIPPED [1] tests\test_media.py:242: M3.2 implementation required
SKIPPED [1] tests\test_media.py:265: M3.2 implementation required
SKIPPED [1] tests\test_media.py:285: M3.2 implementation required
SKIPPED [1] tests\test_media.py:304: M3.2 implementation required
================= 41 passed, 12 skipped, 1 warning in 34.46s ==================

Run 2 result: 0
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.7.0 -- C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\avina\AppData\Local\Temp\asor-m02-ul3r4m0s\repository
configfile: pytest.ini
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 53 items

tests/test_auth.py::TestSignup::test_signup_with_valid_data_returns_201 PASSED [  1%]
tests/test_auth.py::TestSignup::test_signup_with_duplicate_citizen_id_returns_409 PASSED [  3%]
tests/test_auth.py::TestSignup::test_signup_with_duplicate_email_returns_409 PASSED [  5%]
tests/test_auth.py::TestSignup::test_signup_with_invalid_email_returns_400 PASSED [  7%]
tests/test_auth.py::TestSignup::test_signup_with_missing_email_returns_400 PASSED [  9%]
tests/test_auth.py::TestSignup::test_signup_with_missing_password_returns_400 PASSED [ 11%]
tests/test_auth.py::TestSignup::test_signup_with_short_password_returns_400 PASSED [ 13%]
tests/test_auth.py::TestSignup::test_signup_password_is_hashed_not_plaintext PASSED [ 15%]
tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200 PASSED [ 16%]
tests/test_auth.py::TestLogin::test_login_with_invalid_password_returns_401 PASSED [ 18%]
tests/test_auth.py::TestLogin::test_login_with_nonexistent_citizen_returns_401 PASSED [ 20%]
tests/test_auth.py::TestLogin::test_login_returns_session_token PASSED   [ 22%]
tests/test_auth.py::TestLogin::test_login_updates_last_login_timestamp PASSED [ 24%]
tests/test_auth.py::TestLogout::test_logout_returns_204_no_content PASSED [ 26%]
tests/test_auth.py::TestLogout::test_logout_without_token_returns_401 PASSED [ 28%]
tests/test_auth.py::TestAccessControl::test_accessing_reports_without_token_returns_401 PASSED [ 30%]
tests/test_auth.py::TestAccessControl::test_accessing_reports_with_invalid_token_returns_401 PASSED [ 32%]
tests/test_auth.py::TestAccessControl::test_citizen_can_see_own_reports PASSED [ 33%]
tests/test_auth.py::TestAccessControl::test_citizen_cannot_see_other_citizens_reports PASSED [ 35%]
tests/test_auth.py::TestAccessControl::test_citizen_id_from_token_used_for_reports PASSED [ 37%]
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_returns_profile PASSED [ 39%]
tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_without_token_returns_401 PASSED [ 41%]
tests/test_auth.py::TestIntegration::test_complete_citizen_workflow PASSED [ 43%]
tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id PASSED [ 45%]
tests/test_api_endpoints.py::TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports PASSED [ 47%]
tests/test_api_endpoints.py::TestCitizenReportDetails::test_citizen_fetch_report_details_with_timeline PASSED [ 49%]
tests/test_api_endpoints.py::TestOfficerReviewQueue::test_officer_query_review_queue_returns_paginated_list PASSED [ 50%]
tests/test_api_endpoints.py::TestOfficerCaseDetail::test_officer_view_case_detail_shows_evidence PASSED [ 52%]
tests/test_api_endpoints.py::TestOfficerApproval::test_officer_approve_report_awards_points PASSED [ 54%]
tests/test_api_endpoints.py::TestOfficerRejection::test_officer_reject_with_reason_stores_reason PASSED [ 56%]
tests/test_api_endpoints.py::TestOfficerClarificationRequest::test_officer_request_clarification_requeues_case PASSED [ 58%]
tests/test_api_endpoints.py::TestCitizenClarification::test_citizen_clarification_response_resubmits_case PASSED [ 60%]
tests/test_api_endpoints.py::TestOfficerQueueUpdate::test_officer_queue_reflects_requeued_cases PASSED [ 62%]
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_jpeg_returns_media_id_and_hash SKIPPED [ 64%]
tests/test_media.py::TestMediaUploadValidation::test_upload_valid_mp4_video_returns_media_id SKIPPED [ 66%]
tests/test_media.py::TestMediaUploadValidation::test_duplicate_file_returns_409_conflict SKIPPED [ 67%]
tests/test_media.py::TestMediaUploadValidation::test_file_too_large_returns_413_payload_too_large SKIPPED [ 69%]
tests/test_media.py::TestMediaUploadValidation::test_video_too_long_returns_413 SKIPPED [ 71%]
tests/test_media.py::TestMediaUploadValidation::test_unsupported_file_format_returns_422 SKIPPED [ 73%]
tests/test_media.py::TestMediaUploadValidation::test_corrupted_jpeg_returns_422 SKIPPED [ 75%]
tests/test_media.py::TestTechnicalScreening::test_low_resolution_image_flags_warning SKIPPED [ 77%]
tests/test_media.py::TestTechnicalScreening::test_high_blur_video_flags_warning SKIPPED [ 79%]
tests/test_media.py::TestMediaAccessControl::test_citizen_can_download_own_media SKIPPED [ 81%]
tests/test_media.py::TestMediaAccessControl::test_citizen_cannot_download_other_citizens_media SKIPPED [ 83%]
tests/test_media.py::TestMediaAccessControl::test_officer_can_download_any_media SKIPPED [ 84%]
tests/test_verification_harness.py::test_real_schema_and_effective_paths PASSED [ 86%]
tests/test_verification_harness.py::test_independent_lifespans_close_and_do_not_reuse_state PASSED [ 88%]
tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source PASSED [ 90%]
tests/test_identity.py::test_claim_validation_and_error_contract PASSED  [ 92%]
tests/test_identity.py::test_human_permission_boundary_without_business_handlers PASSED [ 94%]
tests/test_identity.py::test_fixed_service_client_audience_scope_matrix PASSED [ 96%]
tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache PASSED [ 98%]
tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers PASSED [100%]

============================== warnings summary ===============================
..\..\..\..\..\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ===========================
SKIPPED [1] tests\test_media.py:50: M3.2 implementation required
SKIPPED [1] tests\test_media.py:72: M3.2 implementation required
SKIPPED [1] tests\test_media.py:95: M3.2 implementation required
SKIPPED [1] tests\test_media.py:117: M3.2 implementation required
SKIPPED [1] tests\test_media.py:139: M3.2 implementation required
SKIPPED [1] tests\test_media.py:161: M3.2 implementation required
SKIPPED [1] tests\test_media.py:183: M3.2 implementation required
SKIPPED [1] tests\test_media.py:219: M3.2 implementation required
SKIPPED [1] tests\test_media.py:242: M3.2 implementation required
SKIPPED [1] tests\test_media.py:265: M3.2 implementation required
SKIPPED [1] tests\test_media.py:285: M3.2 implementation required
SKIPPED [1] tests\test_media.py:304: M3.2 implementation required
================= 41 passed, 12 skipped, 1 warning in 33.84s ==================

Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished

```
