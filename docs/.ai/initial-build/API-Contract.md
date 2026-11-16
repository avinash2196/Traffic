# API and External Contract — initial-build

## Status and authority

Approved by user on 2026-10-24 for DP-M01; identity-profile clarifications Q29/Q30 approved on 2026-10-26 and incorporated as CT-12; runtime-controls clarifications Q31–Q34 approved on 2026-10-30 and incorporated as CT-13 with its CT-12 health-read extension. No executable change or spending is authorized. Sources: approved requirements.md, Architecture-Proposal.md AP-D01–AP-D06, and Plan.md Status dated 2026-10-24, External Contract Requirements and DP-M01. No existing effective contract exists. CT identifiers are approved decisions under that delegated CONTRACT authority. Package versions/executable commands remain DP-M02 decisions; telemetry alert thresholds and retention remain observability Implementation Plan decisions.

## CT-01 — Common HTTP and value rules

Public root: `https://traffic.localhost/api/v1`; identity issuer: `https://auth.traffic.localhost/realms/traffic`. HTTPS required; plaintext mutations return 400 HTTPS_REQUIRED. UTF-8 JSON, UTC RFC3339 millisecond timestamps, canonical lowercase UUID IDs, positive integer revisions and case-sensitive enums. Ownership uses exact authenticated `(iss,sub)` without normalization. Required fields reject absence/null; optional request fields allow absence but reject null unless specified. Text is trimmed, nonblank plain text. Unknown/read-only fields and query parameters reject with 422 INVALID_FIELD. Malformed JSON/UTF-8/duplicate keys: 400 MALFORMED_REQUEST; wrong types, malformed path UUIDs or bounds: 422 VALIDATION_FAILED. JSON body maximum 65,536 bytes; excess 413. Unsupported content type 415. Response null means unavailable/not yet assigned; arrays use [] for empty.

Error shape: `{"error":{"code":"REVISION_CONFLICT","message":"Refresh report.","request_id":"uuid","retryable":false,"details":{}}}`. Status/code/retryable and documented detail keys stable; message informative and sanitized. Missing/invalid token 401 UNAUTHENTICATED; denied role 403 FORBIDDEN; unknown/non-owned resource 404 NOT_FOUND; state conflict 409; stale revision 412 REVISION_CONFLICT; missing precondition 428; transient dependency 503 DEPENDENCY_UNAVAILABLE; throttling 429 RATE_LIMITED. 429/503 include integer Retry-After (default 5 seconds). No credentials, private paths, raw provider response or other citizen identity in errors. Responses use no-store and X-Request-ID; propagate validated traceparent through jobs/gateway without treating correlation as identity.

Collections accept limit integer 1–100 default 20 and opaque cursor <=2048 chars, expire after 24h and bind principal/filters/high-water mark. Invalid cursor 422 INVALID_CURSOR. Reports/exports descend `(created_at,id)`; timeline/audit ascend sequence. Response `{items:[],next_cursor:null}` defines empty/end. Filters are exact case-sensitive state/category equality; no search or arbitrary sorting. New records appear by refreshing first page.

## CT-02 — OIDC, permissions and private boundaries

Keycloak owns local demo accounts, credentials, login/logout and role administration through standard discovery/authorization/token/end-session/JWKS interfaces. Operator provisions citizen/admin accounts; reporting has no password/registration endpoint. Browser client traffic-web uses authorization-code PKCE S256, exact HTTPS redirect URLs, state/nonce; no implicit/password grant or browser secret. Bearer tokens stay in memory, logout clears them. Access lifetime <=5 minutes. GET `/me` returns subject, roles, permissions with the exact approved representation, effective grants and token profile in CT-12.

Validate fixed issuer, RS256 signature, exp/nbf/iat (<=30s skew), access-token type, fixed audience and allowed client. Audience traffic-api for reporting, traffic-gateway for gateway, traffic-media for media. Never accept ID tokens, dynamic issuer/JWKS URL or algorithm substitution. Refresh JWKS every 60s; cached validated keys usable <=300s after successful fetch. Unknown kid triggers one coalesced refresh; unknown key 401, unavailable refresh 503. Expired cache during outage 503. Valid cached keys can validate unexpired tokens; logout revocation across replicas is bounded by access expiry.

| Principal | Allowed operations |
|---|---|
| citizen | Own report creation/read/history/evidence/clarification and awards |
| admin | Read all reports and private evidence |
| admin + review:write | Clarification, final decision, authorized recovery |
| admin + evidence:export | Create/read/download ZIP; separate permission required |
| settings-admin + controls:write | Publish/read controls and audit; no review authority implied |
| service clients | Fixed client-credentials scopes/audiences only: reporting→media ingest/read/export; media worker→original; AI review→derivatives/gateway assessment:create; reporting completion consumer→completion |

Dual citizen/admin cannot review/finalize/export own report (403 SELF_REVIEW_FORBIDDEN). Authentication precedes resource disclosure. Service identities cannot call human operations. Network isolation complements authorization. Least-privilege database roles preserve ownership: reporting alone changes decisions/awards; media owns originals/hash registry; AI owns advisory results; gateway owns provider credentials/ledger; configuration owns snapshots/audit. Evidence streams only through authorized boundaries, never public/static URLs. Internal media capability binds caller/evidence/report/round/purpose and <=60s expiry, with current authorization rechecked. Private access/denial audited; tokens/bytes excluded from logs. Only gateway has provider egress.

## CT-03 — Representation and lifecycle

