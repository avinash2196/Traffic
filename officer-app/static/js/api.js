// API Client Utilities
// For MVP: Call individual backend services directly

// Get API URL for endpoint
let API_BASE = 'http://127.0.0.1:9002/api'; // Default fallback

// Load config from frontend server
async function loadAPIConfig() {
  try {
    const response = await fetch('/config');
    const config = await response.json();
    API_BASE = `${config.api.officer}/api`;
  } catch (err) {
    console.warn('Failed to load config, using default API_BASE:', err);
  }
}

// Initialize config on script load
loadAPIConfig();

// Polling configuration
const POLL_INTERVAL_MS = 30000; // 30 seconds

// Get API URL for endpoint
function apiUrl(endpoint) {
  return `${API_BASE}${endpoint}`;
}

// Make API request with error handling
async function apiRequest(method, endpoint, data = null, useAuthHeader = false) {
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  // Add citizen ID or authorization header
  if (useAuthHeader) {
    const token = localStorage.getItem('reviewer_token');
    if (token) {
      options.headers['Authorization'] = `Bearer ${token}`;
    }
  } else {
    const citizenId = localStorage.getItem('citizen_id');
    if (citizenId) {
      options.headers['X-Citizen-Id'] = citizenId;
    }
  }

  if (data) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(apiUrl(endpoint), options);
    const responseData = await response.json().catch(() => null);

    if (!response.ok) {
      return {
        success: false,
        status: response.status,
        error: responseData?.detail || `HTTP ${response.status}`,
        data: responseData,
      };
    }

    return {
      success: true,
      status: response.status,
      data: responseData,
    };
  } catch (error) {
    return {
      success: false,
      status: 0,
      error: `Network error: ${error.message}`,
      data: null,
    };
  }
}

// Citizen API calls
async function createReport(reportData) {
  return apiRequest('POST', '/reports', reportData);
}

async function getReports(page = 1, pageSize = 10) {
  return apiRequest('GET', `/reports?page=${page}&page_size=${pageSize}`);
}

async function getReportDetail(reportId) {
  return apiRequest('GET', `/reports/${reportId}`);
}

// Officer API calls
async function getReviewQueue(page = 1, pageSize = 10) {
  return apiRequest('GET', `/authority/reports?page=${page}&page_size=${pageSize}`, null, true);
}

async function getReviewDetail(reportId) {
  return apiRequest('GET', `/authority/reports/${reportId}`, null, true);
}

async function submitDecision(reportId, decisionData) {
  return apiRequest('POST', `/authority/reports/${reportId}/decision`, decisionData, true);
}

async function downloadEvidence(reportId) {
  const token = localStorage.getItem('reviewer_token');
  const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
  
  try {
    const response = await fetch(apiUrl(`/authority/reports/${reportId}/evidence.zip`), {
      method: 'GET',
      headers,
    });

    if (!response.ok) {
      return {
        success: false,
        status: response.status,
        error: `Failed to download evidence (HTTP ${response.status})`,
      };
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `evidence-${reportId}.zip`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    return { success: true, status: 200 };
  } catch (error) {
    return {
      success: false,
      status: 0,
      error: `Network error: ${error.message}`,
    };
  }
}

// Health check
async function checkHealth() {
  try {
    const response = await fetch(apiUrl('/health'));
    return response.ok;
  } catch {
    return false;
  }
}

// Export functions
window.API = {
  createReport,
  getReports,
  getReportDetail,
  getReviewQueue,
  getReviewDetail,
  submitDecision,
  downloadEvidence,
  checkHealth,
  POLL_INTERVAL_MS,
};
