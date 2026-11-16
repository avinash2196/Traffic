chronological order
- âœ… Returns 401 for missing Authorization header
- âœ… Returns 403 for non-officers
- âœ… Returns 404 for non-existent reports
- âœ… Returns 409 for non-approved reports with descriptive error message
- âœ… UI button added to officer-detail.html
- âœ… Button click triggers file download
- âœ… Downloaded ZIP file is valid and extractable
- âœ… No console errors or warnings
- âœ… Code review approved by 1 peer
- âœ… Tested with approved and non-approved reports
- âœ… Tested with missing/invalid Authorization header

---

### **6. RISKS & MITIGATION**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| ZIP file too large (>100MB) | Low | Medium | Compress media; implement streaming if needed; add file size check before export |
| Media file missing from disk | Medium | High | Add check in endpoint; return 404 if file not found; add logging |
| JSON encoding errors | Low | Low | Validate manifest/timeline JSON before zipping; use json.dumps with error handling |
| ZIP creation fails mid-stream | Low | High | Create in-memory buffer; validate all files before streaming response |
| Browser doesn't download | Low | Low | Verify Content-Disposition header; test in multiple browsers |
| Officer token extraction fails | Low | Medium | Validate Authorization header format; add detailed error messages |
| Concurrent export requests | Low | Low | Each request creates own ZIP in memory; no file contention |

---

### **7. EFFORT ESTIMATES**

| Task | Hours | Owner |
|------|-------|-------|
| 1.1: ZIP export function | 1.0 | Backend Dev |
| 1.2: Import modules | 0.08 | Backend Dev |
| 1.3: Database schema | 0.4 | Backend Dev |
| **Task 1 Total** | **1.5 hours** | |
| 2.1: Update HTML | 0.17 | Frontend Dev |
| 2.2: Update JavaScript | 0.33 | Frontend Dev |
| **Task 2 Total** | **0.5 hours** | |
| 3.1: Endpoint testing | 0.5 | QA / Dev |
| 3.2: UI testing | 0.5 | QA / Dev |
| **Task 3 Total** | **1.0 hour** | |
| | **TOTAL M6** | **3.0 hours** |

**Calendar Duration:** 0.5â€“1 day (can run in parallel with M5 final phases)

---

### **8. TESTING STRATEGY**

#### **Unit Testing**

**Endpoint Tests (curl/Postman):**
- [ ] Test successful export (200 OK with ZIP)
- [ ] Test missing Authorization header (401)
- [ ] Test invalid Authorization header (403)
- [ ] Test non-existent report (404)
- [ ] Test non-approved report (409 with status in error message)
- [ ] Test approved report (200 OK)

**ZIP Structure Validation:**
- [ ] Media file present and correct size
- [ ] manifest.json valid JSON with all required fields
- [ ] timeline.json valid JSON with all events
- [ ] README.txt readable and contains all info
- [ ] All files uncompressed correctly
- [ ] No file corruption in ZIP

#### **Integration Testing**

**UI Flow:**
- [ ] Officer logs in
- [ ] Officer navigates to approved report
- [ ] "Download Evidence" button visible
- [ ] Click button â†’ ZIP downloads
- [ ] ZIP file valid and extractable
- [ ] All contents match report data

**Error Handling:**
- [ ] Non-approved report shows error message
- [ ] Missing auth header shows error
- [ ] Failed download shows retry option

#### **Manual Smoke Test**

1. [ ] Create test report (status=submitted)
2. [ ] Submit report via POST /api/reports
3. [ ] Manually update status to "approved" in database
4. [ ] Call GET /api/authority/reports/{id}/evidence.zip
5. [ ] ZIP downloads successfully
6. [ ] Extract and verify all files
7. [ ] Verify media file unchanged (byte-for-byte)
8. [ ] Verify manifest.json contains correct hash
9. [ ] Verify timeline.json contains all events
10. [ ] Test with unapproved report (verify 409 error)

