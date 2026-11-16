# ASOR-M08D verification continuation — stopped 2026-11-11

M08D remains incomplete under011 User-Authorized Verification Revision. Shared transport7 passed. Whole intake exceeded its unchanged300-second bound; owned child tree was killed and reaped, with no XML/completed inventory. On user-authorized verification-setup continuation, exact106 collected unique nodes were partitioned into groups of15 (last1), each retaining300s and all assertions. Groups1–3 passed their45 outcomes; group4 stopped after11 passes and1 new assertion failure. Remaining intake groups and all42 OpenAI/common repeats were NOT RUN. No failing test was retried.

Failure: `test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4]` expected upload201 but observed400 `INVALID_MEDIA`, "Media cannot be decoded as declared". The cause is not established. Gemini-specific verification stays explicitly deferred; historical93 passes/1 failure are retained. No complete113/209/repeat42/repeat96 passing claim.

## Actual commands and results

Every child used the existing absolute virtual-environment Python with source-only native Temp repository cwd, expanded Windows loopback, UTF-8/no-bytecode, disabled plugin autoload, approved environment filter and isolated temporary state. Exact command arrays, full synthetic verbose logs and available JUnit inventories are retained in the adjacent JSON. `-vv --tb=long -x` replaced quiet output to retain full fail-fast tracebacks.

| Partition | Bound | Actual result |
| --- | ---: | --- |
| remaining-transport | 180s | 0; {'passed': 7}; 16.52s |
| remaining-intake | 300s | timeout; {}; 301.89s |
| intake-group-1 | 300s | 0; {'passed': 15}; 24.45s |
| intake-group-2 | 300s | 0; {'passed': 15}; 22.04s |
| intake-group-3 | 300s | 0; {'passed': 3, 'skipped': 12}; 15.63s |
| intake-group-4 | 300s | 1; {'passed': 11, 'failed': 1}; 31.52s |

