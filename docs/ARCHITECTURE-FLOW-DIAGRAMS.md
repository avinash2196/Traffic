# RoadWatch Architecture & Flow Diagrams

## 1. CITIZEN WORKFLOW — Complete User Journey

```mermaid
flowchart TD
    Start([Citizen Portal Load]) --> CheckAuth{Authenticated?}
    CheckAuth -->|No| Login["🔐 Login with OIDC<br/>(Demo: X-Citizen-Id header)"]
    Login --> Dashboard
    CheckAuth -->|Yes| Dashboard["📊 Dashboard<br/>View Reports"]
    
    Dashboard --> ChooseAction{Action}
    
    ChooseAction -->|New Report| Upload["📸 Upload Report<br/>- Take/Select Photo<br/>- Enter Violation Type<br/>- Enter Location"]
    ChooseAction -->|View Reports| History["📋 Report History<br/>GET /api/reports<br/>(Paginated List)"]
    ChooseAction -->|Check Status| Details["🔍 Report Details<br/>GET /api/reports/{id}<br/>- Status Timeline<br/>- Events Log<br/>- Provisional Points"]
    
    Upload --> Validate{"File Valid?<br/>(JPG/PNG, <25MB<br/>video: <45s)"}
    Validate -->|Invalid| Error1["❌ Show Error<br/>Retry Upload"]
    Error1 --> Upload
    Validate -->|Valid| Submit["📤 Submit Report<br/>POST /api/reports<br/>{violation_type, location, media_id}"]
    
    Submit --> SubmitSuccess["✅ Report Created<br/>Status: submitted<br/>Report ID: {id}"]
    SubmitSuccess --> WaitScreen["⏳ Waiting for<br/>System Screening"]
    WaitScreen --> CheckStatus{"Check Status<br/>Every 30s"}
    CheckStatus -->|submitted| WaitScreen
    CheckStatus -->|screening| WaitScreen
    CheckStatus -->|awaiting-review| AwaitingReview["📌 Awaiting Officer Review"]
    CheckStatus -->|awaiting-citizen-info| ClarifyNeeded["⚠️ Officer Requesting<br/>Clarification"]
    
    ClarifyNeeded --> ClarifyForm["📝 Clarification Form<br/>- Clarification Text<br/>- New Media Upload<br/>POST /api/reports/{id}/clarification"]
    ClarifyForm --> Resubmit["🔄 Resubmitted<br/>Back to Queue"]
    Resubmit --> WaitScreen
    
    CheckStatus -->|approved| Approved["✅ Report Approved!<br/>Provisional Points: {points}<br/>Status: approved"]
    CheckStatus -->|rejected| Rejected["❌ Report Rejected<br/>Reason: {reason}<br/>Status: rejected"]
    CheckStatus -->|resubmitted| WaitScreen
    
    Details --> DetailView["View Full Report:<br/>- Violation Type<br/>- Location<br/>- Status<br/>- Timeline (events)<br/>- Provisional Points<br/>- Officer Notes"]
    DetailView --> Dashboard
    
    Approved --> Exit1(["✓ End: Approved"])
    Rejected --> Exit2(["✓ End: Rejected"])
    History --> Dashboard
```

---

## 2. OFFICER WORKFLOW — Authority Review & Decision

