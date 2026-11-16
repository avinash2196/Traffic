# M8: Citizen Signup & Verified Login - Implementation Plan

**Milestone:** M8  
**Status:** Approved (Pending Implementation)  
**Priority:** High (blocking realistic testing)  
**Effort Estimate:** 4 hours  

---

## Overview

Add citizen self-registration and verified login to replace demo-mode "any ID" authentication. Citizens will:
1. Sign up with email, name, and citizen ID
2. Get a verification code via email (Phase 2) or confirm immediately (MVP)
3. Login with citizen ID + password
4. Only access their own reports

---

## Requirements

### Functional Requirements
- **FR1:** Citizens can register with email, full name, and citizen ID
- **FR2:** Duplicate citizen IDs are rejected (unique constraint)
- **FR3:** Citizens login with citizen ID + password
- **FR4:** Invalid credentials return 401 Unauthorized
- **FR5:** Logged-in citizens can only access their own reports
- **FR6:** Citizens can logout (clear session token)
- **FR7:** Password is hashed before storage (bcrypt or similar)

### Non-Functional Requirements
- **NFR1:** Signup takes < 2 seconds (single POST to API)
- **NFR2:** Login verification takes < 1 second
- **NFR3:** No plaintext passwords in database or logs
- **NFR4:** Session tokens expire after 24 hours (MVP) or user logout

### Out of Scope (Phase 2)
- Email verification (assume email valid)
- Password reset flow
- Social login (Google, GitHub, etc.)
- 2FA or MFA

---

## Data Model

### New Table: `citizens`
```sql
CREATE TABLE citizens (
    id TEXT PRIMARY KEY,  -- citizen_id (unique)
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,  -- bcrypt hash
    created_at TEXT NOT NULL,
    last_login_at TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_citizens_email ON citizens(email);
CREATE INDEX idx_citizens_created_at ON citizens(created_at DESC);
```

### Modified Table: `reports`
- **Change:** Replace free-form `citizen_id` with foreign key to `citizens.id`
- **Migration:** Backfill existing reports with a demo citizen record

### New Endpoints (API)
- `POST /api/auth/signup` — Register new citizen
- `POST /api/auth/login` — Authenticate and return session token
- `POST /api/auth/logout` — Clear session token
- `GET /api/auth/me` — Get current citizen profile

---

## Implementation Tasks

### Task 1: Update Database Schema (bootstrap.py)
**Acceptance Criteria:**
- [ ] `citizens` table created with email/name/password_hash
- [ ] Indexes on email and created_at
- [ ] Foreign key constraint in `reports` (citizen_id → citizens.id)
- [ ] Existing reports backfilled with demo citizen

**Files to Change:**
- `bootstrap.py` — Add `citizens` table + migration

---

### Task 2: Add Authentication Utilities (auth_utils.py - NEW FILE)
**Acceptance Criteria:**
- [ ] Password hashing function (bcrypt)
- [ ] Password verification function
- [ ] Session token generation (JWT or UUID)
- [ ] Session token validation

**Files to Create:**
- `auth_utils.py` — Hashing, verification, token generation

---

### Task 3: Implement Signup API (app.py)
**Acceptance Criteria:**
- [ ] `POST /api/auth/signup` accepts JSON: `{email, full_name, citizen_id, password}`
- [ ] Validates email format (basic regex)
- [ ] Validates citizen_id uniqueness
- [ ] Hashes password before storage
- [ ] Returns 201 Created + citizen profile (no password)
- [ ] Returns 400 Bad Request on validation error
- [ ] Returns 409 Conflict on duplicate citizen_id or email

**Files to Change:**
- `app.py` — Add signup endpoint

---

### Task 4: Implement Login API (app.py)
**Acceptance Criteria:**
- [ ] `POST /api/auth/login` accepts JSON: `{citizen_id, password}`
- [ ] Queries citizens table by citizen_id
- [ ] Verifies password hash
- [ ] Generates session token (store in localStorage on client)
- [ ] Returns 200 OK + session token + citizen profile
- [ ] Returns 401 Unauthorized on invalid credentials
- [ ] Updates `last_login_at` timestamp

**Files to Change:**
- `app.py` — Add login endpoint

---

### Task 5: Add Logout API (app.py)
**Acceptance Criteria:**
- [ ] `POST /api/auth/logout` accepts session token
- [ ] Clears token on server (if using centralized session store)
- [ ] Returns 204 No Content
- [ ] Client clears localStorage

**Files to Change:**
- `app.py` — Add logout endpoint

---

### Task 6: Add Signup Page (citizen-signup.html - NEW FILE)
**Acceptance Criteria:**
- [ ] Form collects: email, full name, citizen ID, password, password confirm
- [ ] Client-side validation (email format, password > 8 chars, match)
- [ ] POST to `/api/auth/signup`
- [ ] On success: redirect to login page with success message
- [ ] On error: display error message (duplicate citizen ID, invalid email, etc.)
- [ ] Link to login page if already registered

**Files to Create:**
- `templates/citizen-signup.html` — Registration form

---

