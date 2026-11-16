# API Request/Response Reference Guide

**Quick reference for all 6 API endpoints with exact request/response formats for UI integration.**

---

## 🟢 CITIZEN ENDPOINTS

### 1. POST /api/reports — Submit Traffic Violation Report

**What the button does:** Citizen submits a new violation report  
**Where:** `/upload.html` → [Submit Report] button  
**When:** After citizen fills form (violation type, location, media upload)

```
REQUEST
─────────────────────────────────────────────────────────────
Method:   POST
URL:      /api/reports
Headers:
  Content-Type: application/json
  X-Citizen-Id: citizen-abc123xyz

Body (JSON):
{
  "violation_type": "helmet",        // dropdown: helmet, triple-riding, red-light
  "location": "MG Road, Bangalore",  // text input
  "media_id": "abc123xyz"            // from file upload (M3.2 media handler)
}

RESPONSE (201 Created)
─────────────────────────────────────────────────────────────
{
  "report_id": "595fcb31f692470e",
  "status": "submitted",
  "violation_type": "helmet",
  "location": "MG Road, Bangalore",
  "citizen_id": "citizen-abc123xyz",
  "provisional_points": 0,
  "created_at": "2026-11-01T19:00:00Z",
  "updated_at": "2026-11-01T19:00:00Z"
}

JS USAGE:
─────────────────────────────────────────────────────────────
async function submitReport() {
  const citizenId = getCitizenId(); // From localStorage
  const payload = {
    violation_type: document.getElementById('violationType').value,
    location: document.getElementById('location').value,
    media_id: uploadedMediaId // From file upload component
  };
  
  const response = await fetch('/api/reports', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Citizen-Id': citizenId
    },
    body: JSON.stringify(payload)
  });
  
  if (response.status === 201) {
    const data = await response.json();
    console.log('Report created:', data.report_id);
    // Show success message
    showSuccess(`✅ Report submitted! ID: ${data.report_id}`);
    // Redirect to details page after 2s
    setTimeout(() => window.location.href = `/reports/${data.report_id}.html`, 2000);
  } else if (response.status === 400) {
    const error = await response.json();
    showError(`❌ Validation Error: ${error.error}`);
  } else if (response.status === 401) {
    showError('❌ Authentication required. Please refresh.');
  }
}

ERROR CASES:
─────────────────────────────────────────────────────────────
400 Bad Request:
  Missing violation_type, location, or media_id
  → Show: "Please fill all fields"

401 Unauthorized:
  Missing or invalid X-Citizen-Id header
  → Show: "Authentication failed. Refresh page."

500 Server Error:
  Database error or file storage error
  → Show: "Server error. Try again later."
```

---

### 2. GET /api/reports — Fetch Citizen's Report History

**What the page does:** List all reports submitted by this citizen  
**Where:** `/reports.html`  
**When:** Page loads, pagination changes, [Refresh] button clicked

```
REQUEST
─────────────────────────────────────────────────────────────
Method:   GET
URL:      /api/reports?page=1&page_size=10
Headers:
  X-Citizen-Id: citizen-abc123xyz

Query Parameters (optional):
  page:      1 (default)
  page_size: 10 (default, max 100)

RESPONSE (200 OK)
─────────────────────────────────────────────────────────────
{
  "reports": [
    {
      "id": "595fcb31f692470e",
      "violation_type": "helmet",
      "location": "MG Road, Bangalore",
      "status": "submitted",
      "provisional_points": 0,
      "created_at": "2026-11-01T19:00:00Z",
      "updated_at": "2026-11-01T19:00:00Z"
    },
    {
      "id": "a1b2c3d4e5f67890",
      "violation_type": "red-light",
      "location": "Indiranagar, Bangalore",
      "status": "approved",
      "provisional_points": 3,
      "created_at": "2026-10-31T10:00:00Z",
      "updated_at": "2026-11-01T15:30:00Z"
    }
    // ... more reports
  ],
  "total_count": 5,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}

JS USAGE:
─────────────────────────────────────────────────────────────
async function loadReports(page = 1) {
  const citizenId = getCitizenId();
  
  try {
    const url = `/api/reports?page=${page}&page_size=10`;
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'X-Citizen-Id': citizenId
      }
    });
    
    if (response.status === 200) {
      const data = await response.json();
      
      // Render table
      data.reports.forEach(report => {
        const row = `
          <tr>
            <td><a href="/reports/${report.id}.html">${report.id}</a></td>
            <td>${report.violation_type}</td>
            <td><span class="status-${report.status}">${report.status}</span></td>
            <td>${formatDate(report.created_at)}</td>
            <td>${report.provisional_points}</td>
          </tr>
        `;
        tableBody.innerHTML += row;
      });
      
      // Update pagination
      document.getElementById('totalPages').textContent = data.total_pages;
      document.getElementById('totalCount').textContent = data.total_count;
      
    } else if (response.status === 401) {
      showError('Session expired. Refresh page.');
    }
  } catch (error) {
    showError('Failed to load reports. Try again.');
  }
}

ERROR CASES:
─────────────────────────────────────────────────────────────
401 Unauthorized:
  Missing X-Citizen-Id
  → Show: "Please refresh page to re-authenticate"

500 Server Error:
  Database query failed
  → Show: "Failed to load reports. Retry?"
```

