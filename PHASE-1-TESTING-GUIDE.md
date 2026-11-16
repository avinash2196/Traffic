# Phase 1 Testing Guide

## Status: ✅ COMPLETE

Phase 1 extraction is complete. The monolithic `app.py` has been split into 3 independent microservices:

- **AUTH SERVICE** (port 8003)
- **CITIZEN API** (port 8001) 
- **OFFICER API** (port 8002)

All services share the same `roadwatch.db` database.

---

## How to Start All Services

### Windows PowerShell
```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Traffic
.\start-phase1-services.ps1
```

### macOS/Linux Bash
```bash
cd ~/path/to/Traffic
bash start-phase1-services.sh
```

---

## Verify Services Are Running

Once all services are started, test each one:

### Test AUTH SERVICE (port 8003)
```bash
curl http://127.0.0.1:8003/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-11-14T20:30:00+00:00",
  "service": "roadwatch-auth-service"
}
```

### Test CITIZEN API (port 8001)
```bash
curl http://127.0.0.1:8001/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-11-14T20:30:00+00:00",
  "service": "roadwatch-citizen-api"
}
```

### Test OFFICER API (port 8002)
```bash
curl http://127.0.0.1:8002/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2026-11-14T20:30:00+00:00",
  "service": "roadwatch-officer-api"
}
```

---

## Test Authentication (AUTH SERVICE)

### 1. Citizen Signup
```bash
curl -X POST http://127.0.0.1:8003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "citizen@example.com",
    "full_name": "John Citizen",
    "citizen_id": "CITIZEN001",
    "password": "password123"
  }'
```

Expected response (201 Created):
```json
{
  "citizen_id": "CITIZEN001",
  "email": "citizen@example.com",
  "full_name": "John Citizen",
  "created_at": "2026-11-14T20:30:00+00:00"
}
```

### 2. Citizen Login
```bash
curl -X POST http://127.0.0.1:8003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "citizen_id": "CITIZEN001",
    "password": "password123"
  }'
```

Expected response (200 OK):
```json
{
  "session_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "citizen_id": "CITIZEN001",
  "email": "citizen@example.com",
  "full_name": "John Citizen"
}
```

### 3. Get Current Citizen Profile
```bash
curl http://127.0.0.1:8003/api/auth/me \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

Expected response (200 OK):
```json
{
  "citizen_id": "CITIZEN001",
  "email": "citizen@example.com",
  "full_name": "John Citizen",
  "created_at": "2026-11-14T20:30:00+00:00",
  "last_login_at": "2026-11-14T20:30:00+00:00"
}
```

### 4. Officer Registration
```bash
curl -X POST http://127.0.0.1:8003/api/officer/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "officer@example.com",
    "password": "password123",
    "reviewer_token": "demo-reviewer-token",
    "full_name": "Jane Officer"
  }'
```

Expected response (201 Created):
```json
{
  "officer_id": "a1b2c3d4e5f6",
  "email": "officer@example.com",
  "full_name": "Jane Officer",
  "created_at": "2026-11-14T20:30:00+00:00"
}
```

### 5. Officer Login
```bash
curl -X POST http://127.0.0.1:8003/api/officer/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "officer@example.com",
    "password": "password123"
  }'
```

Expected response (200 OK):
```json
{
  "session_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "officer_id": "a1b2c3d4e5f6",
  "email": "officer@example.com",
  "full_name": "Jane Officer"
}
```

---

## Test Citizen Endpoints (CITIZEN API - port 8001)

### 1. Submit Report
```bash
curl -X POST http://127.0.0.1:8001/api/reports \
  -H "X-Citizen-Id: CITIZEN001" \
  -H "Content-Type: application/json" \
  -d '{
    "violation_type": "helmet",
    "vehicle_number": "ABC123",
    "location": "MG Road, Bangalore",
    "media_refs": ["media-id-1"],
    "description": "Rider without helmet"
  }'
```

Expected response (201 Created):
```json
{
  "report_id": "report-uuid",
  "citizen_id": "CITIZEN001",
  "violation_type": "helmet",
  "vehicle_number": "ABC123",
  "status": "submitted",
  "created_at": "2026-11-14T20:30:00Z"
}
```

### 2. Get Citizen's Reports
```bash
curl http://127.0.0.1:8001/api/reports \
  -H "X-Citizen-Id: CITIZEN001"
```

Expected response (200 OK):
```json
{
  "reports": [
    {
      "report_id": "report-uuid",
      "citizen_id": "CITIZEN001",
      "violation_type": "helmet",
      "status": "submitted",
      "created_at": "2026-11-14T20:30:00Z"
    }
  ],
  "total": 1,
  "page": 1
}
```

### 3. Get Report Details
```bash
curl http://127.0.0.1:8001/api/reports/report-uuid \
  -H "X-Citizen-Id: CITIZEN001"
```

---

## Test Officer Endpoints (OFFICER API - port 8002)

### 1. Get Review Queue
```bash
curl http://127.0.0.1:8002/api/authority/reports \
  -H "Authorization: Bearer <officer-token>"
