#!/usr/bin/env powershell
#
# RoadWatch Traffic MVP - All-In-One Startup Script
# Starts all microservices, frontends, and displays a dashboard
#
# Usage: .\START-ALL.ps1
#

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host @"
================================================================================
                 ROADWATCH TRAFFIC MVP - STARTING ALL SERVICES
================================================================================
"@ -ForegroundColor Cyan

# Step 1: Setup virtual environment
Write-Host "`n[1/6] Setting up Python virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path "$ScriptDir\.venv")) {
    Write-Host "      Creating .venv..." -ForegroundColor Gray
    python -m venv "$ScriptDir\.venv"
}
Write-Host "      Done" -ForegroundColor Green

# Step 2: Verify dependencies (already installed from earlier)
Write-Host "`n[2/6] Dependencies already installed..." -ForegroundColor Yellow
Write-Host "      Done" -ForegroundColor Green

# Step 3: Start microservices
Write-Host "`n[3/6] Starting microservices (ports 9001, 9002, 9003, 9004)..." -ForegroundColor Yellow

Write-Host "      - Auth Service (9003)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$ScriptDir'; & '.\.venv\Scripts\Activate.ps1'; cd auth; python app.py`"" -NoNewWindow
Start-Sleep -Milliseconds 500

Write-Host "      - Citizen API (9001)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$ScriptDir'; & '.\.venv\Scripts\Activate.ps1'; cd citizen; python app.py`"" -NoNewWindow
Start-Sleep -Milliseconds 500

Write-Host "      - Officer API (9002)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$ScriptDir'; & '.\.venv\Scripts\Activate.ps1'; cd officer; python app.py`"" -NoNewWindow
Start-Sleep -Milliseconds 500

Write-Host "      - AI Gateway (9004)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$ScriptDir'; & '.\.venv\Scripts\Activate.ps1'; cd ai-gateway; python app.py`"" -NoNewWindow
Start-Sleep -Milliseconds 500

Write-Host "      - AI Worker (Background)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$ScriptDir'; & '.\.venv\Scripts\Activate.ps1'; cd ai-worker; python app.py`"" -NoNewWindow
Start-Sleep -Milliseconds 500

Write-Host "      Done" -ForegroundColor Green

# Step 4: Start frontends
Write-Host "`n[4/6] Starting frontend applications..." -ForegroundColor Yellow

Write-Host "      - Citizen Frontend (3001)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$ScriptDir'; & '.\.venv\Scripts\Activate.ps1'; cd citizen-app; python app.py`"" -NoNewWindow
Start-Sleep -Milliseconds 500

Write-Host "      - Officer Frontend (3002)..." -ForegroundColor Gray
Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$ScriptDir'; & '.\.venv\Scripts\Activate.ps1'; cd officer-app; python app.py`"" -NoNewWindow
Start-Sleep -Milliseconds 500

Write-Host "      Done" -ForegroundColor Green

# Step 5: Wait for services to stabilize
Write-Host "`n[5/6] Waiting for services to stabilize..." -ForegroundColor Yellow
Start-Sleep -Seconds 15
Write-Host "      Done" -ForegroundColor Green

# Step 6: Verify services are running
Write-Host "`n[6/6] Verifying all services..." -ForegroundColor Yellow

$services = @{
    "Auth Service"       = "http://127.0.0.1:9003/health"
    "Citizen API"        = "http://127.0.0.1:9001/health"
    "Officer API"        = "http://127.0.0.1:9002/health"
    "AI Gateway"         = "http://127.0.0.1:9004/health"
    "Citizen Frontend"   = "http://127.0.0.1:3001/"
    "Officer Frontend"   = "http://127.0.0.1:3002/"
}

$allHealthy = $true
foreach ($name in $services.Keys) {
    $url = $services[$name]
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        Write-Host "      [OK] $name" -ForegroundColor Green
    } catch {
        Write-Host "      [FAIL] $name - $($_.Exception.Message)" -ForegroundColor Red
        $allHealthy = $false
    }
}

# Step 7: Display dashboard
Write-Host @"

================================================================================
                        ROADWATCH IS RUNNING!
================================================================================

MICROSERVICES:
  Auth Service          http://127.0.0.1:9003/
  Citizen API           http://127.0.0.1:9001/
  Officer API           http://127.0.0.1:9002/
  AI Gateway            http://127.0.0.1:9004/
  AI Worker             (Background Service)

FRONTENDS:
  Citizen Portal        http://127.0.0.1:3001/     <- Click here to start
  Officer Portal        http://127.0.0.1:3002/     <- Click here to review

TESTING:
  Citizen test flow:
    1. Visit http://127.0.0.1:3001/
    2. Sign up with email/password
    3. Create report with media upload
    4. View report in My Reports

  Officer test flow:
    1. Visit http://127.0.0.1:3002/
    2. Sign up as officer
    3. Review reports in queue
    4. Make decisions (approve/reject)

DATABASE:
  SQLite DB: ./roadwatch.db

LOGS:
  Check each service window for real-time logs

STOPPING SERVICES:
  Close any service window (PowerShell) to stop that service
  Or: Press Ctrl+C in any service window

TROUBLESHOOTING:
  - If services fail to start: Check if ports 9001-9003, 3001-3002 are free
  - If media won't load: Make sure citizen API (9002) is running
  - If login fails: Check auth service (9001) is running

================================================================================
"@ -ForegroundColor Cyan

if ($allHealthy) {
    Write-Host "All services are healthy! You can now use RoadWatch." -ForegroundColor Green
} else {
    Write-Host "WARNING: Some services failed to start. Check the logs above." -ForegroundColor Yellow
}

Write-Host "`n[Keeping this window open to show status - close to stop all services]" -ForegroundColor Gray

# Keep window open
Read-Host "Press Enter to continue (or close window to stop all services)"
