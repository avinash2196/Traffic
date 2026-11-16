# M5 UI SCAFFOLDING — Implementation Checklist & API Mapping

## 🎯 Overview

**Objective:** Build vanilla HTML/CSS/JS UI templates for citizen and officer portals  
**Constraint:** Vanilla (no frameworks), responsive, accessible  
**Architecture:** Separate HTML files + shared CSS + minimal JS for API calls & polling  

---

## 📋 CITIZEN PORTAL — Component Breakdown

### Page 1: Dashboard (`/index.html` or `/dashboard.html`)

**Purpose:** Landing page after authentication  
**API Calls:** None (static)  
**Components:**
- [ ] Navbar with logout button
- [ ] Welcome message with citizen ID
- [ ] Quick stats (reports submitted, approved, pending)
- [ ] CTA buttons:
  - [ ] [+ New Report] → /upload.html
  - [ ] [My Reports] → /reports.html
  - [ ] [Check Status] → /reports.html

**Template Structure:**
```html
<!DOCTYPE html>
<html>
<head>
  <title>RoadWatch - Citizen Portal</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav class="navbar">
    <span>RoadWatch Traffic</span>
    <button id="logout">Logout</button>
  </nav>
  
  <main class="container">
    <h1>Welcome, {citizen_name}</h1>
    <!-- Stats cards, CTA buttons -->
  </main>
  
  <script src="auth.js"></script>
  <script src="dashboard.js"></script>
</body>
</html>
```

---

### Page 2: Upload Report (`/upload.html`)

**Purpose:** Submit new traffic violation report  
**API Call:**
- `POST /api/reports` → Submit report
- `GET /api/reports` → Optional: poll after submit to show created ID

**Components:**
- [ ] Form header
- [ ] Violation Type selector (dropdown or radio)
  - [ ] helmet
  - [ ] triple-riding
  - [ ] red-light
- [ ] Location input (text, autocomplete optional)
- [ ] File upload widget
  - [ ] Accept JPG/PNG (max 25MB)
  - [ ] File size validation
  - [ ] Preview on client side
- [ ] Validation feedback
- [ ] Submit button
  - [ ] Disable during submission
  - [ ] Show loading spinner
- [ ] Success message
  - [ ] Display report_id
  - [ ] Show "View Status" link
- [ ] Error handling
  - [ ] Display error message from API

**JavaScript Logic:**
```javascript
// upload.js
- validateFile() → Check size, type
- handleFileSelect() → Show preview
- submitReport() → POST /api/reports
  - Build FormData with violation_type, location, media_id
  - Handle 201 response
  - Handle 400/401/500 errors
- showSuccess() → Display report_id, auto-redirect to status page
```

**API Request/Response:**
```javascript
// POST /api/reports
const payload = {
  violation_type: "helmet",     // From dropdown
  location: "MG Road, Bangalore", // From text input
  media_id: "abc123xyz"          // From media upload (M3.2)
};

// Response 201
{
  report_id: "595fcb31f692470e",
  status: "submitted",
  violation_type: "helmet",
  citizen_id: "citizen-12345",
  created_at: "2026-11-01T19:00:00Z"
}
```

---

### Page 3: Report List (`/reports.html`)

**Purpose:** View all reports submitted by citizen  
**API Calls:**
- `GET /api/reports?page={n}&page_size=10` → Fetch paginated list

**Components:**
- [ ] Page header with filters
- [ ] Table/List view:
  - [ ] Report ID (clickable → details page)
  - [ ] Violation Type (badge with icon)
  - [ ] Status (colored badge)
  - [ ] Created date (human-readable)
  - [ ] Quick action (View)
- [ ] Pagination controls
  - [ ] Previous/Next buttons
  - [ ] Page indicator (Page 1 of 3)
  - [ ] Jump to page (optional)
- [ ] Empty state (no reports)
- [ ] Loading state (skeleton, spinner)
- [ ] Error state (retry button)
- [ ] [+ New Report] button

