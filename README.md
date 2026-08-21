# ⚡ Mr. Drew's Device Optimizer & Memory Manager

A modern, cross-platform Desktop GUI Application & system prep utility designed to intelligently optimize device performance, reclaim physical RAM, and purge background bloatware before running demanding workloads like **Unreal Engine**, **Roblox Studio**, **Unity**, or **AAA Games**.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

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

## ✨ Features & Interactive Control Panel

- 🔥 **Monster Optimizer Mode**:
  High-yield multi-stage memory recovery. Compacts process working sets, flushes standby page cache, cleans temp files, and terminates bloatware in one click.
- ✂️ **Trim App RAM**:
  Compacts active application working sets (`EmptyWorkingSet`), forcing unused cached memory back into free physical RAM without closing any apps.
- 🛡️ **Purge Standby RAM**:
  Flushes Windows NT Kernel standby page cache via `NtSetSystemInformation` or POSIX `drop_caches`.
- 🧹 **Clear Temp Files**:
  Safely sweeps system `%TEMP%` and `%SystemRoot%\Temp` directories while bypassing locked files.
- 🚫 **End Bloatware**:
  Terminates default background bloatware (`OneDrive.exe`, `Widgets.exe`, `Teams.exe`, `Cortana.exe`, etc.) while protecting critical system services.
- 📊 **Top RAM Apps**:
  Displays a real-time list of top memory-consuming processes sorted by RAM usage.
- ⚡ **Smart Auto-Guard (60s Loop)**:
  Continuous background monitoring thread that automatically triggers Standby List flushing and memory compaction whenever free RAM drops below your target threshold.
- 🔄 **Refresh Stats**:
  Instantly updates live RAM availability and CPU utilization metrics.
- 🗑️ **Clear Console** & 📋 **Copy Log**:
  Quick management controls to copy execution logs or clear the console widget.

---

## 🧠 Smart OS & RAM Adaptability Engine

The application automatically detects your operating system and total physical RAM specs to dynamically compute optimal free memory targets:

| Physical RAM | Smart Target Free RAM |
| :--- | :--- |
| **$\le$ 4 GB** | **$\ge$ 1.5 GB Free** |
| **8 GB** | **$\ge$ 3.0 GB Free** |
| **16 GB** | **$\ge$ 5.0 GB Free** *(Guaranteed!)* |
| **32 GB** | **$\ge$ 10.0 GB Free** |
| **64 GB+** | **$\ge$ 20.0 GB Free** |

---

## 🛡️ OS Safety Whitelist Guarantee

The optimizer incorporates a strict **System Process Whitelist** (`System`, `explorer.exe`, `csrss.exe`, `lsass.exe`, `svchost.exe`, `systemd`, `launchd`, etc.) ensuring **100% device stability**. It never touches critical OS processes.

---

## 📁 Repository Structure

```text
Mr.-Drew-s-Device-Optimizer/
├── app.py                   # Main Desktop GUI Application (Tkinter, Glassmorphic UI)
├── optimizer_core.py        # Cross-platform OS & RAM Smart Adaptation Engine
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
