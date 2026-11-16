# RoadWatch MVP - Ready for Testing

## ✓ Services Status

```
Backend API      (port 8001)  - RUNNING & LISTENING
AI Gateway       (port 9999)  - RUNNING & LISTENING
Frontend Assets               - SERVED from Backend
```

Both services are confirmed listening on their ports and ready to handle requests.

---

## How to Test Right Now

### Option 1: Interactive Test Menu (Recommended)

Open PowerShell and run:
```powershell
.\run-tests.ps1
```

This gives you an interactive menu to:
- [1] Verify all services
- [2] Test citizen signup & login
- [3] Test report submission
- [4] Test officer flow
- [5] Run full end-to-end test
- [6] Check API documentation
- [7] View service logs

### Option 2: API Documentation (Browser)

Open in browser:
```
http://127.0.0.1:8001/api/docs
```

Features:
- Interactive Swagger UI
- Try out all endpoints
- See request/response schemas
- Test authentication

### Option 3: Web Interface (Browser)

**Citizen Portal**:
```
http://127.0.0.1:8001/citizen-signup.html
```

**Officer Portal**:
```
http://127.0.0.1:8001/officer-signup.html
```

### Option 4: Manual Testing (PowerShell)

Test Backend Health:
```powershell
$response = Invoke-WebRequest 'http://127.0.0.1:8001/health'
$response.Content | ConvertFrom-Json | ConvertTo-Json
```

Test Citizen Signup:
```powershell
$body = @{
    email = 'testuser@example.com'
    full_name = 'Test User'
    citizen_id = 'TEST_CITIZEN_001'
    password = 'SecurePass123!'
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri 'http://127.0.0.1:8001/api/auth/signup' `
  -Method Post `
  -Headers @{'Content-Type'='application/json'} `
  -Body $body

$response.Content | ConvertFrom-Json | ConvertTo-Json
```

---

## Full Testing Workflow

### Phase 1: Citizen Journey

1. **Signup**
   ```
   POST /api/auth/signup
   Required: email, full_name, citizen_id, password
   Expected: 201 Created with citizen details
   ```

2. **Login**
   ```
   POST /api/auth/login
   Required: citizen_id, password
   Expected: 200 OK with JWT token
   ```

3. **Submit Report**
   ```
   POST /api/reports
   Required: Authorization header with token
   Required: violation_type, description, location, vehicle_number
   Expected: 201 Created with report_id
   ```

4. **View Your Reports**
   ```
   GET /api/reports
   Required: Authorization header with token
   Expected: 200 OK with list of reports
   ```

5. **Check Report Status**
   ```
   GET /api/reports/{report_id}
   Expected: 200 OK with report details including officer decision
   ```

### Phase 2: Officer Journey

1. **Register**
   ```
   POST /api/officer/register
   Required: officer_id, full_name, station, password
   Expected: 201 Created
   ```

2. **Login**
   ```
   POST /api/officer/login
   Required: officer_id, password
   Expected: 200 OK with JWT token
   ```

3. **View Report Queue**
   ```
   GET /api/authority/reports
   Required: Authorization header with officer token
   Expected: 200 OK with list of all pending reports
   ```

4. **View Specific Report**
   ```
   GET /api/authority/reports/{report_id}
   Expected: 200 OK with report + AI recommendation
   ```

5. **Download Evidence**
   ```
   GET /api/authority/reports/{report_id}/evidence.zip
   Expected: ZIP file with all media
   ```

6. **Submit Decision**
   ```
   POST /api/authority/reports/{report_id}/decision
   Required: decision (APPROVED/REJECTED), points_awarded, remarks
   Expected: 200 OK with updated report status
   ```

### Phase 3: AI Integration Verification

1. **Check AI Gateway Logs** (Terminal where AI Gateway runs)
   ```
   Look for: OpenAI API calls
   Should show: Assessment generation
   ```

2. **Verify Recommendation in Report**
   ```
   When officer views report, should see:
   - recommendation field (AI suggestion)
   - confidence_score (0-100)
   - recommendation_reason
   ```

---

## What Should Happen

### Success Indicators

✓ **Citizen Flow**
- Signup returns 201 with citizen_id
- Login returns 200 with JWT token
- Report submission returns 201 with report_id
- Report appears in citizen's list
- Status changes after officer decision

✓ **Officer Flow**
- Officer registration succeeds
- Officer login returns token
- Queue shows all pending reports
- Report details include AI recommendation
- Officer can submit decision
- Report status updates immediately

✓ **AI Integration**
- AI Gateway receives assessment requests
- OpenAI API is called (check logs)
- Recommendations are generated
- Recommendations appear in officer view

✓ **Database**
- Data persists across requests
- Relationships maintained (citizen→reports→decisions)
- Audit trail created (events table)

---

## Expected Response Times

| Operation | Latency | Why |
|-----------|---------|-----|
| Health check | < 100ms | Direct response |
| Signup | 100-300ms | Password hashing |
| Login | 100-300ms | Password verification |
| Submit report | 200-500ms | Database write |
| View reports | 50-100ms | Query execution |
| Officer decision | 500-1000ms | Multiple writes |
| With AI screening | 3-5 seconds | OpenAI API call |

---

## Common Test Scenarios

### Scenario 1: Simple Report & Approval

```
1. Citizen signs up
   → email: citizen1@test.com
   → citizen_id: CITIZEN_A
   → password: TestPass123!

