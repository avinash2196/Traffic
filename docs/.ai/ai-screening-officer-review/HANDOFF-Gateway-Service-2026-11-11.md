# AI gateway service — chat handoff

## Checkpoint

Safe checkpoint confirmed 2026-11-11, America/Chicago. IP014 is finalized for review; its nine proposed Python blocks compiled, planning evidence is saved, and owned planning processes/carriers/temporary source and state have been cleaned up. No proposed production source was applied.

Workspace: `C:\Users\avina\Downloads\avinash-repo\v11\Traffic`. Reuse this checkout; do not create a worktree or reset its dirty state.

The user requested a new chat because the previous chat is too large. Stop at the implementation-plan approval boundary. **IP014 is NOT approved. Do not apply production changes or run live calls.**

## Intended outcome

Application → separate authenticated FastAPI AI gateway → configured OpenAI provider → structured assessment returned and persisted by the application. Support images and videos with a specific versioned prompt. Keep Gemini configurable, with its verification deferred. The application owns evidence access, claims, one durable queue, at most three transient attempts, officer decisions and awards. Gateway output is advisory.

This is a focused service extraction, not the earlier dashboard/appeal/award epic. No second queue, nested retries, silent fallback, app database/filesystem contract, new providers or unrelated regression repairs.

## Authority and current milestones

All paths below are in this work-item directory.

| Artifact / milestone | Status |
| --- | --- |
| `requirements.md` | Focused requirements approved by user 2026-11-11. |
| `Plan.md` | Focused Plan and later M02A amendment approved by user. |
| `External-Contract.md` | Separate-service contract approved by user; normative AGW-CT01–08. |
| AGW-M01 | Complete: service contract approved. |
| AGW-M02 / IP012 | Executed: 19 intended ordinary missing-boundary failures, two preserved passes; exact three test files applied. |
| AGW-M02A / IP013 | Executed: separate-provider lifecycle first/repeat passed, same 19 intended failures and two preserved passes; exact test-only correction applied. |
| AGW-M03 / IP014 | Implementation plan prepared, **awaiting user approval; production changes NOT applied**. |
| AGW-M04 / IP015 | Pending: live OpenAI image AND video protocol has not been written or executed. |
| Final Review | Pending after live evidence. |

The next action is to present IP014 for approval. Once the user explicitly approves that artifact, record approval in its sole Human Review section before fresh-context implementation execution. Do not treat the previous chat's “go ahead” responses as approval of IP014: they approved earlier specific artifacts.

## IP014 proposal

`014_Implementation_Plan_Service_Extraction_GREEN.md` holds exact complete code for ten files:

- Create `ai_gateway_service.py`, `agw_protocol.py`, `agw_transport.py`, `agw_media.py`, and `docs/AI-GATEWAY-LOCAL.md`.
- Modify `assessment_policy.py`, `openai_adapter.py`, `gemini.py`, `gateway.py`, and `durable.py`.
- No test changes, dependency changes or schema/snapshot migration.

It separates pure provider/media code from app-owned SQLite/evidence access, uses an authenticated HTTP client in the existing durable worker, preserves available usage on errors and validates the returned envelope. The gateway has one prestarted idle killable execution process to avoid per-request process-startup cost. It admits only one synchronous request: there is no waiting job queue, durable service state or retry loop. Interrupted work is reaped and the idle executor replaced before admission is released.

The approved contract proposes pinned `gpt-5.4-2026-03-05`, Responses, medium reasoning, strict JSON schema, 8192 output tokens, no store/tools/fallback. Media profile is `agw-openai-frames-v2`. Images use original bytes; videos use actual rational PTS, at most 32 selected source frames, with deduplication, truthful coverage and uncertainty. Retained Gemini model identity is not proof of live availability.

Review the complete exact IP014 before execution. Its 19 representative checks do not prove every startup, streaming, memory, submillisecond, disconnect, restart or error permutation; its code-audit table and limitations are important.

## Planning evidence, not execution

- IP014's final focused dry run reported **21 passed in 37.64s**: 19 new service outcomes and two existing durable guards.
- A final scoped SQLite deadline correction then passed the **two affected state checks in 12.94s**; the unaffected service cases were not repeated again.
- That last diagnostic driver exited 1 **after passing tests**, on a metadata comparison: `.local` and `__pycache__` directory sizes were reported as 0 versus 4096 across contexts, with unchanged directory mtimes, unchanged file metadata and unchanged allowlisted source hashes. Preserve this exact limitation; do not call the whole protection gate passed or infer private byte identity. No private content was read to resolve it.
- The implementation plan records earlier concrete draft failures and corrections. Do not describe planning results as actual AGW-M03 completion, real provider calls or deployment.

