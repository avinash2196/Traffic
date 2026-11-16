# Requirements — ai-screening-officer-review

## Goal

Extend the current RoadWatch demo with live AI screening and an officer dashboard: AI may screen out clearly irrelevant submissions, while all other submissions reach officers with evidence observations, Indian-law notes and confidence scores. Officers can review submissions at every AI stage and retain final authority over violations and awards. [User: brief] [User: Q2] [User: Q11] [User: Q14]

## Status

Provider-boundary revision approved by user on 2026-11-10 (America/Chicago). The original 2026-11-08 approval remains historical authority for work already executed. The user requested a configurable AI gateway, retention of Gemini, and OpenAI implementation for current testing in Q16. This revision updates those requirements for review before the Plan and provider contract are revised.

## Repository-Confirmed Facts

ASOR-F01 through ASOR-F07 retain the initial capture baseline from 2026-11-08. Current provider-boundary facts are recorded in ASOR-F08 and ASOR-F09 below.

- ASOR-F01: The current application is a FastAPI entry point with citizen reporting and officer routes. Its database wrapper uses SQLite. This is the implementation baseline selected for this work item. [Repo: app.py:23] [Repo: app.py:736] [Repo: app.py:1178] [Repo: bootstrap.py:30] [User: Q2]
- ASOR-F02: The application currently recognizes helmet, triple-riding and red-light categories and maps them to provisional points. Existing behavior is context, not authorization to change the points mapping. [Repo: app.py:33]
- ASOR-F03: The upload route is under `/api/media/`, which the middleware exempts before setting citizen identity, while the upload handler requires that identity. Report attachment currently queries media by ID and updates its report association. These paths require attention for the selected upload-to-AI flow. [Repo: app.py:183] [Repo: app.py:629] [Repo: app.py:636] [Repo: app.py:758] [Repo: app.py:777]
- ASOR-F04: The schema already contains AI-screening status/result/time fields. Existing environment examples instead advertise an OpenAI key/model, and the demo roadmap describes optional OpenAI integration. These facts do not select a provider for this work item. [Repo: bootstrap.py:107] [Repo: .env.example:82] [Repo: .env.example:85] [Repo: docs/Plan.md:349]
- ASOR-F05: Citizen report details and officer queues already contain polling behavior. The transport and polling representation for the new feature are contract/design decisions rather than requirements inferred from that implementation. [Repo: templates/citizen-report-detail.html:118] [Repo: templates/officer-queue.html:104]
- ASOR-F06: Application startup currently constructs a TracerProvider without a configured exporter in that path. The requested operational visibility is recorded separately below rather than assumed to exist. [Repo: app.py:123]
- ASOR-F07: `docs/Plan.md` describes the later local SQLite MVP. Historical `docs/.ai/initial-build` artifacts also exist; the media GREEN plan there remains a draft. Neither the historical plan nor its scratch proposal authorizes this enhancement. [Repo: docs/Plan.md:3] [Repo: docs/Plan.md:37] [Repo: docs/.ai/initial-build/009_Implementation_Plan_Evidence_Intake_Screening_GREEN.md:5]

- ASOR-F08: The current worker factory directly imports the Gemini factory. Provider selection through configuration is not implemented in that factory. [Repo: durable.py:243]
- ASOR-F09: The current Gemini adapter fixes its model to gemini-3.8-flash and rejects other configured model values. Its settings and transport are provider-specific. [Repo: gemini.py:26] [Repo: gemini.py:49] [Repo: gemini.py:168]

No product-level `docs/requirements.md` exists at capture time; the template's product-level relationship section is therefore omitted. [Repo: docs/requirements.md — absence verified during capture]

The selected baseline is the current demo, not completion of the historical service redesign. [User: Q2]

## Requirements

