# ASOR-M08B execution evidence

Verified on 2026-11-10 against approved Implementation Plan 009. Both passes exercised the same isolated local-demo source tree and fixture root. All nine prior RED cases passed, and every other named outcome matched the approved M08A inventory.

## Commands and observed results

Used the Traffic virtual environment Python with the disposable source-only directory as the working directory. Each command ran serially in passes 1 and 2. The XML argument points to a separate output directory under the owned scratch root for each pass. Logs were captured separately. Each pytest invocation reported one warning.

| Command | Limit | Pass 1 | Pass 2 |
| --- | --- | --- | --- |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<pass-dir>/provider.xml tests/test_provider_response.py` | 180 s | Exit 0, 13 passed in 59.25 s | Exit 0, 13 passed in 36.26 s |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<pass-dir>/gemini.xml tests/test_gemini_assessment.py` | 180 s | Exit 0, 47 passed in 36.53 s | Exit 0, 47 passed in 27.71 s |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<pass-dir>/durable.xml tests/test_durable_processing.py` | 180 s | Exit 0, 14 passed in 9.22 s | Exit 0, 14 passed in 9.22 s |
| `python -m pytest -p pytest_asyncio.plugin -q --junitxml=<pass-dir>/intake.xml tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py tests/test_verification_harness.py tests/test_identity.py tests/test_evidence_intake.py` | 300 s | Exit 0, 94 passed and 12 skipped in 48.28 s | Exit 0, 94 passed and 12 skipped in 49.72 s |

Both passes produced 168 passes and the same 12 existing skips. Each complete JUnit inventory matched the named inventory in [008](008_Implementation_Plan_Provider_Response_Correction_RED.md#full-repeated-named-inventories), with the nine provider failures converted to passes. The comparison included module, class when applicable, test name, parameter and outcome. Both runs produced identical SHA-256 digests per selection for the sorted inventory, serialized as UTF-8 `module::name outcome` lines with LF endings.

| Selection | Matched names | SHA-256 in both passes |
| --- | ---: | --- |
| Provider | 13 | `1d25998a96166f186dd7dabb0e99b5bcaf4017fd23fd717c9ca0187318b316e9` |
| Gemini | 47 | `5220aa453a2c9504a56518f44da3a9cd5411306e1275a5861d53c9082db186a7` |
| Durable | 14 | `94e318dc4011a8b86d5d6ce91eaeac34a255d2f82bebda7bb74ac81db697c3f8` |
| Intake | 106 | `78cd4c498fc9b03fad063c31b8e65cdebbeaa07d8a19cded117c8aad6851b3d2` |

## Exact patch, isolation and cleanup

Verified the byte length and SHA-256 of all 45 checkout-source rows in the frozen manifest. Extracted the reviewed diff as UTF-8 with LF endings. Ran `git -c core.autocrlf=false apply --check --ignore-space-change provider-response.patch` and `git -c core.autocrlf=false apply --ignore-space-change provider-response.patch` in the disposable copy and checkout. All four commands exited 0. Both corrected files matched the normalized after-code hashes in 009. All 26 staged Python files compiled.

Used the approved environment filters, disabled bytecode and pytest plugin autoload, and directed temporary state to the owned fixture root. The archived `decoder_carrier.py` matched SHA-256 `5052247f8ccde571d1707a188c07e409a311d18da4205c331840d97823888b5c`. Before each Gemini and intake invocation, the runner started a distinct carrier with `docker run -d --rm --network none --pull never --name <owned-name> --entrypoint /bin/sleep sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de 660`. It verified the image, network mode `none`, zero mounts, both decoder tools and forwarding wrappers on the child PATH before starting the test. No live provider or deployed infrastructure was contacted.

After each test child, the checkout and staged inventories matched the post-patch baseline. The final comparison covered 197 checkout entries and all 45 staged files. Only the two approved production files differed from the original checkout inventory before the evidence and status edits. The original provider test and classifier hashes remained `f614ff22f868dc6853f7b4320d00a5fe379845c9f241135d1287c1554ffbd9f4` and `285278df42c8d7696f329acc00464dedec70751d58d4cc1ca9e35eeed6dea9a3`, respectively.

All eight test children exited and were reaped. Each of the four owned decoder carriers was stopped and confirmed absent after its test. The owned scratch tree, including fixtures, logs and XML, was removed and confirmed absent. Both transient copies of the verification driver were removed. Two driver preflight corrections handled a space in one archived parameterized name and the manifest's 45 source rows. They occurred before source changes or test execution and did not change the approved selection, commands, limits or assertions. The checkout-wide `git diff --check` reported an existing blank line at EOF in `tests/conftest.py:140`, whose bytes matched the frozen manifest throughout verification.