---

### 3. GET /api/reports/{id} — Fetch Single Report with Timeline

**What the page does:** Show full report details + status timeline  
**Where:** `/reports/{id}.html`  
**When:** Page loads, [Auto-refresh] or status polling every 30s

```
REQUEST
─────────────────────────────────────────────────────────────
Method:   GET
URL:      /api/reports/{id}
Headers:
  X-Citizen-Id: citizen-abc123xyz

Path Parameter:
  {id}: Report ID from URL (e.g., "595fcb31f692470e")

RESPONSE (200 OK)
─────────────────────────────────────────────────────────────
{
  "id": "595fcb31f692470e",
  "citizen_id": "citizen-abc123xyz",
  "violation_type": "helmet",
  "location": "MG Road, Bangalore",
  "status": "awaiting-review",
  "provisional_points": 0,
  "created_at": "2026-11-01T19:00:00Z",
  "updated_at": "2026-11-01T19:05:00Z",
  "screening_notes": null,
  "officer_notes": null,
  
  "timeline": [
    {
      "id": "evt-001",
      "event_type": "status_change",
      "actor": "citizen",
      "old_status": null,
      "new_status": "submitted",
      "provisional_points": null,
      "reason": null,
      "created_at": "2026-11-01T19:00:00Z"
    },
    {
      "id": "evt-002",
      "event_type": "status_change",
      "actor": "system",
      "old_status": "submitted",
      "new_status": "screening",
      "provisional_points": null,
      "reason": null,
      "created_at": "2026-11-01T19:01:00Z"
    },
    {
      "id": "evt-003",
      "event_type": "status_change",
      "actor": "system",
      "old_status": "screening",
      "new_status": "awaiting-review",
      "provisional_points": null,
      "reason": null,
      "created_at": "2026-11-01T19:02:00Z"
    }
  ]
}

JS USAGE:
─────────────────────────────────────────────────────────────
async function loadReportDetail(reportId) {
  const citizenId = getCitizenId();
  
  try {
    const response = await fetch(`/api/reports/${reportId}`, {
      headers: { 'X-Citizen-Id': citizenId }
    });
    
    if (response.status === 200) {
      const report = await response.json();
      
      // Render header
      document.getElementById('reportId').textContent = report.id;
      document.getElementById('status').textContent = report.status;
      document.getElementById('statusColor').className = `status-${report.status}`;
      document.getElementById('points').textContent = report.provisional_points;
      
      // Render timeline
      report.timeline.forEach(event => {
        const eventCard = `
          <div class="event-card">
            <span class="event-icon">${getStatusIcon(event.new_status)}</span>
            <div>
              <strong>${event.old_status} → ${event.new_status}</strong>
              <p>by ${event.actor} at ${formatDate(event.created_at)}</p>
              ${event.reason ? `<p>Reason: ${event.reason}</p>` : ''}
              ${event.provisional_points ? `<p>Points: ${event.provisional_points}</p>` : ''}
            </div>
          </div>
        `;
        timelineContainer.innerHTML += eventCard;
      });
      
      // Show clarification form if needed
      if (report.status === 'awaiting-citizen-info') {
        document.getElementById('clarificationForm').style.display = 'block';
      } else {
        document.getElementById('clarificationForm').style.display = 'none';
      }
      
    } else if (response.status === 403) {
      showError('❌ Access denied. This is not your report.');
    } else if (response.status === 404) {
      showError('❌ Report not found.');
    }
  } catch (error) {
    showError('Failed to load report details.');
  }
}

// Auto-refresh every 30 seconds
function startAutoRefresh(reportId) {
  setInterval(() => loadReportDetail(reportId), 30000);
}

ERROR CASES:
─────────────────────────────────────────────────────────────
401 Unauthorized:
  → Redirect to login

403 Forbidden:
  Report belongs to different citizen
  → Show: "You cannot view this report"

404 Not Found:
  Report ID doesn't exist
  → Show: "Report not found"
```