```mermaid
flowchart TD
    Start([Officer Portal Load]) --> CheckAuth{Authenticated?}
    CheckAuth -->|No| Login["🔐 Login with OIDC<br/>(Demo: Authorization header)"]
    Login --> Dashboard
    CheckAuth -->|Yes| Dashboard["📊 Review Queue<br/>GET /api/authority/reports"]
    
    Dashboard --> QueueView["📋 Queue Display<br/>- Paginated (10 per page)<br/>- Status Filter Options<br/>- Created timestamp<br/>- Violation Type"]
    QueueView --> SelectReport["👆 Select Report<br/>from Queue"]
    
    SelectReport --> CaseDetail["🔍 Case Detail View<br/>Report Info:<br/>- Citizen ID<br/>- Violation Type<br/>- Location<br/>- Media Count<br/>- Status<br/>- Events Timeline"]
    
    CaseDetail --> ViewMedia["👀 View Media<br/>GET /api/reports/{id}/media<br/>- Photo/Video Preview<br/>- File Hash<br/>- Technical Screening Result"]
    ViewMedia --> ReadyDecide["✅ Ready to Decide"]
    
    ReadyDecide --> DecisionForm{"Decision:"}
    
    DecisionForm -->|Approve| Approve["✅ Approve Report<br/>POST /api/authority/reports/{id}/decision<br/>{action: 'approve'}<br/>- Status: approved<br/>- Provisional Points: {points}"]
    
    DecisionForm -->|Reject| Reject["❌ Reject Report<br/>POST /api/authority/reports/{id}/decision<br/>{action: 'reject', reason}<br/>- Status: rejected<br/>- Reason: stored in event"]
    
    DecisionForm -->|Request Info| RequestInfo["❓ Request Clarification<br/>POST /api/authority/reports/{id}/decision<br/>{action: 'request-info'}<br/>- Status: awaiting-citizen-info<br/>- Citizen notified"]
    
    Approve --> ApproveSuccess["✅ Decision Recorded<br/>- Provisional Points Awarded<br/>- Event Logged<br/>- Citizen Notified"]
    Reject --> RejectSuccess["✅ Decision Recorded<br/>- Rejection Reason Stored<br/>- Event Logged<br/>- Citizen Notified"]
    RequestInfo --> RequestSuccess["✅ Clarification Requested<br/>- Status Changed<br/>- Event Logged<br/>- Citizen Can Resubmit"]
    
    ApproveSuccess --> BackToQueue["🔄 Back to Queue"]
    RejectSuccess --> BackToQueue
    RequestSuccess --> BackToQueue
    
    BackToQueue --> RefreshQueue["🔄 Refresh Queue<br/>GET /api/authority/reports<br/>(excludes just-decided cases)"]
    RefreshQueue --> QueueView
    
    QueueView --> FilterQueue{"Apply Filter?"}
    FilterQueue -->|By Status| StatusFilter["Filter: awaiting-review<br/>or resubmitted"]
    StatusFilter --> QueueView
    FilterQueue -->|Pagination| PaginateQueue["Next/Prev Page<br/>page={n}, page_size=10"]
    PaginateQueue --> QueueView
    FilterQueue -->|No| QueueView
```

---

## 3. SYSTEM ARCHITECTURE — Components & Data Flow

```mermaid
graph TB
    subgraph Frontend["🖥️ FRONTEND (HTML/CSS/JS)"]
        CitizenUI["👤 Citizen Portal<br/>- Upload Form<br/>- Status Tracker<br/>- Report List<br/>- Clarification Form"]
        OfficerUI["👮 Officer Portal<br/>- Review Queue<br/>- Case Details<br/>- Decision Form<br/>- Media Viewer"]
    end
    
    subgraph API["🔌 FASTAPI BACKEND (Port 8000)"]
        Auth["🔐 Auth Middleware<br/>- X-Citizen-Id (citizen)<br/>- Authorization (officer)"]
        
        CitizenEndpoints["📤 Citizen Endpoints<br/>POST /api/reports<br/>GET /api/reports<br/>GET /api/reports/{id}<br/>POST /api/reports/{id}/clarification"]
        
        OfficerEndpoints["📋 Officer Endpoints<br/>GET /api/authority/reports<br/>POST /api/authority/reports/{id}/decision"]
        
        MediaHandler["🎬 Media Handler<br/>- validate_file()<br/>- compute_hash()<br/>- detect_duplicate()<br/>- screen_technical()<br/>- store_media()"]
    end
    
    subgraph Storage["💾 STORAGE LAYER"]
        DB["🗄️ SQLite Database<br/>- reports (stateful)<br/>- events (append-only)<br/>- media (metadata)"]
        
        FileSystem["📁 Local File System<br/>media/ folder<br/>- Original files<br/>- Hashes for dedup<br/>- Technical scores"]
    end
    
    subgraph Future["🚀 FUTURE (Phase 2+)"]
        OIDC["🔑 OIDC Identity<br/>(Azure Entra, Okta)"]
        AI["🤖 AI Screening<br/>(OpenAI GPT-4V)<br/>- Content check<br/>- Blur/quality"]
        Export["📦 Evidence Export<br/>(ZIP + Timeline)"]
        Analytics["📊 Analytics<br/>(Telemetry)"]
    end
    
    CitizenUI -->|HTTP| Auth
    OfficerUI -->|HTTP| Auth
    Auth -->|Route| CitizenEndpoints
    Auth -->|Route| OfficerEndpoints
    
    CitizenEndpoints -->|Manage Reports| DB
    CitizenEndpoints -->|Handle Media| MediaHandler
    OfficerEndpoints -->|Query Reports| DB
    OfficerEndpoints -->|Record Decisions| DB
    
    MediaHandler -->|Store Files| FileSystem
    MediaHandler -->|Query Status| DB
    
    DB -->|Read Reports| OfficerUI
    DB -->|Read History| CitizenUI
    FileSystem -->|Serve Media| OfficerUI
    FileSystem -->|Download Media| CitizenUI
    
    OfficerEndpoints -.->|Phase 2| AI
    CitizenEndpoints -.->|Phase 2| OIDC
    OfficerEndpoints -.->|Phase 2| Export
    Backend -.->|Phase 2| Analytics
```

