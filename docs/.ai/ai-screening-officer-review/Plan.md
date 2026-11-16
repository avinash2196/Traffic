# Plan — Focused AI Gateway Service

## Objective

Extract the existing provider capability into a separately running FastAPI HTTP service and connect the current application's durable worker to it. Finish with real image and video OpenAI assessments through the application, using a versioned prompt and a safe correlated trace. Gemini stays configurable, with its verification explicitly deferred.

## Authority and Historical State

- Authoritative scope: [requirements.md](requirements.md), confirmed Q17/Q18 and AGW-R01–R09. The user explicitly requested this planning revision; implementation is not authorized.
- This Plan replaces the remaining broad delivery sequence. [Prior Plan](Plan.pre-service-focus-2026-11-11.md) and [prior requirements](requirements.pre-service-focus-2026-11-11.md) preserve their original text, approvals, statuses and evidence links.
- Implementation Plans 001–011 and every ASOR execution/diagnosis artifact remain unchanged historical records. Their approved executions do not authorize this service extraction.
- Historical ASOR-M08D remains incomplete: [execution](ASOR-M08D-Execution-2026-11-11.md) and [continuation](ASOR-M08D-Continuation-2026-11-11.md) retain their failures, stopped checks and NOT RUN inventory. This Plan neither completes it nor requires its former unrelated regression sequence as a prerequisite.
- Historical completed milestones retain their recorded statuses in the archived Plan. Historical pending broad milestones are superseded for this delivery, not completed or erased.
- [MP4 diagnosis](MP4-Diagnosis-2026-11-11.md) observed a passing isolated case and predecessor sequence without establishing the original rejection's cause. No speculative intake repair is planned.
- No test, startup, key, private evidence, database-content inspection or live call was performed for this Plan. The applied working sources are the starting state; no clean or currently passing baseline is asserted.

## Current State

`app.py` starts the application worker through `durable.ai_worker_factory`. `gateway.py` supplies shared settings, registry, evidence loading, durable orchestration and usage projection in that same process. OpenAI and Gemini adapters already exist; common assessment policy is available for reuse.

`openai_adapter.py` currently loads evidence through application SQLite in preflight and writes provider usage directly through its application database/job identity. Wrapping that adapter factory in an HTTP endpoint would preserve the wrong boundary. Extraction must separate those responsibilities while retaining provider media preparation and policy behavior.

The existing OpenAI adapter prepares image inputs and sampled video frames. This is implementation evidence, not proof of a successful real OpenAI assessment or separate service. Current hardcoded model/profile validation also makes model compatibility a contract decision before implementation.

Existing coverage relevant to the boundary includes:

- `tests/test_gateway_openai.py`: request/common policy, configuration and saved snapshots, error/retry/restart/no-fallback behavior, normalization, usage, owned evidence and sampled coverage.
- `tests/test_durable_processing.py`: committed jobs, interrupted attempts, competing claims/stale completion, atomic acceptance, background dispatch, technical outcomes and evidence supersession.
- `tests/test_provider_response.py`: child framing, diagnostic capture, unknown diagnostics, absolute deadlines and timeout cleanup.
- `tests/test_evidence_intake.py`: accepted uploads and owned evidence feeding the worker; select only affected boundary cases.
- Existing launchers isolate source copies and classify exact old inventories. Those inventories are historical, not automatically suitable service tests or current acceptance commands.

## In Scope

- One service assessment boundary; extraction/reuse of current policy and adapters; application worker HTTP integration.
- Application-owned evidence authorization/loading, durable attempts, saved provider/prompt selection and result/usage persistence.
- Stateless service provider invocation, media preparation and structured result/error/usage return, including available usage on failed output.
- Correlated timing/failure/usage evidence, focused deterministic verification and an approved live OpenAI image/video protocol.
- Preservation of current three categories, national-rule notes, confidence/uncertainty conventions and advisory authority.

## Out of Scope

New dashboards, appeals, awards features, auth-service extraction, additional providers, unrelated intake/regression repairs, general rewrites, production deployment and publication. No service queue, service durable job store, shared application database/private-filesystem contract, hidden fallback or nested retries. Gemini-specific verification remains deferred; this is not a Gemini success claim.

## Requirements and Constraints

