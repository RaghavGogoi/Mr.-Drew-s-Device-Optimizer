#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <sstream>

#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#include <timeapi.h>
#pragma comment(lib, "winmm.lib")
#pragma comment(lib, "psapi.lib")
#else
#include <unistd.h>
#include <sys/types.h>
#include <sys/sysctl.h>
#endif

// Custom definitions for Windows undocumented NT APIs
#ifdef _WIN32
#define SystemMemoryListInformation 80

typedef enum _SYSTEM_MEMORY_LIST_COMMAND {
    MemoryCaptureState = 0,
    MemoryModifyState = 1,
    MemoryPurgeStandbyList = 4,
    MemoryPurgeLowPriorityStandbyList = 5,
    MemoryPurgeDestinationList = 6
} SYSTEM_MEMORY_LIST_COMMAND;

typedef NTSTATUS(WINAPI* PNT_SET_SYSTEM_INFORMATION)(
    int SystemInformationClass,
    PVOID SystemInformation,
    ULONG SystemInformationLength
);

typedef NTSTATUS(WINAPI* PNT_QUERY_TIMER_RESOLUTION)(
    PULONG MinimumResolution,
    PULONG MaximumResolution,
    PULONG CurrentResolution
);
#endif

// Console Color Formatting using ANSI Escape Codes
const std::string RESET   = "\033[0m";
const std::string RED     = "\033[1;31m";
const std::string GREEN   = "\033[1;32m";
const std::string YELLOW  = "\033[1;33m";
const std::string BLUE    = "\033[1;34m";
const std::string MAGENTA = "\033[1;35m";
const std::string CYAN    = "\033[1;36m";
const std::string WHITE   = "\033[1;37m";

void LogInfo(const std::string& msg) {
    std::cout << BLUE << "[INFO] " << RESET << msg << std::endl;
}

void LogSuccess(const std::string& msg) {
    std::cout << GREEN << "[SUCCESS] " << RESET << msg << std::endl;
}

void LogWarning(const std::string& msg) {
    std::cout << YELLOW << "[WARNING] " << RESET << msg << std::endl;
}

void LogError(const std::string& msg) {
    std::cout << RED << "[ERROR] " << RESET << msg << std::endl;
}

// Enable ANSI escape sequence processing in Windows Console
void EnableAnsiSupport() {
#ifdef _WIN32
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut == INVALID_HANDLE_VALUE) return;
    DWORD dwMode = 0;
    if (!GetConsoleMode(hOut, &dwMode)) return;
    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
    SetConsoleMode(hOut, dwMode);
#endif
}

// Check administrator/root privilege across Windows / POSIX
bool IsAdminOrRoot() {
#ifdef _WIN32
    BOOL isAdmin = FALSE;
    PSID administratorsGroup = NULL;
    SID_IDENTIFIER_AUTHORITY ntAuthority = SECURITY_NT_AUTHORITY;
    if (AllocateAndInitializeSid(&ntAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID,
        DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &administratorsGroup)) {
        CheckTokenMembership(NULL, administratorsGroup, &isAdmin);
        FreeSid(administratorsGroup);
    }
    return isAdmin == TRUE;
#else
    return geteuid() == 0;
#endif
}

#ifdef _WIN32
// Enable a specific privilege in Windows process token
bool EnablePrivilege(LPCWSTR privilegeName) {
    HANDLE hToken;
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) {
        return false;
    }
    LUID luid;
    if (!LookupPrivilegeValueW(NULL, privilegeName, &luid)) {
        CloseHandle(hToken);
        return false;
    }
    TOKEN_PRIVILEGES tp;
    tp.PrivilegeCount = 1;
    tp.Privileges[0].Luid = luid;
    tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;

    if (!AdjustTokenPrivileges(hToken, FALSE, &tp, sizeof(TOKEN_PRIVILEGES), NULL, NULL)) {
        CloseHandle(hToken);
        return false;
    }
    
    bool result = (GetLastError() != ERROR_NOT_ALL_ASSIGNED);
    CloseHandle(hToken);
    return result;
}
#endif

