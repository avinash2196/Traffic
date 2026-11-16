# ASOR-M08A checkpoint verification — 2026-11-10

**Verified.** The [approved checkpoint procedure](008_Implementation_Plan_Provider_Response_Correction_RED.md#active-verification-procedure--resume-from-the-revised-execution-checkpoint) carried forward two classified RED repetitions and the first Gemini pass from the [revised execution](ASOR-M08A-Revised-Execution-2026-11-10.md). Fresh verification completed Gemini repetition 2, both durable and intake repetitions, and both scratch soundness repetitions.

| Check | Verified outcome |
| --- | --- |
| Provider RED (archived) | Both pytest children exited 1 with the same nine intended ordinary failures and four passes. The launcher exited 0 after classifying two framing failures, six diagnostic failures and one reconstruction deadline failure. |
| Gemini preservation | Archived run 1 passed 47 checks in 67.98 seconds. Run 2 passed the same 47 in 71.16 seconds. Both classified all outcomes without skips or errors. |
| Durable preservation | Both children passed all 14 checks, with the same named outcomes as each other and the approved inventory. |
| Intake preservation | Both children passed 94 checks and skipped the same 12 existing cases, with 106 named outcomes matching the approved inventory. |
| Scratch soundness | Both children passed all 13 checks against the isolated probe, with named outcomes matching the approved inventory. |

All runs used the existing Traffic virtual-environment interpreter with explicit disposable working directories, owned temporary state, UTF-8 and bytecode disabled. The launchers removed provider and bootstrap settings from the child environments. The staged scripts verified the full 52-row archived input manifest, both decoder wrappers and matching provider test/classifier bytes across disposable copies. The local decoder image was available as `sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de`. The intake carrier used network mode `none` and zero mounts. No production code or tests changed in the checkout and no live provider request ran.

The initial local comparison of the Gemini output overlooked pytest progress columns. The first local intake comparison also omitted a parameterized node ID with a space. Normalizing the already captured output recovered the full inventories and matched the archived names in both cases. No test was rerun or changed to resolve either comparison. An initial setup command failed PowerShell parsing before it ran any extraction or test. Its corrected form extracted the approved blocks and passed preflight. The earlier missing decoder and historical timeouts remain documented in the prior execution reports.

## Commands

The following commands used `C:\Users\avina\Downloads\avinash-repo\v11\Traffic\.venv\Scripts\python.exe`. Paths below are relative to the approved outer scratch directory unless marked as checkout.

```text
checkout> python <scratch>\setup.py
repository> python <scratch>\probe.py
repository> python <scratch>\prepare_intake_resume.py
repository> python <scratch>\checkpoint.py <checkout>\docs\.ai\ai-screening-officer-review\ASOR-M08A-Revised-Execution-2026-11-10.md
repository> python tests\verify_gemini_assessment_checkpoint.py --green
repository> python tests\verify_durable_processing_checkpoint.py --green
repository> python <scratch>\run_intake_resume.py
probe-repository> python tests\verify_provider_response_resume.py --green
scratch> python check.py
```

The intake launcher ran the following child command twice in its own nested source-only copy. It logged the exit and complete verbose outcome inventory for each run.

```text
python -m pytest -p pytest_asyncio.plugin -v tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py tests/test_evidence_intake.py
```

## Classified results

### Reused provider RED repetitions 1 and 2

The same 13 named outcomes occurred in both archived repetitions. The first child took 75.05 seconds and the second 65.95 seconds. Both child commands and classification logs are in the [revised execution](ASOR-M08A-Revised-Execution-2026-11-10.md#revised-red).

```
text
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

### Gemini repetition 2

```text
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m07-3onnf6ng\\green-2.xml', 'tests/test_gemini_assessment.py']
green run 2 exit 0
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
================== 47 passed, 1 warning in 71.16s (0:01:11) ===================
Classified 47 green nodes; no errors/skips
Protected source/state unchanged; compare checkpoint inventory with archived run 1
Owned disposable tree removed; children reaped
```

### Durable preservation

```text
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m05-lej2v2ee\\green-1.xml', 'tests/test_durable_processing.py']
green run 1 exit 0
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
======================= 14 passed, 1 warning in 21.58s ========================
Classified 14 green nodes; no errors/skips
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m05-lej2v2ee\\green-2.xml', 'tests/test_durable_processing.py']
green run 2 exit 0
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
======================= 14 passed, 1 warning in 20.39s ========================
Classified 14 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
```

### Intake carrier

```text
Carrier: ['docker', 'run', '-d', '--rm', '--network', 'none', '--pull', 'never', '--name', 'asor-m08a-intake-8c13f901', '--entrypoint', '/bin/sleep', 'traffic-60e6e567315a-runner:latest', '720']
Owned decoder carrier: network none; mounts 0
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', 'tests/verify_current_demo_resume.py', '--intake'] cwd= C:\Users\avina\AppData\Local\Temp\asor-m08a-verify-20261110-8c13f901\repository
Intake verification copy exit 0
Owned decoder carrier stopped and absent
```

### Intake preservation

```text
intake run 1 result: 0
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
============ 94 passed, 12 skipped, 1 warning in 61.26s (0:01:01) =============
intake run 2 result: 0
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
============ 94 passed, 12 skipped, 1 warning in 61.59s (0:01:01) =============
Protected checkout paths and SHA-256 values unchanged
```

### Scratch soundness

```text
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m08a-s0x51f09\\green-1.xml', 'tests/test_provider_response.py']
green run 1 exit 0
tests/test_provider_response.py::test_real_child_response_framing[plain] PASSED
tests/test_provider_response.py::test_real_child_response_framing[gzip] PASSED
tests/test_provider_response.py::test_real_child_response_framing[chunked] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-start-400-PROVIDER_REQUEST_REJECTED-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-finalize-403-PROVIDER_CONFIGURATION-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[file-poll-429-PROVIDER_TRANSIENT-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-reset-PROVIDER_TRANSIENT-NETWORK_ERROR] PASSED
tests/test_provider_response.py::test_unobserved_diagnostic_stays_unknown PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[serialize] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[startup] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[reconstruct] PASSED
tests/test_provider_response.py::test_real_timeout_kills_and_reaps_before_return PASSED
======================= 13 passed, 1 warning in 40.10s ========================
Classified 13 green nodes; no errors/skips
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m08a-s0x51f09\\green-2.xml', 'tests/test_provider_response.py']
green run 2 exit 0
tests/test_provider_response.py::test_real_child_response_framing[plain] PASSED
tests/test_provider_response.py::test_real_child_response_framing[gzip] PASSED
tests/test_provider_response.py::test_real_child_response_framing[chunked] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-start-400-PROVIDER_REQUEST_REJECTED-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[upload-finalize-403-PROVIDER_CONFIGURATION-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[file-poll-429-PROVIDER_TRANSIENT-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-503-PROVIDER_TRANSIENT-HTTP_STATUS] PASSED
tests/test_provider_response.py::test_attempt_diagnostic_capture[generate-reset-PROVIDER_TRANSIENT-NETWORK_ERROR] PASSED
tests/test_provider_response.py::test_unobserved_diagnostic_stays_unknown PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[serialize] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[startup] PASSED
tests/test_provider_response.py::test_absolute_deadline_covers_parent_work[reconstruct] PASSED
tests/test_provider_response.py::test_real_timeout_kills_and_reaps_before_return PASSED
======================= 13 passed, 1 warning in 40.37s ========================
Classified 13 green nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
```

## Source integrity and cleanup

The archived integrity script confirmed that all 194 protected checkout entries matched their original absolute paths, lengths and SHA-256 hashes. It also verified the preserved original source, configuration, tests and launchers, and parsed and matched the provider test and classifier across the disposable copies. Independent before/after inventories matched all 95 frozen disposable source files. The original checkout inventory includes private metadata that is excluded from this report.

Independent checks found zero owned processes, an empty owned launcher temporary directory and no named intake carrier. The literal outer root resolved directly beneath the intended Temp directory and contained no reparse points.

## Checkpoint input manifest

All 52 archived rows below were verified against their staged bytes, including the disposable helpers. Entries contain SHA-256, byte length and source path.

```
text
71ed72a9abcd447edf32e37f50c937b20a1cd2beb40c6b850fa7ddea01e5e1f9  53619  app.py
79e583a03504be0dc52a966ac3e6cbba5a1efe5ab8616fa07c9a2f56c604f608  4473  auth_utils.py
7f4a91f6b7a7cb9e2cb3f5dd5634f25776b8733569373c16186fa0a7cac04a31  24450  bootstrap.py
d0a8cb6d8d03bf71e9e2753617a0f1a2ee3e663ac269c1d86bb6377d3ceda946  10979  controls_http.py
14640b90226e41cbbfc25ecc68a6d36bf111f3c71144b68ec24f9f59659d0ba1  9349  controls_operator.py
af6fbaf6e6dd67e32b7095d9ec8ac12e28009759a8559ec8f3f5a2bb58187f16  17865  durable.py
502b6cfd01c4a414e1eb0ea5670fd81f7c3a25ba75e141b827848ada4360de22  21816  gemini.py
dcff0c3168d6d786857391d03c704f2068b844fba36a5e09cc12d116af3d1a74  5599  intake.py
2a437be18c7b25a10d6e96864fd97fe662be63c8dcf1c35eafe3f4b9296f285d  11249  media.py
c5a2e33860eec755c2a320eb36c4129a83569de196f448d8a446dc22f758c112  336  pytest.ini
cd5d6890b2345fb74b71f0a92608632060120320d1000e741e66772a26216235  29680  runtime_controls.py
fe5885517354ed5dd25887070d818a2a44faed1aac6fee28c4771073686984b4  1286  static/css/base.css
dc585897a111a1a364d777e4a7ddc5a52f9da256d5491fc268a198912dbbaa78  4337  static/css/components.css
e0367ec5e151769e46a46cc09b3e907edbc0915095d66d81ae92481c9c6cb475  2252  static/css/layout.css
7847b965b18ab71256e283f751c1a5ebb14de315f8f255ebdf5a785873c9be4c  3284  static/css/responsive.css
28a025e6f92e0c0956f9b476c9aa0d7ee6e7ee64d941ec9760ec32af3ce25ce6  3761  static/js/api.js
bdb14f52cd028ff343700f0f5f4897bb7eaf48ab814757131e5b71622f37ca0e  1874  static/js/auth.js
49da203258429206a1e7783ded2621c231b0f5b05166e9942d1195db43148613  3722  static/js/common.js
33a652b106fcbea84345682fb6ddac6c52ba4ff01d9c8bb6e07707dd17554539  3193  static/js/utils.js
9f42fa889b58de3bfc7f2305cea77ae4966d5ac2c44d5460bddf47e60941d0e8  3933  templates/citizen-dashboard.html
4c78c8247936c554c723da5c01c8218c88792f14e79d3cf0212fdba83edc33a7  2849  templates/citizen-login.html
f2894968f166dcef59129f4ddcb9746a91e15fb99dbca6ec3b51976084321482  4886  templates/citizen-report-detail.html
8b35a5066d0eecab9c463542bf3c4faea9b1909bf1f072aee903eb714f022fec  7820  templates/citizen-report.html
ccef26379459ca92d6b17efba5eea6a2d8f39dfa03e5463ebe7d66e9a502e876  3345  templates/citizen-reports.html
62a130dc36a58bb32ea9f9146fc0ace0600733650e019b8dfa1caa37555cd3a4  3961  templates/citizen-signup.html
47db566de467bcaca75a44439f63b216bf8697bd3f135476983e602f2fc7291f  7207  templates/officer-detail.html
a4a12d4f17758eb7cff88ceb72aa2d5a8b9e550606575e7d90d458aa90724866  4192  templates/officer-login.html
2617d0f84da3ef3d39189ef9c99f1746224d8569efe1bb69dc6ef1e8764aafc5  3703  templates/officer-queue.html
1b3a8e6f95cc49910eef128f4d49b0a7bb91b4d37e567b105ae522f3466b2548  5940  templates/officer-signup.html
7b13fd4d3f905c3dfce4bcb4e737fd4ffdccdadae939a9644033ccad955950ce  4618  tests/conftest.py
e456805e78b63ec5fa0b1b681414750e0ef4280d65b832e0e9828a8a4ac908b7  18809  tests/test_api_endpoints.py
430012cd766919ee739c24f253abab53ff60742b9c773315dc0ca1427f93f2a7  17951  tests/test_auth.py
d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20  63046  tests/test_controls.py
09e4a9ac403d090e8f3aadd0a62b6326e078254c27891a6e03145781af2a0210  16000  tests/test_durable_processing.py
f668a5be2301b3ffeb0a5c6d162288e9f7aa85a546b7339e5b37ef5ff51dfa34  35513  tests/test_evidence_intake.py
7eca28f4e834514ee387815045b67725cff64d8b8f3992649c2779d33bd20b73  21437  tests/test_gemini_assessment.py
7b22df16cd0c2ca7a7dbebc3e28e2762cf508549f3c212f185a63b683c8a7557  13023  tests/test_identity.py
f9ca6c38d81a9c2bfe6cf374bdfb6cfd0fbc6e2953f3871b0df7d2979fa3bf63  9407  tests/test_identity_oidc.py
667d98ed53c40d0deb7a0663e989268c310a2b746b27017e8bf44260d455dcc5  13126  tests/test_media.py
f614ff22f868dc6853f7b4320d00a5fe379845c9f241135d1287c1554ffbd9f4  13746  tests/test_provider_response.py
e7f09bc4e5498b6302e10f75aebda885a807631cd5975d2d25c9c1fd459086c7  1721  tests/test_verification_harness.py
76fa52c4f46076aa706614930c13f4e1559ad6516e67b07fc5ce660e7afbc038  6526  tests/verify_current_demo.py
8b81890ac1c0bfca6f1e2564583a649d3a3f95e3f2adbc1e4c428cda31e0bb57  5829  tests/verify_durable_processing.py
9dc535df5fc4f781f1d4a588ceeb1bdc16cafd9d59b39ef0e14fdac81b4bb721  5811  tests/verify_gemini_assessment.py
285278df42c8d7696f329acc00464dedec70751d58d4cc1ca9e35eeed6dea9a3  6231  tests/verify_provider_response.py
c8e9a66e8ec78d2a138784cb45094aa0727a9f1684569e00f6363485435b6675  6232  tests/verify_provider_response_resume.py [disposable]
1abce19ac968d2bdfcb65b3a42b9439e10a273fa57f4b425ce9babe2e49513d8  6526  tests/verify_current_demo_resume.py [disposable]
c59f927dd2991f44173e6bff34a7dd53a37cfb33298819c31736207a4d1a08ce  485  decoder.py [disposable]
5052247f8ccde571d1707a188c07e409a311d18da4205c331840d97823888b5c  630  decoder_carrier.py [disposable]
e9599d2ce7fe4d430a63e48cc98b2aaa82dbbf61e92a823d5cb28fe027835aa5  1882  run_intake_carrier.py [disposable]
940dbf88f459120ff7b6191d461714c81dbc4761ad502b1ad08b7c038fb8e487  4491  probe.py [disposable]
13a4b7c5b6a7428fc4ee3ab5b7cdd5226b1ea90e1e85309def9e227c479bc15d  1655  prepare_intake_resume.py [disposable]
196dcf1dde5b5c324a7b448757be918c5d1f20c757fb2a61c3ebad1d07ac4598  5832  tests/verify_gemini_assessment_checkpoint.py [derived]
b3b0a43c6712fb83df8d69e787af086250533f494edfdf3cea13e90edf5c0182  5830  tests/verify_durable_processing_checkpoint.py [derived]
```

## Final cleanup

The literal owned scratch root was removed after archiving, and a separate existence check confirmed it was absent.