Report fields: id, created_at, updated_at, revision, round, category, description, state, evidence[], processing, ai, clarification, final_decision, award. Category is helmet|triple_riding|red_light; description 1–4000 chars. Evidence item: id, sha256 (64 lowercase hex), bytes, format, duration_ms (null for image), technical_state pending|valid|invalid|failed. Processing: stage, attempt, max_attempts, next_attempt_at, last_error_code, manual_review_available, policy_revision. AI status pending|available|disabled|exhausted|failed, source live_provider|test_substitute|none, nullable assessment/reason. No assessment does not mean rejection.

| State | Transition/action |
|---|---|
| screening | Current media pending; valid→ai_review, invalid/exhausted→processing_failed |
| ai_review | Success/disabled/failure/exhaustion→admin_review with explicit advisory availability |
| admin_review | Human request information/approve/reject |
| needs_information | One open request; owner responds; admin may finalize current valid evidence |
| processing_failed | Visible technical failure; admin request information/reject with human reason/retry transient exhaustion; no approval without valid screened evidence |
| approved/rejected | Immutable terminal human outcome; no new round, evidence, retry or decision |

Round starts 1; every durable visible change increments report revision (not heartbeat). Clarification request has UUID/prompt 1–2000 chars/admin/current round. Response text 1–4000 and/or 1–5 new evidence IDs closes request, increments round once and retains history/evidence. New evidence screened; text-only with prior valid evidence proceeds to AI; text-only without valid evidence is accepted but remains processing_failed with VALID_EVIDENCE_REQUIRED. Old completions cannot apply to a newer round; prior assessments stay historical/superseded. No timeout auto-finalization.

Final decision: actor, outcome, reason 1–2000 chars visible to owner, time, round/revision. One submitted category per report, no category edit operation. Approval creates immutable provisional award id/report/category/points/time: helmet=2, triple_riding=3, red_light=3. No award for rejection. Totals derive from award ledger. AI cannot finalize or change points/category.

## CT-04 — Operations, concurrency and replay

All mutations require UUID Idempotency-Key. Report mutations require If-Match `"r<revision>"`; missing 428 PRECONDITION_REQUIRED, mismatch 412. GET report ETag supports 304. Keys scoped principal+operation+resource, retained for demo, fingerprint normalized payload including expected revision. Exact authorized replay returns original status/body, even if resource later changed; changed payload 409 IDEMPOTENCY_KEY_REUSED; pending 409 OPERATION_PENDING with Retry-After 5. Durable mutation and replay outcome atomic; response loss cannot duplicate mutation.

| Operation | Body / success / special conflict |
|---|---|
| POST /evidence | Multipart exactly one file; 202 receipt CT-05 |
| GET /evidence/{id}/ingest | Owner/admin receipt `{id,operation_id,status:pending|ready|failed,reason,sha256,bytes}`; 200 |
| POST /reports | `{category,description,evidence_ids}`; 1–5 distinct ready owned unattached IDs; 201 report/Location; 409 EVIDENCE_NOT_READY or EVIDENCE_ALREADY_ATTACHED |
| GET /reports | Citizen own paged reports; optional state/category; 200 |
| GET /reports/{id} | Owner/admin report; 200/304 |
| GET /reports/{id}/timeline | Owner/admin paged events sequence/type/at/round/revision/actor_type/reason/data; citizen projection omits admin identities and operational internals |
| GET /reports/{id}/evidence/{evidence_id} | Owner/admin original attachment; 200; 409 EVIDENCE_NOT_READY, 503 integrity/storage failure |
| GET /awards | Citizen ledger collection plus total_points integer/provisional:true; empty total zero |
| POST /reports/{id}/clarifications/{request_id}/responses | Owner `{text?,evidence_ids?}` at least one nonempty; 200 report; 409 CLARIFICATION_CLOSED/INVALID_STATE |
| GET /admin/reports | Admin paged reports optional state/category; 200 |
| POST /admin/reports/{id}/clarifications | Reviewer `{prompt}`; 200 report; 409 CLARIFICATION_ALREADY_OPEN/REPORT_FINAL |
| POST /admin/reports/{id}/decisions | Reviewer `{outcome:approved|rejected,reason}`; 200 report; 409 REPORT_FINAL/INVALID_STATE/VALID_EVIDENCE_REQUIRED |
| POST /admin/reports/{id}/retries | Reviewer `{stage:media|ai,reason}`; 202 report; 409 NOT_RETRYABLE/REPORT_FINAL |
| POST /admin/reports/{id}/exports | Exporter `{}` with report If-Match; 202 `{id,status:pending,report_revision}` |
| GET /admin/exports/{id} | Exporter metadata status pending|ready|failed; 200 |
| GET /admin/exports/{id}/download | Exporter ZIP; 200; 409 EXPORT_NOT_READY/503 integrity failure |

Unknown IDs 404, malformed IDs 422, other common failures CT-01. Finalize only admin_review/needs_information, or human rejection from processing_failed. Report creation attaches ready media and durable stage intent atomically. Finalization serializes expected revision, unique final decision and unique award per report in one reporting transaction with timeline; concurrent loser 412, or REPORT_FINAL after refresh. Fresh keys cannot alter finality. Recovery creates new generation/attempt history, never removes prior failures/hash ownership. Only transient exhausted jobs recover, except disabled/budget-blocked AI may be explicitly requested after enabling; valid current evidence required. No automatic replay of manual-ready reports.

## CT-05 — Media, global hash ownership and export

