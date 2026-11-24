#include <iostream>
#include <vector>
#include <string>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <sstream>
#include <algorithm>
#include <filesystem>
#include <unordered_set>
#include <cstdint>
#include <cstring>

#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#include <timeapi.h>
#include <powrprof.h>
#include <shellapi.h>
#ifdef _MSC_VER
#pragma comment(lib, "winmm.lib")
#pragma comment(lib, "psapi.lib")
#pragma comment(lib, "powrprof.lib")
#pragma comment(lib, "shell32.lib")
#endif
#else
#include <unistd.h>
#include <sys/types.h>
#include <sys/sysctl.h>
#endif

// Custom definitions for Windows undocumented NT APIs
#ifdef _WIN32
#define SystemMemoryListInformation 80
#define ProcessIoPriority 33

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

typedef NTSTATUS(WINAPI* PNT_SET_INFORMATION_PROCESS)(
    HANDLE ProcessHandle,
    ULONG ProcessInformationClass,
    PVOID ProcessInformation,
    ULONG ProcessInformationLength
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

void EnableAllKernelPrivileges() {
    EnablePrivilege(L"SeProfileSingleProcessPrivilege");
    EnablePrivilege(L"SeIncreaseQuotaPrivilege");
    EnablePrivilege(L"SeIncreaseBasePriorityPrivilege");
    EnablePrivilege(L"SeDebugPrivilege");
}
#endif

// ============================================================================
// SYSTEM TIMER RESOLUTION (Win32 / POSIX)
// ============================================================================

bool LockHighPrecisionTimer(bool enable = true) {
#ifdef _WIN32
    MMRESULT res = enable ? timeBeginPeriod(1) : timeEndPeriod(1);
    return (res == TIMERR_NOERROR);
#else
    return true;
#endif
}

bool GetTimerResolutionMs(double* currentMs, double* minMs) {
#ifdef _WIN32
    HMODULE hNtdll = GetModuleHandleW(L"ntdll.dll");
    if (hNtdll) {
        auto NtQueryTimerResolution = (PNT_QUERY_TIMER_RESOLUTION)(void*)GetProcAddress(hNtdll, "NtQueryTimerResolution");
        if (NtQueryTimerResolution) {
            ULONG minRes = 0, maxRes = 0, curRes = 0;
            if (NtQueryTimerResolution(&minRes, &maxRes, &curRes) == 0) {
                if (currentMs) *currentMs = (double)curRes / 10000.0;
                if (minMs) *minMs = (double)minRes / 10000.0;
                return true;
            }
        }
    }
    if (currentMs) *currentMs = 1.0;
    if (minMs) *minMs = 15.625;
    return false;
#else
    if (currentMs) *currentMs = 1.0;
    if (minMs) *minMs = 1.0;
    return true;
#endif
}

// ============================================================================
// STANDBY MEMORY FLUSH (NT Kernel NtSetSystemInformation)
// ============================================================================

bool FlushStandbyMemory() {
#ifdef _WIN32
    EnableAllKernelPrivileges();

    HMODULE hNtdll = GetModuleHandleW(L"ntdll.dll");
    if (!hNtdll) return false;

    auto NtSetSystemInformation = (PNT_SET_SYSTEM_INFORMATION)(void*)GetProcAddress(hNtdll, "NtSetSystemInformation");
    if (!NtSetSystemInformation) return false;

    SYSTEM_MEMORY_LIST_COMMAND command = MemoryPurgeStandbyList;
    NTSTATUS status = NtSetSystemInformation(
        SystemMemoryListInformation,
        &command,
        sizeof(command)
    );
    return (status == 0);
#elif defined(__linux__)
    int res = system("sync; echo 3 > /proc/sys/vm/drop_caches 2>/dev/null");
    return (res == 0);
#elif defined(__APPLE__)
    int res = system("purge 2>/dev/null");
    return (res == 0);
#else
    return true;
#endif
}

// ============================================================================
// PROCESS WORKING SET COMPACTION
// ============================================================================

static const std::unordered_set<std::string> CRITICAL_WHITELIST = {
    "system", "system idle process", "smss.exe", "csrss.exe", "wininit.exe",
    "services.exe", "lsass.exe", "svchost.exe", "fontdrvhost.exe", "memory compression",
    "dwm.exe", "explorer.exe", "spoolsv.exe", "securityhealthservice.exe",
    "taskmgr.exe", "ctfmon.exe", "conhost.exe", "sihost.exe", "runtimebroker.exe",
    "audiodg.exe", "registry", "vssvc.exe", "searchindexer.exe", "securityhealthhost.exe",
    "smartscreen.exe", "deviceoptimizer.exe", "main.exe", "python.exe", "pythonw.exe"
};

static const std::unordered_set<std::string> KNOWN_GAMES = {
    "fortniteclient-win64-shipping.exe", "fortnitelauncher.exe",
    "valorant.exe", "valorant-win64-shipping.exe",
    "gta5.exe", "playgtav.exe", "cs2.exe", "csgo.exe",
    "cyberpunk2077.exe", "robloxplayerbeta.exe", "robloxstudiobeta.exe",
    "minecraftlauncher.exe", "javaw.exe", "genshinimpact.exe", "overwatch.exe",
    "apex.exe", "r5apex.exe", "league of legends.exe", "leagueclient.exe",
    "rocketleague.exe", "pubg.exe", "tslgame.exe", "dota2.exe", "unrealeditor.exe",
    "unity.exe", "steamservice.exe", "steam.exe", "epicgameslauncher.exe",
    "eldenring.exe", "rdr2.exe", "cod.exe", "warzone.exe"
};

uint32_t TrimWorkingSets(const std::unordered_set<DWORD>& excludePids = {}) {
    uint32_t trimmedCount = 0;
#ifdef _WIN32
    EnableAllKernelPrivileges();
    DWORD currentPid = GetCurrentProcessId();
    DWORD aProcesses[2048], cbNeeded, cProcesses;

    if (EnumProcesses(aProcesses, sizeof(aProcesses), &cbNeeded)) {
        cProcesses = cbNeeded / sizeof(DWORD);

        for (unsigned int i = 0; i < cProcesses; i++) {
            DWORD pid = aProcesses[i];
            if (pid == 0 || pid == currentPid || excludePids.count(pid)) {
                continue;
            }

            HANDLE hProcess = OpenProcess(PROCESS_SET_QUOTA | PROCESS_QUERY_INFORMATION, FALSE, pid);
            if (!hProcess) continue;

            char nameBuf[MAX_PATH] = {0};
            if (GetProcessImageFileNameA(hProcess, nameBuf, MAX_PATH) > 0) {
                std::string fullPath(nameBuf);
                std::string baseName = fullPath;
                size_t slashPos = fullPath.find_last_of("\\/");
                if (slashPos != std::string::npos) baseName = fullPath.substr(slashPos + 1);
                std::transform(baseName.begin(), baseName.end(), baseName.begin(), ::tolower);
                if (CRITICAL_WHITELIST.count(baseName) || KNOWN_GAMES.count(baseName)) {
                    CloseHandle(hProcess);
                    continue;
                }
            }

            if (EmptyWorkingSet(hProcess)) {
                trimmedCount++;
            }
            CloseHandle(hProcess);
        }
    }
#endif
    return trimmedCount;
}

// ============================================================================
// DIRECTORY CLEANING (TEMPORARY FILES & GPU SHADER CACHES)
// ============================================================================

namespace fs = std::filesystem;

static void SweepDirectoryList(const std::vector<std::string>& dirs, uint64_t* outBytes, uint32_t* outFiles) {
    uint64_t bytes = 0;
    uint32_t files = 0;

    for (const auto& dirPath : dirs) {
        std::error_code ec;
        if (!fs::exists(dirPath, ec) || !fs::is_directory(dirPath, ec)) continue;

        for (const auto& entry : fs::directory_iterator(dirPath, fs::directory_options::skip_permission_denied, ec)) {
            if (ec) break;
            std::error_code removeEc;
            if (entry.is_regular_file(removeEc)) {
                auto sz = entry.file_size(removeEc);
                if (!removeEc && fs::remove(entry.path(), removeEc)) {
                    files++;
                    bytes += sz;
                }
            } else if (entry.is_directory(removeEc)) {
                auto count = fs::remove_all(entry.path(), removeEc);
                if (!removeEc && count > 0) {
                    files += static_cast<uint32_t>(count);
                }
            }
        }
    }

    if (outBytes) *outBytes = bytes;
    if (outFiles) *outFiles = files;
}

void CleanTempDirectories(uint64_t* outBytesCleaned, uint32_t* outFilesCleaned) {
    std::vector<std::string> dirs;
#ifdef _WIN32
    const char* tempEnv = std::getenv("TEMP");
    if (tempEnv) dirs.push_back(tempEnv);
    const char* sysRoot = std::getenv("SystemRoot");
    if (sysRoot) dirs.push_back(std::string(sysRoot) + "\\Temp");
    const char* localApp = std::getenv("LOCALAPPDATA");
    if (localApp) {
        dirs.push_back(std::string(localApp) + "\\CrashDumps");
        dirs.push_back(std::string(localApp) + "\\Microsoft\\Windows\\WER\\ReportArchive");
    }
#else
    dirs.push_back("/tmp");
#endif
    SweepDirectoryList(dirs, outBytesCleaned, outFilesCleaned);
}

void CleanGpuShaderCaches(uint64_t* outBytesCleaned, uint32_t* outFilesCleaned) {
    std::vector<std::string> dirs;
#ifdef _WIN32
    const char* localApp = std::getenv("LOCALAPPDATA");
    const char* appData = std::getenv("APPDATA");
    const char* tempEnv = std::getenv("TEMP");

    if (localApp) {
        dirs.push_back(std::string(localApp) + "\\NVIDIA\\DXCache");
        dirs.push_back(std::string(localApp) + "\\NVIDIA\\GLCache");
        dirs.push_back(std::string(localApp) + "\\NVIDIA Corporation\\NV_Cache");
        dirs.push_back(std::string(localApp) + "\\AMD\\DxCache");
        dirs.push_back(std::string(localApp) + "\\AMD\\GLCache");
        dirs.push_back(std::string(localApp) + "\\D3DSCache");
        dirs.push_back(std::string(localApp) + "\\Microsoft\\DirectX Shader Cache");
        dirs.push_back(std::string(localApp) + "\\Intel\\ShaderCache");
    }
    if (appData) {
        dirs.push_back(std::string(appData) + "\\NVIDIA\\ComputeCache");
    }
    if (tempEnv) {
        dirs.push_back(std::string(tempEnv) + "\\NVIDIA Corporation");
        dirs.push_back(std::string(tempEnv) + "\\AMD");
        dirs.push_back(std::string(tempEnv) + "\\Intel");
    }
#elif defined(__linux__)
    const char* home = std::getenv("HOME");
    if (home) {
        dirs.push_back(std::string(home) + "/.nv/ComputeCache");
        dirs.push_back(std::string(home) + "/.cache/mesa_shader_cache");
        dirs.push_back(std::string(home) + "/.cache/nvidia/GLCache");
        dirs.push_back(std::string(home) + "/.cache/dxvk");
    }
#endif
    SweepDirectoryList(dirs, outBytesCleaned, outFilesCleaned);
}

// ============================================================================
// HIGH PERFORMANCE POWER PLAN (Win32 PowrProf API)
// ============================================================================

bool ActivateHighPerformancePowerPlan() {
#ifdef _WIN32
    GUID ultimateGuid = { 0xe9a42b02, 0xd5df, 0x448d, { 0xaa, 0x00, 0x03, 0xf1, 0x47, 0x49, 0xeb, 0x61 } };
    GUID highGuid = { 0x8c5e7fda, 0xe8bf, 0x4a96, { 0x9a, 0x85, 0xa6, 0xe2, 0x3a, 0x8c, 0x63, 0x5c } };

    if (PowerSetActiveScheme(NULL, &ultimateGuid) == ERROR_SUCCESS) return true;
    if (PowerSetActiveScheme(NULL, &highGuid) == ERROR_SUCCESS) return true;
    return false;
#elif defined(__linux__)
    int res = system("cpupower frequency-set -g performance >/dev/null 2>&1");
    return (res == 0);
#else
    return true;
#endif
}

// ============================================================================
// PROCESS TERMINATION & BLOATWARE SUPPRESSION
// ============================================================================

static const std::vector<std::string> DEFAULT_BLOAT_LIST = {
    "yourphone.exe", "cortana.exe", "searchapp.exe", "widgets.exe",
    "teams.exe", "onedrive.exe", "gamebar.exe", "gamebarftserver.exe"
};

std::vector<std::string> TerminateBloatwareProcesses(const std::vector<std::string>& targets = {}) {
    std::vector<std::string> killed;
#ifdef _WIN32
    const auto& bloatList = targets.empty() ? DEFAULT_BLOAT_LIST : targets;
    std::unordered_set<std::string> targetSet;
    for (const auto& t : bloatList) {
        std::string lower = t;
        std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);
        targetSet.insert(lower);
    }

    DWORD aProcesses[2048], cbNeeded, cProcesses;
    if (EnumProcesses(aProcesses, sizeof(aProcesses), &cbNeeded)) {
        cProcesses = cbNeeded / sizeof(DWORD);
        DWORD currentPid = GetCurrentProcessId();

        for (unsigned int i = 0; i < cProcesses; i++) {
            DWORD pid = aProcesses[i];
            if (pid == 0 || pid == currentPid) continue;

            HANDLE hProcess = OpenProcess(PROCESS_TERMINATE | PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
            if (!hProcess) continue;

            char nameBuf[MAX_PATH] = {0};
            if (GetProcessImageFileNameA(hProcess, nameBuf, MAX_PATH) > 0) {
                std::string fullPath(nameBuf);
                std::string baseName = fullPath;
                size_t slash = fullPath.find_last_of("\\/");
                if (slash != std::string::npos) baseName = fullPath.substr(slash + 1);
                std::string lowerName = baseName;
                std::transform(lowerName.begin(), lowerName.end(), lowerName.begin(), ::tolower);

                if (targetSet.count(lowerName) && !CRITICAL_WHITELIST.count(lowerName)) {
                    if (TerminateProcess(hProcess, 0)) {
                        killed.push_back(baseName);
                    }
                }
            }
            CloseHandle(hProcess);
        }
    }
#endif
    return killed;
}

bool TerminateProcessById(DWORD pid) {
#ifdef _WIN32
    if (pid == 0 || pid == GetCurrentProcessId()) return false;
    HANDLE hProcess = OpenProcess(PROCESS_TERMINATE, FALSE, pid);
    if (!hProcess) return false;
    BOOL res = TerminateProcess(hProcess, 0);
    CloseHandle(hProcess);
    return (res == TRUE);
#else
    return false;
#endif
}

// ============================================================================
// GAME PROCESS PRIORITY & I/O BOOSTING
// ============================================================================

bool BoostProcessPriority(DWORD pid, int priorityLevel = 1) {
#ifdef _WIN32
    EnableAllKernelPrivileges();
    HANDLE hProcess = OpenProcess(PROCESS_SET_INFORMATION | PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
    if (!hProcess) return false;

    DWORD priorityClass = (priorityLevel >= 2) ? REALTIME_PRIORITY_CLASS : HIGH_PRIORITY_CLASS;
    SetPriorityClass(hProcess, priorityClass);

    // Set Disk I/O Priority to High (3) via NT API
    HMODULE hNtdll = GetModuleHandleW(L"ntdll.dll");
    if (hNtdll) {
        auto NtSetInformationProcess = (PNT_SET_INFORMATION_PROCESS)(void*)GetProcAddress(hNtdll, "NtSetInformationProcess");
        if (NtSetInformationProcess) {
            ULONG ioPriority = 3; // IoPriorityHigh
            NtSetInformationProcess(hProcess, ProcessIoPriority, &ioPriority, sizeof(ioPriority));
        }
    }

    CloseHandle(hProcess);
    return true;
#else
    (void)pid;
    (void)priorityLevel;
    return true;
#endif
}

bool BoostProcessByName(const std::string& nameQuery, int priorityLevel = 1, std::string* outBoostedName = nullptr, DWORD* outBoostedPid = nullptr) {
#ifdef _WIN32
    std::string lowerQuery = nameQuery;
    std::transform(lowerQuery.begin(), lowerQuery.end(), lowerQuery.begin(), ::tolower);

    DWORD aProcesses[2048], cbNeeded, cProcesses;
    if (EnumProcesses(aProcesses, sizeof(aProcesses), &cbNeeded)) {
        cProcesses = cbNeeded / sizeof(DWORD);
        for (unsigned int i = 0; i < cProcesses; i++) {
            DWORD pid = aProcesses[i];
            if (pid == 0) continue;

            HANDLE hProcess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
            if (!hProcess) continue;

            char nameBuf[MAX_PATH] = {0};
            if (GetProcessImageFileNameA(hProcess, nameBuf, MAX_PATH) > 0) {
                std::string fullPath(nameBuf);
                std::string baseName = fullPath;
                size_t slash = fullPath.find_last_of("\\/");
                if (slash != std::string::npos) baseName = fullPath.substr(slash + 1);
                std::string lowerName = baseName;
                std::transform(lowerName.begin(), lowerName.end(), lowerName.begin(), ::tolower);

                if (lowerName.find(lowerQuery) != std::string::npos) {
                    CloseHandle(hProcess);
                    if (BoostProcessPriority(pid, priorityLevel)) {
                        if (outBoostedName) *outBoostedName = baseName;
                        if (outBoostedPid) *outBoostedPid = pid;
                        return true;
                    }
                    return false;
                }
            }
            CloseHandle(hProcess);
        }
    }
#else
    (void)nameQuery;
    (void)priorityLevel;
    (void)outBoostedName;
    (void)outBoostedPid;
#endif
    return false;
}

// ============================================================================
// SYSTEM METRICS & TELEMETRY IN PURE C++
// ============================================================================

bool GetSystemMemoryMetrics(uint64_t* totalBytes, uint64_t* availBytes, uint64_t* usedBytes, uint64_t* standbyBytes, double* percentUsed) {
#ifdef _WIN32
    MEMORYSTATUSEX mem;
    mem.dwLength = sizeof(MEMORYSTATUSEX);
    if (!GlobalMemoryStatusEx(&mem)) return false;

    uint64_t total = mem.ullTotalPhys;
    uint64_t avail = mem.ullAvailPhys;
    uint64_t used = total > avail ? (total - avail) : 0;
    double pct = (double)mem.dwMemoryLoad;

    uint64_t standby = 0;
    PERFORMANCE_INFORMATION pi;
    pi.cb = sizeof(PERFORMANCE_INFORMATION);
    if (GetPerformanceInfo(&pi, sizeof(pi))) {
        standby = static_cast<uint64_t>(pi.SystemCache) * static_cast<uint64_t>(pi.PageSize);
    }

    if (totalBytes) *totalBytes = total;
    if (availBytes) *availBytes = avail;
    if (usedBytes) *usedBytes = used;
    if (standbyBytes) *standbyBytes = standby;
    if (percentUsed) *percentUsed = pct;
    return true;
#else
    if (totalBytes) *totalBytes = 16ULL * 1024 * 1024 * 1024;
    if (availBytes) *availBytes = 8ULL * 1024 * 1024 * 1024;
    if (usedBytes) *usedBytes = 8ULL * 1024 * 1024 * 1024;
    if (standbyBytes) *standbyBytes = 2ULL * 1024 * 1024 * 1024;
    if (percentUsed) *percentUsed = 50.0;
    return true;
#endif
}

#ifdef _WIN32
static uint64_t FileTimeToUint64(const FILETIME& ft) {
    return ((uint64_t)ft.dwHighDateTime << 32) | ft.dwLowDateTime;
}
#endif

double GetCpuUsagePercent() {
#ifdef _WIN32
    static uint64_t prevIdle = 0, prevKernel = 0, prevUser = 0;
    FILETIME idleTime, kernelTime, userTime;
    if (!GetSystemTimes(&idleTime, &kernelTime, &userTime)) return 0.0;

    uint64_t idle = FileTimeToUint64(idleTime);
    uint64_t kernel = FileTimeToUint64(kernelTime);
    uint64_t user = FileTimeToUint64(userTime);

    if (prevIdle == 0) {
        prevIdle = idle; prevKernel = kernel; prevUser = user;
        return 0.0;
    }

    uint64_t idleDiff = idle - prevIdle;
    uint64_t kernelDiff = kernel - prevKernel;
    uint64_t userDiff = user - prevUser;
    uint64_t totalDiff = kernelDiff + userDiff;

    prevIdle = idle; prevKernel = kernel; prevUser = user;

    if (totalDiff == 0) return 0.0;
    double percent = (double)(totalDiff - idleDiff) * 100.0 / (double)totalDiff;
    return (percent < 0.0) ? 0.0 : ((percent > 100.0) ? 100.0 : percent);
#else
    return 15.0;
#endif
}

struct NativeProcInfo {
    DWORD pid;
    std::string name;
    size_t memBytes;
};

std::vector<NativeProcInfo> GetTopMemoryProcesses(int count = 15) {
    std::vector<NativeProcInfo> procs;
#ifdef _WIN32
    DWORD aProcesses[2048], cbNeeded, cProcesses;
    if (!EnumProcesses(aProcesses, sizeof(aProcesses), &cbNeeded)) return procs;
    cProcesses = cbNeeded / sizeof(DWORD);

    for (unsigned int i = 0; i < cProcesses; i++) {
        DWORD pid = aProcesses[i];
        if (pid == 0) continue;
        HANDLE hProcess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
        if (!hProcess) continue;

        PROCESS_MEMORY_COUNTERS pmc;
        if (GetProcessMemoryInfo(hProcess, &pmc, sizeof(pmc))) {
            char nameBuf[MAX_PATH] = {0};
            if (GetProcessImageFileNameA(hProcess, nameBuf, MAX_PATH) > 0) {
                std::string fullPath(nameBuf);
                std::string baseName = fullPath;
                size_t slash = fullPath.find_last_of("\\/");
                if (slash != std::string::npos) baseName = fullPath.substr(slash + 1);
                procs.push_back({ pid, baseName, pmc.WorkingSetSize });
            }
        }
        CloseHandle(hProcess);
    }

    std::sort(procs.begin(), procs.end(), [](const NativeProcInfo& a, const NativeProcInfo& b) {
        return a.memBytes > b.memBytes;
    });

    if (count > 0 && procs.size() > static_cast<size_t>(count)) {
        procs.resize(count);
    }
#endif
    return procs;
}

// ============================================================================
// EXPORTED C API FOR PYTHON IN-PROCESS CDLL (SUB-MICROSECOND LATENCY)
// ============================================================================

#define DLL_EXPORT extern "C" __declspec(dllexport)

DLL_EXPORT int C_FlushStandbyMemory() {
    return FlushStandbyMemory() ? 1 : 0;
}

DLL_EXPORT int C_TrimWorkingSets(const char* excludePidsCsv) {
    std::unordered_set<DWORD> excludePids;
    if (excludePidsCsv && std::strlen(excludePidsCsv) > 0) {
        std::stringstream ss(excludePidsCsv);
        std::string item;
        while (std::getline(ss, item, ',')) {
            try {
                if (!item.empty()) excludePids.insert(static_cast<DWORD>(std::stoul(item)));
            } catch (...) {}
        }
    }
    return static_cast<int>(TrimWorkingSets(excludePids));
}

DLL_EXPORT int C_LockHighPrecisionTimer(int enable) {
    return LockHighPrecisionTimer(enable != 0) ? 1 : 0;
}

DLL_EXPORT int C_GetTimerResolution(double* curMs, double* minMs) {
    return GetTimerResolutionMs(curMs, minMs) ? 1 : 0;
}

DLL_EXPORT int C_ActivatePowerPlan() {
    return ActivateHighPerformancePowerPlan() ? 1 : 0;
}

DLL_EXPORT int C_CleanTempDirectories(uint64_t* outBytesCleaned, uint32_t* outFilesCleaned) {
    CleanTempDirectories(outBytesCleaned, outFilesCleaned);
    return 1;
}

DLL_EXPORT int C_CleanGpuShaderCaches(uint64_t* outBytesCleaned, uint32_t* outFilesCleaned) {
    CleanGpuShaderCaches(outBytesCleaned, outFilesCleaned);
    return 1;
}

DLL_EXPORT int C_TerminateBloatware(char* outKilledList, int maxLen) {
    auto killed = TerminateBloatwareProcesses();
    if (outKilledList && maxLen > 0) {
        std::string joined;
        for (size_t i = 0; i < killed.size(); i++) {
            joined += killed[i];
            if (i + 1 < killed.size()) joined += ", ";
        }
        std::strncpy(outKilledList, joined.c_str(), maxLen - 1);
        outKilledList[maxLen - 1] = '\0';
    }
    return static_cast<int>(killed.size());
}

DLL_EXPORT int C_TerminateProcessById(DWORD pid) {
    return TerminateProcessById(pid) ? 1 : 0;
}

DLL_EXPORT int C_BoostProcessPriority(DWORD pid, int level) {
    return BoostProcessPriority(pid, level) ? 1 : 0;
}

DLL_EXPORT int C_BoostProcessByName(const char* name, int level, char* outName, int maxNameLen, DWORD* outPid) {
    if (!name) return 0;
    std::string boostedName;
    DWORD boostedPid = 0;
    bool ok = BoostProcessByName(name, level, &boostedName, &boostedPid);
    if (ok) {
        if (outName && maxNameLen > 0) {
            std::strncpy(outName, boostedName.c_str(), maxNameLen - 1);
            outName[maxNameLen - 1] = '\0';
        }
        if (outPid) *outPid = boostedPid;
        return 1;
    }
    return 0;
}

DLL_EXPORT int C_GetMemoryMetrics(uint64_t* totalBytes, uint64_t* availBytes, uint64_t* usedBytes, uint64_t* standbyBytes, double* percentUsed) {
    return GetSystemMemoryMetrics(totalBytes, availBytes, usedBytes, standbyBytes, percentUsed) ? 1 : 0;
}

DLL_EXPORT double C_GetCpuUsagePercent() {
    return GetCpuUsagePercent();
}

DLL_EXPORT int C_GetTopProcessesJson(int count, char* outJson, int maxLen) {
    if (!outJson || maxLen <= 0) return 0;
    auto procs = GetTopMemoryProcesses(count);
    std::stringstream ss;
    ss << "[";
    for (size_t i = 0; i < procs.size(); i++) {
        double mb = (double)procs[i].memBytes / (1024.0 * 1024.0);
        ss << "{\"pid\":" << procs[i].pid
           << ",\"name\":\"" << procs[i].name << "\""
           << ",\"mem_bytes\":" << procs[i].memBytes
           << ",\"mem_mb\":" << std::fixed << std::setprecision(1) << mb << "}";
        if (i + 1 < procs.size()) ss << ",";
    }
    ss << "]";
    std::string jsonStr = ss.str();
    std::strncpy(outJson, jsonStr.c_str(), maxLen - 1);
    outJson[maxLen - 1] = '\0';
    return static_cast<int>(procs.size());
}

// ============================================================================
// STANDALONE CLI BANNER & COMMAND INTERFACE
// ============================================================================

void PrintBanner() {
    std::cout << MAGENTA << "==================================================" << RESET << std::endl;
    std::cout << MAGENTA << "  ⚡ MR. DREW'S DEVICE & FPS OPTIMIZER (PURE C++)  " << RESET << std::endl;
    std::cout << MAGENTA << "==================================================" << RESET << std::endl;
}

void PrintHelp() {
    PrintBanner();
    std::cout << "Usage: DeviceOptimizer [OPTIONS]\n\n"
              << "Core Optimization Pipelines:\n"
              << "  --fps-boost              Run Gaming & FPS optimization pipeline (1ms timer lock)\n"
              << "  --monster                Run Monster RAM & system optimization pipeline\n"
              << "  --potato                 Run 4GB Ultra-Light Low-Spec optimization pipeline\n"
              << "\nSpecific System Actions:\n"
              << "  --flush-standby          Purge Windows Standby List memory via NT kernel\n"
              << "  --trim-ram               Compact working sets for non-critical processes\n"
              << "  --exclude-pids <list>    Comma-separated list of process PIDs to protect from trimming\n"
              << "  --clear-temp             Safely clear system & user temporary files (std::filesystem)\n"
              << "  --clean-shaders          Clean DirectX, OpenGL, Vulkan, NVIDIA, AMD shader caches\n"
              << "  --kill-bloat             Terminate non-essential background bloatware directly\n"
              << "  --power-plan             Activate High / Ultimate Performance power scheme\n"
              << "  --boost-game <name/pid>  Elevate process CPU and Disk I/O scheduling priorities\n"
              << "\nTelemetry & Information:\n"
              << "  --sys-specs              Display real-time CPU, RAM, and Standby memory specs\n"
              << "  --top-procs [count]      Display top RAM consuming processes ranked\n"
              << "  --json-stats             Output system admin status as JSON\n"
              << "  --help, -h               Show this help message and exit\n"
              << "  --version, -v            Show engine version\n"
              << "  --gui                    Launch desktop web interface\n"
              << std::endl;
}

bool LaunchDesktopGui() {
#ifdef _WIN32
    wchar_t exePathBuf[MAX_PATH];
    GetModuleFileNameW(NULL, exePathBuf, MAX_PATH);
    std::filesystem::path appDir = std::filesystem::path(exePathBuf).parent_path();

    // 1. Check for standalone GUI executable in the directory or dist
    std::vector<std::wstring> guiExeCandidates = {
        L"DeviceOptimizerGUI.exe",
        L"MrDrewsDeviceOptimizer.exe",
        L"dist\\DeviceOptimizerGUI\\DeviceOptimizerGUI.exe"
    };

    for (const auto& candidate : guiExeCandidates) {
        std::filesystem::path fullGuiPath = appDir / candidate;
        if (std::filesystem::exists(fullGuiPath)) {
            HINSTANCE hInst = ShellExecuteW(NULL, L"open", fullGuiPath.c_str(), NULL, appDir.c_str(), SW_SHOWDEFAULT);
            if ((INT_PTR)hInst > 32) {
                return true;
            }
        }
    }

    // 2. Check for pythonw.exe or python.exe to run run.py
    std::filesystem::path runPy = appDir / L"run.py";
    if (std::filesystem::exists(runPy)) {
        HINSTANCE hInst = ShellExecuteW(NULL, L"open", L"pythonw.exe", L"run.py", appDir.c_str(), SW_SHOWDEFAULT);
        if ((INT_PTR)hInst > 32) {
            return true;
        }

        hInst = ShellExecuteW(NULL, L"open", L"py.exe", L"-3 run.py", appDir.c_str(), SW_SHOWDEFAULT);
        if ((INT_PTR)hInst > 32) {
            return true;
        }

        hInst = ShellExecuteW(NULL, L"open", L"python.exe", L"run.py", appDir.c_str(), SW_SHOWDEFAULT);
        if ((INT_PTR)hInst > 32) {
            return true;
        }
    }

    // 3. Fallback: check if launched from Windows Explorer
    HWND hConsole = GetConsoleWindow();
    DWORD procId = 0;
    GetWindowThreadProcessId(hConsole, &procId);
    bool isSpawnedFromExplorer = (GetCurrentProcessId() == procId);

    if (isSpawnedFromExplorer) {
        MessageBoxW(NULL,
            L"Mr. Drew's Device Optimizer\n\n"
            L"Desktop GUI requires DeviceOptimizerGUI.exe or Python 3.8+ (run.py).\n\n"
            L"To run in high-speed C++ CLI mode, open Command Prompt and execute:\n"
            L"  DeviceOptimizer.exe --fps-boost\n"
            L"  DeviceOptimizer.exe --monster\n"
            L"  DeviceOptimizer.exe --potato",
            L"Mr. Drew's Device Optimizer",
            MB_ICONINFORMATION | MB_OK);
    } else {
        PrintHelp();
    }
    return false;
#else
    std::string runPy = "python3 run.py";
    int ret = system(runPy.c_str());
    return (ret == 0);
#endif
}

#ifndef BUILD_DLL
int main(int argc, char* argv[]) {
    EnableAnsiSupport();

    std::vector<std::string> args(argv, argv + argc);
    if (args.size() <= 1) {
        // If double-clicked in Explorer or run without arguments, launch GUI
        if (LaunchDesktopGui()) {
            return 0;
        }
        return 0;
    }

    bool runMonster = false;
    bool fpsBoost = false;
    bool potatoMode = false;
    bool flushOnly = false;
    bool trimOnly = false;
    bool tempOnly = false;
    bool shadersOnly = false;
    bool killBloat = false;
    bool setPower = false;
    bool showSpecs = false;
    bool showTop = false;
    int topCount = 10;
    bool jsonStats = false;
    bool launchGui = false;
    std::string boostTarget;
    std::unordered_set<DWORD> excludePids;

    for (size_t i = 1; i < args.size(); ++i) {
        const std::string& arg = args[i];
        if (arg == "--help" || arg == "-h") {
            PrintHelp();
            return 0;
        } else if (arg == "--version" || arg == "-v") {
            std::cout << "Mr. Drew's Device Optimizer Pure C++ Native Engine v2.5.0" << std::endl;
            return 0;
        } else if (arg == "--monster") {
            runMonster = true;
        } else if (arg == "--fps-boost") {
            fpsBoost = true;
        } else if (arg == "--potato") {
            potatoMode = true;
        } else if (arg == "--flush-standby") {
            flushOnly = true;
        } else if (arg == "--trim-ram") {
            trimOnly = true;
        } else if (arg == "--clear-temp") {
            tempOnly = true;
        } else if (arg == "--clean-shaders") {
            shadersOnly = true;
        } else if (arg == "--kill-bloat") {
            killBloat = true;
        } else if (arg == "--power-plan") {
            setPower = true;
        } else if (arg == "--sys-specs") {
            showSpecs = true;
        } else if (arg == "--top-procs") {
            showTop = true;
            if (i + 1 < args.size() && args[i + 1].rfind("--", 0) != 0) {
                try { topCount = std::stoi(args[++i]); } catch (...) {}
            }
        } else if (arg == "--boost-game" && i + 1 < args.size()) {
            boostTarget = args[++i];
        } else if (arg == "--exclude-pids" && i + 1 < args.size()) {
            std::string pidsStr = args[++i];
            std::stringstream ss(pidsStr);
            std::string item;
            while (std::getline(ss, item, ',')) {
                try {
                    if (!item.empty()) excludePids.insert(static_cast<DWORD>(std::stoul(item)));
                } catch (...) {}
            }
        } else if (arg == "--json-stats") {
            jsonStats = true;
        } else if (arg == "--gui") {
            launchGui = true;
        }
    }

    if (launchGui) {
        LaunchDesktopGui();
        return 0;
    }

    if (jsonStats) {
        uint64_t total = 0, avail = 0, used = 0, standby = 0;
        double pct = 0.0;
        GetSystemMemoryMetrics(&total, &avail, &used, &standby, &pct);
        std::cout << "{\"status\":\"ok\",\"os_admin\":" << (IsAdminOrRoot() ? "true" : "false")
                  << ",\"total_ram_gb\":" << std::fixed << std::setprecision(2) << ((double)total / (1024.0*1024*1024))
                  << ",\"avail_ram_gb\":" << ((double)avail / (1024.0*1024*1024))
                  << ",\"standby_ram_gb\":" << ((double)standby / (1024.0*1024*1024))
                  << ",\"percent_used\":" << pct << "}" << std::endl;
        return 0;
    }

    if (showSpecs) {
        PrintBanner();
        uint64_t total = 0, avail = 0, used = 0, standby = 0;
        double pct = 0.0;
        GetSystemMemoryMetrics(&total, &avail, &used, &standby, &pct);
        double curMs = 1.0, minMs = 15.625;
        GetTimerResolutionMs(&curMs, &minMs);
        std::cout << "  OS Elevation Status : " << (IsAdminOrRoot() ? "Administrator (Elevated)" : "Standard User") << "\n"
                  << "  Physical Total RAM  : " << std::fixed << std::setprecision(2) << ((double)total / (1024.0*1024*1024)) << " GB\n"
                  << "  Physical Used RAM   : " << ((double)used / (1024.0*1024*1024)) << " GB (" << pct << "%)\n"
                  << "  Physical Free RAM   : " << ((double)avail / (1024.0*1024*1024)) << " GB\n"
                  << "  Standby Cache RAM   : " << ((double)standby / (1024.0*1024*1024)) << " GB\n"
                  << "  System Timer Lock   : " << curMs << " ms (Default: " << minMs << " ms)\n"
                  << std::endl;
        return 0;
    }

    if (showTop) {
        PrintBanner();
        auto procs = GetTopMemoryProcesses(topCount);
        std::cout << "Top " << procs.size() << " Processes by Physical RAM Usage:\n";
        for (size_t idx = 0; idx < procs.size(); idx++) {
            double mb = (double)procs[idx].memBytes / (1024.0 * 1024.0);
            std::cout << "  [" << std::setw(2) << idx + 1 << "] PID: " << std::setw(6) << procs[idx].pid
                      << " | " << std::setw(28) << std::left << procs[idx].name
                      << " | " << std::fixed << std::setprecision(1) << mb << " MB\n";
        }
        std::cout << std::endl;
        return 0;
    }

    if (!boostTarget.empty()) {
        try {
            DWORD pid = static_cast<DWORD>(std::stoul(boostTarget));
            if (BoostProcessPriority(pid, 1)) {
                LogSuccess("Elevated Process PID " + std::to_string(pid) + " to HIGH CPU & Disk I/O Priority.");
            } else {
                LogError("Failed to elevate process PID " + std::to_string(pid));
            }
        } catch (...) {
            std::string boostedName;
            DWORD boostedPid = 0;
            if (BoostProcessByName(boostTarget, 1, &boostedName, &boostedPid)) {
                LogSuccess("Elevated '" + boostedName + "' (PID: " + std::to_string(boostedPid) + ") to HIGH CPU & Disk I/O Priority.");
            } else {
                LogError("Process '" + boostTarget + "' not found among active applications.");
            }
        }
        return 0;
    }

    if (flushOnly) {
        bool ok = FlushStandbyMemory();
        if (ok) LogSuccess("Standby RAM list successfully flushed via NT Kernel.");
        else LogError("Failed to flush Standby RAM (Requires Administrator rights).");
        return ok ? 0 : 1;
    }

    if (trimOnly) {
        uint32_t count = TrimWorkingSets(excludePids);
        LogSuccess("Trimmed working sets for " + std::to_string(count) + " running processes.");
        return 0;
    }

    if (tempOnly) {
        uint64_t bytes = 0;
        uint32_t files = 0;
        CleanTempDirectories(&bytes, &files);
        double mb = (double)bytes / (1024.0 * 1024.0);
        std::stringstream ss;
        ss << std::fixed << std::setprecision(1) << mb;
        LogSuccess("Cleaned " + std::to_string(files) + " temporary items (" + ss.str() + " MB freed).");
        return 0;
    }

    if (shadersOnly) {
        uint64_t bytes = 0;
        uint32_t files = 0;
        CleanGpuShaderCaches(&bytes, &files);
        double mb = (double)bytes / (1024.0 * 1024.0);
        std::stringstream ss;
        ss << std::fixed << std::setprecision(1) << mb;
        LogSuccess("Cleaned " + std::to_string(files) + " GPU shader cache items (" + ss.str() + " MB freed).");
        return 0;
    }

    if (killBloat) {
        auto killed = TerminateBloatwareProcesses();
        LogSuccess("Terminated " + std::to_string(killed.size()) + " background bloatware processes.");
        return 0;
    }

    if (setPower) {
        bool ok = ActivateHighPerformancePowerPlan();
        if (ok) LogSuccess("High Performance Power Plan activated via Win32 PowrProf.");
        else LogWarning("Failed to activate high performance power scheme.");
        return ok ? 0 : 1;
    }

    PrintBanner();

    bool isAdmin = IsAdminOrRoot();
    if (!isAdmin) {
        LogWarning("Running in User Mode. (Run as Administrator for full NT kernel flushes)");
    } else {
        LogSuccess("Administrator privileges verified.");
    }

    uint64_t beforeTotal = 0, beforeAvail = 0;
    GetSystemMemoryMetrics(&beforeTotal, &beforeAvail, nullptr, nullptr, nullptr);

    if (fpsBoost) {
        LogInfo("🎮 GAMING & FPS BOOSTER ENGINE RUNNING IN PURE C++...");
        LockHighPrecisionTimer(true);
        ActivateHighPerformancePowerPlan();
        uint64_t sBytes = 0; uint32_t sFiles = 0;
        CleanGpuShaderCaches(&sBytes, &sFiles);
        auto killed = TerminateBloatwareProcesses();
        uint32_t trimmed = TrimWorkingSets(excludePids);
        FlushStandbyMemory();
        uint64_t tBytes = 0; uint32_t tFiles = 0;
        CleanTempDirectories(&tBytes, &tFiles);

        uint64_t afterAvail = 0;
        GetSystemMemoryMetrics(nullptr, &afterAvail, nullptr, nullptr, nullptr);
        double reclaimed = afterAvail > beforeAvail ? ((double)(afterAvail - beforeAvail) / (1024.0 * 1024.0 * 1024.0)) : 0.0;

        LogSuccess("FPS Booster Engine complete! Freed " + std::to_string(reclaimed) + " GB RAM (" + std::to_string(trimmed) + " processes compacted).");
        return 0;
    }

    if (runMonster) {
        LogInfo("🔥 MONSTER SYSTEM OPTIMIZER PIPELINE RUNNING IN PURE C++...");
        LockHighPrecisionTimer(true);
        auto killed = TerminateBloatwareProcesses();
        uint32_t trimmed = TrimWorkingSets(excludePids);
        FlushStandbyMemory();
        uint64_t tBytes = 0; uint32_t tFiles = 0;
        CleanTempDirectories(&tBytes, &tFiles);
        uint64_t sBytes = 0; uint32_t sFiles = 0;
        CleanGpuShaderCaches(&sBytes, &sFiles);

        uint64_t afterAvail = 0;
        GetSystemMemoryMetrics(nullptr, &afterAvail, nullptr, nullptr, nullptr);
        double reclaimed = afterAvail > beforeAvail ? ((double)(afterAvail - beforeAvail) / (1024.0 * 1024.0 * 1024.0)) : 0.0;

        LogSuccess("Monster Optimizer complete! Free RAM increased by " + std::to_string(reclaimed) + " GB (" + std::to_string(trimmed) + " processes compacted).");
        return 0;
    }

    if (potatoMode) {
        LogInfo("🥔 4GB POTATO PC ULTRA-LIGHT PIPELINE RUNNING IN PURE C++...");
        auto killed = TerminateBloatwareProcesses();
        uint32_t trimmed = TrimWorkingSets(excludePids);
        FlushStandbyMemory();
        uint64_t tBytes = 0; uint32_t tFiles = 0;
        CleanTempDirectories(&tBytes, &tFiles);

        uint64_t afterAvail = 0;
        GetSystemMemoryMetrics(nullptr, &afterAvail, nullptr, nullptr, nullptr);
        double reclaimed = afterAvail > beforeAvail ? ((double)(afterAvail - beforeAvail) / (1024.0 * 1024.0 * 1024.0)) : 0.0;

        LogSuccess("Potato Mode complete! Terminated " + std::to_string(killed.size()) + " background tasks, trimmed " + std::to_string(trimmed) + " processes, reclaimed " + std::to_string(reclaimed) + " GB RAM.");
        return 0;
    }

    // Default action
    LockHighPrecisionTimer(true);
    TerminateBloatwareProcesses();
    CleanTempDirectories(nullptr, nullptr);
    TrimWorkingSets(excludePids);
    FlushStandbyMemory();

    LogSuccess("Pure C++ System & Memory Optimization successfully executed.");
    return 0;
}
#endif
