# Plan â€” initial-build

## Status

Approved by user on 2026-10-24. DP-M01 external contract drafting is authorized. Contract approval and every repository-changing milestone retain their separate PDD review gates; no executable change is authorized by Plan approval alone. The user explicitly approved the local-Git/hosted-CI deferral amendment on 2026-10-26 (requirements Q28); local Foundation acceptance now uses the passing local evidence, with hosted execution deferred until GitHub publishing.

## Objective

Deliver the controlled traffic-evidence demo in the approved requirements, with traceable correctness, multi-instance and capacity evidence. A provider-free development result is distinguishable from completed real-provider acceptance.

## Current State

Inspection on 2026-10-24 found README.md and work-item documentation only. There is no application source, build/dependency manifest, executable startup configuration or test suite. README implementation claims are documentary, not verified running behavior. No existing tests provide a behavioral baseline. No product-level docs/requirements.md or repository instruction file was found.

The requirements Status records user approval on 2026-10-24. Architecture-Proposal.md Status records approval of AP-D01â€“AP-D06 on that date and supersedes its historical proposal/pending labels, including the earlier Q24â€“Q26 table state. These approvals do not approve this Plan.

## In Scope

All IB-R01â€“IB-R20 and IB-AC01â€“IB-AC17, subject to the separate live-spending gate, using the approved architecture. Refer to Architecture-Proposal.md for the stack, responsibility boundaries, durable correctness direction, local portable multiple-instance topology, zero-paid mode, benchmark and growth scenario. Later Implementation Plans choose concrete executable changes within those approved choices.

Both planning/approval controls and runtime operational controls are delivered. Planning approval does not publish runtime configuration.

## Out of Scope

Official government/enforcement integration, real redeemable rewards, and AI final approval/rejection are excluded by requirements. Paid provisioning/hosting and live AI spending without separate approved currency, cap and accounting period are excluded by the approved architecture.

## Requirements and Constraints

The authoritative sources are requirements.md (approved requirements, constraints, exclusions and acceptance criteria) and Architecture-Proposal.md (approved architecture decisions AP-D01â€“AP-D06). The traceability table below assigns each requirement once.

The approved benchmark is synthetic evidence, not production capacity certification. One million registered accounts does not mean one million active users. The thirty-day growth scenario is a sizing input, not retention policy or a requirement to provision that storage. The only numeric performance acceptance here is approved benchmark execution and at-most-30-second healthy-connectivity active-page freshness; other timings and resource values are measurements.

Every repository-changing milestone requires its own reviewed Implementation Plan. RED changes tests/checks only; GREEN delivers its predecessor's behavior. CONTRACT delivers a reviewed external contract without an Implementation Plan. Only RED may end with expected failure caused by missing approved behavior. All other milestones require all applicable verification to pass. Completion never authorizes the next milestone.

## User-Approved CI Gate Amendment — 2026-10-26

Requirements Q28 directs local Git initialization and defers hosted CI until GitHub publishing. The provider-free workflow remains in scope for future use; its hosted execution is no longer a DP-M02 or subsequent local-development gate. All local verification criteria remain required. This amendment records an explicit user decision, not a CI success claim. See Local-Git-CI-Deferral.md and DP-M02-Browser-Execution-2026-10-26.md. No later Implementation Plan or executable milestone is approved by this change.

## Non-Blocking Open Decisions

Tool/package versions and exact executable verification commands are left to FOUNDATION Implementation Plan review within the approved stack. They do not alter scope. Alert thresholds and telemetry retention remain explicitly assigned to observability Implementation Plan review.

The user has not approved live AI currency, cap and accounting period. This named input gates only final controlled live-provider evidence, not provider-free development. When that approved milestone reaches the gate, record Waiting for those named inputs from the user; do not mark live acceptance complete or equate substitute evidence with provider evidence. No new budget or spending authority is assumed.

## External Contract Requirements