2. Citizen logs in
   → Get: JWT token

3. Citizen submits report
   → violation_type: helmet
   → location: Test Street
   → Get: report_id (e.g., rpt_abc123)

4. Officer signs up
   → officer_id: OFFICER_A
   → password: TestPass123!

5. Officer logs in
   → Get: JWT token

6. Officer views queue
   → Should see report from CITIZEN_A

7. Officer views specific report
   → Should see AI recommendation

8. Officer submits decision
   → decision: APPROVED
   → points_awarded: 2
   → Report status → "approved"

9. Citizen checks report
   → Should see status = "approved"
   → Should see decision details
```

### Scenario 2: Media Upload & Evidence

```
1. Citizen submits report with media
   → Upload photo/video
   → Media validates (SHA-256 checksum)

2. Officer views report
   → Can see media metadata

3. Officer downloads evidence
   → Gets ZIP with all media

4. Verification
   → Media is accessible
   → Format is correct
   → Checksum valid
```

### Scenario 3: Multiple Reports & Batching

```
1. Multiple citizens submit different reports
2. Officer views queue (should see all)
3. Officer can process reports independently
4. Each report tracked separately
5. Decisions don't affect other reports
```

---

## Troubleshooting

### Service Not Responding

Check if ports are listening:
```powershell
netstat -an | Select-String "8001|9999"
```

Or:
```powershell
Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue
```

### 401 Unauthorized

- Ensure Bearer token is in Authorization header
- Format: `Authorization: Bearer <token>`
- Token may have expired - login again

### 404 Not Found

- Check URL spelling
- Check report_id is correct
- Check citizen/officer exists

### 500 Internal Server Error

Check backend logs (Terminal 1):
```
Look for: Traceback or ERROR messages
Common causes:
  - Missing environment variable
  - Database error
  - Invalid request format
```

### AI Gateway Issues

Check AI Gateway logs (Terminal 2):
```
Look for: OpenAI API errors
Common causes:
  - Invalid API key
  - Rate limiting
  - Network connectivity
```

---

## Performance Observation

Run multiple operations and observe:
- Response times
- Database query performance
- AI screening latency
- Error handling

Document findings for optimization in Phase 2.

---

## Files You Have

| File | Purpose |
|------|---------|
| `run-tests.ps1` | Interactive test runner |
| `TESTING-GUIDE.md` | Detailed test procedures |
| `QUICK-START.md` | Fast startup guide |
| `DEPLOYMENT-STATUS.md` | Complete status report |
| `SERVICES-ARCHITECTURE.md` | Design documentation |

---

## Next Steps After Testing

1. **All tests pass?**
   → Document which features work
   → Plan Phase 2 improvements

2. **Found issues?**
   → Reproduce consistently
   → Review error logs
   → File GitHub issues with details

3. **Performance concerns?**
   → Collect timing data
   → Identify bottlenecks
   → Plan optimizations

4. **Ready for more testing?**
   → Load testing with multiple users
   → Stress testing with large files
   → Security testing with edge cases

---

## Start Testing Now!

Open PowerShell and run:
```powershell
.\run-tests.ps1
```

Or open browser:
```
http://127.0.0.1:8001/api/docs
```

Both services are listening and ready! 🚀

