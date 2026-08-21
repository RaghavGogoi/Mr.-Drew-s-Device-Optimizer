@echo off
title Mr. Drew's Device Optimizer & Memory Manager
echo ========================================================
echo   MR. DREW'S DEVICE OPTIMIZER - QUICK LAUNCHER
echo ========================================================

:: Ensure working directory is directory of this script
cd /d "%~dp0"

:: Check Python availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in system PATH.
    echo Please install Python 3.8+ from https://www.python.org or Microsoft Store.
    pause
    exit /b 1
)

:: Install/verify dependencies
echo [INFO] Verifying Python dependencies...
python -m pip install -r requirements.txt --quiet >nul 2>&1

:: Check for Administrator Privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Requesting Administrator Privileges (UAC)...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b 0
)

echo Starting Device Optimizer Desktop GUI Application as Administrator...
python app.py %*
if %errorlevel% neq 0 (
    echo [ERROR] Application exited with code %errorlevel%.
    pause
)
