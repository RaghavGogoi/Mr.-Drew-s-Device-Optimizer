#!/usr/bin/env bash
echo "========================================================"
echo "  MR. DREW'S DEVICE OPTIMIZER - LINUX / MACOS LAUNCHER"
echo "========================================================"

if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "[ERROR] Python is not installed or not in PATH."
    exit 1
fi

echo "Launching Device Optimizer GUI..."
$PYTHON_BIN app.py "$@"
