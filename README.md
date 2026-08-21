# ⚡ Mr. Drew's Device & FPS Optimizer

A modern, cross-platform Desktop GUI Application & system prep utility designed to intelligently optimize device performance, boost gaming FPS, lower input latency, reclaim physical RAM, and purge background bloatware before running demanding games and workloads like **Unreal Engine**, **Roblox Studio**, **Unity**, **Fortnite**, **Valorant**, or **AAA Games**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-brightgreen.svg)
![Gaming FPS](https://img.shields.io/badge/FPS-Booster%20%26%20Latency-orange.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

---

## 🎮 What's New: FPS Booster & 4GB Potato PC Presets!

- 🚀 **High-FPS & Low Latency Gaming Engine**:
  - **1ms High-Precision System Timer**: Locks system timer resolution to 1.0ms (`timeBeginPeriod`) to eliminate micro-stutters and input lag.
  - **Ultimate / High Performance OS Power Scheme**: Forces Windows/Linux/macOS into maximum frequency state.
  - **GPU Shader Cache Cleaner**: Flushes Nvidia (`DXCache`, `GLCache`), AMD (`DxCache`), Intel, and DirectX shader caches to stop frame dropping and hitches.
  - **Game Process CPU Priority Booster**: Automatically boosts your active game process priority to `HIGH_PRIORITY_CLASS`.
- 🥔 **4GB "Potato Device" Ultra-Light Preset**:
  - Tailored low-RAM profile (targeting **1.5 GB - 2.0 GB free RAM** for 4GB machines).
  - Performs aggressive working-set compaction, drops inactive page caches, and stops telemetry processes to allow smooth gaming even on low-end hardware.
- 🖥️ **Super-Smart OS & GPU Detector**:
  - Automatically detects your OS (Windows 10/11, Linux distributions/SteamOS, macOS Apple Silicon & Intel).
  - Inspects physical/logical CPU cores and GPU vendor (Nvidia, AMD, Intel, Apple Metal) to apply custom hardware tweaks.

---

## 📥 How to Import & Run this Project from GitHub

Follow these simple, step-by-step instructions to clone, import, and launch the project on your machine.

---

### 🟢 Method 1: VSCode Terminal (Recommended)

1. **Open VSCode**.
2. Open the built-in terminal by pressing `Ctrl + ~` (or click **Terminal** -> **New Terminal** in the top menu).
3. Paste and run the following commands to clone and enter the project folder:
   ```bash
   git clone https://github.com/RaghavGogoi/Mr.-Drew-s-Device-Optimizer.git
   cd "Mr.-Drew-s-Device-Optimizer"
   ```
4. Run the one-click launcher:
   ```cmd
   .\run.bat
   ```
   *(On Windows, `run.bat` automatically verifies Python, installs required dependencies, requests Administrator privileges, and launches the app).*

---

### 🔵 Method 2: Windows Command Prompt (CMD)

1. Open **Command Prompt** (press `Win + R`, type `cmd`, and press `Enter`).
2. Clone and launch in one go:
   ```cmd
   git clone https://github.com/RaghavGogoi/Mr.-Drew-s-Device-Optimizer.git
   cd "Mr.-Drew-s-Device-Optimizer"
   run.bat
   ```

---

### 🔷 Method 3: Windows PowerShell

1. Open **PowerShell**.
2. Run the automated PowerShell installer & runner script:
   ```powershell
   git clone https://github.com/RaghavGogoi/Mr.-Drew-s-Device-Optimizer.git
   cd "Mr.-Drew-s-Device-Optimizer"
   powershell -ExecutionPolicy Bypass -File .\scripts\install_and_run.ps1
   ```

---

### 🐧 Method 4: Linux & macOS Terminal

1. Open your **Terminal**.
2. Clone and launch using the bash script:
   ```bash
   git clone https://github.com/RaghavGogoi/Mr.-Drew-s-Device-Optimizer.git
   cd "Mr.-Drew-s-Device-Optimizer"
   chmod +x run.sh
   ./run.sh
   ```
   *(For elevated kernel cache purging on Linux/macOS, run `sudo ./run.sh`)*.

---

### ⚡ Method 5: VSCode One-Key Launch (`Ctrl+Shift+B` or `F5`)

Once you have opened the project folder in VSCode (**File** -> **Open Folder** -> select `Mr.-Drew-s-Device-Optimizer`):
- Press **`Ctrl + Shift + B`** (or **`Cmd + Shift + B`** on macOS) to launch the app instantly.
- Or press **`F5`** to launch in Debug mode.

---

## ✨ Control Panel Features

- 🎮 **RUN FPS & GAME BOOSTER**:
  Runs the full gaming prep pipeline (1ms timer precision, Ultimate Power scheme, GPU shader cache clean, RAM recovery).
- 🥔 **4GB Potato Mode**:
  Triggers ultra-light 4GB RAM gaming preset tailored for budget/low-spec devices.
- ⚡ **Ultimate Power Mode**:
  Enables High/Ultimate performance OS power scheme.
- 🧹 **Clean Shader Cache**:
  Flushes DirectX, OpenGL, and Vulkan GPU shader caches.
- 🎯 **Boost Game Process Priority**:
  Select your active game process and elevate its CPU priority class to High.
- 🔥 **Monster Optimizer Mode**:
  High-yield multi-stage RAM recovery mode that compacts process working sets and flushes standby list cache.
- ✂️ **Trim App RAM**:
  Compacts active application working sets (`EmptyWorkingSet`), forcing unused cached memory back into free physical RAM without closing any apps.
- 🛡️ **Purge Standby RAM**:
  Flushes Windows NT Kernel standby page cache via `NtSetSystemInformation` or POSIX `drop_caches`.
- 🧹 **Clear Temp Files**:
  Safely sweeps system `%TEMP%` and `%SystemRoot%\Temp` directories while bypassing locked files.
- 🚫 **End Bloatware**:
  Terminates default background bloatware (`OneDrive.exe`, `Widgets.exe`, `Teams.exe`, `Cortana.exe`, etc.).
- 📊 **Top RAM Apps**:
  Displays a real-time list of top memory-consuming processes sorted by RAM usage.
- ⚡ **Smart Auto-Guard (60s Loop)**:
  Continuous background monitoring thread that automatically triggers Standby List flushing and memory compaction whenever free RAM drops below your target threshold.

---

## 🧠 Smart OS & RAM Adaptability Engine

The application automatically detects your operating system and total physical RAM specs to dynamically compute optimal free memory targets:

| Physical RAM | Device Profile | Smart Target Free RAM |
| :--- | :--- | :--- |
| **$\le$ 4 GB** | **🥔 Potato Device** | **$\ge$ 1.5 GB Free** |
| **8 GB** | **⚡ Budget PC** | **$\ge$ 3.0 GB Free** |
| **16 GB** | **🚀 Standard Rig** | **$\ge$ 5.0 GB Free** *(Guaranteed!)* |
| **32 GB+** | **🔥 Gaming Rig** | **$\ge$ 10.0 GB Free** |

---

## 🛡️ OS Safety Whitelist Guarantee

The optimizer incorporates a strict **System Process Whitelist** (`System`, `explorer.exe`, `csrss.exe`, `lsass.exe`, `svchost.exe`, `systemd`, `launchd`, etc.) ensuring **100% device stability**. It never touches critical OS processes.

---

## 📁 Repository Structure

```text
Mr.-Drew-s-Device-Optimizer/
├── app.py                   # Main Desktop GUI Application (Tkinter, Glassmorphic UI)
├── optimizer_core.py        # Cross-platform OS, RAM & FPS Smart Adaptation Engine
├── main.cpp                 # C++ Windows NT kernel standby flusher binary source
├── DeviceOptimizer.exe      # Compiled native helper binary
├── run.bat                  # One-click Windows CMD & Administrator launcher
├── run.sh                  # One-click Linux / macOS bash launcher
├── requirements.txt         # Python dependencies (psutil)
├── scripts/
│   └── install_and_run.ps1  # Automated PowerShell bootstrap installer & runner
└── .vscode/
    ├── launch.json          # VSCode F5 debug configuration
    └── tasks.json           # VSCode Ctrl+Shift+B one-key launcher task
```

---

## 📄 Requirements

- **Python 3.8+**
- `psutil` *(automatically installed by `run.bat` / `run.sh` / `install_and_run.ps1`)*

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
