@echo off
title Mr. Drew's Device Optimizer & Memory Manager

cd /d "%~dp0"

:: 1. Launch standalone executable directly if present (instant, zero Python requirement)
if exist "DeviceOptimizerGUI.exe" (
    start "" "DeviceOptimizerGUI.exe" %*
    exit /b 0
)

if exist "dist\DeviceOptimizerGUI\DeviceOptimizerGUI.exe" (
    start "" "dist\DeviceOptimizerGUI\DeviceOptimizerGUI.exe" %*
    exit /b 0
)

:: 2. Check for pythonw in PATH (windowed, clean, no console flash)
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw run.py %*
    exit /b 0
)

:: 3. Check for standard python in PATH
where python >nul 2>&1
if %errorlevel% equ 0 (
    python run.py %*
    exit /b 0
)

:: 4. Check for official Windows py launcher
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 run.py %*
    exit /b 0
)

:: 5. Check common Python installation paths
for %%P in (
    "%LocalAppData%\Programs\Python\Python313\pythonw.exe"
    "%LocalAppData%\Programs\Python\Python312\pythonw.exe"
    "%LocalAppData%\Programs\Python\Python311\pythonw.exe"
    "%LocalAppData%\Programs\Python\Python310\pythonw.exe"
    "%LocalAppData%\Programs\Python\Python39\pythonw.exe"
    "%LocalAppData%\Programs\Python\Python38\pythonw.exe"
    "C:\Program Files\Python313\pythonw.exe"
    "C:\Program Files\Python312\pythonw.exe"
    "C:\Program Files\Python311\pythonw.exe"
    "C:\Program Files\Python310\pythonw.exe"
) do (
    if exist "%%~P" (
        start "" "%%~P" run.py %*
        exit /b 0
    )
)

:: 6. Fallback to native C++ executable
if exist "DeviceOptimizer.exe" (
    echo [INFO] Python runtime not detected in PATH.
    echo [INFO] Launching high-speed C++ Native Engine...
    DeviceOptimizer.exe %*
    exit /b 0
)

echo [ERROR] No Python runtime or standalone executable found.
echo Please install Python 3.8+ from https://www.python.org or run DeviceOptimizer.exe.
pause
exit /b 1
