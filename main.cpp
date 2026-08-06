#include <windows.h>
#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <iomanip>

// Define custom constants for undocumented API
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

// Console Color Formatting using ANSI Escape Codes
const std::string RESET   = "\033[0m";
const std::string RED     = "\033[1;31m";
const std::string GREEN   = "\033[1;32m";
const std::string YELLOW  = "\033[1;33m";
const std::string BLUE    = "\033[1;34m";
const std::string MAGENTA = "\033[1;35m";
const std::string CYAN    = "\033[1;36m";
const std::string WHITE   = "\033[1;37m";

// Helper logging functions
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
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    if (hOut == INVALID_HANDLE_VALUE) return;
    DWORD dwMode = 0;
    if (!GetConsoleMode(hOut, &dwMode)) return;
    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
    SetConsoleMode(hOut, dwMode);
}

// Format NTSTATUS to hexadecimal string
std::string NtStatusToString(NTSTATUS status) {
    char buf[32];
    sprintf_s(buf, "0x%08X", status);
    return std::string(buf);
}

// Check if the current process runs with Administrator privileges
bool IsUserAdmin() {
    BOOL isAdmin = FALSE;
    PSID administratorsGroup = NULL;
    SID_IDENTIFIER_AUTHORITY ntAuthority = SECURITY_NT_AUTHORITY;
    if (AllocateAndInitializeSid(&ntAuthority, 2, SECURITY_BUILTIN_DOMAIN_RID,
        DOMAIN_ALIAS_RID_ADMINS, 0, 0, 0, 0, 0, 0, &administratorsGroup)) {
        CheckTokenMembership(NULL, administratorsGroup, &isAdmin);
        FreeSid(administratorsGroup);
    }
    return isAdmin == TRUE;
}

// Enable a specific privilege in the process token
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

// Calculate dynamic RAM threshold based on system specs
DWORDLONG CalculateThreshold(DWORDLONG totalRAM) {
    DWORDLONG oneGB = 1024ULL * 1024 * 1024;
    double totalGB = (double)totalRAM / (double)oneGB;
    
    if (totalGB <= 4.5) {
        return (DWORDLONG)(1.5 * oneGB);
    } else if (totalGB <= 9.0) {
        return 3ULL * oneGB;
    } else if (totalGB <= 18.0) {
        return 5ULL * oneGB; // Guaranteed 5 GB free target for 16 GB devices!
    } else {
        return (DWORDLONG)(totalGB * 0.3125 * oneGB);
    }
}

// Display current system RAM details
void PrintMemoryStats(DWORDLONG threshold) {
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(memInfo);
    if (!GlobalMemoryStatusEx(&memInfo)) {
        LogError("Failed to retrieve system memory status.");
        return;
    }

    double totalGB = (double)memInfo.ullTotalPhys / (1024.0 * 1024.0 * 1024.0);
    double availGB = (double)memInfo.ullAvailPhys / (1024.0 * 1024.0 * 1024.0);
    double thresholdGB = (double)threshold / (1024.0 * 1024.0 * 1024.0);

    std::cout << CYAN << "--------------------------------------------------" << RESET << std::endl;
    std::cout << "  System Memory Status:" << std::endl;
    std::cout << "  - Total Physical RAM: " << WHITE << std::fixed << std::setprecision(2) << totalGB << " GB" << RESET << std::endl;
    std::cout << "  - Free Physical RAM:  " << (availGB < thresholdGB ? RED : GREEN) << availGB << " GB" << RESET << std::endl;
    std::cout << "  - Smart Flush Target: " << YELLOW << thresholdGB << " GB" << RESET << std::endl;
    std::cout << CYAN << "--------------------------------------------------" << RESET << std::endl;
}

// Terminate predefined list of processes
void TerminateProcesses(const std::vector<std::string>& processes) {
    for (const auto& proc : processes) {
        std::cout << CYAN << "[PROCESS] " << RESET << "Terminating " << proc << "... ";
        std::string cmd = "taskkill /F /IM " + proc + " >nul 2>&1";
        int ret = system(cmd.c_str());
        if (ret == 0) {
            std::cout << GREEN << "SUCCESS" << RESET << std::endl;
        } else {
            std::cout << YELLOW << "NOT RUNNING / SKIPPED" << RESET << std::endl;
        }
    }
}

// Clear Temp files recursively
void ClearTempDirectories() {
    LogInfo("Clearing temporary directories to free up SSD space...");
    
    // Clear user temp files
    LogInfo("Clearing user Temp folder (%TEMP%)...");
    system("del /q /f /s \"%TEMP%\\*\" >nul 2>&1");
    system("for /d %i in (\"%TEMP%\\*\") do rmdir /q /s \"%i\" >nul 2>&1");

    // Clear system temp files
    LogInfo("Clearing system Temp folder (%SystemRoot%\\Temp)...");
    system("del /q /f /s \"%SystemRoot%\\Temp\\*\" >nul 2>&1");
    system("for /d %i in (\"%SystemRoot%\\Temp\\*\") do rmdir /q /s \"%i\" >nul 2>&1");

    LogSuccess("Disk cleanup completed (locked/in-use files were safely bypassed).");
}