- **ASOR-R01 — Baseline and prerequisite scope.** Extend the current FastAPI/SQLite demo and include upload/attachment fixes needed for the AI flow. The original multi-service redesign is deferred. This does not authorize a general rewrite or unrelated feature work. [User: Q2]
- **ASOR-R02 — Media scope.** AI screening must support both photos and videos in the first demo. [User: Q3]
- **ASOR-R03 — Live providers and current test selection.** Retain the Gemini integration and implement OpenAI as an additional provider. Use OpenAI for the current live testing. The demo must make actual calls to the selected provider. Specific supported models and provider media handling are proposed during planning and contract review. [User: Q16, superseding the Gemini-only selection in Q4/Q10]
- **ASOR-R04 — Spending policy.** Preserve the existing policy without an application spending cap for authorized live AI calls as provider selection expands. Transient failures remain bounded to three total attempts. [User: Q4] [User: Q6] [User: Q16 provider extension]
- **ASOR-R05 — Limited automatic screen-out.** AI may directly screen out submissions clearly irrelevant to traffic reporting. It must pass everything else to an officer, including relevant submissions with no apparent violation, unclear evidence and uncertain assessments. Technical AI failures must not cause rejection. [User: brief] [User: Q11]
- **ASOR-R06 — Submission-level relevance.** Assess multiple attachments together when present: one irrelevant attachment must not screen out a claim that contains relevant evidence. [User: brief]
- **ASOR-R07 — Advisory violation assessment.** For material passed to officers, assess the reported violation and provide a recommendation and notes. AI does not decide that a violation legally occurred and does not make the final award decision. [User: Q11] [User: Q14]
- **ASOR-R08 — Indian-law scope.** Assess the existing helmet, triple-riding and red-light categories using Indian national rules. State/local additions and additional violation categories are deferred. [User: Q13]
- **ASOR-R09 — Officer-facing explanation and confidence.** Show evidence observations, recommendation, notes citing the applicable rule/section from reviewed official sources, uncertainty/limitations, and separate 0–100 relevance and suspected-violation confidence scores. Clearly label the scores as AI self-assessments. [User: Q14]
- **ASOR-R10 — Officer dashboard.** Provide counts and views for all open claims, AI-recommended approval, AI-recommended rejection, uncertain/needs-human-judgment claims, pending/running AI, failed AI, AI-screened-out claims, and officer-finalized claims. Distinguish an AI recommendation from an officer decision and an AI screen-out from an officer rejection. [User: brief] [User: Q9]
- **ASOR-R11 — Officer access and actions.** Officers can open and review any claim, including AI-pending, assessed, failed and screened-out claims; they need not wait for AI. Retain human approve, reject and request-information actions, and permit an officer to override an AI screen-out. [User: brief] [User: Q6]
- **ASOR-R12 — Human-final decisions.** Officers retain final authority over violation decisions and awards. An AI recommendation or intake screen-out must not itself award points. [User: brief] [User: Q14]
- **ASOR-R13 — Citizen explanation and recovery.** Show the citizen a specific explanation for an AI screen-out and allow resubmission or a request for officer review. [User: brief]
- **ASOR-R14 — Same-claim manual review.** A request for officer review moves the same AI-screened-out claim into a clearly marked manual-review queue while preserving its evidence and AI explanation; it does not create a separate appeal record. [User: Q7]
- **ASOR-R15 — Background work and restart recovery.** Run AI processing in the background. Jobs must survive application/worker restarts. [User: Q6]
- **ASOR-R16 — Dependency failure and bounded retry.** Retry transient AI failures at most three total attempts. Officers remain able to review immediately; AI errors, timeouts and exhausted processing remain technical outcomes, not automatic claim rejection. [User: brief] [User: Q6]
- **ASOR-R17 — Late-result safety.** If an officer finalizes a claim while AI is pending or running, a later AI result must not change the final decision or points. [User: Q6]
- **ASOR-R18 — Demo operational visibility.** Provide dashboard status/counts/reasons and operational visibility into job attempts, failure reasons, processing time and AI usage/cost. Dashboard and operational logs/usage are sufficient for this work item; exported telemetry and alerts are not required here. [User: Q9]
- **ASOR-R19 — Deployment scope.** Support a single local demo instance. No capacity, latency or uptime targets are required for this work item. [User: Q12]
- **ASOR-R20 — Configurable provider gateway.** Complete a provider-neutral AI gateway boundary in the existing demo. Application configuration selects a provider adapter. Gemini and OpenAI use a shared assessment, error and usage boundary consumed by the claim workflow. Adding another adapter must not require rewriting claim submission, officer review or awards. Retain Gemini while OpenAI is selected for current testing. [User: Q16, accepting the discussed gateway boundary]

## Operational Characteristics

| Characteristic | Answer | Source |
|---|---|---|
| Scale | Single local demo; no capacity target required for this work item. | [User: Q12] |
| Deployment | Single local demo instance extending the current FastAPI/SQLite baseline. This does not prescribe whether background execution shares a process. | [User: Q2] [User: Q12] |
| Availability and latency | No latency or uptime target required for this work item. Jobs must nevertheless survive restarts. | [User: Q12] [User: Q6] |
| Consistency and concurrency | Officers can decide before AI completes. A late AI result cannot change their final decision or points. Manual review preserves the same claim/evidence/AI explanation. | [User: Q6] [User: Q7] |
| Dependency failure | Transient failures have at most three total attempts; technical failure never means rejection; manual review is available immediately. Live processing through the selected provider is required, with OpenAI selected for current testing. [User: Q16] | [User: Q4] [User: Q6] |
| Observability | Dashboard counts/status/reasons, attempts, errors, processing time and AI usage/cost. Exported metrics/traces and alerts are not required for this work item. | [User: Q9] |