The first milestone delivers a new API/external contract artifact; no existing effective contract is present. It must resolve:
- Citizen/admin/authentication operations, role/ownership and token validation behavior, including signing-key cache expiry/outages.
- Report lifecycle, clarification rounds, citizen-visible states/reasons, finality, concurrent/replayed requests, advisory AI and manual review paths.
- Media ingest/private access/export behavior, accepted formats, exact byte/time boundary semantics, duplicate and pending-ingest conflicts, hash reservation/recovery and retention implications.
- Durable stage command/result behavior, revision compatibility, stale completion handling, bounded retry limits, eligible failures, leases/timeouts, exhaustion and authorized recovery.
- HTTPS status polling and freshness behavior, connectivity handling, errors and externally observable missing/empty outcomes.
- Gateway caller/provider behavior, provider/model eligibility, structured assessment, disabled-mode disclosure, AI budget periods/reservations, uncertain results and safe enforcement before dispatch.
- Runtime-editable setting selection, management interface and permissions, validation/ranges, defaults/missing values, publication/versioning/concurrent edits, audit, cross-instance visibility, outage/stale behavior, in-flight effects and spend accounting/enforcement.
- Externally settable deployment/runtime configuration and boundary interactions needed by the approved local topology.

These are decisions for CONTRACT review; this Plan defines no endpoint, schema or precise unresolved semantics. The identity vocabulary and response details were subsequently resolved by user-approved Q29/Q30 on 2026-10-26, incorporated as API-Contract.md CT-12; DP-M03 must use that approved baseline.

## Milestones

The linear sequence isolates security, runtime configuration, media, durable processing, AI, finalization, browser behavior, export, observability and integrated evidence. Those boundaries have distinct failure modes and reviewable completion evidence; no pair is a containing milestone.

Common exclusions for each milestone: no scope from later milestones, no unreviewed contract decisions, no paid provisioning, and no unapproved live calls. RED additionally excludes production, dependency and configuration changes. GREEN excludes new test infrastructure and behavior not expressed by its approved RED evidence.

### DP-M01 â€” External contract
- Type: CONTRACT.
- Predecessor: Plan approval.
- Purpose/rationale: approve external behavior before any executable change.
- Scope: deliver the contract covering every decision listed under External Contract Requirements.
- Owned requirements/concerns: deferred contract decisions; approved boundary compatibility.
- Exclusions: all executable artifacts and implementation design.
- Success: complete contract reviewed and approved by the user; every listed decision resolved, with all contract consistency checks passing.

### DP-M02 â€” Executable prerequisites
- Type: FOUNDATION.
- Predecessor: DP-M01.
- Purpose/rationale: inspection found no executable build or test prerequisites.
- Scope: establish only build, dependencies, bootstrap, local HTTPS/multiple-instance execution, private storage/database/authentication and telemetry test prerequisites, a retained provider-free CI workflow (hosted execution deferred by Q28) and local verification infrastructure needed by all REDs below; establish exact repeatable verification commands and prerequisite health checks.
- Owned requirements/concerns: executable readiness only, including approved stack/topology compatibility.
- Exclusions: domain model/schema, target behavior, production behavior scaffolding, behavioral tests and live calls.
- Success: approved prerequisite checks, build/bootstrap and infrastructure health verification all pass. Each later RED can execute meaningful checks without adding dependencies or infrastructure; absent target behavior remains valid RED evidence.