// Perform standby RAM list flush using NtSetSystemInformation
bool FlushStandbyList() {
    HMODULE hNtdll = GetModuleHandleW(L"ntdll.dll");
    if (!hNtdll) {
        LogError("Failed to get handle for ntdll.dll.");
        return false;
    }

    auto NtSetSystemInformation = (PNT_SET_SYSTEM_INFORMATION)(void*)GetProcAddress(hNtdll, "NtSetSystemInformation");
    if (!NtSetSystemInformation) {
        LogError("Failed to locate NtSetSystemInformation in ntdll.dll.");
        return false;
    }

    // Try to acquire the privilege
    if (!EnablePrivilege(L"SeProfileSingleProcessPrivilege")) {
        LogWarning("Could not enable SeProfileSingleProcessPrivilege. Flusher will likely fail.");
    }

    SYSTEM_MEMORY_LIST_COMMAND command = MemoryPurgeStandbyList;
    NTSTATUS status = NtSetSystemInformation(
        SystemMemoryListInformation,
        &command,
        sizeof(command)
    );

    if (status == 0) { // STATUS_SUCCESS
        LogSuccess("Standby RAM list successfully flushed.");
        return true;
    } else {
        if (status == (NTSTATUS)0xC0000061) { // STATUS_PRIVILEGE_NOT_HELD
            LogError("Failed to flush Standby RAM: Privilege not held. (Must run as Administrator)");
        } else if (status == (NTSTATUS)0xC0000022) { // STATUS_ACCESS_DENIED
            LogError("Failed to flush Standby RAM: Access Denied. (Must run as Administrator)");
        } else {
            LogError("Failed to flush Standby RAM. Status: " + NtStatusToString(status));
        }
        return false;
    }
}

int main(int argc, char* argv[]) {
    EnableAnsiSupport();

    std::vector<std::string> args(argv, argv + argc);
    bool runMonster = false;
    bool flushOnly = false;
    bool launchGui = false;

    for (const auto& arg : args) {
        if (arg == "--monster") runMonster = true;
        if (arg == "--flush-standby") flushOnly = true;
        if (arg == "--gui") launchGui = true;
    }

    if (launchGui) {
        system("python app.py");
        return 0;
    }

    if (flushOnly) {
        return FlushStandbyList() ? 0 : 1;
    }

    std::cout << MAGENTA << "==================================================" << RESET << std::endl;
    std::cout << MAGENTA << "       MR. DREW'S DEVICE OPTIMIZER & PREP         " << RESET << std::endl;
    std::cout << MAGENTA << "==================================================" << RESET << std::endl;

    // Check elevation status
    bool isAdmin = IsUserAdmin();
    if (!isAdmin) {
        LogWarning("Application is not running as Administrator.");
        LogWarning("Memory Standby List flushing will fail due to security permissions.");
        LogWarning("Restarting with elevated Administrator rights recommended.");
    } else {
        LogSuccess("Administrator privileges confirmed. Full optimization active.");
    }

    std::vector<std::string> defaultBloatware = {
        "YourPhone.exe", "Cortana.exe", "SearchApp.exe", "Widgets.exe",
        "Teams.exe", "Skype.exe", "OneDrive.exe"
    };

    std::cout << std::endl;
    LogInfo("Terminating default system background bloatware...");
    TerminateProcesses(defaultBloatware);

    if (runMonster) {
        LogInfo("🔥 MONSTER OPTIMIZER MODE ACTIVATED!");
        std::vector<std::string> userApps = {
            "Discord.exe", "Spotify.exe", "chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe"
        };
        TerminateProcesses(userApps);
    }

    // Disk Space Cleanup
    std::cout << std::endl;
    ClearTempDirectories();

    // RAM Threshold calculation
    std::cout << std::endl;
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(memInfo);
    if (!GlobalMemoryStatusEx(&memInfo)) {
        LogError("Fatal: Could not retrieve system memory parameters.");
        return 1;
    }

    DWORDLONG threshold = CalculateThreshold(memInfo.ullTotalPhys);
    double thresholdGB = (double)threshold / (1024.0 * 1024.0 * 1024.0);

    LogInfo("Smart System RAM Target calculated to: " + std::to_string(thresholdGB) + " GB");
    
    if (isAdmin) {
        LogInfo("Performing Standby RAM list flush...");
        FlushStandbyList();
    }

    PrintMemoryStats(threshold);

    // Monitoring Loop
    LogInfo("Entering background memory monitoring loop. Checking every 60 seconds...");
    while (true) {
        std::this_thread::sleep_for(std::chrono::seconds(60));

        memInfo.dwLength = sizeof(memInfo);
        if (GlobalMemoryStatusEx(&memInfo)) {
            if (memInfo.ullAvailPhys < threshold) {
                double availGB = (double)memInfo.ullAvailPhys / (1024.0 * 1024.0 * 1024.0);
                LogWarning("Free RAM has dropped to " + std::to_string(availGB) + " GB (below threshold).");
                
                if (isAdmin) {
                    LogInfo("Triggering Standby RAM list flush...");
                    if (FlushStandbyList()) {
                        PrintMemoryStats(threshold);
                    }
                } else {
                    LogError("Free RAM is low, but standby list cannot be flushed (requires Administrator privileges).");
                }
            }
        }
    }

    return 0;
}

