# Mr. Drew's Device Optimizer & Memory Manager - PowerShell Auto-Installer & Runner
Write-Host "========================================================" -ForegroundColor Magenta
Write-Host "   MR. DREW'S DEVICE OPTIMIZER - AUTOMATED SETUP" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Magenta

# Set Working Directory
Set-Location -Path $PSScriptRoot\..

# Check Python availability
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "[ERROR] Python is required but was not found in PATH." -ForegroundColor Red
    Write-Host "[INFO] Installing Python via WinGet..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
}

# Install requirements
try {
    Write-Host "[INFO] Checking Python dependencies (psutil)..." -ForegroundColor Cyan
    python -m pip install -r requirements.txt --quiet 2>$null
} catch {
    Write-Host "[NOTICE] Standard library fallback active." -ForegroundColor Yellow
}

# Run GUI application
Write-Host "[SUCCESS] Launching Mr. Drew's Device Optimizer Application..." -ForegroundColor Green
python app.py
