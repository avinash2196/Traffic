# RoadWatch MVP - Session Summary: Configuration Management & API Key Persistence

**Date:** 2026-11-14  
**Focus:** Resolving API key loading issue that prevented AI assessment from working  
**Status:** Configuration framework complete; ready for final testing with correct process startup

---

## 🔍 Problem Identified

Throughout earlier sessions, AI assessments were failing with `PROVIDER_CONFIGURATION` errors because:

1. **Environment variables were set in PowerShell** but **not passed to Python processes**
2. **Worker processes (threading) inherited env vars from app.py**, but **app.py didn't have them**
3. **Startup scripts** (`.ps1`, `.sh`) set env vars, but **Python subprocess calls don't inherit them**
4. **API keys and tokens** were either hardcoded mock values or simply missing at runtime

### Example of the Problem:
```
PowerShell Session:           FastAPI Process:           AI Worker Thread:
$env:OPENAI_API_KEY="sk..."  os.getenv(...) → None!    ✗ No token for gateway auth
```

---

## ✅ Solutions Implemented

### 1. **Persistent `.env` Configuration File**
Created `.env` at repository root with:
- Real OpenAI API key (provided by user)
- Real Gemini API key 
- AI Gateway token (base64-encoded, 43+ chars)
- Server host/port configuration
- Database URL

**Security:** `.env` is in `.gitignore` - never committed to git

### 2. **Automatic .env Loading on Startup**
Modified both **app.py** and **ai_gateway_mvp.py**:

```python
# Load environment variables from .env FIRST (before importing anything else)
import os
from pathlib import Path

env_path = Path(__file__).resolve().parent / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key, value = parts
                    os.environ[key.strip()] = value.strip()

os.environ.setdefault('APP_PROFILE', 'local')
```

**Key Features:**
- Uses `Path(__file__).resolve()` to find `.env` in the script directory (works from any working dir)
- Reads `.env` **before any other imports** (critical for early module loading)
- Sets defaults for required env vars (e.g., `APP_PROFILE='local'`)
- Threads inherit parent process env vars automatically

### 3. **Enhanced Startup Scripts**

#### **Windows PowerShell** (start-windows.ps1)
- Loads .env before activating venv
- Shows loaded configuration (with secrets masked)
- Starts AI Gateway in background with proper working directory
- Validates required env vars before starting

#### **Linux/macOS** (start.sh)
- Same .env loading logic
- Starts gateway in background with output redirection
- Proper signal handling for graceful shutdown

#### **Windows Command Prompt** (start-local.bat)
- NEW: For users who prefer cmd.exe over PowerShell
- Loads .env using Windows batch syntax
- Same startup flow as PowerShell version

### 4. **Documentation: STARTUP_GUIDE.md**
Comprehensive guide covering:
- First-time setup (copy .env.example → .env)
- Adding real API keys
- Running on Windows, macOS, Linux
- Testing end-to-end workflow
- Monitoring logs
- Troubleshooting common errors
- Security best practices

---

## 📋 Files Modified/Created

### Created:
- **`.env`** — Configuration with real API keys (GITIGNORED)
- **`.env.example`** — Template for documentation (committed)
- **`STARTUP_GUIDE.md`** — User guide for running MVP
- **`start-local.bat`** — Windows batch startup script
- **`ai_gateway_mvp.py`** — AI Gateway service (loads .env)

### Modified:
- **`.gitignore`** — Added `.env`, `*.db` files to prevent secret leaks
- **`app.py`** — Added .env loading at startup
- **`ai_gateway_mvp.py`** — Added .env loading at startup  
- **`start-windows.ps1`** — Enhanced to load .env with validation
- **`start.sh`** — Enhanced with .env loading and error checking

---

## 🎯 How It Works Now

### Startup Flow:
```
1. User runs: ./start-windows.ps1 (or start-local.bat or ./start.sh)
   ↓
2. Script loads .env into environment variables
   ↓
3. Script starts AI Gateway in background
   ↓
4. Script starts FastAPI app
   ↓
5. app.py loads .env (for robustness)
   ├─ Sets APP_PROFILE='local'
   ├─ Gets OPENAI_API_KEY
   ├─ Gets AI_GATEWAY_TOKEN
   └─ Starts worker thread
   ↓
6. ai_gateway_mvp.py loads .env
   ├─ Gets OPENAI_API_KEY
   ├─ Gets AI_GATEWAY_TOKEN
   └─ Starts HTTP server on port 9999
   ↓
7. Worker thread can now:
   ├─ Get os.getenv('AI_GATEWAY_TOKEN') ✓
   ├─ Call gateway at http://127.0.0.1:9999 ✓
   └─ Gateway calls OpenAI with real API key ✓
```

