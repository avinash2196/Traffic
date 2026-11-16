# Requirements — initial-build

## Goal

Build a controlled traffic-evidence reporting demo in which citizens upload evidence, AI reviews it, an admin reviews it, and citizens see failures, rejection/approval, and awards. Design for future real use with one million registered users. [User: Q7, Q17, Q18]

## Status

Approved by user on 2026-10-24, including the control-table revision, through the instruction to go ahead with next steps. Approval of requirements does not approve the proposed Q24–Q26 control values. Contracts, Implementation Plans, tests, and production code retain their separate PDD review gates. On 2026-10-26 the user explicitly approved local Git initialization and deferral of hosted CI (Q28); the CI-specific changes below record that decision.

## Sources

- User brief: architecture discussion and instruction to record the agreed architecture and follow PDD step by step.
- Q1–Q9: first requirements-review questions and the user's numbered answers.
- Q10–Q15: scope and scale resolved by Q17–Q18; Q12–Q15 explicitly answered in the latest clarification round.
- Q16–Q18: work-item name, controlled-demo scope, and meaning of one million; explicitly answered by the user.
- Q19–Q23: user accepted the recommended choices and proposed deferrals. New operational recommendations are labeled proposed below rather than attributed as explicit user statements.
- Repository citations describe documentation, not verified running behavior.
- Q27: user explicitly selected both the planning/approval table and database-backed runtime configuration.

## Repository-Confirmed Facts

- At capture time, the repository contained only README.md; no application source, dependency manifest, or tests were present. The README references those missing artifacts. [Repo: README.md:7, README.md:13, README.md:14, README.md:87]
- The README describes a local demo with optional advisory AI, provisional points, a modular monolith, SQLite/local media, and in-process background tasks. Its implementation claims cannot be verified from this checkout. [Repo: README.md:49, README.md:53, README.md:59, README.md:91, README.md:94]
- No product-level docs/requirements.md exists in this checkout. The README is the documentary baseline. [Repo: README.md:1]

## Requirements

| ID | Requirement | Source |
|---|---|---|
| IB-R01 | Deliver a controlled demo, designed to scale toward real use; real production rollout is not established by this requirement. | User: Q17 |
| IB-R02 | Support citizen evidence upload, AI review, subsequent admin review, and citizen-visible outcomes including processing failure, rejection, approval, and awards. | User: Q7 |
| IB-R03 | Support multiple running instances. | User: Q2 |
| IB-R04 | Retry failed screening work. After AI retries are exhausted, allow manual admin review. Define bounded retry limits, eligible failures, and recovery behavior in the CONTRACT milestone. | User: Q3, Q14, Q21 |
| IB-R05 | Reject identical evidence uploads across all citizens, including reuse in clarification uploads. | User: Q5, Q13 |
| IB-R06 | Allow both text clarification and additional evidence in response to an information request. | User: Q6 |
| IB-R07 | Provide a separate authentication boundary and separate AI gateway for centralized access and AI-call tracking. | User: brief |
| IB-R08 | Separate reporting, media screening, and AI review responsibilities; use durable worker handoffs and private media storage. Keep report decisions and awards within the reporting boundary. | User: brief, acceptance of discussed architecture |
| IB-R09 | Use HTTPS APIs and initially periodic polling for status; SSE is a possible later option, not an initial delivery requirement. For an active page with healthy connectivity, expose a persisted status change within 30 seconds. | User: brief, Q20 acceptance of recommended 15–30-second freshness |
| IB-R10 | Provide observability across reporting, media processing, AI review, and admin decisions, including correlation across components and AI usage/error tracking. Define alert thresholds and telemetry retention during the observability milestone's Implementation Plan review. | User: Q9, Q22; User: brief |
| IB-R11 | Design account capacity for one million registered users. This does not define concurrent connections, daily activity, or submission throughput. | User: Q18 |
| IB-R12 | Follow PDD with reviewed requirements, Plan, external contract, individually reviewed milestone Implementation Plans, RED/GREEN delivery for behavior, and final review. Persist decisions and verification in work-item artifacts. | User: brief, request to use PDD |
| IB-R13 | Admin approval/rejection decisions are final. Concurrent review must produce only one final decision and at most one award for an approved report. | User: Q12 |
| IB-R14 | Awards are provisional demo points: 2 for helmet violations and 3 for triple riding or red-light violations. | User: Q15, Q23 acceptance of recommended README rates; Repo: README.md:39 |
| IB-R15 | AI assessments are advisory; the human admin makes the final review decision. | User: Q23 |
| IB-R16 | Use staged evidence for the controlled demo; do not integrate with official government/enforcement systems. | User: Q23 acceptance of recommended baseline |
| IB-R17 | Accept JPG, PNG, MP4, MOV, and WEBM, with a 25 MB per-file limit and 45-second video limit. Define exact byte/time boundary semantics in CONTRACT. | User: Q23; Repo: README.md:45 |
| IB-R18 | Allow authorized admins to export original evidence, its SHA-256 hash, and the report timeline in a ZIP. | User: Q23; Repo: README.md:39 |
| IB-R19 | Local automated tests must run without a live AI provider using a clearly identified test substitute; the demo AI integration remains a real provider integration. Keep the provider-free CI workflow for future use. Hosted CI execution is deferred until GitHub publishing and does not gate Foundation completion or subsequent local PDD work. When activated, CI must also run without live AI. | User: Q21, Q28 |
| IB-R20 | Maintain both a planning/approval control table and a database-backed control table that services read for runtime configuration. The planning table tracks decisions, proposals, and approval state; runtime controls manage operational settings. Selection of runtime-editable settings and their management/consumption behavior requires contract review. | User: control-table request, Q27 |

