# M08 live verification diagnosis — 2026-11-09

## Observed live result

The first authorized image case used the actual application/default Gemini adapter. It ended `failed / PROVIDER_REQUEST_REJECTED`, after one consumed attempt, with no assessment or modelVersion. Its report remained `awaiting-review` with zero points. The batch stopped. Helmet, additional supplied images, mixed images and video were NOT RUN. See [execution evidence](ASOR-M08-Execution-2026-11-09.md).

The current capture does not preserve the original provider HTTP status, request stage or sanitized error reason. None is inferred here. This is a real failed criterion, not merely a missing-input condition.

## Read-only diagnosis after the stop

No further media upload or inference request was made. The designated private key was read only inside diagnostic processes; its value was never printed or passed through command-line arguments. The same approved model remained selected.

1. A metadata GET through the production bounded client failed with `httpx.DecodingError`.
2. Direct metadata GETs through ordinary HTTPX, with redirects disabled and `Accept-Encoding: identity`, returned:

```json
{"operation":"models/gemini-3.8-flash","http_status":200,"approved_model_accessible":true}
{"operation":"models","http_status":200,"approved_model_listed":true}
```

These observations establish access to model metadata with this key. They do not establish inference quota, billing tier, successful file upload, accepted generation request, or image-analysis correctness. No alternate model was called.

## Confirmed transport defect

The child in `durable.py` serializes `response.content` (already content-decoded by HTTPX) while retaining all original response headers. The parent constructs another HTTPX response with those headers and the decoded bytes. A retained `Content-Encoding: gzip` therefore instructs the parent to decode already-decoded data.

Local synthetic reproduction, with no network or private inputs:

```python
import httpx
httpx.Response(200, headers={"content-encoding": "gzip"},
               content=b'{"name":"synthetic"}')
```

Observed: `httpx.DecodingError`. The production bounded metadata GET independently reached the same exception class. This defect is confirmed; it is not proof that it caused the first image case's separate `PROVIDER_REQUEST_REJECTED` result.

## Required next review

- Add meaningful RED coverage for real child/parent response framing, including compressed responses; existing MockTransport checks bypass this transport boundary.
- Plan the smallest framing correction, keeping the absolute deadline, kill/reap, no-retry multiplication and secret boundary intact.
- Preserve sanitized provider HTTP status, stage and allowlisted diagnostic class so a real request rejection can be investigated without raw provider bodies, keys or token URLs.
- Reverify existing behavior and review the failed live protocol before another inference attempt. Do not weaken output validation, substitute models or retry until a desirable answer appears.

No production/test/configuration change was made by this diagnosis. The existing M08 approval history is retained, but its execution stopped at a genuine failed live criterion and requires reviewed next steps. M08 remains Blocked; M09 remains Pending. Video testing is deferred to the user's manual verification; it has not passed.
