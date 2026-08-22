#!/usr/bin/env bash
echo "========================================================"
echo "  MR. DREW'S DEVICE OPTIMIZER - LINUX / MACOS LAUNCHER"
echo "========================================================"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "[ERROR] Python 3 is not installed or not in PATH."
    exit 1
fi

echo "[INFO] Installing / verifying dependencies..."
$PYTHON_BIN -m pip install -r requirements.txt --quiet 2>/dev/null

if command -v g++ &>/dev/null && [ ! -f "DeviceOptimizer" ]; then
    echo "[INFO] Compiling C++ native flusher engine (main.cpp -> DeviceOptimizer)..."
    g++ -O3 main.cpp -o DeviceOptimizer 2>/dev/null && chmod +x DeviceOptimizer
fi

echo "Launching Device Optimizer Obsidian Suite..."
$PYTHON_BIN app.py "$@"
