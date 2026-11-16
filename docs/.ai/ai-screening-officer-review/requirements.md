# Requirements — ai-screening-officer-review

## Goal

Deliver a separately running AI gateway that the current application calls with image/video evidence and a specific versioned assessment prompt, obtaining a real structured OpenAI traffic assessment. Retain Gemini as a configurable adapter. This revision narrows the current delivery to that gateway boundary and its application integration. [User: Q17]

## Status

Approved by user on 2026-11-11 (America/Chicago), jointly with the focused Plan, following the explicit "go ahead" response to their review request. This approval authorizes the service-contract drafting milestone; implementation still requires its reviewed Implementation Plan. [User: Q17/Q18; subsequent joint approval]

## Scope Revision and Historical Authority

The previous full requirements and milestone sequence are preserved in [requirements before service focus](requirements.pre-service-focus-2026-11-11.md) and [Plan before service focus](Plan.pre-service-focus-2026-11-11.md). Completed source changes, incomplete executions and failures remain historical evidence. This requirements revision supersedes their remaining delivery scope; it does not mark any old milestone complete, erase failures or authorize further execution of an old Implementation Plan. The prior external contract is the baseline for previously implemented behavior, not an already approved separate-service API. [User: Q17/Q18]

The former deferral of the original multi-service redesign is replaced only for extracting the AI gateway. No auth-service extraction or broader service redesign is included. The full officer/dashboard/appeal/award work is deferred beyond this focused delivery. [User: Q17]

## Business Context

- Problem: provider integration and broad regression verification have not yet demonstrated the desired application-to-gateway-to-provider flow. The current delivery must have a concrete, bounded finish line. [User: Q17]
- Actors: the application submits evidence and owns the claim workflow; the gateway performs AI assessment; configured providers supply model output; officers retain final claim/award authority. [User: Q17] [User: historical Q14]
- Outcome: the application calls a separate gateway service and receives real structured OpenAI assessments for an image and a video, with a reviewable request-to-result trace. [User: Q17]

## Repository-Confirmed Facts

- AGW-F01: `app.py` imports gateway settings during startup and starts its worker through `durable.ai_worker_factory`; there is no separate HTTP gateway call in that startup path. [Repo: app.py:138] [Repo: app.py:140]
- AGW-F02: `gateway.py` currently contains shared settings, durable orchestration, registry and usage projection in the application process; the registry contains Gemini and OpenAI adapters. [Repo: gateway.py:26] [Repo: gateway.py:124] [Repo: gateway.py:227] [Repo: gateway.py:250]
- AGW-F03: `openai_adapter.py` already targets the Responses endpoint, prepares media including sampled video, and builds an inference request. This is reusable code, not evidence that a separate service or live OpenAI call has succeeded. [Repo: openai_adapter.py:20] [Repo: openai_adapter.py:64] [Repo: openai_adapter.py:138] [Repo: openai_adapter.py:191]
- AGW-F04: `intake.py` validates video with ffprobe and full ffmpeg decoding; its error handler hides the underlying decode exception from clients. [Repo: intake.py:70] [Repo: intake.py:78] [Repo: intake.py:83]
- AGW-F05: The historical M08D execution/continuation reports contain incomplete verification and failures. The later MP4 diagnostic recorded a passing single case and predecessor sequence, explicitly without establishing the original rejection's cause. These remain evidence limitations. [Repo: ASOR-M08D-Execution-2026-11-11.md, Actual commands and outcomes] [Repo: ASOR-M08D-Continuation-2026-11-11.md, New failure traceback] [Repo: MP4-Diagnosis-2026-11-11.md, Findings]

## Requirements