---

## 4. DATA MODEL — Report Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> submitted: 1. Citizen submits report<br/>POST /api/reports
    
    submitted --> screening: System processes<br/>(Optional: AI screening)
    
    screening --> awaiting-review: Ready for officer
    
    awaiting-review --> approved: 2a. Officer approves<br/>POST decision {approve}
    awaiting-review --> rejected: 2b. Officer rejects<br/>POST decision {reject}
    awaiting-review --> awaiting-citizen-info: 2c. Officer requests info<br/>POST decision {request-info}
    
    awaiting-citizen-info --> resubmitted: Citizen responds<br/>POST /api/reports/{id}/clarification
    
    resubmitted --> awaiting-review: Back in queue<br/>for re-review
    
    approved --> [*]: ✅ FINAL: Provisional points awarded
    rejected --> [*]: ❌ FINAL: Rejected, citizen can appeal
    
    note right of awaiting-review
        Officer sees: reports with status
        IN (awaiting-review, resubmitted)
        Sorted by created_at (FIFO)
    end note
```

---

## 5. API INTEGRATION MAP — Frontend to Backend

### **CITIZEN PORTAL API CALLS**

```mermaid
graph LR
    subgraph Citizen["👤 CITIZEN UI"]
        Upload["📸 Upload Form<br/>- Violation Type dropdown<br/>- Location text<br/>- File input"]
        History["📋 Report List<br/>- Click to load"]
        Details["🔍 Report Details<br/>- Status timeline<br/>- Events list"]
        Clarify["📝 Clarification Form<br/>- Text input<br/>- New media"]
    end
    
    subgraph API["🔌 API ENDPOINTS"]
        PostReport["POST /api/reports<br/>Request:<br/>  - violation_type<br/>  - location<br/>  - media_id<br/>Response:<br/>  - report_id<br/>  - status<br/>  - created_at"]
        
        GetReports["GET /api/reports<br/>Query: (optional)<br/>  - page (default 1)<br/>  - page_size (default 10)<br/>Response:<br/>  - reports: []<br/>  - total_count<br/>  - total_pages"]
        
        GetDetail["GET /api/reports/{id}<br/>Response:<br/>  - id, citizen_id<br/>  - violation_type<br/>  - status<br/>  - provisional_points<br/>  - timeline: []"]
        
        PostClarify["POST /api/reports/{id}/clarification<br/>Request:<br/>  - clarification_text<br/>  - new_media_id<br/>Response:<br/>  - status: resubmitted<br/>  - clarification_event"]
    end
    
    Upload -->|Submit| PostReport
    History -->|Load| GetReports
    Details -->|View| GetDetail
    Clarify -->|Submit| PostClarify
    
    GetReports -->|Poll every 30s| GetReports
```

### **OFFICER PORTAL API CALLS**

```mermaid
graph LR
    subgraph Officer["👮 OFFICER UI"]
        Queue["📋 Review Queue<br/>- List reports<br/>- Pagination<br/>- Status filter"]
        CaseView["🔍 Case Details<br/>- Report info<br/>- Media preview<br/>- Timeline"]
        Decision["⚙️ Decision Form<br/>- Approve button<br/>- Reject button<br/>- Request Info button"]
    end
    
    subgraph API["🔌 API ENDPOINTS"]
        GetQueue["GET /api/authority/reports<br/>Query:<br/>  - page (default 1)<br/>  - page_size (default 10)<br/>  - status (filter)<br/>Response:<br/>  - reports: []<br/>  - total_count<br/>  - total_pages<br/>  - media_count per report"]
        
        PostDecision["POST /api/authority/reports/{id}/decision<br/>Request (one of):<br/>  {action: approve}<br/>  {action: reject, reason}<br/>  {action: request-info}<br/>Response:<br/>  - status<br/>  - provisional_points (if approved)<br/>  - decision_event"]
    end
    
    Queue -->|Load| GetQueue
    Queue -->|Filter/Paginate| GetQueue
    CaseView -->|Click report| GetQueue
    Decision -->|Submit| PostDecision
    PostDecision -->|Refresh| GetQueue
