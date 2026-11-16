# ASOR-M08A revised RED execution — 2026-11-10

Executed the diagnostic fixture and disposable verification procedure approved on 2026-11-10. All inputs were synthetic and all app lifespans ran in source-only copies. No production source was changed and no live provider request was made.

## Test revision and checkout integrity

Before applying the three edits from 008, both archived file blocks matched the checkout byte for byte. The fixture now sets a 30-second budget on the app lifespan settings before submission, derives its wait from those same settings plus five seconds, and reports only the failure code and known call stages when its positive control fails.

- Original fixture SHA-256 `ff7776c163833b0b278d12475703e4849f79a27b1260988ceba3f64d9e888e73`
- Revised fixture SHA-256 `f614ff22f868dc6853f7b4320d00a5fe379845c9f241135d1287c1554ffbd9f4`
- Unchanged classifier SHA-256 `285278df42c8d7696f329acc00464dedec70751d58d4cc1ca9e35eeed6dea9a3`

Compared 193 checkout entries by absolute path, byte length and SHA-256, excluding 008, Git, the virtual environment and transient caches as prescribed. The fixture was the only changed entry before status and evidence were written. Compared 103 frozen scratch files by SHA-256. Both disposable copies used identical revised test bytes and identical classifier bytes. Private inventory records are unpublished.

## Isolation and commands

The completed invocations ran with the existing Traffic virtual-environment interpreter and explicit disposable working directories. The launchers used owned temporary paths, UTF-8, bytecode disabled and stripped provider/bootstrap environment variables. The variants retained the approved 180-second provider and 300-second intake child limits. Original Gemini and durable launchers retained 90-second limits. The exact temporary launcher, fixture transformation, decoder and probe code is archived in 008.

```text
repository> python tests/verify_provider_response_resume.py --red
repository> python tests/verify_gemini_assessment.py --green
```

The first additional Gemini preservation invocation exited 1 with 42 passes and five video setup failures (`INVALID_MEDIA`). The disposable decoder wrappers referred to the approved `decoder.py`, which I had omitted. I extracted the exact archived helper and restarted Gemini from its first run. The fixture, launchers, assertions and bounds stayed fixed. The valid revised RED pair was retained.

## Revised RED

Both runs produced the same named outcomes. The classifier verified two framing failures (`RESPONSE_FRAMING_MISSING`), six diagnostic failures (`SAFE_DIAGNOSTIC_MISSING`) and one reconstruction deadline failure (`ABSOLUTE_DEADLINE_MISSING`). The launcher exited 0.

```text
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m08a-lesha_an\\red-1.xml', 'tests/test_provider_response.py']
red run 1 exit 1
============== 9 failed, 4 passed, 1 warning in 75.05s (0:01:15) ==============
Classified 13 red nodes; no errors/skips
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m08a-lesha_an\\red-2.xml', 'tests/test_provider_response.py']
red run 2 exit 1
============== 9 failed, 4 passed, 1 warning in 65.95s (0:01:05) ==============
Classified 13 red nodes; no errors/skips
Protected source/state unchanged; repeated inventories equal
Owned disposable tree removed; children reaped
```

Named inventory for both repetitions

```text
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

## Gemini preservation

The first run completed with all 47 checks passing. The second run reached the original 90-second child limit and was killed and reaped. The launcher publishes test output only after its child returns, so the second child produced no published named outcomes. The timeout stopped this execution. Durable, intake and scratch soundness were not reached. The prior Gemini and durable reports lack comparable per-input hashes, so their historical results were not carried forward.

```text
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m07-hl1cvjqd\\green-1.xml', 'tests/test_gemini_assessment.py']
green run 1 exit 0
================== 47 passed, 1 warning in 67.98s (0:01:07) ===================
Classified 47 green nodes; no errors/skips
Command: ['C:\\Users\\avina\\Downloads\\avinash-repo\\v11\\Traffic\\.venv\\Scripts\\python.exe', '-m', 'pytest', '-p', 'pytest_asyncio.plugin', '-v', '--junitxml=C:\\Users\\avina\\AppData\\Local\\Temp\\asor-m08a-verify-20261110-8c13f901\\temporary\\asor-m07-hl1cvjqd\\green-2.xml', 'tests/test_gemini_assessment.py']
    raise AssertionError("TIMEOUT is infrastructure failure, not RED")
AssertionError: TIMEOUT is infrastructure failure, not RED
```

Named inventory observed before stop

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

## Cleanup

Process inspection found zero owned verification processes. The named decoder carrier was absent and the launcher temporary directory was empty. The literal outer scratch root resolved directly under the intended Temp parent and contained no reparse points.

Removed only the checked outer scratch root after archiving and independently confirmed it was absent.

## Frozen source inputs

The source-only checkout inputs below were checked byte for byte against the frozen verification state before archiving. Disposable helper hashes are reproduced from the exact archived blocks and launcher derivations. SHA-256, byte length and path are listed in that order. This manifest omits real database, media and private paths.

```text
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
```