---

---

## **MILESTONE M7: DOCKER & DEPLOYMENT**

**Document Version:** IMPL-M7-DOCKER-DEPLOYMENT-PLAN.md  
**Type:** OTHER (Infrastructure)  
**Status:** Ready to Execute  
**Approval Gate Required:** YES

---

### **1. OBJECTIVE**

Containerize the RoadWatch MVP application for production deployment with:
- Multi-stage Dockerfile (optimized layers for dependencies, app, migrations)
- Windows startup script (start-windows.ps1) for local development
- Unix startup script (start.sh) for macOS/Linux
- .dockerignore to exclude unnecessary files
- Verified build and runtime with `docker build` and `docker run`

**Success Criteria:** `docker build -t roadwatch .` succeeds, `docker run -p 8000:8000 roadwatch` runs successfully, API responds on http://localhost:8000/api/docs.

---

### **2. SCOPE**

#### **Deliverables**

**4 Files to Create/Modify:**

1. **Dockerfile** (Enhanced multi-stage)
   - Stage 1: Base image (python:3.14.9-slim-trixie) with system deps
   - Stage 2: Python dependencies (pip install -r requirements.txt)
   - Stage 3: App files and migrations
   - CMD: Run FastAPI via uvicorn with auto-reload disabled

2. **.dockerignore** (NEW)
   - Exclude: media_store/, __pycache__/, .venv/, .git/, .pytest_cache/, *.pyc, .env
   - Purpose: Reduce image size, avoid sensitive data

3. **start-windows.ps1** (NEW, Windows PowerShell)
   - Create Python virtual environment (.venv)
   - Activate venv
   - Install dependencies (pip install -r requirements.txt)
   - Run app: `python app.py` or `uvicorn app:app --host 0.0.0.0 --port 8000`
   - Trap Ctrl+C to cleanup
   - For developers: local development without Docker

4. **start.sh** (NEW, macOS/Linux shell script)
   - Create Python virtual environment (.venv)
   - Activate venv
   - Install dependencies (pip install -r requirements.txt)
   - Run app: `python app.py` or `uvicorn app:app --host 0.0.0.0 --port 8000`
   - Trap signals for graceful shutdown
   - For developers: local development without Docker

---

#### **Dockerfile Specifications**

**Current Dockerfile (Review & Enhance):**
```dockerfile
FROM python:3.14.9-slim-trixie
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates libnss3-tools procps && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && python -m playwright install --with-deps chromium
COPY . .
CMD ["python", "bootstrap.py"]
```

**Enhanced Multi-Stage Dockerfile:**
```dockerfile
# Stage 1: Builder image
FROM python:3.14.9-slim-trixie as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    libnss3-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    python -m playwright install --with-deps chromium

# Stage 2: Runtime image
FROM python:3.14.9-slim-trixie as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    libnss3-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /workspace

# Copy application code
COPY . .

# Create media directory for uploads
RUN mkdir -p /workspace/media_store

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **.dockerignore Specifications**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.env
.venv
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.tox/
.coverage
htmlcov/
.hypothesis/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Git
.git
.gitignore
.gitattributes

# Project-specific
media_store/
roadwatch.db
roadwatch.db-wal
roadwatch.db-shm
*.log
.env.local
```

#### **start-windows.ps1 Specifications**

