# Authentication Redirect Loop Fix - Summary

**Date:** November 14, 2026  
**Issue:** After user logs in and auth token is set in localStorage, navigating to protected pages triggered a redirect loop back to the login screen.

---

## Root Cause

The frontend pages were checking `AUTH.isCitizen()` and `AUTH.isReviewer()` **before** the JavaScript files (auth.js, api.js, common.js) had finished loading. This caused:

1. User logs in → `citizen_id` stored in localStorage
2. Page navigates to `/citizen-reports.html`
3. Scripts start loading (but not finished yet)
4. Auth check runs immediately → `AUTH` object is undefined
5. Check fails → redirects to `/citizen-login.html` (even though user is authenticated!)
6. Creates infinite loop

---

## Solution

**Pattern: `checkAuthAndLoad()` with retry logic**

```javascript
function checkAuthAndLoad() {
  // Wait for AUTH object to be fully loaded
  if (typeof AUTH === 'undefined' || !AUTH.isCitizen) {
    setTimeout(checkAuthAndLoad, 50);  // Retry in 50ms
    return;
  }
  
  // AUTH is ready, now check authentication
  if (!AUTH.isCitizen()) {
    window.location.href = '/citizen-login.html';
  } else {
    // Auth passed, initialize page
    setupPage();
  }
}

checkAuthAndLoad();  // Start check when page loads
```

---

## Files Fixed

1. **citizen-reports.html**
   - `checkAuthAndLoad()` waits for AUTH object
   - `setupPage()` initializes logout handler and loads reports
   - Auth check calls `checkAuthAndInitialize()` instead of running immediately

2. **citizen-dashboard.html**
   - Similar pattern with `checkAuthAndLoad()`
   - Defers dashboard data loading until auth passes

3. **citizen-report-detail.html**
   - Wraps detail page initialization in auth check
   - Prevents redirects while scripts load

4. **citizen-report.html**
   - Initializes form submission handlers only after auth passes

5. **officer-queue.html**
   - `checkAuthAndLoad()` ensures officer is authenticated
   - Defers queue loading until auth passes

6. **officer-detail.html**
   - Similar pattern for officer detail page
   - Wraps case initialization and decision form in auth check

---

## Key Improvements

✅ **No race conditions**: Auth check retries until AUTH object is ready  
✅ **No infinite loops**: Page waits for auth before initializing  
✅ **Consistent pattern**: All pages use same retry logic  
✅ **Demo mode compatible**: Works with localStorage-based identity (X-Citizen-Id header)  
✅ **Minimal latency**: 50ms retry interval is imperceptible to users  

---

## Testing the Fix

**Login flow now works correctly:**

1. Navigate to `http://localhost:8000/citizen-login.html`
2. Enter Citizen ID (e.g., "citizen-123")
3. Click "Login" → redirects to `/citizen-reports.html`
4. ✅ Reports page loads successfully (no redirect back to login)
5. ✅ Logout link works and clears auth

**Officer login flow:**

1. Navigate to `http://localhost:8000/officer-login.html`
2. Enter reviewer token (or use default from env)
3. Click "Login" → redirects to `/officer-queue.html`
4. ✅ Queue loads successfully (no redirect)
5. ✅ Logout works correctly

---

## Technical Details

### Why `setTimeout(fn, 50)`?

- **50ms** is a reasonable retry interval
- Allows JavaScript engine time to fully load all script blocks
- Imperceptible to users (human perception is ~100ms)
- Prevents busy-waiting or CPU spinning

### Why check `typeof AUTH === 'undefined'`?

- Covers the case where auth.js hasn't loaded yet
- Safer than just checking `!AUTH` (which could throw if object is partially initialized)
- Also checks the specific method: `!AUTH.isCitizen` or `!AUTH.isReviewer`

### Why defer everything?

- All page initialization (event listeners, data loading) happens in `setupPage()` or `initializeDetailPage()`
- Ensures DOM is ready AND auth is ready before trying to access protected data
- Prevents race conditions between DOM ready and auth ready

---

## Regression Prevention

To prevent this from happening again:

1. ✅ All auth checks now use `checkAuthAndLoad()` pattern
2. ✅ Documentation in code explains why the pattern is needed
3. ✅ Pattern is reusable across all frontend pages
4. ✅ Git commit includes detailed explanation

---

## Verification Checklist

- [x] Citizen login works without redirect loop
- [x] Citizen reports page loads after login
- [x] Officer login works without redirect loop
- [x] Officer queue page loads after login
- [x] Logout clears auth and returns to login
- [x] All pages use consistent auth check pattern
- [x] No console errors on auth check

---

**Next Steps:** If new frontend pages are added, apply the same `checkAuthAndLoad()` pattern to prevent regressions.
