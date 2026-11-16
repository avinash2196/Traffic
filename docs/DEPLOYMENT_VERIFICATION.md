# Deployment Verification Checklist

**Use this checklist to verify RoadWatch is correctly deployed and ready for use.**

---

## ✅ Pre-Deployment Checklist

Before running the startup script or deploying to GCP, verify:

- [ ] Python 3.11+ installed: `python --version`
- [ ] Git installed: `git --version`
- [ ] Git repository cloned: `cd Traffic` works
- [ ] No syntax errors in source: All `.py` files parse successfully
- [ ] Dependencies file exists: `requirements.txt` present
- [ ] Startup script has execute permission (macOS/Linux): `ls -la start.sh`
- [ ] Docker installed (if using Docker): `docker --version`
- [ ] Disk space available: >= 500 MB
- [ ] Network connectivity: `ping google.com` (for GCP) or localhost only (for local)

---

## ✅ Local Deployment Verification (Windows/macOS/Linux)

### Step 1: Run Startup Script

**Windows:**
```powershell
.\start-windows.ps1
```
Expected output: "Server running at http://127.0.0.1:8000"

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```
Expected output: "Uvicorn running on http://127.0.0.1:8000"

### Step 2: Verify Server Health

```bash
curl http://127.0.0.1:8000/health
```
Expected response:
```json
{"status": "ok", "version": "1.0", "database": "connected"}
```

**Checklist:**
- [ ] Server started without errors
- [ ] Health endpoint returns 200 OK
- [ ] Console shows "Application startup complete"
- [ ] No database errors in logs

### Step 3: Verify Web Interface

Open in browser:
- [ ] Citizen login: http://127.0.0.1:8000/citizen-login.html
  - [ ] Page loads without errors
  - [ ] Login form visible
  - [ ] Styling applied (not plain HTML)
- [ ] Officer login: http://127.0.0.1:8000/officer-login.html
  - [ ] Page loads without errors
  - [ ] Login form visible
  - [ ] Styling applied
- [ ] Swagger UI: http://127.0.0.1:8000/api/docs
  - [ ] All 7 endpoints listed
  - [ ] Try-it-out buttons functional

### Step 4: Verify Database

```bash
# Local SQLite check
sqlite3 roadwatch.db "SELECT COUNT(*) FROM reports;"
# Expected: 0 (empty database)

sqlite3 roadwatch.db ".schema"
# Expected: 3 tables (reports, media, events)
```

**Checklist:**
- [ ] Database file created: `roadwatch.db` exists
- [ ] Tables exist: `reports`, `media`, `events`
- [ ] No errors in schema
- [ ] Database is readable and writable

### Step 5: Test Citizen Workflow

1. **Login as citizen:**
   - Open http://127.0.0.1:8000/citizen-login.html
   - Enter any ID (e.g., `testuser1`)
   - Click "Login"

2. **Create report:**
   - Click "Report New Violation"
   - Select violation type: "Riding without helmet"
   - Enter location: "Delhi"
   - Upload a JPG image (< 25 MB)
   - Click "Submit Report"

3. **Verify report created:**
   - Note the report ID in the response
   - Check database:
     ```bash
     sqlite3 roadwatch.db "SELECT * FROM reports LIMIT 1;"
     ```
   - Expected: 1 row with status `Submitted`

**Checklist:**
- [ ] Login page accessible
- [ ] Citizen dashboard loads
- [ ] Report form displays all fields
- [ ] File upload works
- [ ] Report created with unique ID
- [ ] Status is "Submitted"
- [ ] Report appears in database

### Step 6: Test Officer Workflow

1. **Login as officer:**
   - Open http://127.0.0.1:8000/officer-login.html
   - Enter token: `demo-reviewer-token` (or any value)
   - Click "Login"

2. **View queue:**
   - Click "Review Queue"
   - Report created in Step 5 should appear

3. **Review report:**
   - Click on report
   - Verify you can see:
     - [ ] Original photo/video
     - [ ] Report details (location, type)
     - [ ] Timeline events
     - [ ] Evidence ZIP download button (M6)

4. **Submit decision:**
   - Select "Approve"
   - Enter reason: "Valid evidence"
   - Click "Submit Decision"

5. **Verify decision recorded:**
   - Check database:
     ```bash
     sqlite3 roadwatch.db "SELECT * FROM events WHERE report_id = '<ID>';"
     ```
   - Expected: Multiple events including "decision_submitted"

**Checklist:**
- [ ] Officer login works
- [ ] Review queue displays reports
- [ ] Report detail page loads
- [ ] Media preview works (image/video displays)
- [ ] Timeline shows events
- [ ] Decision form visible
- [ ] Decision submitted successfully
- [ ] Database updated with decision

### Step 7: Test Evidence Export (M6)

1. **Download ZIP:**
   - From officer detail page, click "Download Evidence ZIP"
   - File should auto-download as `evidence-<report_id>.zip`

2. **Verify ZIP contents:**
   ```bash
   unzip -l evidence-*.zip
   # Expected files:
   # - manifest.json
   # - original.jpg (or .mp4, etc.)
   # - timeline.json
   ```

3. **Verify ZIP structure:**
   ```bash
   unzip evidence-*.zip -d temp/
   cat temp/manifest.json  # Should contain report metadata
   ls -la temp/            # Should have all expected files
   ```

**Checklist:**
- [ ] Download button accessible
- [ ] ZIP file downloads
- [ ] ZIP contains manifest.json
- [ ] ZIP contains original media file
- [ ] ZIP contains timeline.json
- [ ] All files valid (not corrupted)

### Step 8: Verify Logging

Check that logs are being generated:
```bash
# Console should show:
# - Request logs (POST /api/reports, etc.)
# - No ERROR or CRITICAL messages
# - Health checks logged

