# Manual Browser Testing Checklist

## 1. CITIZEN UPLOAD FLOW
- [ ] Open http://127.0.0.1:8000/citizen-home.html
- [ ] Click "Report Violation"
- [ ] Fill form:
  - [ ] Violation Type: Select "No Helmet" or "Overspeeding"
  - [ ] Vehicle Number: "DL-01-AB-1234" (optional but test it)
  - [ ] Image: Upload a test image
- [ ] Click "Submit Report"
- [ ] Verify success message shows Report ID
- [ ] Verify Vehicle Number appears in submitted report list

## 2. OFFICER REVIEW FLOW
- [ ] Open http://127.0.0.1:8000/officer-login.html
- [ ] Enter token: "demo-reviewer-token"
- [ ] Click "Login"
- [ ] Verify you see "Pending Reports Queue"
- [ ] Verify your submitted report appears in the queue with:
  - [ ] Report ID
  - [ ] Violation type
  - [ ] Citizen who submitted it
  - [ ] Created timestamp
- [ ] Click "Review Case" on the report
- [ ] Verify you can see:
  - [ ] Violation type
  - [ ] Citizen who submitted it
  - [ ] Vehicle number (if submitted)
  - [ ] Image/evidence
  - [ ] Action buttons (Approve, Reject, Request Info)
- [ ] Click "Approve" button
- [ ] Verify confirmation message
- [ ] Verify report disappears from queue

## 3. CITIZEN VIEW UPDATED REPORT
- [ ] Go to http://127.0.0.1:8000/citizen-home.html
- [ ] Click "View My Reports"
- [ ] Find your report in the list
- [ ] Verify status changed to "approved"
- [ ] Verify provisional points awarded:
  - [ ] 2 points for helmet violation
  - [ ] 5 points for overspeeding violation
- [ ] Click "View Details" to see full timeline
- [ ] Verify timeline shows:
  - [ ] Initial submission by citizen
  - [ ] Officer approval decision

## 4. ERROR CASES TO TEST
- [ ] Wrong token login: Try invalid token (should show error)
- [ ] No token access: Try accessing officer queue without logging in (should fail)
- [ ] Invalid date: Submit report with invalid date (should reject)
- [ ] Non-image file: Try uploading .txt or .pdf (should reject)
- [ ] Duplicate image: Upload same image twice (should show duplicate message)
- [ ] Missing fields: Try submitting without violation type (should require field)

## 5. FEATURES TO VERIFY
- [ ] Vehicle number field persists in database
- [ ] Vehicle number displays in report table and details
- [ ] Provisional points calculation works correctly
- [ ] Officer token validation enforces proper auth
- [ ] Demo mode messaging is removed
- [ ] Queue auto-refreshes every 30 seconds
- [ ] No images are cached (each upload is fresh)

## API ENDPOINTS TESTED
- ✓ POST /api/media/upload - Upload image
- ✓ POST /api/reports - Submit report
- ✓ GET /api/authority/reports - Get officer queue
- ✓ GET /api/reports/{id} - Get report details
- ✓ POST /api/authority/reports/{id}/decision - Officer approves/rejects
- ✓ GET /api/authority/reports/{id}/evidence.zip - Download evidence

## SUCCESS CRITERIA (ALL MUST PASS)
- ✓ Citizen can submit report with image and vehicle number
- ✓ Officer can view pending reports in queue
- ✓ Officer can approve/reject/request-info on reports
- ✓ Citizen sees status and points update after officer decision
- ✓ Token validation rejects invalid credentials
- ✓ Vehicle number persists and displays correctly
- ✓ Provisional points awarded on approval
- ✓ Timeline shows decision history
