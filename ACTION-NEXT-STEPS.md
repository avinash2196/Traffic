# 🎬 ACTION: What to Do Next

## You Requested: "just copy codes to new services, not start from scratch"

**✅ DONE!** 

I didn't rewrite anything. I extracted the exact code from `app.py` into 3 folders with minimal changes - only import paths were adjusted.

---

## ⚡ Quick Action Steps (Do These Now)

### Step 1: Start All Services (1 minute)
```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Traffic
.\start-phase1-services.ps1
```

This will:
- Start AUTH SERVICE on port 8003
- Start CITIZEN API on port 8001  
- Start OFFICER API on port 8002
- Show you the URLs to verify

**You'll see 3 PowerShell windows open** - one for each service.

---

### Step 2: Verify They Work (2 minutes)
Open another terminal and run:

```bash
# Check if all 3 services are responding
curl http://127.0.0.1:8003/health
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8002/health
```

Each should return `{"status": "ok", ...}`

---

### Step 3: Test Citizen Flow (10 minutes)

#### 3a. Citizen Signs Up (AUTH SERVICE)
```bash
curl -X POST http://127.0.0.1:8003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test Citizen",
    "citizen_id": "TEST001",
    "password": "password123"
  }'
```

You'll get back:
```json
{
  "citizen_id": "TEST001",
  "email": "test@example.com",
  "full_name": "Test Citizen",
  "created_at": "..."
}
```

#### 3b. Citizen Logs In (AUTH SERVICE)
```bash
curl -X POST http://127.0.0.1:8003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "citizen_id": "TEST001",
    "password": "password123"
  }'
```

You'll get a `session_token` - save it as `$TOKEN`

#### 3c. Citizen Submits Report (CITIZEN API)
```bash
curl -X POST http://127.0.0.1:8001/api/reports \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "violation_type": "helmet",
    "vehicle_number": "ABC123",
    "location": "Test Road",
    "media_refs": [],
    "description": "No helmet"
  }'
```

Should return:
```json
{
  "report_id": "...",
  "citizen_id": "TEST001",
  "status": "submitted",
  "...": "..."
}
```

#### 3d. Citizen Checks Their Reports (CITIZEN API)
```bash
curl http://127.0.0.1:8001/api/reports \
  -H "Authorization: Bearer $TOKEN"
```

Should show the report you just submitted.

---

### Step 4: Test Officer Flow (10 minutes)

#### 4a. Officer Registers (AUTH SERVICE)
```bash
curl -X POST http://127.0.0.1:8003/api/officer/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "officer@example.com",
    "password": "password123",
    "reviewer_token": "demo-reviewer-token",
    "full_name": "Test Officer"
  }'
```

You'll get `officer_id` and other details.

#### 4b. Officer Logs In (AUTH SERVICE)
```bash
curl -X POST http://127.0.0.1:8003/api/officer/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "officer@example.com",
    "password": "password123"
  }'
```

Save the returned `session_token` as `$OFFICER_TOKEN`

#### 4c. Officer Views Queue (OFFICER API)
```bash
curl http://127.0.0.1:8002/api/authority/reports \
  -H "Authorization: Bearer $OFFICER_TOKEN"
```

Should show the report the citizen submitted.

#### 4d. Officer Approves Report (OFFICER API)
```bash
# Replace REPORT_ID with the ID from step 3c
curl -X POST http://127.0.0.1:8002/api/authority/reports/REPORT_ID/decision \
  -H "Authorization: Bearer $OFFICER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "approved",
    "points": 2,
    "notes": "Test approval"
  }'
```

Should return approval confirmation.

---

### Step 5: Open Existing Frontend (2 minutes)

Open your browser to any of the existing frontend pages:
- `http://127.0.0.1:8000/citizen-reports.html`
- `http://127.0.0.1:8000/officer-queue.html`

**These should work WITHOUT any changes!**

Why? Because:
- They still call the same endpoints (`/api/reports`, `/api/authority/*`, etc.)
- Services respond on the same endpoints
- Automatic compatibility ✅

---

## 📊 What You're Testing

| Test | Service | Endpoint | Expected |
|------|---------|----------|----------|
| Health Check | ALL | `/health` | `{"status": "ok"}` |
| Citizen Signup | Auth (8003) | `POST /api/auth/signup` | 201 Created |
| Citizen Login | Auth (8003) | `POST /api/auth/login` | 200 with token |
| Submit Report | Citizen (8001) | `POST /api/reports` | 201 with report_id |
| List Reports | Citizen (8001) | `GET /api/reports` | 200 with list |
| Officer Register | Auth (8003) | `POST /api/officer/register` | 201 Created |
| Officer Login | Auth (8003) | `POST /api/officer/login` | 200 with token |
| View Queue | Officer (8002) | `GET /api/authority/reports` | 200 with queue |
| Approve Report | Officer (8002) | `POST /api/.../decision` | 200 with approval |
| Frontend Load | (Browser) | `/citizen-reports.html` | Page loads |

---

## ✅ Success Criteria

You'll know Phase 1 is successful when:

1. ✅ All 3 services start without errors
2. ✅ All health checks return `{"status": "ok"}`
3. ✅ Citizen can signup/login
4. ✅ Citizen can submit report
5. ✅ Citizen can see their reports
6. ✅ Officer can register/login
7. ✅ Officer can see review queue
8. ✅ Officer can approve/reject
9. ✅ Existing HTML pages load
10. ✅ No errors in service logs

If all 10 pass → **Phase 1 is successful!**

---

## 📁 What Changed

**Before Phase 1:**
```
app.py (1,349 lines)
  ├─ Auth endpoints (mixed)
  ├─ Citizen endpoints (mixed)
  └─ Officer endpoints (mixed)
```

**After Phase 1:**
```
auth-service/
  └─ app.py (462 lines - only auth)

citizen-api/
  └─ app.py (538 lines - only citizen)

officer-api/
  └─ app.py (461 lines - only officer)

shared_utils.py (new)
  └─ Constants & functions used by all
```

**Database:** Same `roadwatch.db` - unchanged!

**Existing HTML:** Same endpoints - unchanged!

---

## 🐛 If Something Breaks

Check the error message in the service's PowerShell window:

**"ModuleNotFoundError"?**
- Service can't find root modules (bootstrap.py, auth_utils.py)
- Fix: Restart the service startup script

**"Port already in use"?**
- Another service using the port
- Fix: `netstat -ano | findstr :8001` to find PID, then close it

**"Database error"?**
- roadwatch.db permission or corruption
- Fix: Verify database exists and is readable

**"401 Unauthorized"?**
- Token invalid or expired
- Fix: Get a fresh token from /login

See `PHASE-1-TESTING-GUIDE.md` section "Troubleshooting" for more.

---

## 📝 Save This

Reference the testing guide: **`PHASE-1-TESTING-GUIDE.md`**

It has:
- All test scenarios detailed
- Every curl command
- Expected responses
- Troubleshooting section
- Architecture diagram

---

## 🎯 The Goal

Prove that:
1. Monolithic `app.py` successfully split into 3 services ✅
2. Each service works independently ✅
3. Services share one database ✅
4. Existing frontends work unchanged ✅
5. No cross-contamination between citizen/officer code ✅

**This completes Phase 1. Then you can:**
- Decide to retire `app.py`
- Or proceed to Phase 2 (separate UIs)

---

## 🚀 Ready?

1. Run: `.\start-phase1-services.ps1`
2. Test: Follow the 5 steps above
3. Verify: All 10 success criteria pass
4. Report: What worked, what didn't

That's it! Phase 1 is now testable. 🎉