25 MB is exactly 25,000,000 original bytes inclusive; zero invalid. Stream-count enforcement independent of Content-Length; crossing returns 413 FILE_TOO_LARGE. Multipart overhead allowance 65,536 bytes. Accept JPEG/JPG, PNG, MP4, QuickTime MOV, WEBM by signature/readable container; declared MIME if present must agree (image/jpeg,image/png,video/mp4,video/quicktime,video/webm). Extension informational; corrupt/unsupported/encrypted/external-resource/no decodable primary video/image content invalid. Support JPEG/PNG, H.264 MP4/MOV, VP8/VP9 WEBM; unsupported codec UNDECODABLE_MEDIA. Audio ignored. Original immutable; derivatives never define hash.

Video <=45 seconds exactly inclusive: rational maximum decoded video-frame presentation end minus minimum start, no floating rounding before eligibility. Unknown/nonfinite/negative/indeterminate duration INVALID_DURATION; >45 VIDEO_TOO_LONG. Display duration_ms ceiling(seconds×1000), eligibility exact rational. Decoder bounded to 60s wall, 512MiB, 4096×4096 pixels, one child, no network/shell; content resource-limit failure MEDIA_RESOURCE_LIMIT is terminal; infrastructure interruption transient.

Evidence receipt after durable staged bytes/reservation is 202 pending (201 ready if already finalized). Server computes SHA-256 from full original. Global unique hash includes all citizens/clarification, accepted unattached and rejected reports. Another operation on retained hash gets 409 DUPLICATE_EVIDENCE without original identity; pending reservation 409 EVIDENCE_INGEST_PENDING/Retry-After 5; same idempotent ingest resumes. Report/clarification attachment atomic, no partial subset.

Protocol: fsync generated quarantine bytes; reserve unique hash/immutable evidence ID tied to operation; verify hash; atomic same-filesystem rename/fsync directory; mark ready in media transaction. No report publication until ready. Filesystem/SQL are not atomic. Reconciler at most every 30s, reservation lease 120s renewable. After expiry first fence uploader; verified staged/final bytes complete ready, otherwise remove unreferenced bytes before releasing failed pre-acceptance reservation. Crash before reservation leaves orphan removed after 120s; crash after rename/before ready reconciles; crash after ready retains hash even if report never attached. Reconciliation outage retains reservation, degraded status; timeout alone never releases possible accepted ownership. Stale uploader cannot finalize. Oversize/rejected pre-acceptance intake releases only after reconciliation; technically invalid but already accepted original retains hash/bytes. Accepted hash/originals persist throughout staged demo, no deletion/automatic expiry; explicit stopped whole-dataset reset is operator-only, no production/legal retention policy implied. Disk-full fails closed.

Export captures consistent report revision/timeline/evidence references. ZIP: manifest.json (report/revision/round/time/evidence IDs/bytes/SHA-256), timeline.json through snapshot revision ordered sequence, originals/<evidence-id>.<canonical-extension>. Include retained originals from all rounds, including invalid originals, never derivatives substituted. Verify hash while building; mismatch fails export, no partial download. ZIP immutable/private; download rechecks export permission and audits actor/report/revision/result. Generated attachment name/nosniff, no Range support (416). No credentials/raw provider diagnostics in archive.

## CT-06 — Durable stage/retry contract

Version-1 command: message_id, kind media.screen|ai.review, schema_version=1, report_id, round, input_revision, recovery_generation, evidence_ids sorted immutable IDs, clarification_text nullable, policy_revision, correlation_id, created_at. Unique logical key `(kind,report_id,round,input_revision,recovery_generation)`; identical redelivery no new work; different payload same key quarantined MESSAGE_CONFLICT. Malformed/unsupported schema/missing source dead-lettered, not endlessly retried. Reporting intent atomic with business change; result owner persists result+outbox atomically; reporting inbox consumption+projection atomic. At least once delivery, not exactly-once provider execution.

Completion carries command identity plus result_id, attempt, fencing_token, outcome success|invalid|retryable_failure|terminal_failure|exhausted, result, reason_code, completed_at. Reporting checks current round/input revision/generation/expected stage against its stored active stage intent and verifies nonfinal status; input_revision identifies that intent's immutable inputs, not the latest mutable report projection revision, so progress updates do not invalidate their own completion. Stale/final completions recorded ignored STALE_COMPLETION, acknowledged, cannot overwrite. Apply once. Claims use increasing fencing token/owner/deadline; heartbeat/result/outbox conditional on current unexpired token. Lost lease discards result LEASE_LOST; stale worker cannot publish. Expired claim counts attempt; restart never resets count.

Defaults media/AI 3 total attempts, delays 5 then 20s plus uniform 0–2s jitter. Retry only connection failures, timeouts, 408/429/5xx, temporary infrastructure/storage/DB faults. Content invalidity, malformed response/message, configuration/auth 4xx terminal. Provider Retry-After bounded 1–120s can increase delay. Media and AI operation timeout 60s, lease 90s, heartbeat 15s. DB outage stops new claims; no local queue fallback. Completion delivery retries durably 5–30s without redoing completed stage. Media exhaustion processing_failed; AI terminal/exhausted/disabled/budget-blocked admin_review/manual with reason. AI failure never human rejection. Recovery CT-04 audited new generation/current policy, no infinite automated recovery.

## CT-07 — Gateway/advisory boundary

Private POST /internal/v1/assessments requires the CT-12 AI-review identity: azp traffic-ai-review, audience traffic-gateway and scope assessment:create together. Body: operation_id, report_id, round, input_revision, recovery_generation, evidence_refs, category, clarification_text, policy_revision. Same operation exact replay returns ledger outcome; changed payload 409, pending 409 OPERATION_PENDING. Only scoped private derivative references, no arbitrary URL. <=5 images, <=2048×2048 each, <=5,000,000 total bytes, text <=8000 chars; videos yield <=5 deterministic evenly spaced frames with original-hash provenance. No citizen identity/original filename sent.

