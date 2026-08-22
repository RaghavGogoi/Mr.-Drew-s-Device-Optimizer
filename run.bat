@echo off
title Mr. Drew's Device Optimizer & Memory Manager (Obsidian Suite)
echo ========================================================
echo   MR. DREW'S DEVICE OPTIMIZER - OBSIDIAN SUITE LAUNCHER
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

:: Compile C++ Native Engine if compiler available and binary missing or outdated
where g++ >nul 2>&1
if %errorlevel% equ 0 (
    if not exist "DeviceOptimizer.exe" (
        echo [INFO] Compiling high-speed native C++ engine (main.cpp ^-> DeviceOptimizer.exe)...
        g++ -O3 main.cpp -o DeviceOptimizer.exe -lpsapi -lwinmm >nul 2>&1
        if exist "DeviceOptimizer.exe" (
            echo [SUCCESS] C++ Native Engine compiled successfully!
        )
    )
)

echo [INFO] Launching Device Optimizer Obsidian Suite...
python app.py %*
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application exited with code %errorlevel%.
    pause
)
