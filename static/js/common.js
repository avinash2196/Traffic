// Common UI Utilities

// Show toast notification
function showToast(message, type = 'info', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(400px)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Show alert
function showAlert(message, type = 'info') {
  const alert = document.createElement('div');
  alert.className = `alert alert-${type}`;
  alert.textContent = message;
  
  const container = document.querySelector('main') || document.body;
  container.insertBefore(alert, container.firstChild);

  setTimeout(() => alert.remove(), 5000);
}

// Show loading indicator
function showLoading(message = 'Loading...') {
  const loading = document.createElement('div');
  loading.id = 'loading-indicator';
  loading.innerHTML = `
    <div class="spinner"></div>
    <p>${message}</p>
  `;
  loading.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 9999; text-align: center; background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);';
  document.body.appendChild(loading);
}

// Hide loading indicator
function hideLoading() {
  const loading = document.getElementById('loading-indicator');
  if (loading) loading.remove();
}

// Format date
function formatDate(isoDateString) {
  const date = new Date(isoDateString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Format violation type
function formatViolation(type) {
  const labels = {
    'helmet': 'No Helmet',
    'triple_riding': 'Triple Riding',
    'red_light': 'Red Light',
  };
  return labels[type] || type;
}

// Get status badge HTML
function getStatusBadge(status) {
  const badges = {
    'pending': '<span class="badge badge-pending">Pending</span>',
    'approved': '<span class="badge badge-approved">Approved</span>',
    'rejected': '<span class="badge badge-rejected">Rejected</span>',
    'processing': '<span class="badge badge-processing">Processing</span>',
  };
  return badges[status] || `<span class="badge">${status}</span>`;
}

// Get status color
function getStatusColor(status) {
  const colors = {
    'pending': '#ffc107',
    'approved': '#28a745',
    'rejected': '#dc3545',
    'processing': '#0066cc',
  };
  return colors[status] || '#666';
}

// Confirm action
function confirmAction(message) {
  return new Promise((resolve) => {
    if (confirm(message)) {
      resolve(true);
    } else {
      resolve(false);
    }
  });
}

// Format file size
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Load authenticated media (images/videos that require auth headers)
async function loadAuthenticatedMedia(mediaUrl, mediaType = 'image') {
  try {
    const citizenId = localStorage.getItem('citizen_id');
    const headers = {};
    if (citizenId) {
      headers['X-Citizen-Id'] = citizenId;
    }

    const response = await fetch(mediaUrl, {
      method: 'GET',
      headers: headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const blob = await response.blob();
    return URL.createObjectURL(blob);
  } catch (error) {
    console.error(`Failed to load media: ${error.message}`);
    return null;
  }
}

// Validate email
function isValidEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

// Disable button
function disableButton(buttonElement) {
  buttonElement.disabled = true;
  buttonElement.style.opacity = '0.6';
}

// Enable button
function enableButton(buttonElement) {
  buttonElement.disabled = false;
  buttonElement.style.opacity = '1';
}

// Export functions
window.UI = {
  showToast,
  showAlert,
  showLoading,
  hideLoading,
  formatDate,
  formatViolation,
  getStatusBadge,
  getStatusColor,
  confirmAction,
  formatFileSize,
  isValidEmail,
  disableButton,
  enableButton,
};
