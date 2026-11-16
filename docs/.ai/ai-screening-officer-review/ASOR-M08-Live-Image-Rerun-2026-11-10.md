# ASOR-M08 live image rerun — 2026-11-10

The user authorized the image rerun after [M08B verification](ASOR-M08B-Execution-2026-11-10.md). The exact external runner from [007](007_Implementation_Plan_Gemini_Assessment_GREEN.md#exact-live-runner--external-verification-protocol-only) ran in a disposable source-only copy using the existing interpreter, the real managed application and its default Gemini worker. The runner received only the first case so that its result could be checked before another case was submitted. All locations and vehicle numbers were unknown staged context. The duplicate helmet image was excluded.

| Authorized case | Outcome |
| --- | --- |
| Suspected triple riding | Failed. The photo shows multiple visible riders, with the exact count uncertain. |
| Apparently unhelmeted riders | Not run after the first failure. |
| Fruit image submitted under helmet | Not run after the first failure. |
| Busy road still under red-light | Not run after the first failure. |
| Mixed fruit and busy-road images under red-light | Not run after the first failure. |
| Video | Deferred to manual verification by the user. |

The exact runner exited 1 on the first case. Before cleanup, a read-only query of the isolated database returned the allowlisted diagnostic below.

```text
case=photo-triple-riding-01
selected_model=gemini-3.8-flash
state=failed
failure_code=PROVIDER_REQUEST_REJECTED
attempt_count=1
provider_status=402
request_stage=upload-start
diagnostic_class=HTTP_STATUS
workflow_status=awaiting-review
points=0
assessment_present=false
```

The provider rejected initiation of the resumable upload. Image transfer and generation were not reached. The provider's specific reason and the project's billing tier remain unverified. The November 9 attempt's original status and stage remain unknown. There was no returned model version or assessment to evaluate against the configured `asor-prompt-v1`, `asor-relevance-v1` or `asor-in-national-2026-11-08-v1`.

The public Standard pricing basis was checked on November 10. Google lists free-tier input and output and paid rates of USD 0.75 per million input tokens and USD 3.75 per million output tokens through December 31, 2026. Starting January 1, 2027, the posted paid rates are USD 1.50 and USD 7.50 respectively. No actual charges were verified. [Google Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-flash)

The run stopped at the rejection. The 199 recorded protected file paths, lengths and hashes matched, including the key file and source images. The key value stayed within the live run and its provider child. The disposable database, uploaded local copy and temporary logs were removed after the sanitized result was captured. No owned Python or decoder process remained. Production source was unchanged.

M08 is blocked on live verification. M09 remains pending.
