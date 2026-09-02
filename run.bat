@echo off
title Mr. Drew's Device Optimizer & Memory Manager

cd /d "%~dp0"

where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw run.py %*
    exit /b 0
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    python run.py %*
    exit /b 0
)

echo [ERROR] Python is not installed or not in system PATH.
echo Please install Python 3.8+ from https://www.python.org or Microsoft Store.
pause
exit /b 1
