# RoadWatch MVP - Testing Guide

## Current Status

**Services Running**:
- ✓ Backend API (port 8001)
- ✓ AI Gateway (port 9999)
- ⏳ Frontend (port 3000) - Starting...

---

## Step 1: Verify Services Are Up

```powershell
# In a new terminal, run the test script
python test-services-simple.py
```

Expected output:
```
[PASS]   Backend API
[PASS]   AI Gateway
[SUCCESS] All services are running and responsive!
```

---

## Step 2: Access API Documentation

Open in your browser:
```
http://127.0.0.1:8001/api/docs
```

This shows all available endpoints with:
- Request schemas
- Response schemas
- Try it out functionality
- Authentication requirements

---

## Step 3: Test Citizen Flow

### 3a. Citizen Signup

Use Swagger UI at `/api/docs` or run:

```powershell
$body = @{
    email = "citizen@example.com"
    full_name = "John Doe"
    citizen_id = "CITIZEN_001"
    password = "SecurePass123!"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/auth/signup" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | ConvertFrom-Json | ConvertTo-Json
```

Expected response (201 Created):
```json
{
  "citizen_id": "CITIZEN_001",
  "email": "citizen@example.com",
  "full_name": "John Doe",
  "created_at": "2026-11-13T22:00:00Z"
}
```

### 3b. Citizen Login

```powershell
$body = @{
    citizen_id = "CITIZEN_001"
    password = "SecurePass123!"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/auth/login" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body

$token = ($response.Content | ConvertFrom-Json).token
Write-Host "Token: $token"
```

### 3c. Submit a Report

```powershell
$body = @{
    violation_type = "helmet"
    description = "Rider without helmet on highway"
    location = "Main Street, Downtown"
    vehicle_number = "ABC123"
} | ConvertTo-Json

$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/reports" `
  -Method Post `
  -Headers $headers `
  -Body $body

$reportId = ($response.Content | ConvertFrom-Json).report_id
Write-Host "Report created: $reportId"
$response.Content | ConvertFrom-Json | ConvertTo-Json
```

Expected response (201 Created):
```json
{
  "report_id": "rpt_abc123xyz",
  "citizen_id": "CITIZEN_001",
  "violation_type": "helmet",
  "status": "submitted",
  "points": 0,
  "created_at": "2026-11-13T22:00:00Z"
}
```

### 3d. View Your Reports

```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/reports" `
  -Headers $headers | ConvertFrom-Json | ConvertTo-Json
```

### 3e. View Specific Report

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/reports/$reportId" `
  -Headers $headers | ConvertFrom-Json | ConvertTo-Json