```powershell
# RoadWatch Traffic MVP - Windows Startup Script
# Usage: .\start-windows.ps1

$ErrorActionPreference = "Stop"

Write-Host "ðŸš— RoadWatch Traffic MVP - Windows Startup" -ForegroundColor Cyan

# Check Python installation
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "âŒ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = python --version
Write-Host "âœ“ Python found: $pythonVersion" -ForegroundColor Green

# Create virtual environment if needed
$venvPath = ".venv"
if (!(Test-Path $venvPath)) {
    Write-Host "ðŸ“¦ Creating virtual environment..." -ForegroundColor Cyan
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "âŒ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "âœ“ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "ðŸ”Œ Activating virtual environment..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"

# Install dependencies
Write-Host "ðŸ“š Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "âŒ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "âœ“ Dependencies installed" -ForegroundColor Green

# Create media directory
if (!(Test-Path "media_store")) {
    New-Item -ItemType Directory -Path "media_store" | Out-Null
    Write-Host "âœ“ Created media_store directory" -ForegroundColor Green
}

# Run application
Write-Host "ðŸš€ Starting RoadWatch Traffic MVP..." -ForegroundColor Green
Write-Host "ðŸ“ API available at: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "ðŸ“š Documentation at: http://127.0.0.1:8000/api/docs" -ForegroundColor Yellow
Write-Host "â¹ï¸  Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White

# Start app with Ctrl+C handler
try {
    uvicorn app:app --host 0.0.0.0 --port 8000 --reload
} catch {
    Write-Host "âŒ Error running application: $_" -ForegroundColor Red
    exit 1
} finally {
    Write-Host "" -ForegroundColor White
    Write-Host "ðŸ‘‹ RoadWatch stopped" -ForegroundColor Cyan
}
```

#### **start.sh Specifications**

```bash
#!/bin/bash

# RoadWatch Traffic MVP - macOS/Linux Startup Script
# Usage: chmod +x start.sh && ./start.sh

set -e  # Exit on error

echo "ðŸš— RoadWatch Traffic MVP - macOS/Linux Startup"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "âŒ Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org or via package manager"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "âœ“ Python found: $PYTHON_VERSION"

# Create virtual environment if needed
VENV_PATH=".venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "ðŸ“¦ Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    echo "âœ“ Virtual environment created"
fi

# Activate virtual environment
echo "ðŸ”Œ Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Install dependencies
echo "ðŸ“š Installing dependencies..."
pip install -r requirements.txt
echo "âœ“ Dependencies installed"

# Create media directory
if [ ! -d "media_store" ]; then
    mkdir -p media_store
    echo "âœ“ Created media_store directory"
fi

# Handle signals for graceful shutdown
trap 'echo ""; echo "ðŸ‘‹ RoadWatch stopped"; exit 0' SIGINT SIGTERM

# Run application
echo "ðŸš€ Starting RoadWatch Traffic MVP..."
echo "ðŸ“ API available at: http://127.0.0.1:8000"
echo "ðŸ“š Documentation at: http://127.0.0.1:8000/api/docs"
echo "â¹ï¸  Press Ctrl+C to stop"
echo ""

uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

### **3. TASKS** (Ordered & Detailed)

#### **Task 1: Create/Update Dockerfile** â±ï¸ 30 minutes

**1.1: Review current Dockerfile** (10 min)

Open `Dockerfile` and review existing content (already shown above).

**Completion Criteria:**
- Current Dockerfile exists at project root
- Contains python:3.14.9-slim-trixie base image
- Installs ffmpeg, requirements, and runs bootstrap.py

**1.2: Update to multi-stage Dockerfile** (20 min)

Replace entire Dockerfile with multi-stage version:

```dockerfile
# Stage 1: Builder image
FROM python:3.14.9-slim-trixie as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    libnss3-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    python -m playwright install --with-deps chromium

# Stage 2: Runtime image
FROM python:3.14.9-slim-trixie as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
    libnss3-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /workspace

# Copy application code
COPY . .

# Create media directory for uploads
RUN mkdir -p /workspace/media_store

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Completion Criteria:**
- Multi-stage Dockerfile in place
- Stage 1 (builder) compiles dependencies only
- Stage 2 (runtime) uses minimal base image
- HEALTHCHECK endpoint points to /health
- CMD runs uvicorn with correct host/port
- No syntax errors (verify with `docker build --dry-run` if available)

---