---

### 4. POST /api/reports/{id}/clarification — Submit Clarification Response

**What the button does:** Citizen responds to officer's request for more info  
**Where:** `/reports/{id}.html` → [Submit Clarification] button (only if status = awaiting-citizen-info)  
**When:** Citizen fills clarification form (text + new media)

```
REQUEST
─────────────────────────────────────────────────────────────
Method:   POST
URL:      /api/reports/{id}/clarification
Headers:
  Content-Type: application/json
  X-Citizen-Id: citizen-abc123xyz

Body (JSON):
{
  "clarification_text": "Here's a clearer photo showing the violation",
  "new_media_id": "xyz789abc"  // From file upload
}

RESPONSE (200 OK)
─────────────────────────────────────────────────────────────
{
  "report_id": "595fcb31f692470e",
  "status": "resubmitted",
  "new_media_id": "xyz789abc",
  "clarification_event": {
    "id": "evt-005",
    "event_type": "clarification",
    "actor": "citizen",
    "old_status": "awaiting-citizen-info",
    "new_status": "resubmitted",
    "created_at": "2026-11-01T19:25:00Z"
  }
}

JS USAGE:
─────────────────────────────────────────────────────────────
async function submitClarification(reportId) {
  const citizenId = getCitizenId();
  const payload = {
    clarification_text: document.getElementById('clarificationText').value,
    new_media_id: newMediaId  // From file upload
  };
  
  const response = await fetch(`/api/reports/${reportId}/clarification`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Citizen-Id': citizenId
    },
    body: JSON.stringify(payload)
  });
  
  if (response.status === 200) {
    const data = await response.json();
    showSuccess('✅ Clarification submitted! Case re-entered queue.');
    setTimeout(() => window.location.reload(), 2000);
  } else if (response.status === 409) {
    showError('❌ Report is not awaiting clarification.');
  }
}

ERROR CASES:
─────────────────────────────────────────────────────────────
400 Bad Request:
  Missing clarification_text or new_media_id
  → Show: "Please fill all fields"

401 Unauthorized:
  → Redirect to login

403 Forbidden:
  Not citizen's report
  → Show: "Not your report"

404 Not Found:
  Report doesn't exist
  → Show: "Report not found"

409 Conflict:
  Status is not awaiting-citizen-info
  → Show: "Officer is not waiting for clarification"
```

---

## 🔵 OFFICER ENDPOINTS

### 5. GET /api/authority/reports — Fetch Officer Review Queue

**What the page does:** List all reports awaiting officer review  
**Where:** `/authority/queue.html`  
**When:** Page loads, filter/pagination changes, [Refresh] button clicked

