@echo off
REM RoadWatch MVP - Windows Startup Script
REM This script loads environment variables and starts all services

cd /d "%~dp0"

echo.
echo ========================================
echo RoadWatch MVP - Windows Startup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found in PATH
    exit /b 1
)

echo Creating virtual environment...
if not exist .venv (
    python -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ========================================
echo Loading Configuration
echo ========================================
echo.

REM Load .env into environment
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" (
        if not "%%a:~0,1%%"=="#" (
            set "%%a=%%b"
        )
    )
)

echo Configuration loaded:
echo   OPENAI_API_KEY=%OPENAI_API_KEY:~0,20%...
echo   GATEWAY_TOKEN=%GATEWAY_TOKEN%
echo   AI_GATEWAY_URL=%AI_GATEWAY_URL%
echo   FASTAPI_HOST=%FASTAPI_HOST%
echo   FASTAPI_PORT=%FASTAPI_PORT%
echo.

echo ========================================
echo Starting Services
echo ========================================
echo.

REM Clean database
if exist roadwatch.db del roadwatch.db
if exist roadwatch.db-shm del roadwatch.db-shm
if exist roadwatch.db-wal del roadwatch.db-wal

REM Bootstrap database
echo Initializing database...
python bootstrap.py

REM Start AI Gateway in separate window
echo Starting AI Gateway on port 9999...
start "RoadWatch - AI Gateway" python ai_gateway_mvp.py

REM Wait for gateway to start
timeout /t 3 /nobreak

REM Start FastAPI app
echo Starting FastAPI app on port 8000...
echo.
uvicorn app:app --host 127.0.0.1 --port 8000 --reload

REM Note: Press Ctrl+C to stop. Services in separate windows will keep running.