## Exact executed commands

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-vv', '--tb=long', '-x', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\remaining-transport.xml', 'tests/test_provider_response.py', '-k', 'not (attempt_diagnostic_capture or unobserved_diagnostic)']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-vv', '--tb=long', '-x', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\remaining-intake.xml', 'tests/test_auth.py', 'tests/test_api_endpoints.py', 'tests/test_media.py', 'tests/test_verification_harness.py', 'tests/test_identity.py', 'tests/test_evidence_intake.py']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-vv', '--tb=long', '-x', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\intake-group-1.xml', 'tests/test_auth.py::TestSignup::test_signup_with_valid_data_returns_201', 'tests/test_auth.py::TestSignup::test_signup_with_duplicate_citizen_id_returns_409', 'tests/test_auth.py::TestSignup::test_signup_with_duplicate_email_returns_409', 'tests/test_auth.py::TestSignup::test_signup_with_invalid_email_returns_400', 'tests/test_auth.py::TestSignup::test_signup_with_missing_email_returns_400', 'tests/test_auth.py::TestSignup::test_signup_with_missing_password_returns_400', 'tests/test_auth.py::TestSignup::test_signup_with_short_password_returns_400', 'tests/test_auth.py::TestSignup::test_signup_password_is_hashed_not_plaintext', 'tests/test_auth.py::TestLogin::test_login_with_valid_credentials_returns_200', 'tests/test_auth.py::TestLogin::test_login_with_invalid_password_returns_401', 'tests/test_auth.py::TestLogin::test_login_with_nonexistent_citizen_returns_401', 'tests/test_auth.py::TestLogin::test_login_returns_session_token', 'tests/test_auth.py::TestLogin::test_login_updates_last_login_timestamp', 'tests/test_auth.py::TestLogout::test_logout_returns_204_no_content', 'tests/test_auth.py::TestLogout::test_logout_without_token_returns_401']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-vv', '--tb=long', '-x', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\intake-group-2.xml', 'tests/test_auth.py::TestAccessControl::test_accessing_reports_without_token_returns_401', 'tests/test_auth.py::TestAccessControl::test_accessing_reports_with_invalid_token_returns_401', 'tests/test_auth.py::TestAccessControl::test_citizen_can_see_own_reports', 'tests/test_auth.py::TestAccessControl::test_citizen_cannot_see_other_citizens_reports', 'tests/test_auth.py::TestAccessControl::test_citizen_id_from_token_used_for_reports', 'tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_returns_profile', 'tests/test_auth.py::TestGetCurrentCitizen::test_get_current_citizen_without_token_returns_401', 'tests/test_auth.py::TestIntegration::test_complete_citizen_workflow', 'tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id', 'tests/test_api_endpoints.py::TestCitizenReportHistory::test_citizen_fetch_history_returns_own_reports', 'tests/test_api_endpoints.py::TestCitizenReportDetails::test_citizen_fetch_report_details_with_timeline', 'tests/test_api_endpoints.py::TestOfficerReviewQueue::test_officer_query_review_queue_returns_paginated_list', 'tests/test_api_endpoints.py::TestOfficerCaseDetail::test_officer_view_case_detail_shows_evidence', 'tests/test_api_endpoints.py::TestOfficerApproval::test_officer_approve_report_awards_points', 'tests/test_api_endpoints.py::TestOfficerRejection::test_officer_reject_with_reason_stores_reason']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-vv', '--tb=long', '-x', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\intake-group-3.xml', 'tests/test_api_endpoints.py::TestOfficerClarificationRequest::test_officer_request_clarification_requeues_case', 'tests/test_api_endpoints.py::TestCitizenClarification::test_citizen_clarification_response_resubmits_case', 'tests/test_api_endpoints.py::TestOfficerQueueUpdate::test_officer_queue_reflects_requeued_cases', 'tests/test_media.py::TestMediaUploadValidation::test_upload_valid_jpeg_returns_media_id_and_hash', 'tests/test_media.py::TestMediaUploadValidation::test_upload_valid_mp4_video_returns_media_id', 'tests/test_media.py::TestMediaUploadValidation::test_duplicate_file_returns_409_conflict', 'tests/test_media.py::TestMediaUploadValidation::test_file_too_large_returns_413_payload_too_large', 'tests/test_media.py::TestMediaUploadValidation::test_video_too_long_returns_413', 'tests/test_media.py::TestMediaUploadValidation::test_unsupported_file_format_returns_422', 'tests/test_media.py::TestMediaUploadValidation::test_corrupted_jpeg_returns_422', 'tests/test_media.py::TestTechnicalScreening::test_low_resolution_image_flags_warning', 'tests/test_media.py::TestTechnicalScreening::test_high_blur_video_flags_warning', 'tests/test_media.py::TestMediaAccessControl::test_citizen_can_download_own_media', 'tests/test_media.py::TestMediaAccessControl::test_citizen_cannot_download_other_citizens_media', 'tests/test_media.py::TestMediaAccessControl::test_officer_can_download_any_media']
```

```text
['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-vv', '--tb=long', '-x', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08d-exec-20261111-70d6c2\\intake-group-4.xml', 'tests/test_verification_harness.py::test_real_schema_and_effective_paths', 'tests/test_verification_harness.py::test_independent_lifespans_close_and_do_not_reuse_state', 'tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source', 'tests/test_identity.py::test_claim_validation_and_error_contract', 'tests/test_identity.py::test_human_permission_boundary_without_business_handlers', 'tests/test_identity.py::test_fixed_service_client_audience_scope_matrix', 'tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache', 'tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers', 'tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpeg-a.jpg]', 'tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpg-a.jpg]', 'tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[png-image/png-a.png]', 'tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4]', 'tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mov-video/quicktime-a.mov]', 'tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[avi-video/x-msvideo-a.avi]', 'tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[long-video/mp4-a.mp4]']
```

## New failure traceback

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.7.0 -- C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\avina\AppData\Local\Temp\asor-m08d-exec-20261111-70d6c2\repository
configfile: pytest.ini
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 15 items

tests/test_verification_harness.py::test_real_schema_and_effective_paths PASSED [  6%]
tests/test_verification_harness.py::test_independent_lifespans_close_and_do_not_reuse_state PASSED [ 13%]
tests/test_identity.py::test_me_all_role_combinations_and_canonical_claim_source PASSED [ 20%]
tests/test_identity.py::test_claim_validation_and_error_contract PASSED  [ 26%]
tests/test_identity.py::test_human_permission_boundary_without_business_handlers PASSED [ 33%]
tests/test_identity.py::test_fixed_service_client_audience_scope_matrix PASSED [ 40%]
tests/test_identity.py::test_jwks_refresh_outage_and_bounded_cache PASSED [ 46%]
tests/test_identity.py::test_unknown_key_refresh_is_coalesced_and_recovers PASSED [ 53%]
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpeg-a.jpg] PASSED [ 60%]
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[jpeg-image/jpg-a.jpg] PASSED [ 66%]
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[png-image/png-a.png] PASSED [ 73%]
tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4] FAILED [ 80%]

================================== FAILURES ===================================
_ test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4] _

wire = (<httpx.Client object at 0x00000273BEAA0FC0>, <sqlite3.Connection object at 0x00000273BEA2FA60>, WindowsPath('C:/Users...-20261111-70d6c2/temporary/pytest-of-avina/pytest-4/test_real_formats_without_new_3/2dd037768b7d48b7bed0ed7b0c524d84'))
key = 'mp4', mime = 'video/mp4', name = 'a.mp4'

    @pytest.mark.parametrize("key,mime,name", [
        ("jpeg", "image/jpeg", "a.jpg"), ("jpeg", "image/jpg", "a.jpg"),
        ("png", "image/png", "a.png"), ("mp4", "video/mp4", "a.mp4"),
        ("mov", "video/quicktime", "a.mov"), ("avi", "video/x-msvideo", "a.avi"),
        ("long", "video/mp4", "a.mp4"),
    ])
    def test_real_formats_without_new_quality_or_duration_limits(wire, key, mime, name):
        client, _, _ = wire
        data = photo("PNG") if key == "png" else photo() if key == "jpeg" else VIDEOS[key]
>       handle = upload(client, data, name, mime)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

C:\Users\avina\AppData\Local\Temp\asor-m08d-exec-20261111-70d6c2\repository\tests\test_evidence_intake.py:118: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

client = <httpx.Client object at 0x00000273BEAA0FC0>
data = b'\x00\x00\x00\x1cftypisom\x00\x00\x02\x00isomiso2mp41\x00\x00\x00\x08free\x00\x00\x00\x1cmdat\x00\x00\x01\xb3\x00\x10...0\x00\x00\x00\x00\x00\x00\x00,ilst\x00\x00\x00$\xa9too\x00\x00\x00\x1cdata\x00\x00\x00\x01\x00\x00\x00\x00Lavf61.7.103'
name = 'a.mp4', mime = 'video/mp4', headers = None

    def upload(client, data=None, name="proof.jpg", mime="image/jpeg", headers=None):
        content = photo() if data is None else data
        response = client.post("/api/media/upload", headers=OWNER if headers is None else headers,
                               files={"media_file": (name, content, mime)})
>       assert response.status_code == 201, response.text
E       AssertionError: {"error":"Media cannot be decoded as declared","detail":"Media cannot be decoded as declared","code":"INVALID_MEDIA"}
E       assert 400 == 201
E        +  where 400 = <Response [400 Bad Request]>.status_code

C:\Users\avina\AppData\Local\Temp\asor-m08d-exec-20261111-70d6c2\repository\tests\test_evidence_intake.py:66: AssertionError
============================== warnings summary ===============================
..\..\..\..\..\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
- generated xml file: C:\Users\avina\AppData\Local\Temp\asor-m08d-exec-20261111-70d6c2\intake-group-4.xml -
=========================== short test summary info ===========================
FAILED tests/test_evidence_intake.py::test_real_formats_without_new_quality_or_duration_limits[mp4-video/mp4-a.mp4] - AssertionError: {"error":"Media cannot be decoded as declared","detail":"Media cannot be decoded as declared","code":"INVALID_MEDIA"}
assert 400 == 201
 +  where 400 = <Response [400 Bad Request]>.status_code
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!
================== 1 failed, 11 passed, 1 warning in 27.51s ===================

```

