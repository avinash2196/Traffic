#!/usr/bin/env powershell

$ErrorActionPreference = "Stop"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

Write-Host ""
Write-Host "Starting all RoadWatch services..." -ForegroundColor Cyan
Write-Host ""

$services = @(
    @{dir="auth"; port="9003"; name="Auth Service"},
    @{dir="citizen"; port="9001"; name="Citizen API"},
    @{dir="officer"; port="9002"; name="Officer API"},
    @{dir="ai-gateway"; port="9004"; name="AI Gateway"},
    @{dir="ai-worker"; port="bg"; name="AI Worker"},
    @{dir="citizen-app"; port="9000"; name="Citizen App"},
    @{dir="officer-app"; port="9010"; name="Officer App"}
)

foreach ($svc in $services) {
    $portText = if ($svc.port -eq "bg") { "background" } else { "port " + $svc.port }
    Write-Host "  Starting $($svc.name) ($portText)..." -ForegroundColor Green
    
    $startCode = @"
        cd '$SCRIPT_DIR\$($svc.dir)'
        if (-Not (Test-Path .venv)) {
            python -m venv .venv
        }
        .\.venv\Scripts\Activate.ps1
        pip install -r requirements.txt --quiet
        python app.py
"@
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $startCode -NoNewWindow
    Start-Sleep -Milliseconds 800
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ALL SERVICES STARTED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "BACKEND APIs:" -ForegroundColor Yellow
Write-Host "  Auth Service:     http://127.0.0.1:9003"
Write-Host "  Citizen API:      http://127.0.0.1:9001"
Write-Host "  Officer API:      http://127.0.0.1:9002"
Write-Host "  AI Gateway:       http://127.0.0.1:9004"
Write-Host ""
Write-Host "FRONTEND Apps (open in browser):" -ForegroundColor Magenta
Write-Host "  Citizen App:      http://127.0.0.1:9000"
Write-Host "  Officer App:      http://127.0.0.1:9010"
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
