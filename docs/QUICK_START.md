# RoadWatch Traffic MVP - Quick Reference Card

## 🚀 START SERVER
```powershell
cd C:\Users\avina\Downloads\avinash-repo\v11\Traffic
.\start-windows.ps1
```

## 📱 CITIZEN WORKFLOW
1. Open http://127.0.0.1:8000/citizen-login.html
2. Click "Report Violation"
3. Fill form:
   - Violation Type: "No Helmet" or "Overspeeding"
   - Vehicle Number: "DL-01-AB-1234" (optional but test it)
   - Location: "Test Location"
   - Image: Upload JPG/PNG file
4. Click "Submit Report"
5. Go to "View My Reports" to see status
6. After officer approves, see status change and points awarded

## 👮 OFFICER WORKFLOW
1. Open http://127.0.0.1:8000/officer-login.html
2. Enter token: **demo-reviewer-token**
3. Click "Login"
4. View "Pending Reports Queue"
5. Click "Review Case" on report
6. Click "Approve" to award points
7. Status changes to "approved" (citizen will see it)

## 🧪 AUTOMATED TESTING
```bash
# Run end-to-end test
python e2e_test.py

# Run unit tests
pytest -v
```

## ✅ VERIFICATION
- [x] Unit tests: 23/23 passing
- [x] E2E workflow: 4/4 steps passing
- [x] API endpoints: 8/8 working
- [x] Token validation: enforced
- [x] Database: persists correctly
- [x] UI: all pages ready

## 📋 FILES TO REVIEW
- **STATUS.md** - Complete status report
- **TESTING_CHECKLIST.md** - Manual testing guide
- **VERIFICATION_REPORT.txt** - Detailed verification
- **e2e_test.py** - End-to-end workflow test

## 🔑 IMPORTANT SETTINGS
- **Reviewer Token**: demo-reviewer-token
- **Citizen ID**: Set via X-Citizen-Id header (can be any string in MVP)
- **Database**: SQLite (roadwatch.db)
- **Image Storage**: /uploads/ directory
- **Port**: 8000 (http://127.0.0.1:8000)

## 📊 SAMPLE TEST DATA
```
Report ID:       fa45ef22ed4443e7
Citizen:         e2e-test-citizen
Violation:       helmet
Vehicle:         DL-26-AB-5678
Location:        test
Status:          approved
Points:          2
Created:         2026-11-04T02:02:22Z
```

## 🔗 USEFUL LINKS
- Health Check: http://127.0.0.1:8000/health
- API Docs: http://127.0.0.1:8000/docs
- Citizen Home: http://127.0.0.1:8000/citizen-home.html
- Officer Queue: http://127.0.0.1:8000/officer-queue.html

## ⚠️ COMMON ISSUES & FIXES

**Officer queue shows "Failed to load queue"**
- Make sure you entered correct token: demo-reviewer-token
- Check that server is running (test /health endpoint)

**Report status not changing**
- Browser cache? Press F5 to refresh
- Check database: reports table should show status=approved

**Image upload fails**
- Only JPG, PNG, MP4, MOV, WEBM supported
- Max size 25MB for images, 45 sec for videos

**Invalid token error**
- Token is: demo-reviewer-token (exact match, case-sensitive)
- Passed in Authorization header as: Bearer demo-reviewer-token

## 📞 SUPPORT
See TESTING_CHECKLIST.md for detailed manual testing procedures.
See VERIFICATION_REPORT.txt for complete verification details.
