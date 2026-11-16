#!/usr/bin/env powershell
# Startup script for Phase 1 - Run all 3 microservices

param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

Write-Host @"
╔══════════════════════════════════════════════════════════════════════════╗
║           PHASE 1: STARTING ALL 3 ROADWATCH MICROSERVICES               ║
╚══════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Change to script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Kill any existing Python processes (if --Clean flag)
if ($Clean) {
    Write-Host "`n🧹 Cleaning up existing processes..." -ForegroundColor Yellow
    Get-Process python -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host "   Terminating PID $($_.Id)"
        $_ | Stop-Process -Force -ErrorAction SilentlyContinue
    }
}

# Setup virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "`n📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "`n✓ Virtual environment ready" -ForegroundColor Green

# Install dependencies
Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

# Start each service in a separate PowerShell process
Write-Host @"

╔══════════════════════════════════════════════════════════════════════════╗
║                         STARTING SERVICES                               ║
╚══════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n🚀 1. Starting AUTH SERVICE (port 8003)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @"
-NoProfile -Command {
    Set-Location "$ScriptDir"
    .\.venv\Scripts\Activate.ps1
    cd auth-service
    python app.py
}
"@ -NoNewWindow

Write-Host "   ✓ AUTH SERVICE started (check http://127.0.0.1:8003/health)" -ForegroundColor Green

Write-Host "`n🚀 2. Starting CITIZEN API (port 8001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @"
-NoProfile -Command {
    Set-Location "$ScriptDir"
    .\.venv\Scripts\Activate.ps1
    cd citizen-api
    python app.py
}
"@ -NoNewWindow

Write-Host "   ✓ CITIZEN API started (check http://127.0.0.1:8001/health)" -ForegroundColor Green

Write-Host "`n🚀 3. Starting OFFICER API (port 8002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @"
-NoProfile -Command {
    Set-Location "$ScriptDir"
    .\.venv\Scripts\Activate.ps1
    cd officer-api
    python app.py
}
"@ -NoNewWindow

Write-Host "   ✓ OFFICER API started (check http://127.0.0.1:8002/health)" -ForegroundColor Green

Write-Host @"

╔══════════════════════════════════════════════════════════════════════════╗
║                    ALL SERVICES STARTING UP                             ║
╚══════════════════════════════════════════════════════════════════════════╝

📍 SERVICE ENDPOINTS:

  🔐 AUTH SERVICE (port 8003):
     - Health: http://127.0.0.1:8003/health
     - POST /api/auth/signup
     - POST /api/auth/login
     - POST /api/officer/register
     - POST /api/officer/login

  👤 CITIZEN API (port 8001):
     - Health: http://127.0.0.1:8001/health
     - POST /api/media/upload
     - POST /api/reports
     - GET /api/reports
     - GET /api/reports/{report_id}

  🚔 OFFICER API (port 8002):
     - Health: http://127.0.0.1:8002/health
     - GET /api/authority/reports
     - GET /api/authority/reports/{report_id}
     - POST /api/authority/reports/{report_id}/decision

📊 SHARED:
   - Database: ./roadwatch.db
   - Static: ./static/
   - Templates: ./templates/

🧪 QUICK TEST:
   Run in another terminal:
   
   # Test AUTH SERVICE
   curl http://127.0.0.1:8003/health
   
   # Test CITIZEN API
   curl http://127.0.0.1:8001/health
   
   # Test OFFICER API
   curl http://127.0.0.1:8002/health

💡 NOTES:
   - Each service runs in its own PowerShell window
   - Close any window to stop that service
   - All services use the same ./roadwatch.db
   - Check your .env file for configuration

🔌 FRONTEND:
   Existing frontends (citizen-reports.html, officer-queue.html, etc.)
   automatically work with these services - no changes needed!

╚══════════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n⏳ Waiting for services to stabilize... (20 seconds)" -ForegroundColor Yellow
Start-Sleep -Seconds 20

Write-Host "`n✅ All services should now be running!" -ForegroundColor Green
Write-Host "📖 See PHASE-1-EXTRACTION-COMPLETE.md for more details" -ForegroundColor Cyan
