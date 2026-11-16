# RoadWatch Local Deployment Guide

**Quick Start:** 5 minutes to running UI + API

---

## 📋 Prerequisites

- **Python 3.11+** (check: `python --version`)
- **Git** (for cloning repo)
- **~500 MB disk space** (for dependencies + database)
- **Port 8000** available (configurable)

---

## 🚀 Option 1: Fastest Start (Windows)

### Step 1: Navigate to project
```powershell
cd Traffic
```

### Step 2: Run startup script
```powershell
.\start-windows.ps1
```

**What it does:**
- Creates `.venv` (virtual environment)
- Installs `requirements.txt`
- Initializes SQLite database (`roadwatch.db`)
- Starts uvicorn server on `http://127.0.0.1:8000`

**Output:**
```
🚗 RoadWatch Traffic MVP - Windows Startup
✓ Python found: Python 3.14.9
✓ Virtual environment created
✓ Dependencies installed
✓ Created media_store directory
🚀 Starting RoadWatch Traffic MVP...
📍 API available at: http://127.0.0.1:8000
📊 Documentation at: http://127.0.0.1:8000/api/docs
ℹ️  Press Ctrl+C to stop
```

**Stop:** Press `Ctrl+C`

---

## 🚀 Option 2: Fastest Start (macOS/Linux)

### Step 1: Navigate to project
```bash
cd Traffic
```

### Step 2: Make script executable
```bash
chmod +x start.sh
```

### Step 3: Run startup script
```bash
./start.sh
```

**Output:** (same as Windows)

**Stop:** Press `Ctrl+C`

---

## 🚀 Option 3: Manual Setup (Advanced)

### Step 1: Create virtual environment
```bash
python -m venv .venv
```

### Step 2: Activate it
**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create media directory
```bash
mkdir -p media_store
```

### Step 5: Start app
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Step 6: Stop app
```bash
Ctrl+C
```

---

## 🔄 Run Again (After First Setup)

**After the initial setup, you only need to:**

### Windows
```powershell
# Option 1: Use startup script (recommended)
.\start-windows.ps1

# Option 2: Manual (requires venv activation)
.venv\Scripts\Activate.ps1
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

### macOS/Linux
```bash
# Option 1: Use startup script (recommended)
./start.sh

# Option 2: Manual (requires venv activation)
source .venv/bin/activate
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

**Note:** `.venv` and `requirements.txt` only need to be set up once. After that, you just activate the venv and start the server.

---

## 📖 Access the App

### Web UI
- **Citizen Portal:** http://127.0.0.1:8000/citizen-login.html
- **Officer Portal:** http://127.0.0.1:8000/officer-login.html
- **API Docs:** http://127.0.0.1:8000/api/docs (Swagger UI)
- **Health Check:** http://127.0.0.1:8000/health

### Demo Credentials
**Citizen Login:**
- Any ID (demo mode, no validation)
- Example: `user123`

**Officer Login:**
- Any token (demo mode)
- Example: `demo-reviewer-token`

---

## 📊 Database Setup

### Automatic (Default)
Database is created automatically at startup:
```
roadwatch.db
```

Schema created:
- `reports` — Violation reports
- `media` — Attached photos/videos
- `events` — Audit trail (append-only)

### Reset Database
```bash
# Stop the app (Ctrl+C)
rm roadwatch.db
# Restart app (schema recreated automatically)
```

### View Database
```bash
# Install sqlite3 CLI (if not present)
# macOS: brew install sqlite
# Ubuntu: sudo apt-get install sqlite3
# Windows: Download from https://www.sqlite.org

sqlite3 roadwatch.db
sqlite> SELECT * FROM reports;
sqlite> .tables
sqlite> .quit
```

---

## 🔧 Environment Variables

**Optional** — Set before starting app:

### Authentication
```bash
export ROADWATCH_REVIEWER_TOKEN="your-secret-token"
```
(Default: `"local-reviewer-only"`)

### Database Location
```bash
export DATABASE_URL="sqlite:///./roadwatch.db"
```
(Default: `./roadwatch.db`)

### Media Storage
```bash
export MEDIA_STORE_PATH="/path/to/media"
```
(Default: `./media_store`)

### AI Screening (Optional, Phase 2)

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)

**Set the key before starting app:**

Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE"
$env:OPENAI_MODEL="gpt-4o-mini"
$env:ENABLE_AI_SCREENING="true"
.\start-windows.ps1
```

macOS/Linux:
```bash
export OPENAI_API_KEY="sk-proj-YOUR-KEY-HERE"
export OPENAI_MODEL="gpt-4o-mini"
export ENABLE_AI_SCREENING="true"
./start.sh
```

**Or edit `.env` file:**
```bash
# Copy template
cp .env.example .env

# Edit with your editor (nano, vim, VSCode, etc.)
nano .env
# Set: OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
# Set: ENABLE_AI_SCREENING=true
# Save and exit

# Then start (loads .env automatically)
.\start-windows.ps1  # or ./start.sh
```

**Note:** AI screening is OPTIONAL. App works fine without it (Phase 2 feature).

---

### Other API Keys (Future)

Future integrations will use similar pattern:
```bash
export VAHAN_API_KEY="..."          # Vehicle verification
export POLICE_API_URL="..."          # Police registration
export ECHALLAN_API_KEY="..."        # e-Challan system
```

All keys should be set via environment variables, NEVER hardcoded in files.

### Server Config
```bash
export ROADWATCH_HOST="0.0.0.0"
export ROADWATCH_PORT="8000"
```

### Logging
```bash
export LOG_LEVEL="INFO"  # INFO, DEBUG, WARNING, ERROR
```

---

## 📝 Environment File (.env)

Create `.env` file in project root:

```bash
# Copy from .env.example
cp .env.example .env
```

Edit `.env`:
```env
# Authentication
ROADWATCH_REVIEWER_TOKEN=local-reviewer-only

