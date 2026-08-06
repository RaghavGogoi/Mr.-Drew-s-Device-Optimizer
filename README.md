# ⚡ Mr. Drew's Device Optimizer & Memory Manager

A modern, cross-platform Desktop GUI Application & system prep utility designed to intelligently optimize device performance, reclaim physical RAM, and purge bloatware before running demanding workloads like **Unreal Engine**, **Roblox Studio**, **Unity**, or **AAA Games**.

---

## ✨ Key Features

- 🚀 **Easiest One-Command Setup**:
  - **VSCode**: Simply open the workspace and press `Ctrl+Shift+B` or press `F5` to pull up and run the desktop application automatically!
  - **Windows**: Double-click `run.bat` or run `powershell -ExecutionPolicy Bypass -File .\scripts\install_and_run.ps1`.
  - **Linux & macOS**: Run `./run.sh`.
- 🧠 **Smart OS & RAM Adaptability Engine**:
  - Automatically detects OS (Windows 10/11, Linux distributions, macOS) and device physical RAM.
  - Dynamically calculates target free RAM thresholds:
    - **16 GB RAM System**: Automatically guarantees **$\ge$ 5.0 GB target free RAM**.
    - **8 GB RAM System**: Automatically targets **$\ge$ 3.0 GB free RAM**.
    - **32 GB RAM System**: Automatically targets **$\ge$ 10.0 GB free RAM**.
    - **64 GB RAM System**: Automatically targets **$\ge$ 20.0 GB free RAM**.
- 🔥 **Monster Optimizer Mode**:
  - High-yield multi-stage RAM recovery mode that preserves as much memory as possible without crashing or harming your system.
  - Safely compacts working sets of active processes, purges standby list cache, clears temporary files, and stops background bloatware.
  - Includes a strict **OS System Process Whitelist** (`System`, `explorer.exe`, `csrss.exe`, `lsass.exe`, `systemd`, `launchd`, etc.) ensuring 100% device safety and stability.
- 🖥️ **Full Desktop GUI Application**:
  - Includes a standalone visual desktop app (`app.py`) with dark glassmorphic styling, live memory progress gauge bar, real-time CPU/RAM status cards, auto-guard toggle, and logging console.

---

## 💻 Quick Start & One-Command Execution

### Method 1: VSCode One-Key Launch
Open the repository folder in VSCode:
1. Press `Ctrl+Shift+B` (or `Cmd+Shift+B` on macOS).
2. Or press `F5` to launch the **Device Optimizer GUI App** automatically.

### Method 2: Terminal / Console Command
Run the quick launcher for your OS:

#### Windows (CMD / PowerShell)
```cmd
.\run.bat
```
*or via PowerShell:*
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_and_run.ps1
```

#### Linux & macOS
```bash
chmod +x run.sh
./run.sh
```

---

## 🛡️ How Monster Optimizer Preserves RAM Safely

1. **Working Set Compression**: Calls OS memory APIs (`EmptyWorkingSet`) to force non-essential applications to dump unused cached memory back to physical RAM without closing them.
2. **Standby Memory Purging**: Flushes standby page cache via Windows NT Kernel (`NtSetSystemInformation` Class 80) or POSIX `drop_caches`/`purge`.
3. **Temp File Sweeper**: Automatically clears `%TEMP%` and `%SystemRoot%\Temp` files while safely bypassing locked/in-use files.
4. **Smart Process Management**: Automatically terminates bloatware (`OneDrive.exe`, `Widgets.exe`, `Teams.exe`, `Cortana.exe`, etc.) while protecting critical operating system services.

---

## 📁 Repository Structure

- [app.py](file:///c:/Users/Raghav%20Gogoi/Mr.%20Drew%27s%20Device%20Optimizer/app.py): Main Desktop GUI Application.
- [optimizer_core.py](file:///c:/Users/Raghav%20Gogoi/Mr.%20Drew%27s%20Device%20Optimizer/optimizer_core.py): Cross-platform OS & RAM smart adaptation engine with Monster Optimizer logic.
- [main.cpp](file:///c:/Users/Raghav%20Gogoi/Mr.%20Drew%27s%20Device%20Optimizer/main.cpp): Native C++ high-performance Windows flusher helper binary.
- [run.bat](file:///c:/Users/Raghav%20Gogoi/Mr.%20Drew%27s%20Device%20Optimizer/run.bat): One-click launcher for Windows.
- [run.sh](file:///c:/Users/Raghav%20Gogoi/Mr.%20Drew%27s%20Device%20Optimizer/run.sh): One-click launcher for Linux / macOS.
- [.vscode/tasks.json](file:///c:/Users/Raghav%20Gogoi/Mr.%20Drew%27s%20Device%20Optimizer/.vscode/tasks.json): Integrated VSCode tasks for one-key execution.
