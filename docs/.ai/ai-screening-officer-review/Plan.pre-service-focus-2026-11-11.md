# Plan — ai-screening-officer-review

## Status

Provider-boundary Plan revision and corresponding External-Contract.md amendment approved by user on 2026-11-10. Requirements Q16/R03/R04/R20 and AC02/AC12 were approved November 10, 2026 (America/Chicago); this Plan revision and the amended contract are drafts, not approved execution authority. November 8/9 approvals remain historical authority for executed work only. Preparing this revision authorizes no implementation or live call. After joint approval, each new M08C/M08D milestone requires its own reviewed Implementation Plan; resumed M08 requires a newly reviewed live protocol. The stopped 007 artifact, completed 008/009 correction evidence and all original failed live evidence remain historical; none authorizes gateway/OpenAI work or another live run.

## Objective

Extend the current RoadWatch local FastAPI/SQLite demo with configurable provider screening, retained Gemini and OpenAI for current photo/video testing, durable background processing, an officer dashboard and citizen recovery. Only clearly irrelevant submissions may be automatically screened out. Everything else goes to officers, who retain final decision and award authority at every AI stage.

## Current State

The retained bullets below describe the original 2026-11-08 planning baseline; the Execution Status table records completed work. The November 10 baseline below governs the new provider revision; original source-line observations are historical, not claims that completed fixes are still missing.

- The selected baseline is the current application, not the historical multi-service build (requirements ASOR-R01/Q2). `app.py:23,101,142,736,1001,1178` implement FastAPI startup, reporting and officer handling; `bootstrap.py:21–38` uses SQLite/WAL and `bootstrap.py:160` supplies transactions. The app startup opens `./roadwatch.db` (`app.py:110`). Do not run its lifespan against the user's working directory during verification.
- Current points are helmet 2, triple-riding 3, red-light 3 (`app.py:33–37`). This work item does not authorize changing this mapping. Decisions currently require an awaiting-review claim (`app.py:1215`); approval changes points (`app.py:1226`); rejection references an undefined `reason` (`app.py:1261`). The prerequisite fixes necessary for required review actions belong to the officer capability below, not unrelated cleanup.
- Upload is exempted before identity is populated (`app.py:183`), but its handler requires identity (`app.py:636`). It writes a client-supplied filename below local storage (`app.py:677–682`) and returns an existing media identifier for a duplicate hash (`app.py:698–714`). Attachment looks up media by identifier and reassigns its report association without an ownership check (`app.py:758–779`). Citizen media serving explicitly bypasses ownership (`app.py:904–929`). These are real intake/attachment/privacy prerequisites for the required AI flow.
- The live upload route accepts declared MIME types with a 10 MiB check (`app.py:640–665`). The separate `MediaUploadHandler` declares different formats/25 MiB/45 seconds (`media.py:31–57`); the active upload route does not call it. Neither its constants nor historical draft proposals define this enhancement's contract. The current citizen form submits one media identifier (`templates/citizen-report.html:149–181`), so combined-attachment relevance requires an actual intake change.
- The current schema has media-level AI result/status/time fields (`bootstrap.py:107–109`), but no durable AI job lifecycle in that schema. Existing officer queue defaults select awaiting-review/resubmitted reports (`app.py:1018–1024`); officer details and citizen details do not yet provide the required assessment/dashboard distinctions. Existing pages poll (`templates/officer-queue.html:104`, `templates/citizen-report-detail.html:118`). UI inserts report values into HTML (`templates/officer-detail.html:77–131`), relevant when displaying untrusted AI explanations.
- `tests/test_auth.py:14–63` exercises signup/login/logout/access control and complete citizen workflow, but its fixture deletes `./roadwatch.db` and sidecars and reloads modules. `tests/conftest.py:19–111` builds a separate handwritten schema and patches bootstrap; it differs from current production schema, including required media association and omitted vehicle data. Its client lacks lifespan management (`tests/conftest.py:216–223`). These are unsafe or unreliable prerequisites for new regression evidence.
- Existing relevant tests are `TestSignup`, `TestLogin`, `TestLogout`, `TestAccessControl`, `TestGetCurrentCitizen`, `TestIntegration` in `tests/test_auth.py`; and submission, history, timeline, queue, detail, approval, rejection, clarification and queue-update classes in `tests/test_api_endpoints.py:32–459`. The latter has ten active tests with no explicit skip calls; some officer assertions are commented out, and submission expects `submitted` without the currently required vehicle number (`tests/test_api_endpoints.py:35–61`). This is evidence of drift, not proof either side is the approved new contract. `tests/test_media.py` contains twelve explicit `pytest.skip` calls with commented request/assertion bodies and fake media helpers; skips are neither RED evidence nor passing coverage. Its `.bak` file and historical test counts/hashes are not current executable evidence.
- `pytest.ini` establishes pytest configuration/markers; `requirements.txt` lists current dependencies. The existing `provider-free.yml` workflow instead runs the old multi-role foundation checks (`tools/check.py:24–72`), not these current-demo business tests. Preserve unrelated identity/control behavior and that workflow; do not turn it into an acceptance claim for this feature or require the old multi-service infrastructure for this demo.
- `.env.example:82–85` and `docs/Plan.md:349` describe optional OpenAI. `docs/Plan.md:28` claims the MVP complete; the historical `009_Implementation_Plan_Evidence_Intake_Screening_GREEN.md:5` remains a draft. These documents are context, not verified current enhancement evidence. The approved requirements explicitly supersede the old optional-provider/intake assumptions. No product-level `docs/requirements.md` exists. No approved current external contract was found that supersedes the selected runtime; the request/response reference differs from runtime (see contract baseline below).
- Planning used source inspection only. No test, application startup, provider call, build or database/media mutation was run to create this Plan. There is no verified passing baseline here. Earlier bounded isolated attempts reported to the planning task timed out; they establish neither success nor an intended assertion failure and are not milestone evidence.

### Provider revision baseline — 2026-11-10

Approved requirements R03/R20/Q16 deliberately change the Gemini-only selection. Current `durable.py` still directly imports Gemini snapshot validation and the worker factory; `app.py` snapshots settings at claim acceptance; `gemini.py` fixes the model and owns policy validation, media transport and raw usage capture. The new configurable boundary and OpenAI adapter are not implemented. The completed M08B evidence records 168 passes and 12 existing skips; it proves the bounded Gemini correction, not OpenAI behavior. The November 10 image rerun recorded upload-start HTTP 402, one consumed attempt and no assessment. That Gemini live blocker is retained as history and superseded as the current provider prerequisite by explicit OpenAI selection; neither billing resolution nor successful inference is claimed. Original photo/video acceptance remains required and manual video remains NOT RUN.

Authoritative inputs: approved November 10 requirements; the complete amended External-Contract.md (draft awaiting joint review); completed M01–M08B execution/checkpoint evidence; stopped 007 and completed 008/009 Implementation Plans; November 9 diagnosis and November 10 image rerun. Historical approvals remain limited to their original scopes. No product-level `docs/requirements.md` exists. This is static planning only: no private key/media inspection, live call, startup, database read or test execution.

## In Scope

- Required upload/attachment corrections, photos and videos, and combined-evidence submissions on the current demo.
- Configurable in-demo provider gateway, retained Gemini and OpenAI selected for current live testing without an application spending cap; advisory national-rule assessment for the existing three categories, with grounded explanations and separately labelled AI confidence scores.
- Durable background work, restart recovery, at most three total attempts for transient failures, and safe technical failure handling.
- Officer access/actions at every AI stage, dashboard distinctions, human-final decisions/points and protection from late AI results.
- Citizen screen-out explanation, resubmission and same-claim manual review preserving evidence/explanation.
- Local operational visibility and a live end-to-end demonstration with reviewable evidence.

## Out of Scope

- Original multi-service redesign, unrelated identity/control redesign or general application rewrite (ASOR-R01).
- AI-final violation decisions or awards, rejection because AI failed, separate appeal records, additional violation categories or state/local law additions (requirements Explicit Exclusions).
- Exported telemetry/alerts and capacity/latency/uptime targets are **not required**, rather than prohibited future work (ASOR-R18/R19).

