# Runtime controls contract clarifications

## Human Review

**Q31–Q34 approved by user on 2026-10-30.** Approval covers the exact controls decisions below, including the rejection-only service actor in Controls-Service-Audit-Actor-Clarification.md, and their incorporation into requirements.md and API-Contract.md CT-13. This is not an Implementation Plan, executable-change approval or spending authorization. DP-M05 remains Pending until its own reviewed Implementation Plan and execution; recommendation/proposal wording below is retained as the reviewed decision text.

## Verified basis

Rechecked requirements IB-R20/Q27, Architecture-Proposal AP-D06, Plan DP-M05/06 and its concern ownership, API-Contract CT-01/02/04/08/09/10/12, current bootstrap.py and tools/local.py on 2026-10-30. CT-01 already defines collection pagination and timestamp/UUID conventions; those are not reopened. CT-08 defines snapshots, settings/ranges, publication, audit, consumer refresh/staleness and initialization, but does not specify the initialization mechanism, actor/audit representations, or internal health route and caller permission. Current code has identity and Foundation readiness only; it supplies none of those missing controls behaviors.

The following recommendations were approved as Q31–Q33. Their implementation remains future work. Record them in the requirements clarification log and incorporate the normative delta into the API contract before preparing DP-M05 tests.

## Q31 — Explicit baseline and management behavior

Recommend an operator-only initialization command, with its exact executable interface reviewed in the GREEN Implementation Plan. It uses the private configuration-database role, validates the complete CT-08 defaults, and atomically creates revision 1 plus its publication audit entry. Baseline has `ai_enabled=false`, `ai_budget=null`, schema_version 1 and no spending authority. No application startup, GET, consumer fallback or environment override implicitly publishes it. There is no public initialization endpoint or `c0` bootstrap convention.

Initialization requires a reason. Repeating initialization against an initialized store returns the current snapshot without overwriting it, advancing revision or duplicating the initial publication audit. A concurrent initializer creates only one baseline. Ordinary HTTP publication still requires the existing positive-revision `If-Match: "c<revision>"` and Idempotency-Key. A new authorized publication with identical values and a fresh key/current precondition creates a new revision; an exact authorized idempotent replay returns the original snapshot without another publication.

Management reads use the current primary-store snapshot. Missing baseline returns 503 `CONTROLS_UNAVAILABLE`; database/audit-store failure returns 503 `DEPENDENCY_UNAVAILABLE`. Both use the CT-01 envelope, retryable=true and Retry-After 5. Missing required precondition or idempotency key returns 428 `PRECONDITION_REQUIRED`; malformed controls ETag or UUID key returns 422 `VALIDATION_FAILED`; stale valid ETag returns 412 `REVISION_CONFLICT`. CT-08 payload validation remains 422 `INVALID_CONTROL`, including an attempt to enable AI without the required authority/eligibility/private credentials. The explicitly nullable `ai_budget` remains an exception to general null rejection.

Publication reason is trimmed plain text of 1–2000 characters; other missing, null, unknown or invalid publication fields retain CT-08 validation. Snapshot `created_at` and `effective_at` are the same committed publication timestamp, in the existing UTC millisecond representation. Revision is a positive integer; publication does not schedule future activation.

## Q32 — Actor and audit representation, replay and failure handling

Recommend snapshot actor as exactly:

```json
{"type":"human","issuer":"https://auth.traffic.localhost/realms/traffic","subject":"exact JWT sub","client_id":"traffic-web"}
```

The initializer uses exactly `{type:"system",issuer:null,subject:"controls-bootstrap",client_id:null}`. Human issuer, subject and client ID come only from the validated principal, preserving their approved identity semantics. Actor objects are read-only; clients cannot submit them.

Q34 supplements this actor schema as follows:

For a rejected authenticated service-client publication attempt, permit audit actor exactly:

```json
{"type":"service","issuer":"https://auth.traffic.localhost/realms/traffic","subject":"exact validated JWT sub","client_id":"traffic-completion"}
```

The subject is the exact validated token subject, not the illustrative string. client_id is the validated fixed CT-12 azp of the actual service caller, not necessarily the example traffic-completion. issuer is the validated fixed issuer. These values never come from the submitted publication body, an inferred service-account username or an arbitrary client string.

Only rejection audit entries may use this service variant. The request remains 403 FORBIDDEN; its outcome is rejected, error_code FORBIDDEN, reason Publication rejected, publication_revision null and old_values/new_values null under CT-13.2. An invalid token remains 401 and follows the existing unauthenticated failure-signal rule.

