# Contributing to Mr. Drew's Device & FPS Optimizer

Thank you for your interest in contributing to Mr. Drew's Device Optimizer! We welcome community contributions to make this software faster, safer, and accessible to everyone worldwide.

---

## Code of Conduct

All contributors and community participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat all members with respect and professionalism.

---

## Getting Started

### 1. Prerequisites
* **Operating System:** Windows 10/11 (64-bit recommended for Win32/NT kernel development), Linux, or macOS.
* **Python:** Version 3.8 or higher.
* **C++ Compiler:** MinGW-w64 `g++` (version 9+ supporting C++17) or Microsoft Visual C++ (MSVC).

### 2. Setting Up Your Development Environment
```cmd
# Clone repository
git clone https://github.com/RaghavGogoi/Mr.-Drew-s-Device-Optimizer.git
cd "Mr.-Drew-s-Device-Optimizer"

# Install development dependencies
pip install -r requirements.txt

# Run the automated build and test runner
run.bat
```

### 3. Recompiling Native C++ Kernel Binaries
```cmd
# Compile standalone CLI binary
g++ -O3 -std=c++17 main.cpp -o DeviceOptimizer.exe -static -lpsapi -lwinmm -lpowrprof -lshell32

# Compile native shared library (device_optimizer.dll)
g++ -DBUILD_DLL -O3 -std=c++17 -shared main.cpp -o device_optimizer.dll -static -lpsapi -lwinmm -lpowrprof -lshell32
```

---

## Coding Standards

### C++ Architecture (`main.cpp`)
* Code must be compliant with **C++17**.
* Always check Win32 / NT API return values and handles (`INVALID_HANDLE_VALUE`, `NULL`).
* Always close handles with `CloseHandle()` or use RAII wrappers to avoid resource leaks.
* Whitelist protection must never be compromised or bypassed under any circumstances.
* Use static linking flags (`-static`) to avoid external MinGW runtime DLL dependencies.

### Python Bridge (`app.py`, `optimizer_core.py`, `config.py`)
* Maintain type annotations across public methods.
* Keep all background threads as daemon threads (`daemon=True`) to guarantee clean process shutdown.
* Never hardcode user file paths; use `os.path` and `get_resource_path()` for frozen/standalone compatibility.

### Frontend UI (`gui/`)
* Zero external JavaScript framework dependencies: use modern Vanilla ES6+ standards.
* Respect low-power mode and visibility events to avoid burning CPU cycles when minimized.

---

## Running Tests

Before submitting any Pull Request, ensure that all tests pass:

```cmd
python -m unittest discover tests -v
```

---

## Submitting Pull Requests

1. Fork the repository and create your feature branch: `git checkout -b feature/amazing-feature`.
2. Commit your changes: `git commit -m 'feat: add amazing feature'`.
3. Push to the branch: `git push origin feature/amazing-feature`.
4. Open a Pull Request referencing any relevant issues.