## Requirements and Constraints

All twenty ASOR requirements and twelve ASOR acceptance criteria in the approved November 10 requirements are authoritative. Q16 updates R03/R04 and adds R20/AC12; other requirements remain unchanged. Their individual delivery/verification owners appear below. A model score alone is not an approved rejection threshold; clearly irrelevant intake is the sole automatic screen-out ground. Unclear, uncertain and no-apparent-violation traffic evidence reaches an officer. Technical failures do not become decisions. Multiple attachments are assessed as a submission. AI scores are self-assessments, not calibrated legal probabilities.

**Planning selection — ASOR-PD01, revised for Q16:** OpenAI is explicitly selected for current testing; retain Gemini as an available configured adapter. The amended External-Contract.md owns the proposed `gpt-6.1-terra` selection, retained Gemini model, official evidence/rationale, media handling, configuration and usage/pricing basis. Those delegated choices await joint contract/Plan review; this Plan does not independently approve or duplicate them. No automatic provider/model fallback or application spending cap is authorized. Actual account/model availability and traffic accuracy remain unproved. Provider limits and uncertain pricing do not become claim-admission or balance gates.

The current single-local-instance topology remains. Durable recovery and concurrent officer/AI safety are required even without scale or uptime targets. Preserve existing data, evidence and events while extending behavior. Secrets stay out of artifacts, responses and logs; approved live calls do not authorize reading private local files during planning. Existing unrelated behavior is a constraint, not permission to expand scope.

## Non-Blocking Open Decisions

- Specific dependency/package version, durable execution mechanism, schema evolution mechanics, file layout and prompt/parameter implementation are left to the relevant milestone Implementation Plan review. No new infrastructure is selected by this Plan.
- Dashboard visual layout and wording beyond approved distinctions are left to contract/UI review and the relevant Implementation Plans.
- Live verification uses user-provided credentials and representative media supplied for the demo. Their absence now does not block Plan review; a later approved milestone records `Waiting — selected OpenAI credentials and representative demo media from user` if needed. Credentials must be supplied privately, never committed or printed.

## External Contract Requirements

ASOR-M01 historically delivered `External-Contract.md` in this work-item folder. Its November 10 provider amendment is the complete resulting consumer/operator contract awaiting joint review with this Plan. It changes externally observable intake, status, review and recovery behavior, so CONTRACT comes first and has no Implementation Plan.

**Baseline:** use the selected current runtime's operations in `app.py` and its current browser consumers, carrying forward unaffected behavior. `docs/API-REQUEST-RESPONSE-REFERENCE.md:9–46` is a reference candidate, not an approved effective baseline: it omits the current required vehicle number and shows `submitted` where runtime returns `awaiting-review` (`app.py:742–753,788–794`). Record these divergences explicitly in the contract baseline and changes section; the user's Q2 selection of the current demo does not approve that stale reference. Verify all carried-forward operations against current source/consumers; if a genuinely authoritative approved contract is found to conflict, stop for human review rather than select one silently.

The contract must resolve, without this Plan preselecting the answer:

- Intake/attachment operations for photo/video and combined evidence; ownership, authorized access, reassociation/duplicate handling, valid media and attachment boundaries, safe upload failure behavior, and compatibility changes necessary for the required flow. Carry forward unrelated behavior rather than inventing new categories or arbitrary validation policies.
- Concrete external representations of AI progress, outcomes, technical failure, recommendations, officer-final outcomes and manual review; dashboard counts/filter membership and overlap; empty/missing/legacy assessment behavior and status refresh behavior.
- Separate 0–100 relevance/violation confidence representations and labels; observations, recommendation, explanations and limitations. Define malformed, incomplete, unavailable and ungrounded output behavior consistent with officer referral and no technical rejection.
- The relevance examples and combined-attachment policy needed to implement ASOR-R05/R06 without a new confidence-based rejection ground. Include irrelevant, relevant/no-apparent-violation, unclear/uncertain and mixed-evidence cases.
- The reviewed official national-rule/section reference set for helmet, triple-riding and red-light, including applicability/limitations. Verify current authoritative Indian sources during CONTRACT; do not invent clauses, fines or jurisdictional extensions. Define how citations remain within that reviewed set and how unsupported applicability is communicated.
- Officer approve/reject/request-information/override operations at every AI stage; final-decision/award invariants under late or competing results; citizen explanation/resubmission and same-claim manual-review actions preserving evidence/explanation. Define concurrency, repeated-action, error and authorization behavior for these required operations.
- Observable background/retry/restart semantics, including the three-total-attempt transient bound, technical outcomes, legacy/in-progress work and immediate officer access. Define public failure detail versus operational detail.
- Operator-settable provider, selected credentials/model and execution settings, common assessment/error/usage boundary, retained Gemini, immutable job selections, legacy compatibility and provider media coverage needed by this flow; observable usage/cost basis, unavailable usage/uncertain billing representation, processing time and attempt visibility. Respect ASOR-PD01 and no application budget-cap gate.

Exact endpoints, methods, codes, fields, schemas, validation bounds and error shapes belong to that contract, not this Plan. Its scope is these approved changes; it does not reopen unaffected identity/control contracts.

## Milestones

The sequence is strictly linear. Capability boundaries separate intake integrity, durable execution, provider/policy assessment, human-decision safety, officer presentation, citizen recovery and operational visibility. Each is independently testable and reviewable; a single feature-wide RED/GREEN would hide their different risks. Every repository-changing milestone needs reviewed Implementation Plan coverage and verification; the new M08C/M08D pair retains separate Implementation Plan reviews; completing one does not authorize the next. CONTRACT has its own reviewed deliverable instead.

No FOUNDATION is proposed: pytest/FastAPI and local persistence already exist. Missing AI production behavior is a RED condition. Existing harness repair is a behavior-preserving OTHER milestone, not production scaffolding. If inspection before a RED identifies a genuine additional executable prerequisite, stop and replan; do not smuggle setup into RED/GREEN.

### ASOR-M01 — External contract

- **Type:** CONTRACT. **Predecessor:** Plan approval.
- **Capability/purpose and rationale:** establish the changed consumer/operator behavior before any executable change.
- **Scope:** deliver and review the complete resulting contract covering every decision listed above, verified against the selected current baseline with explicit deltas.
- **Owned requirements/concerns:** ASOR-C01 contract decisions and compatibility delta; implements no behavioral requirement.
- **Exclusions:** executable changes, Implementation Plan, unreviewed new rejection grounds or legal scope.
- **Success criteria:** baseline/deltas reconciled, all listed decisions resolved consistently with requirements and model selection, and human approval recorded in the contract. Every contract verification check passes.

### ASOR-M02 — Safe current-demo verification harness

- **Type:** OTHER. **Predecessor:** ASOR-M01.
- **Capability/purpose and rationale:** establish trustworthy regression execution without changing production behavior; current fixture deletion/reloads/schema drift can invalidate later RED evidence.
- **Scope:** test-only lifecycle, schema/fixture and isolation corrections necessary for this work item's verification. Before M02 Implementation Plan approval, inventory the exact affected tests and baseline findings and obtain user-approved handling of each harness defect, contract mismatch and behavioral failure. Execution must not decide which assertions or failures to accept. The stale report-submission payload/status correction is included only as specified in Q15 below.
- **Owned requirements/concerns:** ASOR-C02 safe repeatable verification and evidence validity. No production requirement is implemented.
- **No-behavior-change statement:** changes are limited to exercising current behavior correctly and protecting local data; production behavior and existing assertions are not relaxed. Q15 corrects a stale expectation to the already approved contract, rather than changing required behavior. Assertions requiring changed production behavior belong in their capability RED, not here.
- **Baseline evidence:** source hazards at `tests/test_auth.py:18–28`, `tests/conftest.py:33–94,97–111,126–132,216–223`; record bounded isolated baseline execution and real outcomes before changes. A timeout is inconclusive, not valid RED or a pass.
- **Preserved tests:** active authentication/access-control/workflow tests in `tests/test_auth.py`, and compatible active history/timeline assertions in `tests/test_api_endpoints.py`; record actual coverage and unresolved contract drift individually. The twelve skipped media placeholders cannot be counted as preservation evidence.
- **Exclusions:** production changes, changed business expectations, deleting/skipping/weakening assertions to make checks pass, adopting historical infrastructure, claiming all tests passed because a selected subset did.
- **Success criteria/completion evidence:** harness checks and the exact preservation checks approved in M02's Implementation Plan pass in repeated isolated execution with explicit proof of isolated database/media paths and closed lifespan/resources. That approved plan must identify any existing failure, its disposition and approved later scope before execution; selected passing checks must never be reported as the entire baseline passing. No execution-time reassignment or weakening of expectations is allowed. If production changes or an unowned behavioral conflict are needed, stop and replan. All this milestone's verification commands pass; an unresolved failing check is not successful OTHER completion.