### DP-M03 â€” Identity RED
- Type: RED.
- Predecessor: DP-M02.
- Purpose/rationale: Identity is independently reviewable before protected workflows.
- Scope: tests/checks verify: Separate authentication and AI-gateway access responsibilities; enforce identity, role and caller-permission behavior under the reviewed contract; verify boundary denial independently of a full report workflow.
- Owned requirements/concerns: verification only for IB-R07 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M04.
- Prerequisites: DP-M02 supplies identity test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M04 â€” Identity GREEN
- Type: GREEN.
- Predecessor: DP-M03.
- Purpose/rationale: Identity is independently reviewable before protected workflows.
- Scope: Separate authentication and AI-gateway access responsibilities; enforce identity, role and caller-permission behavior under the reviewed contract; verify boundary denial independently of a full report workflow.
- Owned requirements/concerns: IB-R07; Authentication and authorization; approved separate authentication and gateway boundaries.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M03 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M05 â€” Runtime controls RED
- Type: RED.
- Predecessor: DP-M04.
- Purpose/rationale: Configuration consistency and spend authorization require their own evidence.
- Scope: tests/checks verify: Maintain the planning/approval record and deliver database-backed operational controls consumed by services, with reviewed management permissions, validation, publication, concurrent edits, audit, multi-instance visibility, outage and in-flight behavior; enforce disabled live AI until separately approved spending authority exists.
- Owned requirements/concerns: verification only for IB-R20 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M06.
- Prerequisites: DP-M02 supplies control-management and multi-instance database test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M06 â€” Runtime controls GREEN
- Type: GREEN.
- Predecessor: DP-M05.
- Purpose/rationale: Configuration consistency and spend authorization require their own evidence.
- Scope: Maintain the planning/approval record and deliver database-backed operational controls consumed by services, with reviewed management permissions, validation, publication, concurrent edits, audit, multi-instance visibility, outage and in-flight behavior; enforce disabled live AI until separately approved spending authority exists.
- Owned requirements/concerns: IB-R20; AP-D06 runtime control direction; AP-D04 zero-paid mode; safe concurrent budget accounting and uncertain provider outcomes.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M05 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M07 â€” Evidence intake and screening RED
- Type: RED.
- Predecessor: DP-M06.
- Purpose/rationale: Media safety and global identity have independent failure and race cases.
- Scope: tests/checks verify: Accept JPG, PNG, MP4, MOV and WEBM within the approved 25 MB and 45-second limits using CONTRACT boundary semantics; reject unsupported or over-limit media and global identical originals across citizens and clarification uploads, including concurrent ingestion; retain private original access and recover interrupted ingestion without exposing another citizen.
- Owned requirements/concerns: verification only for IB-R05, IB-R17 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M08.
- Prerequisites: DP-M02 supplies media fixture, decoding, storage, race and fault-injection test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M08 â€” Evidence intake and screening GREEN
- Type: GREEN.
- Predecessor: DP-M07.
- Purpose/rationale: Media safety and global identity have independent failure and race cases.
- Scope: Accept JPG, PNG, MP4, MOV and WEBM within the approved 25 MB and 45-second limits using CONTRACT boundary semantics; reject unsupported or over-limit media and global identical originals across citizens and clarification uploads, including concurrent ingestion; retain private original access and recover interrupted ingestion without exposing another citizen.
- Owned requirements/concerns: IB-R05, IB-R17; Private media and global hash ownership; bounded screening, original integrity and crash reconciliation.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M07 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M09 â€” Durable processing RED
- Type: RED.
- Predecessor: DP-M08.
- Purpose/rationale: Durability and recovery must be established before AI or decision integration.
- Scope: tests/checks verify: Process reporting, media screening and AI review through approved durable ownership boundaries across multiple instances; verify retry eligibility and bounds, lease recovery, stale-worker and stale-round rejection, idempotent handoffs and exhaustion visibility; preserve the durable eligibility for manual admin review after AI exhaustion and reject stale/final-round completion; this checks eligibility and handoff behavior, not the later decision UI.
- Owned requirements/concerns: verification only for IB-R03, IB-R04, IB-R08 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M10.
- Prerequisites: DP-M02 supplies database transaction, multi-process, clock and restart test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M10 â€” Durable processing GREEN
- Type: GREEN.
- Predecessor: DP-M09.
- Purpose/rationale: Durability and recovery must be established before AI or decision integration.
- Scope: Process reporting, media screening and AI review through approved durable ownership boundaries across multiple instances; verify retry eligibility and bounds, lease recovery, stale-worker and stale-round rejection, idempotent handoffs and exhaustion visibility; preserve the durable eligibility for manual admin review after AI exhaustion and reject stale/final-round completion; this checks eligibility and handoff behavior, not the later decision UI.
- Owned requirements/concerns: IB-R03, IB-R04, IB-R08; AP-D01 durable correctness direction; AP-D02 multiple-instance processing; reporting owns decisions and awards.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M09 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M11 â€” Advisory AI RED
- Type: RED.
- Predecessor: DP-M10.
- Purpose/rationale: Provider behavior and provider-free automation have a separate integration boundary.
- Scope: tests/checks verify: Deliver advisory provider integration exclusively through the distinct AI gateway, with no AI final decision; run local automated tests using an explicitly identified AI substitute without credentials or external AI calls and retain matching provider-free CI configuration for future activation (hosted execution deferred by Q28); verify disabled-mode disclosure, gateway access and budget enforcement, bounded provider failures and accounting recovery.
- Owned requirements/concerns: verification only for IB-R15, IB-R19 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M12.
- Prerequisites: DP-M02 supplies provider-free integration, network-denial and ci execution prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M12 â€” Advisory AI GREEN
- Type: GREEN.
- Predecessor: DP-M11.
- Purpose/rationale: Provider behavior and provider-free automation have a separate integration boundary.
- Scope: Deliver advisory provider integration exclusively through the distinct AI gateway, with no AI final decision; run local automated tests using an explicitly identified AI substitute without credentials or external AI calls and retain matching provider-free CI configuration for future activation (hosted execution deferred by Q28); verify disabled-mode disclosure, gateway access and budget enforcement, bounded provider failures and accounting recovery.
- Owned requirements/concerns: IB-R15, IB-R19; Real provider adapter capability; labeled test substitute confined to tests/benchmark; gateway credential isolation.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M11 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M13 â€” Final decisions and awards RED
- Type: RED.
- Predecessor: DP-M12.
- Purpose/rationale: Finality and financial-like invariants warrant isolated concurrency review.
- Scope: tests/checks verify: Deliver final admin approval/rejection and citizen-visible provisional points: 2 for helmet violations and 3 for triple riding or red-light violations; conflicting concurrent or repeated decisions yield one immutable final decision and at most one award, with consistent timeline and point totals.
- Owned requirements/concerns: verification only for IB-R13, IB-R14 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M14.
- Prerequisites: DP-M02 supplies concurrent decision, replay and transaction test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M14 â€” Final decisions and awards GREEN
- Type: GREEN.
- Predecessor: DP-M13.
- Purpose/rationale: Finality and financial-like invariants warrant isolated concurrency review.
- Scope: Deliver final admin approval/rejection and citizen-visible provisional points: 2 for helmet violations and 3 for triple riding or red-light violations; conflicting concurrent or repeated decisions yield one immutable final decision and at most one award, with consistent timeline and point totals.
- Owned requirements/concerns: IB-R13, IB-R14; Human finalization and reporting-owned award consistency.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M13 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M15 â€” Citizen workflow RED
- Type: RED.
- Predecessor: DP-M14.
- Purpose/rationale: User-visible integration and freshness are independently measurable after underlying capabilities.
- Scope: tests/checks verify: Deliver the controlled demo citizen upload, processing and AI review, subsequent admin review, clarification using text or additional evidence or both, and visible failure/rejection/approval/reasons/awards; active pages under healthy connectivity show persisted changes through HTTPS polling within 30 seconds.
- Owned requirements/concerns: verification only for IB-R01, IB-R02, IB-R06, IB-R09 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M16.
- Prerequisites: DP-M02 supplies https browser, polling timing and user-journey test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M16 â€” Citizen workflow GREEN
- Type: GREEN.
- Predecessor: DP-M15.
- Purpose/rationale: User-visible integration and freshness are independently measurable after underlying capabilities.
- Scope: Deliver the controlled demo citizen upload, processing and AI review, subsequent admin review, clarification using text or additional evidence or both, and visible failure/rejection/approval/reasons/awards; active pages under healthy connectivity show persisted changes through HTTPS polling within 30 seconds.
- Owned requirements/concerns: IB-R01, IB-R02, IB-R06, IB-R09; Authorized status projection; clarification revision behavior; HTTPS polling and reconnect disclosure.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M15 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M17 â€” Evidence export RED
- Type: RED.
- Predecessor: DP-M16.
- Purpose/rationale: Export confidentiality and integrity form a small independent capability.
- Scope: tests/checks verify: Allow authorized admins to export a ZIP containing original evidence, matching SHA-256 hash and consistent report timeline; deny unauthorized export and preserve audited private evidence access.
- Owned requirements/concerns: verification only for IB-R18 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M18.
- Prerequisites: DP-M02 supplies archive inspection and permission test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M18 â€” Evidence export GREEN
- Type: GREEN.
- Predecessor: DP-M17.
- Purpose/rationale: Export confidentiality and integrity form a small independent capability.
- Scope: Allow authorized admins to export a ZIP containing original evidence, matching SHA-256 hash and consistent report timeline; deny unauthorized export and preserve audited private evidence access.
- Owned requirements/concerns: IB-R18; Export permission, evidence integrity and audit.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M17 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M19 â€” Observability RED
- Type: RED.
- Predecessor: DP-M18.
- Purpose/rationale: Cross-component diagnostics require the preceding running workflows.
- Scope: tests/checks verify: Expose correlated reporting, media, AI and admin/award telemetry, including queue/backlog/recovery, processing failures, AI latency/usage/cost/reservations/errors, status freshness and control revision visibility; verify redaction and operational signals against reviewed alert and retention decisions.
- Owned requirements/concerns: verification only for IB-R10 and the corresponding concerns assigned in traceability; implementation ownership belongs to DP-M20.
- Prerequisites: DP-M02 supplies telemetry capture, collection, retention and alert test prerequisites; preceding GREEN milestones supply already delivered behavior. No additional FOUNDATION is projected; re-inspect before planning and stop for reviewed replanning if prerequisites are missing.
- Exclusions: common exclusions and RED restrictions above; no real provider call while spending is unapproved.
- Success: reviewed tests/checks expose missing approved behavior, with each failure attributable to that behavior rather than broken infrastructure. Previously completed verification remains passing.