## Decisions Deferred to Later Milestones

- Review the OpenAI model selection, provider configuration representation, shared provider contract and media-handling details during planning and contract review. Existing photo/video support and officer authority remain required. Gemini remains available. [User: Q16] [User: Q3] [User: Q14]
- Resolve the concrete external status/response representation, confidence-score representation, legal-reference set, relevance examples, and review-action contracts in the external-contract review before their implementation or RED tests. These must implement ASOR-R05/R08/R09/R10/R14 rather than introduce new rejection grounds. The confirmed requirement is that only irrelevant claims are automatically screened out; no confidence threshold is prescribed by these requirements. [User: Q11] [User: Q13] [User: Q14]
- State/local legal additions and additional violation categories are deferred beyond the selected demo scope; they are not silently inferred from the general phrase “Indian laws.” [User: Q13]

## Explicit Exclusions

- Do not implement the original multi-service redesign as part of this work item. [User: Q2]
- AI must not automatically finalize a violation or grant an award. Its automatic rejection authority is limited to intake irrelevance. [User: brief] [User: Q11] [User: Q14]
- AI errors/timeouts must not reject a claim. [User: brief] [User: Q6]
- Do not replace same-claim manual review with a separate appeal record. [User: Q7]
- No state/local law additions or additional violation categories are included in this work item. [User: Q13]

## Non-Blocking Decisions

- Dashboard presentation, labels and layout details beyond the required distinctions and views are left to planning and contract/UI review. [Left to planning and contract/UI review — non-blocking]
- Provider credentials, SDK/package choice, background execution mechanism, schema and file layout are implementation decisions, not selected by this requirements capture. [Left to Implementation Plan review — non-blocking]
- Exported telemetry/alerts and capacity/latency/uptime targets are explicitly not required here; this is not a prohibition on future work. [User: Q9] [User: Q12]

## Acceptance Criteria

| ID | Observable outcome | Requirements |
|---|---|---|
| ASOR-AC01 | The current demo's upload/attachment flow can submit a photo and a video for screening with the required prerequisite fixes, without introducing the original multi-service redesign. | ASOR-R01, ASOR-R02 |
| ASOR-AC02 | Demonstrate actual OpenAI screening using the reviewed model selection for current testing, with the existing no-application-cap policy. Retain the Gemini adapter as an available configured provider. | ASOR-R03, ASOR-R04 |
| ASOR-AC03 | A clearly irrelevant submission is automatically screened out with an explanation. Relevant, uncertain, unclear and no-apparent-violation submissions reach officers. A technical error is not classified as rejection. | ASOR-R05, ASOR-R07, ASOR-R13, ASOR-R16 |
| ASOR-AC04 | Where a claim has multiple attachments, relevant evidence prevents automatic screen-out merely because another attachment is irrelevant. | ASOR-R06 |
| ASOR-AC05 | For each of the three selected violation categories, officers can see observations, a recommendation, notes citing reviewed national-rule references, limitations, and separate labelled 0–100 AI relevance/violation confidence scores. | ASOR-R07, ASOR-R08, ASOR-R09 |
| ASOR-AC06 | Dashboard counts/views distinguish pending/running, positive/negative recommendations, uncertainty, failure, AI screen-out and final officer outcomes; officers can open claims in every AI state. | ASOR-R10, ASOR-R11, ASOR-R18 |
| ASOR-AC07 | An officer can approve, reject or request information without waiting for AI, including reviewing/overriding an AI-screened-out claim. AI alone never awards points or finalizes a violation. | ASOR-R11, ASOR-R12 |
| ASOR-AC08 | The citizen can see the AI screen-out explanation and resubmit or request manual review; the latter keeps the same claim ID, evidence and AI explanation and appears in a marked manual-review queue. | ASOR-R13, ASOR-R14 |
| ASOR-AC09 | AI execution occurs in the background; pending/in-progress work is recoverable after a restart. Transient failures stop after at most three total attempts, with manual officer review available. | ASOR-R15, ASOR-R16 |
| ASOR-AC10 | Finalize a claim while AI is still processing, then complete the AI work: the officer's final decision and points remain unchanged. | ASOR-R12, ASOR-R17 |
| ASOR-AC11 | The single local demo exposes the requested job status/counts/reasons, attempt/failure information, processing time and AI usage/cost. Capacity, latency, uptime, exported telemetry and alert delivery are not acceptance gates for this work item. | ASOR-R18, ASOR-R19 |
| ASOR-AC12 | Provider configuration selects the appropriate gateway adapter. Gemini and OpenAI return the common assessment/error/usage boundary to the existing claim workflow. The gateway permits another adapter to be added without rewriting claim, officer-review or award behavior. | ASOR-R20 |

## Clarification Log