## Local Source Control and CI Decision

Use a local Git repository for this controlled demo. Hosted CI execution is deferred until GitHub publishing; retain its workflow definition. Local verification remains mandatory, and deferred hosted CI must not be reported as successful execution. This explicitly supersedes the original Foundation hosted-execution gate. Publishing, creating a remote, and committing are not authorized by initialization alone. [User: Q28, 2026-10-26]

## Operational Characteristics

| Characteristic | Answer | Source |
|---|---|---|
| Scale | One million registered users. Workload sizing, upload volume, growth horizon, and associated capacity evidence are deferred to architecture review within Plan preparation. No throughput is inferred from account count. | User: Q18, Q19 acceptance of offered deferral |
| Deployment | Multiple instances; controlled demo now, scalable toward real use. Hosting target and demo budget are to be decided in the same architecture review before infrastructure planning. | User: Q2, Q17, Q19; proposed review placement |
| Availability and latency | Active-page status freshness: at most 30 seconds under healthy connectivity. Production uptime SLA, other numeric latency targets, and zero-downtime deployment are not required for this controlled-demo work item. | User: Q20; interpretation confirmed by requirements approval on 2026-10-24 |
| Consistency and concurrency | Final admin decisions; concurrent review produces one final decision and at most one award for an approved report. | User: Q12 |
| Dependency failure | Retry screening; allow manual admin review after AI retry exhaustion. CONTRACT defines bounded retry/error behavior. Local automated tests/CI run without a live provider. | User: Q3, Q14, Q21 |
| Observability | Correlation, queue/processing failures and backlog, AI latency/usage/cost/errors, admin/award visibility. Alert thresholds and retention are decided in the observability milestone's Implementation Plan. | User: Q9, Q22; User: brief |

## Decisions Deferred to Later Milestones

### Architecture Control Table

This planning table tracks current decisions and proposals. A separate database-backed runtime control table is also required by IB-R20; its implementation has not started. Approval tracking does not itself publish a runtime setting. [User: control-table request, Q27]

| Control | Approved value | Proposal / pending decision | Status | Decision owner |
|---|---|---|---|---|
| Registered-account capacity | 1,000,000 | Benchmark dataset uses synthetic accounts | Capacity approved; dataset proposal pending | Architecture review (Q24) |
| Concurrent active users | Not set | 100 | Proposed | Architecture review (Q24) |
| Submission rate | Not set | 10 per minute | Proposed | Architecture review (Q24) |
| Benchmark duration | Not set | 30 minutes | Proposed | Architecture review (Q24) |
| Hosting | Multiple instances required | Local multi-instance demo with portable deployment configuration | Proposed | Architecture review (Q25) |
| Paid hosting budget | Not set | No paid hosting initially | Proposed, not spending authorization | User (Q26) |
| Live AI budget | Not set | User supplies currency, spending cap, and accounting period | Awaiting value; no spending authorization | User (Q26) |
| Active-page status freshness | At most 30 seconds with healthy connectivity | No change | Approved (Q20 and requirements approval) | Requirements |
| Retry policy | Bounded retries; manual review after AI exhaustion | Limits, eligible failures, and recovery behavior | Deferred | CONTRACT (Q21) |
| Alert thresholds | Not set | Determine with observability design | Deferred | Observability Implementation Plan (Q22) |
| Telemetry retention | Not set | Determine with observability design | Deferred | Observability Implementation Plan (Q22) |
| Source control / hosted CI | Local Git; keep CI workflow | Activate hosted CI when publishing to GitHub | Hosted execution deferred; local checks required | User Q28 |