### DP-M20 â€” Observability GREEN
- Type: GREEN.
- Predecessor: DP-M19.
- Purpose/rationale: Cross-component diagnostics require the preceding running workflows.
- Scope: Expose correlated reporting, media, AI and admin/award telemetry, including queue/backlog/recovery, processing failures, AI latency/usage/cost/reservations/errors, status freshness and control revision visibility; verify redaction and operational signals against reviewed alert and retention decisions.
- Owned requirements/concerns: IB-R10; Correlation and safe telemetry across approved boundaries; alert thresholds and telemetry retention are owned by this milestone's Implementation Plans, with decisions first reviewed in its RED Implementation Plan and carried forward unchanged to GREEN.
- Exclusions: common exclusions and GREEN restrictions above.
- Success: the approved DP-M19 checks and prior regression verification all pass; running behavior and completion evidence demonstrate this scope.

### DP-M21 â€” Controlled demonstration and capacity validation
- Type: OTHER.
- Predecessor: DP-M20.
- Purpose/rationale: validate delivered behavior and capacity without inventing a missing production capability to justify RED.
- Scope: execute the staged demo and repeatable synthetic benchmark using 1,000,000 registered accounts, 100 concurrent active users and 10 uploads/minute for 30 minutes; record topology, hardware, workload/media mix, warmup, substitute profile, latency/resource/storage measurements, healthy-connectivity freshness and separately labeled failure/concurrency probes. Record the approved growth scenario comparison. Complete a controlled real-provider journey and correlated gateway usage/error evidence only after separate approved spending authority permits calls.
- Owned requirements/concerns: IB-R11 capacity evidence, IB-R16 staged demonstration; AP-D03 benchmark, AP-D05 sizing scenario, AP-D02 local multiple-instance evidence and real-provider validation gate.
- No-behavior-change statement: all production behavior is delivered by DP-M04â€“DP-M20. This milestone changes no production behavior or tests; it runs a reviewed validation protocol and records evidence only. A revealed behavioral defect stops for normal reviewed replanning and RED/GREEN delivery.
- Baseline evidence: record the complete passing predecessor regression suite, approved local topology, account dataset state, available machine resources and disabled AI policy before validation.
- Preserved tests: the complete passing suites established by DP-M03â€“DP-M20 remain unchanged and must pass after validation.
- Inputs/protocol ownership: its Implementation Plan specifies exact commands/steps, locally generated synthetic account and staged-media inputs, non-sensitive input locations, machine prerequisites and a met/not-met rule for every observation. The user supplies separately approved AI currency/cap/accounting period and provider credentials through the reviewed private configuration boundary; credentials and provider inputs are never committed. DP-M02 supplies benchmark and provider-evidence execution prerequisites.
- Exclusions: common exclusions; production/test/configuration changes, paid provisioning and live calls before budget approval.
- Success/completion evidence: all protocol checks, approved invariants, benchmark execution and healthy-connectivity freshness checks pass, with measured resource/latency results and labeled fault results recorded; preserved tests pass. Real-provider journey and correlated usage/error evidence pass within the separately approved spending authority. Substitute-only results leave this milestone Waiting for the named budget inputs from the user and IB-AC01/IB-AC05 live-provider acceptance unfulfilled.
DP-M02 serves every RED: DP-M03 identity, DP-M05 controls, DP-M07 media, DP-M09 durability, DP-M11 AI, DP-M13 decisions, DP-M15 citizen workflow, DP-M17 export, DP-M19 observability. This projected walk includes browser, media, concurrency/restart, telemetry and benchmark prerequisites from the outset, without implementing their behavior. Later REDs use delivered predecessors; no RED creates infrastructure.

