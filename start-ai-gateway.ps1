# Start AI Gateway with real OpenAI/Gemini integration
$ErrorActionPreference = "Stop"

Write-Host "Starting AI Gateway Service..." -ForegroundColor Green

# Ensure we're in the right directory
if (-Not (Test-Path ".\ai-gateway\app.py")) {
    Write-Host "ERROR: Must run from project root (ai-gateway/app.py not found)" -ForegroundColor Red
    exit 1
}

# Ensure venv is active
if (-Not (Test-Path .\.venv\Scripts\Activate.ps1)) {
    Write-Host "ERROR: Virtual environment not found. Run 'python -m venv .venv' first." -ForegroundColor Red
    exit 1
}

# Activate venv
.\.venv\Scripts\Activate.ps1

# Check for required API keys
if (-Not $env:OPENAI_API_KEY) {
    Write-Host "WARNING: OPENAI_API_KEY environment variable not set - OpenAI assessments will fail" -ForegroundColor Yellow
}

# Set gateway configuration
$env:AI_GATEWAY_TOKEN = 'tj5sT85gzRwNAHVDwC6und342OcscHdReGuFeZcFhq8'
$env:AI_PROVIDER = 'openai'
$env:AI_GATEWAY_PORT = '9004'

Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "  Service: AI Gateway (real assessments)"
Write-Host "  AI_PROVIDER: $env:AI_PROVIDER"
Write-Host "  AI_GATEWAY_PORT: $env:AI_GATEWAY_PORT"
Write-Host "  AI_GATEWAY_TOKEN: $($env:AI_GATEWAY_TOKEN.Substring(0, 10))..."
if ($env:OPENAI_API_KEY) {
    Write-Host "  OPENAI_API_KEY: $($env:OPENAI_API_KEY.Substring(0, 10))..."
}
Write-Host ""

# Start gateway from ai-gateway directory
Write-Host "Starting on http://127.0.0.1:$env:AI_GATEWAY_PORT (Ctrl+C to stop)" -ForegroundColor Yellow
cd ai-gateway
uvicorn app:app --host 127.0.0.1 --port $env:AI_GATEWAY_PORT --log-level info
