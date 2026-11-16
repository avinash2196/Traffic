#!/usr/bin/env powershell
# Start all three microservices for RoadWatch Traffic MVP

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "STARTING ROADWATCH MICROSERVICES (9001, 9002, 9003)" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan

# Activate venv
if (-not (Test-Path "$ScriptDir\.venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv "$ScriptDir\.venv"
}

# Start Auth Service (9001)
Write-Host "`nStarting AUTH SERVICE (9001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @"
-NoProfile -Command {
    Set-Location "$ScriptDir"
    & ".\\.venv\Scripts\Activate.ps1"
    cd auth
    python app.py
}
"@ -NoNewWindow -PassThru | Out-Null
Write-Host "   - AUTH SERVICE started" -ForegroundColor Green

# Start Citizen API (9002)
Write-Host "`nStarting CITIZEN API (9002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @"
-NoProfile -Command {
    Set-Location "$ScriptDir"
    & ".\\.venv\Scripts\Activate.ps1"
    cd citizen
    python app.py
}
"@ -NoNewWindow -PassThru | Out-Null
Write-Host "   - CITIZEN API started" -ForegroundColor Green

# Start Officer API (9003)
Write-Host "`nStarting OFFICER API (9003)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList @"
-NoProfile -Command {
    Set-Location "$ScriptDir"
    & ".\\.venv\Scripts\Activate.ps1"
    cd officer
    python app.py
}
"@ -NoNewWindow -PassThru | Out-Null
Write-Host "   - OFFICER API started" -ForegroundColor Green

Write-Host @"

=========================================================
               SERVICES STARTING UP (30 seconds)
=========================================================

ENDPOINTS:
   Auth Service:    http://127.0.0.1:9001/health
   Citizen API:     http://127.0.0.1:9002/health
   Officer API:     http://127.0.0.1:9003/health
   API Gateway:     http://127.0.0.1:9000/
   Citizen Frontend: http://127.0.0.1:3001/

Waiting for services to stabilize...
"@ -ForegroundColor Cyan

Start-Sleep -Seconds 30

Write-Host "`nAll services should now be running!" -ForegroundColor Green
Write-Host "Try visiting: http://127.0.0.1:3001/" -ForegroundColor Green