## Requirement Traceability

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
| IB-R07 | DP-M04 | DP-M03 |
| IB-R20 | DP-M06 | DP-M05 |
| IB-R05 | DP-M08 | DP-M07 |
| IB-R17 | DP-M08 | DP-M07 |
| IB-R03 | DP-M10 | DP-M09 |
| IB-R04 | DP-M10 | DP-M09 |
| IB-R08 | DP-M10 | DP-M09 |
| IB-R15 | DP-M12 | DP-M11 |
| IB-R19 | DP-M12 | DP-M11 |
| IB-R13 | DP-M14 | DP-M13 |
| IB-R14 | DP-M14 | DP-M13 |
| IB-R02 | DP-M16 | DP-M15 |
| IB-R06 | DP-M16 | DP-M15 |
| IB-R09 | DP-M16 | DP-M15 |
| IB-R18 | DP-M18 | DP-M17 |
| IB-R10 | DP-M20 | DP-M19 |
| IB-R01 | DP-M16 | DP-M15 |
| IB-R11 | DP-M21 | DP-M21 |
| IB-R16 | DP-M21 | DP-M21 |
| IB-R12 â€” reviewed artifact chain, approvals, RED/GREEN records and final review | none â€” Final Review obligation | Final Review |
| Deferred external contract decisions | DP-M01 | Human contract review |
| Executable prerequisites for every RED | DP-M02 | DP-M02 prerequisite verification |
| Authentication and authorization; approved separate authentication and gateway boundaries | DP-M04 | DP-M03 |
| AP-D06 runtime control direction; AP-D04 zero-paid mode; safe concurrent budget accounting and uncertain provider outcomes | DP-M06 | DP-M05 |
| Private media and global hash ownership; bounded screening, original integrity and crash reconciliation | DP-M08 | DP-M07 |
| AP-D01 durable correctness direction; AP-D02 multiple-instance processing; reporting owns decisions and awards | DP-M10 | DP-M09 |
| Real provider adapter capability; labeled test substitute confined to tests/benchmark; gateway credential isolation | DP-M12 | DP-M11 |
| Human finalization and reporting-owned award consistency | DP-M14 | DP-M13 |
| Authorized status projection; clarification revision behavior; HTTPS polling and reconnect disclosure | DP-M16 | DP-M15 |
| Export permission, evidence integrity and audit | DP-M18 | DP-M17 |
| Correlation and safe telemetry across approved boundaries; alert thresholds and telemetry retention are owned by this milestone's Implementation Plans, with decisions first reviewed in its RED Implementation Plan and carried forward unchanged to GREEN | DP-M20 | DP-M19 |
| AP-D03 benchmark; AP-D05 growth scenario sizing comparison without retention commitment; AP-D02 local portable multi-instance demo; staged evidence only; real-provider evidence gate | DP-M21 | DP-M21 |
| No official integration, redeemable awards or AI finalization | none â€” exclusion | Final Review |
| No paid provisioning or unapproved live AI spend | none â€” exclusion | Final Review |
| Production uptime SLA, other numeric latency targets and zero-downtime deployment | none â€” not required | none |