One gateway operation_id UUID is persisted per durable logical command plus attempt number and remains stable for redelivery of that same attempt. A fresh eligible retry increments attempt and uses a new operation_id and reservation. An uncertain operation is never dispatched again; replay returns its uncertain ledger state (409 OPERATION_UNCERTAIN). A later eligible attempt may dispatch only within remaining allowance while the prior reservation remains outstanding. evidence_refs is a nonempty array of 1–5 objects `{evidence_id,derivative_id}` with UUIDs resolving to scoped immutable media objects; null/empty/duplicate references reject 422. Command evidence_ids likewise is a nonempty distinct UUID array; text-only clarification commands carry prior valid evidence IDs, never null. clarification_text alone may be null when absent.

Eligible configurable adapter openai-compatible-vision must support bounded multimodal billing, strict JSON and usage evidence. Operator pins exact allowlisted endpoint hostname/provider/model/version/adapter/pricing revision; floating model aliases ineligible. Actual provider/model eligibility validated before dispatch, no live selection call here. Response schema traffic-advisory.v1 exact fields: schema_version, suggested_category helmet|triple_riding|red_light|uncertain, confidence finite number 0..1, evidence_summary 1–2000 chars, limitations array <=10 strings 1–300 chars. Unknown/null fields invalid. No final decision/award field. Evidence instructions untrusted, never tools or system authority. Invalid response terminal AI_RESPONSE_INVALID/manual path.

200 response: operation_id,status available,assessment,provider/model/version/schema,usage,cost,price_revision,source live_provider. Missing provider usage explicit null/conservative liability. 503 AI_DISABLED/BUDGET_UNAVAILABLE/BUDGET_EXHAUSTED/AI_POLICY_UNAVAILABLE; 502 AI_RESPONSE_INVALID/PROVIDER_FAILED; 504 PROVIDER_TIMEOUT. Workers translate to CT-06, never report rejection. Gateway tracks attempts/latency/usage/reservations/cost/errors/correlation. Test-substitute explicit test/benchmark-only adapter returns same schema/source test_substitute, forbids credentials/provider egress, never silent fallback in demo. Provider-free tests/benchmark do not fulfill controlled real-provider acceptance. Manual path works while disabled/failing.

usage is null or `{input_units,output_units,unit_type}`: nonnegative integer counts and pinned adapter unit_type `tokens|billable_units`, never a guessed count. cost is `{currency,reserved_minor,settled_minor,accounting_status}`: CT-09 currency, nonnegative integer minor units, settled_minor nullable until verified settlement, accounting_status reserved|dispatching|settled|uncertain|released. An assessment can be available while cost remains uncertain if usage is absent; missing usage never releases liability. All other evidence arrays use [] rather than null when none exists; request arrays must meet each operation's stated nonempty bounds.

## CT-08 — Runtime controls

CT-13 resolves baseline initialization, management edge cases, exact actor/audit records and authenticated per-instance control health. Its specific rules supplement this section; settings, ranges, freshness and in-flight policy below remain unchanged.

Planning approval documentation and runtime publication are distinct. Runtime snapshots immutable `{schema_version:1,revision,effective_at,values,actor,reason,created_at}`; effective_at commit time, no scheduled publication. Secrets, points/media limits/category rules, provider eligibility and approval authority excluded. Initialization explicitly publishes validated baseline; missing snapshot blocks affected new work, no silent environment override.

Settings-admin with controls:write, as required by CT-02/CT-12 for read and publication, GET /admin/controls returns snapshot/ETag `"c<revision>"`; GET /admin/controls/audit paged old/new values/actor/reason/time. POST /admin/controls/publications body `{schema_version:1,reason,values}` is full replacement, requires controls:write, idempotency and controls If-Match. 201 complete snapshot; missing/unknown/null keys 422 INVALID_CONTROL, stale 412, DB unavailable 503. Atomic validated publish/audit, no partial patch/direct browser DB writes. Attempts and validation failures audited sans secrets.

| values field | Type/default/allowed inclusive range |
|---|---|
| media_max_attempts, ai_max_attempts | Integer 3; 1–5 total |
| retry_base_seconds, retry_max_seconds, retry_jitter_seconds | Integers 5,20,2; base 1–30, max base–120, jitter 0–2; exponential base×4^(failed attempt−1) capped at max |
| lease_seconds, heartbeat_seconds | Integers 90,15; lease 75–180, heartbeat 5–20; lease >=3×heartbeat and operation timeout+15 |
| media_timeout_seconds, ai_timeout_seconds | Integer 60; media 10–60, AI 5–60 |
| ai_max_concurrency | Integer 1; 1–4 globally across gateway replicas via durable slots |
| poll_interval_seconds, poll_jitter_seconds | Integers 10,2; interval 5–10, jitter 0–2 |
| ai_enabled | Boolean false; true only with CT-09 authority/eligible provider/private credentials |
| ai_budget | null initially or full CT-09 object |

Consumers fetch every <=5s, validate/swap full snapshot atomically; authenticated internal health exposes instance/revision/age/degraded reason. Ordinary last-known-valid settings usable <=60s since confirmed read, then new affected work stops with degraded 503. In-flight claims retain recorded ordinary policy; subsequent attempts use latest. No coordination lease renewal means stop committing. AI enablement/budget always fresh transactional reads/reservations before dispatch, never cached. Disable affects not-yet-dispatched requests immediately; in-flight may finish/account. Management DB outage rejects writes. No telemetry retention/alert values decided here.

## CT-09 — Budget authority, accounting and uncertainty