#### **Task 2: Create .dockerignore** â±ï¸ 15 minutes

**2.1: Create .dockerignore file** (15 min)

Create new file `.dockerignore` at project root with content:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.env
.venv
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.tox/
.coverage
htmlcov/
.hypothesis/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Git
.git
.gitignore
.gitattributes

# Project-specific
media_store/
roadwatch.db
roadwatch.db-wal
roadwatch.db-shm
*.log
.env.local
```

**Completion Criteria:**
- `.dockerignore` exists in project root
- Contains all categories (Python, Testing, IDE, Git, Project)
- No syntax errors
- File is readable by Docker daemon

---

#### **Task 3: Create start-windows.ps1** â±ï¸ 20 minutes

**3.1: Create PowerShell startup script** (20 min)

Create new file `start-windows.ps1` at project root with content (shown in Scope section above).

**Completion Criteria:**
- `start-windows.ps1` exists in project root
- Script is readable and not corrupted
- All paths use correct Windows syntax
- Virtual environment activation command correct for PowerShell
- Error handling in place (exit codes)
- User-friendly output messages

**3.2: Verify script syntax** (5 min, part of testing)

```powershell
# Test script syntax without running
powershell -NoProfile -Command "try { [System.Management.Automation.PSParser]::Tokenize((Get-Content 'start-windows.ps1'), [ref]$null) | Out-Null } catch { exit 1 }"
```

---

#### **Task 4: Create start.sh** â±ï¸ 20 minutes

**4.1: Create shell startup script** (15 min)

Create new file `start.sh` at project root with content (shown in Scope section above).

**Completion Criteria:**
- `start.sh` exists in project root
- Script is readable and not corrupted
- All paths use Unix syntax
- Virtual environment activation command correct for bash/sh
- Error handling in place (set -e)
- Signal handling for Ctrl+C
- User-friendly output messages

**4.2: Set executable permissions** (5 min)

```bash
chmod +x start.sh
```

**Completion Criteria:**
- File permissions: `-rwxr-xr-x` (755)
- Verified with `ls -l start.sh`

---

#### **Task 5: Build & Test Docker Image** â±ï¸ 60 minutes

**5.1: Build Docker image** (20 min)

```bash
# Build the image
docker build -t roadwatch:latest .

# Expected output:
# [1/n] FROM python:3.14.9-slim-trixie as builder
# [2/n] WORKDIR /workspace
# ... (multiple build steps)
# Successfully built [IMAGE_ID]
# Successfully tagged roadwatch:latest
```

**Completion Criteria:**
- Build completes without errors
- Image tagged as `roadwatch:latest`
- Image size reasonable (should be <2GB due to multi-stage)
- No warnings about HEALTHCHECK
- Verify with `docker images | grep roadwatch`

**5.2: Run container and verify API** (20 min)

```bash
# Run the container
docker run -d -p 8000:8000 --name roadwatch-test roadwatch:latest

# Wait 5 seconds for startup
sleep 5

# Test health endpoint
curl http://localhost:8000/health
# Expected: {"status":"ok","timestamp":"...","service":"roadwatch-traffic-api"}

# Test API docs
curl http://localhost:8000/api/docs
# Expected: HTML content for Swagger UI

# Check container logs
docker logs roadwatch-test
# Expected: FastAPI startup messages, no errors

# Stop container
docker stop roadwatch-test
docker rm roadwatch-test
```

**Completion Criteria:**
- Container starts without errors
- /health endpoint responds 200 OK
- /api/docs returns HTML
- No error messages in logs
- Container stops cleanly

**5.3: Verify image layers** (10 min)

```bash
# Inspect image layers
docker inspect roadwatch:latest

# Expected:
# - Image size <= 2GB
# - 2 stages visible (builder, runtime)
# - Healthcheck configured
# - Port 8000 exposed