**JavaScript Logic:**
```javascript
// reports.js
- loadReports(page=1) → GET /api/reports?page={page}&page_size=10
  - Show loading skeleton
  - Populate table rows
  - Update pagination
- handlePagination(pageNumber) → loadReports(pageNumber)
- formatStatus(status) → Return CSS class + display text
- formatDate(isoString) → Return human-readable date
- handleRowClick(reportId) → Navigate to details page
```

**API Request/Response:**
```javascript
// GET /api/reports?page=1&page_size=10
// Response 200
{
  reports: [
    {
      id: "595fcb31f692470e",
      violation_type: "helmet",
      location: "MG Road, Bangalore",
      status: "submitted",
      provisional_points: 0,
      created_at: "2026-11-01T19:00:00Z"
    },
    // ... more reports
  ],
  total_count: 5,
  page: 1,
  page_size: 10,
  total_pages: 1
}
```

---

### Page 4: Report Details with Timeline (`/reports/{id}.html`)

**Purpose:** View single report status, timeline, and conditional clarification form  
**API Calls:**
- `GET /api/reports/{id}` → Fetch report + timeline
- `POST /api/reports/{id}/clarification` → Submit clarification (conditional)

**Components:**
- [ ] Report header card
  - [ ] Report ID (copyable)
  - [ ] Status badge (color-coded)
  - [ ] Violation Type
  - [ ] Location
  - [ ] Provisional Points (if awarded)
  - [ ] Created timestamp
- [ ] Timeline section
  - [ ] Event cards in chronological order
  - [ ] Event type icon + label (status_change, clarification, decision, etc.)
  - [ ] Actor (citizen, system, officer)
  - [ ] Old status → New status
  - [ ] Timestamp
  - [ ] Reason (if rejection)
  - [ ] Provisional points (if decision)
- [ ] Conditional sections:
  - [ ] **If status = "awaiting-citizen-info":**
    - [ ] Clarification request notice
    - [ ] Clarification form:
      - [ ] Text textarea for clarification
      - [ ] File upload for new media
      - [ ] [Submit Clarification] button
  - [ ] **If status = "approved" or "rejected":**
    - [ ] Final verdict section
    - [ ] Officer notes (if any)
    - [ ] Provisional points (if approved)
- [ ] [Back to List] button
- [ ] Auto-refresh button (or every 30s)

**JavaScript Logic:**
```javascript
// report-details.js
- extractReportId() → From URL path
- loadReportDetails(reportId) → GET /api/reports/{reportId}
  - Show loading skeleton
  - Populate report header
  - Render timeline events
  - Show/hide clarification form based on status
- renderTimeline(events) → Create event cards
  - Sort by created_at ascending
  - Format each event with icon, label, timestamp
- submitClarification(reportId, text, mediaId)
  - POST /api/reports/{reportId}/clarification
  - Handle 200 response (refresh page)
  - Handle errors
- autoRefresh(interval=30000) → Call loadReportDetails every 30s
```

**API Request/Response:**
```javascript
// GET /api/reports/{id}
// Response 200
{
  id: "595fcb31f692470e",
  citizen_id: "citizen-12345",
  violation_type: "helmet",
  location: "MG Road, Bangalore",
  status: "awaiting-review",
  provisional_points: 0,
  created_at: "2026-11-01T19:00:00Z",
  updated_at: "2026-11-01T19:05:00Z",
  timeline: [
    {
      id: "evt-001",
      event_type: "status_change",
      actor: "citizen",
      old_status: null,
      new_status: "submitted",
      created_at: "2026-11-01T19:00:00Z"
    },
    {
      id: "evt-002",
      event_type: "status_change",
      actor: "system",
      old_status: "submitted",
      new_status: "screening",
      created_at: "2026-11-01T19:01:00Z"
    },
    // ... more events
  ]
}
```

---

## 📋 OFFICER PORTAL — Component Breakdown

### Page 1: Review Queue (`/authority/queue.html`)

**Purpose:** Display paginated list of reports awaiting review  
**API Calls:**
- `GET /api/authority/reports?page={n}&page_size=10&status={status}` → Fetch queue