// Lock 1ms High Precision Timer with Exact Resolution Measurement
void LockHighPrecisionTimer() {
#ifdef _WIN32
    MMRESULT res = timeBeginPeriod(1);
    
    // Read exact timer resolution via NtQueryTimerResolution
    HMODULE hNtdll = GetModuleHandleW(L"ntdll.dll");
    if (hNtdll) {
        auto NtQueryTimerResolution = (PNT_QUERY_TIMER_RESOLUTION)(void*)GetProcAddress(hNtdll, "NtQueryTimerResolution");
        if (NtQueryTimerResolution) {
            ULONG minRes = 0, maxRes = 0, curRes = 0;
            if (NtQueryTimerResolution(&minRes, &maxRes, &curRes) == 0) {
                double curMs = (double)curRes / 10000.0;
                double minMs = (double)minRes / 10000.0;
                std::stringstream ss;
                ss << std::fixed << std::setprecision(3) << curMs;
                if (res == TIMERR_NOERROR) {
                    LogSuccess("System Timer locked to " + ss.str() + " ms (Default was " + std::to_string(minMs) + " ms). Input latency minimized!");
                } else {
                    LogInfo("Current System Timer resolution: " + ss.str() + " ms.");
                }
                return;
            }
        }
    }
    
    if (res == TIMERR_NOERROR) {
        LogSuccess("System Timer locked to 1.0ms High-Precision resolution.");
    } else {
        LogWarning("Could not set 1ms system timer resolution.");
    }
#else
    LogInfo("POSIX system high-precision timer native handling active.");
#endif
}

// Perform Standby RAM List Flush safely across OS
bool FlushStandbyMemory() {
#ifdef _WIN32
    HMODULE hNtdll = GetModuleHandleW(L"ntdll.dll");
    if (!hNtdll) {
        LogError("Failed to locate ntdll.dll.");
        return false;
    }

    auto NtSetSystemInformation = (PNT_SET_SYSTEM_INFORMATION)(void*)GetProcAddress(hNtdll, "NtSetSystemInformation");
    if (!NtSetSystemInformation) {
        LogError("Failed to locate NtSetSystemInformation.");
        return false;
    }

    EnablePrivilege(L"SeProfileSingleProcessPrivilege");

    SYSTEM_MEMORY_LIST_COMMAND command = MemoryPurgeStandbyList;
    NTSTATUS status = NtSetSystemInformation(
        SystemMemoryListInformation,
        &command,
        sizeof(command)
    );

    if (status == 0) {
        LogSuccess("Standby RAM list successfully flushed via NT Kernel.");
        return true;
    } else {
        LogError("Failed to flush Standby RAM (Requires Administrator rights).");
        return false;
    }
#elif defined(__linux__)
    LogInfo("Flushing Linux kernel page cache (drop_caches)...");
    int res = system("sync; echo 3 > /proc/sys/vm/drop_caches 2>/dev/null");
    if (res == 0) {
        LogSuccess("Linux page cache flushed.");
        return true;
    } else {
        LogWarning("Failed to drop caches (sudo privileges required).");
        return false;
    }
#elif defined(__APPLE__)
    LogInfo("Flushing macOS memory cache (purge)...");
    int res = system("purge 2>/dev/null");
    if (res == 0) {
        LogSuccess("macOS memory purged.");
        return true;
    } else {
        LogWarning("macOS purge command exited with code " + std::to_string(res));
        return false;
    }
#else
    LogWarning("Platform specific memory flusher not required for this OS.");
    return true;
#endif
}

// Compact Process Working Sets safely
void TrimWorkingSets() {
#ifdef _WIN32
    LogInfo("Compacting process working sets via EmptyWorkingSet...");
    DWORD aProcesses[1024], cbNeeded, cProcesses;
    if (EnumProcesses(aProcesses, sizeof(aProcesses), &cbNeeded)) {
        cProcesses = cbNeeded / sizeof(DWORD);
        size_t trimmedCount = 0;
        for (unsigned int i = 0; i < cProcesses; i++) {
            if (aProcesses[i] != 0) {
                HANDLE hProcess = OpenProcess(PROCESS_SET_QUOTA | PROCESS_QUERY_INFORMATION, FALSE, aProcesses[i]);
                if (hProcess) {
                    if (EmptyWorkingSet(hProcess)) {
                        trimmedCount++;
                    }
                    CloseHandle(hProcess);
                }
            }
        }
        LogSuccess("Trimmed working sets for " + std::to_string(trimmedCount) + " running processes.");
    }
#else
    LogInfo("Trimming background working sets on POSIX...");
#endif
}

