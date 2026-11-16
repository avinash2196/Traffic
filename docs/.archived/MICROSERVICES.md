# RoadWatch Traffic MVP - Multi-Service Architecture

After extensive testing, we've split the monolith into **3 independent microservices** to prevent circular dependencies and enable parallel development.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend Service                       │
│              (HTML/CSS/JS - Port 3001)                  │
│                  Nginx or HTTP Server                    │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼────────┐ ┌──▼──────────┐ ┌─▼──────────────┐
│  API Backend   │ │  AI Gateway  │ │  Reverse Proxy │
│  (Port 8001)   │ │ (Port 5000)  │ │   (Port 80)    │
│    FastAPI     │ │    Flask     │ │     Nginx      │
└────────────────┘ └──────────────┘ └────────────────┘
```

## 📁 Directory Structure

```
traffic-app/
├── frontend/                 # Frontend Service
│   ├── Dockerfile           # Frontend container
│   ├── nginx.conf           # Nginx configuration
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
│
├── backend/                 # API Backend Service
│   ├── Dockerfile           # Backend container
│   ├── app.py              # FastAPI application
│   ├── auth_utils.py       # Authentication
│   ├── bootstrap.py        # Database initialization
│   ├── intake.py           # Media handling
│   ├── durable.py          # Job management
│   ├── requirements.txt    # Python dependencies
│   └── roadwatch.db        # SQLite database
│
├── gateway/                 # AI Gateway Service
│   ├── Dockerfile          # Gateway container
│   ├── gateway.py          # Flask application
│   ├── agw_protocol.py     # Protocol handling
│   └── agw_settings.py     # Configuration
│
├── docker-compose.yml      # Orchestrate all 3 services
├── start-services.ps1      # Local development startup
├── stop-services.ps1       # Stop all services
└── README.md               # This file
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Production)

```powershell
# Set environment variables
$env:ROADWATCH_REVIEWER_TOKEN = "demo-reviewer-token-mvp"
$env:OPENAI_API_KEY = "your-key"

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3001
- API: http://localhost:8001
- Gateway: http://localhost:5000

### Option 2: Local Development (Separate Processes)

```powershell
# Start all services in separate processes
.\start-services.ps1

# Services will be available at:
# Frontend: http://127.0.0.1:3001
# API:      http://127.0.0.1:8001
# Gateway:  http://127.0.0.1:5000

# Stop services
.\stop-services.ps1
```

## 🔄 Service Independence

Each service is **completely independent**:

### Frontend Service
- **Serves:** HTML, CSS, JavaScript
- **Dependencies:** None (can run standalone)
- **Port:** 3001
- **Restarts:** Won't affect Backend or Gateway

### Backend Service  
- **Serves:** REST API for reports, auth, media
- **Dependencies:** SQLite database
- **Port:** 8001
- **Restarts:** Won't affect Frontend or Gateway
- **Features:**
  - Citizen reports API
  - Officer review queue
  - Media upload/download
  - Authentication

### AI Gateway Service
- **Serves:** AI processing (Gemini & OpenAI)
- **Dependencies:** API keys (optional)
- **Port:** 5000
- **Restarts:** Won't affect Frontend or Backend
- **Features:**
  - Evidence assessment
  - Recommendations
  - Graceful degradation if unavailable

## 🔌 Communication Flow

```
Browser
  ↓ (HTTP)
Frontend (3001)
  ├─ Serves HTML/CSS/JS
  └─ Makes API calls to Backend
     ↓ (HTTP)
     Backend (8001)
       ├─ Handles reports
       ├─ Manages media
       ├─ Checks with Gateway (optional)
       └─ Returns JSON
         ↓ (HTTP, optional)
         AI Gateway (5000)
           ├─ Calls Gemini API
           └─ Calls OpenAI API