```

---

## Step 4: Test Officer Flow

### 4a. Officer Signup

```powershell
$body = @{
    officer_id = "OFFICER_001"
    full_name = "Jane Smith"
    station = "Downtown Station"
    password = "SecurePass123!"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/officer/register" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body | ConvertFrom-Json | ConvertTo-Json
```

### 4b. Officer Login

```powershell
$body = @{
    officer_id = "OFFICER_001"
    password = "SecurePass123!"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/officer/login" `
  -Method Post `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body

$officerToken = ($response.Content | ConvertFrom-Json).token
Write-Host "Officer Token: $officerToken"
```

### 4c. View Reports Queue

```powershell
$headers = @{
    "Authorization" = "Bearer $officerToken"
}

Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/authority/reports" `
  -Headers $headers | ConvertFrom-Json | ConvertTo-Json
```

Expected response: List of all submitted reports waiting for review

### 4d. View Specific Report (with AI Recommendation)

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/authority/reports/$reportId" `
  -Headers $headers | ConvertFrom-Json | ConvertTo-Json
```

**Look for**:
- `recommendation` field (AI-generated suggestion)
- `recommendation_source` (should be "ai_gateway")
- `confidence_score` (0-100)

### 4e. Download Report Evidence

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/authority/reports/$reportId/evidence.zip" `
  -Headers $headers `
  -OutFile "evidence_$reportId.zip"

Write-Host "Downloaded: evidence_$reportId.zip"
```

### 4f. Submit Officer Decision

```powershell
$body = @{
    decision = "APPROVED"
    points_awarded = 2
    remarks = "Violation confirmed - no helmet observed"
    follow_up_required = $false
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/authority/reports/$reportId/decision" `
  -Method Post `
  -Headers $headers `
  -Body $body | ConvertFrom-Json | ConvertTo-Json
```

Expected response (200 OK):
```json
{
  "report_id": "rpt_abc123xyz",
  "decision": "APPROVED",
  "points_awarded": 2,
  "decided_by": "OFFICER_001",
  "decision_date": "2026-11-13T22:00:00Z",
  "status": "approved"
}
```

---

## Step 5: Test Media Upload

### 5a. Upload Media with Report

You can upload media when creating a report using the Swagger UI or:

```powershell
# First, prepare a form with file
$FilePath = "C:\path\to\photo.jpg"

# Using Invoke-WebRequest with form data
$headers = @{
    "Authorization" = "Bearer $token"
}

# Upload media
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/media/upload" `
  -Method Post `
  -Headers $headers `
  -Form @{
      file = Get-Item -Path $FilePath
  }

$mediaId = ($response.Content | ConvertFrom-Json).media_id
Write-Host "Media uploaded: $mediaId"
```

### 5b. Download Media

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8001/api/media/$mediaId/photo.jpg" `
  -Headers $headers `
  -OutFile "downloaded_photo.jpg"
```

---

## Step 6: Test AI Integration

The AI Gateway is called automatically when officers review reports.

### Check AI Processing in Logs

**Backend logs** (Terminal 1):
```
Look for: POST http://127.0.0.1:9999/assess
Response: assessment with recommendation
```

**AI Gateway logs** (Terminal 2):
```
Look for: OpenAI API call
Response: Policy validation
```

### Manual AI Test

```powershell
$body = @{
    image_url = "http://example.com/test-violation.jpg"
    violation_type = "helmet"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:9999/assess" `
  -Method Post `
  -Headers @{
      "Authorization" = "Bearer OqROzN00FM7z7D1_OFlt9nKKsMpInqN0pUuq3PyEofQ"
      "Content-Type" = "application/json"
  } `
  -Body $body | ConvertFrom-Json | ConvertTo-Json
```

---

## Step 7: Test Frontend (When Ready)

Once frontend starts on port 3000:

```
http://127.0.0.1:3000/citizen
http://127.0.0.1:3000/authority
```

Features to test:
- [ ] Citizen login with CITIZEN_001 / SecurePass123!
- [ ] Submit report with description
- [ ] Upload photo/video
- [ ] View report status
- [ ] Officer login with OFFICER_001 / SecurePass123!
- [ ] View pending reports
- [ ] See AI recommendation
- [ ] Approve/Reject report
- [ ] View decision confirmation

---

## Testing Checklist

### Citizen Flow
- [ ] Signup works
- [ ] Login works
- [ ] Submit report works
- [ ] View reports works
- [ ] Upload media works
- [ ] Track status works
- [ ] Receive decision works

### Officer Flow
- [ ] Signup works
- [ ] Login works
- [ ] View reports queue works
- [ ] See report details works
- [ ] See AI recommendation works
- [ ] Download evidence works
- [ ] Submit decision works
- [ ] See confirmation works

### AI Integration
- [ ] AI Gateway responds
- [ ] OpenAI API calls work
- [ ] Recommendations generated
- [ ] Policy validation passes
- [ ] Error handling works

### Database
- [ ] Data persists
- [ ] Relationships maintained
- [ ] Audit trail recorded
- [ ] No orphaned records

### API
- [ ] All endpoints respond
- [ ] Auth required where needed
- [ ] Validation working
- [ ] Error messages helpful
- [ ] Status codes correct

---

## Quick Commands Summary

```powershell
# Test all services
python test-services-simple.py

# Open API docs
Start-Process "http://127.0.0.1:8001/api/docs"

# Check backend logs (in Terminal 1)
# Check AI gateway logs (in Terminal 2)
# Check frontend logs (in Terminal 3)

# Kill a service (if stuck)
Get-Process python | Where-Object {$_.Id -eq <PID>} | Stop-Process -Force
```

---

## Expected Test Results

### Successful Citizen Flow
```
1. Signup → 201 Created
2. Login → 200 OK, token returned
3. Submit report → 201 Created, report_id returned
4. View reports → 200 OK, list of reports
5. View specific report → 200 OK, report details
6. Status after officer decision → "approved" or "rejected"
```

### Successful Officer Flow
```
1. Signup → 201 Created
2. Login → 200 OK, token returned
3. View queue → 200 OK, list of pending reports
4. View specific report → 200 OK, with AI recommendation
5. Submit decision → 200 OK, decision confirmed
6. Status changes to "approved" or "rejected"
```

### Successful AI Integration
```
1. Officer views report
2. AI recommendation appears in response
3. Recommendation includes: violation_type, confidence, reason
4. Officer can approve, reject, or override
5. Decision recorded in database
```

---

## Troubleshooting During Testing

### 401 Unauthorized
- Check token is included in Authorization header
- Format: `Authorization: Bearer <token>`
- Token expires after session, login again

### 404 Not Found
- Check URL is correct
- Check resource ID is correct (e.g., report_id)
- Check citizen/officer exists

### 500 Internal Server Error
- Check backend logs (Terminal 1)
- Check AI gateway logs (Terminal 2)
- Common issues: missing environment variables, database errors

### Slow Response
- AI integration takes 3-5 seconds (normal - OpenAI API)
- Check internet connection
- Check OpenAI API key is valid

### Frontend Won't Load
- Check frontend is running (Terminal 3)
- Clear browser cache: Ctrl+Shift+Delete
- Check console for errors (F12)

---

## Performance Expectations

| Operation | Latency | Notes |
|-----------|---------|-------|
| Health check | < 100ms | Direct response |
| Login | 100-300ms | Password hashing |
| Submit report | 200-500ms | Database write |
| List reports | 50-150ms | Database query |
| Officer review (with AI) | 3-5 seconds | OpenAI API call |
| Media download | < 500ms | File I/O |

---

## Next Steps After Testing

1. **All tests pass?** → Document any issues
2. **Performance OK?** → Ready for integration testing
3. **Found bugs?** → Fix and re-test
4. **Need features?** → Plan next sprint
5. **Ready for deployment?** → Create Docker images

---

**Good luck with testing!**
When done, let me know what works, what doesn't, and what you'd like to improve.

