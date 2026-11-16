# RoadWatch Quick Reference Card

## 🚀 Quick Start (Copy-Paste)

### Windows
```powershell
cd Traffic
.\start-windows.ps1
```
Access: http://127.0.0.1:8000/citizen-login.html

### macOS/Linux
```bash
cd Traffic
chmod +x start.sh
./start.sh
```
Access: http://127.0.0.1:8000/citizen-login.html

---

## 🌐 URLs

| Service | URL |
|---------|-----|
| Citizen Portal | http://127.0.0.1:8000/citizen-login.html |
| Officer Portal | http://127.0.0.1:8000/officer-login.html |
| API Docs | http://127.0.0.1:8000/api/docs |
| Health Check | http://127.0.0.1:8000/health |

---

## 👤 Demo Credentials

| Role | Login | Password/Token |
|------|-------|----------------|
| Citizen | Any ID | (demo, no validation) |
| Officer | Any Token | (demo, no validation) |

**Example:**
- Citizen ID: `user123`
- Officer Token: `demo-reviewer-token`

---

## 📦 Files & Directories

```
Traffic/
├── app.py                  # FastAPI server
├── bootstrap.py            # Database schema
├── media.py                # Media validation
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker build
├── start.sh / .ps1         # Startup scripts
├── templates/              # 8 HTML pages
├── static/                 # CSS + JS
├── LOCAL_DEPLOYMENT.md     # Local setup guide
├── GCP_DEPLOYMENT.md       # GCP production guide
├── .env.example            # Environment variables
├── COMPLETION.md           # Project summary
├── Plan.md                 # Architecture
└── README.md               # Overview
```

---

## 🗄️ Database

### Tables
- `reports` — Violation reports
- `media` — Attached files
- `events` — Audit trail (append-only)

### View data (local)
```bash
sqlite3 roadwatch.db "SELECT * FROM reports;"
```

### Reset database
```bash
rm roadwatch.db
# Restart app to recreate
```

---

## 🔐 Environment Variables

### Required (MVP)
```bash
ROADWATCH_REVIEWER_TOKEN=local-reviewer-only
```

### Optional
```bash
DATABASE_URL=sqlite:///./roadwatch.db
MEDIA_STORE_PATH=./media_store
LOG_LEVEL=INFO
OPENAI_API_KEY=sk-...  # AI screening
```

### Load from file
```bash
cp .env.example .env
# Edit .env with your values
# App automatically loads .env on startup
```

---

## 📊 API Endpoints

### Citizen
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/reports` | Create report |
| GET | `/api/reports` | List reports |
| GET | `/api/reports/{id}` | Report detail |

### Officer
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/authority/queue` | Review queue |
| GET | `/api/authority/reports/{id}` | Case detail |
| POST | `/api/authority/reports/{id}/decision` | Submit decision |
| GET | `/api/authority/reports/{id}/evidence.zip` | Download ZIP |

**Full docs:** http://127.0.0.1:8000/api/docs

---

## 🧪 Test Workflow (5 steps)

1. **Citizen Login:** http://127.0.0.1:8000/citizen-login.html
   - Enter any ID (e.g., `user1`)
2. **Create Report:** Report Violation → Select type → Upload photo/video → Submit
3. **Get Report ID:** Note the report ID from response
4. **Officer Login:** http://127.0.0.1:8000/officer-login.html
   - Enter any token (e.g., `token1`)
5. **Review & Decide:** Review Queue → Select case → Approve/Reject → Download ZIP (M6)

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Change port: `uvicorn app:app --port 8001` |
| ModuleNotFoundError | Activate venv: `.venv\Scripts\Activate.ps1` |
| Database locked | Kill Python: `pkill python` |
| Static files missing | Verify `static/` directory exists |
| Jinja2 error | Install: `pip install jinja2==3.1.2` |

**Full troubleshooting:** See `LOCAL_DEPLOYMENT.md`

---

## 🚢 Docker

### Build
```bash
docker build -t roadwatch .
```

### Run
```bash
docker run -p 8000:8000 roadwatch
```

### Stop
```bash
docker ps  # Find CONTAINER_ID
docker stop <CONTAINER_ID>
```

---

## ☁️ GCP Deployment (10 minutes)

### Quick Deploy
```bash
gcloud run deploy roadwatch \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

### Full Setup
See `GCP_DEPLOYMENT.md` for:
- PostgreSQL Cloud SQL setup
- Cloud Storage configuration
- Monitoring & scaling
- Security hardening
- CI/CD pipeline

---

## 📋 Deployment Checklist

### Local
- [ ] Python 3.11+ installed
- [ ] Run `./start.sh` or `start-windows.ps1`
- [ ] Access http://127.0.0.1:8000/citizen-login.html
- [ ] Create test report
- [ ] Review in officer portal
- [ ] Download evidence ZIP

### GCP
- [ ] APIs enabled (Cloud Run, Cloud SQL, Storage)
- [ ] PostgreSQL instance created
- [ ] Docker image pushed to GCR
- [ ] Cloud Run service deployed
- [ ] Environment variables set
- [ ] Database migrated
- [ ] HTTPS/TLS verified
- [ ] Monitoring configured
- [ ] Backups enabled

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Project overview |
| `LOCAL_DEPLOYMENT.md` | Local setup (detailed) |
| `GCP_DEPLOYMENT.md` | GCP production (detailed) |
| `COMPLETION.md` | Project summary |
| `Plan.md` | Architecture & decisions |
| `.env.example` | Environment template |
| `verify_integration.py` | Integration check |

---

## 🔗 Quick Links

- **Local Setup:** `LOCAL_DEPLOYMENT.md` (9 KB, ~15 min read)
- **GCP Setup:** `GCP_DEPLOYMENT.md` (14 KB, ~20 min read)
- **API Reference:** Swagger UI at http://127.0.0.1:8000/api/docs
- **Environment:** `.env.example` (8 KB, copy & fill)

---

## ✅ Health Checks

```bash
# API health
curl http://127.0.0.1:8000/health

# Database (local)
sqlite3 roadwatch.db "SELECT COUNT(*) FROM reports;"

# Integration verification
python verify_integration.py
```

---

## 🎯 Next Steps

1. **Try locally** (5 min) → Run startup script
2. **Test workflow** (5 min) → Create report, review, download ZIP
3. **Review docs** (30 min) → Read COMPLETION.md
4. **Deploy to GCP** (30 min) → Follow GCP_DEPLOYMENT.md
5. **Go production** → Add security, monitoring, CI/CD

---

## 📞 Support

- **Local issues:** See `LOCAL_DEPLOYMENT.md` troubleshooting
- **GCP issues:** See `GCP_DEPLOYMENT.md` troubleshooting
- **API issues:** Check http://127.0.0.1:8000/api/docs
- **Code:** Review comments in `app.py`, `bootstrap.py`

---

**Version:** 1.0 (MVP Complete)  
**Last Updated:** 2026-11-02  
**Status:** Production Ready ✅

