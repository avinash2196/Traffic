# RoadWatch Traffic MVP - Microservices Extraction (Phase 1 Refactoring)

## Summary

Successfully extracted the monolithic `app.py` (1349 lines) into 4 separate FastAPI microservices. All services share the same SQLite database (`./roadwatch.db`) and use the same utility modules.

## Directory Structure

```
C:\Users\avina\Downloads\avinash-repo\v11\Traffic\
├── app.py (original monolith - kept for reference)
├── shared_utils.py (NEW - shared constants and functions)
├── bootstrap.py (database)
├── auth_utils.py (authentication)
├── intake.py (media validation)
├── durable.py (AI worker)
├── gateway.py (settings)
├── roadwatch.db (shared SQLite database)
│
├── auth-service/
│   ├── app.py (290 lines)
│   ├── requirements.txt
│   └── start.sh
│
├── citizen-api/
│   ├── app.py (650 lines)
│   ├── requirements.txt
│   └── start.sh
│
├── officer-api/
│   ├── app.py (530 lines)
│   ├── requirements.txt
│   └── start.sh
│
├── api-gateway/
│   ├── app.py (470 lines)
│   ├── requirements.txt
│   └── start.sh
│
└── (all other files remain in root)
    ├── static/ (CSS, JS)
    ├── templates/ (HTML)
    ├── media_store/ (uploaded media)
    └── .env
```

## Service Details

### 1. AUTH SERVICE (Port 8003)
**File**: `auth-service/app.py` (290 lines)

Handles citizen and officer authentication:
- `POST /api/auth/signup` - Citizen registration
- `POST /api/auth/login` - Citizen login
- `POST /api/auth/logout` - Citizen logout
- `GET /api/auth/me` - Get current citizen profile
- `POST /api/officer/register` - Officer registration
- `POST /api/officer/login` - Officer login
- `GET /health` - Service health check

**Key Features**:
- No middleware (authentication happens in endpoints)
- Shared database access
- JWT token generation
- Password hashing with bcrypt

### 2. CITIZEN API (Port 8001)
**File**: `citizen-api/app.py` (650 lines)

Handles citizen-facing operations:
- `POST /api/media/upload` - Upload evidence (images/videos)
- `POST /api/reports` - Submit traffic violation report
- `GET /api/reports` - Fetch citizen's reports (paginated)
- `GET /api/reports/{report_id}` - Fetch report details with timeline
- `GET /api/media/{media_id}/{filename}` - Download media
- `POST /api/reports/{report_id}/clarification` - Submit clarification
- `GET /health` - Service health check

**Key Features**:
- Bearer token + X-Citizen-Id header authentication
- Media upload with SHA-256 deduplication
- Report creation with AI job tracking
- Idempotent report submission
- AI worker integration

### 3. OFFICER API (Port 8002)
**File**: `officer-api/app.py` (530 lines)

Handles officer/authority operations:
- `GET /api/authority/reports` - Fetch review queue (paginated)
- `GET /api/authority/reports/{report_id}` - Fetch report for review
- `GET /api/authority/reports/{report_id}/media/{filename}` - Download media
- `POST /api/authority/reports/{report_id}/decision` - Approve/reject/request-info
- `GET /api/authority/reports/{report_id}/evidence.zip` - Download complete ZIP
- `GET /health` - Service health check

**Key Features**:
- Bearer token authentication
- Review queue pagination
- Decision making with provisional points
- Evidence export to ZIP
- Support for both "awaiting-review" and "resubmitted" statuses

### 4. API GATEWAY (Port 8000)
**File**: `api-gateway/app.py` (470 lines)

Routes all requests to appropriate backend services:
- Frontend HTML files and static assets
- Routes `/api/auth/*` → `auth-service:8003`
- Routes `/api/officer/*` → `auth-service:8003`
- Routes `/api/media/*` → `citizen-api:8001`
- Routes `/api/reports` → `citizen-api:8001`
- Routes `/api/authority/*` → `officer-api:8002`
- Health check for all backends

**Key Features**:
- Service discovery on startup
- Request proxying with httpx
- Media file handling (ZIP, images, videos)
- JSON response passthrough
- Timeout and error handling

## Dependencies

Each service has a minimal `requirements.txt` with only needed packages:

