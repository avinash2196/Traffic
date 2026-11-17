#!/usr/bin/env powershell
<#
.SYNOPSIS
Start RoadWatch MVP with AI Gateway + Backend API
.DESCRIPTION
Starts the AI Gateway (port 9999) and Backend API (port 8001) services
Run in one terminal to see logs from both services
#>

param(
    [switch]$Gateway = $true,
    [switch]$Backend = $true
)

$ErrorActionPreference = "Stop"

Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║        RoadWatch MVP - Service Orchestrator                       ║
╚════════════════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Load .env file for configuration
$envFile = ".\.env"
if (Test-Path $envFile) {
    Write-Host "✓ Loading .env configuration" -ForegroundColor Green
    $envVars = @{}
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line -split '=', 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                Set-Item -Path "env:$key" -Value $value
                $envVars[$key] = $value
            }
        }
    }
} else {
    Write-Host "⚠ .env file not found - using defaults" -ForegroundColor Yellow
}

# Set defaults
if (-not $env:ROADWATCH_REVIEWER_TOKEN) {
    $env:ROADWATCH_REVIEWER_TOKEN = "demo-reviewer-token-mvp"
}
if (-not $env:APP_PROFILE) {
    $env:APP_PROFILE = "local"
}

Write-Host ""
Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Profile: $($env:APP_PROFILE)" -ForegroundColor Gray
Write-Host "  OpenAI Key: $(if ($env:OPENAI_API_KEY) { "Set" } else { "Not set (AI may fail)" })" -ForegroundColor Gray
Write-Host "  AI Gateway URL: $($env:AI_GATEWAY_URL)" -ForegroundColor Gray
Write-Host ""

# Check Python
$python = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
Write-Host "Using: $python" -ForegroundColor Gray

# Function to start a service in background
function Start-ServiceWindow {
    param(
        [string]$Name,
        [int]$Port,
        [scriptblock]$Command
    )
    
    Write-Host "🚀 Starting $Name on port $Port..." -ForegroundColor Green
    
    # Create a script file to run in new window
    $scriptPath = "$env:TEMP\roadwatch_start_$Name.ps1"
    $script = @"
`$ErrorActionPreference = 'Continue'
Write-Host '═' * 80 -ForegroundColor Cyan
Write-Host 'RoadWatch: $Name (port $Port)' -ForegroundColor Green
Write-Host '═' * 80 -ForegroundColor Cyan
Write-Host ''
Set-Location '$((Get-Location).Path)'
`$env:ROADWATCH_REVIEWER_TOKEN = '$($env:ROADWATCH_REVIEWER_TOKEN)'
`$env:AI_GATEWAY_URL = '$($env:AI_GATEWAY_URL)'
`$env:OPENAI_API_KEY = '$($env:OPENAI_API_KEY)'
`$env:GEMINI_API_KEY = '$($env:GEMINI_API_KEY)'
`$env:APP_PROFILE = '$($env:APP_PROFILE)'

& { $($Command.ToString()) }

Read-Host 'Press Enter to close this window'
"@
    
    $script | Out-File -FilePath $scriptPath -Encoding UTF8
    Start-Process powershell -ArgumentList "-NoExit -File $scriptPath" -WindowStyle Normal
    Start-Sleep -Milliseconds 800
}

# Start services
if ($Gateway) {
    $gwCmd = {
        Write-Host "Starting AI Gateway Service..." -ForegroundColor Yellow
        Push-Location ai-gateway
        & $python -m uvicorn app:app --host 127.0.0.1 --port 9004
        Pop-Location
    }
    Start-ServiceWindow -Name "AI Gateway" -Port 9004 -Command $gwCmd
}

if ($Backend) {
    Start-Sleep -Seconds 2
    
    $apiCmd = {
        Write-Host "Starting Backend API..." -ForegroundColor Yellow
        Write-Host "📚 API Docs: http://127.0.0.1:8001/api/docs" -ForegroundColor Cyan
        & $python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
    }
    Start-ServiceWindow -Name "Backend API" -Port 8001 -Command $apiCmd
}

Write-Host ""
Write-Host "✓ Services launched in separate windows" -ForegroundColor Green
Write-Host ""
Write-Host "Quick Test:" -ForegroundColor Cyan
Write-Host "  curl http://127.0.0.1:8001/health" -ForegroundColor Gray
Write-Host ""
Write-Host "API Documentation:" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:8001/api/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Logs appear in service windows. Close individual windows to stop that service." -ForegroundColor Gray