The application remains the only durable worker/queue/retry owner, with at most three total transient attempts and restart recovery. It owns claims, upload access, status and awards. The service cannot finalize claims or award points; transport/provider failures stay technical outcomes.

Only authorized evidence bytes and necessary context cross the boundary. Provider credentials remain service-side. Normal logs/responses exclude keys, raw media and sensitive prompt/evidence content. Safe correlation, timings, error metadata and usage support diagnosis; synthetic decoder diagnostics may retain safe stderr.

Versioned prompt/context, saved provider/model identity and media coverage must remain traceable. Sampled video cannot imply full temporal evidence. Reuse existing policy rather than inventing replacement legal conclusions or changing officer authority.

## Non-Blocking Open Decisions

None needed to approve this delivery sequence. Concrete technical choices below belong to the CONTRACT review; they are not unconfirmed product requirements or permission to begin coding.

## External Contract Requirements

AGW-M01 produces a separately reviewed service contract, starting from [External-Contract.md](External-Contract.md) as the historical in-process behavior baseline. Its existing approval is not approval of a network API. Verify baseline/source deltas and state which behavior is preserved and which service-facing behavior changes.

The contract must settle all of the following before executable work:

1. HTTP operation, versioned request/success/error DTOs, validation and status mapping; required observations, recommendations, separate confidence scores, limitations and category/rule conventions.
2. Authorized evidence transfer, identifiers/order/integrity, image/video format and size compatibility, invalid evidence handling, transient storage lifetime and cleanup; no caller paths or shared application storage as the service contract.
3. Caller authentication/authorization, local binding and configuration, credential ownership and safe rejection behavior without extracting an auth service.
4. Prompt text/version and context representation, trust separation for citizen/media text, policy/legal/media-profile versions and required identity returned with results.
5. Provider/model selection and validation, saved legacy/current snapshot compatibility, restart behavior during transition, fail-closed incompatibilities and absence of silent fallback. Verify current official model/media capability before fixing the supported live selection.
6. Finite upload/decode/provider/HTTP/attempt deadlines and their ordering; cancellation, disconnection, service restart and partial response semantics.
7. One application-owned attempt budget; zero nested service/provider retry loops. Define ambiguous outcomes, possible duplicate provider invocation/billing, late response acceptance and usage uncertainty without promising exactly-once provider execution or adding service persistence.
8. Correlation and attempt identity, available usage on success/refusal/invalid output, unknown usage semantics, failure stage/retryability, safe timings/log fields and result persistence ownership.
9. Service/application compatibility and startup/configuration expectations; no claim-state mutation authority in service DTOs. Include concrete examples and acceptance mappings rather than source code.

## Milestones

Decomposition: Split — one CONTRACT, one cohesive RED/GREEN pair, one intervening test-only OTHER harness correction and one OTHER live validation protocol. The intervening amendment below awaits user review; the original approval and completed RED remain historical authority. The HTTP contract and later live-input/provider setup require separate review boundaries. RED and GREEN have separate Implementation Plans because this crosses an external contract and is not the eligible small paired-plan case. Do not split again by file, provider or architectural layer.

### AGW-M01 — Service Contract (CONTRACT)

- Predecessor: approval of this Plan.
- Purpose/rationale: settle the new network boundary and compatibility before tests or extraction assume its behavior.
- Scope: the service contract decisions listed above, with deltas from historical behavior and current official model capability verification.
- Owned concern: external-contract definition and compatibility decisions; no implementation ownership of behavioral requirements.
- Exclusions: executable artifacts, Implementation Plan, provider calls and private-input inspection.
- Success: complete concrete contract submitted for human review; milestone completes only after user approval. No executable verification command is required.

### AGW-M02 — Service Boundary Behavior (RED)

- Predecessor: AGW-M01 approved contract.
- Purpose/rationale: one coherent failing specification for the application-to-service-to-provider boundary, including state ownership and failure semantics.
- Scope: deterministic contract, actual separate-process HTTP integration and affected preservation checks, using synthetic evidence and a controlled provider substitute.
- Verification concerns: all AGW-M03 behavior and AGW-R08 focused evidence selection; map each assertion to the approved contract.
- Exclusions: production changes, real providers, keys/private media, unrelated test repairs and Gemini-specific execution.
- Success: intended new behavioral assertions fail because the service boundary is absent; preserved applicable checks pass. Infrastructure errors, timeouts, skips and historical unrelated failures are not RED evidence.
- Prerequisite decision: existing Python/FastAPI/pytest/subprocess infrastructure supports meaningful RED; missing service symbols/HTTP behavior are expected RED conditions, not FOUNDATION work. Reinspect before the IP; a genuine infrastructure blocker requires replanning rather than hidden setup.
- Deliverable: separately reviewed `012_Implementation_Plan_...RED.md`; exact tests and safe verification commands belong there.

