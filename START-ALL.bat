@echo off
REM RoadWatch Traffic MVP - One-Click Startup
REM This batch file launches the PowerShell startup script

cd /d "%~dp0"

echo.
echo ================================================================
echo         RoadWatch Traffic MVP - Startup
echo ================================================================
echo.
echo Starting PowerShell startup script...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File START-ALL.ps1

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start services
    echo.
    pause
)