```

---

## 6. DATABASE SCHEMA — Quick Reference

```mermaid
erDiagram
    REPORTS ||--o{ EVENTS : has
    REPORTS ||--o{ MEDIA : has
    
    REPORTS {
        string id PK
        string citizen_id FK
        string violation_type
        string location
        string status
        int provisional_points
        string created_at
        string updated_at
        string screening_notes "nullable"
        string officer_notes "nullable"
    }
    
    EVENTS {
        string id PK
        string report_id FK
        string event_type
        string actor "citizen/system/officer"
        string old_status "nullable"
        string new_status
        int provisional_points "nullable"
        string reason "nullable"
        string created_at
    }
    
    MEDIA {
        string id PK
        string report_id FK
        string filename
        string mime_type
        int file_size
        string file_hash "SHA-256"
        float technical_score "0.0-1.0"
        string storage_path
        string created_at
    }
```

---

## 7. UI PAGE LAYOUT MAP

```
CITIZEN PORTAL
├── /dashboard (default)
│   ├── Welcome message
│   ├── [+ New Report] button
│   └── Recent reports summary
│
├── /upload
│   ├── Violation Type dropdown
│   ├── Location input
│   ├── File upload widget
│   ├── Submit button
│   └── [View My Reports] link
│
├── /reports (list)
│   ├── Search/filter bar
│   ├── Report table:
│   │   ├── Report ID (clickable)
│   │   ├── Violation Type
│   │   ├── Status badge
│   │   ├── Created date
│   │   └── Action (view)
│   ├── Pagination controls
│   └── [+ New Report] button
│
└── /reports/{id}
    ├── Report header (ID, status, points)
    ├── Report details
    │   ├── Violation Type
    │   ├── Location
    │   ├── Media count
    │   └── Created timestamp
    ├── Timeline/Events section
    │   └── Event cards (status changes, officer actions)
    ├── Conditional sections:
    │   ├── [Clarification Form] if status=awaiting-citizen-info
    │   └── [Final Verdict] if status=approved/rejected
    └── [Back] link

OFFICER PORTAL
├── /queue (default)
│   ├── Status filter (awaiting-review, resubmitted)
│   ├── Report table:
│   │   ├── Report ID (clickable)
│   │   ├── Citizen ID (masked)
│   │   ├── Violation Type
│   │   ├── Location
│   │   ├── Status
│   │   ├── Media count
│   │   └── Submitted time
│   ├── Pagination (page/page_size)
│   └── [Refresh] button
│
└── /queue/{id} (case detail)
    ├── Case header
    │   ├── Report ID
    │   ├── Status badge
    │   ├── Violation Type
    │   └── Media count
    ├── Report Details
    │   ├── Citizen ID (masked)
    │   ├── Location
    │   ├── Created timestamp
    │   └── Description (if any)
    ├── Media Section
    │   ├── Photo/video viewer
    │   ├── File hash (for audit)
    │   └── Technical score (if screened)
    ├── Timeline/Events
    │   └── All events (citizen uploads, status changes, etc.)
    ├── Decision Section
    │   ├── [✅ Approve] button
    │   ├── [❌ Reject] + reason field
    │   └── [❓ Request Info] button
    └── [Back to Queue] link
```

---

## 8. HEADER DEFINITIONS & AUTHENTICATION

### **Request Headers Required**

| Endpoint | Auth Header | Example |
|---|---|---|
| `POST /api/reports` | `X-Citizen-Id` | `X-Citizen-Id: citizen-abc123xyz` |
| `GET /api/reports` | `X-Citizen-Id` | `X-Citizen-Id: citizen-abc123xyz` |
| `GET /api/reports/{id}` | `X-Citizen-Id` | `X-Citizen-Id: citizen-abc123xyz` |
| `POST /api/reports/{id}/clarification` | `X-Citizen-Id` | `X-Citizen-Id: citizen-abc123xyz` |
| `GET /api/authority/reports` | `Authorization` | `Authorization: Bearer demo-token` |
| `POST /api/authority/reports/{id}/decision` | `Authorization` | `Authorization: Bearer demo-token` |

### **Response Status Codes**

| Status | Meaning | Example |
|---|---|---|
| `200 OK` | Success (GET, POST decision) | Officer approves report |
| `201 Created` | Resource created | Report submitted |
| `400 Bad Request` | Invalid input | Missing violation_type |
| `401 Unauthorized` | Missing auth header | No X-Citizen-Id |
| `403 Forbidden` | Access denied | Citizen views other's report |
| `404 Not Found` | Report doesn't exist | GET /api/reports/invalid-id |
| `409 Conflict` | Invalid status transition | Approve already-approved report |
| `500 Server Error` | Backend error | Database error |

---

## 9. POLLING & REAL-TIME UPDATE STRATEGY

```mermaid
sequenceDiagram
    actor Citizen
    participant UI as Citizen UI
    participant API as FastAPI Backend
    participant DB as Database
    
    Citizen->>UI: 1. Submit Report
    UI->>API: POST /api/reports
    API->>DB: INSERT INTO reports (status=submitted)
    DB-->>API: OK
    API-->>UI: 201 {report_id, status}
    UI->>Citizen: ✅ Report created!
    
    Note over UI: Start polling loop
    loop Every 30 seconds
        UI->>API: GET /api/reports/{id}
        API->>DB: SELECT status FROM reports
        DB-->>API: {status}
        API-->>UI: 200 {status, timeline}
        alt Status changed
            UI->>Citizen: 🔄 Status updated to: screening
        else Status unchanged
            Note over UI: Wait 30s, poll again
        end
    end
    
    Note over DB: Officer reviews (in parallel)
    UI->>API: GET /api/reports/{id}
    API-->>UI: {status: awaiting-review}
    
    UI->>Citizen: ⏳ Officer is reviewing...
    
    Note over DB: Officer approves
    UI->>API: GET /api/reports/{id}
    API-->>UI: {status: approved, provisional_points: 2}
    UI->>Citizen: ✅ Approved! Points: 2
    
    Note over UI: Stop polling loop
```

---

## 10. ERROR HANDLING & VALIDATION FLOW

```mermaid
flowchart TD
    Request["📨 Incoming Request"]
    
    Request --> AuthCheck{"Auth Header<br/>Present?"}
    AuthCheck -->|No| Auth401["❌ 401 Unauthorized<br/>Missing X-Citizen-Id or Authorization"]
    Auth401 --> ErrorResponse["Return JSON:<br/>{error, code}"]
    
    AuthCheck -->|Yes| RouteCheck{"Route<br/>Exists?"}
    RouteCheck -->|No| Route404["❌ 404 Not Found"]
    Route404 --> ErrorResponse
    
    RouteCheck -->|Yes| ValidateInput{"Input<br/>Valid?"}
    ValidateInput -->|No| Validate400["❌ 400 Bad Request<br/>Missing/invalid fields"]
    Validate400 --> ErrorResponse
    
    ValidateInput -->|Yes| CheckAccess{"Access<br/>Allowed?"}
    CheckAccess -->|No| Access403["❌ 403 Forbidden<br/>Citizen viewing other's report"]
    Access403 --> ErrorResponse
    
    CheckAccess -->|Yes| CheckStatus{"Status<br/>Transition<br/>Valid?"}
    CheckStatus -->|No| Status409["❌ 409 Conflict<br/>Invalid status for action"]
    Status409 --> ErrorResponse
    
    CheckStatus -->|Yes| Execute["✅ Execute Business Logic"]
    Execute --> DB["💾 Database Operation"]
    DB --> Success["✅ 200/201 OK<br/>Return Result"]
    
    DB -.->|Error| DBError["❌ 500 Server Error<br/>Database failure"]
    DBError --> ErrorResponse
    
    ErrorResponse --> LogError["📝 Log Error:<br/>timestamp, endpoint, error"]
    LogError --> Client["Return to Client"]
    Success --> Client
```

---

## 11. VIOLATION TYPES & POINTS MAPPING

```mermaid
graph LR
    subgraph Violations["🚗 Violation Types"]
        Helmet["🪖 helmet"]
        Triple["👥 triple-riding"]
        RedLight["🚦 red-light"]
    end
    
    subgraph Points["⭐ Provisional Points"]
        P2["2 points"]
        P3["3 points"]
        P3b["3 points"]
    end
    
    Helmet -->|No decay, no location adjustment| P2
    Triple -->|No escalation in MVP| P3
    RedLight -->|No time-of-day adjustment| P3b
    
    Note over Points
        Phase 1 (MVP): Fixed points
        Phase 2: Add decay (after N days)
        Phase 3: Add location multipliers
        Future: Escalation system
    end
```

