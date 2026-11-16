# Officer/Reviewer Demo Guide 🚨

## Quick Start

### What is the Reviewer Token?

The **Reviewer Token** is a shared security code that officers/reviewers must provide when registering. It acts as a **gatekeeper** to prevent unauthorized people from signing up as officers.

In the MVP (demo mode), the default token is:
```
demo-reviewer-token
```

### Why Do We Need It?

- Only authorized people can become reviewers/officers
- Prevents random people from registering as officers
- Simple MVP solution (production would use OIDC/OAuth)

---

## How to Access the Officer/Reviewer Portal

### Step 1: Navigate to Officer Signup
```
http://127.0.0.1:3002/signup
```

### Step 2: Fill the Registration Form

| Field | Example Value |
|-------|---|
| **Full Name** | Jane Smith |
| **Email** | jane.smith@example.com |
| **Password** | MyPassword123 |
| **Reviewer Token** | `demo-reviewer-token` |

### Step 3: Click Register

You're now registered as an officer! ✅

### Step 4: Login

```
http://127.0.0.1:3002/
```

Use:
- **Email**: jane.smith@example.com
- **Password**: MyPassword123

---

## What Can Officers Do?

### 1. View Review Queue
- Dashboard shows all pending reports awaiting review
- See violation type, submitter, and submission date

### 2. Review Evidence
- Click on any report to view details
- See uploaded photo/video evidence
- Read violation description

### 3. Make Decisions
- **Approve**: Accept the violation, award points
- **Reject**: Dismiss without points
- Points range: 0-10 (see POINTS_BY_VIOLATION)

### 4. See Full Audit Trail
- All decisions are logged
- Timestamp of review
- Reason for decision

---

## Demo Workflow (Officer Side)

### Scenario: Officer Reviews a Citizen's Report

#### Step 1: Access Review Queue
1. Login to: http://127.0.0.1:3002/
2. Click "Review Queue" or go to: `/queue`
3. See list of pending reports from citizens

#### Step 2: Click a Report to Review
1. Click on any report in the queue
2. View the evidence (photo/video)
3. Read violation details

#### Step 3: Make a Decision
1. Click **"Approve"** or **"Reject"**
2. If approving, enter points (e.g., 5)
3. Add any notes (optional)
4. Click confirm

#### Step 4: Citizen Sees Decision
- Citizen logs back in to their portal
- Sees your decision on their report
- Sees the points you awarded

---

## Default Demo Token

```
demo-reviewer-token
```

**Where it comes from:**
- Environment variable: `ROADWATCH_REVIEWER_TOKEN`
- File: `.env` (if exists)
- Default: `demo-reviewer-token` (hardcoded in MVP)

### Change the Token (Optional)

To use a different reviewer token, set the environment variable:

**Windows (PowerShell):**
```powershell
$env:ROADWATCH_REVIEWER_TOKEN = "my-custom-token"
START-ALL.bat
```

**macOS/Linux (Bash):**
```bash
export ROADWATCH_REVIEWER_TOKEN="my-custom-token"
./START-ALL.sh
```

Or create a `.env` file:
```env
ROADWATCH_REVIEWER_TOKEN=my-custom-token
```

---

## API Endpoints (Officer/Reviewer)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/officer/register` | Register as officer |
| `POST` | `/api/officer/login` | Login to officer account |
| `GET` | `/api/officer/reports` | Get review queue |
| `GET` | `/api/officer/reports/{id}` | Get report details |
| `POST` | `/api/officer/reports/{id}/decision` | Submit decision |

