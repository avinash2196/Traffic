#!/usr/bin/env powershell
<#
.SYNOPSIS
Stop all RoadWatch services
#>

Write-Host "Stopping all services..." -ForegroundColor Yellow

# Stop all Python processes running our services
$processes = Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object { 
    $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*gateway*" -or $_.CommandLine -like "*http.server*"
}

if ($processes) {
    foreach ($proc in $processes) {
        Write-Host "Stopping process: $($proc.ProcessName) (PID: $($proc.Id))" -ForegroundColor Cyan
        Stop-Process -Id $proc.Id -Force
    }
} else {
    Write-Host "No services running" -ForegroundColor Yellow
}

# Stop Nginx if running
$nginx = Get-Process -Name nginx -ErrorAction SilentlyContinue
if ($nginx) {
    Write-Host "Stopping Nginx (PID: $($nginx.Id))" -ForegroundColor Cyan
    Stop-Process -Id $nginx.Id -Force
}

Write-Host "All services stopped" -ForegroundColor Green