## Protection and cleanup

All172 explicit allowlisted source/document/config-example SHA-256 entries remained equal before evidence edits; all six approved source hashes match prior execution. All37 real database/media/private-local file size/mtime and directory mtime entries remained equal without opening private contents. Two directory sizes (.local and .local/private) report4096 under restricted shell and0 under expanded shell, with equal mtime; this reporting difference is disclosed rather than claimed byte protection. Metadata does not prove private byte identity. Root/test Python parsed without bytecode. No production/test/dependency/configuration change, key/private evidence/real database read, live call, staging or commit. Unrelated dirty work preserved.

Pinned decoder image sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de, network none, zero mounts, actual tool versions and Windows wrapper-path equality verified before each launcher. Exact011 stdin helper extracted unchanged. Direct docker tool versions avoided the source-operand wrapper restriction. Every started child returned or was killed/reaped; both owned carriers stopped and independently absent. Exact literal Temp ancestry and no links/junctions checked before removal; owned tree confirmed absent.

Deviations: initial shell-TEMP launcher path varied between calls; recreated at literal approved root before tests. Initial whole intake timeout retained. User then authorized fine bounded groups of the exact106 nodes with no deadline/assertion/source change; no unchanged whole-intake rerun. The later ordinary assertion failure stopped work immediately.

Gemini47, six provider diagnostics and retained explicit/legacy Gemini node were not rerun. No next milestone or live protocol prepared.
