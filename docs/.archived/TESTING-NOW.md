# RoadWatch MVP - Testing Checklist

**Status:** All services started ✅ | **Time:** ~5 minutes to test | **Date:** 2026-11-15

---

## 🚀 Quick Health Check (1 minute)

Open PowerShell and run:

```powershell
# Test all service endpoints
$services = @{
    "Auth Service"     = "http://127.0.0.1:9003/health"
    "Citizen API"      = "http://127.0.0.1:9001/health"
    "Officer API"      = "http://127.0.0.1:9002/health"
}

foreach ($name in $services.Keys) {
    try {
        $response = Invoke-WebRequest -Uri $services[$name] -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        Write-Host "✅ $name - OK" -ForegroundColor Green
    } catch {
        Write-Host "❌ $name - FAILED" -ForegroundColor Red
    }
}
```

---

## 🧪 Test Scenarios (4 minutes)

### Test 1: Citizen Signup & Login (2 minutes)

**Request:**
```bash
curl -X POST http://127.0.0.1:9003/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "citizen@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

**Expected Response:** 201 Created
```json
{
  "citizen_id": "citizen-uuid",
  "email": "citizen@example.com",
  "session_token": "eyJhbGc...",
  "expires_in": 86400
}
```

**Then login:**
```bash
curl -X POST http://127.0.0.1:9003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "citizen@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected Response:** 200 OK (same structure as signup)

---

### Test 2: Upload Media (1 minute)

**Prerequisite:** Use token from Test 1

**PowerShell:**
```powershell
$token = "eyJhbGc..."  # From signup response

# Create a test image
$imageBytes = [System.Convert]::FromBase64String("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
[System.IO.File]::WriteAllBytes("C:\temp\test.png", $imageBytes)

# Upload
$response = Invoke-WebRequest -Uri "http://127.0.0.1:9001/api/media/upload" `
  -Method Post `
  -Headers @{"Authorization" = "Bearer $token"} `
  -Form @{file = Get-Item "C:\temp\test.png"} `
  -UseBasicParsing

$response.Content | ConvertFrom-Json | ConvertTo-Json
```

**Expected Response:** 201 Created
```json
{
  "media_id": "media-uuid",
  "filename": "test.png",
  "size": 68,
  "format": "image",
  "sha256": "hash..."
}
```

---

### Test 3: Submit Report (1 minute)

**Prerequisite:** Token from Test 1, Media ID from Test 2

**Request:**
```bash
curl -X POST http://127.0.0.1:9001/api/reports \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGc..." \
  -d '{
    "violation_type": "helmet",
    "vehicle_number": "DL01AB1234",
    "location": "Connaught Place, Delhi",
    "media_ids": ["media-uuid"]
  }'
```

**Expected Response:** 201 Created
```json
{
  "report_id": "report-uuid",
  "citizen_id": "citizen-uuid",
  "status": "submitted",
  "provisional_points": 0,
  "created_at": "2026-11-15T14:30:00Z",
  "media": [
    {
      "media_id": "media-uuid",
      "filename": "test.png",
      "format": "image"
    }
  ]
}
```

---

### Test 4: Fetch Reports (Citizen View)

**Request:**
```bash
curl -X GET "http://127.0.0.1:9001/api/reports?page=1&size=10" \
  -H "Authorization: Bearer eyJhbGc..."
```

**Expected Response:** 200 OK
```json
{
  "reports": [
    {
      "report_id": "report-uuid",
      "violation_type": "helmet",
      "vehicle_number": "DL01AB1234",
      "status": "submitted",
      "provisional_points": 0,
      "created_at": "2026-11-15T14:30:00Z"
    }
  ],
  "page": 1,
  "size": 10,
  "total": 1
}
```

---

### Test 5: Officer Login

**Request:**
```bash
curl -X POST http://127.0.0.1:9003/api/officer/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "officer@example.com",
    "password": "OfficerPass123!",
    "token": "demo-reviewer-token"
  }'
```

**Expected Response:** 200 OK
```json
{
  "officer_id": "officer-uuid",
  "email": "officer@example.com",
  "session_token": "eyJhbGc...",
  "expires_in": 86400
}
```

---

### Test 6: Officer Review Queue

**Prerequisite:** Officer token from Test 5

**Request:**
```bash
curl -X GET "http://127.0.0.1:9002/api/authority/reports?status=submitted&page=1&size=10" \
  -H "Authorization: Bearer <officer_token>"
```

