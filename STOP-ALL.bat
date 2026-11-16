@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================
echo STOPPING ALL ROADWATCH SERVICES
echo ============================================
echo.

echo [1/2] Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Python processes stopped
) else (
    echo ℹ No Python processes running
)

echo [2/2] Stopping all Node processes...
taskkill /F /IM node.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Node processes stopped
) else (
    echo ℹ No Node processes running
)

echo.
echo ============================================
echo ALL SERVICES STOPPED
echo ============================================
echo.
echo Waiting 2 seconds before exit...
timeout /t 2 /nobreak