## Verification Commands

No executable project command is currently supported by repository evidence. DP-M02's reviewed Implementation Plan must establish exact commands for prerequisite health/build, local and CI provider-free tests, database/media and multi-instance integration, browser HTTPS/freshness, fault/concurrency probes, telemetry checks and synthetic benchmark execution. Subsequent Implementation Plans source and refine their exact invocations from those resulting executable artifacts, not README claims or instruction files.

Sources: requirements IB-R03â€“IB-R11, IB-R13â€“IB-R20; approved architecture sections Local topology, Required later evidence, Polling and observability, and Capacity and media estimates for review. DP-M21's controlled live-provider evidence commands require the separately approved spending input. CONTRACT verification is document review against the decision list. Final Review inspects recorded approvals, actual command/output evidence, all criteria and exclusions.

Each execution records the actual command with trimmed real output below Execution Status or a linked evidence artifact, explains command deviations and stops every process it started. DP-M02 owns execution prerequisites; RED milestones own their checks; GREEN milestones own running behavioral evidence; DP-M21 owns the benchmark dataset/run records and controlled provider evidence. No verification depends on an unowned executable artifact.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| DP-M01 — External contract | Completed — user approvals recorded 2026-10-24, 2026-10-26 and 2026-10-30 | API-Contract.md approved Status and CT-11–13; Identity-Contract-Clarifications.md Q29/Q30 and Controls-Contract-Clarifications.md Q31–Q34 approval, including Controls-Service-Audit-Actor-Clarification.md. No executable change is authorized by contract approval. |
| DP-M02 — Executable prerequisites FOUNDATION | Completed — 2026-10-26 | All mandatory local checks passed, including three full runs, restart, collector traces and empty domain databases. [Execution evidence](DP-M02-Browser-Execution-2026-10-26.md); [user-approved CI deferral](Local-Git-CI-Deferral.md), requirements Q28. Hosted CI is deferred, not passed. |
| DP-M03 â€” Identity RED | Completed — 2026-10-30 | Seven intended identity failures verified twice; all inherited local checks passed; resources removed and private state unchanged. [Execution evidence](DP-M03-Execution-2026-10-30.md). |
| DP-M04 â€” Identity GREEN | Completed — 2026-10-30 | Exact approved bootstrap applied; seven identity tests passed twice and all inherited checks/cleanup passed. [Execution evidence](DP-M04-Execution-2026-10-30.md). |
| DP-M05 — Runtime controls RED | Completed — 2026-10-31 | Exact approved 14-test file applied; 21 collected; 14 intended ordinary controls failures twice, seven identity regressions passed twice; three Foundation passes/restart, strict readiness, collector receipts, owner/database/isolation/hash checks and scoped cleanup/private-state equality passed. [Successful reapproved retry evidence](DP-M05-Execution-Retry-2026-10-31.md); [preserved stopped first attempt](DP-M05-Execution-2026-10-31.md). |
| DP-M06 â€” Runtime controls GREEN | Completed — 2026-10-31 | Exact approved three new files/two diffs applied; all21 immutable tests passed twice in same project (79.51s/93.97s); malformed-policy/optimized/SQL fault guards, explicit operator baseline/migrations, owner/grants/persistence/restart, three Foundation passes, collector receipts, exact source/isolation checks and scoped cleanup/private-state equality passed. [Execution evidence](DP-M06-Execution-2026-10-31.md). |
| DP-M07 â€” Evidence intake and screening RED | Completed — RED verified 2026-11-01 | Exact12 missing-media assertions twice (3.52s/5.48s); immutable21 regressions twice (92.53s/53.57s); four full Foundation checks, inherited owner/grants/persistence/restart/collector/hash/isolation and scoped cleanup/private equality passed. [Retry2 execution evidence](DP-M07-Execution-Retry-2-2026-11-01.md); original and first retry stops preserved. |
| DP-M08 â€” Evidence intake and screening GREEN | Pending | No execution evidence. |
| DP-M09 â€” Durable processing RED | Pending | No execution evidence. |
| DP-M10 â€” Durable processing GREEN | Pending | No execution evidence. |
| DP-M11 â€” Advisory AI RED | Pending | No execution evidence. |
| DP-M12 â€” Advisory AI GREEN | Pending | No execution evidence. |
| DP-M13 â€” Final decisions and awards RED | Pending | No execution evidence. |
| DP-M14 â€” Final decisions and awards GREEN | Pending | No execution evidence. |
| DP-M15 â€” Citizen workflow RED | Pending | No execution evidence. |
| DP-M16 â€” Citizen workflow GREEN | Pending | No execution evidence. |
| DP-M17 â€” Evidence export RED | Pending | No execution evidence. |
| DP-M18 â€” Evidence export GREEN | Pending | No execution evidence. |
| DP-M19 â€” Observability RED | Pending | No execution evidence. |
| DP-M20 â€” Observability GREEN | Pending | No execution evidence. |
| DP-M21 â€” Controlled demonstration and capacity validation | Pending | No execution evidence. Live-provider portion will wait for separate user-approved currency, cap and period. |

