# ASOR-M08C execution — 2026-11-10

Approved010 scope: exact two new test/helper files and two existing-test diffs only. No production, dependency or configuration changes; no live provider calls, key/private media/backup content reads, staging, commit or publication. M08D and live acceptance remain Pending.

## Actual commands and results

Native source-only root `C:\Users\avina\AppData\Local\Temp\asor-m08c-exec-20261110-7b92d1`; existing absolute .venv interpreter. Expanded native Windows loopback, UTF-8/no bytecode, disabled plugin autoload, stripped provider/bootstrap environment, isolated TMP/TEMP/TMPDIR and owned decoder wrappers were used. No checkout app/real database startup.

- `['docker', 'run', '-d', '--rm', '--network', 'none', '--pull', 'never', '--name', 'asor-m08c-exec-7b92d1', '--entrypoint', '/bin/sleep', 'sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de', '660']`.
- `['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', 'tests/verify_gateway_openai.py', '--red']` — cwd `C:\Users\avina\AppData\Local\Temp\asor-m08c-exec-20261110-7b92d1\repository`; outer limit 390s.
- `['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08c-exec-20261110-7b92d1\\preserved.xml', 'tests/test_provider_response.py::test_unobserved_diagnostic_stays_unknown']` — cwd `C:\Users\avina\AppData\Local\Temp\asor-m08c-exec-20261110-7b92d1\repository`; outer limit 180s.

Exact helper-emitted child commands:

```text
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08c-exec-20261110-7b92d1\\temporary\\asor-m08c-check-xk0yqm9b\\red-1.xml', 'tests/test_gateway_openai.py'] cwd= C:\Users\avina\AppData\Local\Temp\asor-m08c-exec-20261110-7b92d1\temporary\asor-m08c-check-xk0yqm9b\repository limit=180s
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-q', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08c-exec-20261110-7b92d1\\temporary\\asor-m08c-check-xk0yqm9b\\red-2.xml', 'tests/test_gateway_openai.py'] cwd= C:\Users\avina\AppData\Local\Temp\asor-m08c-exec-20261110-7b92d1\temporary\asor-m08c-check-xk0yqm9b\repository limit=180s
```

Exact helper exit0. Both internal children: 180-second bound, ordinary pytest exit1, exactly29 intended missing-selection assertion failures, zero errors/skips/unexpected passes. No cleaning between persistent/configuration repeats; named inventories equal. All failures reached `AssertionError: GATEWAY_SELECTION_NOT_SNAPSHOTTED` after an accepted owned-photo/report, rather than import/setup failure. All later assertions remain intact for GREEN.

```text
29 failed, 1 warning in 23.70s
29 failed, 1 warning in 23.91s
Repeated named outcomes: 29
Source hashes unchanged; owned copy/state removed; test children reaped
1 passed, 1 warning in 4.02s
```

Preserved XML: exactly `tests.test_provider_response::test_unobserved_diagnostic_stays_unknown`, passed. Existing Starlette/HTTPX deprecation warning only. No broad168-pass rerun or production probe repeated. Historical M08B13 provider/47 Gemini/14 durable/94 intake passes+12 existing skips remain checkpoint evidence, not OpenAI/live evidence. All retained scenario assertions remain unchanged.

## Named inventories

Both RED runs contained each following node, failed at the ordinary missing-selection assertion:

- `test_errors_retry_restart_no_fallback[401-PROVIDER_CONFIGURATION-False]` — failed twice.
- `test_errors_retry_restart_no_fallback[402-PROVIDER_REQUEST_REJECTED-False]` — failed twice.
- `test_errors_retry_restart_no_fallback[429-PROVIDER_TRANSIENT-True]` — failed twice.
- `test_invalid_selected_configuration[AI_PROVIDER-]` — failed twice.
- `test_invalid_selected_configuration[AI_PROVIDER-unknown]` — failed twice.
- `test_invalid_selected_configuration[OPENAI_API_KEY-]` — failed twice.
- `test_invalid_selected_configuration[OPENAI_MODEL-latest]` — failed twice.
- `test_output_normalization[authority-INVALID_MODEL_OUTPUT]` — failed twice.
- `test_output_normalization[duplicate-INVALID_MODEL_OUTPUT]` — failed twice.
- `test_output_normalization[incomplete-MODEL_OUTPUT_UNAVAILABLE]` — failed twice.
- `test_output_normalization[malformed-INVALID_MODEL_OUTPUT]` — failed twice.
- `test_output_normalization[refusal-MODEL_OUTPUT_UNAVAILABLE]` — failed twice.
- `test_owned_evidence_preflight` — failed twice.
- `test_registered_adapter_shared_worker` — failed twice.
- `test_request_and_common_policy` — failed twice.
- `test_retained_explicit_and_legacy_gemini` — failed twice.
- `test_sampled_video_coverage_and_human_referral[complete]` — failed twice.
- `test_sampled_video_coverage_and_human_referral[coverage]` — failed twice.
- `test_sampled_video_coverage_and_human_referral[deadline]` — failed twice.
- `test_sampled_video_coverage_and_human_referral[decode-error]` — failed twice.
- `test_sampled_video_coverage_and_human_referral[invented-time]` — failed twice.
- `test_sampled_video_coverage_and_human_referral[screenout]` — failed twice.
- `test_snapshot_fail_closed[ambiguous-legacy-None]` — failed twice.
- `test_snapshot_fail_closed[media_profile_version-unknown]` — failed twice.
- `test_snapshot_fail_closed[missing-None]` — failed twice.
- `test_snapshot_fail_closed[model-latest]` — failed twice.
- `test_snapshot_fail_closed[provider-unknown]` — failed twice.
- `test_snapshot_fail_closed[request_profile_version-unknown]` — failed twice.
- `test_usage_attribution_and_unknowns` — failed twice.