Proposed benchmark numbers describe synthetic test traffic, not proven capacity. Planning controls such as benchmark duration and hosting choice are distinct from possible runtime controls such as retry limits and AI spend limits. The requirement for runtime storage is confirmed; no particular schema, admin editing interface, propagation semantics, or unapproved control value is established by this table.

- Architecture review during Plan preparation: workload sizing, media volume/growth horizon, capacity-evidence scope, hosting target, and demo budget. These must be reviewed before Plan approval; registration capacity is not a claim about traffic capacity. [User: Q19; proposed review placement]
- CONTRACT, first milestone after Plan approval: bounded retry policy, eligible failures, exhaustion/recovery contract, and precise media-limit semantics. [User: Q21, Q23]
- Runtime control CONTRACT decisions for review: which settings services consume; management permissions and interface; validation and allowed ranges; defaults/missing values; versioning and concurrent edits; audit history; update visibility across instances; database/cache outage behavior; whether changes affect in-flight jobs; and spend accounting period/enforcement semantics if AI budgets are runtime controls. These are design questions, not newly confirmed product requirements. No separate configuration service is implied by the table requirement. [User: Q27; proposed contract decision ownership]
- Observability milestone Implementation Plan: alert thresholds and telemetry retention. Plan must assign ownership of this decision. [User: Q22]

## Explicit Exclusions

AI must not make the final review decision; that decision belongs to the human admin. [User: Q23]

No official government/enforcement integration or real redeemable rewards in this controlled demo. [User: Q15, Q23]

## Non-Blocking Decisions

- Choice of fresh role agents for artifact-driven steps, rather than requiring new sidebar chats, is a workflow mechanism. Requirements clarification stays in the main conversation. [Left to PDD execution — non-blocking]

## Acceptance Criteria

| ID | Criterion | Requirement |
|---|---|---|
| IB-AC01 | Demonstrate citizen upload through AI review and admin decision, showing the resulting status/reason and applicable award to that citizen. | IB-R01, IB-R02 |
| IB-AC02 | Demonstrate processing across multiple instances, with a screening failure retried according to the subsequently agreed policy. | IB-R03, IB-R04 |
| IB-AC03 | Identical evidence is rejected for the same citizen, a different citizen, and a clarification upload. | IB-R05 |
| IB-AC04 | A citizen can respond to a clarification request using text, additional evidence, or both. | IB-R06 |
| IB-AC05 | Authentication and AI gateway have distinct responsibilities; AI calls pass through the gateway and expose correlated usage and error telemetry. | IB-R07, IB-R10 |
| IB-AC06 | Reporting, media screening, and AI review interact through the agreed boundaries, with durable handoffs and private evidence access. | IB-R08 |
| IB-AC07 | An active citizen page with healthy connectivity displays a persisted status change through HTTPS polling within 30 seconds. | IB-R09 |
| IB-AC08 | Capacity evidence addresses one million registered accounts and the workload established in architecture review; no throughput claim is accepted from account count alone. | IB-R11 |
| IB-AC09 | Delivery records reviewed artifacts, milestone approvals, RED/GREEN evidence where applicable, and final review under this work item. | IB-R12 |
| IB-AC10 | Concurrent conflicting admin decisions result in one final decision; an approved report receives one award, with no duplicate award on repeated requests. Final approval/rejection cannot be changed. | IB-R13 |
| IB-AC11 | Approval grants 2 provisional demo points for helmet violations and 3 for triple riding or red-light violations, displayed to the citizen. | IB-R14 |
| IB-AC12 | AI findings do not finalize approval/rejection; the admin decides. A report remains eligible for manual admin review after AI retries are exhausted. | IB-R04, IB-R15 |
| IB-AC13 | Demonstration evidence is staged; no official enforcement action or government integration occurs. | IB-R16 |
| IB-AC14 | Supported formats within the approved limits are accepted; unsupported formats and files/videos exceeding the CONTRACT-defined limits are rejected. | IB-R17 |
| IB-AC15 | An authorized admin exports a ZIP with original evidence, matching SHA-256 hash, and report timeline; unauthorized access is denied. | IB-R18 |
| IB-AC16 | Local automated tests complete using a test AI substitute without provider credentials or external AI calls. The retained CI workflow uses the same provider-free checks; actual hosted execution is deferred by Q28, not claimed as passed. | IB-R19 |
| IB-AC17 | Planning decisions and proposals are tracked with approval status; services read their applicable operational settings from database-backed runtime controls. Management, validation, and multi-instance behavior conform to the subsequently reviewed control contract. | IB-R20 |

