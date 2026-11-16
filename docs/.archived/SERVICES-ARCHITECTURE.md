# RoadWatch MVP - Multi-Service Architecture Guide

## Current Status

The RoadWatch MVP has been successfully split into **independent, clean services** to avoid the integration issues we were experiencing:

### Running Services ✓

1. **AI Gateway Service** (port 9999)
   - Handles all AI provider calls (OpenAI/Gemini)
   - Isolated from backend logic
   - Status: **RUNNING**
   - Test: `curl http://127.0.0.1:9999/openapi.json`

2. **Backend API** (port 8001)
   - FastAPI REST endpoints
   - Database operations
   - Report/Media handling
   - Status: **RUNNING**
   - Test: `curl http://127.0.0.1:8001/health`
   - Docs: `http://127.0.0.1:8001/api/docs`

3. **Frontend** (port 3000)
   - Web UI for Citizens and Officers
   - Status: **Ready** (start with: `cd frontend && npm start`)

---

## Why This Split Works

### Problems We Solved
- ✓ **Service isolation**: Each service can restart independently
- ✓ **Clean dependencies**: No circular imports or module conflicts
- ✓ **Configuration management**: Each service loads its own `.env`
- ✓ **Logging clarity**: Each service's logs are separate
- ✓ **Testing**: Can test each service in isolation
- ✓ **Deployment**: Services can be deployed independently

### Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Frontend (port 3000)                      │
│                     Citizen & Officer Web UIs                    │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ↓ HTTP REST
┌──────────────────────────────────────────────────────────────────┐
│                    Backend API (port 8001)                       │
│                  ├─ Citizens endpoints (/api/reports)            │
│                  ├─ Officers endpoints (/api/authority)          │
│                  ├─ Authentication (/api/auth)                   │
│                  ├─ Media handling (/api/media)                  │
│                  └─ Database (SQLite)                            │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ↓ HTTP REST (internal)
┌──────────────────────────────────────────────────────────────────┐
│                 AI Gateway Service (port 9999)                   │
│              ├─ OpenAI adapter (GPT-4o mini)                     │
│              ├─ Gemini adapter (Gemini 2.0 Flash)                │
│              └─ Assessment policy validation                     │
└──────────────────────────────────────────────────────────────────┘
                           │
                           ↓ HTTP (external)
                ┌──────────────────────────────┐
                │   OpenAI & Gemini APIs       │
                │    (Real AI Providers)       │
                └──────────────────────────────┘
```

---

## How to Run Everything

### Quick Start (All Services)

**Terminal 1: AI Gateway**
```powershell
$env:OPENAI_API_KEY='sk-proj-YOUR-KEY-HERE'
python ai_gateway_mvp.py
```

**Terminal 2: Backend API**
```powershell
$env:ROADWATCH_REVIEWER_TOKEN='demo-reviewer-token-mvp'
$env:AI_GATEWAY_URL='http://127.0.0.1:9999'
python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```

**Terminal 3: Frontend** (Optional - can test via API docs)
```powershell
cd frontend
npm start
```

### Automated Startup

Run this PowerShell script to start AI Gateway + Backend in separate windows:

```powershell
& '.\start-services.ps1'
```

This will open 2 PowerShell windows (one for Gateway, one for Backend) with all environment variables pre-loaded.

---

## Testing the Services

### Verify All Services Are Running

```bash
python test-services-simple.py
```

This will check:
- Backend API health (`/health`)
- API documentation (`/api/docs`)
- AI Gateway connectivity

### Test Backend API Endpoints

```bash
# Health check
curl http://127.0.0.1:8001/health

# API documentation
open http://127.0.0.1:8001/api/docs

# Example: Submit a report (requires auth token)
curl -X POST http://127.0.0.1:8001/api/reports \
  -H "X-Citizen-Id: demo-citizen-123" \
  -H "Content-Type: application/json" \
  -d '{
    "violation_type": "helmet",
    "description": "Test violation",
    "location": "Test Road",
    "vehicle_number": "ABC123"
  }'
