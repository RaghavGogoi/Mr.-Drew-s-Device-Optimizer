@echo off
title Mr. Drew's Device Optimizer & Memory Manager
echo ========================================================
echo   MR. DREW'S DEVICE OPTIMIZER - QUICK LAUNCHER
echo ========================================================
echo Checking Python environment...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in PATH. Please install Python 3.x.
    pause
    exit /b 1
)

echo Starting Device Optimizer Desktop GUI Application...
start "" python app.py %*
exit /b 0