### Example: Get Review Queue

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:9003/api/officer/reports
```

---

## Testing Multiple Officers

You can register multiple officers with different names/emails but the **same reviewer token**.

### Officer 1
- Name: Jane Smith
- Email: jane@example.com
- Token: `demo-reviewer-token`

### Officer 2
- Name: John Doe
- Email: john@example.com
- Token: `demo-reviewer-token`

Both can login independently and review reports.

---

## Troubleshooting

### "Invalid reviewer token"
- Check you're using: `demo-reviewer-token`
- Make sure there are no extra spaces
- Verify `ROADWATCH_REVIEWER_TOKEN` environment variable is set correctly

### "Email already exists"
- Use a different email address
- Officer emails must be unique in the database
- Check database: `SELECT * FROM users WHERE role='officer'`

### "Officer portal won't load"
- Check if port 3002 is running
- Check port 9003 (Officer API) is running
- Clear browser cache and refresh

### "Can't see any reports in queue"
- Make sure citizens have submitted reports first
- Wait a few seconds for data sync
- Check database has reports in `reports` table

---

## Officer Portal Features

### Dashboard
- Total pending reports count
- Quick stats (approved, rejected)
- Search by violation type

### Review Queue
- Sortable list of reports
- Filter by status (pending, approved, rejected)
- Pagination support

### Report Detail
- Full evidence view (photos/videos)
- Violation type and description
- Citizen information (anonymized)

### Decision Making
- Approve/Reject buttons
- Points award field
- Notes field (optional)
- Confirm before submitting

### History
- See all reviewed reports
- Filter by your decisions
- Export reports (future feature)

---

## Report Statuses (From Officer Perspective)

| Status | Meaning | Action |
|--------|---------|--------|
| **pending** | Waiting for officer review | Review it |
| **approved** | Officer approved | See points awarded |
| **rejected** | Officer rejected | See rejection reason |
| **escalated** | Needs manual review | Contact admin |

---

## Points System

Officers award points based on violation type:

| Violation | Default Points | Officer Can Override |
|-----------|-----------------|---------------------|
| Speed violation | 5 | Yes (0-10) |
| Running red light | 3 | Yes (0-10) |
| Improper parking | 2 | Yes (0-10) |
| Reckless driving | 10 | Yes (0-10) |
| Other | 1 | Yes (0-10) |

---

## Hints for Testing

1. **Test as two different officers** - Verify data isolation
2. **Upload same photo twice** - Test duplicate handling
3. **Approve some, reject others** - Test all decision types
4. **Award max/min points** - Test edge cases
5. **Check audit trail** - Verify all actions logged

---

## Next Steps

1. **Start the system**:
   ```bash
   START-ALL.bat    # Windows
   ./START-ALL.sh   # macOS/Linux
   ```

2. **Register as officer**:
   - Go to: http://127.0.0.1:3002/signup
   - Use token: `demo-reviewer-token`

3. **Review reports**:
   - Have a citizen submit a report first
   - Go to: http://127.0.0.1:3002/queue
   - Review and decide

4. **Verify feedback**:
   - Switch back to citizen portal
   - Check that citizen sees your decision

---

## FAQ

**Q: Can I change the reviewer token?**
A: Yes, set `ROADWATCH_REVIEWER_TOKEN` environment variable before starting.

**Q: What if I forget the reviewer token?**
A: Check `.env` file or ask the admin. Default is `demo-reviewer-token`.

**Q: Can officers see each other's activity?**
A: Yes, all officers can see all reports and decisions (no per-officer filtering in MVP).

**Q: How long are officer sessions valid?**
A: 24 hours. After that, login again.

**Q: Can I change my password?**
A: Not in MVP. Restart your browser and login again.

**Q: Where are my decisions stored?**
A: In `roadwatch.db` in the `decisions` table.

---

## Security Notes (MVP)

⚠️ **This is demo/development mode only:**
- No real OIDC/OAuth
- Shared reviewer token (not scalable)
- No encryption on storage
- Logs include user data
- No rate limiting on API

For production, implement:
- Real OIDC/OAuth
- Per-officer authorization tokens
- Encrypted database
- Proper logging (no PII)
- Rate limiting and DDoS protection

---

## Related Documentation

- **READY-TO-TEST.md** - Full testing guide
- **SYSTEM-STATUS.md** - System architecture
- **README.md** - Project overview
- **START-HERE.md** - Navigation guide

---

**Status**: ✅ Officer/Reviewer demo ready  
**Token**: `demo-reviewer-token`  
**Portal**: http://127.0.0.1:3002/  
**Last Updated**: 2026-11-15