## Risks

- Documentation-only baseline (README.md and inspected work-item documents): no command, environment capacity or claimed behavior is verified. DP-M02 establishes executable prerequisites before meaningful RED.
- Architecture-Proposal.md, Local topology and Tradeoffs: local shared failure domains do not prove production availability. DP-M21 reports hardware/resource constraints and actual multiple-instance results without overstating capacity.
- Architecture-Proposal.md, Both control tables: live spending is unapproved. DP-M06 and DP-M12 enforce disabled operation; DP-M21 waits for approved spending and real evidence, keeping substitute outcomes explicitly labeled.
- Architecture-Proposal.md, Capacity and media estimates: media/database/telemetry overhead is estimated. DP-M21 records measured storage/resources and the approved growth scenario comparison; no paid resources or month-long storage provisioning is implied.
- requirements.md deferred decisions and Architecture-Proposal.md correctness sections: retry, configuration and boundary semantics can affect correctness. DP-M01 resolves them before executable planning; incompatible findings stop for reviewed replanning.

## Final Acceptance Criteria

| Criterion | Source | Demonstrated by |
| --- | --- | --- |
| IB-AC01 â€” Citizen upload through AI and admin decision, reason and award | requirements.md | DP-M16; DP-M21 real-provider journey (waiting for separate spending approval) |
| IB-AC02 â€” Multiple instances and reviewed screening retry | requirements.md | DP-M10; DP-M21 integrated multiple-instance evidence |
| IB-AC03 â€” Global duplicate rejection including citizen/clarification and races | requirements.md | DP-M08 |
| IB-AC04 â€” Text, additional evidence, and combined clarification | requirements.md | DP-M16 |
| IB-AC05 â€” Distinct authentication/gateway and correlated AI usage/errors | requirements.md | DP-M04, DP-M20; DP-M21 real-provider usage/error evidence (waiting for separate spending approval) |
| IB-AC06 â€” Durable ownership boundaries and private evidence | requirements.md | DP-M10, with DP-M08 private-media evidence |
| IB-AC07 â€” HTTPS polling displays persisted change within 30 seconds under healthy connectivity | requirements.md | DP-M16; DP-M21 benchmark freshness |
| IB-AC08 â€” One-million-account and approved synthetic workload evidence without inferred throughput | requirements.md | DP-M21 |
| IB-AC09 â€” Reviewed artifacts, milestone approvals, RED/GREEN evidence and final review | requirements.md | Final Review |
| IB-AC10 â€” One immutable final decision and no duplicate award under conflict/replay | requirements.md | DP-M14 |
| IB-AC11 â€” Citizen-visible approved provisional point rates | requirements.md | DP-M14 and DP-M16 |
| IB-AC12 â€” Advisory AI and manual review after exhaustion | requirements.md | DP-M12 and DP-M10 |
| IB-AC13 â€” Staged demonstration and no government/enforcement integration | requirements.md | DP-M21 staged evidence; Final Review exclusion inspection |
| IB-AC14 â€” Format and exact contract boundary acceptance/rejection | requirements.md | DP-M08 |
| IB-AC15 â€” Authorized original/hash/timeline ZIP and unauthorized denial | requirements.md | DP-M18 |
| IB-AC16 — Local provider-free tests; retained CI workflow with hosted execution deferred by Q28 | requirements.md | DP-M12 for behavioral tests; DP-M02 for prerequisite workflow and local checks. Hosted execution is deferred until GitHub publishing, not claimed. |
| IB-AC17 â€” Planning approval tracking and reviewed database runtime controls across instances | requirements.md | DP-M06 |
| DP-PC01 â€” Contract decisions complete and human-approved | DP-M01 success | DP-M01 contract review |
| DP-PC02 â€” All RED prerequisites executable, no behavior scaffolding | DP-M02 success | DP-M02 passing prerequisite evidence |
| DP-PC03 â€” Each RED demonstrates intended missing behavior; each GREEN and prior regression suite pass | DP-M03â€“DP-M20 success | Each respective RED/GREEN execution record; DP-M21 passing validation and preserved-test evidence; Final Review checks the complete chain |
| DP-PC04 â€” Approved architecture choices and limitations represented, including growth scenario measurements | AP-D01â€“AP-D06 | DP-M04, DP-M06, DP-M08, DP-M10, DP-M12, DP-M20 and DP-M21 evidence; Final Review architecture inspection |
| DP-PC05 â€” Exclusions and not-required characteristics remain correctly distinguished | requirements.md and approved architecture | Final Review |

Final Review answers IB-R12 explicitly, checks every criterion against actual evidence, and lists any README statements made false for the user to update. It cannot close live-provider criteria using a fake assessment or a benchmark substitute.