# Check for error patterns:
grep -i "error\|exception\|traceback" logs/*
# Expected: No matches
```

**Checklist:**
- [ ] Logs display to console
- [ ] No ERROR level messages
- [ ] No exceptions in logs
- [ ] Requests are logged with timestamps

### Step 9: Verify Media Storage

Check that uploaded files are stored correctly:
```bash
ls -la media_store/
# Expected: Directory contains SHA-256 hash directories

# Count files
find media_store/ -type f | wc -l
# Expected: >= 1 (the file you uploaded)
```

**Checklist:**
- [ ] `media_store` directory exists
- [ ] Contains subdirectories (organized by hash prefix)
- [ ] Uploaded files are present
- [ ] Files are readable

---

## ✅ Docker Deployment Verification

### Step 1: Build Docker Image

```bash
docker build -t roadwatch .
```

Expected output:
```
...
Successfully built <IMAGE_ID>
Successfully tagged roadwatch:latest
```

**Checklist:**
- [ ] No build errors
- [ ] Image builds successfully
- [ ] Image size < 500 MB: `docker images roadwatch`
- [ ] Latest tag applied

### Step 2: Run Docker Container

```bash
docker run -d -p 8000:8000 --name roadwatch-test roadwatch
# Wait 5 seconds for startup

docker logs roadwatch-test
```

Expected output:
```
Application startup complete [INFO]
Uvicorn running on http://0.0.0.0:8000 [INFO]
```

**Checklist:**
- [ ] Container starts without errors
- [ ] Container running: `docker ps` shows roadwatch-test
- [ ] Logs show successful startup
- [ ] No critical errors in logs

### Step 3: Test Container Health

```bash
curl http://127.0.0.1:8000/health
```

Expected response:
```json
{"status": "ok", "database": "connected"}
```

**Checklist:**
- [ ] Health endpoint returns 200
- [ ] Database shows as connected
- [ ] Response is valid JSON

### Step 4: Verify File System

```bash
docker exec roadwatch-test ls -la /app/
# Expected: app.py, bootstrap.py, media.py, templates/, static/, requirements.txt

docker exec roadwatch-test ls -la /app/media_store/
# Expected: Directory exists (created at startup)
```

**Checklist:**
- [ ] All required files present in container
- [ ] `media_store` directory exists
- [ ] Permissions correct (not root-only)

### Step 5: Clean Up

```bash
docker stop roadwatch-test
docker rm roadwatch-test
```

**Checklist:**
- [ ] Container stopped cleanly
- [ ] No errors during cleanup

---

## ✅ GCP Deployment Verification

### Prerequisites (Before Deploying)

- [ ] `gcloud` CLI installed: `gcloud --version`
- [ ] Authenticated to GCP: `gcloud auth application-default login`
- [ ] Project set: `gcloud config set project PROJECT_ID`
- [ ] Required APIs enabled:
  ```bash
  gcloud services enable run.googleapis.com sqladmin.googleapis.com storage.googleapis.com
  ```
- [ ] Cloud SQL instance created: `gcloud sql instances list`
- [ ] Cloud Storage bucket created: `gsutil ls`

### Step 1: Deploy to Cloud Run

```bash
gcloud run deploy roadwatch \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300
```

Expected output:
```
Service [roadwatch] revision [roadwatch-00001-xxx] has been deployed
URL: https://roadwatch-XXXXXX.run.app
```

**Checklist:**
- [ ] Deployment completes without errors
- [ ] Service URL returned
- [ ] Service is "Healthy" (shown in GCP Console)

### Step 2: Test Cloud Run Service

```bash
export SERVICE_URL="https://roadwatch-XXXXXX.run.app"
curl $SERVICE_URL/health
```

Expected response:
```json
{"status": "ok", "database": "connected"}
```

**Checklist:**
- [ ] Health endpoint returns 200
- [ ] Service is accessible from internet
- [ ] HTTPS certificate valid (no SSL errors)

### Step 3: Verify Cloud SQL Connection

Check that Cloud Run can reach Cloud SQL:

```bash
gcloud run services describe roadwatch --region us-central1
# Look for: CLOUD_SQL_CONNECTION_NAME environment variable
# Format: PROJECT:REGION:INSTANCE

# Test from Cloud Run:
curl -s $SERVICE_URL/health | jq '.database'
# Expected: "connected"
```

**Checklist:**
- [ ] Environment variable set correctly
- [ ] Cloud SQL connection shows "connected"
- [ ] No "connection timeout" errors
- [ ] No "access denied" errors

### Step 4: Verify Cloud Storage (Media)

Check that media uploads are stored in GCS:

```bash
# Set environment variable:
gcloud run services update roadwatch \
  --region us-central1 \
  --set-env-vars MEDIA_STORE_PATH=gs://roadwatch-media-$PROJECT_ID

# Upload test media (via UI or API), then verify:
gsutil ls gs://roadwatch-media-$PROJECT_ID/
# Expected: Directory structure with uploaded files
```

**Checklist:**
- [ ] GCS bucket accessible from Cloud Run
- [ ] Files upload to GCS (not local disk)
- [ ] No "access denied" errors
- [ ] Bucket lifecycle policy set (if needed)

### Step 5: Test Web Interface (Cloud Run)

Open in browser:
- [ ] Citizen login: `$SERVICE_URL/citizen-login.html` loads
- [ ] Officer login: `$SERVICE_URL/officer-login.html` loads
- [ ] Swagger UI: `$SERVICE_URL/api/docs` displays all endpoints
- [ ] All pages have HTTPS (green lock icon)

**Checklist:**
- [ ] Pages load over HTTPS
- [ ] No mixed-content warnings
- [ ] Styling applied correctly
- [ ] Forms functional

### Step 6: Verify Logs (Cloud Run)

```bash
gcloud run services logs read roadwatch --limit 50 --region us-central1
# Look for:
# - Application startup logs
# - Request logs (GET /citizen-login.html, etc.)
# - No ERROR or CRITICAL messages
```

**Checklist:**
- [ ] Logs appear in Cloud Logging
- [ ] Startup logs show success
- [ ] No exceptions or errors
- [ ] Request rate normal (no spike)

### Step 7: Monitor Metrics (Cloud Run)

In GCP Console:
- Go to Cloud Run → roadwatch → Metrics
- [ ] Request count > 0 (if you accessed the service)
- [ ] Latency < 500ms (typical)
- [ ] Error rate = 0% (no 4xx or 5xx)
- [ ] Memory usage < 512 Mi

**Checklist:**
- [ ] Metrics dashboard shows data
- [ ] No performance issues (high latency, errors)
- [ ] Scaling works (if testing under load)
- [ ] Memory stays within limits

### Step 8: Test End-to-End Workflow (Cloud Run)

Same as Local Step 5-7:
1. Create report (citizen)
2. Review report (officer)
3. Download evidence ZIP
4. Verify in Cloud SQL database

**Checklist:**
- [ ] Citizen workflow works
- [ ] Officer workflow works
- [ ] Evidence ZIP download works
- [ ] Data persists in Cloud SQL
- [ ] Media stored in Cloud Storage

---

## ✅ Post-Deployment Verification

### Security Checks

```bash
# Check for secrets in logs
gcloud logging read "resource.type=cloud_run_revision AND severity=INFO" \
  --limit 100 | grep -i "api_key\|password\|token\|secret"
# Expected: No matches

# Verify CORS headers
curl -H "Origin: http://example.com" $SERVICE_URL/health -v
# Expected: No CORS errors (or appropriate Allow-Origin header)

# Verify no debugging endpoints exposed
curl $SERVICE_URL/debug/
# Expected: 404 Not Found
```

**Checklist:**
- [ ] No secrets in logs
- [ ] No debug endpoints accessible
- [ ] CORS configured correctly
- [ ] Security headers present (X-Frame-Options, etc.)

### Performance Checks

```bash
# Test response time (local)
time curl http://127.0.0.1:8000/api/docs > /dev/null
# Expected: < 100ms

# Test under load (optional, local only)
# Use: ab (Apache Bench), wrk, or hey
ab -n 100 -c 10 http://127.0.0.1:8000/health
# Expected: No errors, > 90% success rate
```

**Checklist:**
- [ ] Response time acceptable (< 500ms)
- [ ] No errors under normal load
- [ ] Scaling works (if auto-scaling enabled)

### Backup & Recovery Checks

```bash
# Local: Verify database backup
ls -la roadwatch.db*
# Expected: roadwatch.db present

# GCP: Verify Cloud SQL backups
gcloud sql backups list --instance=roadwatch-db
# Expected: Automated backups scheduled
```

**Checklist:**
- [ ] Database backups exist
- [ ] Backup schedule is automated
- [ ] Backup retention policy set
- [ ] Recovery tested (restore from backup)

---

## 🚨 Troubleshooting During Verification

| Issue | Symptom | Solution |
|-------|---------|----------|
| Port 8000 in use | `Address already in use` | Kill process: `lsof -i :8000 \| grep -v PID \| awk '{print $2}' \| xargs kill -9` |
| Database locked | `database is locked` | Remove lock: `rm roadwatch.db-wal roadwatch.db-shm` |
| Missing dependencies | `ModuleNotFoundError` | Install: `pip install -r requirements.txt` |
| Static files missing | 404 on `/static/css/base.css` | Verify directory exists: `ls static/css/base.css` |
| Jinja2 error | `TemplateNotFound` | Install: `pip install jinja2==3.1.2` |
| GCP auth failed | `Credentials could not be found` | Authenticate: `gcloud auth login` |
| Cloud SQL connection timeout | `connection timeout` | Check firewall, IP allowlist, service status |
| Health check failing | HTTP 500 on `/health` | Check logs: `docker logs <container>` or `gcloud logging read` |

---

## ✅ Final Sign-Off Checklist

**Mark all as complete before considering deployment verified:**

- [ ] Pre-deployment checks passed
- [ ] Local deployment verification passed (8 steps)
- [ ] Docker deployment verification passed (5 steps) [if using Docker]
- [ ] GCP deployment verification passed (8 steps) [if deploying to GCP]
- [ ] Post-deployment security checks passed
- [ ] Post-deployment performance checks passed
- [ ] Backup & recovery checks passed
- [ ] No critical errors in logs
- [ ] All 7 API endpoints functional
- [ ] Both citizen and officer workflows tested
- [ ] Evidence ZIP export tested
- [ ] Database schema validated
- [ ] Media storage verified
- [ ] HTTPS/TLS working (GCP only)
- [ ] Monitoring & alerts configured (GCP only)
- [ ] Support documentation available

---

## 📞 Verification Complete!

If all checks passed, your RoadWatch deployment is **ready for use** ✅

**Next steps:**
1. Share access credentials with users
2. Monitor logs and metrics
3. Run scheduled backups
4. Update security group rules (if needed)
5. Plan Phase 2 features (real auth, PostgreSQL, AI screening)

**For issues:** Refer to `LOCAL_DEPLOYMENT.md` or `GCP_DEPLOYMENT.md` troubleshooting sections.

---

**Document Version:** 1.0  
**Last Updated:** 2026-11-02  
**Applicable to:** RoadWatch MVP v1.0 and later