```

Expected response (200 OK):
```json
{
  "reports": [
    {
      "report_id": "report-uuid",
      "citizen_id": "CITIZEN001",
      "violation_type": "helmet",
      "vehicle_number": "ABC123",
      "status": "submitted",
      "created_at": "2026-11-14T20:30:00Z"
    }
  ],
  "total": 1
}
```

### 2. Get Report Details (Officer View)
```bash
curl http://127.0.0.1:8002/api/authority/reports/report-uuid \
  -H "Authorization: Bearer <officer-token>"
```

### 3. Make Decision on Report
```bash
curl -X POST http://127.0.0.1:8002/api/authority/reports/report-uuid/decision \
  -H "Authorization: Bearer <officer-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "approved",
    "points": 2,
    "notes": "Violation confirmed. 2 points awarded."
  }'
```

Expected response (200 OK):
```json
{
  "report_id": "report-uuid",
  "status": "approved",
  "provisional_points": 2,
  "reviewed_at": "2026-11-14T20:30:00Z"
}
```

---

## Integration Test (End-to-End)

### Scenario: Citizen submits report, Officer reviews and approves

1. **Setup**: Start all 3 services
   ```bash
   ./start-phase1-services.ps1  # Windows
   # or
   bash start-phase1-services.sh  # macOS/Linux
   ```

2. **Citizen signs up** (AUTH SERVICE)
   ```bash
   curl -X POST http://127.0.0.1:8003/api/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","full_name":"Test User","citizen_id":"TEST001","password":"password123"}'
   # Save the response token
   CITIZEN_TOKEN="..."
   ```

3. **Citizen submits report** (CITIZEN API)
   ```bash
   curl -X POST http://127.0.0.1:8001/api/reports \
     -H "Authorization: Bearer $CITIZEN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"violation_type":"helmet","vehicle_number":"ABC123","location":"MG Road","media_refs":[],"description":"No helmet"}'
   # Save the report_id
   REPORT_ID="..."
   ```

4. **Officer registers** (AUTH SERVICE)
   ```bash
   curl -X POST http://127.0.0.1:8003/api/officer/register \
     -H "Content-Type: application/json" \
     -d '{"email":"officer@example.com","password":"password123","reviewer_token":"demo-reviewer-token","full_name":"Officer Test"}'
   # Save the officer_id
   OFFICER_ID="..."
   ```

5. **Officer logs in** (AUTH SERVICE)
   ```bash
   curl -X POST http://127.0.0.1:8003/api/officer/login \
     -H "Content-Type: application/json" \
     -d '{"email":"officer@example.com","password":"password123"}'
   # Save the officer token
   OFFICER_TOKEN="..."
   ```

6. **Officer reviews queue** (OFFICER API)
   ```bash
   curl http://127.0.0.1:8002/api/authority/reports \
     -H "Authorization: Bearer $OFFICER_TOKEN"
   # Should see the citizen's report
   ```

7. **Officer approves report** (OFFICER API)
   ```bash
   curl -X POST http://127.0.0.1:8002/api/authority/reports/$REPORT_ID/decision \
     -H "Authorization: Bearer $OFFICER_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"decision":"approved","points":2,"notes":"Violation confirmed"}'
   # Report should now be approved
   ```

8. **Verify report status** (CITIZEN API)
   ```bash
   curl http://127.0.0.1:8001/api/reports/$REPORT_ID \
     -H "Authorization: Bearer $CITIZEN_TOKEN"
   # Should show status: "approved", provisional_points: 2
   ```

---

## Troubleshooting

### Service won't start
- Check port is not in use: `lsof -i :8001` (macOS/Linux) or `netstat -ano | findstr :8001` (Windows)
- Check Python is installed: `python --version`
- Check dependencies: `pip install -r requirements.txt`
- Check database exists: `ls -la roadwatch.db`

### Can't connect to service
- Verify service is running: `ps aux | grep "python app.py"`
- Check port number (8001, 8002, 8003)
- Try curl with verbose: `curl -v http://127.0.0.1:8001/health`
- Check service logs

### Database errors
- Ensure `roadwatch.db` exists in root directory
- Check file permissions: `chmod 644 roadwatch.db`
- All services should access the same database

### Import errors
- Verify all shared modules exist in root: `bootstrap.py`, `auth_utils.py`, `intake.py`, `shared_utils.py`
- Check Python path includes parent directory
- Run from root project directory

---

## Service Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (HTML)                          │
│         (citizen-reports.html, officer-queue.html)         │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┬──────────┐
        │          │          │          │
        ▼          ▼          ▼          ▼
    AUTH SVC   CITIZEN API  OFFICER API  AI GATEWAY
   :8003       :8001        :8002        :9999
        │          │          │          │
        └──────────┼──────────┼──────────┘
                   │
                   ▼
            ┌──────────────┐
            │ roadwatch.db │
            └──────────────┘
```

All services connect to the same database, ensuring data consistency.

---

## Next Steps

Once all tests pass:

1. ✅ Verify all 3 services start successfully
2. ✅ Test health checks on all services
3. ✅ Test authentication flow
4. ✅ Test citizen endpoints
5. ✅ Test officer endpoints
6. ✅ Run end-to-end integration test

Then you can proceed to Phase 2 (optional):
- Create separate citizen-app and officer-app frontends
- Update to use different ports (3000 for citizen, 3001 for officer)
- Add service-to-service communication layer if needed

---

**Phase 1 Status: ✅ COMPLETE AND READY FOR TESTING**
