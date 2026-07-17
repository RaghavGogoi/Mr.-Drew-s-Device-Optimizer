# Mr. Drew's Device Optimizer & Launch Prep Utility

A lightweight, low-overhead C++ command-line system resource optimizer designed specifically for game developers, software engineers, and gamers. This utility helps you maximize available system resources (RAM, CPU, and disk space) before launching demanding workloads like **Unreal Engine**, **Roblox Studio**, or heavy AAA games on Windows setups (especially laptops with dedicated GPUs like an RTX 4060).

---

## Features

- **Hardware-Aware Memory Thresholds:** Automatically detects total system RAM using the Windows API (`GlobalMemoryStatusEx`) and dynamically computes a target threshold:
  - Total RAM $\le$ 8 GB $\rightarrow$ 2 GB threshold.
  - Total RAM $\gt$ 8 GB & $\lt$ 16 GB $\rightarrow$ 3 GB threshold.
  - Total RAM $\ge$ 16 GB $\rightarrow$ 4 GB threshold.
- **Smart Process Killer:** Automatically terminates standard Windows background bloatware (Cortana, Widgets, Skype, Teams, OneDrive, YourPhone). Optionally prompts you to safely terminate active user apps (e.g., Discord, Spotify, Chrome, Edge, Firefox, Brave) before launching your workspace.
- **SSD Disk Cleanup:** Recursively and safely removes temporary files from both `%TEMP%` and `%SystemRoot%\Temp` directories. In-use/locked files are automatically bypassed to prevent application instability.
- **Standby Memory Purging:** Calls the undocumented NT kernel function `NtSetSystemInformation` (Class 80, Command 4: `MemoryPurgeStandbyList`) to free up RAM cached in the standby list.
- **Continuous Background Monitoring:** Enters a background monitoring loop that inspects available RAM every 60 seconds. If free memory drops below the dynamic threshold, it automatically triggers a standby RAM purge to keep your workspace smooth.
- **User-Friendly Console UI:** Professional styling using ANSI escape sequences with clear logging levels (`[INFO]`, `[SUCCESS]`, `[WARNING]`, `[ERROR]`).

---

## How It Works

Windows caches recently used files and programs in the **Standby List** of physical memory. While this speeds up access to those files, large compilers, game engines, and games often need large blocks of *completely free physical RAM* directly at launch. If they must wait for Windows to discard the Standby list page-by-page, it can cause transient stuttering, disk thrashing, or high paging file usage.

This utility elevates its process privileges to acquire `SeProfileSingleProcessPrivilege` (via `OpenProcessToken` and `AdjustTokenPrivileges`) and issues a command directly to the Windows Memory Manager to discard and flush these standby pages instantly.

---

## Requirements

1. **Operating System:** Windows 10 or Windows 11 (64-bit).
2. **Compiler:** A C++11 (or newer) compliant compiler:
   - **MSVC (Microsoft Visual C++):** Available via Visual Studio or Build Tools for Visual Studio.
   - **MinGW-w64 / GCC:** Version 7.0 or newer.
3. **Privileges:** You **MUST** run the compiled executable as an **Administrator** for the Standby RAM list flush to succeed.

---

## Build Instructions

Choose one of the methods below to build the project.

### Method 1: Using Microsoft Visual C++ Compiler (MSVC)
Open the **Developer Command Prompt for Visual Studio** and navigate to the directory containing `main.cpp`. Run:

```bash
cl.exe /EHsc /O2 main.cpp /Fe:DeviceOptimizer.exe
```

This compiles a highly optimized binary named `DeviceOptimizer.exe`.

### Method 2: Using GCC / MinGW-w64
Open a command prompt/terminal and compile:

```bash
g++ -O3 -std=c++11 main.cpp -o DeviceOptimizer.exe -lpsapi
```

*Note: If `g++` is not recognized (due to your PATH environment variable not reloading in the current terminal after installation), you can use the direct absolute path of the WinGet installation:*

```bash
& "C:\Users\Raghav Gogoi\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin\g++.exe" -O3 -std=c++11 main.cpp -o DeviceOptimizer.exe -lpsapi
```

---

## Run Instructions

1. Right-click on your command prompt (CMD, PowerShell, or Windows Terminal) and select **Run as Administrator**.
2. Run the compiled executable:
   ```bash
   .\DeviceOptimizer.exe
   ```
3. Follow the console prompt to select whether you want to terminate user applications (Discord, web browsers, etc.).
4. The tool will perform the initial optimization and enter the continuous 60-second monitoring loop in the background.

> [!CAUTION]
> Running this utility without Administrator privileges will restrict it from executing the Standby RAM flush due to Windows security policies. It will still perform the bloatware termination and temp folder cleanup, but will log access denied errors for standby memory operations.

---

## Ideal Use Cases

- **Engine Prep:** Clear out browser memory leaks and system cache before booting **Unreal Engine** or **Unity** editor.
- **Roblox Studio / VR Development:** Minimize background overhead when working with high-poly count simulations or running VR preview builds.
- **Gaming Launchpad:** Reclaim up to 4+ GB of standby RAM cache to mitigate stuttering in memory-intensive games (e.g., Cyberpunk 2077, Hogwarts Legacy) on modern gaming laptops.