# Database
DATABASE_URL=sqlite:///./roadwatch.db

# Media Storage
MEDIA_STORE_PATH=./media_store

# Server
ROADWATCH_HOST=0.0.0.0
ROADWATCH_PORT=8000

# Logging
LOG_LEVEL=INFO

# OpenAI (Optional, for Phase 2 AI screening)
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Observability
OTEL_EXPORTER_OTLP_PROTO_HTTP_ENDPOINT=
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("ROADWATCH_REVIEWER_TOKEN")
```

---

## 🐛 Troubleshooting

### Port 8000 already in use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
uvicorn app:app --port 8001
```

### Python not found
```bash
# Install Python 3.11+
# Windows: https://www.python.org/downloads/
# macOS: brew install python@3.12
# Ubuntu: sudo apt-get install python3.12

python --version
```

### Module not found error
```bash
# Ensure .venv activated
which python  # macOS/Linux (should show .venv)

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database locked
```bash
# Another app instance is using database
# Stop all python processes and restart

# Windows:
taskkill /IM python.exe /F

# macOS/Linux:
pkill python
```

### Import error: `ModuleNotFoundError: No module named 'jinja2'`
```bash
pip install jinja2==3.1.2
```

---

## 📤 Testing Workflow

### 1. Create a report (Citizen)
- Go to: http://127.0.0.1:8000/citizen-login.html
- Enter any ID (e.g., `user123`)
- Click "Report Violation"
- Select violation type (e.g., "No Helmet")
- Upload a photo or video
- Submit

**Response:** Report ID (e.g., `rep_abc123`)

### 2. Check report status (Citizen)
- Go to: "My Reports"
- Status shows: `pending`

### 3. Review report (Officer)
- Go to: http://127.0.0.1:8000/officer-login.html
- Enter any token (e.g., `demo-reviewer-token`)
- Click "Review Queue"
- See pending reports
- Click "Review Case"

### 4. Make decision (Officer)
- View evidence (photo/video)
- Click "Download Evidence ZIP" (M6 feature)
- Select decision: "Approve & Award Points" or "Reject"
- Click "Submit Decision"

### 5. Check final status (Citizen)
- Go to "My Reports"
- Status updated to: `approved` or `rejected`
- Points awarded (if approved): `2` (helmet) or `3` (triple-riding/red-light)

---

## 🚢 Docker Deployment (Local)

### Build image
```bash
docker build -t roadwatch:latest .
```

### Run container
```bash
docker run -p 8000:8000 -v $(pwd)/media_store:/workspace/media_store roadwatch:latest
```

**Windows PowerShell:**
```powershell
docker run -p 8000:8000 -v ${PWD}/media_store:/workspace/media_store roadwatch:latest
```

### Access
- UI: http://localhost:8000/citizen-login.html
- API Docs: http://localhost:8000/api/docs

### Stop container
```bash
docker ps  # Find CONTAINER ID
docker stop <CONTAINER_ID>
```

---

## 📊 Monitoring & Logs

### View live logs
```bash
# With --reload (development)
uvicorn app:app --reload  # Logs in console

# With Docker
docker logs -f <CONTAINER_ID>
```

### Log levels
```bash
export LOG_LEVEL=DEBUG  # Verbose
export LOG_LEVEL=INFO   # Normal
export LOG_LEVEL=WARNING  # Errors only
```

### Check database
```sql
sqlite3 roadwatch.db "SELECT * FROM reports;"
sqlite3 roadwatch.db "SELECT * FROM events ORDER BY created_at DESC LIMIT 10;"
```

---

## 🔐 Security (Local Dev Only)

### Current Setup (MVP)
- ✅ No authentication validation (demo mode)
- ✅ Any citizen ID accepted
- ✅ Any officer token accepted
- ✅ File upload validated (MIME type, size, frames)
- ✅ SQLite transactions (ACID)

### Production Requirements (Phase 2)
- [ ] OIDC integration (Google, Microsoft, custom)
- [ ] JWT token validation
- [ ] Role-based access control (RBAC)
- [ ] HTTPS/TLS
- [ ] Rate limiting
- [ ] Request signing

See `GCP_DEPLOYMENT.md` for production security setup.

---

## 📈 Performance Notes

### Local Testing
- ~100ms per request (SQLite, SSD)
- Polling every 30 seconds (configurable in JS)
- No caching (perfect for dev)

### Production
- Use PostgreSQL for scale
- Add Redis for caching
- CDN for static assets
- Load balancer for HA

---

## 🆘 Support

### Check health
```bash
curl http://127.0.0.1:8000/health
```

### View API docs
http://127.0.0.1:8000/api/docs (interactive Swagger UI)

### Run verification
```bash
python verify_integration.py
```

### Restart app
```bash
# Press Ctrl+C
# Re-run start.sh or uvicorn command
```

---

## ✅ Checklist

- [ ] Python 3.11+ installed
- [ ] `cd Traffic` directory
- [ ] Run `.\start-windows.ps1` or `./start.sh`
- [ ] Access http://127.0.0.1:8000/citizen-login.html
- [ ] Create a test report
- [ ] Review in officer portal
- [ ] Download evidence ZIP (M6)
- [ ] All working!

**Done! Your local RoadWatch is running.** 🎉

---

**Document:** `LOCAL_DEPLOYMENT.md`  
**Last Updated:** 2026-11-02  
**Version:** 1.0