**Clarification Q15 — test disposition (2026-11-08):** The user confirmed “Correct the stale test to the approved contract.” In `tests/test_api_endpoints.py::TestCitizenReportSubmission::test_citizen_submit_report_returns_201_with_report_id`, the proposed test-only change may add the currently required `vehicle_number` to the payload and replace the stale `submitted` status expectation with the approved `awaiting-review` value. Retain the other HTTP 201, report ID, violation, citizen and timestamp checks. No production change or further assertion weakening is covered. This decision permits that exact correction in the M02 Implementation Plan; the Implementation Plan still requires its own review before repository execution.

### ASOR-M03 — Evidence intake RED

- **Type:** RED. **Predecessor:** ASOR-M02.
- **Capability/purpose and rationale:** expose actual upload/attachment defects before feeding private evidence to AI.
- **Scope:** checks for ASOR-R01 current-demo prerequisites, ASOR-R02 photo/video intake and ASOR-C03 ownership/attachment/file-boundary safety under the approved contract, including combined-evidence intake, duplicate/reassociation safety and no unrelated data loss.
- **Owned concerns:** verification only for ASOR-R01/R02 and ASOR-C03.
- **Exclusions:** production/scaffolding, AI assessment, broad rewrite, skipped placeholders as evidence.
- **Success criteria:** executable checks fail for these intended missing behaviors, not unrelated fixtures/dependencies; unchanged behavior remains checked and failures are explained.

### ASOR-M04 — Evidence intake GREEN

- **Type:** GREEN. **Predecessor:** ASOR-M03.
- **Capability/purpose and rationale:** make the evidence flow safe and usable before scheduling assessments.
- **Scope:** deliver ASOR-R01/R02 and ASOR-C03 as specified by M03 and the contract, including required current-demo upload/attachment/authorized evidence-access corrections and combined attachments.
- **Owned requirements/concerns:** ASOR-R01, ASOR-R02, ASOR-C03.
- **Exclusions:** unrelated media redesign, new violations, assessment/jobs, new tests.
- **Success criteria:** predecessor checks and relevant preservation checks pass, for both media types and mixed attachments, without mutating unrelated user data.

### ASOR-M05 — Durable processing RED

- **Type:** RED. **Predecessor:** ASOR-M04.
- **Capability/purpose and rationale:** verify restart and retry behavior independently of model quality.
- **Scope:** checks for ASOR-R15 recoverable background work, ASOR-R16 at most three total transient attempts with technical outcomes/officer availability, and ASOR-C04 durable state/data compatibility, duplicate execution and stale completion safety. Exercise pending and in-progress restart windows and consumed attempts across recovery.
- **Owned concerns:** verification only for ASOR-R15/R16 and ASOR-C04.
- **Exclusions:** live-model acceptance, dashboard/citizen presentation, production changes.
- **Success criteria:** intended behavior failures from runnable checks; unrelated infrastructure/setup errors are not RED evidence.

### ASOR-M06 — Durable processing GREEN

- **Type:** GREEN. **Predecessor:** ASOR-M05.
- **Capability/purpose and rationale:** deliver recoverable execution before live assessments depend on it.
- **Scope:** deliver ASOR-R15/R16 and ASOR-C04 verified by M05, preserving existing local claims/media/events while introducing durable work and technical outcome visibility to consumers. No error, timeout or exhausted attempt becomes rejection.
- **Owned requirements/concerns:** ASOR-R15, ASOR-R16, ASOR-C04.
- **Exclusions:** unbounded retries, a multi-instance service redesign, production legal adjudication, new tests.
- **Success criteria:** predecessor and relevant regression checks pass, including restart recovery and attempt accounting; no duplicate claim/award effects or lost committed work.

### ASOR-M07 — Gemini assessment and relevance policy RED

- **Type:** RED. **Predecessor:** ASOR-M06.
- **Capability/purpose and rationale:** isolate the model/provider boundary and the limited automated authority before UI integration.
- **Scope:** checks for ASOR-R03 live selected-model capability, R05 irrelevance-only automatic screen-out, R06 whole-submission relevance, R07 advisory recommendation, R08 reviewed national-rule scope and R09 grounded notes/limitations/separate scores. Include both media types, all three categories, mixed attachments, relevant/no-apparent-violation, uncertainty, malformed/unsupported outputs and provider failure. ASOR-C05 covers untrusted evidence/model text, unauthorized evidence/secret exposure and preventing output from granting new authority.
- **Owned concerns:** verification only for ASOR-R03/R05–R09 and ASOR-C05. M17 later supplies completed live end-to-end acceptance evidence; substitute-only evidence cannot close R03.
- **Exclusions:** model-created law/fines, confidence-only rejection thresholds, final decisions/points, production changes.
- **Success criteria:** runnable checks fail for intended missing integration/policy behavior; the approved check protocol identifies inputs and observations for later live verification. Provider access/setup failure is not valid RED evidence.

### Correction revision rationale and boundary — 2026-11-09

[Actual M08 execution](ASOR-M08-Execution-2026-11-09.md) passed the offline pairs but stopped on the first photo: `PROVIDER_REQUEST_REJECTED`, one consumed attempt, no assessment, officer-reviewable and zero points. Its original HTTP status/stage/reason was not retained and remains unknown. [Read-only diagnosis](ASOR-M08-Live-Diagnosis-2026-11-09.md) separately confirms decoded-response bytes crossing the child/parent boundary with retained encoding headers, causing double decoding for gzip. Metadata GET 200 establishes key/model metadata access only; it proves neither inference/upload acceptance nor that framing caused the original rejection. The remaining live cases are NOT RUN.

**Decomposition: one pair.** One cohesive correction RED/GREEN pair is the fewest reviewable decomposition: framing integrity and safe failure capture address the same bounded provider-response boundary and can be verified together offline. Existing harness/process facilities support RED; no FOUNDATION or new external contract is needed. C05 owns this transport/privacy correction; CT17 already defines safe status/class failure detail. The pair supplies minimal capture for subsequent diagnosis, while M15/M16 retain full R18/C09 operator presentation, accounting, logs and cost scope. It introduces no new diagnostic endpoint or external representation, and cannot close R03 or replace resumed M08 live evidence.

### ASOR-M08A — Bounded provider response correction RED