Initially ai_enabled=false/ai_budget=null: no live calls. Publishing configuration is not user spending approval. Future explicit user approval must specify currency/cap/period/provider scope in an approval artifact; main conversation records it, operator supplies private read-only authorization reference/digest. This draft supplies no authority. Runtime values cannot exceed it.

Budget exact object: authorization_ref (1–200 chars), currency uppercase ISO-4217, cap_minor integer 0..9,000,000,000,000, period_start/end UTC, provider_id/model_id/model_version/price_revision exact pinned strings. Fixed half-open [start,end), end>start; no auto-renew/rolling reset. Monetary arithmetic exact integer minor units using pinned currency exponent; rational price calculations rounded upward once to minor units. Null/missing/invalid/expired budget blocks. Zero cap permits no positive liability.

Before dispatch shared ledger transaction validates fresh authority/policy/current period/eligibility, obtains global concurrency slot, and reserves enforceable worst-case total: settled+outstanding_reserved+new_reservation <=cap. Include bounded billed input/image expansion/output/request fees and applicable billing currency/taxes; no guessed FX. Adapter must establish finite provider-enforceable bound from pinned contractual prices/request controls. Unknown/unbounded billing disables even with credentials/cap. SDK automatic retries disabled; each possible charged new attempt reserves separately unless verified provider idempotency proves single charge. Cap covers gateway-authorized calls, not unrelated out-of-band account usage.

Operation ledger states reserved|dispatching|settled|uncertain|released. Reserve durably before dispatch; mark dispatching before send. Crash with provable no dispatch may release reserved liability; crash after dispatching (even before send), timeout/cancel/lost response/missing usage retains full uncertain reservation. Never free uncertainty by expiry/period reset. Late result settles once by operation/provider identity; verified zero charge releases. Accounting corrections require settings-admin audited evidence, not arbitrary reset. Actual liability exceeding proven reservation halts dispatch/raises accounting fault. Cap reduction below settled+reserved 409 BUDGET_LIABILITY_CONFLICT. Existing liabilities retain original period/pricing; replacement authorization cannot count unresolved aggregate allowance twice, no overlapping budgets for same authorized provider-account scope. Manual report path never waits for ledger reconciliation.

## CT-10 — Polling and local configuration

Active browser polls report every 10s plus 0–2s jitter, one in flight, <=5s request timeout, immediate focus/reconnect refresh. ETag reads committed primary state, no stale replica cache. Persisted change→render <=30s under healthy connectivity/agreed workload including poll/server/render, verified end-to-end. Failed polls show last-success time/stale connectivity disclosure; hidden/offline pages no freshness claim. 401 login; 403/404 stop inaccessible polling; 429/503 respect Retry-After and disclose degraded state. Disabled AI explicitly says no live assessment/manual review. No SSE requirement.

Approved local Compose topology remains proxy+two reporting/media-worker/AI-worker/gateway instances, Keycloak, PostgreSQL, private media/shared volume and local telemetry; no sticky sessions/cloud/public hosting. Startup validates deployment inputs; secrets injected via private files, never runtime table. APP_PROFILE local|test|benchmark; INSTANCE_ID UUID; SERVICE_ROLE reporting|media-worker|ai-worker|gateway|completion-worker. Configuration names/shapes:

| Name | Shape |
|---|---|
| PUBLIC_ORIGIN, OIDC_ISSUER, OIDC_WEB_CLIENT_ID | Exact CT-01 HTTPS origins/issuer; traffic-web |
| OIDC_AUDIENCE, OIDC_SERVICE_CLIENT_ID, OIDC_CLIENT_SECRET_FILE | Fixed CT-02/CT-12 role mapping; absolute private secret file |
| DATABASE_DSN_FILE, KEYCLOAK_DATABASE_DSN_FILE | Absolute private files containing PostgreSQL role-specific connection URI |
| MEDIA_ROOT | Absolute private shared-volume directory, quarantine/final same filesystem |
| TLS_CERT_FILE, TLS_KEY_FILE, TRUST_CA_FILE | Absolute local trusted TLS files; verification never disabled |
| KEYCLOAK_ADMIN_SECRET_FILE | Private bootstrap/admin secret file, not application control |
| GATEWAY_ORIGIN, MEDIA_INTERNAL_ORIGIN | Fixed private HTTPS allowlisted service origins |
| AI_ADAPTER | disabled|openai-compatible-vision|test-substitute; substitute only test/benchmark, live prohibited there |
| AI_PROVIDER_CONFIG_FILE | Private JSON provider_id, endpoint HTTPS allowlist, model_id/version, adapter_version, price_revision, response_schema, positive integer input/output billed-unit bounds, exact rational currency price_schedule; gateway only |
| AI_PROVIDER_SECRET_FILE, AI_SPEND_AUTHORIZATION_FILE | Absolute private credential/approval files; missing live disabled; authorization names approved artifact/digest and maximum CT-09 scope |
| OTEL_EXPORTER_OTLP_ENDPOINT, LOG_LEVEL | Local collector URL; debug|info|warning|error default info, secrets/tokens/media always redacted |
| TEST_SUBSTITUTE_PROFILE_FILE | Test/benchmark JSON latency_ms integer 0..60000, fail_first_attempts 0..5, outcome valid|invalid_schema|timeout|provider_error; deterministic by operation ID |

No env flag bypasses spending checks. Provider/price rotation needs eligibility/policy validation preserving history. Secrets rotate by restarting affected processes; no public snapshot contains them. Disabled optional AI alone does not fail reporting readiness. Shared local failure domains, synthetic capacity evidence and growth estimates remain AP limitations, not SLA/retention promises.

