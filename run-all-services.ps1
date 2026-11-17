# ============================================================================
# RoadWatch Multi-Service Orchestrator
# ============================================================================
# Runs three independent services:
#   1. AI Gateway (port 9999) - OpenAI/Gemini adapter
#   2. Backend API (port 8001) - FastAPI REST endpoints only
#   3. Frontend UI (port 3000) - Streamlit web interface
#
# Each service runs in its own PowerShell window and can be stopped independently
# ============================================================================

param(
    [switch]$KeepOpen = $false  # Keep window open if service fails
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Load .env file
$envFile = Join-Path (Get-Location) ".env"
if (Test-Path $envFile) {
    Write-Host "✓ Loading configuration from .env" -ForegroundColor Green
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line -split '=', 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                Set-Item -Path "env:$key" -Value $value
            }
        }
    }
} else {
    Write-Host "⚠ .env file not found at $(Split-Path -Parent $envFile)" -ForegroundColor Yellow
}

# Set defaults
$env:APP_PROFILE ??= "local"
$env:ROADWATCH_REVIEWER_TOKEN ??= "demo-reviewer-token-mvp"

Write-Host @"
╔════════════════════════════════════════════════════════════════════╗
║          RoadWatch MVP - Multi-Service Orchestrator               ║
╠════════════════════════════════════════════════════════════════════╣
║ Config:                                                            ║
║   OpenAI Key: $(if ($env:OPENAI_API_KEY) { "✓ Set ($(($env:OPENAI_API_KEY).Substring(0, 10))...)" } else { "✗ Missing" })
║   Reviewer Token: $(if ($env:ROADWATCH_REVIEWER_TOKEN) { "✓ Set" } else { "✗ Missing" })
║   AI Gateway URL: $($env:AI_GATEWAY_URL)
╠════════════════════════════════════════════════════════════════════╣
║ Services:                                                          ║
║   [1] AI Gateway Service (port 9999)                               ║
║   [2] Backend API (port 8001)                                      ║
║   [3] Frontend UI (port 3000)                                      ║
╚════════════════════════════════════════════════════════════════════╝
"@

# Function to start a service in a new PowerShell window
function Start-Service {
    param(
        [string]$Name,
        [string]$Port,
        [scriptblock]$ScriptBlock,
        [hashtable]$Env = @{}
    )
    
    Write-Host "🚀 Starting $Name on port $Port..." -ForegroundColor Cyan
    
    $pwshPath = if ($PSVersionTable.PSVersion.Major -ge 7) { "pwsh.exe" } else { "powershell.exe" }
    $scriptStr = $ScriptBlock.ToString()
    
    # Create script that runs in new window with env vars
    $envScript = "
        `$ErrorActionPreference = 'Continue'
        `$WarningPreference = 'Continue'
        Write-Host `'========================================`' -ForegroundColor Cyan
        Write-Host `'$Name on port $Port`' -ForegroundColor Green
        Write-Host `'========================================`' -ForegroundColor Cyan
        Write-Host `'`' 
"
    
    # Add env vars
    foreach ($key in $Env.Keys) {
        $value = $Env[$key]
        $envScript += "`n        `$env:$key = `'$value`'"
    }
    
    $envScript += "`n        " + $scriptStr
    $envScript += "`n        Read-Host `'Press Enter to close this window`'"
    
    $bytes = [System.Text.Encoding]::Unicode.GetBytes($envScript)
    $encodedScript = [Convert]::ToBase64String($bytes)
    
    Start-Process $pwshPath -ArgumentList "-NoExit -EncodedCommand $encodedScript" -WindowStyle Normal
    Start-Sleep -Milliseconds 500
}

# Extract unique env vars for each service
$aiGatewayEnv = @{
    OPENAI_API_KEY = $env:OPENAI_API_KEY
    OPENAI_MODEL = $env:OPENAI_MODEL
    GEMINI_API_KEY = $env:GEMINI_API_KEY
    GEMINI_MODEL = $env:GEMINI_MODEL
    GATEWAY_TOKEN = $env:GATEWAY_TOKEN
    LOG_LEVEL = $env:LOG_LEVEL
}

$backendEnv = @{
    ROADWATCH_REVIEWER_TOKEN = $env:ROADWATCH_REVIEWER_TOKEN
    AI_GATEWAY_URL = $env:AI_GATEWAY_URL
    GATEWAY_TOKEN = $env:GATEWAY_TOKEN
    DATABASE_URL = $env:DATABASE_URL
    LOG_LEVEL = $env:LOG_LEVEL
}

$frontendEnv = @{
    BACKEND_API_URL = "http://127.0.0.1:8001"
    AI_GATEWAY_URL = $env:AI_GATEWAY_URL
}

try {
    # 1. Start AI Gateway
    Start-Service -Name "AI Gateway Service" -Port 9004 -Env $aiGatewayEnv -ScriptBlock {
        cd $pwd
        if (-Not (Test-Path .venv)) {
            Write-Host "Installing virtual environment..." -ForegroundColor Yellow
            python -m venv .venv
        }
        & ".\.venv\Scripts\Activate.ps1" 2>$null
        python -m pip install -q -r requirements.txt 2>$null
        Write-Host ""
        Write-Host "Starting AI Gateway Service..." -ForegroundColor Green
        Write-Host ""
        cd ai-gateway
        python -m uvicorn app:app --host 127.0.0.1 --port 9004
    }
    
    Start-Sleep -Seconds 3
    
    # 2. Start Backend API
    Start-Service -Name "Backend API" -Port 8001 -Env $backendEnv -ScriptBlock {
        cd $pwd
        if (-Not (Test-Path .venv)) {
            Write-Host "Installing virtual environment..." -ForegroundColor Yellow
            python -m venv .venv
        }
        & ".\.venv\Scripts\Activate.ps1" 2>$null
        python -m pip install -q -r requirements.txt 2>$null
        Write-Host ""
        Write-Host "Starting Backend API on http://127.0.0.1:8001" -ForegroundColor Green
        Write-Host "API Docs: http://127.0.0.1:8001/api/docs" -ForegroundColor Green
        Write-Host ""
        python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
    }
    
    Start-Sleep -Seconds 3
    
    # 3. Start Frontend
    Write-Host "📝 Frontend setup:" -ForegroundColor Cyan
    Write-Host "   To run the frontend, execute in a terminal:" -ForegroundColor Gray
    Write-Host "   npm install && npm start" -ForegroundColor Gray
    Write-Host "   Or use: python -m streamlit run frontend/app.py" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host @"
✓ Services started! 

Open in browser:
  API Docs:       http://127.0.0.1:8001/api/docs
  Citizen Portal: http://127.0.0.1:3000
  Officer Portal: http://127.0.0.1:3000/authority
  
AI Gateway:     http://127.0.0.1:9004 (internal)

Press Ctrl+C to stop this orchestrator. All services will remain running.
Use the individual service windows to view logs or stop specific services.
"@
    
    # Keep main window open
    while ($true) {
        Start-Sleep -Seconds 10
    }
    
} catch {
    Write-Host "❌ Error: $($_)" -ForegroundColor Red
    if ($KeepOpen) {
        Read-Host "Press Enter to close"
    }
    exit 1
}
