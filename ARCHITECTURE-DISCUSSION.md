# RoadWatch Architecture Refactoring - Design Discussion

**Date:** November 14, 2026  
**Status:** ARCHITECTURE DESIGN PHASE (Pre-Implementation)

---

## 1. CURRENT STATE (Problems We're Facing)

### Current Monolithic Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     app.py (1349 lines)                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ - Citizen report endpoints                           │  │
│  │ - Officer review endpoints                           │  │
│  │ - Media upload/download                              │  │
│  │ - Authentication (demo mode)                         │  │
│  │ - Database operations (SQLite)                       │  │
│  │ - Frontend static file serving                       │  │
│  │ - Serves BOTH citizen & officer UIs                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
    AI Gateway          SQLite DB          Frontend HTML
    (9999)            (shared)          (citizen+officer)
```

### Problems with Current Approach

1. **Cascading Failures**
   - Fix in citizen logic breaks officer flow
   - Changes to media handling affect both UIs
   - Example: Login page regression when fixing reports page

2. **Mixed Concerns**
   - 1349 lines of code doing 6 different jobs
   - Citizen-specific logic mixed with officer-specific logic
   - Hard to test one feature without loading entire app

3. **Scaling Issues**
   - Can't run 2 instances of "citizen service" while keeping 1 officer service
   - All users compete for same resources
   - No way to deploy fixes for citizen without restarting officer service

4. **Debugging Difficulty**
   - Single log stream for all operations
   - Hard to trace which code path caused which issue
   - Auth check running for all routes regardless of role

5. **Frontend Brittleness**
   - Single HTML page structure tries to serve both roles
   - CSS/JS logic contains role-switching (if citizen show X, if officer show Y)
   - One auth redirect loop in shared code affects both user types

---

## 2. PROPOSED ARCHITECTURE

### High-Level Structure
```
┌──────────────────────────────────────────────────────────────────┐
│                        ROADWATCH MVP                              │
└──────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────┐    ┌──────────────────────────┐
│   CITIZEN FRONTEND (Port 3000)  │    │  OFFICER FRONTEND (3001) │
│  - Citizen dashboard            │    │  - Officer queue         │
│  - Report submission            │    │  - Case review           │
│  - Report status tracking       │    │  - Decision making       │
│  - Evidence upload/view         │    │  - Assessment view       │
└──────────────┬──────────────────┘    └─────────────┬────────────┘
               │                                     │
               └─────────────────┬───────────────────┘
                                 │
               ┌─────────────────┴────────────────┐
               │   API Gateway (Port 8000)       │
               │   - Route citizen → citizen-api │
               │   - Route officer → officer-api │
               │   - Rate limiting               │
               │   - Logging/Monitoring          │
               └────────────┬────────────────────┘
                            │
        ┌───────────────────┼───────────────────┬──────────────────┐
        │                   │                   │                  │
        ▼                   ▼                   ▼                  ▼
   ┌─────────┐         ┌─────────┐        ┌──────────┐      ┌──────────┐
   │ Citizen │         │ Officer │        │ Auth     │      │   AI     │
   │ API     │         │ API     │        │ Service  │      │ Gateway  │
   │(8001)   │         │(8002)   │        │(8003)    │      │ (9999)   │
   └────┬────┘         └────┬────┘        └────┬─────┘      └────┬─────┘
        │                   │                  │                  │
        │ - Report CRUD     │ - Queue CRUD    │ - Token valid   │ - Image
        │ - Media upload    │ - Decision      │ - User lookup   │   analysis
        │ - Status check    │   submission    │ - Session mgmt  │ - Scoring
        │ - Statistics      │ - Assessment    │                 │ - Recom-
        │                   │   view          │                 │   mendations
        │
        └───────────────────┼───────────────────┬──────────────────┘
                            │                   │
                            ▼                   ▼
                      ┌─────────────────┐  ┌──────────────┐
                      │   SQLite DB     │  │ Media Store  │
                      │  roadwatch.db   │  │  /media_store│
                      └─────────────────┘  └──────────────┘