**Expected Response:** 200 OK
```json
{
  "reports": [
    {
      "report_id": "report-uuid",
      "citizen_id": "citizen-uuid",
      "violation_type": "helmet",
      "vehicle_number": "DL01AB1234",
      "location": "Connaught Place, Delhi",
      "status": "submitted",
      "created_at": "2026-11-15T14:30:00Z"
    }
  ],
  "page": 1,
  "size": 10,
  "total": 1
}
```

---

### Test 7: Make Decision (Officer)

**Request:**
```bash
curl -X POST http://127.0.0.1:9002/api/authority/reports/report-uuid/decision \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <officer_token>" \
  -d '{
    "action": "approve",
    "provisional_points": 2,
    "notes": "Clear violation, helmet not worn properly"
  }'
```

**Expected Response:** 200 OK
```json
{
  "report_id": "report-uuid",
  "status": "approved",
  "provisional_points": 2,
  "updated_at": "2026-11-15T14:35:00Z",
  "event_id": "event-uuid"
}
```

---

### Test 8: Verify Event Log (Database)

**Check that events are immutable:**

```bash
# Connect to SQLite
sqlite3 roadwatch.db

# View event log
SELECT id, report_id, event_type, actor_type, created_at FROM events ORDER BY created_at DESC LIMIT 10;

# Verify no UPDATE on events
UPDATE events SET event_type = 'modified' WHERE id = 'event-uuid';
-- Should fail or be prevented
```

**Expected:** Event table is append-only, no UPDATE operations possible

---

## 📊 Test Results Form

Fill in as you test:

```markdown
| Test | Status | Time | Notes |
|------|--------|------|-------|
| Health Check | ☐ Pass ☐ Fail | ___ | |
| Citizen Signup | ☐ Pass ☐ Fail | ___ | |
| Citizen Login | ☐ Pass ☐ Fail | ___ | |
| Media Upload | ☐ Pass ☐ Fail | ___ | |
| Submit Report | ☐ Pass ☐ Fail | ___ | |
| Fetch Reports | ☐ Pass ☐ Fail | ___ | |
| Officer Login | ☐ Pass ☐ Fail | ___ | |
| Review Queue | ☐ Pass ☐ Fail | ___ | |
| Make Decision | ☐ Pass ☐ Fail | ___ | |
| Event Log | ☐ Pass ☐ Fail | ___ | |
```

---

## 🛠️ Troubleshooting

### "Connection refused" on any endpoint
1. Check service is running:
   ```powershell
   Get-Process python | Format-Table Id, ProcessName
   ```
2. Check port is free:
   ```powershell
   netstat -ano | findstr "900[123]"
   ```
3. Restart the service:
   - Stop PowerShell window running the service
   - Re-run `START-ALL.ps1`

### "Invalid token" error
1. Verify token format: should start with `eyJ`
2. Verify token isn't expired (24-hour expiration)
3. Re-login to get fresh token

### "File not found" on media download
1. Verify media was uploaded successfully (test 2)
2. Check media_store directory exists:
   ```powershell
   Test-Path ./media_store
   ```
3. Check permissions:
   ```powershell
   Get-Acl ./media_store | Format-List
   ```

### Database locked error
1. Close any other SQLite connections
2. Check for leftover processes:
   ```powershell
   Get-Process sqlite* -ErrorAction SilentlyContinue
   ```
3. Restart all services

---

## 📈 Performance Expectations

| Operation | Expected Time | Threshold |
|-----------|---------------|-----------|
| Health check | < 100ms | 500ms |
| Signup | 100-200ms | 1s |
| Login | 100-150ms | 1s |
| Media upload (1MB) | 200-500ms | 2s |
| Submit report | 100-200ms | 1s |
| Fetch reports | 50-100ms | 500ms |
| Make decision | 100-200ms | 1s |

---

## ✅ Sign-Off

- [ ] All health checks passed
- [ ] All 8 test scenarios passed
- [ ] No errors in service logs
- [ ] Database events are immutable
- [ ] Performance within thresholds
- [ ] Ready for production testing

**Tester:** _________________ | **Date:** _________________ | **Time:** _________________

---

## 📞 Next Steps

1. **If all tests pass:** Proceed to integration testing (Multi-user scenarios)
2. **If some fail:** Check logs in each service window, troubleshoot, and retry
3. **If critical failure:** Contact development team with error logs

---

**Document Version:** 1.0 | **Last Updated:** 2026-11-15