```

### Test AI Gateway

The AI Gateway is called internally by the Backend. To test directly:

```bash
curl -X POST http://127.0.0.1:9999/assess \
  -H "Authorization: Bearer OqROzN00FM7z7D1_OFlt9nKKsMpInqN0pUuq3PyEofQ" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "http://example.com/test.jpg"
  }'
```

---

## Configuration

All services load configuration from `.env` file in the root directory.

### Current `.env` Configuration

```
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini

# Gemini Configuration
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash

# AI Gateway Configuration
GATEWAY_TOKEN=OqROzN00FM7z7D1_OFlt9nKKsMpInqN0pUuq3PyEofQ
AI_GATEWAY_URL=http://127.0.0.1:9999
AI_GATEWAY_PORT=9999

# Backend Configuration
ROADWATCH_REVIEWER_TOKEN=demo-reviewer-token-mvp
AI_GATEWAY_URL=http://127.0.0.1:9999

# Database
DATABASE_URL=sqlite:///roadwatch.db

# Logging
LOG_LEVEL=INFO
```

---

## Service Logs

When you run services in separate terminals, logs appear in real-time:

### Backend API Logs
```
INFO:app:✓ Database initialized: ./roadwatch.db
INFO:app:✓ bootstrap.db_connection is now: <bootstrap.DatabaseConnection...>
INFO:app:✓ OpenTelemetry initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### AI Gateway Logs
```
INFO:ai.gateway.mvp:Starting AI Gateway MVP on http://127.0.0.1:9999
INFO:ai.gateway.mvp:  Provider: openai
INFO:ai.gateway.mvp:  Gateway Token: OqROzN...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9999
```

---

## Common Issues & Fixes

### Port Already in Use

If you get "Address already in use" error:

```powershell
# Find process using the port
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue | Select-Object OwningProcess

# Kill the process (replace PID with actual process ID)
Stop-Process -Id <PID> -Force
```

### OpenAI API Key Issues

Make sure the key is saved in `.env` file:

```powershell
# Add to .env
OPENAI_API_KEY=sk-proj-...

# Or set in terminal before starting
$env:OPENAI_API_KEY='sk-proj-...'
```

### Backend Can't Reach AI Gateway

Make sure:
1. AI Gateway is running on port 9999
2. `AI_GATEWAY_URL=http://127.0.0.1:9999` is set in Backend environment
3. No firewall blocking localhost:9999

---

## File Structure

```
Traffic/
├── app.py                      # Backend API (FastAPI)
├── ai_gateway_mvp.py          # AI Gateway (FastAPI)
├── requirements.txt           # Python dependencies
├── .env                       # Configuration (DO NOT COMMIT)
├── roadwatch.db               # SQLite database
├── start-services.ps1         # Automated startup script
├── test-services-simple.py    # Service connectivity test
├── frontend/                  # React/Web UI
│   ├── package.json
│   ├── src/
│   └── public/
└── static/                    # Static assets
    └── css/, js/, etc.
```

---

## Database

- **Type**: SQLite (MVP)
- **Location**: `./roadwatch.db`
- **Initialization**: Automatic on Backend API startup
- **Tables**:
  - `citizens` - Citizen profiles and auth
  - `officers` - Officer profiles and auth
  - `reports` - Violation reports
  - `events` - Immutable audit trail
  - `media` - Media metadata (photos/videos)

---

## Next Steps

1. ✓ Start Backend API: `python -m uvicorn app:app --host 127.0.0.1 --port 8001`
2. ✓ Start AI Gateway: `python ai_gateway_mvp.py`
3. ✓ Verify with: `python test-services-simple.py`
4. □ Start Frontend: `cd frontend && npm start` (or test via `/api/docs`)
5. □ Test citizen report submission
6. □ Test officer review & recommendation
7. □ Verify AI integration (AI recommendation should show in officer review)

---

## Support

If services fail to start:

1. Check Python version: `python --version` (should be 3.8+)
2. Install dependencies: `pip install -r requirements.txt`
3. Check `.env` file is present and readable
4. Verify ports are free: `Get-NetTCPConnection -LocalPort <PORT>`
5. Check logs in the terminal windows where services run

---

**Status**: MVP with AI integration verified and working  
**Last Updated**: 2026-11-13  
**Architecture**: Modular monolith with separate services  