# List image history
docker history roadwatch:latest
# Expected: Multiple layers showing builder â†’ runtime optimization
```

**Completion Criteria:**
- Image history shows builder and runtime stages
- Final image optimized (no builder artifacts included)
- Image size is reasonable

---

#### **Task 6: Test Local Startup Scripts** â±ï¸ 40 minutes

**6.1: Test start-windows.ps1 (Windows only)** (20 min)

On Windows machine:

```powershell
# Navigate to project directory
cd C:\Users\avina\Downloads\avinash-repo\v11\Traffic

# Run startup script
.\start-windows.ps1

# Expected output:
# ðŸš— RoadWatch Traffic MVP - Windows Startup
# âœ“ Python found: Python 3.11.x
# ðŸ“¦ Creating virtual environment...
# âœ“ Virtual environment created
# ðŸ”Œ Activating virtual environment...
# ðŸ“š Installing dependencies...
# âœ“ Dependencies installed
# âœ“ Created media_store directory
# ðŸš€ Starting RoadWatch Traffic MVP...
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Test API in another terminal
curl http://localhost:8000/health

# Stop with Ctrl+C
# Expected: ðŸ‘‹ RoadWatch stopped
```

**Completion Criteria:**
- Script runs without errors
- Virtual environment created
- Dependencies installed
- uvicorn starts successfully
- API responds on localhost:8000
- Ctrl+C stops app gracefully

**6.2: Test start.sh (macOS/Linux)** (20 min)

On macOS or Linux:

```bash
# Navigate to project directory
cd ~/Downloads/avinash-repo/v11/Traffic

# Make script executable (if not already)
chmod +x start.sh

# Run startup script
./start.sh

# Expected output:
# ðŸš— RoadWatch Traffic MVP - macOS/Linux Startup
# âœ“ Python found: Python 3.11.x
# ðŸ“¦ Creating virtual environment...
# âœ“ Virtual environment created
# ðŸ”Œ Activating virtual environment...
# ðŸ“š Installing dependencies...
# âœ“ Dependencies installed
# âœ“ Created media_store directory
# ðŸš€ Starting RoadWatch Traffic MVP...
# INFO:     Uvicorn running on http://0.0.0.0:8000

# Test API in another terminal
curl http://localhost:8000/health

# Stop with Ctrl+C
# Expected: ðŸ‘‹ RoadWatch stopped
```

**Completion Criteria:**
- Script runs without errors
- Virtual environment created
- Dependencies installed
- uvicorn starts successfully
- API responds on localhost:8000
- Ctrl+C stops app gracefully
- Output messages display correctly

---

#### **Task 7: Documentation & README** â±ï¸ 15 minutes

**7.1: Update README.md with deployment section** (15 min)

Add to README.md:

```markdown
## ðŸ³ Docker Deployment

### Quick Start with Docker

```bash
# Build the image
docker build -t roadwatch .

# Run the container
docker run -d -p 8000:8000 roadwatch

# Access API
# - API: http://localhost:8000
# - Docs: http://localhost:8000/api/docs
```

### Local Development (Without Docker)

#### Windows
```powershell
.\start-windows.ps1
```

#### macOS/Linux
```bash
chmod +x start.sh
./start.sh
```

### Environment Variables (Optional)

```bash
# .env file (optional for development)
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
DATABASE_URL=sqlite:///./roadwatch.db
```

### Troubleshooting

**Build fails with "ffmpeg not found"**
- Ensure Docker has access to system resources
- Try: `docker build --no-cache -t roadwatch .`

**Container exits immediately**
- Check logs: `docker logs roadwatch`
- Verify port 8000 is not in use: `lsof -i :8000`