## CT-11 — Traceability and consistency self-check

| Checked approved question | Resolution |
|---|---|
| IB-R01/R11/R16, AP-D01–05: staged/local and capacity scope preserved? | CT-10 profiles/topology; no new production/SLA, benchmark/growth inputs unchanged |
| IB-R02/R06/R13/R14/R15: visible failure, all clarification forms, final human decision and points? | CT-03 lifecycle/awards; CT-04 operations/atomic finality |
| IB-R03/R04/R08: restart, duplicate delivery, stale lease/round, bounded recovery? | CT-06 keys/fencing/retries/outbox/inbox; CT-05 reconciliation |
| IB-R05/R17: global clarification hashes and exact boundaries? | CT-05 bytes/rational duration/reservations/retention and owner-safe errors |
| IB-R07: auth/key outage/private authorization? | CT-02 Keycloak/scopes/ownership/JWKS, CT-10 private config |
| IB-R09: freshness includes render/outage disclosure? | CT-10 timing; CT-08 bounded poll controls |
| IB-R10: observability without stealing deferred decisions? | CT-01 correlation, CT-06 attempts, CT-07 ledger, CT-08 audit; alert/retention remain deferred |
| IB-R18: original/hash/consistent ZIP and authorization? | CT-05 manifest/snapshot/integrity and CT-04 export permission |
| IB-R19/AP-D04: substitute vs real evidence and zero-spend? | CT-07 explicit adapter/source, CT-09 null budget/fail-closed |
| IB-R20/AP-D06: types/defaults/access/version/audit/propagation/outage/in-flight? | CT-08 complete snapshots/control table; CT-09 fresh safety; CT-10 secrets excluded |
| DP-M01: parsing/null/unknown/empty/access/concurrency/errors testable? | CT-01 shared rules apply CT-04/07/08; CT-03 null responses; endpoint table states success/conflicts |
| IB-R12: gates preserved? | Awaiting review; only this artifact, no approval/Plan/source/test/config/deployment/live call |

Final consistency pass compared human finality CT-03/04/06 to IB-R13; no AI decision authority. Compared CT-05 hash release to IB-R05/AP recovery: accepted identity never released. Compared CT-08 cached ordinary controls with CT-09 fresh dispatch: no cached authorization. Compared CT-06 retries and CT-09 liabilities: redelivery never silently repeats charged work. Compared null budget to AP-D04: no live spending authorized. Compared topology with AP-D01/02: no broker/cloud/config service added. No material approved-artifact contradiction found. CT decisions were approved by user on 2026-10-24.


## CT-12 — Approved identity-profile clarifications (Q29/Q30)

User-approved on 2026-10-26. Source: Identity-Contract-Clarifications.md Q29/Q30. This section supplies the exact identity representation and fixed client/scope vocabulary for CT-02/07/08/10. It resolves their shorthand where needed without adding routes or granting business authority. The normative choices below are copied from the reviewed addendum; labels such as proposed describe their original presentation and are superseded by recorded approval.

### CT-12.1 — `/me` and human claim mapping

The following exact additions to CT-02 were approved.

`GET /api/v1/me` is a human operation, returning 200 JSON with exactly three required, non-null fields; no additional fields:

```json
{
  "subject": "35a26b15-0ae4-4caf-ad87-d97a664b17e3",
  "roles": ["citizen", "admin"],
  "permissions": ["citizen:own", "reports:read:any", "review:write"]
}
```

The example represents `realm_access.roles` containing `citizen`, `admin`, `review:write`; it does **not** imply that admin grants review permission. `subject` is the exact validated JWT `sub` string (nonempty, no normalization; not constrained to UUID). Ownership remains the exact `(iss, sub)` pair from CT-01; issuer is fixed and is not an additional response field. No username, email or Keycloak profile is returned.

| Response field | Exact schema and computation proposed |
|---|---|
| subject | Nonempty JSON string, exact `sub` |
| roles | Unique JSON string array; subset of `citizen`, `admin`, `settings-admin`, in that fixed order; only base roles present in `realm_access.roles` |
| permissions | Unique JSON string array; subset of the six literals in the table below, in table order; computed from conjunctions below, never copied from an untrusted request or arbitrary JWT permission field |

| Ordered effective permission literal | Required realm roles | Meaning already bounded by the contract |
|---|---|---|
| citizen:own | citizen | Own reporting/evidence/clarification/history and awards operations in CT-02/04 |
| reports:read:any | admin | Admin report/private evidence reads in CT-02/04 |
| review:write | admin **and** review:write | Clarification request, decision and authorized recovery |
| evidence:export | admin **and** evidence:export | Create/read/download ZIP |
| controls:read | settings-admin **and** controls:write | CT-08 GET controls and audit, preserving CT-02's combined grant requirement |
| controls:write | settings-admin **and** controls:write | CT-08 publication |

These literals describe existing powers only; `citizen:own`, `reports:read:any` and `controls:read` are proposed output vocabulary, not new realm roles. `review:write`, `evidence:export`, `controls:write` remain separately granted realm roles. CT-08's settings-admin shorthand is interpreted consistently with CT-02's combined settings-admin/control-write requirement: both grants are required for reading controls/audit and for publication. No read-only authority is added to a bare settings-admin role.