### AGW-M02A — Provider Harness Lifecycle Correction (OTHER)

- Proposed amendment, awaiting user review: the original requirements and AGW-CT01–08 contract remain approved and unchanged. This milestone changes test infrastructure only, owning no production behavior requirement.
- Predecessor: completed AGW-M02 valid RED; its 19 intended failures and two preserved passes remain valid and recorded without relabelling.
- Baseline: the synthetic provider currently runs a blocking four-second callback inside the service process and removes `provider-active` only in that callback's `finally`. Forced local process termination skips it on Windows; leaving the callback running would evade CT06 cancellation. The planning diagnostic in IP013 records this lifecycle conflict and the observed virtual-environment launcher/server PID distinction.
- Scope: move the same synthetic Responses wire builder into an independently owned literal-loopback HTTP server process; service test transport remaps only the fixed public Responses URL to that server, with real HTTP and zero retries. Keep all 19 existing behavioral assertions and their deadlines unchanged. Add an independent positive/client-kill/remote-drain diagnostic and bounded owned process-tree cleanup.
- Exclusions: production behavior/code, contract/requirements changes, test weakening, live providers, private inputs, decoder changes and broad historical inventories.
- Success: lifecycle diagnostic and its state repeat pass; exact `--red` classifier exits zero for the unchanged 19 intended behavioral failures and two preserved passes; source/private-state protections and owned cleanup succeed. Missing service behavior remains RED, never an OTHER test success claim.
- Deliverable: `013_Implementation_Plan_Provider_Harness_Lifecycle_OTHER.md`, jointly reviewable with this amendment. Execution requires the user's approval recorded in both artifacts. This amendment does not approve the IP.

### AGW-M03 — Service Extraction and Application Integration (GREEN)

- Predecessor: AGW-M02A verified harness correction. AGW-M02 valid RED remains a completed prerequisite, preserved in its execution evidence.
- Purpose/rationale: deliver the single end-to-end service capability with all its state, provider and transport responsibilities reviewed together.
- Scope: separate running service; application evidence authorization/loading and HTTP dispatch; stateless adapter/policy reuse; application result/usage persistence and existing durable retries/recovery; safe boundary diagnostics and configuration compatibility.
- Owns: AGW-R01/R02/R03/R04/R06/R07/R09 behavioral delivery.
- Exclusions: additional queue/retries, application database or private-filesystem mounts in service, live calls, unrelated product behavior and test additions.
- Success: new RED assertions and the full applicable focused boundary selection pass; separate-process evidence proves HTTP traversal and service isolation. Persist available failure usage and preserve unknowns; retained provider selection has no hidden fallback.
- Deliverable: separately reviewed `014_Implementation_Plan_...GREEN.md`, grounded in the actual RED evidence. Exact code/config/dependency/startup changes belong to that IP.
- Before any needed dependency/bootstrap change, identify whether it is a genuine separate prerequisite; do not hide FOUNDATION work in GREEN.

### AGW-M04 — OpenAI Live Demonstration (OTHER)

- Predecessor: AGW-M03 verified GREEN.
- Purpose/rationale: prove the requested actual provider flow, which deterministic substitutes cannot establish.
- Owns: AGW-R05 and focused verification/reporting delivery AGW-R08.
- No behavior change: execute a validation protocol and record evidence only; no source, tests, configuration or dependency edits. Any behavior fix returns to approved planning/RED/GREEN.
- Baseline: approved contract, GREEN focused evidence, selected service/application versions and a recorded safe preflight. Historical Gemini 402 and incomplete OpenAI verification are not successful baseline evidence.
- Preserved tests: use AGW-M03 passing focused selection as the unchanged executable baseline; evidence-only recording does not require an unchanged broad rerun.
- Inputs: user-authorized image and video supplied in a user-designated private location, plus service-side credentials entered by the user; protocol specifies each input/provider/model/prompt and placement without committing media or exposing keys.
- Protocol: `015_Implementation_Plan_...OTHER.md` defines exact startup/preflight/submission/observation/cleanup steps and met/not-met rules before execution. Submit both media types through the application, not directly to the gateway/provider.
- Completion: both traverse application → separate gateway → actual OpenAI → application with schema-valid advisory results, correlated timings/usage/provider/prompt identity, truthful sampled coverage and preserved claim/award authority. Record exact commands, trimmed safe observations, deviations and process cleanup.
- Missing inputs: mark Waiting with the named user input; no fabricated evidence. Failed calls/decodes/schema checks remain failures; OTHER cannot finish passing by recording a failure as a success or substituting Gemini.