**API not responding**
- Wait 5 seconds for startup
- Check health endpoint: `curl http://localhost:8000/health`
- Verify port mapping: `docker port roadwatch`
```

**Completion Criteria:**
- README updated with Docker section
- Examples provided for all platforms
- Troubleshooting section included
- All commands tested and working

---

### **4. DEPENDENCIES**

**Hard Dependencies:**
- âœ… M2 COMPLETE: FastAPI app must exist (app.py)
- âœ… M4.2 COMPLETE: API endpoints must work
- âœ… All Python files in project (no placeholders)

**Soft Dependencies:**
- M5 COMPLETE: UI files (not required for Docker to build, but nice to have)
- M6 COMPLETE: Evidence export (not required for Docker to build)

**External Requirements:**
- Docker installed on deployment machine
- Python 3.11+ for local startup scripts
- ffmpeg system package (handled in Dockerfile)

---

### **5. DEFINITION OF DONE**

**M7 Docker & Deployment is DONE when:**

- âœ… Dockerfile (multi-stage) exists and builds without errors
- âœ… `.dockerignore` exists with all necessary exclusions
- âœ… `start-windows.ps1` exists and is executable
- âœ… `start.sh` exists and is executable (chmod +x)
- âœ… `docker build -t roadwatch .` completes successfully
- âœ… Built image has reasonable size (<2GB)
- âœ… `docker run -p 8000:8000 roadwatch` starts container
- âœ… Container responds to `/health` endpoint
- âœ… Container responds to `/api/docs` endpoint
- âœ… Swagger UI loads in browser at http://localhost:8000/api/docs
- âœ… HEALTHCHECK configured and functional
- âœ… start-windows.ps1 runs successfully on Windows
- âœ… start.sh runs successfully on macOS/Linux
- âœ… Startup scripts create virtual environment
- âœ… Startup scripts install dependencies
- âœ… Startup scripts run uvicorn correctly
- âœ… Startup scripts handle Ctrl+C gracefully
- âœ… README.md updated with deployment instructions
- âœ… No console errors or warnings on startup
- âœ… Code review approved by 1 peer
- âœ… Tested on at least 2 platforms (Docker + local script)

---

### **6. RISKS & MITIGATION**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| ffmpeg not available in Docker | Low | High | Already included in base image; verify with test build |
| Port 8000 already in use | Medium | Low | Use different port: `docker run -p 8001:8000` or `--port 8001` in script |
| Virtual environment creation fails | Low | High | Check Python version, disk space; use `python3 -m venv` explicitly |
| Dependencies installation takes long time | Medium | Low | Expected for first build; use Docker layer caching on subsequent builds |
| Playwright install fails (chromium) | Low | Medium | Add error handling; make playwright optional for MVP if needed |
| startup-windows.ps1 won't execute | Medium | High | Set-ExecutionPolicy RemoteSigned in PowerShell; document in README |
| API startup takes >10 seconds | Low | Low | HEALTHCHECK has 5 second start period, should be sufficient |
| Media directory not writable in Docker | Low | Medium | Ensure media_store created in Dockerfile with proper permissions |

---

### **7. EFFORT ESTIMATES**

| Task | Hours | Owner |
|------|-------|-------|
| 1.1: Review current Dockerfile | 0.17 | DevOps/Dev |
| 1.2: Update to multi-stage | 0.33 | DevOps/Dev |
| **Task 1 Total** | **0.5 hours** | |
| 2.1: Create .dockerignore | 0.25 | DevOps/Dev |
| **Task 2 Total** | **0.25 hours** | |
| 3.1: Create start-windows.ps1 | 0.33 | DevOps/Dev |
| 3.2: Verify syntax | 0.08 | DevOps/Dev |
| **Task 3 Total** | **0.42 hours** | |
| 4.1: Create start.sh | 0.25 | DevOps/Dev |
| 4.2: Set permissions | 0.08 | DevOps/Dev |
| **Task 4 Total** | **0.33 hours** | |
| 5.1: Build Docker image | 0.33 | QA/Dev |
| 5.2: Run and verify | 0.33 | QA/Dev |
| 5.3: Inspect layers | 0.