Recognize roles only from `realm_access.roles`; never from `resource_access`, a generic `roles`/`permissions` claim, `scope`, username or groups. Unknown role strings (including Keycloak defaults) are ignored; duplicate role strings collapse. Missing `realm_access` or missing `roles` means no recognized roles. Present `realm_access` must be an object, and present `roles` an array of strings; null/wrong types invalidate authentication (401). Base roles combine by union; permission-like roles without their matching base role confer nothing. An authenticated human with no recognized roles gets 200 `/me` with `roles:[]`, `permissions:[]`; protected business operations deny 403. Admin alone cannot review/export; citizen+admin has both base powers but self-review/finalization/export still denies 403 `SELF_REVIEW_FORBIDDEN`. No base role implies another.

#### Minimum token claim contract for both questions

These are explicit application token-profile choices, not assertions about every default Keycloak token. Signature/issuer/RS256/audiences, <=30-second skew, <=5-minute access lifetime, key refresh/cache/coalescing/outage behavior and CT-01 authentication errors remain unchanged.

- Require JOSE `alg="RS256"`, nonempty string `kid`; if JOSE `typ` is present it must be `JWT`. Require payload `typ="Bearer"` as the access-token discriminator; missing/other payload type, including `ID`, denies 401. An ID token never becomes acceptable merely by having an audience or valid signature.
- Require `iss`, `sub`, `azp` as nonempty strings; `iss` exactly CT-01 issuer. Require `exp` and `iat` as integer NumericDate seconds (JSON booleans are not integers). Require `exp>iat`, `exp-iat<=300`; validate expiry and future issuance with the existing <=30-second skew.
- `nbf` is optional; if present require integer NumericDate and validate with that skew. Absence does not fail validation. This clarifies CT-02's `nbf` validation without requiring an optional claim to exist.
- Require `aud` as a nonempty string or nonempty array of nonempty strings containing the receiver's fixed audience. Arrays must contain no duplicates. Other audience values confer no additional access. Validate receiver audience and allowed `azp` independently.
- Human tokens require `azp="traffic-web"` and reporting audience `traffic-api`. They cannot authorize any service operation even when given service-looking scopes or extra audiences. Human `scope` is not a source of application permissions; if present it must be a string. Unused standard claims are ignored and confer no authority.
- Service tokens require the fixed `azp`/audience/scope mapping in Q30. Service identity is classified by this configured client allowlist, never by a `service-account-` username, role presence or arbitrary `sub` prefix. `sub` remains required for audit identity; neither caller-supplied nor dynamically discovered client identities are accepted.

Missing/malformed/invalid authentication claims, unknown `azp`, wrong receiver audience or token type use 401 `UNAUTHENTICATED`; valid authenticated principal of the wrong human/service class or lacking a required permission/scope uses 403 `FORBIDDEN`. For this distinction, authentication recognizes only the globally fixed client IDs in Q30 plus traffic-web and validates the receiving boundary's audience. Authorization then requires an allowed client/receiver/operation row: a recognized client presenting a valid receiver-audience token but lacking that row is denied 403, even if it copies another client's scope. This does not permit dynamic client IDs or grant authority from an audience alone. CT-01 error envelope, cache headers and request IDs apply. Existing JWKS-unavailable cases remain 503, not converted to 401.

### CT-12.2 — fixed service identities and scope matrix

These literal client IDs and scopes are the approved CT-02 responsibility mapping, including CT-07 `assessment:create`. Each is a confidential client with client-credentials enabled, browser/interactive grants disabled and private injected secret per CT-10. Replicas of the same role use the same configured client ID. No gateway outbound OIDC client is needed: provider credentials remain solely gateway-owned under the existing CT-07/09 rules.

| Caller / fixed `azp` = configured client ID | Receiver audience | Exact allowed application scopes | Existing CT-02 responsibility |
|---|---|---|---|
| reporting / traffic-reporting | traffic-media | media:ingest media:read media:export | Ingest, authorized private read, export assembly |
| media worker / traffic-media-worker | traffic-media | media:original | Read originals for screening |
| AI review / traffic-ai-review | traffic-media | media:derivative | Read scoped derivatives only |
| AI review / traffic-ai-review | traffic-gateway | assessment:create | CT-07 POST /internal/v1/assessments |
| reporting completion consumer / traffic-completion | traffic-api | completion:consume | CT-06 completion boundary |
| reporting / traffic-reporting | traffic-api | controls:health | CT-13 GET /internal/v1/controls/health only |
| reporting / traffic-reporting | traffic-media | controls:health | CT-13 GET /internal/v1/controls/health only |
| reporting / traffic-reporting | traffic-gateway | controls:health | CT-13 GET /internal/v1/controls/health only |

The client allowlist is exactly the table plus human `traffic-web`; no arbitrary configured string becomes authorized. Receiver audience configuration is `traffic-api` for reporting/completion reception and AI-worker diagnostic health, `traffic-media` for media reception, `traffic-gateway` for gateway reception. Outbound `OIDC_SERVICE_CLIENT_ID` is `traffic-reporting`, `traffic-media-worker`, `traffic-ai-review`, or `traffic-completion` for the respective role; no outbound client secret is assigned to gateway. Audience is the receiving boundary, not the caller's name. These are CT-10 mappings; provisioning/configuration changes require later milestone review. The CT-13 health rows add no client identity or business-operation power.

Service `scope` is required as a string of distinct, case-sensitive ASCII-space-separated scope tokens (no leading/trailing/repeated spaces); an empty string is valid authentication but authorizes no service operation. Only a scope listed for that exact client/receiver pair grants access; unrelated scopes are ignored and never expand the allowlist. Each operation requires its row's applicable scope in addition to the client/audience checks; the three reporting media scopes authorize only their corresponding ingest/read/export purpose, not one another. A token may carry multiple listed scopes/audiences, but each receiver independently applies only its own row. Gateway assessment creation requires `azp=traffic-ai-review`, audience `traffic-gateway`, and `assessment:create` together. No other service client acquires this power through a copied scope.

