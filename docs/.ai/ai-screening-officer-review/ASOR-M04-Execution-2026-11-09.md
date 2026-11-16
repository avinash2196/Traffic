# ASOR-M04 execution evidence — 2026-11-09

Executed only the approved Evidence Intake GREEN milestone by a fresh-context implementation-engineer role. Authority: [003 approved Implementation Plan](003_Implementation_Plan_Evidence_Intake_GREEN.md), user approval 2026-11-09, approved requirements/Plan/External Contract and completed M02/M03 evidence. M05 remains Pending. No test, dependency, configuration, provider, staging, commit or publication change.

## Exact implementation and data safeguards

Extracted both complete unified diffs from 003, checked each with `git apply --check --ignore-whitespace`, then applied each with `git apply --ignore-whitespace`. Created only intake.py from its complete approved block. Both reverse patch checks passed; all three files parsed. Only app.py/bootstrap.py changed and intake.py was added. M02/M03 dirty tests and documents retained their preimages.

Before source changes, expanded read-only `Get-CimInstance Win32_Process` found no Python/uvicorn process; `Get-NetTCPConnection -State Listen` found no 8000/8001 listener (8080 belonged to another process). Expanded `docker ps --no-trunc` returned an empty inventory. No task demo existed to stop; no unrelated service was stopped. Restricted CIM/Docker inspection was denied; expanded inspection succeeded. An attempted inspect of guessed traffic-demo returned no such container, and performed no mutation.

A new stable host-visible private directory retained 170 absolute full-path/length/SHA-256 preimages, original app.py/bootstrap.py, an SQLite backup and corresponding media tree. The backup used SQLite's backup API with a read-only source connection while no demo ran; both connections closed, backup integrity_check was ok. Private recovery data is retained outside the repository, uncommitted and undeleted; its location was provided privately to the coordinating role. No private path inventory, data values or hashes are published here. No backup or live data was used for verification.

Actual backup core:

```python
source = sqlite3.connect((root/'roadwatch.db').as_uri()+'?mode=ro', uri=True)
dest = sqlite3.connect(private/'roadwatch.db')
source.backup(dest)
assert dest.execute('pragma integrity_check').fetchone()[0] == 'ok'
dest.close(); source.close()
shutil.copytree(root/'media_store', private/'media_store')
```

The read-only WAL-mode backup created baseline-absent roadwatch.db-wal (0 bytes) and roadwatch.db-shm (32768 bytes). Independent comparison detected these rather than hiding them. After the runner completed its snapshot checks, no owned Python remained; exclusive FileShare.None read handles proved both files unheld, main DB length/hash matched its original preimage, and WAL was still empty. Removed only those two exact literal, positively attributed inert sidecars. No checkpoint, real migration or application startup occurred. Final comparison restored the complete protected path set: exactly app.py/bootstrap.py changed, intake.py alone added; all original tests/configuration/DB/media/.local lengths/hashes equal. Startup migration is implemented and verified below on synthetic legacy data. The real database remains byte-identical and has not been migrated; migration occurs on the next deliberate deployment/startup with the retained coherent backup. Applying code and safe verification do not constitute deployment.

## Actual verification commands and results

Used the exact current-host execution option in 003: its setup and run PowerShell blocks were mechanically extracted and executed, with literal owned area `C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10`. Setup copied root Python, pytest.ini, tests/templates/static only. No actual database/media/.local/.git/.venv was copied to verification scratch. Existing checkout venv was used unchanged. Decoder forwarding passed actual temporary media bytes to the existing FFmpeg carrier through stdin with --network none and --rm; production decoder arguments otherwise retained. No tool install, mocked decoder, fixture-specific acceptance or production Docker dependency.

Run command, with disposable repository as the tool working directory and expanded Windows socket capability:

```powershell
$taskRoot='C:\Users\avina\AppData\Local\Temp\asor-m04-execution-20261109-b4e82c10'
$env:PATH="$taskRoot\bin;"+$env:PATH
$env:TMP="$taskRoot\temporary"
$env:TEMP=$env:TMP
$env:TMPDIR=$env:TMP
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\repository\tests\verify_current_demo.py" --intake *> "$taskRoot\execution.log"
if ($LASTEXITCODE -ne 0) { throw 'Verification failed; preserve and inspect evidence' }
& 'C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe' "$taskRoot\check_integrity.py"
if ($LASTEXITCODE -ne 0) { throw 'Integrity mismatch; stop and preserve evidence' }
```

Unchanged launcher ran the six documented modules twice using `-m pytest -p pytest_asyncio.plugin -v`, retaining the inherited 180-second child wait, provider/bootstrap environment stripping and owned temporary state. No root pytest or real checkout lifespan. Actual command exit0:

```text
intake run 1 result: 0
============ 94 passed, 12 skipped, 1 warning in 108.05s (0:01:48) ============
intake run 2 result: 0
============ 94 passed, 12 skipped, 1 warning in 73.60s (0:01:13) =============
Protected checkout paths and SHA-256 values unchanged
Disposable repository and test state removed; child processes finished
Independent protected inventory unchanged
Independent verbose inventories equal:106 nodes;94 passed/12 existing skipped each
```

Independently parsed full verbose node/status lists match exactly, 106 each. Both real image/video and mixed attachments, actual byte boundaries, duplicate privacy, owned attachment/race, legacy containment and ZIP assertions passed unchanged. No assertion/skip/timeout was changed.

Synthetic migration command used the existing venv with PYTHONUTF8=1/PYTHONDONTWRITEBYTECODE=1, disposable area cwd and an owned temporary migration.py (outside frozen source). It extracted the original bootstrap schema from the retained source preimage, created a synthetic legacy database, populated every historical media column plus associated report/event rows, approved status/17 points/AI payload and synthetic file bytes, then opened twice through the new copied DatabaseConnection. Each open compared original columns/IDs/report/event rows and bytes, null additions, integrity and foreign keys:

```text
Synthetic legacy migration open 1 : all original columns/IDs/association/report status/points/events/AI and media bytes preserved; nullable additions null; integrity ok; foreign keys empty
Synthetic legacy migration open 2 : all original columns/IDs/association/report status/points/events/AI and media bytes preserved; nullable additions null; integrity ok; foreign keys empty
```

Invocation-only corrections: an initial orchestration call had a JavaScript syntax error before any command; setup extraction initially expected two PowerShell blocks but the document has three including cleanup, so extraction stopped before setup and was corrected. Inventory regex initially excluded parameter names containing spaces, failed its own count assertion and was corrected to capture whole node labels; the unchanged logs then yielded equal106-node lists. No verification/source/test was changed or rerun to conceal failures.

## Cleanup, preservation and limits

All owned server/test/decoder processes finished. Expanded owned Python inventory was empty, Docker ps empty. Exact documented cleanup checked resolved literal ownership, removed only the execution area (source-only copies, synthetic database/media, decoder forwarding tools and logs after private evidence retention), and independently confirmed absence. Private recovery backup/preimages remain intentionally retained. No global Temp cleanup, unknown process stopping, real media deletion or real DB checkpoint occurred.

```text
Independent 170-file preimage comparison: exactly app.py/bootstrap.py changed; intake.py alone added; all tests/configuration/real DB/media/private-local path/length/SHA preserved
Both exact approved reverse patch checks passed; three source files parse
Owned execution area absent: True
```

Native Windows PATH decoders remain an unmet deployment prerequisite; this proves real decoder semantics through the approved offline carrier, not a native decoder install or dependency-complete container build. Twelve old media skips supply no coverage; seven old API bodies remain setup-only; historical controls/OIDC infrastructure tests were not run. Existing Starlette/httpx warning retained. The inherited subprocess.wait bound is not an independent absolute watchdog. No live Gemini, durable jobs, officer-decision/recovery behavior, release acceptance or future milestone completion is claimed.

## Repeated node/status inventory

Both selections produced this identical inventory:

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