- **Type:** RED. **Predecessor:** completed ASOR-M07 and recorded stopped M08 execution/diagnosis; revised Plan approval.
- **Capability/purpose and rationale:** expose the confirmed framing defect and missing safe diagnostic capture at the real child/parent boundary before correction.
- **Scope:** meaningful offline checks for compressed/gzip and uncompressed response framing through the actual bounded child/parent path rather than only MockTransport; decoded bytes and response metadata must remain mutually consistent with no double decoding. Check minimal per-attempt provider HTTP status (when actually observed), request stage and allowlisted diagnostic class capture for unsuccessful HTTP/transport outcomes; absent values remain explicitly unknown. Verify that raw provider bodies/messages, keys, token URLs, private paths, evidence and prompts cannot enter persisted diagnostic detail or logs. Preserve classifications, absolute attempt deadlines across serialization/startup/network/reconstruction, timeout kill/reap before return, no overlapping orphan requests and no additional inference or retry multiplication.
- **Owned requirements/concerns:** verification of the bounded correction within ASOR-C05 and existing CT15–17; supplements M07 without reopening its completed evidence. R03/R05–R09 remain M08-owned; R18/C09 full delivery remains M16-owned.
- **Exclusions:** production/configuration changes, live requests or private media/key reads, new business/contract behavior, retry/model/output-policy changes, full operational presentation or accounting.
- **Success criteria:** runnable deterministic checks demonstrate intended missing framing/capture behavior, with no import/environment failures mislabelled RED. Deadline, kill/reap, privacy and attempt-bound preservation checks retain meaningful assertions. The Implementation Plan defines exact safe isolated commands and evidence; no root pytest or real application startup. No live call is needed to establish RED.

### ASOR-M08B — Bounded provider response correction GREEN

- **Type:** GREEN. **Predecessor:** verified ASOR-M08A.
- **Capability/purpose and rationale:** correct the same bounded response boundary with the smallest production change supported by RED.
- **Scope:** make child/parent bytes and framing/encoding metadata consistent for compressed and plain HTTP responses; retain minimal sanitized per-attempt observed HTTP status, request stage and allowlisted diagnostic class under existing CT17. Preserve null/unknown when status or stage cannot be established; do not invent the original rejection cause. Preserve existing failure classification, public generic failures, officer referral, attempt accounting, absolute deadlines, kill/reap, owned-resource cleanup and privacy. No extra inference, nested retries or expanded total-attempt bound.
- **Owned requirements/concerns:** ASOR-C05 bounded transport/diagnostic correction verified by M08A; minimal capture only under CT17. M08 retains assessment/live capability and M16 retains full R18/C09 visibility delivery.
- **Exclusions:** new tests, live calls, raw provider payload retention, new provider/model/SDK/configuration, output-validation relaxation, new endpoint or full operational UI/accounting.
- **Success criteria:** all M08A checks and unchanged original 47 Gemini, 14 durable and 94 intake/preservation checks pass with the 12 existing skips explicitly distinguished; no weakening of assertions or substitution for live evidence. The reviewed isolated protocol proves deadline/kill/reap/privacy/no-retry-multiplication preservation and original dirty checkout/private data protection. Correction completion authorizes neither M08 retry nor M09.

### Provider-boundary revision and decomposition — 2026-11-10

**Decomposition: one pair.** M08C/M08D form one cohesive provider-selection capability with separate RED/GREEN execution statuses and separately reviewed Implementation Plans. The contract amendment makes v0.16's small-change paired-plan shortcut ineligible. Joint contract/Plan approval comes first, followed by M08C's reviewed exact tests, verified RED, and M08D's reviewed exact production changes. Within GREEN, establish and verify the common gateway with retained Gemini first, then implement OpenAI against that boundary, matching Q16's order; these are ordered delivery steps, not hidden milestones. Existing isolated harness and provider-response facilities permit meaningful RED; absent target provider behavior is RED, not a reason for FOUNDATION. No new dependency/service is selected here.

The amended contract affects executed durable snapshot checks (M05/M06), Gemini assessment/policy checks (M07/stopped M08), and transport/diagnostic checks (M08A/M08B). M08C maps each affected amended rule to a new check or same-coverage replacement and distinguishes preserved passing checks from genuine missing-behavior RED. Existing Gemini expectations stay exercised with explicit Gemini selection; historical evidence is not rewritten or reused as OpenAI proof. M15/M16 retain full operational presentation/accounting delivery.

### ASOR-M08C — Configurable gateway and OpenAI RED

- **Type:** RED. **Predecessor:** ASOR-M08B; execution additionally requires joint approval of this Plan and amended contract, then its own reviewed Implementation Plan.
- **Capability/purpose and rationale:** prove the missing configurable common provider boundary and current OpenAI integration together while protecting retained Gemini behavior.
- **Scope:** checks for R20 and the prerequisite provider-integration behavior supporting R03 under amended CT11/CT12/CT15–CT18: explicit selection, common assessment/error/usage behavior, immutable job selection through retry/restart, compatible legacy Gemini work, safe invalid configuration and no automatic fallback. Verify contract-defined OpenAI media preparation/coverage, combined evidence, incomplete-video human referral, output normalization, privacy/authority and minimum provider-attributed usage capture needed by the new boundary. Map all affected amended contract rules, including existing executed-test expectations, without weakening coverage. Preserve R05–R09 common policy, R04 no-cap, R15/R16 attempts/deadline/recovery, human-final decisions and existing intake/transport safety as passing preservation checks, not new RED claims.
- **Owned requirements/concerns verified:** R20; prerequisite provider-integration checks supporting R03 completion at M08, without a second R03 delivery owner; C05 new-provider trust boundary and C09 minimum usage-input capture. R05–R09 are preserved and remain originally delivered/verified by M08/M07; full R18/C09 presentation remains M16/M15.
- **Exclusions:** production changes, private/live inputs, live provider calls, new dependency/service, fallback, spending/pricing gate and full operational presentation.
- **Success criteria:** missing gateway/OpenAI behavior yields intended ordinary assertion failures; preserved checks pass; no unrelated environment/import failure counts as RED. Affected-contract coverage and positive-before-negative checks are reviewable, with no fabricated usage/coverage metadata. Existing state/config isolation facilities suffice; otherwise stop for replanning.

### ASOR-M08D — Configurable gateway and OpenAI GREEN

- **Type:** GREEN. **Predecessor:** verified ASOR-M08C.
- **Capability/purpose and rationale:** satisfy the same cohesive RED capability inside the existing local monolith.
- **Scope:** deliver R20 gateway/adapters/configuration and common-boundary integration needed by R03 under the amended contract, first common gateway/retained Gemini, then OpenAI. Keep workflow/officer/awards independent of provider translation. Preserve immutable job selections and historical Gemini data/work, common policy/security/retries, private media authority and safe technical failure. Deliver contract-required OpenAI media coverage/referral and minimum attributed usage inputs without fabricated legacy values; later M16 still owns full operator display/cost accounting.
- **Owned requirements/concerns:** R20 only for gateway/adapters/configuration/common boundary; R03 remains solely M08-owned and consumes this prerequisite implementation evidence; C05 new-provider boundary; C09 minimum usage-input capture only.
- **Exclusions:** new service/dependency selection, unrelated redesign, automatic fallback/cap, live acceptance, full M16 presentation and any waiver of both-media evidence.
- **Success criteria:** M08C's new and affected checks pass with retained explicit-Gemini behavior, legacy compatibility and unchanged common policy/safety. Run affected checks first and the full approved isolated current-demo suite once at GREEN execution; repeat only state/configuration checks that require isolation/repeatability evidence. Record the effective provider setting and named inventory, verify protected source/data against the execution manifest and existing skips. No live call is needed or authorized by this milestone. Completion does not authorize resumed M08.

### ASOR-M08 — Current selected-provider live assessment GREEN (resumed)