## Protection and deviations

New test/helper hashes match010: `5fb0f9e164842a2afaea5744aaf9da02de13bce31204bedb329bb2ccb3b4258b` / `6a64e4a3311e2f5c626100e24c425f17fb03cc2e84f7f9a3bd8e557392e132c0`. Existing-test after hashes match010: `cac4245095c4d72d25c0b719f7e16d5ee0780b62ab4a9db7789359cb40287aa0` / `198f3b2e41489a6b7480fc4e21e21c2a299ea9563b5bb9f85778381e99a29cc8`. These after hashes are CRLF despite010's 'normalized' label. Initial LF outputs failed the guard before testing and were corrected to approved CRLF bytes. Original before hashes are LF; inverse exact edits with LF normalization reproduced and verified `7eca28f4e834514ee387815045b67725cff64d8b8f3992649c2779d33bd20b73` / `f614ff22f868dc6853f7b4320d00a5fe379845c9f241135d1287c1554ffbd9f4`.

The initial per-call restricted Temp capture became inaccessible to subsequent calls. A stable native Temp allowlist/metadata baseline was captured after exact test application and before verification; original test preimages were reconstructed and hash-verified. No full preapplication manifest comparison is claimed. All163 allowlisted source/document hashes and40 other-file metadata records matched across verification and final pre-cleanup recheck. Private metadata equality does not prove private byte identity.

Routine setup corrections before any test: original-preimage LF normalization; Windows wrapper comparison using resolved Path equality because shutil.which returned uppercase `.CMD`. The preflight attempt carrier was stopped/absent. Final successful preflight verified pinned image `sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de`, network none, zero mounts, both actual tools and wrappers. Exact archived decoder_carrier.py hash: `5052247f8ccde571d1707a188c07e409a311d18da4205c331840d97823888b5c`. Its source inputs are constrained beneath owned temporary state. RED gates stopped before video extraction/inference.

After successful tests, an immediate docker-ps absence assertion raced asynchronous `--rm` removal following successful docker stop. Subsequent independent checks confirmed the owned carrier absent. No test rerun, limit change or assertion waiver occurred. Archive log parsing removed pytest's appended/truncated failure-message suffix to compare names; helper XML classification itself had already passed unchanged.

## Cleanup

All owned test/HTTP/transport children returned and were reaped; helper nested roots removed. Decoder stopped/absent. Outer literal root was checked as a direct native Temp child with no symlink/junction and removed/confirmed absent before this archive and status update. No unrelated paths/processes removed.

## Allowlisted content protection

163 path/size/SHA-256 records. Snapshot JSON SHA-256 `c9ca1463440fa09d14e25bedc610fb217ee558bf522a4df17ae7cdb9a2039b63`.

