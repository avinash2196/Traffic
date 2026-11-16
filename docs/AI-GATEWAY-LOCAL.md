# Local AI gateway startup

The application and gateway run in separate processes. This guide describes the local contract; actual provider/private-evidence validation belongs to AGW-M04 and is not performed by this plan.

Use the existing environment with requirements.txt installed. Both ffmpeg and ffprobe must resolve on the gateway process PATH. Native Windows installations need those executables available before startup. The repository Dockerfile already supplies FFmpeg; the test-only pinned container carrier is not a runtime decoder bridge or a host installation instruction.

Configure both processes with the same independently generated service token (at least 32 random bytes encoded as unpadded base64url). Set AI_PROVIDER=openai and OPENAI_MODEL=gpt-5.4-2026-03-05 in both. Configure only the application with AI_GATEWAY_URL=http://127.0.0.1:8091. Configure only the gateway process with OPENAI_API_KEY. Enter secrets through the process environment; do not put them into commands, repository files or logs. Gemini retains AI_PROVIDER=gemini, GEMINI_MODEL=gemini-3.8-flash and gateway-only GEMINI_API_KEY; its live availability and verification are deferred.

From the repository source directory, start the gateway with:

```powershell
.\.venv\Scripts\python.exe -m uvicorn ai_gateway_service:app --host 127.0.0.1 --port 8091 --workers 1 --no-access-log --log-level warning --no-proxy-headers
```

Start the existing application in a separate process using its existing local startup instructions. Keep application database/media access and citizen/officer authorization there. Gateway deployment contains only ai_gateway_service.py, agw_*.py, assessment_policy.py, openai_adapter.py, gemini.py and the existing Python dependencies/decoder binaries. Do not copy/mount application database, private media, application environment or application state modules into the service.

No reload, multiple gateway workers, remote binding, provider base-URL overrides or redirects are supported by this local contract. Missing service URL/token fails AI dispatch closed while manual review remains available. Startup validates configuration and decoder availability without calling a provider. The gateway clears its own orphan scratch and keeps no durable jobs/results. Cancellation terminates local work, but remote provider work/billing may continue; there is no exactly-once guarantee.

New jobs save the v2 OpenAI selection. Historical terra/v1 snapshots fail closed and remain manually reviewable. Existing Gemini snapshots retain their identity; changing environment selection never retargets an already saved job. At most three consumed application attempts apply, including interrupted attempts. The service has no queue/retry/fallback.