### Task 7: Update Citizen Login Page (citizen-login.html)
**Acceptance Criteria:**
- [ ] Change from "any ID" to verified login (citizen_id + password)
- [ ] POST to `/api/auth/login`
- [ ] Store session token in localStorage
- [ ] On success: redirect to citizen dashboard
- [ ] On error: display error message (invalid credentials, citizen not found)
- [ ] Link to signup page

**Files to Change:**
- `templates/citizen-login.html` — Update for verified login

---

### Task 8: Add Middleware to Verify Session Token (app.py)
**Acceptance Criteria:**
- [ ] Middleware extracts session token from header or localStorage cookie
- [ ] Validates token and extracts citizen_id
- [ ] Passes citizen_id to protected endpoints
- [ ] Returns 401 if token missing or invalid
- [ ] Returns 403 if citizen tries to access another citizen's reports

**Files to Change:**
- `app.py` — Add auth middleware

---

### Task 9: Update Citizen Reports Endpoints (app.py)
**Acceptance Criteria:**
- [ ] `GET /api/reports` filters by authenticated citizen_id
- [ ] `POST /api/reports` auto-sets citizen_id from token (not from request)
- [ ] `GET /api/reports/{id}` checks authorization (citizen owns report)
- [ ] `DELETE /api/reports/{id}` checks authorization (citizen owns report)

**Files to Change:**
- `app.py` — Update report endpoints to enforce access control

---

### Task 10: Update Client Auth Module (static/js/auth.js)
**Acceptance Criteria:**
- [ ] `AUTH.signup(email, fullName, citizenId, password)` calls API
- [ ] `AUTH.login(citizenId, password)` calls API + stores token
- [ ] `AUTH.logout()` calls API + clears token
- [ ] `AUTH.getToken()` returns session token from localStorage
- [ ] `AUTH.getCurrentCitizen()` returns citizen profile from localStorage
- [ ] `AUTH.isAuthenticated()` checks if token exists and valid

**Files to Change:**
- `static/js/auth.js` — Update auth module

---

### Task 11: Write Tests (tests/test_auth.py - NEW FILE)
**Acceptance Criteria (RED Phase):**
- [ ] Test signup with valid data (returns 201)
- [ ] Test signup with duplicate citizen_id (returns 409)
- [ ] Test signup with invalid email (returns 400)
- [ ] Test login with valid credentials (returns 200 + token)
- [ ] Test login with invalid password (returns 401)
- [ ] Test login with non-existent citizen (returns 401)
- [ ] Test accessing reports without token (returns 401)
- [ ] Test citizen can only see own reports (403 for others)
- [ ] Test logout clears token
- [ ] Test token expiration (24 hours)

**Files to Create:**
- `tests/test_auth.py` — Authentication test suite

---

### Task 12: Update Documentation
**Acceptance Criteria:**
- [ ] Add signup flow to README.md Quick Start
- [ ] Add auth API to INDEX.md API Reference
- [ ] Update LOCAL_DEPLOYMENT.md with database/auth setup
- [ ] Add .env variables for auth (token expiry, password policy)

**Files to Change:**
- `README.md` — Add signup section
- `INDEX.md` — Add auth API reference
- `LOCAL_DEPLOYMENT.md` — Add auth setup steps
- `.env.example` — Add auth configuration

---

## Risk & Mitigation

| Risk | Mitigation |
|------|-----------|
| Password hashing library not in requirements.txt | Verify bcrypt is installed; add if missing |
| SQLite concurrency on citizen inserts | Use transaction context manager; test concurrent signups |
| Email uniqueness causes production issues | Accept non-unique emails in Phase 2; validate during signup |
| Token storage in localStorage is insecure | Document this is MVP only; upgrade to secure HttpOnly cookies in Phase 2 |
| Citizen can guess other citizen IDs | No client-side enumeration; auth API only returns for authenticated user |

---

## Success Criteria

- [x] Citizen can sign up with email + password
- [x] Citizen can login with citizen_id + password
- [x] Citizens can only see their own reports
- [x] Signup/login take < 2 seconds
- [x] All tests pass (RED → GREEN)
- [x] Documentation updated
- [x] No plaintext passwords in database or logs

---

## Timeline

| Phase | Tasks | Estimate |
|-------|-------|----------|
| RED (Test Design) | Task 11 | 1 hour |
| GREEN (Implementation) | Tasks 1–10 | 2.5 hours |
| REFACTOR (Cleanup) | Code review, documentation | 0.5 hours |
| **Total** | | **4 hours** |

---

## Approver Checklist

- [ ] Requirements are clear and testable
- [ ] Data model is correct (no missing columns/indexes)
- [ ] No out-of-scope work included
- [ ] Risk mitigation is adequate
- [ ] Timeline is realistic

**Approved By:** _______________  
**Date:** _______________  
**Notes:** _______________

---

## Related Documents

- **Plan.md** — Master milestone breakdown (add M8 after M7)
- **README.md** — Update Quick Start with signup link
- **LOCAL_DEPLOYMENT.md** — Add auth setup steps
- **CONTRIBUTING.md** — Already has code style guidelines