- **Type:** GREEN. **Predecessor:** ASOR-M08D. Original M07 RED and stopped M08/offline/live evidence remain required historical inputs.
- **Capability/purpose and rationale:** finish original assessment/live acceptance using explicitly selected OpenAI under Q16, while retaining Gemini.
- **Scope:** original R05–R09/C05 assessment delivery and R03 selected-provider delivery including actual live acceptance, using the amended contract and M08D integration. Original advisory observations, reviewed national references, uncertainty, labelled scores, combined-evidence policy and irrelevance-only automatic screen-out remain unchanged.
- **Owned requirements/concerns:** R03 in full, including actual selected-provider live acceptance; R05, R06, R07, R08, R09; C05 original assessment behavior. M08D delivers the R20 prerequisite gateway/OpenAI integration; it cannot complete R03 without this live evidence.
- **Resumption and evidence:** a newly reviewed M08 Implementation Plan starts from verified M08D, stopped 007, completed 009/checkpoints and both failed live histories. Use recorded manifests to confirm applicability of the latest full suite; rerun affected checks only when state/configuration or protocol changes require it, rather than repeating unchanged broad loops. Follow image-first OpenAI execution and preserve the original category, mixed/unclear/relevant/irrelevant, grounding and routing met/not-met rules. Manual video remains NOT RUN until the user actually provides verification evidence; photos cannot close both-media acceptance. Incomplete sampled video follows the amended contract's human-referral rule. Missing inputs keep this milestone incomplete. Retained Gemini's 402 does not require another Gemini live call before current OpenAI testing, and is not a claim of resolved billing. Record sanitized failure evidence and stop on a failed criterion; no retry-until-success, inferred cause, substitution or waiver.
- **Exclusions:** new production/tests, application cap, fallback, unsupported legal extensions, AI-final awards/decisions and Gemini billing remediation.
- **Success criteria:** actual selected-model OpenAI photo and video evidence meets original acceptance plus amended coverage rules, with privately supplied credentials and recorded model/prompt/case/pricing context; retained Gemini is verified as configured preservation. No deterministic-accuracy claim or calibrated-probability claim. Both-media evidence remains required for completion.

### ASOR-M09 — Officer decisions and late-result safety RED

- **Type:** RED. **Predecessor:** ASOR-M08.
- **Capability/purpose and rationale:** establish the human authority boundary before expanding dashboard actions.
- **Scope:** checks for ASOR-R11 immediate authenticated officer access/approve/reject/request-information/override across every AI state, R12 human-only final decision/award, R17 late-result invariance, and ASOR-C06 competing/repeated actions and decision/award/event consistency. Prove AI processing is active before asserting it cannot change a finalized decision; include completion before/after finalization and recovered work.
- **Owned concerns:** verification only for ASOR-R11/R12/R17 and ASOR-C06.
- **Exclusions:** new point schedules, UI layout, citizen appeal workflow, production changes.
- **Success criteria:** runnable checks demonstrate the specific missing action/concurrency protections; no vacuous no-AI-effect test is accepted.

### ASOR-M10 — Officer decisions and late-result safety GREEN

- **Type:** GREEN. **Predecessor:** ASOR-M09.
- **Capability/purpose and rationale:** deliver immediate officer authority and atomic outcomes independent of AI timing.
- **Scope:** deliver ASOR-R11/R12/R17 and ASOR-C06 verified by M09, including required existing reject/request-information corrections and screen-out override. Existing point mapping remains; late/duplicate AI work cannot overwrite final decisions or points.
- **Owned requirements/concerns:** ASOR-R11, ASOR-R12, ASOR-R17, ASOR-C06.
- **Exclusions:** automatic AI awards, unrelated decision redesign or new tests.
- **Success criteria:** predecessor and relevant regression checks pass, including authenticated access in all AI states and concurrent/late-result scenarios with consistent decision/points/events.

### ASOR-M11 — Officer dashboard RED

- **Type:** RED. **Predecessor:** ASOR-M10.
- **Capability/purpose and rationale:** verify visible workflow distinctions separately from decision correctness.
- **Scope:** checks for ASOR-R10 counts/views and ASOR-C07 officer presentation of every AI stage, assessment explanations/scores/citations, and immediate actions already delivered by M10. Distinguish recommendations, intake screen-out, technical failure and officer-final outcomes, using approved membership/refresh semantics and authorized access.
- **Owned concerns:** verification only for ASOR-R10 and ASOR-C07.
- **Exclusions:** new decision policy, operational accounting implementation, production changes.
- **Success criteria:** executable API/browser checks fail for intended missing dashboard behavior, with meaningful count/detail/action assertions.

### ASOR-M12 — Officer dashboard GREEN

- **Type:** GREEN. **Predecessor:** ASOR-M11.
- **Capability/purpose and rationale:** deliver the officer's review surface on the verified authority boundary.
- **Scope:** deliver ASOR-R10/ASOR-C07 verified by M11: required views/counts, full case access, advisory explanation presentation and available actions in every AI state, with safe rendering of untrusted text.
- **Owned requirements/concerns:** ASOR-R10, ASOR-C07.
- **Exclusions:** AI-final decisions, a dashboard-only access-control boundary, new tests.
- **Success criteria:** predecessor and relevant regression checks pass; required distinctions and actions work through the actual browser and API.

### ASOR-M13 — Citizen recovery RED

- **Type:** RED. **Predecessor:** ASOR-M12.
- **Capability/purpose and rationale:** verify the complete recovery path after intake screen-out.
- **Scope:** checks for ASOR-R13 specific citizen explanation/resubmission/review request and R14 same-claim marked manual-review queue retaining evidence and AI explanation; ASOR-C08 citizen ownership, safe explanation rendering and race/repeated-action handling under the contract. Include competing officer finalization so recovery cannot silently undo a final decision.
- **Owned concerns:** verification only for ASOR-R13/R14 and ASOR-C08.
- **Exclusions:** separate appeal records, new rejection reasons, production changes.
- **Success criteria:** runnable checks fail for intended missing citizen/queue behavior and assert identifier/evidence/explanation preservation and unauthorized access rejection.

### ASOR-M14 — Citizen recovery GREEN

- **Type:** GREEN. **Predecessor:** ASOR-M13.
- **Capability/purpose and rationale:** complete the user-visible response to automatic intake screen-out.
- **Scope:** deliver ASOR-R13/R14/ASOR-C08 verified by M13 across citizen explanation/actions and the officer's marked same-claim queue. Retain evidence and AI explanation rather than replacing them with a separate appeal.
- **Owned requirements/concerns:** ASOR-R13, ASOR-R14, ASOR-C08.
- **Exclusions:** separate appeal aggregate, bypass of officer finality, new tests.
- **Success criteria:** predecessor and relevant regression checks pass through API/browser workflow, including preserved same-claim context and authorization.

### ASOR-M15 — Operational visibility RED

- **Type:** RED. **Predecessor:** ASOR-M14.
- **Capability/purpose and rationale:** verify that the completed flow explains its execution and cost without exporting sensitive payloads.
- **Scope:** checks for ASOR-R18 dashboard status/counts/reasons, operational attempts/failures/time/usage/cost and ASOR-C09 attribution, effective pricing/estimate basis, incomplete usage handling, and safe logs. Cover successful calls, retries, technical failures and restart recovery; absence of provider usage must not silently mean zero cost.
- **Owned concerns:** verification only for ASOR-R18 and ASOR-C09.
- **Exclusions:** exported telemetry, alerts, spending-cap enforcement or performance SLA, production changes.
- **Success criteria:** runnable checks fail for intended missing visibility/accounting, while making no invented billing certainty claim.

### ASOR-M16 — Operational visibility GREEN

- **Type:** GREEN. **Predecessor:** ASOR-M15.
- **Capability/purpose and rationale:** make required processing/cost evidence accessible for this local demo.
- **Scope:** deliver ASOR-R18/ASOR-C09 verified by M15, joining existing dashboard state with job attempts/failures/time and attributed AI usage/cost, including uncertainty and pricing basis, without exposing credentials or raw private evidence in logs.
- **Owned requirements/concerns:** ASOR-R18, ASOR-C09.
- **Exclusions:** cap gates, exported telemetry/alerting projects, new tests.
- **Success criteria:** predecessor and relevant regression checks pass; demo operators can inspect all requested information across success/retry/recovery/failure paths.

### ASOR-M17 — Controlled live-demo acceptance