| Q | Question | Answer |
|---|---|---|
| Q1 | Work-item name? | `ai-screening-officer-review`. |
| Q2 | Extend the current FastAPI/SQLite demo with required upload/attachment fixes, or use the original service architecture? | Extend current demo + required upload fixes; original multi-service redesign deferred. |
| Q3 | Photos and videos, or photos first? | Photos and videos in the first demo. |
| Q4 | AI provider/model and currency/spending cap/accounting period? | “use google and lets put no limits ..live calls should be make”. Google clarified by Q10; no application spending cap. |
| Q5 | Approve relevance policy during contract review or specify it now? | “I’ll specify the rules now”; resolved through Q11, Q13 and Q14. |
| Q6 | Background AI, restart survival, at most three total transient-failure attempts, immediate officer decisions, and no late-AI change to final decision/points? | Confirm all rules. |
| Q7 | Same-claim manual review preserving evidence/explanation, or separate appeal? | Reopen the same claim for manual review. |
| Q8 | Deployment, capacity, latency and uptime needs? | “yes”; ambiguous answer resolved by Q12, not treated as an independent numeric or topology requirement. |
| Q9 | Dashboard/counts/status/reasons plus attempts/failures/time/usage/cost, or exported telemetry and alerts now? | Dashboard + operational logs/usage; alerts later. |
| Q10 | Gemini API with API key and model selection during planning? | Gemini API; select model during planning. |
| Q11 | Irrelevance versus officer-review rules, including borderline evidence? | “Ai should screen out irrelavnt directly , everything else should go to officer and should also show AI confidence score .. review as per given laws (Indian ) and then pass to officer withe notes”. |
| Q12 | Clarify the operational “yes”? | Single local demo instance; no capacity, latency or uptime targets required for this work item. |
| Q13 | Three existing categories with national rules, or broader/state/local scope? | Existing helmet, triple-riding and red-light categories + national rules. |
| Q14 | Observations, recommendation, official-source rule/section notes, uncertainty/limitations, separate labelled 0–100 relevance/violation confidence scores, and officer-final decisions/awards? | Confirm this output. |
| Q15 | Correct the stale submission test to the approved contract? | User confirmed “Correct the stale test to the approved contract.” This test-only decision is recorded in Plan.md under M02 and remains historical. |
| Q16 | Complete the configurable gateway boundary, retain Gemini and implement OpenAI for current testing? | “yes lets finish this boundary and then do the open Ai implementation ..keep gemini there but we will tets it with open ai for now”. This accepts the previously discussed shared provider interface and normalized assessment/error/usage boundary. |

The brief comprises the discussion accepted by “ok create new workitem for this”: officer access to all AI stages; AI recommendations separated from final decisions; limited irrelevance screen-out; dashboard views; citizen explanation/resubmission/manual review; combined-attachment relevance; and human-final decisions/awards. Subsequent explicit answers refine that brief, particularly Q11's “everything else should go to officer.” [User: brief] [User: Q11]

## Provenance Check

- R01 traces to Q2, R02 to Q3, R03 to Q16, and R04 to Q4/Q6 with provider selection extended by Q16. R20 traces to Q16 and the gateway proposal the user accepted. Q16 explicitly supersedes the earlier Gemini-only selection in Q4/Q10 while retaining Gemini as an adapter.
- R05 traces to the brief/Q11, R06 to combined-attachment relevance, R07 to Q11/Q14, R08 to Q13, R09 to Q14, R10 to dashboard discussion/Q9, R11 to officer-access discussion/Q6, R12 to human-final discussion/Q14, R13 to citizen-recovery discussion, R14 to Q7, R15/R16/R17 to Q6, R18 to Q9 and R19 to Q12. These business rules retain their previous meaning.
- R01/R02 map to AC01, R03/R04 to AC02, R05 to AC03, R06 to AC04, R07 to AC03/AC05, R08/R09 to AC05, R10 to AC06, R11 to AC06/AC07, R12 to AC07/AC10, R13 to AC03/AC08, R14 to AC08, R15 to AC09, R16 to AC03/AC09, R17 to AC10, R18 to AC06/AC11, R19 to AC11 and R20 to AC12. Every acceptance criterion lists its requirements.
- The current provider facts were inspected at durable.py:243 and gemini.py:26/49/168. F01-F07 remain identified as the original capture baseline. Historical plans and optional OpenAI environment examples do not establish a completed configurable gateway.
- Model selection, configuration keys, request/response details and provider video-processing mechanics remain for review in the Plan and external contract. No new category, final AI award authority, confidence threshold, performance target or deployment service is introduced by this requirements revision.
- This revision changes only this requirements artifact. Existing implementation, test evidence and provider contract retain their recorded history pending reviewed downstream amendments.