**Components:**
- [ ] Page header
  - [ ] "Review Queue" title
  - [ ] Total reports count
  - [ ] Last refreshed timestamp
- [ ] Filter bar
  - [ ] Status dropdown (All / awaiting-review / resubmitted)
  - [ ] [Filter] button or auto-filter on select
- [ ] Table/List view:
  - [ ] Report ID (clickable → case detail)
  - [ ] Citizen ID (masked: citizen-**)
  - [ ] Violation Type (badge)
  - [ ] Location
  - [ ] Status (badge)
  - [ ] Created timestamp (time-ago format)
  - [ ] Media count badge
  - [ ] Quick action (Open/Review)
- [ ] Pagination controls
- [ ] Loading state (skeleton rows)
- [ ] Empty state (no reports in queue)
- [ ] Error state (retry button)
- [ ] [Refresh] button (manual refresh)

**JavaScript Logic:**
```javascript
// queue.js
- loadQueue(page=1, status=null) → GET /api/authority/reports?page={page}&page_size=10&status={status}
  - Show loading skeleton
  - Populate table rows
  - Update pagination
- handleFilterChange(newStatus) → loadQueue(1, newStatus)
- handlePagination(pageNumber) → loadQueue(pageNumber)
- formatCitizenId(id) → Mask to "citizen-**"
- formatTimeAgo(isoString) → "2 hours ago", "5 minutes ago"
- handleRowClick(reportId) → Navigate to case detail
- refreshManual() → loadQueue()
```

**API Request/Response:**
```javascript
// GET /api/authority/reports?page=1&page_size=10
// Response 200
{
  reports: [
    {
      id: "595fcb31f692470e",
      citizen_id: "citizen-12345",
      violation_type: "helmet",
      location: "MG Road, Bangalore",
      status: "awaiting-review",
      media_count: 1,
      created_at: "2026-11-01T19:00:00Z"
    },
    // ... more reports
  ],
  total_count: 25,
  page: 1,
  page_size: 10,
  total_pages: 3
}
```

---

### Page 2: Case Detail & Decision (`/authority/case/{id}.html`)

**Purpose:** View full case details, media, and make decision  
**API Calls:**
- `GET /api/authority/reports?page=1&page_size=1` + filter by ID (workaround, no single-report GET for officer)
  OR manual lookup via report list
- `POST /api/authority/reports/{id}/decision` → Submit officer decision

**Components:**
- [ ] Case header
  - [ ] Report ID (copyable)
  - [ ] Status badge
  - [ ] Violation Type badge
  - [ ] Created timestamp
  - [ ] Assigned to: (shows "You" for demo)
- [ ] Report details card
  - [ ] Citizen ID (masked: citizen-**)
  - [ ] Violation Type
  - [ ] Location
  - [ ] Created date (full timestamp)
  - [ ] Description/Notes (if available)
- [ ] Media section
  - [ ] Media viewer (image or video player)
    - [ ] Full-screen toggle
    - [ ] Download button
  - [ ] File metadata
    - [ ] Filename
    - [ ] File hash (SHA-256, for audit trail)
    - [ ] Technical screening score (if available, Phase 2)
- [ ] Timeline/Events section
  - [ ] All events (citizen uploads, clarifications, officer actions)
  - [ ] Chronological order
  - [ ] Same format as citizen details page
- [ ] Decision section
  - [ ] [✅ Approve] button → Show confirm + direct to queue
  - [ ] [❌ Reject] button → Show modal with reason field
    - [ ] Reason dropdown or text
    - [ ] [Submit Rejection] button
  - [ ] [❓ Request Clarification] button → Show confirm modal
    - [ ] Optional: custom message field
    - [ ] [Request Info] button
  - [ ] Buttons disabled during submission
- [ ] [Back to Queue] button