Published snapshots and publication audit retain human actors; the baseline retains the existing system actor. Services cannot publish controls, replay a human publication, gain human grants or alter snapshots. No route, client identity, scope, permission or milestone ownership is added.

GET controls audit retains the existing `{items,next_cursor}` collection envelope and ascending sequence/cursor rules. Each item has exactly these fields:

| Field | Proposed representation |
|---|---|
| id, request_id | Canonical UUIDs; HTTP request_id matches the response header |
| sequence | Positive monotonically increasing audit sequence |
| at | UTC millisecond timestamp |
| actor | The actor object above |
| action | `initialize` or `publish` |
| outcome | `published`, `rejected` or `replayed` |
| reason | Normalized reason for publication; fixed `Publication rejected` or `Idempotent replay` for those outcomes |
| publication_revision | Created/original publication revision for published/replayed, otherwise null |
| old_values, new_values | Complete safe CT-08 values for a committed publication; old_values null for baseline; both null for rejected/replayed attempts |
| error_code | CT-01/08 failure code for rejection, otherwise null |

Audit captures authenticated HTTP publication attempts, including forbidden callers, validation/precondition/concurrency rejection and idempotent replay. A replay audit entry is not a second publication audit entry and creates no new snapshot. Unauthenticated failures remain sanitized security signals rather than configuration-database audit entries. Reading controls or audit is not itself a publication attempt. Repeated operator initialization is the no-op described in Q31.

Only allowlisted committed control values enter old/new fields. Rejected bodies, unknown field names/values, submitted invalid reasons, tokens, credentials and private file contents are not stored in audit. Failure entries use fixed reason text plus the stable error code/request ID, with no raw request or provider diagnostics.

Snapshot publication and its audit/idempotency result commit atomically. If the required audit write fails, publication fails with 503 and no snapshot change. During a configuration-database outage no durable database audit entry can be promised: return 503 without mutation and emit a sanitized failure signal containing request ID and error class. Detailed operational signal implementation remains with its existing observability owner; no fallback database, local durable queue or unapproved storage is introduced.

## Q33 — Per-instance control health and least-privilege caller

Recommend `GET /internal/v1/controls/health` on the existing application role processes. This adds no service, public management permission or business handler. It returns exactly:

```json
{"instance_id":"uuid","service_role":"reporting","revision":1,"age_ms":0,"degraded_reason":null}
```

service_role uses the existing five-role enum. revision is the last validated positive revision or null before any valid snapshot; age_ms is the nonnegative integer age since the last confirmed valid read, or null with no valid snapshot. degraded_reason is null, `missing_snapshot`, `invalid_snapshot`, `store_unavailable` or `stale_snapshot`. A failed or invalid read does not reset the confirmed-read age. A successful read resets it even if the revision is unchanged. Once age exceeds 60,000ms, stale_snapshot takes precedence. Existing CT-08 rules still determine whether affected new work may proceed; health metadata itself grants no work or spend authority.

An authorized health read returns 200 even when its metadata reports degradation; CT-01 authentication/authorization/dependency error envelopes still apply to request failures. Foundation readiness remains unchanged and independent of controls.

Extend the CT-12 matrix only for the existing confidential `traffic-reporting` client: add scope `controls:health` for receiving audiences `traffic-api`, `traffic-media` and `traffic-gateway`, solely for this GET operation. This permits diagnostic reads from reporting/completion/AI roles using traffic-api, media roles using traffic-media, and gateway roles using traffic-gateway. It grants no controls publication, human operation, media access or assessment dispatch. Other service clients and human principals cannot use this operation. Existing fixed-client classification, canonical service scope grammar and receiver-audience checks remain; invalid authentication is 401 and an authenticated wrong caller/scope is 403.

## Preserved boundaries

No live AI spending is authorized. Positive budget/accounting tests may use clearly labeled synthetic authority and provider-free test inputs; those fixtures never become production spending authority. DP-M06 owns independent control/ledger safety and uncertain-liability behavior already assigned by the Plan; DP-M12 later integrates provider workflows with those capabilities. No concern is reassigned and no real provider call is required here.

All existing settings/ranges, five-second consumer refresh rule, sixty-second ordinary stale allowance, fresh transactional AI authorization/reservation, immutable in-flight ordinary policy, identity grants and pagination remain unchanged. Concrete internal Python seams, SQL schema, migrations and command implementation belong to subsequent reviewed Implementation Plans.