```
REQUEST
─────────────────────────────────────────────────────────────
Method:   GET
URL:      /api/authority/reports?page=1&page_size=10&status=awaiting-review
Headers:
  Authorization: Bearer demo-token

Query Parameters (optional):
  page:   1 (default)
  page_size: 10 (default)
  status: awaiting-review | resubmitted | null (all statuses)

RESPONSE (200 OK)
─────────────────────────────────────────────────────────────
{
  "reports": [
    {
      "id": "595fcb31f692470e",
      "citizen_id": "citizen-abc123xyz",
      "violation_type": "helmet",
      "location": "MG Road, Bangalore",
      "status": "awaiting-review",
      "media_count": 1,
      "created_at": "2026-11-01T19:00:00Z"
    },
    {
      "id": "a1b2c3d4e5f67890",
      "citizen_id": "citizen-xyz789abc",
      "violation_type": "red-light",
      "location": "Indiranagar, Bangalore",
      "status": "resubmitted",
      "media_count": 2,
      "created_at": "2026-11-01T18:00:00Z"
    }
    // ... more reports
  ],
  "total_count": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3
}

JS USAGE:
─────────────────────────────────────────────────────────────
async function loadQueue(page = 1, statusFilter = null) {
  const authToken = getAuthToken(); // From localStorage
  
  let url = `/api/authority/reports?page=${page}&page_size=10`;
  if (statusFilter) url += `&status=${statusFilter}`;
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Authorization': authToken
      }
    });
    
    if (response.status === 200) {
      const data = await response.json();
      
      // Render queue table
      data.reports.forEach(report => {
        const row = `
          <tr onclick="window.location.href='/authority/case/${report.id}.html'">
            <td>${report.id}</td>
            <td>${maskCitizenId(report.citizen_id)}</td>
            <td>${report.violation_type}</td>
            <td>${report.location}</td>
            <td><span class="status-${report.status}">${report.status}</span></td>
            <td>${report.media_count} 📎</td>
            <td>${formatTimeAgo(report.created_at)}</td>
          </tr>
        `;
        queueBody.innerHTML += row;
      });
      
      // Update pagination
      document.getElementById('totalReports').textContent = data.total_count;
      
    } else if (response.status === 401) {
      showError('Unauthorized. Check auth token.');
    }
  } catch (error) {
    showError('Failed to load queue.');
  }
}

// Handle filter change
document.getElementById('statusFilter').addEventListener('change', (e) => {
  loadQueue(1, e.target.value);
});

ERROR CASES:
─────────────────────────────────────────────────────────────
401 Unauthorized:
  Missing or invalid Authorization header
  → Show: "Authentication failed"

500 Server Error:
  Database error
  → Show: "Failed to load queue"
```

---

### 6. POST /api/authority/reports/{id}/decision — Submit Officer Decision

**What the button does:** Officer approves, rejects, or requests more info  
**Where:** `/authority/case/{id}.html` → [Approve], [Reject], or [Request Info] button  
**When:** Officer submits decision

```
REQUEST (3 variants)
─────────────────────────────────────────────────────────────

VARIANT A: APPROVE
Method:   POST
URL:      /api/authority/reports/{id}/decision
Headers:
  Content-Type: application/json
  Authorization: Bearer demo-token

Body:
{
  "action": "approve"
}

VARIANT B: REJECT
Body:
{
  "action": "reject",
  "reason": "blurry"  // or "low-quality", "invalid", etc.
}

VARIANT C: REQUEST INFO
Body:
{
  "action": "request-info"
}

RESPONSE (200 OK) — VARIANT A (Approve)
─────────────────────────────────────────────────────────────
{
  "id": "595fcb31f692470e",
  "status": "approved",
  "provisional_points": 2,
  "decision_event": {
    "id": "evt-004",
    "event_type": "decision",
    "actor": "officer",
    "old_status": "awaiting-review",
    "new_status": "approved",
    "provisional_points": 2,
    "created_at": "2026-11-01T19:30:00Z"
  }
}

RESPONSE (200 OK) — VARIANT B (Reject)
─────────────────────────────────────────────────────────────
{
  "id": "595fcb31f692470e",
  "status": "rejected",
  "reason": "blurry",
  "decision_event": {
    "id": "evt-004",
    "event_type": "decision",
    "actor": "officer",
    "old_status": "awaiting-review",
    "new_status": "rejected",
    "reason": "blurry",
    "created_at": "2026-11-01T19:30:00Z"
  }
}

RESPONSE (200 OK) — VARIANT C (Request Info)
─────────────────────────────────────────────────────────────
{
  "id": "595fcb31f692470e",
  "status": "awaiting-citizen-info",
  "decision_event": {
    "id": "evt-004",
    "event_type": "decision",
    "actor": "officer",
    "old_status": "awaiting-review",
    "new_status": "awaiting-citizen-info",
    "created_at": "2026-11-01T19:30:00Z"
  }
}

JS USAGE:
─────────────────────────────────────────────────────────────
// APPROVE
async function approveReport(reportId) {
  const authToken = getAuthToken();
  
  const response = await fetch(`/api/authority/reports/${reportId}/decision`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': authToken
    },
    body: JSON.stringify({ action: 'approve' })
  });
  
  if (response.status === 200) {
    const data = await response.json();
    showSuccess(`✅ Approved! Points awarded: ${data.provisional_points}`);
    setTimeout(() => window.location.href = '/authority/queue.html', 2000);
  }
}

// REJECT
async function rejectReport(reportId, reason) {
  const authToken = getAuthToken();
  
  const response = await fetch(`/api/authority/reports/${reportId}/decision`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': authToken
    },
    body: JSON.stringify({
      action: 'reject',
      reason: reason  // From dropdown or text input
    })
  });
  
  if (response.status === 200) {
    showSuccess(`✅ Rejected with reason: ${reason}`);
    setTimeout(() => window.location.href = '/authority/queue.html', 2000);
  }
}

// REQUEST INFO
async function requestClarification(reportId) {
  const authToken = getAuthToken();
  
  const response = await fetch(`/api/authority/reports/${reportId}/decision`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': authToken
    },
    body: JSON.stringify({ action: 'request-info' })
  });
  
  if (response.status === 200) {
    showSuccess('✅ Citizen notified to submit clarification');
    setTimeout(() => window.location.href = '/authority/queue.html', 2000);
  }
}

ERROR CASES:
─────────────────────────────────────────────────────────────
400 Bad Request:
  Missing action field or invalid action
  → Show: "Invalid decision"

401 Unauthorized:
  Missing or invalid auth token
  → Show: "Authentication failed"

404 Not Found:
  Report doesn't exist
  → Show: "Report not found"

409 Conflict:
  Report is not in awaiting-review status
  → Show: "Cannot decide. Report status changed or already decided."
```

