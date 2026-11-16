# Regression Prevention Guide

**Problem**: "We fix one thing and break something that was working"

**Solution**: Follow this guide to prevent regressions

---

## The Core Issue

When changes are made to one part of the app, they can accidentally break other parts:

```
1. You fix auth issue in citizen-reports.html
2. Works great!
3. Later, you need to fix something in citizen-dashboard.html
4. You copy code from citizen-reports.html
5. But you accidentally copy OLD code that has the bug
6. Now citizen-dashboard.html is broken again
7. User complains: "Why is it broken again?"
```

---

## Prevention Strategy

### Step 1: Read FIXES-LOG.md BEFORE Working on Auth

**When**: About to work on login, logout, auth headers, redirects, localStorage

**What to do**:
```
1. Open FIXES-LOG.md
2. Read "How to Prevent Future Regressions"
3. Read "Common Mistakes & How to Avoid Them"
4. Read the relevant Fix section
5. THEN write your code
```

**Why**: Prevents copy-pasting broken patterns

---

### Step 2: Understand the Pattern

**Authentication pages must follow this pattern:**

```javascript
// Step 1: Setup script includes (loads auth.js first)
<script src="/static/js/utils.js"></script>
<script src="/static/js/auth.js"></script>
<script src="/static/js/api.js"></script>
<script src="/static/js/common.js"></script>
<script>

// Step 2: CHECK AUTH SYNCHRONOUSLY (no delays!)
if (!AUTH.isCitizen()) {  // or !AUTH.isReviewer()
  window.location.href = '/citizen-login.html';  // or /officer-login.html
}

// Step 3: Setup logout handler
document.getElementById('logout-link').addEventListener('click', (e) => {
  e.preventDefault();
  AUTH.clearAuth();
  window.location.href = '/citizen-login.html';
});

// Step 4: Define your data loading function
async function loadData() {
  // ... your code here
}

// Step 5: Call your function (only after auth passes)
loadData();

</script>
```

**Key Points**:
- ✓ Auth check is synchronous (no setTimeout)
- ✓ Auth check comes FIRST (before any other code)
- ✓ Data loading is CONDITIONAL (only if auth passes)
- ✓ Logout clears BOTH tokens

---

### Step 3: Verify Before Committing

**Checklist before git commit:**

- [ ] Login as citizen → redirects to citizen page (not login)
- [ ] Login as officer → redirects to officer page (not login)
- [ ] Access protected page without auth → redirects to login
- [ ] Logout as citizen → redirects to citizen-login.html
- [ ] Logout as officer → redirects to officer-login.html
- [ ] Check browser console for JavaScript errors
- [ ] Check network tab for 401/403 responses
- [ ] Verify localStorage has correct keys (`citizen_id` or `reviewer_token`)

**If any of these fail**:
- [ ] Don't commit yet
- [ ] Read FIXES-LOG.md troubleshooting section
- [ ] Fix the issue
- [ ] Re-test all items above
- [ ] Then commit

---

### Step 4: Document Your Change

**In your git commit message:**

```
[AUTH FIX] Fix login redirect issue in citizen-dashboard.html

Auth check was delayed 100ms, causing race condition where API calls
would fail before auth check completed. Removed setTimeout and made
auth check synchronous.

Auth pattern:
1. Check if authenticated (synchronous)
2. If not, redirect to login
3. If yes, continue with page setup and data loading

Verified: Login -> Reports flow works correctly. No console errors.

Related: See FIXES-LOG.md for complete auth documentation.
```

---

### Step 5: Add Comments to Your Code

**When fixing auth issues, add explanatory comments:**

```javascript
// CRITICAL FIX: Auth check MUST be synchronous and happen FIRST
// This prevents race condition where API calls happen before auth validation
if (!AUTH.isCitizen()) {
  window.location.href = '/citizen-login.html';
}

// Now safe to load data - we know user is authenticated
loadData();
```

**Why**: Explains to future developers WHY it's written this way

---

## Common Patterns That Cause Regressions

### ❌ Pattern 1: Delayed Auth Check

```javascript
setTimeout(() => {
  if (!AUTH.isCitizen()) redirect();
}, 100);

loadData();  // Problem: runs before auth check!
```

**Fix**: Remove setTimeout
```javascript
if (!AUTH.isCitizen()) redirect();
loadData();  // Now only runs if auth passes
```

---

### ❌ Pattern 2: Copy-Paste Without Understanding

```javascript
// You copy this from one file to another:
if (!AUTH.isCitizen()) window.location.href = '/citizen-login.html';

// But the original file might have had this bug in it:
setTimeout(() => {
  if (!AUTH.isCitizen()) window.location.href = '/citizen-login.html';
}, 100);
```