- **Type:** OTHER. **Predecessor:** ASOR-M16.
- **Capability/purpose and rationale:** validate the already delivered capabilities together in the selected single-local-instance demo; this boundary supplies acceptance evidence rather than inventing missing integration behavior.
- **Scope:** execute a reviewed validation protocol for ASOR-AC01–AC12: actual photo/video intake to explicitly selected OpenAI with retained Gemini configuration coverage, officer dashboard/actions, citizen recovery, restart survival, late-result safety and operational evidence. Preserve ASOR-R19's existing single-local-instance topology.
- **Owned concerns:** ASOR-C10 integrated acceptance evidence only. Behavioral requirements keep their earlier delivery owners; ASOR-R04 remains an exclusion and ASOR-R19 a preserved deployment constraint.
- **No-behavior-change statement:** no production, test, dependency or configuration change is authorized. The only repository deliverable is recorded validation evidence. Any behavioral defect stops validation for replanning of the owning capability; this milestone cannot fix whatever fails.
- **Baseline evidence:** approved M04/M06/M08/M10/M12/M14/M16 GREEN evidence and M02's exact approved preservation/baseline disposition. Confirm their recorded success and current applicability before starting.
- **Inputs and protocol:** the user supplies selected OpenAI credentials privately and representative demo photos/videos for helmet, triple-riding and red-light, plus clearly irrelevant, relevant/no-apparent-violation, unclear/uncertain and mixed relevant/irrelevant evidence. The Implementation Plan identifies each input, who supplies it, its approved noncommitted local location, the exact commands/browser steps, repeatable model-evaluation procedure, expected observation and met/not-met rule before approval. It includes independent citizen/officer sessions, pending/in-progress restart cases, a real active AI call during officer finalization followed by completion, the three-attempt technical-failure check and usage/cost observations. Existing approved checks may supply controlled failure evidence; simulated results cannot substitute for the required successful live photo/video demonstration. Missing credentials/media cause Waiting, not assumed acceptance. No additional accuracy threshold or latency target is introduced.
- **Preserved tests:** the exact approved M02 preservation set, plus the behavior checks delivered by M03/M05/M07/M09/M11/M13/M15, including their authorized ownership, decision/points/event and citizen-context checks. Record selected coverage and every unexecuted/inconclusive check explicitly; do not claim an all-suite pass from a subset.
- **Exclusions:** executable changes, new behavior, deployment redesign, arbitrary accuracy/performance targets, substitute-only acceptance, unbounded retries and self-approval of release.
- **Success criteria/completion evidence:** all protocol checks and preserved checks pass, all twelve ASOR acceptance criteria have concrete observations, and evidence identifies model/prompt/input context, official pricing basis, actual usage/cost and uncertainty without secrets. The uncapped-call exclusion and preserved single-instance topology are explicitly inspected. Any defect is recorded and stops completion pending the normal review/replanning path; no failure is waived during execution. Stop all started processes and record cleanup. Final Review independently evaluates the result.

## Requirement Traceability

Each approved behavioral requirement has exactly one delivery owner; exclusions and preserved constraints have none; RED identifies its primary executable verification. Later end-to-end evidence supplements those checks without creating a second owner.

| Requirement / Concern | Owning Milestone | Verifying Milestone |
| --- | --- | --- |
| ASOR-R01 current demo and prerequisite fixes | ASOR-M04 | ASOR-M03 |
| ASOR-R02 photos and videos | ASOR-M04 | ASOR-M03 |
| ASOR-R03 retained providers/current OpenAI | ASOR-M08 | ASOR-M07 original assessment; ASOR-M08C provider-integration prerequisite checks; M08 live acceptance |
| ASOR-R04 no application spending cap | none — exclusion | Final Review |
| ASOR-R05 irrelevance-only automatic screen-out | ASOR-M08 | ASOR-M07 |
| ASOR-R06 combined-attachment relevance | ASOR-M08 | ASOR-M07 |
| ASOR-R07 advisory recommendation | ASOR-M08 | ASOR-M07 |
| ASOR-R08 three categories/national rules | ASOR-M08 | ASOR-M07 |
| ASOR-R09 grounded explanation and separate labelled scores | ASOR-M08 | ASOR-M07 |
| ASOR-R10 officer dashboard counts/views | ASOR-M12 | ASOR-M11 |
| ASOR-R11 officer access/actions at every AI stage | ASOR-M10 | ASOR-M09 |
| ASOR-R12 human-final decisions/awards | ASOR-M10 | ASOR-M09 |
| ASOR-R13 citizen explanation and recovery | ASOR-M14 | ASOR-M13 |
| ASOR-R14 same-claim manual review | ASOR-M14 | ASOR-M13 |
| ASOR-R15 background/restart recovery | ASOR-M06 | ASOR-M05 |
| ASOR-R16 transient attempt bound/technical failures | ASOR-M06 | ASOR-M05 |
| ASOR-R17 late-result safety | ASOR-M10 | ASOR-M09 |
| ASOR-R18 local operational visibility | ASOR-M16 | ASOR-M15 |
| ASOR-R19 single-local-instance deployment | none — preserved | ASOR-M17 |
| ASOR-R20 configurable gateway | ASOR-M08D | ASOR-M08C |
| R05–R09 common policy after provider amendment | none — preserved | ASOR-M08C |
| ASOR-C01 external decisions/compatibility delta | ASOR-M01 | Human review of ASOR-M01 |
| ASOR-C02 safe repeatable harness/evidence | ASOR-M02 | ASOR-M02 |
| ASOR-C03 intake ownership/attachment/file-boundary safety | ASOR-M04 | ASOR-M03 |
| ASOR-C04 durable data compatibility/duplicates/stale work | ASOR-M06 | ASOR-M05 |
| ASOR-C05 evidence/model trust boundary and secret protection | ASOR-M08 assessment; ASOR-M08B bounded transport/minimal diagnostic correction; ASOR-M08D new-provider boundary | ASOR-M07 assessment; ASOR-M08A correction; ASOR-M08C new-provider boundary |
| ASOR-C06 decision/award/event race consistency | ASOR-M10 | ASOR-M09 |
| ASOR-C07 officer presentation/access/safe rendering | ASOR-M12 | ASOR-M11 |
| ASOR-C08 citizen ownership/preservation/race safety | ASOR-M14 | ASOR-M13 |
| ASOR-C09 minimum new-provider usage inputs | ASOR-M08D | ASOR-M08C |
| ASOR-C09 full usage/cost presentation and safe logs | ASOR-M16 | ASOR-M15 |
| ASOR-C10 integrated acceptance evidence | ASOR-M17 | ASOR-M17 |
| Original multi-service redesign/general rewrite | none — exclusion | Final Review |
| AI-final violations/awards; rejection on technical failure | none — exclusion | Final Review |
| Separate appeal record | none — exclusion | Final Review |
| Additional categories/state/local legal additions | none — exclusion | Final Review |
| Exported telemetry/alerts | none — not required | none |
| Capacity/latency/uptime targets | none — not required | none |
| Existing points mapping and unrelated identity/control behavior | none — preserved | ASOR-M09 and ASOR-M17 preservation checks |
| Review evidence against all ASOR-AC criteria, scope and model selection; identify README/old roadmap statements made false without editing them in review | none — Final Review obligation | Final Review |

ASOR-C concerns are Plan-level delivery/preservation safeguards derived from the inspected paths and approved flow; they are proposed for this Plan's review, not additional user business requirements. ASOR-PD01 is the delegated planning model decision and is carried by ASOR-R03's owner rather than a second delivery requirement.

## Verification Commands

No verification command below was executed during planning. Exact safe working directories, fixture corrections, bounded execution, case selectors and any new verification entry points belong to the milestone Implementation Plans. No existing root-directory test invocation is safe by assumption.