Execution after approval uses the exact current `tests/verify_gateway_service.py --green` protocol: 19 + 2 passing cases, the two state repeats, and the approved synthetic lifecycle first/repeat. No old 209/96 suite, Gemini suite or repeated broad planning loop. Read the IP for exact commands, source guards and expected evidence.

## Important harness facts

`tests/agw_provider_child.py` runs a synthetic provider in a separate owned loopback process. Its transport remaps only the fixed OpenAI URL to that local provider. It returns provider wire JSON, not fabricated application state. Real app worker/JobStore behavior is exercised separately.

The initial in-process blocking MockTransport was unsuitable for forced cancellation: terminating its process skipped the marker-removing `finally`. IP013 corrected this without changing the 19 behavioral assertions or the under-three-second timeout. The simulated remote provider may continue four seconds and drain after the local client is killed, matching remote-outcome ambiguity.

Windows `.venv` launcher PID can differ from actual server PID. Use the approved owned process-tree cleanup, not merely `Popen.terminate()` on the launcher. Deliberate cancellation produces `ConnectionResetError` traces in the synthetic provider; they were retained, with server survival and marker drainage verified. They are not real OpenAI failures.

## Local verification and privacy

- Use literal host paths under `C:\Users\avina\AppData\Local\Temp\asor-...` from the first setup call. Restricted `$env:TEMP` can virtualize between calls. Do not erase retained logs or reuse a target the verifier refuses.
- Native Windows local-socket tests need an expanded `exec_command` invocation with explicit owned disposable cwd. Source-only copies exclude `.local`, `.env`, real databases/media and backups. Root pytest historically had unsafe fixtures; use only the approved verifier.
- Native FFmpeg/ffprobe are absent on this Windows host. Verification uses pinned image `sha256:f3b04288897b10d8d6f605460bd416fac376b3b13bd29797922f843bd88f05de`, network none, zero mounts, stdin-forwarding wrappers. This is a decoder tool carrier, not a full app runtime. Check both wrapper resolutions and direct container tool versions; wrapper `-version` alone lacks its required input operand. Track carrier lifetime and owned processes.
- Actual service startup requires native decoder tools on PATH as documented; no host installation or runtime Docker bridge was performed. Live environment preparation belongs to the approved M04 protocol.
- Hash explicit public source allowlists only. Private files: metadata only, no content hashes or key reads during planning. Directory size reports are unreliable across execution contexts.
- No staging, commits, remote publication or production deployment was authorized. Existing dirty source belongs to prior recorded work. Preserve it.

## Private live inputs — paths only

OpenAI key is at `.local\openAi-api-key.txt`; Gemini key at `.local\gemini-api-key.txt`. These must not be read during handoff/review/planning or printed. Later approved live execution may load them privately into the appropriate service environment.

User-authorized photos are in `C:\Users\avina\Downloads\traffic images`: `three.jpg` (suspected triple riding, count may be unclear), `without helmet.jpeg`, `open-image.jpg` (traffic but red-light proof unclear), `traffic.jpg` (fruit basket/irrelevant); a helmet-copy file is byte-identical, so avoid duplicate calls. No representative user video is supplied yet. The user earlier offered a public video; obtain/confirm an authorized video input in the live protocol. Do not waive live video acceptance.

## History to preserve, not rerun by default

Earlier full scope is archived as `requirements.pre-service-focus-2026-11-11.md`, `Plan.pre-service-focus-2026-11-11.md`, and `External-Contract.pre-service-focus-2026-11-11.md`. Historical ASOR-M08D is incomplete. Gemini upload-start HTTP402 remains unresolved/deferred. An MP4 upload rejection later passed an instrumented single case and original 15-case sequence; its original cause was not established. No current full-suite success claim.

## Process

Use installed Production Engineering Standards **0.16.0** at `C:/Users/avina/.codex/plugins/cache/pes-marketplace/production-engineering-standards/0.16.0/skills`. The repository instruction header's older version is historical context. PDD role commands use fresh-context role agents reading artifacts; this explicitly authorizes that delegation. Do not create further user-owned chats unless asked.

The user is frustrated by long loops and repeated setup failures. Keep updates concise, complete already-authorized work, preserve actual failure evidence, and ask only at concrete review boundaries. In the new chat, first read this handoff and IP014 Review Summary/Human Review, report readiness and wait for IP014 approval. Do not rerun planning checks merely to reconstruct the old conversation.
