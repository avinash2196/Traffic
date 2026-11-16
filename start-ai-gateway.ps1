# Start AI Gateway MVP with real API integration
$ErrorActionPreference = "Stop"

Write-Host "Starting AI Gateway MVP..." -ForegroundColor Green

# Ensure venv is active
if (-Not (Test-Path .\.venv\Scripts\Activate.ps1)) {
    Write-Host "ERROR: Virtual environment not found. Run 'python -m venv .venv' first." -ForegroundColor Red
    exit 1
}

# Activate venv
.\.venv\Scripts\Activate.ps1

# Check for required API keys
if (-Not $env:OPENAI_API_KEY) {
    Write-Host "ERROR: OPENAI_API_KEY environment variable not set" -ForegroundColor Red
    exit 1
}

# Set gateway configuration
$env:AI_GATEWAY_TOKEN = 'tj5sT85gzRwNAHVDwC6und342OcscHdReGuFeZcFhq8'
$env:AI_PROVIDER = 'openai'

Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  AI_PROVIDER: $env:AI_PROVIDER"
Write-Host "  AI_GATEWAY_TOKEN: $($env:AI_GATEWAY_TOKEN.Substring(0, 10))..."
Write-Host "  OPENAI_API_KEY: $($env:OPENAI_API_KEY.Substring(0, 10))..."
Write-Host ""

# Start gateway
Write-Host "Starting on http://127.0.0.1:9999 (Ctrl+C to stop)" -ForegroundColor Yellow
uvicorn ai_gateway_mvp:app --host 127.0.0.1 --port 9999 --log-level info
