# Mr. Drew's Device & FPS Optimizer

A high-performance desktop application designed to optimize system memory, reduce latency, manage process priorities, and manage GPU shader caches on Windows workstations.

Built with a dual architecture combining a **Native C++ Kernel Engine** (`DeviceOptimizer.exe`) for low-level Win32 system calls and a modern **PyWebView HTML5 Desktop Interface**.

---

## Technical Features

### Memory Management & Kernel Compaction
* **Working Set Compaction:** Invokes Win32 `EmptyWorkingSet` across user-space processes to purge unreferenced working set pages.
* **Standby List Flushing:** Calls native `NtSetSystemInformation` with `SystemMemoryListInformation` to release cached standby pages.
* **Automated Background Daemon:** Continuously monitors available physical RAM and executes memory maintenance when free memory drops below configured thresholds.

### Gaming & Latency Optimization
* **High-Precision System Timer:** Locks Windows system timer resolution to 1.0 ms via `timeBeginPeriod` to minimize thread scheduling latency.
* **CPU Priority Management:** Adjusts process scheduling priority classes to `HIGH_PRIORITY_CLASS` for active game executables.
* **Disk I/O Scheduling:** Configures `ProcessIoPriorityHigh` to prioritize disk read throughput for active gaming workloads.
* **GPU Shader Cache Management:** Sweeps DirectX, OpenGL, Vulkan, NVIDIA (DXCache/GLCache), AMD, and Intel compiled shader caches.

### Interface & User Experience
* **Responsive HTML5 Engine:** Zero-dependency UI built with Vanilla CSS Grid/Flexbox layouts and native Web Audio API telemetry feedback.
* **Interactive Spotlight System:** Position-aware guided tour engine with element tracking, viewport bounds detection, and manual drag controls.
* **Custom Theme Pipeline:** Supports 6 visual themes (Obsidian, Cosmic, Emerald, Ember, OLED, Frost) with dynamic CSS custom property injection.

---

## Architecture & Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, Vanilla CSS3, JavaScript (ES6+) | Hardware-accelerated desktop view rendered inside PyWebView. |
| **Bridge API** | Python 3, `pywebview` | Bi-directional JSON bridge between JS frontend and system services. |
| **Native Engine** | C++17 (MSVC / MinGW `g++`) | Win32 API kernel wrapper for high-speed privilege & memory operations. |
| **Telemetry System** | Windows API (`GlobalMemoryStatusEx`, `NtQuerySystemInformation`) | High-frequency physical RAM and CPU core usage polling. |

---

## Installation & Deployment

### Windows Setup

#### Prerequisites
* Windows 10 or Windows 11 (64-bit)
* Python 3.8 or higher
* MinGW `g++` or MSVC (optional, for compiling C++ kernel binary)

#### Quick Run
Execute the automated boot script from Command Prompt or PowerShell:

```cmd
git clone https://github.com/RaghavGogoi/Mr.-Drew-s-Device-Optimizer.git
cd "Mr.-Drew-s-Device-Optimizer"
run.bat
```

`run.bat` automatically verifies Python dependencies, compiles `main.cpp` into `DeviceOptimizer.exe` if a C++ compiler is detected, and initializes the desktop application.

---

## Command Line & System Integration

### System Safety Protection
The application maintains an immutable whitelist of critical system processes (`explorer.exe`, `svchost.exe`, `lsass.exe`, `csrss.exe`) to prevent accidental process termination and ensure system stability.

### Directory Structure

```
Mr. Drew's Device Optimizer/
├── app.py                  # PyWebView main application entry point and JS bridge
├── config.py               # Application configuration persistence manager
├── optimizer_core.py       # Python system optimization interface
├── main.cpp                # Native C++ optimization kernel source
├── tutorial_manager.py     # Tutorial definitions and guide reference
├── run.bat                 # Windows automated initialization script
├── run.py                  # Universal cross-platform launcher
├── run.sh                  # Linux/macOS launcher script
├── tests/                  # Automated verification and unit test suite
├── gui/
│   ├── index.html          # Main HTML5 application container
│   ├── styles.css          # Theme system and layout stylesheets
│   ├── main.js             # Frontend application controller and interactive guide
│   └── assets/             # Application icons and branding assets
```

### Running Automated Tests

Run the test suite to verify the native engine, API bridge, and optimization pipelines:

```cmd
python -m unittest discover tests -v
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