Criteria with explicitly deferred details are completed against the reviewed architecture, CONTRACT, or Implementation Plan that owns those details.

## Clarification Log

| Q | Question | Answer |
|---|---|---|
| 1 | Local demo or real pilot? | Initial yes ambiguous; resolved by Q17. |
| 2 | One instance or multiple? | Support multiple. |
| 3 | Screening failure/restart behavior? | Retry; detailed bounded policy assigned to CONTRACT by Q21. |
| 4 | Final decisions and concurrent reviewer/award behavior? | Yes; confirmed by Q12. |
| 5 | How should identical uploads behave? | Reject identical; global and clarification scope confirmed by Q13. |
| 6 | Text-only clarification or additional evidence? | Allow both. |
| 7 | What defines completion? | Upload, AI review, admin review, visible rejected/failed outcomes, and awards. |
| 8 | Scale, latency, downtime targets? | Registered users resolved by Q18; Q19–Q20 record sizing deferral and recommended operational targets for review. |
| 9 | Required production visibility? | Ensure observability is correct; architecture discussion elaborated signals. |
| 10 | Controlled demo or real pilot? | Resolved by Q17. |
| 11 | Meaning of one million? | Resolved by Q18. |
| 12 | Are decisions final, with one final decision and one award under concurrent review? | Yes. |
| 13 | Reject identical uploads across all citizens, including clarification reuse? | Yes. |
| 14 | After AI retries are exhausted, allow manual admin review? | Yes. |
| 15 | Provisional demo points or redeemable awards? | Yes to provisional demo points, for now. |
| 16 | Use work-item name initial-build? | Yes, as per PDD. |
| 17 | Controlled demo or real pilot? | Controlled demo, scalable for real use. |
| 18 | Meaning of one million? | One million registered users. |
| 19 | What daily/concurrent usage, upload volume, growth horizon, demo hosting target and budget should capacity planning address? | Yes to the offered architecture-review deferral. No numeric traffic target or budget supplied; review placement is proposed above. |
| 20 | What status freshness, key-operation latency, availability, and deployment downtime are needed, or explicitly not required for this work item? | Use recommended: 30-second maximum active-page freshness. Proposed for review: other numeric latency, production SLA, and zero-downtime requirements are not required for the demo. |
| 21 | May retry limits be decided in contract review, and should local tests work without live AI? | Yes; use recommended: bounded retries defined in CONTRACT and provider-free automated local/CI tests. |
| 22 | May alert thresholds and telemetry retention be decided during observability planning? | Yes; assign to the observability milestone Implementation Plan. |
| 23 | Preserve README scope/limits: staged evidence, no official integration, advisory AI with final admin decisions, media formats/limits, export, and provisional points/rates? What should change? | Keep advisory AI and final human review; use recommended staged evidence, no official integration, listed media formats/limits, ZIP export, and existing provisional point rates. |
| 24 | Use 1 million synthetic accounts, 100 concurrent active users, 10 submissions/minute, and a 30-minute benchmark? | No benchmark approval yet; user requested a control table to manage these decisions. |
| 25 | Use a locally hosted multi-instance demo with portable deployment configuration? | No hosting selection yet; tracked in Architecture Control Table. |
| 26 | What hosting and live AI spending caps apply? | No caps supplied; tracked in Architecture Control Table. |
| 27 | Should the control table also be database-backed runtime configuration, or only a planning/approval table? | Both planning/approval tracking and database-backed runtime configuration. Confirmed in chat and the structured question reply. |

