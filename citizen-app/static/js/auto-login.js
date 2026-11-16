// Auto-login for demo mode
// This ensures all users have a citizen ID for testing
(function() {
  // Only run once per page load
  if (window._autoLoginRan) return;
  window._autoLoginRan = true;

  // Check if citizen ID exists
  const existingId = localStorage.getItem('citizen_id');
  if (existingId) {
    console.log('Using existing citizen ID:', existingId);
    return;
  }

  // Auto-generate a demo citizen ID
  const demoCitizenId = 'demo-' + Math.random().toString(36).substring(2, 11);
  localStorage.setItem('citizen_id', demoCitizenId);
  console.log('Auto-logged in with demo citizen ID:', demoCitizenId);
})();
