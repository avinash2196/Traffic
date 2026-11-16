# RoadWatch MVP - Quick Start Guide

## 🚀 Setup (First Time Only)

### 1. Copy Configuration Template
```bash
cp .env.example .env
```

### 2. Add Your Real API Keys
Edit `.env` and add your actual keys:
```
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
GEMINI_API_KEY=YOUR-GEMINI-KEY-HERE
```

**Get API Keys:**
- **OpenAI**: https://platform.openai.com/account/api-keys (costs money)
- **Gemini**: https://aistudio.google.com/app/apikey (free tier available)

### 3. Save `.env` Securely
⚠️ **IMPORTANT:** `.env` is in `.gitignore` - NEVER commit it to git!

## 🎯 Running the MVP

### **Windows (PowerShell)**
```powershell
.\start-windows.ps1
```

### **macOS/Linux (Bash)**
```bash
chmod +x start.sh
./start.sh
```

Both scripts will:
1. ✅ Check Python installation
2. ✅ Create virtual environment
3. ✅ Install dependencies
4. ✅ Load `.env` configuration
5. ✅ Start AI Gateway (port 9999)
6. ✅ Start FastAPI app (port 8000)

## 📋 What Happens at Startup

```
Loading configuration from .env...
  ✓ OPENAI_API_KEY = ***
  ✓ GATEWAY_TOKEN = ***
  ✓ Configuration loaded

✓ Python found: Python 3.11.x
✓ Virtual environment exists
🔌 Activating virtual environment...
📚 Installing dependencies...
✓ Dependencies installed

🤖 Starting AI Gateway on port 9999...
✓ AI Gateway started (PID: 12345)

========================================
🚀 RoadWatch Traffic MVP - STARTING
========================================

Configuration:
  API Host: 127.0.0.1
  API Port: 8000
  Gateway URL: http://127.0.0.1:9999

Web Interface:
  Citizen Portal: http://127.0.0.1:8000/citizen-login.html
  Officer Portal: http://127.0.0.1:8000/officer-login.html

API Documentation:
  Swagger UI: http://127.0.0.1:8000/api/docs
  Health: http://127.0.0.1:8000/health

Control:
  Stop server: Press Ctrl+C
```

## 🧪 Testing End-to-End

Once the app is running:

### **1. Upload a Report**
```bash
curl -X POST http://localhost:8000/api/reports \
  -H "X-Citizen-Id: test-citizen-001" \
  -H "Content-Type: application/json" \
  -d '{
    "violation_type": "helmet",
    "description": "Rider without helmet"
  }'
```

Response (example):
```json
{
  "report_id": "eb93b6cf846e4b93",
  "status": "awaiting-review",
  "created_at": "2026-11-13T23:14:26Z",
  "citizen_id": "test-citizen-001",
  "ai": {
    "state": "pending",
    "attempt_count": 0
  }
}
```

### **2. Upload Media for That Report**
```bash
curl -X POST http://localhost:8000/api/reports/eb93b6cf846e4b93/media \
  -H "X-Citizen-Id: test-citizen-001" \
  -F "file=@test_helmet.jpg"
```

### **3. Poll Assessment Status**
```bash
# Check every 5 seconds (OpenAI takes ~5-10 seconds per assessment)
for i in {1..10}; do
  curl -s http://localhost:8000/api/reports/eb93b6cf846e4b93 | jq .ai
  sleep 5
done
```

Watch for:
- ✅ `"state": "completed"` = AI assessment finished
- ✅ `"recommendation": "penalize"` or `"dismiss"` = AI decision
- ⚠️ `"state": "failed"` = Something went wrong (check logs)

### **4. Officer Reviews Report**
```bash
curl -X GET http://localhost:8000/api/queue \
  -H "X-Reviewer-Token: OqROzN00FM7z7D1_OFlt9nKKsMpInqN0pUuq3PyEofQ"
```

## 📊 Monitoring Logs

**In a separate terminal:**

### **Windows (PowerShell)**
```powershell
# AI Gateway logs
Get-Content gateway.log -Wait

# FastAPI app logs (shown in startup terminal)
```

### **macOS/Linux (Bash)**
```bash
# AI Gateway logs
tail -f gateway.log

# FastAPI app logs (shown in startup terminal)
```

## ❌ Troubleshooting

### **"ERROR: OPENAI_API_KEY not set in .env"**
→ Did you copy `.env.example` to `.env`? Did you add your real key?

### **"502 Bad Gateway" / "MODEL_OUTPUT_UNAVAILABLE"**
→ AI Gateway crashed or isn't responding
→ Check `gateway.log` for OpenAI API errors
→ Verify your `OPENAI_API_KEY` is correct (not expired)

### **"HTTP 401 Unauthorized" on officer endpoints**
→ Gateway token is invalid or missing
→ Check `.env` has `GATEWAY_TOKEN=OqROzN00FM7z7D1_OFlt9nKKsMpInqN0pUuq3PyEofQ`

### **"Port 8000 already in use"**
→ Kill existing Python process:
```bash
# Windows
taskkill /F /PID <process_id>

# macOS/Linux
kill <process_id>
```

### **"Cannot find module 'openai'" or similar**
→ Virtual environment activation failed
→ Try: `python -m pip install -r requirements.txt`

## 🔑 Understanding .env

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI authentication | `sk-proj-...` |
| `GEMINI_API_KEY` | Google Gemini auth (optional) | `AIzaSy...` |
| `GATEWAY_TOKEN` | AI Gateway auth token | `OqROzN...` |
| `AI_GATEWAY_URL` | Where app finds gateway | `http://127.0.0.1:9999` |
| `FASTAPI_HOST` | App server host | `127.0.0.1` |
| `FASTAPI_PORT` | App server port | `8000` |
| `DATABASE_URL` | Database connection | `sqlite:///roadwatch.db` |

## 🛡️ Security Best Practices

1. ✅ **`.env` is GITIGNORED** - Your secrets won't leak to git
2. ✅ **Never share `.env`** - It contains real API keys
3. ✅ **Use `.env.example` for templates** - Share this instead, with placeholder values
4. ✅ **Rotate keys regularly** - If `.env` is ever exposed, regenerate API keys
5. ✅ **Use environment-specific keys** - Don't reuse dev keys in production

## 📝 Creating `.env` from Scratch

If you want to create `.env` manually without copying `.env.example`:

```bash
# Windows (PowerShell)
@"
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
GEMINI_API_KEY=YOUR-KEY
GATEWAY_TOKEN=OqROzN00FM7z7D1_OFlt9nKKsMpInqN0pUuq3PyEofQ
AI_GATEWAY_URL=http://127.0.0.1:9999
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
DATABASE_URL=sqlite:///roadwatch.db
"@ | Set-Content .env

# macOS/Linux (Bash)
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
GEMINI_API_KEY=YOUR-KEY
GATEWAY_TOKEN=OqROzN00FM7z7D1_OFlt9nKKsMpInqN0pUuq3PyEofQ
AI_GATEWAY_URL=http://127.0.0.1:9999
FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
DATABASE_URL=sqlite:///roadwatch.db
EOF
```

Then edit and add your real API keys.

## 🎓 Next Steps

1. Run the startup script
2. Upload a test report with media
3. Watch the AI assessment complete
4. Review recommendation in officer portal
5. Check logs for any errors

Happy testing! 🚗✨