| Path | Bytes | SHA-256 |
| --- | --- | --- |
| `.env.example` | 7562 | `a0d897149c29d6ebcd813f5033758cbbaa708b824f260671a6e89b95c704bcf1` |
| `app.py` | 53619 | `71ed72a9abcd447edf32e37f50c937b20a1cd2beb40c6b850fa7ddea01e5e1f9` |
| `auth_utils.py` | 4473 | `79e583a03504be0dc52a966ac3e6cbba5a1efe5ab8616fa07c9a2f56c604f608` |
| `bootstrap.py` | 24450 | `7f4a91f6b7a7cb9e2cb3f5dd5634f25776b8733569373c16186fa0a7cac04a31` |
| `controls_http.py` | 10979 | `d0a8cb6d8d03bf71e9e2753617a0f1a2ee3e663ac269c1d86bb6377d3ceda946` |
| `controls_operator.py` | 9349 | `14640b90226e41cbbfc25ecc68a6d36bf111f3c71144b68ec24f9f59659d0ba1` |
| `docs\.ai\ai-screening-officer-review\001_Implementation_Plan_Safe_Verification_Harness_OTHER.md` | 52406 | `0159f175471104b634b54f3486e04a52d115a7131fe8feaf4a92c6b7429fa232` |
| `docs\.ai\ai-screening-officer-review\002_Implementation_Plan_Evidence_Intake_RED.md` | 111013 | `e387b06a44c4195ae7cd84112fd6d5b6fe6c75c008d23f1acac587b2b8deeba6` |
| `docs\.ai\ai-screening-officer-review\003_Implementation_Plan_Evidence_Intake_GREEN.md` | 63370 | `6328297563c90ace7a338f8e779eb707b935aa565e3ddab76cd1bdf9d7556de7` |
| `docs\.ai\ai-screening-officer-review\004_Implementation_Plan_Durable_Processing_RED.md` | 54318 | `74a635c9a2c2a057c5f03cbbc2889a2d70b36f5f167d9d3714713f9b670dd974` |
| `docs\.ai\ai-screening-officer-review\005_Implementation_Plan_Durable_Processing_GREEN.md` | 45740 | `cc7aa437987381f3dfc85ef6371ef317b38f13cac7cd1cdaadb59d9de7f0e780` |
| `docs\.ai\ai-screening-officer-review\006_Implementation_Plan_Gemini_Assessment_RED.md` | 74198 | `db50a927a94618cc22561ab011e2fc12a28d034c2cb0b1124d7a18eca91afed8` |
| `docs\.ai\ai-screening-officer-review\007_Implementation_Plan_Gemini_Assessment_GREEN.md` | 95333 | `69c6b8a51b95502ba4a1ddea3303219d8be88a66846c8cf7e788b25c3ddd3a05` |
| `docs\.ai\ai-screening-officer-review\008_Implementation_Plan_Provider_Response_Correction_RED.md` | 117887 | `c84abacecdb4cc4a5dd6a95a5abc99e5b017929eb751d1d5462aab8b274aa236` |
| `docs\.ai\ai-screening-officer-review\009_Implementation_Plan_Provider_Response_Correction_GREEN.md` | 28817 | `31434f3e2e4c142b86e7ee8a471620c8d10cb6735f12d21bca2a60a3748b32c2` |
| `docs\.ai\ai-screening-officer-review\010_Implementation_Plan_Gateway_OpenAI_RED.md` | 65387 | `355eb91083f71acd877c09518e1277b63ad8eb2b969c053a26863df843ac8e55` |
| `docs\.ai\ai-screening-officer-review\ASOR-M02-Execution-2026-11-09.md` | 19454 | `321bfeb1fdbbbba01e6f4c434ab621a2847badd0a05dc1e6a91853452563f401` |
| `docs\.ai\ai-screening-officer-review\ASOR-M03-Execution-2026-11-09.md` | 21330 | `d5d522f9560414c50caffea031eabe8f78f50420ceff5cb4d621b4de2f6dac4d` |
| `docs\.ai\ai-screening-officer-review\ASOR-M04-Execution-2026-11-09.md` | 19543 | `1ad9e4d0891e7d31657b156991b7613ced4fe5362e1f312c202c2f512ad73edd` |
| `docs\.ai\ai-screening-officer-review\ASOR-M05-Execution-2026-11-09.md` | 18978 | `e95827d8088291efb7d7f33c3947615ebcb4ec22ff9deb68e00dce04bdda60d1` |
| `docs\.ai\ai-screening-officer-review\ASOR-M06-Execution-2026-11-09.md` | 24614 | `7d9ae6d6be6e3da893f945eccf4444a2c530365a897dd7fed94ae439c95685a3` |
| `docs\.ai\ai-screening-officer-review\ASOR-M07-Execution-2026-11-09.md` | 27972 | `64ee861a04bc4a8dd4a16d09d7b5aaa349010e6898cfb2eca1719b8aef8c6821` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08-Execution-2026-11-09.md` | 36075 | `6e57972c8bb24fb821ccf9f8da5b71a32d9e3e72492a6e1ae59352177fd98dda` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08-Live-Diagnosis-2026-11-09.md` | 3412 | `a57114721d3c523a9571447c16a63c65235aca5e7f750f6d80f3dd724e6063b2` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08-Live-Image-Rerun-2026-11-10.md` | 2888 | `230e750351bae9c2a6459278bbe595ba80a068fa2dda62f977c6f6951679e7f7` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08A-Checkpoint-Execution-2026-11-10.md` | 47781 | `da1ebfa4533902814b729e34176a9c625477f9eb670106a5e71c7ebfa5e82a6e` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08A-Execution-2026-11-10.md` | 39076 | `db1fb3eaa050b3fa8e9a7b672080be84e92de084dfc7eadffe8448af0e4ecbb1` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08A-Resume-Execution-2026-11-10.md` | 5033 | `bd7fb5e1a2ce3fe5f1a6a4c20ac1584e74d4779d9e07d0e16e79edb942f61866` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08A-Revised-Execution-2026-11-10.md` | 17687 | `de66c36dba51eb934e13c95dcbe505f77cce3a7eedb6f031ae89b965928d3ffc` |
| `docs\.ai\ai-screening-officer-review\ASOR-M08B-Execution-2026-11-10.md` | 5015 | `4b1b77281a357aa23f5e252e355aab03e086fd8041c5634d96bbebd3dcc05265` |
| `docs\.ai\ai-screening-officer-review\External-Contract.md` | 85046 | `080449ab8e0532797077f204b8c0768bcec25418f845d742af8f2f41d7929ead` |
| `docs\.ai\ai-screening-officer-review\Live-Verification-Setup.md` | 4817 | `2abfcc83c6f44859c1221cb4304fd74135ea042fdb36c390c577712f4abd24bb` |
| `docs\.ai\ai-screening-officer-review\Plan.md` | 71456 | `c84a5a5af385acc83619a46fdc4c598e82721d5acce09f887c358f806a737d9d` |
| `docs\.ai\ai-screening-officer-review\requirements.md` | 20943 | `ba028cab663b63b048b52f38251dcbd721b5bfb9e7b9f336835ff1b5c1f86632` |
| `docs\.ai\initial-build\001_Implementation_Plan_Foundation.md` | 45605 | `a73d109291ec62b3728fc6e692ee1f484cbed95cc032c05aa588ff40554ba65f` |
| `docs\.ai\initial-build\002_Implementation_Plan_Foundation_TLS_Repair.md` | 21988 | `a65363e9e54405f0bd237d7569bfee28a531a35f6ceaa31b608af804d71a8429` |
| `docs\.ai\initial-build\003_Implementation_Plan_Foundation_Browser_Routing_Repair.md` | 24497 | `dd24e34b07e59055b253902917066ab4fb43c2f48ef6b57933382094da06ea0b` |
| `docs\.ai\initial-build\004_Implementation_Plan_Identity_RED.md` | 48934 | `ea0c854237da365edbf22486bd97c9575aea7e7fc2fab8f156b775a6e1a78631` |
| `docs\.ai\initial-build\005_Implementation_Plan_Identity_GREEN.md` | 58636 | `a170bf012f80e3c8c39e46ab45d747c1b13c9083ca38e2d7c12564e4f08d15ea` |
| `docs\.ai\initial-build\006_Implementation_Plan_Runtime_Controls_RED.md` | 90177 | `620706a44285c1e4e01b6be6abd10404e48e1f38bf31362fcf27c55645502245` |
| `docs\.ai\initial-build\007_Implementation_Plan_Runtime_Controls_GREEN.md` | 78633 | `c5f84e4ef99e0024d971a545a3698815d71cc637518998a523d0ea60fb826951` |
| `docs\.ai\initial-build\008_Implementation_Plan_Evidence_Intake_Screening_RED.md` | 47337 | `fc1b301bc9f42ca623a005f59f39e428eebb3197ba5519cc7a1149fcd2bf053d` |
| `docs\.ai\initial-build\009_Implementation_Plan_Evidence_Intake_Screening_GREEN.md` | 79057 | `5d081a0c8faf6de0a8880158cb232cee0e1784145ed92e8e486b765fd83848f3` |
| `docs\.ai\initial-build\API-Contract.md` | 52874 | `cc8747113f3e0f8a0edf0546a6553f9c417d6dc8afedf2a0c3f557eb7d50e3cb` |
| `docs\.ai\initial-build\Architecture-Proposal.md` | 24743 | `7a62fa1fe414618c2902b2a2297448296cef685041c3580c5090d35798d3ce14` |
| `docs\.ai\initial-build\Controls-Contract-Clarifications.md` | 10686 | `33e11ec43106e912ed85dae2daa92dbf78a4bdf4e97cdf8cfa8093c5e7f17065` |
| `docs\.ai\initial-build\Controls-GREEN-Planning-Dry-Run-2026-10-31.md` | 49229 | `14e6d648c9e1894bc65a67fcee00a9598314c82579e11df13db909792ca1e11f` |
| `docs\.ai\initial-build\Controls-RED-Planning-Dry-Run-2026-10-31.md` | 70121 | `fbdccfc0d81c0c83d9dc3477f7740589929c4fec943e4d77850c6428613823ba` |
| `docs\.ai\initial-build\Controls-Service-Audit-Actor-Clarification.md` | 2380 | `def0739a5dc5ed47bde9718dd7c867b45456c443007cfed14ad5613f7f5a12af` |
| `docs\.ai\initial-build\DP-M02-Browser-Execution-2026-10-26.md` | 78283 | `63fd3bdbdd7c45a4da6b6da87f9d0df555a1497d479fda62f806bc00ad9051d5` |
| `docs\.ai\initial-build\DP-M02-Evidence.md` | 15888 | `6831a66c478059ca5320c7414aac2f53328d94e46c13c95967e9601a755bf2a1` |
| `docs\.ai\initial-build\DP-M02-TLS-Execution-2026-10-26.md` | 62684 | `9b89f469e49041098c39e09e4e5537b05d081d4796ef90c5b2465deae8f51076` |
| `docs\.ai\initial-build\DP-M03-Execution-2026-10-30.md` | 11772 | `3528fd3981808610204c242a8cd2802f22563eee5f405de1a00b80ca37efb198` |
| `docs\.ai\initial-build\DP-M04-Execution-2026-10-30.md` | 18626 | `30ead596054f3be573aa6bedd3133d09daa9d10768adb9e398983a9721d5dbfc` |
| `docs\.ai\initial-build\DP-M05-Execution-2026-10-31.md` | 7133 | `ae0d554499578af3919a099d497f389028bfe924deee525a804aaa078767c63d` |
| `docs\.ai\initial-build\DP-M05-Execution-Retry-2026-10-31.md` | 54772 | `24413614cdb6a0f23d8b31606f812ce95a815ea151d2040763a46c75fd3107cb` |
| `docs\.ai\initial-build\DP-M06-Execution-2026-10-31.md` | 61765 | `a4e222448bc1ad96128e5db02a7e7c1224d9af978ead07a95a0b67a5b5913f4b` |
| `docs\.ai\initial-build\DP-M07-Execution-2026-11-01.md` | 15323 | `4aee8ec9bd4d9275d5f4de705f99a0ab649751f0ebfd5cf2e9731e9b8b525eac` |
| `docs\.ai\initial-build\DP-M07-Execution-Retry-2-2026-11-01.md` | 113901 | `bc55ab08676a6fd4bb027c6f03b5a9fe32cf71e88339acd76bd8eee85473abfd` |
| `docs\.ai\initial-build\DP-M07-Execution-Retry-2026-11-01.md` | 2224 | `9fe14f9aa5e1f2f42ef5f79d72ef8228449ead771d04e66549758bf4993ea5d7` |
| `docs\.ai\initial-build\Evidence-Intake-RED-Planning-Dry-Run-2026-11-01.md` | 666581 | `895e49bcdbcb6b21bd7890235f081c9caa18f7794491f6fbe4cb00a056d5d5a7` |
| `docs\.ai\initial-build\Identity-Contract-Clarifications.md` | 12823 | `7ca2bf8c40eb7eb44661c3dc4f482767db6e38bad43cc73aaab51c455906daab` |
| `docs\.ai\initial-build\Identity-Fixture-Scope-Amendment-Proposal-2026-10-30.md` | 5714 | `7bd2bdc2f395eb179296c9093a8e1a892397f1c08cfadd887b20a0e0da4b9f6d` |
| `docs\.ai\initial-build\Identity-Readiness-Verification-2026-10-30.md` | 7470 | `950ad4b0cbf44c738b88003f3fd1933bda5c1162f1844d932718e5dda6cb3496` |
| `docs\.ai\initial-build\Identity-Scope-Verification-2026-10-30.md` | 22643 | `e9436a37226a25b0b1d73cd23107635de5570b77ed73f053f4982edecef6793d` |
| `docs\.ai\initial-build\Identity-Startup-Diagnosis-2026-10-29.md` | 8570 | `7066731b3152dd9e0cefbf503bac6373e250e76917fa2c83b6bfd258a0461f3f` |
| `docs\.ai\initial-build\Local-Git-CI-Deferral.md` | 2418 | `a2134cee0fc7b10dd02da892f1809f27cd47ca714ab120f3463cc8fc86e800bb` |
| `docs\.ai\initial-build\Plan.md` | 45159 | `cf2c9da2f220ec2789e7ab73c913116ffc9d80273a9216c7a1287f1a10a86966` |
| `docs\.ai\initial-build\requirements.md` | 24333 | `412d934fab14aef387fda60615d34f87fa8153870df83e74f151164aa90bdd65` |
| `docs\API-REQUEST-RESPONSE-REFERENCE.md` | 26424 | `ddd31964e42019147e6d197e2836f374c2b9aa595be1215137624520b58880ff` |
| `docs\APPROVAL-SUMMARY.md` | 7779 | `65918bdd64144ec33fef0b2c1975eecbfbb2d84f9166e18cb2fc0d11f59a52a7` |
| `docs\ARCHITECTURE-FLOW-DIAGRAMS.md` | 19924 | `e1abfe699b3570eeaf601a4098a1567a8ac2f65783565236dba4f2c0318e5fe5` |
| `docs\CHECKPOINT_CITIZEN_MEDIA_DISPLAY.md` | 5504 | `3476011d48131efd863f5348b32addfa23790601ddd5cca34e178e04ebf4af01` |
| `docs\CHECKPOINT_M9_AUTH.md` | 7035 | `835c644d34038a38164635d9ab9e5a009585d26fcdb2bb2995c2e5956d07838e` |
| `docs\CITIZEN_SIGNUP_PLAN.md` | 10006 | `4572f5b0c3a1e7676d65221401431bddfefe0bd61ab10495578372bab84ff0ae` |
| `docs\COMPLETION.md` | 13467 | `2d8e6fd0ca2b2458ed95f597d657c3aea783efd9fc8aa269f4aaff8df0fffd2d` |
| `docs\COMPLETION_CHECKLIST.md` | 7430 | `4ab3e9b9e9724ebf244e72ad342455451ea950c2a373c93d4d47e176fbf6fe8a` |
| `docs\CONTRIBUTING.md` | 17268 | `7a0cdc99effa01d341a8e210c9518b55d8aeba3bbae44a95ca7112dcf66c282e` |
| `docs\DELIVERABLES.md` | 15889 | `f4994865e3941ef0b3d4ca6b2dfcbcab115255fcac7cc8cad3e65742d5fcf966` |
| `docs\DEPLOYMENT_VERIFICATION.md` | 15922 | `46a389d86d3b5f70662ad4d7a978f45f211662e458c7980ba59f532fb9450956` |
| `docs\EXECUTION-HANDOFF.md` | 9048 | `4cd0737382463c212e32fb3124a552b699255ace04cc542d99363f54bfb1735c` |
| `docs\EXECUTION-PROGRESS-M1-M3.1.md` | 6818 | `554e1e7c365da5a54b7e1e1428910902abdd64d0f526c29ce00383fa0a79166b` |
| `docs\EXECUTION-PROGRESS-M1-M4.1.md` | 13602 | `89e34829b630016e9e91b4de91d9eb07ffefe0581886cfba54c7d9e4a2c7dfd0` |
| `docs\FINAL_SUMMARY.md` | 3808 | `d61ad10189fd6ef0da8786b006b29b6790a22c785e4d156d2dec42f49c40fd52` |
| `docs\FINAL_VERIFICATION.md` | 10031 | `1901e74e5d55fa361127a0dffa188ef184f584df520b74b9e74f6842c3699452` |
| `docs\GCP_DEPLOYMENT.md` | 15180 | `64d9792b569744ffc20db9223eb03cb2ed039059d7b2bb64e6cbd84c15c20d32` |
| `docs\IMPL-M1-DATABASE-SCHEMA.md` | 21784 | `f05e601afe89bcb12932e3e09f4b62b98683b9cf1747301c040fca12753264f6` |
| `docs\IMPL-M3.1-MEDIA-UPLOAD-RED.md` | 18092 | `6ea4067745ea0a36528339177c091630c11b6a28e0a9dbba45637d13041be0ea` |
| `docs\IMPL-M3.2-MEDIA-UPLOAD-GREEN.md` | 10029 | `41582f216b8b7f0d57d24599ee2b606cf75b4c45f3cf47be4799807e4ecece33` |
| `docs\IMPL-M4.2-API-ENDPOINTS-GREEN.md` | 16332 | `63f6a50a611944b66dd142790063ae23c811dec99e03b868903be88620d7af66` |
| `docs\IMPLEMENTATION-PLANS-M5-M6-M7.md` | 26060 | `5d3ee90974031a15614a3137b4f883d089031c0d07851603ad603e30800d9853` |
| `docs\INDEX.md` | 21664 | `3ecb0b605a5ac4f7c3be2b62937c481201bb3b61c9478dbe65eed54e19424d86` |
| `docs\INTEGRATION-SUMMARY.md` | 13335 | `81ecfcc02105a8615c415f8a933a2df09316749bb16c3435a03fb6e4a2b90a9e` |
| `docs\LATEST_FIX_SUMMARY.md` | 3507 | `a9e7e80b213ced82498c8132ce3009947e0eaae1cc245f7c6bacaf2d7e0bb92e` |
| `docs\LOCAL_DEPLOYMENT.md` | 11091 | `bb95512e1aab43df3c3c17b596c2d72848bc1e06164dd2a38ec4828d382c3e84` |
| `docs\M3.2-M4.2-COMPLETION-SUMMARY.md` | 17114 | `21da48c7fc2784978c5ff3c5ef0817e7286f3f457d9fe0e51de0d9f69a81883a` |
| `docs\M5-DOCUMENTATION-INDEX.md` | 9092 | `2bc19bc88632f3259182cc49cf95d917301a566d321afd9983f2f55008535b53` |
| `docs\M5-PLANNING-COMPLETE.md` | 11475 | `8ab080702522b0bfc93599f840963b48e91daf4b5e404920eac18acaab174d6a` |
| `docs\M5-UI-IMPLEMENTATION-CHECKLIST.md` | 23786 | `f0ddcf3b924d63868e278f72db5460ba663e50bc1b1014b6b2126dd0c2d48332` |
| `docs\MEDIA-UPLOAD-FIX.md` | 4679 | `fffe2f023517d222c7dd53e97ca91e929181270f5cda99af2246909787e2cf3f` |
| `docs\MVP_RELEASE.md` | 14473 | `5acbfb8ca527cfd0a8f6b1177c38b00f2944d7ef03ceb13105132b2bb37ed4c3` |
| `docs\NEXT_STEPS.md` | 13444 | `356c4251fb117c55a5645765319f4f2f3cb9b2d73fabaf16730972ddbcac4cb6` |
| `docs\PARALLEL-IMPLEMENTATION-ROADMAP.md` | 6459 | `623b67cca7a7d2fb0bce9f52a5f961641e13b7478fc202617284fce2e8409726` |
| `docs\Plan.md` | 19503 | `8a27e2587af3991285d4a03430293c8d3058c6832856aab5d873487370e42208` |
| `docs\PLUGIN-REVIEW.md` | 46934 | `48dce7d71d2d0711ecb51c401e6ec872d64302505b50c5282cdde9db13eb72d1` |
| `docs\PLUGIN_REVIEW_UPDATE_SUMMARY.md` | 6278 | `f91021ade9c043a8d97ee39c8449ebfc31667c53481c9a380d21d4ff02400371` |
| `docs\QUICK_REFERENCE.md` | 6700 | `0d35eff78c63b3197009d22840189e1bc587f5fbe3874b275c67f20fef8d1b5b` |
| `docs\QUICK_START.md` | 2983 | `470934ac49ef4e29cd2030c782e598e2a2bb05b1e8e3df07f7bd34eae6f9d692` |
| `docs\README-INTEGRATION.md` | 13727 | `779000b2b891201f7ed0f70e0c77bc77cfee37d1cb0da1fbe8b3cc48a215a2e5` |
| `docs\README.md` | 8636 | `4b53930d3820956e532c7fe9918ff2f8c2294cea104f514179ffbed7a36e27ef` |
| `docs\RELEASE_NOTES.md` | 10557 | `bc5482c238bedde5239bcc1c3ede3184ec7be22ccced25a646b34748a16cd00c` |
| `docs\REVIEW_CASE_FIX.md` | 4363 | `aaf21147c0d995f299e6bbf10e94d258acc70cb28f93894402ef3693ae6a5170` |
| `docs\RUNNING-GUIDE.md` | 8905 | `fdab71acb67074c7e5086bfd61ac5bab9a74b025e6d0281a6bb7cfae8595c897` |
| `docs\SESSION-SUMMARY-M5-PLANNING.md` | 12580 | `44d173561dc5da3185118c54e165e1cf1b212146d6107ef7d7ba6aea4464359e` |
| `docs\SESSION_STATUS_FINAL.md` | 5923 | `3bbdb1555c14db8eb598b7cb22aa19e9d16bd25c62379199dfa43547189d60f0` |
| `docs\SESSION_SUMMARY.md` | 5893 | `a227f5b0e4d79565e3b46d1d29d6bc25834f58d401af05ea4a9f316e44d12483` |
| `docs\START_HERE.md` | 8993 | `434ab0b09c6ed72676c455fecf393ba3e75cbd4db43965bb9a45b61b644635e8` |
| `docs\STATUS.md` | 10040 | `f9623e06d59f8b54f6866f9e3c6949a5dc84ba93f9fe3e32e6829eea09299eac` |
| `docs\TESTING_CHECKLIST.md` | 3343 | `b325b7063e11632366d13f8a1387240ecb17f043f878fe88d2f4617191d5c125` |
| `durable.py` | 19403 | `d61acafac7b8fd234300c79de1219c29bdb1de6c8f3848b55f4e97b95103b8c1` |
| `gemini.py` | 22744 | `04ad63d537d600b54d58abf7bf63598731fc432f0d0b4aa4fedf54bc8a7646cb` |
| `intake.py` | 5599 | `dcff0c3168d6d786857391d03c704f2068b844fba36a5e09cc12d116af3d1a74` |
| `media.py` | 11249 | `2a437be18c7b25a10d6e96864fd97fe662be63c8dcf1c35eafe3f4b9296f285d` |
| `pytest.ini` | 336 | `c5a2e33860eec755c2a320eb36c4129a83569de196f448d8a446dc22f758c112` |
| `README.md` | 5387 | `5ddb64e441e940670f8a40a7cc9b27c64fca8f9b1796719c10b88c3e10c1f894` |
| `requirements.txt` | 321 | `0f92f78ec6c38421c999a1096f7b773e4d6aef5dbdaf53b45dbcbed6c79601d8` |
| `runtime_controls.py` | 29680 | `cd5d6890b2345fb74b71f0a92608632060120320d1000e741e66772a26216235` |
| `static\css\base.css` | 1286 | `fe5885517354ed5dd25887070d818a2a44faed1aac6fee28c4771073686984b4` |
| `static\css\components.css` | 4337 | `dc585897a111a1a364d777e4a7ddc5a52f9da256d5491fc268a198912dbbaa78` |
| `static\css\layout.css` | 2252 | `e0367ec5e151769e46a46cc09b3e907edbc0915095d66d81ae92481c9c6cb475` |
| `static\css\responsive.css` | 3284 | `7847b965b18ab71256e283f751c1a5ebb14de315f8f255ebdf5a785873c9be4c` |
| `static\js\api.js` | 3761 | `28a025e6f92e0c0956f9b476c9aa0d7ee6e7ee64d941ec9760ec32af3ce25ce6` |
| `static\js\auth.js` | 1874 | `bdb14f52cd028ff343700f0f5f4897bb7eaf48ab814757131e5b71622f37ca0e` |
| `static\js\common.js` | 3722 | `49da203258429206a1e7783ded2621c231b0f5b05166e9942d1195db43148613` |
| `static\js\utils.js` | 3193 | `33a652b106fcbea84345682fb6ddac6c52ba4ff01d9c8bb6e07707dd17554539` |
| `templates\citizen-dashboard.html` | 3933 | `9f42fa889b58de3bfc7f2305cea77ae4966d5ac2c44d5460bddf47e60941d0e8` |
| `templates\citizen-login.html` | 2849 | `4c78c8247936c554c723da5c01c8218c88792f14e79d3cf0212fdba83edc33a7` |
| `templates\citizen-report-detail.html` | 4886 | `f2894968f166dcef59129f4ddcb9746a91e15fb99dbca6ec3b51976084321482` |
| `templates\citizen-report.html` | 7820 | `8b35a5066d0eecab9c463542bf3c4faea9b1909bf1f072aee903eb714f022fec` |
| `templates\citizen-reports.html` | 3345 | `ccef26379459ca92d6b17efba5eea6a2d8f39dfa03e5463ebe7d66e9a502e876` |
| `templates\citizen-signup.html` | 3961 | `62a130dc36a58bb32ea9f9146fc0ace0600733650e019b8dfa1caa37555cd3a4` |
| `templates\officer-detail.html` | 7207 | `47db566de467bcaca75a44439f63b216bf8697bd3f135476983e602f2fc7291f` |
| `templates\officer-login.html` | 4192 | `a4a12d4f17758eb7cff88ceb72aa2d5a8b9e550606575e7d90d458aa90724866` |
| `templates\officer-queue.html` | 3703 | `2617d0f84da3ef3d39189ef9c99f1746224d8569efe1bb69dc6ef1e8764aafc5` |
| `templates\officer-signup.html` | 5940 | `1b3a8e6f95cc49910eef128f4d49b0a7bb91b4d37e567b105ae522f3466b2548` |
| `tests\conftest.py` | 4618 | `7b13fd4d3f905c3dfce4bcb4e737fd4ffdccdadae939a9644033ccad955950ce` |
| `tests\test_api_endpoints.py` | 18809 | `e456805e78b63ec5fa0b1b681414750e0ef4280d65b832e0e9828a8a4ac908b7` |
| `tests\test_auth.py` | 17951 | `430012cd766919ee739c24f253abab53ff60742b9c773315dc0ca1427f93f2a7` |
| `tests\test_controls.py` | 63046 | `d0c3e86f7a958661aa69e27910365951714167858ed680b80eaf9e6fa70c8c20` |
| `tests\test_durable_processing.py` | 16000 | `09e4a9ac403d090e8f3aadd0a62b6326e078254c27891a6e03145781af2a0210` |
| `tests\test_evidence_intake.py` | 35513 | `f668a5be2301b3ffeb0a5c6d162288e9f7aa85a546b7339e5b37ef5ff51dfa34` |
| `tests\test_gateway_openai.py` | 23656 | `5fb0f9e164842a2afaea5744aaf9da02de13bce31204bedb329bb2ccb3b4258b` |
| `tests\test_gemini_assessment.py` | 21841 | `cac4245095c4d72d25c0b719f7e16d5ee0780b62ab4a9db7789359cb40287aa0` |
| `tests\test_identity.py` | 13023 | `7b22df16cd0c2ca7a7dbebc3e28e2762cf508549f3c212f185a63b683c8a7557` |
| `tests\test_identity_oidc.py` | 9407 | `f9ca6c38d81a9c2bfe6cf374bdfb6cfd0fbc6e2953f3871b0df7d2979fa3bf63` |
| `tests\test_media.py` | 13126 | `667d98ed53c40d0deb7a0663e989268c310a2b746b27017e8bf44260d455dcc5` |
| `tests\test_provider_response.py` | 14023 | `198f3b2e41489a6b7480fc4e21e21c2a299ea9563b5bb9f85778381e99a29cc8` |
| `tests\test_verification_harness.py` | 1721 | `e7f09bc4e5498b6302e10f75aebda885a807631cd5975d2d25c9c1fd459086c7` |
| `tests\verify_current_demo.py` | 6526 | `76fa52c4f46076aa706614930c13f4e1559ad6516e67b07fc5ce660e7afbc038` |
| `tests\verify_durable_processing.py` | 5829 | `8b81890ac1c0bfca6f1e2564583a649d3a3f95e3f2adbc1e4c428cda31e0bb57` |
| `tests\verify_gateway_openai.py` | 7308 | `6a64e4a3311e2f5c626100e24c425f17fb03cc2e84f7f9a3bd8e557392e132c0` |
| `tests\verify_gemini_assessment.py` | 5811 | `9dc535df5fc4f781f1d4a588ceeb1bdc16cafd9d59b39ef0e14fdac81b4bb721` |
| `tests\verify_provider_response.py` | 6231 | `285278df42c8d7696f329acc00464dedec70751d58d4cc1ca9e35eeed6dea9a3` |

## Other metadata protection

40 path/size/mtime records only; no private content/hash read or backup. Snapshot JSON SHA-256 `6fb1dfe081dcb7256d90bdf4c3036997b99458421008445f554c8137dd41803c`.

| Path | Bytes | mtime_ns |
| --- | --- | --- |
| `.dockerignore` | 517 | 1793595219988839600 |
| `.gitignore` | 78 | 1792898201180297500 |
| `Dockerfile` | 1235 | 1793595270974960800 |
| `roadwatch.db` | 126976 | 1794171051258729800 |
| `start-windows.ps1` | 4022 | 1793671294921440600 |
| `start.sh` | 1508 | 1793595188355042400 |
| `.github\copilot-instructions.md` | 14335 | 1793578161610126500 |
| `.github\workflows\provider-free.yml` | 816 | 1792898201379694700 |
| `.local\compose.json` | 17001 | 1792898388511298000 |
| `.local\gemini-api-key.txt` | 53 | 1794280122943851100 |
| `.local\openAi-api-key.txt` | 164 | 1794363991446306900 |
| `.local\private\ai.dsn` | 70 | 1792898388490397200 |
| `.local\private\ai.password` | 48 | 1792898388490397200 |
| `.local\private\ca.crt` | 1436 | 1792898388467784500 |
| `.local\private\Caddyfile` | 764 | 1792898388509524300 |
| `.local\private\collector.json` | 333 | 1792898388507892500 |
| `.local\private\configuration.dsn` | 92 | 1792898388497239600 |
| `.local\private\configuration.password` | 48 | 1792898388492431000 |
| `.local\private\gateway.dsn` | 80 | 1792898388492431000 |
| `.local\private\gateway.password` | 48 | 1792898388490397200 |
| `.local\private\init.sql` | 774 | 1792898388497239600 |
| `.local\private\keycloak-admin.password` | 48 | 1792898388477043200 |
| `.local\private\keycloak.dsn` | 82 | 1792898388485000900 |
| `.local\private\keycloak.password` | 48 | 1792898388483469100 |
| `.local\private\media.dsn` | 76 | 1792898388488364100 |
| `.local\private\media.password` | 48 | 1792898388488364100 |
| `.local\private\postgres.dsn` | 82 | 1792898388481439700 |
| `.local\private\postgres.password` | 48 | 1792898388480519600 |
| `.local\private\reporting.dsn` | 84 | 1792898388486283600 |
| `.local\private\reporting.password` | 48 | 1792898388486283600 |
| `.local\private\tls.crt` | 1736 | 1792898388467784500 |
| `.local\private\tls.key` | 2484 | 1792898388473441000 |
| `.local\private\traffic-realm.json` | 604 | 1792898388499258200 |
| `media_store\20875598e19c4b43\without helmet.jpeg` | 30315 | 1793767030711839000 |
| `media_store\79b591276eb84741\without helmet.jpeg` | 30315 | 1793769104077181300 |
| `media_store\93295ec88d434321\test_display.jpg` | 1305 | 1793767249227640700 |
| `media_store\98f0f6a896974378\helmet_violation.jpg` | 1617 | 1793767352829237600 |
| `tests\test_media.py.bak` | 27759 | 1793513936128832900 |
| `tools\check.py` | 5311 | 1793059154861089900 |
| `tools\local.py` | 10714 | 1793492254919352200 |