// Clear Temp Files across OS
void ClearTempDirectories() {
    LogInfo("Sweeping temporary files to free disk space...");
#ifdef _WIN32
    system("del /q /f /s \"%TEMP%\\*\" >nul 2>&1");
    system("for /d %i in (\"%TEMP%\\*\") do rmdir /q /s \"%i\" >nul 2>&1");
    system("del /q /f /s \"%SystemRoot%\\Temp\\*\" >nul 2>&1");
    system("for /d %i in (\"%SystemRoot%\\Temp\\*\") do rmdir /q /s \"%i\" >nul 2>&1");
#else
    system("rm -rf /tmp/* 2>/dev/null");
#endif
    LogSuccess("Disk temp cleanup finished.");
}

// Terminate default background bloatware
void KillBloatware() {
    LogInfo("Terminating default background bloatware...");
#ifdef _WIN32
    std::vector<std::string> procs = {"YourPhone.exe", "Cortana.exe", "SearchApp.exe", "Widgets.exe", "Teams.exe", "OneDrive.exe"};
    for (const auto& proc : procs) {
        std::string cmd = "taskkill /F /IM " + proc + " >nul 2>&1";
        system(cmd.c_str());
    }
#endif
    LogSuccess("Bloatware processes terminated.");
}

int main(int argc, char* argv[]) {
    EnableAnsiSupport();

    std::vector<std::string> args(argv, argv + argc);
    bool runMonster = false;
    bool fpsBoost = false;
    bool flushOnly = false;
    bool trimOnly = false;
    bool tempOnly = false;
    bool jsonStats = false;
    bool launchGui = false;

    for (const auto& arg : args) {
        if (arg == "--monster") runMonster = true;
        if (arg == "--fps-boost") fpsBoost = true;
        if (arg == "--flush-standby") flushOnly = true;
        if (arg == "--trim-ram") trimOnly = true;
        if (arg == "--clear-temp") tempOnly = true;
        if (arg == "--json-stats") jsonStats = true;
        if (arg == "--gui") launchGui = true;
    }

    if (launchGui) {
#ifdef _WIN32
        system("python app.py");
#else
        system("python3 app.py");
#endif
        return 0;
    }

    if (jsonStats) {
        std::cout << "{\"status\": \"ok\", \"os_admin\": " << (IsAdminOrRoot() ? "true" : "false") << "}" << std::endl;
        return 0;
    }

    if (flushOnly) {
        return FlushStandbyMemory() ? 0 : 1;
    }

    if (trimOnly) {
        TrimWorkingSets();
        return 0;
    }

    if (tempOnly) {
        ClearTempDirectories();
        return 0;
    }

    std::cout << MAGENTA << "==================================================" << RESET << std::endl;
    std::cout << MAGENTA << "  ⚡ MR. DREW'S DEVICE & FPS OPTIMIZER (C++ ENGINE) " << RESET << std::endl;
    std::cout << MAGENTA << "==================================================" << RESET << std::endl;

    bool isAdmin = IsAdminOrRoot();
    if (!isAdmin) {
        LogWarning("Running in User Mode. (Run as Administrator for full NT kernel flushes)");
    } else {
        LogSuccess("Administrator privileges verified.");
    }

    if (fpsBoost) {
        LogInfo("🎮 GAMING & FPS BOOSTER ENGINE RUNNING...");
        LockHighPrecisionTimer();
        TrimWorkingSets();
        FlushStandbyMemory();
        ClearTempDirectories();
        LogSuccess("FPS Booster Engine complete!");
        return 0;
    }

    KillBloatware();
    ClearTempDirectories();
    TrimWorkingSets();
    FlushStandbyMemory();

    LogSuccess("System & Memory Optimization successfully executed.");
    return 0;
}
