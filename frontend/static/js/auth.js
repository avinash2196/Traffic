// Authentication Utilities
const AUTH_KEY_CITIZEN = 'citizen_id';
const AUTH_KEY_REVIEWER = 'reviewer_token';

// Set citizen ID (demo mode)
function setCitizenId(citizenId) {
  if (citizenId) {
    localStorage.setItem(AUTH_KEY_CITIZEN, citizenId);
  } else {
    localStorage.removeItem(AUTH_KEY_CITIZEN);
  }
}

// Get citizen ID
function getCitizenId() {
  return localStorage.getItem(AUTH_KEY_CITIZEN);
}

// Check if user is citizen
function isCitizen() {
  return !!getCitizenId() && !getReviewerToken();
}

// Set reviewer token
function setReviewerToken(token) {
  if (token) {
    localStorage.setItem(AUTH_KEY_REVIEWER, token);
  } else {
    localStorage.removeItem(AUTH_KEY_REVIEWER);
  }
}

// Get reviewer token
function getReviewerToken() {
  return localStorage.getItem(AUTH_KEY_REVIEWER);
}

// Check if user is reviewer/officer
function isReviewer() {
  return !!getReviewerToken();
}

// Clear all auth
function clearAuth() {
  localStorage.removeItem(AUTH_KEY_CITIZEN);
  localStorage.removeItem(AUTH_KEY_REVIEWER);
}

// Get user display name
function getUserDisplayName() {
  if (isReviewer()) {
    return 'Officer';
  }
  const citizenId = getCitizenId();
  return citizenId ? `Citizen ${citizenId.substring(0, 8)}` : 'Guest';
}

// Redirect to login if not authenticated
function requireAuth(requireReviewerAuth = false) {
  if (requireReviewerAuth && !isReviewer()) {
    window.location.href = '/officer-login.html';
    return false;
  }
  if (!requireReviewerAuth && !isCitizen()) {
    window.location.href = '/citizen-login.html';
    return false;
  }
  return true;
}

// Export functions
window.AUTH = {
  setCitizenId,
  getCitizenId,
  isCitizen,
  setReviewerToken,
  getReviewerToken,
  isReviewer,
  clearAuth,
  getUserDisplayName,
  requireAuth,
};
