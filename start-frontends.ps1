#!/usr/bin/env powershell

param(
    [switch]$Wait = $false
)

$ErrorActionPreference = "Stop"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

# Citizen App
$citizenDir = Join-Path (Split-Path -Parent $SCRIPT_DIR) "citizen-app"
$officerDir = Join-Path (Split-Path -Parent $SCRIPT_DIR) "officer-app"

Write-Host "Starting Citizen App (port 3000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList @"
    Set-Location '$citizenDir'
    if (-Not (Test-Path .venv)) {
        python -m venv .venv
    }
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt > `$null 2>&1
    uvicorn app:app --reload --host 127.0.0.1 --port 3000
"@ -NoNewWindow -PassThru | Out-Null

Start-Sleep -Seconds 2

Write-Host "Starting Officer App (port 3001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList @"
    Set-Location '$officerDir'
    if (-Not (Test-Path .venv)) {
        python -m venv .venv
    }
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt > `$null 2>&1
    uvicorn app:app --reload --host 127.0.0.1 --port 3001
"@ -NoNewWindow -PassThru | Out-Null

Write-Host ""
Write-Host "Both frontend apps starting:" -ForegroundColor Cyan
Write-Host "  Citizen App:  http://127.0.0.1:3000" -ForegroundColor Yellow
Write-Host "  Officer App:  http://127.0.0.1:3001" -ForegroundColor Yellow
Write-Host ""

if ($Wait) {
    Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Gray
    Read-Host "Ready. Press Enter to continue"
}