```

## 🧪 Testing Each Service

### Test Frontend (Load HTML)
```powershell
curl http://127.0.0.1:3001/citizen-login.html
```

### Test Backend (API call)
```powershell
curl -H "X-Citizen-Id: alice" http://127.0.0.1:8001/api/reports
```

### Test Gateway (Health check)
```powershell
curl http://127.0.0.1:5000/health
```

## 📊 Benefits of This Split

| Problem | Before (Monolith) | After (Microservices) |
|---------|-------------------|----------------------|
| Frontend change breaks API | ✗ Yes | ✅ No |
| API change breaks Frontend | ✗ Yes | ✅ No |
| Restart one = restart all | ✗ Yes | ✅ Restart only what changed |
| Deploy Frontend only | ✗ No | ✅ Yes |
| Scale independently | ✗ No | ✅ Yes |
| Team parallel work | ✗ No | ✅ Yes |
| Local dev speed | ✗ Slow reload | ✅ Fast reload |

## ⚙️ Environment Variables

### For All Services
```
ROADWATCH_REVIEWER_TOKEN=demo-reviewer-token-mvp
```

### For Backend
```
DATABASE_URL=sqlite:///./roadwatch.db
```

### For Gateway (Optional)
```
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-2.0-flash
```

## 🔍 Monitoring

### Docker Compose
```powershell
# View all services
docker-compose ps

# View logs for specific service
docker-compose logs api

# View real-time logs
docker-compose logs -f

# Health check
docker-compose exec api curl http://localhost:8001/api/health
```

### Local Services
```powershell
# See which services are running
Get-Process python | Where-Object { $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*gateway*" }

# View logs (they'll be printed to console)
```

## 🐛 Troubleshooting

### Frontend not loading
- Check port 3001 is accessible: `curl http://127.0.0.1:3001`
- Check static files exist in `frontend/static/` and `frontend/templates/`

### API not responding
- Check port 8001 is accessible: `curl http://127.0.0.1:8001/api/health`
- Check database file exists: `backend/roadwatch.db`
- Check environment variables set

### Gateway not working
- Optional service - API works without it
- Check port 5000: `curl http://127.0.0.1:5000/health`
- Check API keys are set in environment

### Port already in use
```powershell
# Find process using port
netstat -ano | findstr :8001

# Kill process (replace XXXX with PID)
taskkill /PID XXXX /F
```

## 🔐 Security Notes

### Demo Mode
- Uses forged `X-Citizen-Id` header (intentional for MVP)
- No password validation
- Shared officer token
- **For testing only - NOT production-ready**

### For Production
- Implement OAuth/OIDC
- Use HTTPS
- Enable password hashing
- Use strong, unique tokens
- Add CORS restrictions
- Set up WAF

## 📝 Deployment Guide

### Docker Deployment
```bash
# Build all images
docker-compose build

# Push to registry
docker tag roadwatch-frontend myregistry/roadwatch-frontend:latest
docker push myregistry/roadwatch-frontend:latest
# Repeat for other services

# Deploy to Kubernetes/Swarm with docker-compose or helm chart
```

### Kubernetes Deployment
```yaml
# Create separate deployments for each service
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/backend-deployment.yaml  
kubectl apply -f k8s/gateway-deployment.yaml

# Setup Ingress for routing
kubectl apply -f k8s/ingress.yaml
```

## 🎯 Next Steps

1. **Verify all 3 services work** ✓ (This session)
2. Write comprehensive tests for each service
3. Set up CI/CD pipeline
4. Create Kubernetes manifests
5. Add monitoring/alerting
6. Document API for third-party integrations

## 📞 Support

- **Frontend Issues:** Check `frontend/` directory, Nginx logs
- **API Issues:** Check `backend/` directory, FastAPI logs
- **Gateway Issues:** Check `gateway/` directory, Flask logs
- **Integration Issues:** Check docker-compose networking

---

**Architecture Status:** ✅ **SPLIT AND READY**  
**Last Updated:** 2026-11-13  
**Version:** 1.0.0-microservices
