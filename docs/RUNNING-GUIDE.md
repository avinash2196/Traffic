# RoadWatch Traffic MVP - Deployment & Running Guide

## ✓ RUNNING BOTH BACKEND & FRONTEND

The RoadWatch MVP is a **monolithic FastAPI application** - both backend API and frontend HTML/CSS/JS are served from the same process.

### Quick Start

```powershell
# Navigate to project directory
cd C:\Users\avina\Downloads\avinash-repo\v11\Traffic

# Run startup script
.\start-windows.ps1
```

Server will start at `http://127.0.0.1:8000`

---

## 🔧 Prerequisites Check

### Database
- ✓ **SQLite** (included, auto-initialized)
- ✓ Schema includes: citizens, reports, events, media, operators tables
- ✓ Location: `./roadwatch.db` (auto-created by startup script)

### Environment Variables
- ✓ `APP_PROFILE=local` (set by startup script)
- ✓ `AI_ADAPTER=disabled` (set by startup script, optional for Phase 2)
- ✗ `OPENAI_API_KEY` (NOT needed for MVP; optional if you want AI screening)

### API Keys Required for MVP
**NONE** - The MVP runs completely offline with no external dependencies.

| Feature | API Key Needed? | Status |
|---------|-----------------|--------|
| Citizen Signup/Login | No | ✓ Working |
| Report Upload | No | ✓ Working |
| Officer Review Queue | No | ✓ Working |
| Evidence Export | No | ✓ Working |
| AI Screening | Yes* | Optional (Phase 2) |

*AI screening is disabled by default. To enable, set `OPENAI_API_KEY=sk-...` and set `AI_ADAPTER=enabled`

### Table Entries Required
**NONE** - All tables are auto-created with proper schema.

| Table | Status | Auto-Created? |
|-------|--------|---------------|
| `citizens` | ✓ Ready | Yes |
| `reports` | ✓ Ready | Yes |
| `events` | ✓ Ready | Yes |
| `media` | ✓ Ready | Yes |
| `operators` | ✓ Ready | Yes |

---

## 🚀 Complete Startup Flow

### 1. **Database Initialization**
```
✓ Checks if roadwatch.db exists
✓ If missing: creates schema (all 5 tables with indexes)
✓ Sets up WAL mode for concurrency
✓ Sets up foreign key constraints
```

**No manual SQL needed** - bootstrap.py handles everything.

### 2. **Virtual Environment**
```
✓ Creates .venv if missing
✓ Installs all requirements from requirements.txt
✓ No additional pip installs needed
```

### 3. **Application Startup**
```
✓ Initializes database connection
✓ Mounts static files (CSS, JS, images)
✓ Loads Jinja2 templates (HTML pages)
✓ Starts uvicorn server on 127.0.0.1:8000
✓ Enables file watcher for auto-reload
```

---

## 🌐 Access Points (After Startup)

### Citizen Portal
- **Login Page**: http://127.0.0.1:8000/citizen-login.html
- **Dashboard**: http://127.0.0.1:8000/citizen-dashboard.html (after login)
- **Submit Report**: http://127.0.0.1:8000/citizen-report.html
- **View Reports**: http://127.0.0.1:8000/citizen-reports.html
- **Report Details**: http://127.0.0.1:8000/citizen-report-detail.html

### Officer Portal
- **Login Page**: http://127.0.0.1:8000/officer-login.html
- **Review Queue**: http://127.0.0.1:8000/officer-queue.html
- **Case Details**: http://127.0.0.1:8000/officer-detail.html

### API Documentation
- **Swagger UI**: http://127.0.0.1:8000/api/docs
- **Health Check**: http://127.0.0.1:8000/health
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

---

## 🔐 Demo Authentication (No Signup Required)

### Citizen Demo Account
```
citizen_id: citizen-demo-001
password: Demo@1234
```

**OR** Create new account via signup endpoint:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "yourname@example.com",
    "full_name": "Your Name",
    "citizen_id": "CITIZEN-YOUR-ID",
    "password": "SecurePass123!"
  }'