| Command / check | Source and intended use |
| --- | --- |
| `python -m pytest --collect-only -q tests/test_auth.py tests/test_api_endpoints.py tests/test_media.py` | Existing pytest configuration and files. Run only in the approved isolated verification environment after source/fixture review; collection itself can execute imports/fixtures. Inventory active/skipped checks; not behavioral evidence. |
| `python -m pytest -q tests/test_auth.py` | Existing authentication/access-control/workflow tests. M02 preservation/harness baseline and later regressions, only with verified isolated DB/media paths and bounded execution; never in the user's live working directory. |
| `python -m pytest -q tests/test_api_endpoints.py` | Existing reporting/officer tests. Inventory current contract/assertion drift at M02; approved M03/M09/M13 RED checks own affected behavior expectations. Do not treat this command as known passing or silently weaken it. |
| `python -m pytest -q tests/test_media.py` | Existing media placeholders, explicitly not acceptance or RED evidence while skipped. M03's Implementation Plan defines executable contract-based replacement coverage; retain visibility of skipped/unimplemented coverage. |
| `python -m pytest -q tests/test_identity.py tests/test_controls.py` | Existing unrelated identity/control safety net. Inspect their fixture/runtime prerequisites before selecting a safe bounded invocation; failures need classification, not the old service redesign. Real-infrastructure tests are not silently claimed run by these checks. |
| Approved milestone-specific checks and actual HTTP/browser/live demonstration protocol | ASOR-AC01–AC12. RED Implementation Plans define precise checks and necessary representative inputs; GREEN executes those checks. Include real transport for changed errors, actual browser actions, restart recovery and competing officer/AI completion. Record model/prompt/case version and repeatable observations separately from deterministic assertions. |

The existing workflow's `python tools/check.py` checks old multi-role infrastructure and reads `/private/ca.crt`; it is not a current-demo verification command for this work item. No build, Docker startup or costly planning dry run is required. Select the new and affected checks for each milestone from its changed behavior and contract mapping. GREEN execution runs the full approved isolated current-demo suite once, then repeats only persistent-state/configuration checks requiring isolation evidence; unchanged checkpoint inventories/manifests establish applicability without redundant broad reruns. Final Review reruns only if no full run covers the current source state. Unrelated baseline failures, timeouts and absent prerequisites remain visible and cannot be relabelled successful verification. Stop/replan where they invalidate a milestone's success criteria. Do not add provider-free CI as a new business acceptance requirement; preserve the existing unrelated workflow and use live calls for the approved demo.

## Execution Status

| Milestone | Status | Evidence / Notes |
| --- | --- | --- |
| ASOR-M01 External contract | Completed — user approval 2026-11-08 | [Approved external contract](External-Contract.md), including ASOR-CT01–18, baseline/deltas, reviewed national references and contract verification. No executable change. |
| ASOR-M02 Safe verification harness OTHER | Completed — executed 2026-11-09 | [Execution evidence](ASOR-M02-Execution-2026-11-09.md): exact five test files; two isolated runs each 41 passed, 12 existing skips; protected hashes and owned cleanup verified. |
| ASOR-M03 Evidence intake RED | Completed - executed 2026-11-09 | [Execution evidence](ASOR-M03-Execution-2026-11-09.md): exact three test/harness files; two isolated preservation runs each 40 passed/12 existing skips; two classified RED runs each 54 intended assertions, no errors/new skips; protected runner hashes and owned cleanup verified; invocation/private-evidence limitations disclosed. |
| ASOR-M04 Evidence intake GREEN | Completed — executed 2026-11-09 | [Execution evidence](ASOR-M04-Execution-2026-11-09.md): exact three approved production files; unchanged isolated pair each 94 passed/12 existing skips; matching106-node inventories, synthetic legacy migration twice/integrity/FK checks, protected preimages and owned cleanup verified; private recovery backup retained, real DB unmigrated and byte-identical. |
| ASOR-M05 Durable processing RED | Completed — executed 2026-11-09 | [Execution evidence](ASOR-M05-Execution-2026-11-09.md): exact two approved test/helper files; isolated preservation pair each94 passed/12 existing skips; RED pair each14 intended pending assertions, no errors/skips; identical inventories, original protected bytes and owned cleanup verified. |
| ASOR-M06 Durable processing GREEN | Completed — executed 2026-11-09 | [Execution evidence](ASOR-M06-Execution-2026-11-09.md): exact three approved production files; unchanged durable pair each14 passed/no errors or skips; unchanged preservation pair each94 passed/12 existing skips; equal inventories, synthetic default/startup probes, protected original bytes and owned cleanup verified. Real migration/startup deferred; private recovery retained. |
| ASOR-M07 Gemini assessment RED | Completed — executed 2026-11-09 | [Execution evidence](ASOR-M07-Execution-2026-11-09.md): exact two approved test/check additions; unchanged durable pair14 passes each; intake pair94 passes/12 existing skips each; Gemini RED pair47 exact intended ordinary failures each; equal full inventories, protected original180-file bytes and owned cleanup verified. No live provider call; M08 remains Pending. |
| ASOR-M08A Bounded provider response correction RED | Verified | [Checkpoint execution](ASOR-M08A-Checkpoint-Execution-2026-11-10.md) matched both archived RED runs and verified Gemini (47 passes each), durable (14 passes each), intake (94 passes and 12 existing skips each) and scratch soundness (13 passes each). Protected checkout and frozen scratch hashes matched. |
| ASOR-M08B Bounded provider response correction GREEN | Completed | [Verified execution](ASOR-M08B-Execution-2026-11-10.md) on 2026-11-10. Two passes each reported 168 passed and the same 12 existing skips across 180 named outcomes. |
| ASOR-M08C Configurable gateway and OpenAI RED | Completed - executed 2026-11-10 | [Verified RED execution](ASOR-M08C-Execution-2026-11-10.md): two exact29 ordinary missing-selection failure inventories, zero errors/skips; affected preserved node1 pass; source hashes/metadata and owned cleanup verified. |
| ASOR-M08D Configurable gateway and OpenAI GREEN | Blocked — continuation stopped 2026-11-11 | [Continuation evidence](ASOR-M08D-Continuation-2026-11-11.md): transport7 passes; whole intake300s timeout, fine-group continuation stopped on MP4 upload400 vs201; remaining intake/repeat42 NOT RUN. Sources/protection/owned cleanup verified; Gemini-specific verification deferred; original failure retained. |
| ASOR-M08 Current selected-provider live assessment GREEN | Pending | Revised behind M08D and a newly reviewed OpenAI live protocol. Historical [image rerun](ASOR-M08-Live-Image-Rerun-2026-11-10.md): Gemini upload-start HTTP 402, one attempt/no assessment; remaining photos NOT RUN and video NOT RUN — manual verification later. Q16 supersedes Gemini-only live selection, without resolving billing. [Original execution](ASOR-M08-Execution-2026-11-09.md) and [diagnosis](ASOR-M08-Live-Diagnosis-2026-11-09.md), stopped 007 and completed 009 remain historical. |
| ASOR-M09 Officer decisions RED | Pending | No Implementation Plan or execution. |
| ASOR-M10 Officer decisions GREEN | Pending | No Implementation Plan or execution. |
| ASOR-M11 Officer dashboard RED | Pending | No Implementation Plan or execution. |
| ASOR-M12 Officer dashboard GREEN | Pending | No Implementation Plan or execution. |
| ASOR-M13 Citizen recovery RED | Pending | No Implementation Plan or execution. |
| ASOR-M14 Citizen recovery GREEN | Pending | No Implementation Plan or execution. |
| ASOR-M15 Operational visibility RED | Pending | No Implementation Plan or execution. |
| ASOR-M16 Operational visibility GREEN | Pending | No Implementation Plan or execution. |
| ASOR-M17 Controlled live-demo acceptance OTHER | Pending | No Implementation Plan or execution. |

Future execution evidence belongs below this table: actual commands with trimmed real output, deviations and reasons, input/model context without secrets, and process cleanup. No planning-time result is milestone execution evidence.

## Risks

The original source observations below are retained historical risks; completed intake/durable/correction evidence records their delivered safeguards. They do not reopen completed milestones. The current provider-hardwiring risk and amendment scope are recorded in the November 10 baseline above.