| ID | Requirement | Source |
| --- | --- | --- |
| AGW-R01 | Run the AI gateway as a separate service from the existing application, with an HTTP boundary. Reuse the current adapters and common assessment policy rather than restart provider integration. | User Q17 |
| AGW-R02 | Define one assessment contract accepting image/video evidence, violation context/category and a specific versioned assessment prompt; return observations, suspected violations/recommendation, separate confidence scores, limitations, provider/model identity, usage and structured errors. | User Q17; historical Q14 |
| AGW-R03 | Select OpenAI through configuration for this delivery's actual provider calls. Retain configurable Gemini; do not silently fall back to another provider. Adding a provider must not require rewriting claim/officer/award behavior. | User Q17; historical Q16 |
| AGW-R04 | The existing application's background worker calls the gateway. Durable jobs, saved selection and bounded retry ownership stay in the application; do not introduce a second queue or nested gateway/provider retries. Preserve at most three total transient attempts and restart recovery. | User Q17; historical Q6 |
| AGW-R05 | Demonstrate a real image assessment and a real video assessment through application → gateway → OpenAI → application using authorized evidence and the assessment prompt. Report actual sampled-frame coverage/limitations for video; do not represent sampled evidence as full temporal coverage. | User Q17 |
| AGW-R06 | Capture an end-to-end correlated request/result trace, timings, provider usage and structured failure information. Keep keys, raw media contents and sensitive prompt/evidence data out of normal logs and responses; retain safe diagnostic metadata and decoder stderr when diagnosing synthetic fixtures. | User Q17; prior instruction to log the end-to-end diagnostic |
| AGW-R07 | Preserve application ownership of claims, uploads, officer review and awards. Gateway output is advisory and cannot finalize claim status or award points. Technical AI/transport failures remain technical outcomes, never automatic claim rejection. | User Q17; historical Q6/Q14 |
| AGW-R08 | Verify this boundary with focused contract, cross-process integration and failure checks. Keep Gemini-specific verification explicitly deferred, including historical failures; never report it or the former full suite as passing. | User Q17; prior instruction to leave Gemini tests and move ahead |
| AGW-R09 | Preserve the current demo's three assessment categories (helmet, triple riding, red light), reviewed national-rule notes and uncertainty conventions while moving the boundary. Do not infer legal certainty or change review/award rules. | User Q17's reuse/preservation scope; historical Q13/Q14 |

## Scenarios

- AGW-S01: An image report accepted by the application is processed by its durable worker through the separate gateway and yields a real OpenAI assessment under the selected prompt. Maps AC01/AC02/AC03. [User: Q17]
- AGW-S02: A video follows the same path, with disclosed sampling and uncertainty; the returned assessment remains advisory. Maps AC02/AC03/AC05. [User: Q17]
- AGW-S03: The gateway/provider is unavailable, times out, refuses output or returns invalid output. The application records a technical outcome and its bounded retry rules apply, without a final violation/award decision or hidden fallback. Maps AC04/AC05. [User: Q17] [User: historical Q6/Q14]
- AGW-S04: An operator follows a correlation identifier from the application attempt through gateway media preparation/provider call to the recorded result or failure and usage, without exposing secrets or evidence contents. Maps AC03/AC04. [User: Q17]

## Operational Characteristics

| Characteristic | Answer | Source |
| --- | --- | --- |
| Deployment | One local demo deployment, with application and gateway running as separate services. | User Q17; historical Q12 |
| Capacity/latency/availability | No capacity, latency or uptime target required for this work item. Finite request/decode/attempt deadlines and their relationship are contract/design decisions. | User historical Q12 |
| State and consistency | Application retains durable jobs/attempts/restart recovery and owns claim/award state; gateway owns provider invocation only. | User Q17; historical Q6 |
| Dependency failures | At most three application-owned transient attempts; no nested retries or silent fallback. | User Q17; historical Q6 |
| Visibility | Correlated logs, timings, failures and usage for the focused flow; new dashboards, exported monitoring and alerts are not required here. | User Q17; historical Q9 |
| Spending | Authorized live OpenAI calls have no application spending cap; this does not authorize keys/media in logs. | User historical Q4/Q16; Q17 |
| Data preservation | Preserve existing claims, evidence and current workflow while extracting the gateway. New durable media storage or retention infrastructure is not requested. | User Q17 |