### Final Review

Predecessor: AGW-M04 complete. Review code or production readiness for this named work item; write `Final-Review.md` against all acceptance rows, evidence and approved IPs. This review does not implement findings, approve itself or authorize rollout. Record Written — awaiting user decision.

## Requirement Traceability

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
| AGW-R01 Separate HTTP service/reuse | AGW-M03 | AGW-M02/M03; M04 live traversal |
| AGW-R02 Versioned evidence/result contract | AGW-M03 | AGW-M01 contract review; M02/M03; M04 real results |
| AGW-R03 Configured OpenAI/retained Gemini/no fallback | AGW-M03 | AGW-M02/M03; M04 selected OpenAI |
| AGW-R04 App-owned attempts/queue/restart | AGW-M03 | AGW-M02/M03 |
| AGW-R05 Real image/video demonstration | AGW-M04 | AGW-M04 |
| AGW-R06 Safe correlation/errors/usage | AGW-M03 | AGW-M02/M03/M04 |
| AGW-R07 Application authority/technical outcomes | AGW-M03 | AGW-M02/M03/M04 |
| AGW-R08 Focused verification/honest deferred coverage | AGW-M04 | AGW-M02/M03/M04; Final Review |
| AGW-R09 Categories/rule notes/uncertainty preservation | AGW-M03 | AGW-M02/M03/M04 |
| New external contract/compatibility decisions | AGW-M01 | AGW-M01 approval; Final Review |
| Test-only provider harness lifecycle correction | AGW-M02A (OTHER; no production requirement ownership) | AGW-M02A lifecycle diagnostic, unchanged RED classifier and preserved checks |
| Excluded product work/queues/shared-storage/fallback | none — exclusion | Final Review |
| Historical failures/deferred Gemini/stale documentation report | none — Final Review obligation | Final Review |

## Verification Commands and Scope

Repository evidence supplies Python/pytest and existing isolation launchers, not authorization to run their historical inventories unchanged. No commands ran for the original Plan drafting; the proposed M02A amendment has only the synthetic planning diagnostic recorded in IP013. The approved RED IP must define exact source-only isolated-copy commands, named selection and output classification; GREEN uses that approved evidence and selection.

- Run new/changed and affected boundary checks first. At GREEN execution run the full applicable focused boundary selection once, covering contract DTOs/media/auth, genuine cross-process HTTP, synthetic OpenAI wire behavior, failure/usage handling, deadlines, restart/ambiguous outcomes, application ownership and safe logs.
- Review existing tests named in Current State and select affected nodes explicitly. Historical in-process assertions may need contract-driven RED updates; preserve equivalent behavioral coverage rather than silently weakening them.
- Repeat only the persistent state/configuration subset when that runtime/configuration change requires a repeat under PDD v0.16; record its reason/inventory. No automatic full-suite replay, old full209/repeat96 gate or per-file RED/GREEN restart.
- Use synthetic fixtures, controlled providers, source-only scratch copies and dedicated temporary database/media paths; exclude live/private state. Never run unsafe root fixtures or silently count missing/skipped assertions as coverage.
- Record each actual command with trimmed real output, failures, NOT RUN cases, deviations and cleanup. A newly exposed unrelated failure is reported honestly, not repaired under this Plan or called passing.
- If synthetic decoder observation is required, retain safe tool/version/exit/timing/stderr metadata through the reviewed protocol; observation does not authorize speculative repairs.
- Live verification is exclusively AGW-M04's approved exact protocol and cannot be replaced by deterministic results.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| AGW-M01 Service Contract | Completed — approved 2026-11-11 | [Service contract](External-Contract.md) approved by user; documentation only. |
| AGW-M02 Service Boundary RED | Completed — valid RED 2026-11-11 | [Execution evidence](AGW-M02-Execution-2026-11-11.md): 19 intended assertion failures, 2 preserved passes; exact verifier exit 0; protection/cleanup checks passed. |
| AGW-M02A Provider Harness Lifecycle OTHER | Completed — verified 2026-11-11 | [Execution evidence](AGW-M02A-Execution-2026-11-11.md): exact IP013; lifecycle first/repeat passed, 19 intended RED failures, 2 preserved passes, verifier exit0; protection and cleanup passed. |
| AGW-M03 Service Extraction GREEN | Completed — verified 2026-11-11 | [Execution evidence](AGW-M03-Execution-2026-11-11.md): exact approved IP014 applied; verifier exit 0, 19 service + 2 preserved + 2 state-repeat passes, lifecycle first/repeat passed; protection and cleanup passed. |
| AGW-M04 OpenAI Live Demonstration OTHER | Pending | IP015 not created; image/video live evidence required. |
| Final Review | Pending | No focused Final-Review.md written. |