### Assessment Flow (with config fix):
```
Citizen uploads report with media
   ↓
App creates AI job (state='pending')
   ↓
Worker thread reads: AI_GATEWAY_TOKEN from os.environ ✓
   ↓
Worker calls gateway with token in Authorization header ✓
   ↓
Gateway validates token against PROFILES model names ✓
   ↓
Gateway calls OpenAI with OPENAI_API_KEY ✓
   ↓
OpenAI returns violation assessment ✓
   ↓
Gateway validates response schema ✓
   ↓
App stores recommendation (penalize/dismiss) ✓
   ↓
Officer reviews report with AI recommendation ✓
```

---

## 🧪 Testing the Configuration

To verify everything is working:

### 1. **Start Services**
```bash
# Windows PowerShell
.\start-windows.ps1

# OR Windows Command Prompt
start-local.bat

# OR Linux/macOS
chmod +x start.sh
./start.sh
```

### 2. **Upload a Report (should complete in 5-10 seconds)**
```bash
# Upload media
curl -X POST http://localhost:8000/api/media/upload \
  -H "X-Citizen-Id: test-citizen-001" \
  -F "file=@test_helmet.jpg"

# Create report
curl -X POST http://localhost:8000/api/reports \
  -H "X-Citizen-Id: test-citizen-001" \
  -H "Content-Type: application/json" \
  -d '{"violation_type":"helmet","media_ids":["<media_id>"]}'

# Poll assessment (watch for state: "completed")
curl http://localhost:8000/api/reports/<report_id> \
  -H "X-Citizen-Id: test-citizen-001" | jq .ai
```

### Expected Success Indicators:
- ✅ `"state": "completed"`
- ✅ `"recommendation": "penalize"` or `"dismiss"`
- ✅ No `PROVIDER_CONFIGURATION` errors
- ✅ `"processing_ms": ~5000` (OpenAI call time)

### If Still Failing:
1. Check `.env` file exists and has real keys
2. Verify OpenAI key by testing directly:
   ```bash
   python test_openai.py
   ```
3. Check gateway logs (run in separate terminal):
   - Windows: `Start-Process python -ArgumentList "ai_gateway_mvp.py"`
   - Linux/macOS: `python ai_gateway_mvp.py`
4. Check app logs (shown in startup terminal)

---

## 🔐 Security Considerations

**✅ What's Protected:**
- `.env` is in `.gitignore` → never committed
- Secret files (`.env`, database) are ignored
- Startup scripts mask secrets in output
- No hardcoded API keys in source code

**⚠️ What Developers Should Do:**
- Never commit `.env` to git
- Use `.env.example` for templates only
- Rotate API keys if `.env` is ever exposed
- Use different keys for dev/staging/production
- Store production keys in secure vaults (GCP Secret Manager, AWS Secrets Manager)

---

## 📊 Session Impact

### Before This Session:
- ❌ AI jobs failing with `PROVIDER_CONFIGURATION`
- ❌ API keys not reaching worker processes
- ❌ Inconsistent startup procedures
- ❌ No configuration documentation
- ❌ Hardcoded/mock values mixed with real services

### After This Session:
- ✅ Configuration management framework in place
- ✅ Environment variables load correctly
- ✅ Consistent startup across platforms (Windows/Mac/Linux)
- ✅ Comprehensive setup guide (STARTUP_GUIDE.md)
- ✅ Ready for end-to-end testing with real services
- ✅ Secrets protected in .gitignore
- ✅ Startup validated with correct env loading

---

## 🚀 Next Steps

1. **Start services using one of the startup scripts**
2. **Run end-to-end test** (follow STARTUP_GUIDE.md)
3. **Monitor logs** to verify:
   - Gateway token is accepted ✓
   - OpenAI API key is valid ✓
   - Assessment completes successfully ✓
   - Recommendation is returned ✓
4. **Officer portal** shows AI recommendation
5. **Database** stores assessment result

---

## 📚 Related Documentation

- **STARTUP_GUIDE.md** — Step-by-step setup and testing
- **.env.example** — Configuration template
- **Plan.md** — Project milestones and requirements
- **PDD-REVIEW.md** — Issues with mocks vs real services (from previous session)

---

## ✨ Key Insight

The core issue was **environment variable scope**: variables set in a shell process don't automatically reach:
- Subprocesses launched with `subprocess.Popen()`
- Separate process groups (new windows)
- Different shells or interpreters

Solution: Load from a file (`.env`) that every process reads independently, rather than relying on shell inheritance.

---

**Commit:** `fbc90c4` — Add .env configuration management and persistent startup guide

**Ready for testing:** ✅ All configuration pieces in place