**Fix**: Read FIXES-LOG.md to understand the correct pattern

---

### ❌ Pattern 3: Forgetting Logout Cleanup

```javascript
function logout() {
  localStorage.removeItem('citizen_id');
  // Oops! Forgot to clear reviewer_token
  window.location.href = '/login.html';
}

// Now if officer logs out, but reviewer_token remains, they have partial access
```

**Fix**: Clear BOTH tokens
```javascript
function logout() {
  localStorage.removeItem('citizen_id');
  localStorage.removeItem('reviewer_token');
  window.location.href = '/login.html';
}

// Or use the helper:
AUTH.clearAuth();  // Clears both
```

---

### ❌ Pattern 4: API Calls Without Auth Headers

```javascript
async function getReports() {
  const response = await fetch('/api/reports');
  // Missing auth header - backend returns 401!
}
```

**Fix**: Include auth header
```javascript
async function getReports() {
  const citizenId = localStorage.getItem('citizen_id');
  const headers = citizenId ? { 'X-Citizen-Id': citizenId } : {};
  
  const response = await fetch('/api/reports', { headers });
  // Now backend knows who's making the request
}

// Or use the wrapper:
const result = await API.getReports();  // Automatically adds headers
```

---

## Reference Documents

### Quick Reference
1. **LOGIN-FIX.md** - What broke and how to fix it
2. **FIXES-LOG.md** - Complete technical reference
3. **This document** - How to prevent regressions

### When to Read Each

| Situation | Read This |
|-----------|-----------|
| "Why am I getting redirected to login?" | LOGIN-FIX.md |
| "I need to understand auth patterns" | FIXES-LOG.md Fix #1-5 |
| "How do I prevent this from breaking again?" | This document |
| "What auth headers should I use?" | FIXES-LOG.md Fix #3 |
| "Testing fails - what do I check?" | FIXES-LOG.md Testing Checklist |

---

## Regression Prevention Checklist

**Before working on auth/login code:**

- [ ] Read FIXES-LOG.md sections on the problem
- [ ] Understand WHY it was broken
- [ ] Understand HOW it was fixed
- [ ] Understand the CORRECT pattern
- [ ] Find an example in the code that's already correct
- [ ] Copy from the CORRECT version

**While writing code:**

- [ ] Auth check is synchronous (no setTimeout)
- [ ] Auth check happens FIRST
- [ ] Data loading is CONDITIONAL on auth passing
- [ ] Both tokens are cleared on logout
- [ ] Auth headers are included in API calls
- [ ] Comments explain WHY not just WHAT

**After writing code:**

- [ ] Run full login test (citizen and officer)
- [ ] Check browser console for errors
- [ ] Check network tab for auth headers
- [ ] Verify localStorage has correct keys
- [ ] Test logout functionality
- [ ] Document what you changed and why in git commit

**Before committing:**

- [ ] All tests pass
- [ ] No console errors
- [ ] Auth flow works end-to-end
- [ ] Commit message references FIXES-LOG.md
- [ ] Code has explanatory comments

---

## Escalation Path

### If a regression appears:

1. **Check FIXES-LOG.md** first (60% of time this will solve it)
2. **Check browser DevTools**:
   - Open DevTools (F12)
   - Go to Application tab
   - Check localStorage for auth keys
   - Go to Console tab - any errors?
   - Go to Network tab - check response codes
3. **Check the patterns in this guide** - which one did you violate?
4. **Compare with working file** - find a page that has the same auth flow working, compare code
5. **If still stuck** - Document:
   - What you changed
   - What broke
   - What you expected
   - Share both with team

---

## Example: Fixing a Regression

### Scenario: New page has broken login

1. **Symptom**: User logs in but gets redirected to login page
2. **First step**: Read LOGIN-FIX.md
3. **Second step**: Check the auth pattern in the HTML file
4. **Find the problem**:
   ```javascript
   setTimeout(() => {  // <-- THIS IS THE PROBLEM!
     if (!AUTH.isCitizen()) redirect();
   }, 100);
   loadData();  // Runs before auth check!
   ```
5. **Apply the fix**:
   ```javascript
   if (!AUTH.isCitizen()) {  // Remove setTimeout
     window.location.href = '/citizen-login.html';
   } else {
     loadData();  // Only if auth passes
   }
   ```
6. **Test**: Login flow now works
7. **Document**: Add comment explaining the fix
8. **Commit**: Reference this guide in commit message

---

## The Golden Rule

> **Any page that requires authentication must check auth FIRST, SYNCHRONOUSLY, BEFORE doing anything else.**

If you follow this rule, you won't have login redirects.

---

**Version**: 1.0  
**Last Updated**: 2026-11-13  
**Status**: ACTIVE  

