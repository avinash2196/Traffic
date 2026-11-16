# RoadWatch — Citizen + Authority MVP

An independently runnable **India-focused traffic evidence reporting demonstration**. It includes two distinct interfaces and a working end-to-end workflow. **It is not connected to Delhi Traffic Prahari, Indian police, VAHAN, or e-challan services.** Approval and points are demo-only.

## Quick Start (5 minutes)

### Windows
```powershell
.\start-windows.ps1
```

### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

### Manual Setup
```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Access the app:**
- **Citizen Portal:** http://127.0.0.1:8000/citizen-login.html
- **Officer Portal:** http://127.0.0.1:8000/officer-login.html
- **API Docs (Swagger):** http://127.0.0.1:8000/api/docs

**Demo credentials (any value):**
- Citizen ID: `user123` (or any string)
- Officer Token: `demo-reviewer-token` (or any string)

### Environment Variables (Optional)
```bash
export ROADWATCH_REVIEWER_TOKEN="your-secure-token"
export LOG_LEVEL="INFO"
export OPENAI_API_KEY="sk-..."  # For AI screening (Phase 2)
```

See `.env.example` for all variables.

**For detailed local setup:** See `LOCAL_DEPLOYMENT.md`  
**For GCP deployment:** See `GCP_DEPLOYMENT.md`

**Security Note:** Do not expose this service to the internet in MVP. It uses demo identity, shared tokens, and local storage. See production hardening in `GCP_DEPLOYMENT.md`.

## One complete demonstration

1. Visit the **citizen** portal. Select `Riding without helmet`, enter a location, upload a JPEG, then submit.
2. The case gets a unique report ID and four traceable stages: `Submitted → Evidence screening → Awaiting officer review → Officer decision`.
3. Visit the **authority** portal, enter the demo reviewer token, open the report, inspect the **original** photo/video and its advisory screening assessment.
4. Enter a reason and choose **Approve**, **Reject**, or **More information**. If additional information is requested, the citizen can send a text clarification and return the report to the review queue. All actions appear in the timestamped timeline.
5. Approving a report awards **provisional demo points** (2 for helmet, 3 for triple riding/red light). Authorities can download an evidence ZIP containing the original file, SHA-256 hash and report timeline. Exporting doesn't transmit anything to authorities.

## Actual scope, and what "AI" means here

| Capability | In MVP | Notes |
|---|---|---|
| Citizen upload JPG/PNG/MP4/MOV/WEBM | ✅ | 25 MB file / 45-second video limit |
| Submission history / status timeline | ✅ | SQLite events |
| Authority queue and evidence preview | ✅ | Local reviewer token |
| Review approve/reject/needs info | ✅ | Reason mandatory; review can happen only when awaiting action |
| Provisional points | ✅ | No money, no redemption |
| Original file SHA-256 / duplicate detection | ✅ | Identical binary files, not perceptual duplicates |
| Original media ZIP export | ✅ | Demo only |
| Technical image/video checks | ✅ | Container readability, frame sampling, advisory blur/resolution checks |
| **Actual multimodal AI triage** | **Optional** | Requires `OPENAI_API_KEY`; described below |
| Authenticity/alteration detection | ❌ | Hash tracks original uploads; does **not** prove truth/authenticity |
| Verified violation classification | ❌ | Model observations are not findings or legal proof |
| Automatic licence-plate OCR | ⚠️ | Optional model may suggest a plate, **unverified** |
| Real government integration, challans | ❌ | Not simulated as official actions |
| Real user authentication / RBAC | ❌ | Header-based citizen identity; shared token for local reviewers |
| Real retry queue / distributed workers | ❌ | FastAPI in-process background tasks |

### Enable optional AI advisory screening

Set an OpenAI API key **only if you are permitted to send the evidence to that third-party service**. Data in video frames and photographs may include number plates and identifiable bystanders. Obtain appropriate legal approvals/consent before processing real citizen data.

```bash
# macOS/Linux:
export OPENAI_API_KEY="your-key"
# Windows PowerShell:
$env:OPENAI_API_KEY="your-key"
```

The server then submits at most five **sampled frames**, plus the alleged violation category, to a vision-enabled model via Chat Completions, seeking a structured **advisory** assessment. The default model is `gpt-4.1-mini` (override with `OPENAI_MODEL`). The integration is provided but **not externally tested without an API key**. The model can be wrong, miss events between frames, confuse the traffic signal or hallucinates plate numbers. A real police deployment would need benchmarked models, video temporal reasoning, policies and legal validation. When the key is absent, the UI explicitly says **technical media check only**; it never pretends that AI confirmed a violation.

### Data model and API

- `reports` — citizen, alleged category, event location/time, original media path, SHA-256, advisory screening, status, provisional points.
- `events` — append-only report timeline (status, actor, timestamp, reason).
- `POST /api/reports` — submit citizen evidence.
- `GET /api/reports` — citizen history and provisional point totals.
- `GET /api/reports/{id}` — case timeline.
- `GET /api/reports/{id}/media` — original, access-checked media.
- `POST /api/reports/{id}/clarification` — citizen response to officer information request.
- `GET /api/authority/reports` — reviewer queue.
- `POST /api/authority/reports/{id}/decision` — human review.
- `GET /api/authority/reports/{id}/evidence.zip` — reviewer evidence export.

Run tests with `python -m pytest -q`.

## Architecture decision for this MVP

**Modular monolith, async screening, two role-focused interfaces.** This minimizes cost and moving parts while preserving a clear separation between citizen reporting, media handling, advisory analysis, officer review and event history.

```text
Citizen UI ──POST media──► FastAPI ──► SQLite metadata + original media
                               │
                               └──► Background screening (technical; optional AI)
                                                │
                                                ▼
Authority UI ◄── queue, evidence, assessment and event history ──► Officer decision
                                                │
                                                ▼
                                  Citizen status + provisional points
```

**Proposed production evolution:** replace demo identity with OTP/OIDC + officer SSO + role-based access control; encrypted object storage with signed URLs; PostgreSQL; durable job queue; specialized OCR/temporal traffic-video models; robust audit/event outbox; official authority integration; security, privacy and deployment reviews; separate private reviewer/authority networks where required. None are implemented in this starter.

## Important known limitations

- **Security:** Demo citizen identification uses `X-Citizen-Id` and is forgeable. Officer authentication is a shared secret. Local-only by design.
- **Privacy/legal:** No retention/deletion schedule, masking, redaction, DPIA or Indian legal review. **Only use staged/non-sensitive sample evidence.**
- **Media:** Reads an untrusted video container with OpenCV. Production requires isolation, antivirus, codec limits and abuse protection.
- **Duplicate detection:** Same SHA-256, not visually similar or repeated overlapping clips.
- **Video/red light:** Sampling frames cannot establish a red-light offense. Original full video must be reviewed. This demo must not issue legal conclusions.
- **Point abuse:** Awards are provisional on demo officer approval; no appeals/reversal or economic incentives.
- **Operational:** SQLite/file storage, no managed secrets, no monitoring, no distributed background retries; suitable only for controlled demonstration.
- **No genuine officer or enforcement connection.** Never describe the demo statuses as official government decisions.

## Suggested pilot acceptance tests

Measure report submit-to-review cycle time; reviewer minutes with and without AI; evidence quality; false-positive/false-negative rates **by violation type**; duplicated uploads; reviewer agreement; reliability of citizen timeline. Start with synthetic or appropriately authorized historical evidence and do not make automatic penalties.