Historical statuses/evidence remain in the archived Plan and linked artifacts above; no historical failed, blocked or pending row has been relabelled complete. Future evidence records actual commands/output below this table or in linked execution artifacts.

## Risks

- Adapter database/usage coupling (`openai_adapter.py` preflight/dispatch) can accidentally preserve shared state behind HTTP. Contract and focused isolation checks require bytes/context in, result/error/usage out, with app-owned persistence.
- Existing snapshot/profile constraints (`gateway.py` settings/validation) can reject a supported model or change restart selection. Contract defines compatibility before code; deterministic checks cover saved jobs and mismatch handling.
- Network ambiguity can consume provider resources without a received result. Contract exposes unknown outcome/usage and app-owned bounded recovery; no exactly-once billing claim or extra service retry.
- Video decode and sampled frames (`openai_adapter.py` media preparation; historical MP4 diagnosis) can fail or omit evidence. Preserve safe diagnostics and truthful coverage; failed video blocks live completion rather than prompting unrelated repairs.
- Historical launchers encode old inventories and deferred Gemini cases. Reviewed focused selection and real output prevent accidental broad gates or false success claims.

## Final Acceptance Criteria

| Criterion | Source | Demonstrated by |
| --- | --- | --- |
| Separate application/service use the approved HTTP contract and application-owned worker. | AGW-AC01; R01/R02/R04 | M01 approval; M03 cross-process evidence; M04 traversal |
| Real image and real video each produce a valid OpenAI assessment with truthful coverage. | AGW-AC02; R02/R03/R05 | M04 live evidence; synthetic checks insufficient |
| Required advisory fields, uncertainty, provider/model/prompt identity, usage and correlated timings exist. | AGW-AC03; R02/R03/R05/R06/R09 | M03 deterministic results and M04 real results |
| Failures, bounded retries/restart, no nested retry/fallback and safe logs verified; Gemini deferred. | AGW-AC04; R03/R04/R06/R08 | M02/M03 focused checks; M04 safe trace; Final Review |
| Application state/officer/award authority and category/legal conventions preserved. | AGW-AC05; R07/R09 | M03 preservation checks; M04 observation |
| Exact focused/live evidence and historical failures/limitations reported without broad-suite claims. | AGW-AC06; R08 | M04 evidence and Final Review |
| Approved contract/separate IPs, valid RED then passing GREEN/OTHER, exclusions and process cleanup evidenced. | Plan gates/success criteria | Final Review inspection of M01–M04 artifacts |
| Stale product/user-facing documentation listed for the user, without silently rewriting it. | PDD Final Review obligation | Final Review |

## Status

Amendment approved by user on 2026-11-11 (America/Chicago), jointly with IP013: AGW-M02A and its consequential IP numbering/predecessor/verification changes are authorized. IP013 authorizes its exact test-harness correction only. Requirements and External-Contract approvals are unchanged.

Original approval: Approved by user on 2026-11-11 (America/Chicago), jointly with the focused requirements. AGW-M01 service-contract drafting is authorized. No test, implementation, startup or live provider call is authorized by this approval; the contract and later milestone Implementation Plans retain their review gates.