| Risk and evidence | In-scope response / boundary |
| --- | --- |
| Unsafe live-data test fixture and schema/lifespan mismatch (`tests/test_auth.py:18–28`; `tests/conftest.py:33–94,97–111,216–223`) can destroy data or produce misleading failures. | M02 establishes safe evidence before behavioral RED; no root DB/media/private-local mutations, assertion weakening or all-pass claim from a timeout. |
| Upload identity bypass, filename use, unowned attachment/reassignment and unauthenticated media (`app.py:183,636,679,758–779,904–929`) can prevent the demo or expose someone else's evidence to Gemini. | M03/M04 correct the required authenticated intake/evidence boundary before AI processing. Contract owns compatibility and duplicate semantics; no unrelated identity redesign. |
| Current single SQLite connection (`bootstrap.py:30,160`) and pretransaction status check (`app.py:1204–1226`) do not establish safe background/officer coordination. | M05/M06 verify durable recovery/duplicate protection; M09/M10 verify decision races, points and events. Single instance does not remove concurrency risk. |
| Existing rejection references an undefined value (`app.py:1261`) and awaiting-review guard excludes other stages (`app.py:1215`). | Required officer-action corrections are explicitly owned by M10 and driven by M09. |
| Current schema has media AI fields but no job lifecycle (`bootstrap.py:91–109`); model failure after a provider response may leave uncertain billing or recovery state. | M06 owns recoverable attempts; M08 owns technical output handling; M16 makes usage/cost uncertainty explicit. Three total transient attempts and no technical rejection remain unchanged. |
| Browser uses interpolated HTML (`templates/officer-detail.html:77–131`) and AI/evidence text is untrusted. | M08 restricts model authority and reviewed citations; M12/M14 verify safe rendering and authorization. Do not treat text in evidence as operational instructions. |
| Stale optional-OpenAI roadmap and incompatible media constants (`.env.example:82–85`; `docs/Plan.md:349`; `media.py:31–57`; `app.py:640–665`) can be mistaken for authority. | M01 defines only approved deltas from selected runtime; M08D carries configurable retained Gemini/current OpenAI integration. Final Review lists stale user-facing statements for the user to update. |
| Skipped media coverage and active-but-drifted API tests (`tests/test_media.py`; `tests/test_api_endpoints.py:35–61`) cannot substantiate readiness. | M02 records baseline classification; each RED provides real executable requirement evidence. Do not copy historical test counts/hashes or claim skipped assertions pass. |
| Live provider capability/availability/pricing can change; visual observations and legal applicability may be wrong (official model/deprecation/pricing sources above). | Verify supported model/account access during approved execution; retain uncertainty and human-final authority; review national sources in M01 and live representative evidence in M08/M17. No accuracy promise, invented fines, silent substitution or cap gate. |

## Final Acceptance Criteria

| Criterion | Source | Demonstrated by |
| --- | --- | --- |
| Photo and video can enter the selected current demo with required prerequisites fixed. | ASOR-AC01 / R01/R02 | M04 checks; M17 complete live flow. |
| Actual selected-model OpenAI calls occur for current testing without an application spending cap; Gemini remains configured and available. | ASOR-AC02 / R03/R04; Q16 / ASOR-PD01 | M08D retained-provider checks; M08 live evidence; M17 live demonstration. |
| Provider configuration selects a common assessment/error/usage gateway; another adapter does not require rewriting claim/officer/award behavior. | ASOR-AC12 / R20 | M08D deterministic integration and boundary evidence; M17 configuration validation. |
| Only clearly irrelevant intake screens out; everything else reaches an officer, with no technical rejection. | ASOR-AC03 / R05/R07/R13/R16 | M06/M08 behavior; M14 citizen presentation; M17 representative cases. |
| Mixed relevant/irrelevant attachments do not wrongly screen out the claim. | ASOR-AC04 / R06 | M08 combined-evidence checks and M17 case. |
| Each selected category shows observations/recommendation/reviewed national references/limitations and separate labelled self-assessed scores. | ASOR-AC05 / R07/R08/R09 | M08 assessment evidence, M12 browser display, M17 reviewed cases. |
| Required dashboard counts/views distinguish AI stages/recommendations/technical failure/screen-out/final outcomes; all stages open. | ASOR-AC06 / R10/R11/R18 | M10 access, M12 dashboard and M16 visibility checks; M17 demonstration. |
| Officer acts immediately in every AI stage and overrides screen-out; AI never finalizes or awards. | ASOR-AC07 / R11/R12 | M10 action/authority evidence and M17 live scenario. |
| Citizen sees explanation and can resubmit or request marked same-claim manual review, preserving evidence/explanation. | ASOR-AC08 / R13/R14 | M14 API/browser evidence and M17 workflow. |
| Background work survives pending/in-progress restart and transient attempts stop at three, with immediate officer review. | ASOR-AC09 / R15/R16 | M06 recovery/attempt checks and M17 restart scenario. |
| Officer finalization during processing survives late AI completion without changing decision/points. | ASOR-AC10 / R12/R17 | M10 race evidence and M17 active-processing demonstration. |
| One local demo exposes job status/counts/reasons/attempts/failures/time/usage/cost; no unrequested operational target gates acceptance. | ASOR-AC11 / R18/R19 | M16 visibility and M17 single-instance evidence. |
| Baseline/delta decisions approved before executable work; each non-RED milestone has passing evidence and each RED has intended failure evidence; unrelated behavior/data preserved. | Plan milestone success criteria / ASOR-C01–C10 | M01 human review, M02 isolation/preservation evidence, M03–M16 milestone evidence and M17 validation evidence; Final Review inspection. |
| Exclusions respected; stale user-facing/product statements listed; no self-approved rollout or hidden model substitution. | Requirements exclusions; Plan boundaries / ASOR-PD01 | Final Review. |

## Plan Self-Checks

- **Authority/status:** approved November 10 requirements/Q16 govern current provider scope; this Plan and amended contract await joint approval. Original approvals/execution remain historical, not advance authorization. Contract owns model/media/configuration/usage decisions; exact code belongs to later Implementation Plans.
- **Coverage/ownership:** original R01–R19 delivery remains as traced; R20→M08D/M08C. R03 has one delivery owner, resumed M08; M08D supplies its R20 integration prerequisite and M08C verifies the prerequisite contract behavior, while actual live evidence remains essential to R03 completion. C05 adds only the new-provider trust boundary; C09 separates minimum input capture from full M16 presentation. R05–R09 preserved checks in M08C are not RED evidence or duplicate delivery ownership. AC12 is in Final Acceptance; AC02 now names current OpenAI with Gemini retained.
- **Sequence/prerequisites:** completed M01–M08B rows and their linked evidence are retained. M08C RED→M08D GREEN→resumed M08→unchanged M09–M17 is strictly linear. Separate Implementation Plan approvals retain RED-before-GREEN execution gates; the contract amendment excludes the paired-plan shortcut. Existing harness permits meaningful RED; no FOUNDATION or dependency is assumed necessary. Later RED prerequisites remain covered by their existing predecessors.
- **Verification:** no tests/startup/database/private-input/live inspection ran for this revision. Later plans map affected amended contract rules and original Gemini checks, run new/affected checks first, full approved local suite once at GREEN execution, and repeat only state/configuration checks where required. Checkpoint manifests establish current applicability and prevent redundant unchanged broad loops. Existing skips remain visible.
- **History/acceptance:** stopped 007, verified 008/009, metadata-only diagnosis and Gemini 402 remain distinct historical facts. No billing conclusion or Gemini live prerequisite is imposed on current OpenAI selection. Photos do not close video acceptance: manual video stays NOT RUN until actual evidence. No cap/fallback/service/unrelated scope or acceptance waiver is added. Only Plan.md changes; no Implementation Plan, executable artifact, staging or publication is authorized.


### User-directed continuation — 2026-11-11

User: "leave gemini test and move ahead". The011 User-Authorized Verification Revision records the approved reduced continuation inventory. Gemini-specific verification is deferred with the existing failure preserved; shared transport, intake/preservation and OpenAI/common state repeats remain required. No test source or implementation changes and no complete209/repeat96 claim. M08D remains incomplete until that continuation is verified.