**JavaScript Logic:**
```javascript
// case-detail.js
- extractReportId() → From URL path
- loadCaseDetail(reportId) 
  - Show loading skeleton
  - Fetch report (from list API or manual query)
  - Render case details, media, timeline
  - Enable decision buttons
- renderMediaViewer(media)
  - Detect type (image/video)
  - Render <img> or <video>
  - Add full-screen button
- submitApproval(reportId)
  - POST /api/authority/reports/{reportId}/decision
    - payload: {action: "approve"}
  - On 200: Show success, redirect to queue after 2s
  - On error: Show error modal, keep on page
- submitRejection(reportId, reason)
  - POST /api/authority/reports/{reportId}/decision
    - payload: {action: "reject", reason}
  - On 200: Show success, redirect to queue
- submitRequestInfo(reportId)
  - POST /api/authority/reports/{reportId}/decision
    - payload: {action: "request-info"}
  - On 200: Show success, redirect to queue
- handleDecisionResponse(response)
  - Extract status, provisional_points
  - Show confirmation toast
```

**API Request/Response:**
```javascript
// POST /api/authority/reports/{id}/decision
// Request (Approve)
{
  action: "approve"
}
// Response 200
{
  id: "595fcb31f692470e",
  status: "approved",
  provisional_points: 2,
  decision_event: {
    event_type: "decision",
    actor: "officer",
    old_status: "awaiting-review",
    new_status: "approved",
    provisional_points: 2,
    created_at: "2026-11-01T19:30:00Z"
  }
}

// Request (Reject)
{
  action: "reject",
  reason: "blurry"
}
// Response 200
{
  id: "595fcb31f692470e",
  status: "rejected",
  reason: "blurry",
  decision_event: {
    event_type: "decision",
    actor: "officer",
    old_status: "awaiting-review",
    new_status: "rejected",
    reason: "blurry",
    created_at: "2026-11-01T19:30:00Z"
  }
}

// Request (Request Info)
{
  action: "request-info"
}
// Response 200
{
  id: "595fcb31f692470e",
  status: "awaiting-citizen-info",
  decision_event: {
    event_type: "decision",
    actor: "officer",
    old_status: "awaiting-review",
    new_status: "awaiting-citizen-info",
    created_at: "2026-11-01T19:30:00Z"
  }
}
```

---

## 🛠️ Shared Assets — CSS, JS Libraries, Utilities

### File Structure
```
static/
├── css/
│   ├── base.css          # Reset, typography, colors
│   ├── layout.css        # Grid, flexbox, spacing
│   ├── components.css    # Buttons, cards, badges, forms
│   └── responsive.css    # Mobile breakpoints (768px, 1024px)
├── js/
│   ├── auth.js           # Get/validate citizen_id or auth token
│   ├── api.js            # Fetch wrapper, error handling
│   ├── utils.js          # formatDate, maskId, etc.
│   └── common.js         # Navbar, logout, shared interactions
└── images/
    ├── logo.svg
    ├── icons/            # Violation types, status badges
```

### auth.js
```javascript
// Citizen side
function getCitizenId() {
  return localStorage.getItem('citizen_id') || generateCitizenId();
}

function generateCitizenId() {
  const id = 'citizen-' + Math.random().toString(36).substr(2, 9);
  localStorage.setItem('citizen_id', id);
  return id;
}

// Officer side
function getAuthToken() {
  return localStorage.getItem('auth_token') || 'Bearer demo-token';
}
```

### api.js
```javascript
// Generic fetch wrapper
async function apiCall(method, endpoint, body=null, isOfficer=false) {
  const headers = {
    'Content-Type': 'application/json',
  };
  
  if (isOfficer) {
    headers['Authorization'] = getAuthToken();
  } else {
    headers['X-Citizen-Id'] = getCitizenId();
  }
  
  const options = {
    method,
    headers,
  };
  
  if (body) options.body = JSON.stringify(body);
  
  try {
    const response = await fetch(`/api${endpoint}`, options);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || `HTTP ${response.status}`);
    }
    
    return { success: true, data, status: response.status };
  } catch (error) {
    return { success: false, error: error.message, status: response?.status };
  }
}

// Usage
const result = await apiCall('GET', '/reports', null, false);
if (result.success) {
  // Handle data
} else {
  // Show error: result.error
}
```

