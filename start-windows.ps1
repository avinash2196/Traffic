# RoadWatch Traffic MVP - Windows Startup Script
# Usage: .\start-windows.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚗 RoadWatch Traffic MVP - Windows Startup" -ForegroundColor Cyan
Write-Host ""

# Load environment variables from .env
if (Test-Path ".env") {
    Write-Host "📝 Loading configuration from .env..." -ForegroundColor Cyan
    Get-Content .env | ForEach-Object {
        $line = $_.Trim()
        if ($line -and !$line.StartsWith("#")) {
            $parts = $line -split "=", 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                [Environment]::SetEnvironmentVariable($key, $value, "Process")
                Write-Host "  ✓ $key = $(if ($key -match 'KEY|TOKEN|SECRET') { '***' } else { $value })" -ForegroundColor Gray
            }
        }
    }
    Write-Host "✓ Configuration loaded" -ForegroundColor Green
}
else {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Please create .env by copying .env.example:" -ForegroundColor Yellow
    Write-Host "  copy .env.example .env" -ForegroundColor Gray
    Write-Host "  Edit .env with your real API keys" -ForegroundColor Gray
    exit 1
}

Write-Host ""

# Verify required variables
if (!$env:OPENAI_API_KEY -or $env:OPENAI_API_KEY -eq "") {
    Write-Host "ERROR: OPENAI_API_KEY not set in .env" -ForegroundColor Red
    exit 1
}

if (!$env:GATEWAY_TOKEN -or $env:GATEWAY_TOKEN -eq "") {
    Write-Host "ERROR: GATEWAY_TOKEN not set in .env" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Required variables verified" -ForegroundColor Green
Write-Host ""

# Check Python installation
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org" -ForegroundColor Yellow
    exit 1
}

$pythonVersion = python --version
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green

# Create virtual environment if needed
$venvPath = ".venv"
if (!(Test-Path $venvPath)) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Cyan
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
else {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
}

Write-Host ""

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Cyan
& "$venvPath\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

Write-Host ""

# Install dependencies
Write-Host "📚 Installing dependencies..." -ForegroundColor Cyan
pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green

Write-Host ""

# Create media directory
if (!(Test-Path "media_store")) {
    New-Item -ItemType Directory -Path "media_store" -Force | Out-Null
    Write-Host "✓ Created media_store directory" -ForegroundColor Green
}
else {
    Write-Host "✓ media_store directory exists" -ForegroundColor Green
}

Write-Host ""

# Initialize database
if (!(Test-Path "roadwatch.db")) {
    Write-Host "📊 Initializing database..." -ForegroundColor Cyan
    python bootstrap.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Database initialization had issues, continuing..." -ForegroundColor Yellow
    }
    Write-Host "✓ Database ready" -ForegroundColor Green
}
else {
    Write-Host "✓ Database exists" -ForegroundColor Green
}

Write-Host ""

# Start AI Gateway in background
Write-Host "🤖 Starting AI Gateway on port 9004..." -ForegroundColor Cyan
Push-Location ai-gateway
$gatewayJob = Start-Process -FilePath python -ArgumentList "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "9004" -NoNewWindow -PassThru -ErrorAction SilentlyContinue
Pop-Location
Write-Host "✓ AI Gateway started (PID: $($gatewayJob.Id))" -ForegroundColor Green

# Give gateway time to start
Start-Sleep -Seconds 2

Write-Host ""

# Run application
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 RoadWatch Traffic MVP - STARTING" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  API Host: $($env:FASTAPI_HOST)" -ForegroundColor White
Write-Host "  API Port: $($env:FASTAPI_PORT)" -ForegroundColor White
Write-Host "  Gateway URL: http://127.0.0.1:9004" -ForegroundColor White
Write-Host ""
Write-Host "Web Interface:" -ForegroundColor Yellow
Write-Host "  Citizen Portal: http://127.0.0.1:$($env:FASTAPI_PORT)/citizen-login.html" -ForegroundColor White
Write-Host "  Officer Portal: http://127.0.0.1:$($env:FASTAPI_PORT)/officer-login.html" -ForegroundColor White
Write-Host ""
Write-Host "API Documentation:" -ForegroundColor Yellow
Write-Host "  Swagger UI: http://127.0.0.1:$($env:FASTAPI_PORT)/api/docs" -ForegroundColor White
Write-Host "  Health: http://127.0.0.1:$($env:FASTAPI_PORT)/health" -ForegroundColor White
Write-Host ""
Write-Host "Control:" -ForegroundColor Yellow
Write-Host "  Stop server: Press Ctrl+C" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set trap for cleanup on exit
$null = Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action {
    Write-Host ""
    Write-Host "Stopping AI Gateway..." -ForegroundColor Yellow
    Stop-Process -Id $gatewayJob.Id -Force -ErrorAction SilentlyContinue
}

# Start uvicorn with environment variables
$env:FASTAPI_HOST = $env:FASTAPI_HOST -or "127.0.0.1"
$env:FASTAPI_PORT = $env:FASTAPI_PORT -or "8000"

uvicorn app:app --host $env:FASTAPI_HOST --port $env:FASTAPI_PORT --reload

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "⛔ RoadWatch Traffic MVP - STOPPED" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cleanup
Stop-Process -Id $gatewayJob.Id -Force -ErrorAction SilentlyContinue