## Decisions Deferred to the Service Contract

Endpoint/DTOs, evidence transfer and size/format compatibility, caller authentication/authorization, prompt/version representation, provider/model selection compatibility, timeout/cancellation/ambiguous-outcome semantics, attempt correlation and safe logging fields must be concrete before implementation. These are contract/design decisions within the confirmed boundary, not additional feature requests. Exact supported model capability must be verified from current official sources before live use. [User: Q17's define-one-contract step; historical model selection delegation]

## Explicit Exclusions

- New officer dashboards, citizen appeals, awards functionality, new providers, auth-service extraction and unrelated regression repairs are outside this delivery. Existing state/authorization/award behavior remains a constraint. [User: Q17]
- No second queue, gateway retry orchestration, automatic provider fallback or general application rewrite. [User: Q17]
- No production deployment, repository publication or claim of comprehensive production readiness is authorized by the instruction to update requirements and start planning. [User: Q18's documentation/planning-only scope]

## Acceptance Criteria

| ID | Observable acceptance | Requirements |
| --- | --- | --- |
| AGW-AC01 | Application and gateway run separately; the application invokes the approved HTTP assessment contract rather than an in-process provider adapter. | R01/R02/R04 |
| AGW-AC02 | Real image and real video evidence each traverse application → gateway → selected OpenAI provider → application and produce a schema-valid assessment; returned video coverage is truthful. Synthetic checks alone do not satisfy this criterion. | R02/R03/R05 |
| AGW-AC03 | Assessment contains the required observations, confidence/limitations, provider/model/prompt identity and available usage, with one correlated request-to-result trace and timing evidence. | R02/R03/R05/R06/R09 |
| AGW-AC04 | Focused checks demonstrate structured transport/provider/invalid-output failures, bounded app-owned attempts, no nested retries/fallback and no secret/raw-evidence log disclosure. Gemini verification remains clearly deferred. | R03/R04/R06/R08 |
| AGW-AC05 | Gateway cannot decide claim outcomes/points; existing application state and officer authority are preserved. Category/legal output conventions remain advisory. | R07/R09 |
| AGW-AC06 | Final review reports the exact focused checks and live evidence, historical unresolved failures, deferred Gemini coverage and any remaining limitations, without claiming old broad-suite completion. | R08 |

## Clarification Log

Original Q1–Q16 are preserved verbatim in the archived requirements; their unchanged answers above are cited explicitly.

| Q | Question / instruction | Confirmed answer |
| --- | --- | --- |
| Q17 | Recommendation: separate gateway; one assessment contract; reuse adapters; app-owned jobs/retries and HTTP integration; actual image/video OpenAI evidence and safe traces; focused verification; later dashboards/appeals/awards. | User: "yes update the requirement as per that and then start the plan" confirms the recommended scope. |
| Q18 | Authorization for this step. | Same user instruction explicitly requests requirements revision and planning; no implementation execution requested in this step. |

## Provenance and Consistency Check

- R01–R09 each cite the confirmed Q17 scope or unchanged earlier user answers; their acceptance mapping is R01→AC01, R02→AC01/02/03, R03→AC02/03/04, R04→AC01/04, R05→AC02/03, R06→AC03/04, R07→AC05, R08→AC04/06, R09→AC03/05.
- S01→AC01/02/03, S02→AC02/03/05, S03→AC04/05, S04→AC03/04. No scenario lacks acceptance.
- Current citations inspected: app.py138/140; gateway.py26/124/227/250; openai_adapter.py20/64/138/191; intake.py70/78/83; named execution/continuation/diagnostic evidence sections. Historical requirements are labelled archived, not current source facts.
- Confirmed recommendation Q17 supplies the solution boundary; no unconfirmed recommended requirement is introduced. Detailed API/security/model choices remain explicit contract decisions before code.
- The former monolith-only boundary and broad remaining milestones are superseded for this delivery; archived evidence/approvals are preserved rather than relabelled successful. Full product scope is not declared implemented or permanently removed.