### utils.js
```javascript
function formatDate(isoString) {
  const date = new Date(isoString);
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function formatTimeAgo(isoString) {
  const seconds = Math.floor((new Date() - new Date(isoString)) / 1000);
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60,
  };
  
  for (const [label, secondsInUnit] of Object.entries(intervals)) {
    const interval = Math.floor(seconds / secondsInUnit);
    if (interval >= 1) {
      return interval === 1 ? `${interval} ${label} ago` : `${interval} ${label}s ago`;
    }
  }
  return 'just now';
}

function maskCitizenId(id) {
  return id.substring(0, 8) + '**';
}

function getStatusColor(status) {
  const colors = {
    'submitted': 'gray',
    'screening': 'blue',
    'awaiting-review': 'orange',
    'awaiting-citizen-info': 'orange',
    'resubmitted': 'blue',
    'approved': 'green',
    'rejected': 'red',
  };
  return colors[status] || 'gray';
}

function getStatusIcon(status) {
  const icons = {
    'submitted': '📤',
    'screening': '👀',
    'awaiting-review': '⏳',
    'awaiting-citizen-info': '❓',
    'resubmitted': '🔄',
    'approved': '✅',
    'rejected': '❌',
  };
  return icons[status] || '•';
}
```

---

## 📐 HTML Template Boilerplate

### Citizen Portal Base
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RoadWatch - Citizen Portal</title>
  <link rel="stylesheet" href="/static/css/base.css">
  <link rel="stylesheet" href="/static/css/layout.css">
  <link rel="stylesheet" href="/static/css/components.css">
  <link rel="stylesheet" href="/static/css/responsive.css">
</head>
<body>
  <nav class="navbar">
    <div class="navbar-brand">
      🚗 RoadWatch Traffic
    </div>
    <div class="navbar-menu">
      <a href="/dashboard.html">Dashboard</a>
      <a href="/reports.html">My Reports</a>
      <span id="citizen-id" class="citizen-info"></span>
      <button id="logout-btn" class="btn-logout">Logout</button>
    </div>
  </nav>
  
  <main class="container">
    <!-- Page-specific content here -->
  </main>
  
  <footer class="footer">
    <p>&copy; 2026 RoadWatch. All rights reserved.</p>
  </footer>
  
  <script src="/static/js/utils.js"></script>
  <script src="/static/js/auth.js"></script>
  <script src="/static/js/api.js"></script>
  <script src="/static/js/common.js"></script>
  <script src="/static/js/page-specific.js"></script> <!-- Page-specific JS -->
</body>
</html>
```

### Officer Portal Base
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RoadWatch - Officer Portal</title>
  <link rel="stylesheet" href="/static/css/base.css">
  <link rel="stylesheet" href="/static/css/layout.css">
  <link rel="stylesheet" href="/static/css/components.css">
  <link rel="stylesheet" href="/static/css/responsive.css">
  <link rel="stylesheet" href="/static/css/officer.css">
</head>
<body>
  <nav class="navbar navbar-officer">
    <div class="navbar-brand">
      👮 RoadWatch Authority Portal
    </div>
    <div class="navbar-menu">
      <a href="/authority/queue.html">Review Queue</a>
      <span class="officer-info">Officer Mode</span>
      <button id="logout-btn" class="btn-logout">Logout</button>
    </div>
  </nav>
  
  <main class="container">
    <!-- Page-specific content here -->
  </main>
  
  <footer class="footer">
    <p>&copy; 2026 RoadWatch Authority. Confidential.</p>
  </footer>
  
  <script src="/static/js/utils.js"></script>
  <script src="/static/js/auth.js"></script>
  <script src="/static/js/api.js"></script>
  <script src="/static/js/common.js"></script>
  <script src="/static/js/page-specific.js"></script>
</body>
</html>
```

---

## ✅ Checklist for M5 Completion

### Phase 1: Setup & Base
- [ ] Create directory structure (`templates/`, `static/css/`, `static/js/`)
- [ ] Write base.css, layout.css, components.css, responsive.css
- [ ] Write utils.js, auth.js, api.js, common.js
- [ ] Create navbar + footer components
- [ ] Verify app.py serves static files from `/static/`
- [ ] Test basic CSS rendering on mock page