| 28 | Initialize local Git and defer hosted CI for now? | Yes. User explicitly confirmed on 2026-10-26. Hosted execution is deferred until GitHub publishing; local checks remain required. |

| 29 | Approve the exact /me schema, canonical human claims, effective permissions and minimum token profile in Identity-Contract-Clarifications.md? | Approved by user on 2026-10-26; incorporated in API-Contract.md CT-12.1. |
| 30 | Approve the fixed service client IDs, receiver audiences, scope strings and human/service denials in that addendum? | Approved by user on 2026-10-26; incorporated in API-Contract.md CT-12.2. |
| 31 | Approve explicit operator-only baseline initialization, management preconditions/errors, publication reason and timestamp behavior in Controls-Contract-Clarifications.md? | Approved by user on 2026-10-30; incorporated in API-Contract.md CT-13.1. |
| 32 | Approve exact actor/audit representations, replay/rejection redaction, atomic audit publication and outage limitations in that addendum? | Approved by user on 2026-10-30; incorporated in API-Contract.md CT-13.2. |
| 33 | Approve the per-instance control-health route/representation and controls:health-only extension for the existing traffic-reporting client? | Approved by user on 2026-10-30; incorporated in API-Contract.md CT-13.3 and the CT-12 matrix. |
| 34 | Allow a validated service actor solely in rejection audit records for forbidden authenticated service-client publication attempts? | Approved by user on 2026-10-30; Controls-Service-Audit-Actor-Clarification.md incorporated into CT-13.2. No management permission is added. |

The prior unnumbered question about 15–30-second citizen status updates is covered by Q20; the upper bound is 30 seconds.

## Provenance Check

- IB-R01–IB-R20 name user answers or the accepted architecture discussion; IB-AC01–IB-AC17 map every requirement, including concurrency (IB-R13/IB-AC10), awards (IB-R14/IB-AC11), advisory AI (IB-R15/IB-AC12), staged evidence (IB-R16/IB-AC13), media limits (IB-R17/IB-AC14), export (IB-R18/IB-AC15), provider-free tests (IB-R19/IB-AC16), and both control tables (IB-R20/IB-AC17).
- Q17 and Q18 establish controlled-demo scope and registered-account scale; no concurrent-user or production-readiness target is inferred.
- README references were checked during capture; references to missing source/tests remain documentary claims only.
- Q12–Q15 confirm final decisions, duplicate scope, manual fallback, and provisional points. Q23 carries forward the specifically recommended README features and rates. Q19/Q21/Q22 assign later decisions; no numeric throughput, budget, retry limit, alert threshold, or retention period is invented.
- Q20 accepts recommended status freshness; the absence of other numeric operational targets and Q19's review placement were confirmed through requirements approval on 2026-10-24.
- The fresh-role-agent mechanism is labeled non-blocking and follows the requested PDD workflow.
- All requirement IDs have acceptance-criterion mappings. Q27 explicitly confirms both control-table capabilities. Additional control-contract topics are labeled design questions for review, not presumed approved behavior.
- The control-table revision adds IB-R20/IB-AC17; user approval of this revision is recorded in Status. Q24–Q26 values remain proposed or unset; selecting runtime configuration and approving requirements did not approve a benchmark, hosting choice, or spending cap.

- Q28 explicitly changes IB-R19/IB-AC16 and the Foundation CI gate. No runtime assertion, supported format, identity rule, or provider-spending authority changed; no hosted execution is inferred from local evidence.

- Q29/Q30 record approval of the existing identity clarification artifact and its incorporation as API-Contract.md CT-12. They fix machine-readable expectations for IB-R07; no new route, product feature, test execution, Implementation Plan approval or spending is inferred.

- Q31–Q33 record approval of Controls-Contract-Clarifications.md and incorporation as API-Contract.md CT-13. They resolve IB-R20 baseline, audit and control-health expectations, including a narrowly scoped CT-12 health-read extension. No service is added, no milestone concern is reassigned, and no test execution, production change or spending authority is inferred.

- Q34 completes the audit actor representation for already-forbidden authenticated service publication attempts. It preserves 403 rejection, null publication/value fields, validated identity provenance and all existing permissions; it authorizes no implementation or test execution.
