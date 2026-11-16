# RoadWatch Traffic MVP - Core Services

## 7 CORE SERVICES (ALL REQUIRED)

### MICROSERVICES (5)

| # | Service | Port | Directory | Purpose |
|---|---------|------|-----------|---------|
| 1 | **Auth Service** | 9003 | `/auth/` | JWT token generation, citizen/officer registration & login |
| 2 | **Citizen API** | 9001 | `/citizen/` | Media upload, report submission, evidence management |
| 3 | **Officer API** | 9002 | `/officer/` | Review queue, report decisions, approvals |
| 4 | **AI Gateway** | 9004 | `/ai-gateway/` | AI-powered evidence screening, Gemini/OpenAI integration |
| 5 | **AI Worker** | - | `/ai-worker/` | Background job processing, async screening tasks |

### FRONTENDS (2)

| # | Service | Port | Directory | Purpose |
|---|---------|------|-----------|---------|
| 6 | **Citizen Frontend** | 3001 | `/citizen-app/` | Report submission UI, evidence upload interface |
| 7 | **Officer Frontend** | 3002 | `/officer-app/` | Review queue UI, decision interface |

---

## Startup Order

1. **Auth Service (9003)** - Must start first (other services depend on it)
2. **Citizen API (9001)** - Requires Auth Service
3. **Officer API (9002)** - Requires Auth Service
4. **AI Gateway (9004)** - Requires OpenAI/Gemini API keys
5. **AI Worker** - Background processor (non-blocking)
6. **Citizen Frontend (3001)** - Requires Citizen API (9001)
7. **Officer Frontend (3002)** - Requires Officer API (9002)

---

## Dependencies

### AI Gateway Requirements
- ✅ `OPENAI_API_KEY` - OpenAI API key
- ✅ `OPENAI_MODEL` - Model name (gpt-4o-mini)
- ✅ `GEMINI_API_KEY` - Google Gemini API key
- ✅ `GEMINI_MODEL` - Gemini model name
- ✅ Files: `ai_gateway_mvp.py`, `assessment_policy.py`, `agw_protocol.py`, `agw_transport.py`

### AI Worker Requirements
- ✅ SQLite database connection
- ✅ Job queue table
- ✅ Event log table

### All Services Require
- ✅ Python 3.9+
- ✅ Virtual environment (`.venv/`)
- ✅ Dependencies: `pip install -r requirements.txt`
- ✅ `.env` file with configuration

---

## Service Communication

```
Citizen App (3001) ──┐
                     └──> Citizen API (9001) ──┐
                                               ├──> Auth Service (9003)
Officer App (3002) ──┐                         │
                     └──> Officer API (9002) ──┘

Citizen API (9001) ──┐
                     ├──> AI Gateway (9004) ──> Gemini/OpenAI APIs
Officer API (9002) ──┘
                     └──> AI Worker ──> Job Queue

All ──> SQLite Database (roadwatch.db)
```

---

## Verification

After starting all 7 services, verify with:

```bash
# All should return 200 OK
curl http://127.0.0.1:9003/health  # Auth
curl http://127.0.0.1:9001/health  # Citizen API
curl http://127.0.0.1:9002/health  # Officer API
curl http://127.0.0.1:9004/health  # AI Gateway
curl http://127.0.0.1:3001/        # Citizen Frontend
curl http://127.0.0.1:3002/        # Officer Frontend
```

---

## Total System Requirements

| Component | Type | Status |
|-----------|------|--------|
| Microservices | 5 | CORE |
| Frontends | 2 | CORE |
| **Total** | **7** | **REQUIRED** |

**All 7 services MUST be running for full RoadWatch functionality.**