```

### Component Breakdown

#### **Frontend Layer**

**Citizen Frontend (citizen-app/)**
- Single Page App for citizen users only
- Pages:
  - Login/Signup
  - Dashboard (stats, quick actions)
  - Report submission (form + media upload)
  - My Reports (list with status)
  - Report detail (evidence view + timeline)
- Tech: HTML/CSS/JS (static or Vue.js)
- Calls: `/api/citizen/*` endpoints only
- Auth: X-Citizen-Id header (or JWT in future)

**Officer Frontend (officer-app/)**
- Single Page App for officer/reviewer users only
- Pages:
  - Login
  - Queue (pending reports)
  - Case detail (evidence + decision form)
  - History (past cases)
  - Statistics (dashboard)
- Tech: HTML/CSS/JS (static or Vue.js)
- Calls: `/api/officer/*` endpoints only
- Auth: X-Reviewer-Token header (or JWT in future)

**Benefits:**
- ✅ No role-switching logic in frontend
- ✅ Separate CSS/JS (no bloat)
- ✅ Can be deployed independently
- ✅ Cleaner UX (no conditional UI)
- ✅ Different design for different users

---

#### **Backend Layer - Microservices**

**1. Citizen API (Port 8001)**
```
GET  /api/citizen/reports          → Get user's reports
POST /api/citizen/reports          → Create new report
GET  /api/citizen/reports/{id}     → Get report detail
POST /api/citizen/media/upload     → Upload evidence

Depends on:
  - Auth Service (validate X-Citizen-Id)
  - Database (read/write reports)
  - Media Store (upload/access)
```

**2. Officer API (Port 8002)**
```
GET  /api/officer/queue            → Get pending reports
GET  /api/officer/queue/{id}       → Get case detail
POST /api/officer/queue/{id}/decide → Submit decision
GET  /api/officer/stats            → Get dashboard stats

Depends on:
  - Auth Service (validate X-Reviewer-Token)
  - AI Gateway (get assessment)
  - Database (read reports, write decisions)
```

**3. Auth Service (Port 8003)**
```
POST /auth/validate-citizen        → Validate citizen token
POST /auth/validate-officer        → Validate officer token
POST /auth/generate-token          → Generate new token

Stores:
  - Valid tokens
  - User mappings
  - Sessions (if needed)
```

**4. AI Gateway (Port 9999)** ← Already exists
```
POST /api/assess                   → Send image for assessment
GET  /api/assess/{job_id}         → Get assessment result

Calls:
  - OpenAI API
  - Gemini API
  - Returns: recommendation, confidence, violation type
```

**5. API Gateway (Port 8000)** ← NEW
```
Routes requests to appropriate backend:
  GET /citizen/* → routes to http://citizen-api:8001/api/citizen/*
  GET /officer/* → routes to http://officer-api:8002/api/officer/*
  
Features:
  - Authentication enforcement
  - Rate limiting
  - Logging
  - Error handling
  - CORS management
```

**6. Media Service** (Optional, can be part of backends initially)
```
POST /media/upload     → Upload evidence file
GET  /media/{id}       → Download evidence
DELETE /media/{id}     → Delete evidence

Storage:
  - Local filesystem (/media_store)
  - Checksum validation
  - Access control checks
```

---

## 3. DATA FLOW EXAMPLES

### Citizen Submitting Report
```
1. Citizen enters report form in citizen-app (Port 3000)
2. Form submission:
   POST /api/citizen/reports
   Header: X-Citizen-Id: citizen-123
   Body: {violation_type, vehicle_number, location, media_id}

3. API Gateway (8000) receives:
   - Validates request is from /citizen/* endpoint
   - Routes to Citizen API (8001)

4. Citizen API (8001):
   - Calls Auth Service (8003): "Is citizen-123 valid?"
   - Calls Database: Store report
   - Returns: {report_id, status: "pending"}

5. Frontend shows: "Report submitted! ID: REP-123"

6. (Async) AI Gateway (9999) processes media:
   - Calls OpenAI/Gemini
   - Gets recommendation
   - Updates report with AI assessment

7. Citizen views report:
   - Sees status: "PENDING REVIEW"
   - Sees AI recommendation (if available)
```

### Officer Reviewing Report
```
1. Officer logs in to officer-app (Port 3001)
2. Officer visits queue page

3. Frontend calls:
   GET /api/officer/queue
   Header: X-Reviewer-Token: token-xyz

4. API Gateway (8000) routes to Officer API (8002)

5. Officer API (8002):
   - Calls Auth Service: "Is token-xyz valid?"
   - Calls Database: Get all pending reports
   - For each report, calls AI Gateway: "What's the assessment?"
   - Returns: [{report_id, vehicle, violation, ai_status, ...}, ...]

6. Officer sees queue with AI recommendations

7. Officer clicks "Review" for report REP-123

8. Frontend calls:
   GET /api/officer/queue/REP-123
   - Gets full case details
   - Gets evidence URLs (from Media Service)
   - Gets AI assessment

9. Officer fills decision form:
   POST /api/officer/queue/REP-123/decide
   Body: {decision: "approved", points: 2, comments: "Clear violation"}

10. Officer API (8002):
    - Validates decision
    - Calls Database: Update report with decision
    - Calls Database: Create event log
    - Returns: {status: "success"}

11. Frontend shows: "Decision recorded"
```

---

## 4. DATA CONSISTENCY & SHARING

### Shared Data (Single SQLite)
```
Tables accessed by multiple services:
  - reports (citizen-api writes, officer-api reads+writes)
  - events (all services read, citizen-api & officer-api write)
  - media_metadata (citizen-api writes, officer-api reads)
  - ai_assessments (AI gateway writes, officer-api reads)

Approach:
  ✅ Keep SQLite shared (simple for MVP)
  ✅ Use transactions for consistency
  ✅ Add table-level locks if needed
  ⚠️  Future: Move to PostgreSQL with proper isolation
```

### Isolation Levels
```
Citizen API:
  - Can only read/write citizen_id's own reports
  - Cannot see other citizens' data
  - Cannot write decisions or assessments

Officer API:
  - Can read all reports
  - Can write decisions on any report
  - Can see AI assessments

AI Gateway:
  - Read-only access to media
  - Write-only access to assessments
```

---

## 5. DEPLOYMENT & OPERATIONS

### Local Development (Current Approach)
```bash
# Terminal 1: Citizen Frontend
cd citizen-app && npm start  # Port 3000

# Terminal 2: Officer Frontend  
cd officer-app && npm start  # Port 3001

# Terminal 3: API Gateway
python api_gateway.py        # Port 8000

# Terminal 4: Citizen API
cd services/citizen-api && python app.py  # Port 8001

# Terminal 5: Officer API
cd services/officer-api && python app.py  # Port 8002

# Terminal 6: Auth Service
cd services/auth && python app.py         # Port 8003

# Terminal 7: AI Gateway
python ai_gateway_mvp.py               # Port 9999
```

### Docker Compose (Production)
```yaml
version: '3.8'
services:
  citizen-app:
    build: ./citizen-app
    ports: ["3000:80"]
    
  officer-app:
    build: ./officer-app
    ports: ["3001:80"]
    
  api-gateway:
    build: ./services/api-gateway
    ports: ["8000:8000"]
    environment:
      - CITIZEN_API_URL=http://citizen-api:8001
      - OFFICER_API_URL=http://officer-api:8002
      
  citizen-api:
    build: ./services/citizen-api
    ports: ["8001:8001"]
    environment:
      - DATABASE_URL=sqlite:///roadwatch.db
      - AUTH_SERVICE_URL=http://auth-service:8003
      
  officer-api:
    build: ./services/officer-api
    ports: ["8002:8002"]
    environment:
      - DATABASE_URL=sqlite:///roadwatch.db
      - AUTH_SERVICE_URL=http://auth-service:8003
      - AI_GATEWAY_URL=http://ai-gateway:9999
      
  auth-service:
    build: ./services/auth
    ports: ["8003:8003"]
    environment:
      - DATABASE_URL=sqlite:///roadwatch.db
      
  ai-gateway:
    build: ./services/ai-gateway
    ports: ["9999:9999"]
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./media_store:/app/media_store
      
  db:
    image: sqlite:latest
    volumes:
      - ./data:/data
```

---

## 6. IMPLEMENTATION PHASES

### Phase 1: Extract & Refactor (Week 1)
```
1. [ ] Create directory structure
    /citizen-app          (new)
    /officer-app          (new)
    /services/
        /citizen-api      (extract from app.py)
        /officer-api      (extract from app.py)
        /auth             (extract from app.py)
        /api-gateway      (new)

2. [ ] Extract routes from app.py
    - Citizen routes → citizen-api/app.py
    - Officer routes → officer-api/app.py
    - Auth logic → auth/app.py

3. [ ] Split frontends
    - Duplicate templates/ → citizen-app/
    - Duplicate templates/ → officer-app/
    - Remove role-switching logic
    - Remove unused pages

4. [ ] Create shared library
    - database.py (shared connection)
    - models.py (shared schemas)
    - auth_utils.py (shared validation)
```

### Phase 2: Service Communication (Week 2)
```
1. [ ] Create API Gateway
    - Route citizen requests to citizen-api
    - Route officer requests to officer-api
    - Handle auth header validation

2. [ ] Update citizen-api
    - Add calls to auth-service for token validation
    - Add calls to AI gateway for assessments

3. [ ] Update officer-api
    - Add calls to auth-service
    - Add calls to AI gateway
    - Add queue management logic

4. [ ] Create Auth Service
    - Token validation endpoints
    - User lookup (if needed)
```

### Phase 3: Testing & Verification (Week 3)
```
1. [ ] Unit tests for each service
    - Test citizen-api in isolation
    - Test officer-api in isolation
    - Mock external service calls

2. [ ] Integration tests
    - Test citizen → api-gateway → citizen-api
    - Test officer → api-gateway → officer-api
    - Test inter-service communication

3. [ ] E2E tests
    - Full citizen workflow
    - Full officer workflow
    - AI assessment flow

4. [ ] Load testing
    - Test independent scaling
    - Verify no cross-contamination
```

### Phase 4: Deployment & Documentation (Week 4)
```
1. [ ] Docker setup
    - Dockerfile for each service
    - docker-compose.yml
    - .env.example with all services

2. [ ] Deployment scripts
    - start-all-services.sh (local dev)
    - deploy-to-cloud.sh (production)

3. [ ] Documentation
    - Architecture guide
    - API documentation
    - Deployment guide
    - Troubleshooting guide
```

---

## 7. BENEFITS & TRADE-OFFS

### Benefits ✅

| Aspect | Benefit |
|--------|---------|
| **Isolation** | Fix citizen bugs without affecting officer flow |
| **Scaling** | Run 3 citizen APIs + 1 officer API if needed |
| **Testing** | Test citizen API without loading officer logic |
| **Debugging** | Clear log separation by service |
| **Deployment** | Deploy citizen changes without restarting officer |
| **Ownership** | Team A owns citizen, Team B owns officer |
| **UX** | Cleaner UI (no role-switching logic) |
| **Maintenance** | Smaller codebases are easier to understand |
| **Performance** | Lighter frontend (no unused code) |
| **Future-proof** | Easy to add new roles (e.g., admin dashboard) |

### Trade-Offs ⚠️

| Trade-Off | Impact | Mitigation |
|-----------|--------|-----------|
| **More services to manage** | Operational complexity | Docker Compose handles this |
| **Inter-service latency** | Network calls slower than function calls | Caching + optimization |
| **Debugging distributed issues** | Harder to trace across services | Centralized logging (ELK stack) |
| **Database consistency** | Shared SQLite has limits | Add proper indexing + transactions |
| **Deployment complexity** | Need to update multiple services | CI/CD pipeline automates this |

---

## 8. CURRENT STATE vs PROPOSED

### Current (Monolith)
```
app.py (1349 lines)
  ├─ Citizen Routes (30% of code)
  ├─ Officer Routes (30% of code)
  ├─ Auth Logic (10% of code)
  ├─ Media Logic (15% of code)
  ├─ Database Operations (15% of code)
  └─ Frontend Serving (mixed everywhere)

Problems:
  ❌ All services restart if one part breaks
  ❌ Hard to test independently
  ❌ Cascading failures (every fix breaks something)
  ❌ Single log stream for everything
  ❌ Can't scale individual features
  ❌ Citizen and officer logic intertwined
```

### Proposed (Microservices + Separate Frontends)
```
citizen-app/              → citizen-frontend (port 3000)
officer-app/              → officer-frontend (port 3001)
services/
  ├─ api-gateway/         → router (port 8000)
  ├─ citizen-api/         → citizen service (port 8001)
  ├─ officer-api/         → officer service (port 8002)
  ├─ auth/                → auth service (port 8003)
  └─ ai-gateway/          → AI service (port 9999)

Benefits:
  ✅ Services run independently
  ✅ Test each in isolation
  ✅ Fix citizen without affecting officer
  ✅ Separate logs for debugging
  ✅ Scale individual features
  ✅ Clean separation of concerns
```

---

## 9. QUESTIONS FOR DISCUSSION

1. **Frontend Technology**
   - Keep as static HTML (faster startup)?
   - Or use Vue.js/React (more maintainable)?

2. **Database**
   - Keep SQLite (simple, works for MVP)?
   - Or move to PostgreSQL (more robust, multi-service ready)?

3. **Authentication**
   - Keep demo mode (X-Citizen-Id header)?
   - Or implement JWT tokens (more realistic)?

4. **API Gateway**
   - Build custom (using FastAPI)?
   - Or use existing tool (nginx, Kong)?

5. **Deployment**
   - Local dev only (manual terminal windows)?
   - Docker Compose for consistency?
   - Cloud deployment (AWS ECS, GCP Cloud Run)?

6. **Priority**
   - Phase 1: Just get services running separately?
   - Phase 1+2: Get services communicating?
   - Full: Do all 4 phases?

---

## 10. NEXT STEPS

**To proceed, we need decisions on:**

1. ✅/❌ Do we agree this architecture is better?
2. ✅/❌ Should we split frontends (citizen vs officer)?
3. ✅/❌ Should we create separate backend services?
4. ⚠️  What's the timeline? (How much effort can we spend?)
5. ⚠️  What are the dependencies? (Do we need to maintain backward compatibility?)
6. ⚠️  What's the risk tolerance? (Can we break things during refactoring?)

---

## 11. RISK ASSESSMENT

**High Risk:**
- ❌ Current monolith continues → more cascading failures
- ❌ Quick patches without architecture → technical debt increases

**Medium Risk:**
- ⚠️  Refactoring during active development → coordination needed

**Low Risk:**
- ✅ Planned architecture with clear phases → manageable scope
- ✅ Test-driven refactoring → catch issues early
- ✅ Parallel development → can keep old system working while building new

---

**Status:** Awaiting your feedback on architecture direction and implementation approach.

Would you like to:
1. **Discuss any specific component** (auth, API gateway, frontend split)?
2. **Refine the implementation phases** (timeline, priority)?
3. **Answer the decision questions** above?
4. **Start Phase 1** (extraction and refactoring)?