### Phase 2: Citizen Portal
- [ ] Create `/templates/dashboard.html`
  - [ ] Navbar + welcome message
  - [ ] CTA buttons functional
  - [ ] Verify auth on page load
- [ ] Create `/templates/upload.html`
  - [ ] Form with all fields
  - [ ] File validation + preview
  - [ ] POST /api/reports integration
  - [ ] Success message + auto-redirect
- [ ] Create `/templates/reports.html`
  - [ ] GET /api/reports integration
  - [ ] Table rendering
  - [ ] Pagination working
  - [ ] Clickable report IDs
- [ ] Create `/templates/reports/{id}.html`
  - [ ] GET /api/reports/{id} integration
  - [ ] Timeline rendering
  - [ ] Conditional clarification form
  - [ ] Status polling (every 30s)
  - [ ] Auto-refresh visible feedback

### Phase 3: Officer Portal
- [ ] Create `/templates/authority/queue.html`
  - [ ] GET /api/authority/reports integration
  - [ ] Table rendering with media count
  - [ ] Status filter working
  - [ ] Pagination working
  - [ ] Clickable report IDs
- [ ] Create `/templates/authority/case/{id}.html`
  - [ ] Case details + media viewer
  - [ ] Timeline rendering
  - [ ] Three decision buttons functional
  - [ ] POST /api/authority/reports/{id}/decision integration
  - [ ] Success/error handling
  - [ ] Auto-redirect after decision

### Phase 4: Testing & Refinement
- [ ] Test all forms with valid data
- [ ] Test all error paths (400, 401, 403, 404, 409, 500)
- [ ] Test pagination edge cases (first page, last page, out of bounds)
- [ ] Test responsive CSS (768px, 1024px breakpoints)
- [ ] Test status transitions (all state machine paths)
- [ ] Test concurrent operations (two officers, citizen clarifies mid-review)
- [ ] Verify all API calls use correct headers + formats
- [ ] Verify all error messages are user-friendly

### Phase 5: Documentation
- [ ] Update README.md with UI URLs
- [ ] Document local development (Python static file serving)
- [ ] Document demo citizen/officer credentials
- [ ] Add screenshots to ARCHITECTURE-FLOW-DIAGRAMS.md

---

## 🔑 Key Implementation Principles

1. **No Frameworks:** Vanilla HTML/CSS/JS only. Use Fetch API for HTTP.

2. **Responsive by Default:** Mobile-first CSS, test on mobile at 375px width.

3. **Error Handling:** Every API call shows user-friendly errors. No silent failures.

4. **Accessibility:** Semantic HTML, ARIA labels for non-obvious elements, keyboard navigation.

5. **Security:** 
   - Never store tokens in cookies (use localStorage for demo, HttpOnly in production)
   - Sanitize displayed data (citizen IDs, notes from officer)
   - HTTPS only in production

6. **Performance:** 
   - Load shared CSS/JS once
   - Lazy-load images
   - Debounce/throttle rapid API calls (e.g., pagination)

7. **UX Polish:**
   - Loading states (spinners, skeletons)
   - Empty states (friendly messages)
   - Success toasts (green, dismissable)
   - Error modals (red, with retry)
   - Disable buttons during submission
   - Show last-refreshed timestamp

---

## 📞 API Integration Checklist

For **each API endpoint**, verify:

- [ ] Correct HTTP method (GET/POST)
- [ ] Correct URL path
- [ ] Correct request headers (X-Citizen-Id or Authorization)
- [ ] Correct request body (JSON structure)
- [ ] Handle 200/201 response (extract data correctly)
- [ ] Handle 400 (show validation errors)
- [ ] Handle 401 (redirect to login)
- [ ] Handle 403 (show "access denied")
- [ ] Handle 404 (show "not found")
- [ ] Handle 409 (show "invalid action")
- [ ] Handle 500 (show "server error, try again")
- [ ] Show loading state during request
- [ ] Disable buttons during request
- [ ] Log errors to console (for debugging)