```

### Officer Demo Account
```
Auth Token: local-reviewer-only
(Hardcoded for MVP - shared demo token)
```

---

## 🗂️ File Storage

### Media Upload Location
- **Path**: `./media_store/` (created by startup script)
- **Capacity**: Limited only by disk space
- **Formats**: JPG, MP4 (validated on upload)
- **Size Limits**: 25 MB per file

### Database Location
- **Path**: `./roadwatch.db` (SQLite)
- **Size**: ~50 KB (empty), grows with data
- **Backup**: Copy `roadwatch.db` to backup location

---

## 🧪 Testing the Deployment

### 1. Health Check
```bash
curl http://127.0.0.1:8000/health
# Expected: {"status": "ok", "timestamp": "...", "service": "roadwatch-traffic-api"}
```

### 2. Citizen Signup
```bash
curl -X POST http://127.0.0.1:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","full_name":"Test","citizen_id":"TEST-1","password":"Pass123!"}'
# Expected: 201 Created with citizen_id in response
```

### 3. Citizen Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"citizen_id":"TEST-1","password":"Pass123!"}'
# Expected: 200 OK with session_token (JWT)
```

### 4. List Reports (Authenticated)
```bash
curl http://127.0.0.1:8000/api/reports \
  -H "Authorization: Bearer <session_token>"
# Expected: 200 OK with reports array (empty initially)
```

---

## ⚙️ Configuration Options

### Environment Variables (Optional)
```bash
# Set before running start-windows.ps1
$env:OPENAI_API_KEY = "sk-..."        # Enable AI screening (Phase 2)
$env:AI_ADAPTER = "enabled"           # Enable AI screening
$env:DATABASE_URL = "..."             # Use PostgreSQL instead of SQLite
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317"  # Send traces
```

### Database Configuration
To switch to PostgreSQL (Phase 2 only):
1. Set `$env:DATABASE_URL = "postgresql://user:pass@localhost/roadwatch"`
2. Create PostgreSQL database and run migrations
3. Restart application

---

## 🐛 Troubleshooting

### Issue: Port 8000 Already in Use
```
ERROR: [WinError 10013] Address already in use
```
**Solution**: Kill existing process or use different port
```bash
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Or use different port:
uvicorn app:app --host 127.0.0.1 --port 8001
```

### Issue: Database Lock
```
ERROR: database is locked
```
**Solution**: Delete old WAL files and restart
```bash
rm roadwatch.db-wal
rm roadwatch.db-shm
.\start-windows.ps1
```

### Issue: Static Files Not Found
```
404 Not Found: /static/...
```
**Solution**: Ensure `static/` directory exists with CSS/JS files

### Issue: Templates Not Loading
```
TemplateNotFound: citizen-login.html
```
**Solution**: Ensure `templates/` directory has HTML files

---

## 📊 What's Included in MVP

### ✓ Implemented Features
- [x] Citizen signup with password hashing (bcrypt)
- [x] Citizen login with JWT tokens
- [x] Report submission with file upload
- [x] Report status tracking (submitted → screening → review → decision)
- [x] Officer review queue with case details
- [x] Evidence export (ZIP with media + timeline)
- [x] Responsive UI (works on desktop & tablet)
- [x] API documentation (Swagger UI)
- [x] Database schema with indexes
- [x] Immutable audit trail (events table)

### ⚙️ Optional Features (Phase 2)
- [ ] AI media screening (requires OpenAI API key)
- [ ] PostgreSQL backend (documented, not implemented)
- [ ] Real OIDC integration
- [ ] SMS/email notifications
- [ ] VAHAN integration for vehicle data

---

## 📝 Quick Reference

| Task | Command | Expected Result |
|------|---------|-----------------|
| Start server | `.\start-windows.ps1` | Server listening on 127.0.0.1:8000 |
| Run tests | `python -m pytest tests/test_auth.py -v` | 23/23 tests PASS |
| Check health | `curl http://127.0.0.1:8000/health` | 200 OK with status |
| Reset database | `rm roadwatch.db*` + restart | Fresh schema created |
| View API docs | http://127.0.0.1:8000/api/docs | Swagger UI loads |
| Test signup | `python test_api.py` | All auth endpoints working |

---

## 🎯 Next Steps After Running

1. **Test Citizen Flow**
   - Sign up at http://127.0.0.1:8000/citizen-login.html
   - Go to dashboard
   - Submit a test report
   - View report status

2. **Test Officer Flow**
   - Log in at http://127.0.0.1:8000/officer-login.html
   - View review queue
   - Click on a report
   - Approve/reject report

3. **Test API**
   - Run: `python test_api.py`
   - Verify all endpoints respond correctly

4. **Export Evidence**
   - Submit a report as citizen
   - Download as ZIP from officer portal
   - Check manifest + media + timeline

---

**Status**: ✓ MVP Ready for Testing  
**Last Updated**: 2026-11-02  
**Backend**: FastAPI 0.162.0 + Uvicorn  
**Frontend**: Vanilla HTML + Jinja2  
**Database**: SQLite with WAL mode  

No external API keys or database setup required. Just run `.\start-windows.ps1` and go!
