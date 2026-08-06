# Mr. Drew's Device Optimizer & Memory Manager - PowerShell Auto-Installer & Runner
Write-Host "========================================================" -ForegroundColor Magenta
Write-Host "   MR. DREW'S DEVICE OPTIMIZER - AUTOMATED SETUP" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Magenta

# Check Python availability
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "[ERROR] Python is required but was not found in PATH." -ForegroundColor Red
    Write-Host "[INFO] Installing Python via WinGet..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
}

# Optional: Install psutil if pip is available
try {
    Write-Host "[INFO] Checking Python dependencies (psutil)..." -ForegroundColor Cyan
    python -m pip install psutil --quiet 2>$null
} catch {
    Write-Host "[NOTICE] Standard library fallback active." -ForegroundColor Yellow
}

# Run the GUI app
Write-Host "[SUCCESS] Launching Mr. Drew's Device Optimizer Application..." -ForegroundColor Green
python app.py