Service clients receive no human realm role grants; even an accidentally role-bearing service token cannot call `/me`, citizen/admin/control-management operations (403). Human clients cannot call media/assessment/completion/control-health service operations (403 after valid authentication for that receiver); a human token with wrong receiver audience first fails authentication (401). Service private-media access also requires the already-approved <=60-second caller/evidence/report/round/purpose capability and current authorization; a scope never replaces it. No new media/completion routes or message transport are defined here, and no service may finalize reports, grant awards, manage roles, publish controls or bypass ownership.

Identity consistency check: the exact response, claim mapping and original client matrix match the approved identity addendum, with the approved CT-13 health-only extension; settings read/publication retain the combined grants; unknown clients fail authentication, known but unauthorized class/pair/scope fails authorization. Hosted CI remains deferred by Q28. No test or implementation is approved by this contract amendment.

## CT-13 — Runtime controls clarification

Q31–Q34 approved by user on 2026-10-30 in Controls-Contract-Clarifications.md and Controls-Service-Audit-Actor-Clarification.md. This is the normative incorporated delta; no executable or spending authority follows from contract approval.

### CT-13.1 — Explicit baseline and management behavior

Use an operator-only initialization command, with its exact executable interface reviewed in the GREEN Implementation Plan. It uses the private configuration-database role, validates the complete CT-08 defaults, and atomically creates revision 1 plus its publication audit entry. Baseline has `ai_enabled=false`, `ai_budget=null`, schema_version 1 and no spending authority. No application startup, GET, consumer fallback or environment override implicitly publishes it. There is no public initialization endpoint or `c0` bootstrap convention.

Initialization requires a reason. Repeating initialization against an initialized store returns the current snapshot without overwriting it, advancing revision or duplicating the initial publication audit. A concurrent initializer creates only one baseline. Ordinary HTTP publication still requires the existing positive-revision `If-Match: "c<revision>"` and Idempotency-Key. A new authorized publication with identical values and a fresh key/current precondition creates a new revision; an exact authorized idempotent replay returns the original snapshot without another publication.

Management reads use the current primary-store snapshot. Missing baseline returns 503 `CONTROLS_UNAVAILABLE`; database/audit-store failure returns 503 `DEPENDENCY_UNAVAILABLE`. Both use the CT-01 envelope, retryable=true and Retry-After 5. Missing required precondition or idempotency key returns 428 `PRECONDITION_REQUIRED`; malformed controls ETag or UUID key returns 422 `VALIDATION_FAILED`; stale valid ETag returns 412 `REVISION_CONFLICT`. CT-08 payload validation remains 422 `INVALID_CONTROL`, including an attempt to enable AI without the required authority/eligibility/private credentials. The explicitly nullable `ai_budget` remains an exception to general null rejection.

Publication reason is trimmed plain text of 1–2000 characters; other missing, null, unknown or invalid publication fields retain CT-08 validation. Snapshot `created_at` and `effective_at` are the same committed publication timestamp, in the existing UTC millisecond representation. Revision is a positive integer; publication does not schedule future activation.

### CT-13.2 — Actor and audit representation, replay and failure handling

Snapshot actor is exactly:

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

| Field | Representation |
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

### CT-13.3 — Per-instance control health and least-privilege caller

Define `GET /internal/v1/controls/health` on the existing application role processes. This adds no service, public management permission or business handler. It returns exactly:

```json
{"instance_id":"uuid","service_role":"reporting","revision":1,"age_ms":0,"degraded_reason":null}
```

service_role uses the existing five-role enum. revision is the last validated positive revision or null before any valid snapshot; age_ms is the nonnegative integer age since the last confirmed valid read, or null with no valid snapshot. degraded_reason is null, `missing_snapshot`, `invalid_snapshot`, `store_unavailable` or `stale_snapshot`. A failed or invalid read does not reset the confirmed-read age. A successful read resets it even if the revision is unchanged. Once age exceeds 60,000ms, stale_snapshot takes precedence. Existing CT-08 rules still determine whether affected new work may proceed; health metadata itself grants no work or spend authority.

An authorized health read returns 200 even when its metadata reports degradation; CT-01 authentication/authorization/dependency error envelopes still apply to request failures. Foundation readiness remains unchanged and independent of controls.

Extend the CT-12 matrix only for the existing confidential `traffic-reporting` client: add scope `controls:health` for receiving audiences `traffic-api`, `traffic-media` and `traffic-gateway`, solely for this GET operation. This permits diagnostic reads from reporting/completion/AI roles using traffic-api, media roles using traffic-media, and gateway roles using traffic-gateway. It grants no controls publication, human operation, media access or assessment dispatch. Other service clients and human principals cannot use this operation. Existing fixed-client classification, canonical service scope grammar and receiver-audience checks remain; invalid authentication is 401 and an authenticated wrong caller/scope is 403.

### CT-13.4 — Preserved boundaries

No live AI spending is authorized. Positive budget/accounting tests may use clearly labeled synthetic authority and provider-free test inputs; those fixtures never become production spending authority. DP-M06 owns independent control/ledger safety and uncertain-liability behavior already assigned by the Plan; DP-M12 later integrates provider workflows with those capabilities. No concern is reassigned and no real provider call is required here.

All existing settings/ranges, five-second consumer refresh rule, sixty-second ordinary stale allowance, fresh transactional AI authorization/reservation, immutable in-flight ordinary policy, identity grants and pagination remain unchanged. Concrete internal Python seams, SQL schema, migrations and command implementation belong to subsequent reviewed Implementation Plans.