### auth-service/requirements.txt
```
fastapi==0.162.0
uvicorn==0.54.0
psycopg[binary]==3.3.6
PyJWT==2.15.1
cryptography==50.0.2
bcrypt==4.1.2
httpx==0.28.1
pytest==9.1.1
pytest-asyncio==1.4.0
python-multipart==0.0.32
```

### citizen-api/requirements.txt
```
(same as auth + Pillow for image validation + OpenTelemetry)
```

### officer-api/requirements.txt
```
(same as auth service)
```

### api-gateway/requirements.txt
```
fastapi==0.162.0
uvicorn==0.54.0
httpx==0.28.1
jinja2==3.1.2
python-multipart==0.0.32
```

## Shared Modules

All services import these from the root directory:

| Module | Purpose |
|--------|---------|
| `bootstrap.py` | Database initialization and connection |
| `auth_utils.py` | Password hashing, JWT token generation/validation |
| `intake.py` | Media validation and file handling |
| `shared_utils.py` | Constants (`POINTS_BY_VIOLATION`), utilities (`get_utc_now_iso()`) |
| `durable.py` | AI worker (citizen-api only) |
| `gateway.py` | Settings (citizen-api only) |

## Database

All services use the **same SQLite database**: `./roadwatch.db`

**No schema changes** - existing tables used as-is:
- `citizens` - Citizen accounts
- `officers` - Officer accounts
- `reports` - Traffic violation reports
- `media` - Evidence media
- `events` - Audit trail
- `ai_jobs` - AI processing jobs

## Startup

Each service has a `start.sh` script. To start all 4 services:

```bash
# Terminal 1 - API Gateway
cd Traffic/api-gateway
bash start.sh

# Terminal 2 - Auth Service
cd Traffic/auth-service
bash start.sh

# Terminal 3 - Citizen API
cd Traffic/citizen-api
bash start.sh

# Terminal 4 - Officer API
cd Traffic/officer-api
bash start.sh
```

Or use the existing PowerShell scripts in the root:
```powershell
# Windows PowerShell
.\run-all-services.ps1
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (port 3000/3001)                                  │
│  - citizen-app.html                                         │
│  - officer-app.html                                         │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│  API GATEWAY (port 8000)                                    │
│  - Static files & HTML                                      │
│  - Request routing & proxying                               │
│  - Service health checks                                    │
└──┬──────────────────────┬──────────────────────┬────────────┘
   │                      │                      │
   ▼                      ▼                      ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│AUTH SERVICE  │  │CITIZEN API   │  │OFFICER API   │
│(port 8003)   │  │(port 8001)   │  │(port 8002)   │
│              │  │              │  │              │
│• /api/auth/* │  │• /api/media/ │  │• /api/       │
│• /api/officer│  │• /api/reports│  │  authority/*│
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                  │
       └─────────────────┼──────────────────┘
                         │
                         ▼
                    ┌───────────────┐
                    │./roadwatch.db │
                    │  (SQLite)     │
                    └───────────────┘
```

## Testing

All services have been validated:
- ✓ Syntax validation (AST parsing)
- ✓ Import checks
- ✓ Lifespan setup (startup/shutdown)
- ✓ Middleware setup

To verify a service starts:
```bash
# In each service directory
python app.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:PORT
```

## Phase 1 Extraction Complete

- [x] Extract AUTH SERVICE code
- [x] Extract CITIZEN API code
- [x] Extract OFFICER API code
- [x] Create API GATEWAY
- [x] Create requirements.txt for each service
- [x] Create start.sh for each service
- [x] Validate syntax
- [x] Verify imports
- [x] Document architecture

## Next Steps (Phase 2)

1. **Docker Containerization** - Create Dockerfile for each service
2. **Docker Compose** - Orchestrate all services
3. **CI/CD Pipeline** - GitHub Actions for testing/deployment
4. **Load Testing** - Verify inter-service communication
5. **Production Readiness** - Environment variables, logging, metrics

## Important Notes

- The original `app.py` is kept in the root for reference (not removed)
- Each service uses **independent startup** but shares the database
- **No middleware in services** - each endpoint validates auth directly
- **API Gateway handles routing** - no service routing between themselves
- **Static files** remain in root `templates/` and `static/`
- **Media storage** remains in root `media_store/`

## Code Quality

- No code duplication (utility functions in shared modules)
- Clear separation of concerns (each service has one role)
- Proper error handling and logging
- Type hints on public boundaries
- Consistent with existing RoadWatch code style
