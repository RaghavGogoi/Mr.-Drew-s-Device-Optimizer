# Mr. Drew's Device & FPS Optimizer

A high-performance desktop application and standalone native CLI suite designed to optimize system memory, reduce latency, manage process priorities, and purge GPU shader caches on Windows workstations.

Built with a high-speed dual architecture combining a **Pure C++17 Kernel Engine** (`DeviceOptimizer.exe` and in-process `device_optimizer.dll`) for sub-millisecond Win32/NT system calls and a modern **PyWebView HTML5 Desktop Interface**.

---

## Technical Features

### Memory Management & Pure C++ Compaction
* **In-Process Working Set Compaction:** Direct C++ execution of Win32 `EmptyWorkingSet` across user-space processes (sub-15ms system-wide sweep) with critical system whitelist and game process protection.
* **Standby List Flushing:** Calls native `NtSetSystemInformation` with `SystemMemoryListInformation` via NT kernel to purge unreferenced standby cache memory in < 1ms.
* **Automated Background Daemon:** Continuously monitors available physical RAM and executes memory maintenance when free memory drops below configured thresholds.

### Gaming & Latency Optimization
* **High-Precision System Timer:** Locks Windows system timer resolution to 1.0 ms via `timeBeginPeriod` to minimize thread scheduling jitter and input latency.
* **CPU Priority Management:** Adjusts process scheduling priority classes to `HIGH_PRIORITY_CLASS` or `REALTIME_PRIORITY_CLASS` in pure C++.
* **Disk I/O Scheduling:** Configures NT `ProcessIoPriority` (Class 33 / `IoPriorityHigh`) to maximize disk read throughput and eliminate asset loading stutters.
* **GPU Shader Cache Sweeper:** Pure C++ `std::filesystem` directory cleaner for DirectX, OpenGL, Vulkan, NVIDIA (`DXCache`/`GLCache`), AMD, and Intel compiled shader caches.
* **Win32 Power Plan Management:** Instantly switches to Ultimate / High Performance power plans via Win32 `PowrProf` (`PowerSetActiveScheme`) with zero subprocess overhead.

### Interface & User Experience
* **Responsive HTML5 Engine:** Zero-dependency UI built with Vanilla CSS Grid/Flexbox layouts and native Web Audio API telemetry feedback.
* **Live Hardware & C++ Badges:** Displays real-time OS, Elevation (Standard/Admin), and Native C++ Engine status directly in the header.
* **Interactive Spotlight System:** Position-aware guided tour engine with element tracking, viewport bounds detection, and manual drag controls.
* **Custom Theme Pipeline:** Supports 6 visual themes (Obsidian, Cosmic, Emerald, Ember, OLED, Frost) with dynamic CSS custom property injection.

---

## Architecture & Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, Vanilla CSS3, JavaScript (ES6+) | Hardware-accelerated desktop view rendered inside PyWebView. |
| **Bridge API** | Python 3, `pywebview`, `ctypes` | In-process native C ABI loader binding directly to `device_optimizer.dll`. |
| **Native C++ Engine** | C++17 (MSVC / MinGW-w64 `g++`) | Dual-target codebase (`DeviceOptimizer.exe` standalone CLI & `device_optimizer.dll` shared library). |
| **Telemetry System** | Win32 / NT APIs (`GlobalMemoryStatusEx`, `GetPerformanceInfo`, `GetSystemTimes`) | Sub-millisecond physical RAM, standby list cache, and non-blocking CPU usage telemetry. |

---

## Standalone C++ CLI Usage

`DeviceOptimizer.exe` can be used completely independently of Python as a standalone, zero-dependency console optimizer:

```cmd
# Show system memory metrics, standby cache, and timer resolution
DeviceOptimizer.exe --sys-specs

# List top memory-consuming processes
DeviceOptimizer.exe --top-procs

# Run Gaming & FPS optimization pipeline (1ms timer lock, power plan, working set trim)
DeviceOptimizer.exe --fps-boost

# Run Monster Optimizer (deep RAM recovery, temp clean, shader sweep)
DeviceOptimizer.exe --monster

# Run 4GB Potato PC ultra-light preset
DeviceOptimizer.exe --potato

# Flush standby RAM list only
DeviceOptimizer.exe --flush-standby

# Compact working sets of background processes
DeviceOptimizer.exe --trim-ram

# Purge GPU shader caches across DirectX, NVIDIA, AMD, Intel
DeviceOptimizer.exe --clean-shaders

# Clear temporary directories and crash dumps
DeviceOptimizer.exe --clear-temp

# Terminate default background bloatware
DeviceOptimizer.exe --kill-bloat

# Boost a running game process to High CPU & I/O Priority
DeviceOptimizer.exe --boost-game "RobloxPlayerBeta.exe"
```

---

## Installation & Deployment

### Windows Setup

#### Prerequisites
* Windows 10 or Windows 11 (64-bit)
* Python 3.8 or higher
* MinGW-w64 `g++` or MSVC (optional, for compiling C++ kernel binary)

#### Quick Run
Execute the automated boot script from Command Prompt or PowerShell:

```cmd
git clone https://github.com/RaghavGogoi/Mr.-Drew-s-Device-Optimizer.git
cd "Mr.-Drew-s-Device-Optimizer"
run.bat
```

`run.bat` automatically verifies Python dependencies, compiles `main.cpp` into `DeviceOptimizer.exe` and `device_optimizer.dll` if `g++` is detected, and initializes the desktop application.

#### Manual C++ Compilation
To manually compile both the executable and shared library:

```cmd
# Standalone CLI executable
g++ -O3 -std=c++17 main.cpp -o DeviceOptimizer.exe -static -lpsapi -lwinmm -lpowrprof

# Native C ABI shared library (loaded in-process by Python)
g++ -DBUILD_DLL -O3 -std=c++17 -shared main.cpp -o device_optimizer.dll -static -lpsapi -lwinmm -lpowrprof
```

---

## Command Line & System Integration

### System Safety Protection
The application maintains an immutable whitelist of critical system processes (`explorer.exe`, `svchost.exe`, `lsass.exe`, `csrss.exe`) to prevent accidental process termination and ensure system stability.

### Directory Structure

```
Mr. Drew's Device Optimizer/
├── app.py                  # PyWebView main application entry point and JS bridge
├── config.py               # Application configuration persistence manager
├── optimizer_core.py       # Python system optimization interface with in-process C++ DLL bindings
├── main.cpp                # Native C++ optimization kernel source (CLI & DLL)
├── DeviceOptimizer.exe     # Compiled standalone C++ executable
├── device_optimizer.dll    # Compiled native in-process C shared library
├── tutorial_manager.py     # Tutorial definitions and guide reference
├── run.bat                 # Windows automated initialization script
├── run.py                  # Universal cross-platform launcher (auto-compiles C++ engine)
├── run.sh                  # Linux/macOS launcher script
├── tests/                  # Automated verification and unit test suite
├── gui/
│   ├── index.html          # Main HTML5 application container
│   ├── styles.css          # Theme system and layout stylesheets
│   ├── main.js             # Frontend application controller and interactive guide
│   └── assets/             # Application icons and branding assets
```

### Running Automated Tests

Run the test suite to verify the native engine, DLL bridge, API bridge, and optimization pipelines:

```cmd
python -m unittest discover tests -v
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