---

## 📊 Status Code Quick Ref

| Code | Meaning | Action |
|------|---------|--------|
| **200** | OK | Process success response |
| **201** | Created | New resource created (POST /api/reports) |
| **400** | Bad Request | Show validation error from response.error |
| **401** | Unauthorized | Redirect to login / refresh auth |
| **403** | Forbidden | Show "Access denied" |
| **404** | Not Found | Show "Resource not found" |
| **409** | Conflict | Show "Invalid action" (status conflict) |
| **500** | Server Error | Show "Server error, try again" + retry button |

---

## 🔒 Header Quick Ref

| Portal | Header | Format |
|--------|--------|--------|
| **Citizen** | `X-Citizen-Id` | `citizen-{random}` or `citizen-12345` |
| **Officer** | `Authorization` | `Bearer demo-token` |

---

## 🕐 Polling Strategy (Citizen)

```javascript
// Start when citizen views report detail
function startStatusPolling(reportId, intervalMs = 30000) {
  const pollInterval = setInterval(async () => {
    const response = await fetch(`/api/reports/${reportId}`, {
      headers: { 'X-Citizen-Id': getCitizenId() }
    });
    
    if (response.ok) {
      const report = await response.json();
      
      // Check if status changed
      const oldStatus = document.getElementById('status').textContent;
      if (report.status !== oldStatus) {
        console.log(`Status changed: ${oldStatus} → ${report.status}`);
        showNotification(`Status updated to: ${report.status}`);
        // Refresh entire page to show new timeline + decision
        window.location.reload();
      }
    }
  }, intervalMs);
  
  return pollInterval;  // Can call clearInterval(pollInterval) to stop
}

// Call on page load
const pollerId = startStatusPolling('595fcb31f692470e', 30000);

// Call on page unload to stop polling
window.addEventListener('beforeunload', () => {
  clearInterval(pollerId);
});
```

---

## ✅ Testing Scenarios

Use this to verify all API paths work end-to-end:

**Scenario 1: Happy Path (Citizen → Approved)**
1. Citizen uploads report → 201 POST /api/reports
2. Citizen checks status (3 times, 30s apart) → 200 GET /api/reports/{id}
3. Officer reviews queue → 200 GET /api/authority/reports
4. Officer opens case → manual lookup or search
5. Officer approves → 200 POST /api/authority/reports/{id}/decision {approve}
6. Citizen sees approval → 200 GET /api/reports/{id} (new event in timeline)

**Scenario 2: Clarification Loop**
1. Officer requests info → 200 POST /api/authority/reports/{id}/decision {request-info}
2. Citizen submits clarification → 200 POST /api/reports/{id}/clarification
3. Citizen checks status → 200 GET /api/reports/{id} (status=resubmitted)
4. Officer sees resubmitted → 200 GET /api/authority/reports?status=resubmitted
5. Officer approves resubmission → 200 POST /api/authority/reports/{id}/decision {approve}

**Scenario 3: Rejection**
1. Officer rejects → 200 POST /api/authority/reports/{id}/decision {reject, reason}
2. Citizen sees rejection → 200 GET /api/reports/{id} (status=rejected, event with reason)

