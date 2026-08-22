// Tutorial Steps Database
const TUTORIAL_STEPS = [
    {
        id: "welcome",
        category: "🚀 GETTING STARTED",
        title: "Welcome to Mr. Drew's Device & FPS Optimizer",
        icon: "⚡",
        color: "#00F0FF",
        how: "Combines a native C++ engine, GPU shader management, real-time memory compaction, and process priority tuning into one fast suite.",
        why: "Eliminates game micro-stutters, reclaims 2 to 5 GB physical RAM, lowers input lag, and prevents texture pop-in.",
        when: "Run before starting gaming sessions (Fortnite, Valorant, Roblox, Unreal Engine), or run Smart Auto-Guard in the background.",
        action_id: null,
        action_label: null
    },
    {
        id: "fps_booster",
        category: "🎮 GAMING ENGINE",
        title: "RUN FPS & GAME BOOSTER",
        icon: "🎮",
        color: "#F59E0B",
        how: "Locks system timer resolution to 1.0ms, flushes GPU shader caches (Nvidia/AMD/DirectX), and elevates game process CPU priority to High.",
        why: "Fixes frame drops, removes micro-stutters, and lowers input latency in competitive games.",
        when: "Click right before launching your game or whenever you notice stutters during gameplay.",
        action_id: "run_fps_booster",
        action_label: "🧪 Try FPS Booster Now"
    },
    {
        id: "asset_loader",
        category: "🎮 GAMING ENGINE",
        title: "Fast Asset Loader",
        icon: "🚀",
        color: "#10B981",
        how: "Sets Disk I/O priority to High (ProcessIoPriorityHigh) for active game processes and protects loaded game assets from RAM eviction.",
        why: "Accelerates map loading, texture streaming, and 3D asset rendering; stops texture pop-in.",
        when: "Use when loading open-world games, map transitions, or heavy Roblox / Unreal Engine projects.",
        action_id: "accelerate_asset_loading",
        action_label: "🧪 Test Asset Loader"
    },
    {
        id: "potato_mode",
        category: "🥔 LOW-SPEC ENGINE",
        title: "4GB Potato Mode",
        icon: "🥔",
        color: "#EAB308",
        how: "Triggers aggressive memory compaction targeting 1.5 GB free RAM, drops inactive page caches, and terminates background bloatware.",
        why: "Enables smooth gaming and app performance on budget/low-spec devices with 4GB to 8GB physical RAM without paging stutters.",
        when: "Activate on low-end laptops or budget PCs before launching any game.",
        action_id: "run_potato_mode",
        action_label: "🧪 Test Potato Mode"
    },
    {
        id: "ultimate_power",
        category: "⚡ POWER ENGINE",
        title: "Ultimate Power Mode",
        icon: "⚡",
        color: "#10B981",
        how: "Forces Windows OS power scheme to High / Ultimate Performance, disabling CPU core parking and power throttling.",
        why: "Ensures CPU cores run at peak clock speeds without sudden frequency drops during demanding scenes.",
        when: "Enable when gaming, video editing, or rendering on desktop or plugged-in laptops.",
        action_id: "enable_power_plan",
        action_label: "🧪 Enable Ultimate Power"
    },
    {
        id: "monster_optimizer",
        category: "🧠 MEMORY ENGINE",
        title: "RUN MONSTER OPTIMIZER",
        icon: "🔥",
        color: "#A855F7",
        how: "Multi-stage deep RAM recovery: compacts background working sets via EmptyWorkingSet, flushes kernel standby page list, and sweeps temp memory.",
        why: "Recovers the maximum possible physical memory (up to 3-6 GB RAM) in one click without closing critical system apps.",
        when: "Use when overall RAM usage exceeds 80%, or before running memory-heavy applications.",
        action_id: "run_monster_optimizer",
        action_label: "🧪 Run Monster Optimizer"
    },
    {
        id: "trim_ram",
        category: "🧠 MEMORY ENGINE",
        title: "Trim App RAM",
        icon: "✂️",
        color: "#00F0FF",
        how: "Iterates through non-critical user applications and compacts their active working set memory into physical free RAM.",
        why: "Instantly reclaims RAM held hostage by web browsers (Chrome, Edge) and background software (Discord, Spotify).",
        when: "Use while multitasking when you want to free RAM without quitting open applications.",
        action_id: "trim_working_sets",
        action_label: "🧪 Trim App RAM Now"
    },
    {
        id: "purge_standby",
        category: "🧠 MEMORY ENGINE",
        title: "Purge Standby RAM",
        icon: "🛡️",
        color: "#3B82F6",
        how: "Calls C++ NtSetSystemInformation with SystemMemoryListInformation (or POSIX drop_caches on Linux/macOS) to clear cached standby list memory.",
        why: "Fixes Windows Standby RAM bugs that cause game crashes and hitching when free RAM drops to zero.",
        when: "Use when Standby cached memory is high and free memory is low.",
        action_id: "purge_standby",
        action_label: "🧪 Purge Standby RAM"
    },
    {
        id: "clear_temp",
        category: "🧹 CLEANING ENGINE",
        title: "Clear Temp Files",
        icon: "🧹",
        color: "#EC4899",
        how: "Recursively cleans %TEMP%, %SystemRoot%\\Temp, log caches, and leftover installer clutter while bypassing locked files safely.",
        why: "Frees up gigabytes of SSD/HDD drive space and removes system clutter.",
        when: "Run weekly or whenever drive space is tight.",
        action_id: "clear_temp",
        action_label: "🧪 Clear Temp Files"
    },
    {
        id: "game_picker",
        category: "🎯 PRIORITY TUNER",
        title: "Boost Game Priority",
        icon: "🎯",
        color: "#F59E0B",
        how: "Lets you pick your active game process and elevates its OS scheduling priority class to High Priority.",
        why: "Guarantees that the CPU allocates maximum execution clock cycles to your game over background threads.",
        when: "Use whenever playing competitive multiplayer games or resource-demanding titles.",
        action_id: "open_game_picker",
        action_label: "🧪 Select & Boost Game"
    },
    {
        id: "shader_cleaner",
        category: "🎨 GRAPHICS TUNER",
        title: "Clean Shader Cache",
        icon: "🧹",
        color: "#00F0FF",
        how: "Sweeps compiled DirectX, OpenGL, Vulkan, Nvidia (DXCache/GLCache), AMD (DxCache), and Intel GPU shader caches.",
        why: "Fixes corrupted shader stuttering, visual artifacts, and frame drops caused by stale shader caches.",
        when: "Run after updating graphics drivers, installing game updates, or experiencing graphical stutters.",
        action_id: "clean_shader_cache",
        action_label: "🧪 Clean Shader Cache"
    },
    {
        "id": "end_bloatware",
        category: "🛡️ SECURITY & CLEANING",
        title: "End Bloatware",
        icon: "🚫",
        color: "#EF4444",
        how: "Safely terminates non-essential background bloatware (OneDrive, Widgets, Teams, Cortana) protected by safety whitelists.",
        why: "Stops unwanted background telemetry, reduces background CPU usage, and saves memory.",
        when: "Run on computer startup or before launching games.",
        action_id: "kill_bloatware",
        action_label: "🧪 Terminate Bloatware"
    },
    {
        id: "top_procs",
        category: "📊 SYSTEM ANALYTICS",
        title: "Top RAM Apps",
        icon: "📊",
        color: "#10B981",
        how: "Scans active processes, calculates physical RAM usage (RSS), and ranks top memory consumers in real-time.",
        why: "Provides full visibility into what applications are consuming system resources.",
        when: "Use to inspect system memory distribution or identify memory hogs.",
        action_id: "view_top_processes",
        action_label: "🧪 View Top RAM Apps"
    },
    {
        id: "auto_guard",
        category: "⚡ AUTOMATION ENGINE",
        title: "Smart Auto-Guard (60s Loop)",
        icon: "⚡",
        color: "#A855F7",
        how: "Background thread continuously monitors physical free RAM. If free memory falls below target threshold, automatically triggers standby list flush and memory compaction.",
        why: "Provides automatic, set-and-forget 24/7 protection against memory leaks and RAM exhaustion stutters.",
        when: "Turn on for long gaming sessions or background server operations.",
        action_id: "toggle_auto_guard",
        action_label: "🧪 Toggle Auto-Guard"
    }
];

let currentTutorialStep = 0;
let isPyWebViewReady = false;

// Initialization
document.addEventListener("DOMContentLoaded", () => {
    initPyWebViewBridge();
    populateTutorialJumpSelect();
    populateTutorialCategoryTabs();
    
    // Poll stats every 2 seconds
    setInterval(refreshSystemStats, 2000);
});

function initPyWebViewBridge() {
    window.addEventListener('pywebviewready', () => {
        isPyWebViewReady = true;
        logToConsole("PyWebView Native Bridge Connected!");
        refreshSystemStats();
        checkFirstRunStatus();
    });

    // Fallback for direct browser access
    setTimeout(() => {
        if (!isPyWebViewReady) {
            logToConsole("Running in Web Mode (Bridge Active via Local Server).");
            refreshSystemStats();
            checkFirstRunStatus();
        }
    }, 800);
}

// Page Navigation
function switchPage(pageId) {
    document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
    document.querySelectorAll(".page").forEach(el => el.classList.remove("active"));

    const navItem = document.querySelector(`.nav-item[data-page="${pageId}"]`);
    const pageEl = document.getElementById(pageId);

    if (navItem) navItem.classList.add("active");
    if (pageEl) pageEl.classList.add("active");

    if (pageId === "page-tools") {
        triggerAction("view_top_processes");
    }
}

// Stats Polling & Gauge Rendering
async function refreshSystemStats() {
    try {
        let specs = null;
        let hw = null;

        if (window.pywebview && window.pywebview.api) {
            specs = await window.pywebview.api.get_system_specs();
            hw = await window.pywebview.api.get_hardware_details();
        } else {
            // Mock data if running purely in static browser
            specs = { total_ram_gb: 16.0, avail_ram_gb: 8.4, used_ram_gb: 7.6, target_free_gb: 5.0, percent_used: 47.5, cpu_percent: 12.4, os_name: "Windows", timer_res_ms: 1.0 };
            hw = { device_profile: "🚀 Standard Rig (16GB RAM)", gpu_vendor: "NVIDIA GeForce RTX 3060", cpu_cores_logical: 16, cpp_engine_active: true };
        }

        // Update Dashboard Cards
        document.getElementById("dash-total-ram").innerText = `${specs.total_ram_gb} GB`;
        document.getElementById("dash-free-ram").innerText = `${specs.avail_ram_gb} GB`;
        document.getElementById("dash-target-ram").innerText = `≥ ${specs.target_free_gb} GB`;
        document.getElementById("dash-cpu-percent").innerText = `${specs.cpu_percent}%`;

        // Update SVG Gauge
        const pct = specs.percent_used;
        document.getElementById("dash-ram-percent").innerText = `${pct}% RAM Used`;
        document.getElementById("gauge-center-num").innerText = `${pct}%`;

        const circle = document.getElementById("svg-gauge-circle");
        const maxOffset = 314.15;
        const offset = maxOffset - (pct / 100.0) * maxOffset;
        circle.style.strokeDashoffset = offset;

        // Color based on target
        if (specs.avail_ram_gb >= specs.target_free_gb) {
            circle.style.stroke = "var(--green)";
        } else {
            circle.style.stroke = "var(--amber)";
        }

        // Update Linear Progress Bar
        const fill = document.getElementById("ram-progress-fill");
        fill.style.width = `${pct}%`;
        fill.style.background = specs.avail_ram_gb >= specs.target_free_gb ? 
            "linear-gradient(90deg, var(--cyan-bg), var(--cyan))" : 
            "linear-gradient(90deg, var(--amber-bg), var(--amber))";

        document.getElementById("ram-used-detail").innerText = `${specs.used_ram_gb} GB Used`;
        document.getElementById("ram-avail-detail").innerText = `${specs.avail_ram_gb} GB Free`;

        // Update Status Panel on FPS Page
        document.getElementById("fps-status-timer").innerText = `${specs.timer_res_ms || 1.0} ms (Locked)`;

        // Update Badges & Engine Subtitle
        document.getElementById("badge-os").innerText = `💻 ${specs.os_name} (${hw.cpu_cores_logical} Cores)`;
        const cppStr = hw.cpp_engine_active ? "⚡ C++ ENGINE ACTIVE" : "🐍 PYTHON CORE";
        document.getElementById("engine-subtitle").innerText = `${cppStr} | ${hw.device_profile} | GPU: ${hw.gpu_vendor}`;

        // Settings Specs List
        const specsList = document.getElementById("settings-specs-list");
        if (specsList) {
            specsList.innerHTML = `
                <li>• Operating System: ${specs.os_name}</li>
                <li>• Logical CPU Cores: ${hw.cpu_cores_logical}</li>
                <li>• GPU Vendor: ${hw.gpu_vendor}</li>
                <li>• Hardware Profile: ${hw.device_profile}</li>
                <li>• System Timer Precision: ${specs.timer_res_ms} ms</li>
                <li>• Native C++ Engine: ${hw.cpp_engine_active ? 'Active' : 'Not Compiled'}</li>
                <li>• Total Memory: ${specs.total_ram_gb} GB</li>
                <li>• Target Free Threshold: ${specs.target_free_gb} GB</li>
            `;
        }
    } catch (e) {
        console.error("Stats refresh error:", e);
    }
}

// Action Trigger Gateway
async function triggerAction(actionId, extraArg = null) {
    logToConsole(`[ACTION START] Invoking '${actionId}'...`);

    if (window.pywebview && window.pywebview.api) {
        try {
            const res = await window.pywebview.api.execute_action(actionId, extraArg);
            if (res && res.logs) {
                res.logs.forEach(msg => logToConsole(msg));
            } else if (typeof res === "string") {
                logToConsole(res);
            }
            refreshSystemStats();
        } catch (err) {
            logToConsole(`[ACTION ERROR] ${err}`);
        }
    } else {
        logToConsole(`[ACTION MOCK] Executed '${actionId}' in preview mode.`);
    }
}

// Process Table Handler
async function refreshTopProcesses() {
    try {
        let procs = [];
        if (window.pywebview && window.pywebview.api) {
            procs = await window.pywebview.api.get_top_ram_processes(15);
        } else {
            procs = [
                { pid: 14208, name: "Valorant.exe", mem_mb: 2840.5 },
                { pid: 8912, name: "chrome.exe", mem_mb: 1420.2 },
                { pid: 4310, name: "Discord.exe", mem_mb: 480.1 }
            ];
        }

        const tbody = document.getElementById("top-procs-tbody");
        tbody.innerHTML = "";

        procs.forEach(p => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><code>${p.pid}</code></td>
                <td><strong>${p.name}</strong></td>
                <td class="text-cyan">${p.mem_mb} MB</td>
                <td><button class="btn btn-sm btn-red" onclick="triggerAction('kill_process', ${p.pid})">End Process</button></td>
            `;
            tbody.appendChild(tr);
        });

        logToConsole(`[TOP PROCESSES] Loaded top ${procs.length} memory consuming processes.`);
    } catch (e) {
        console.error("Process refresh error:", e);
    }
}

// Tutorial Modal System
async function checkFirstRunStatus() {
    try {
        if (window.pywebview && window.pywebview.api) {
            const firstRun = await window.pywebview.api.is_first_run();
            if (firstRun) {
                openTutorialModal();
            }
        }
    } catch (e) {}
}

function openTutorialModal() {
    currentTutorialStep = 0;
    document.getElementById("tutorial-modal").classList.add("active");
    updateTutorialModalDisplay();
}

function closeTutorialModal(markCompleted = true) {
    document.getElementById("tutorial-modal").classList.remove("active");
    if (markCompleted && window.pywebview && window.pywebview.api) {
        window.pywebview.api.set_first_run_completed(true);
    }
}

function populateTutorialJumpSelect() {
    const sel = document.getElementById("step-jump-select");
    sel.innerHTML = "";
    TUTORIAL_STEPS.forEach((step, idx) => {
        const opt = document.createElement("option");
        opt.value = idx;
        opt.innerText = `${idx + 1}. ${step.title}`;
        sel.appendChild(opt);
    });
}

function jumpToTutorialStep(stepIdx) {
    currentTutorialStep = parseInt(stepIdx);
    updateTutorialModalDisplay();
}

function updateTutorialModalDisplay() {
    const step = TUTORIAL_STEPS[currentTutorialStep];

    document.getElementById("step-jump-select").value = currentTutorialStep;
    document.getElementById("modal-cat-badge").innerText = `STEP ${currentTutorialStep + 1} OF ${TUTORIAL_STEPS.length} • ${step.category}`;
    document.getElementById("modal-cat-badge").style.color = step.color;
    document.getElementById("modal-title").innerText = `${step.icon} ${step.title}`;

    document.getElementById("modal-how").innerText = step.how;
    document.getElementById("modal-why").innerText = step.why;
    document.getElementById("modal-when").innerText = step.when;

    // Action Test Button
    const btnAction = document.getElementById("btn-modal-try-action");
    if (step.action_id && step.action_label) {
        btnAction.innerText = step.action_label;
        document.getElementById("modal-action-wrapper").style.display = "block";
    } else {
        document.getElementById("modal-action-wrapper").style.display = "none";
    }

    // Progress Bar Fill
    const pct = ((currentTutorialStep + 1) / TUTORIAL_STEPS.length) * 100;
    const fill = document.getElementById("modal-prog-fill");
    fill.style.width = `${pct}%`;
    fill.style.background = step.color;

    // Prev / Next Buttons
    document.getElementById("btn-modal-prev").disabled = (currentTutorialStep === 0);
    const btnNext = document.getElementById("btn-modal-next");
    if (currentTutorialStep === TUTORIAL_STEPS.length - 1) {
        btnNext.innerText = "🎓 Finish & Open App";
        btnNext.className = "btn btn-green";
    } else {
        btnNext.innerText = "Next Step ▶";
        btnNext.className = "btn btn-cyan";
    }
}

function prevTutorialStep() {
    if (currentTutorialStep > 0) {
        currentTutorialStep--;
        updateTutorialModalDisplay();
    }
}

function nextTutorialStep() {
    if (currentTutorialStep < TUTORIAL_STEPS.length - 1) {
        currentTutorialStep++;
        updateTutorialModalDisplay();
    } else {
        closeTutorialModal(true);
    }
}

function executeModalStepAction() {
    const step = TUTORIAL_STEPS[currentTutorialStep];
    if (step.action_id) {
        triggerAction(step.action_id);
    }
}

// Category Tabs in Tutorial Hub
function switchCategoryTab(tabId) {
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

    document.querySelector(`.tab-btn[data-tab="${tabId}"]`).classList.add("active");
    document.getElementById(tabId).classList.add("active");
}

function populateTutorialCategoryTabs() {
    const listGaming = document.getElementById("tut-list-gaming");
    const listMemory = document.getElementById("tut-list-memory");
    const listTools = document.getElementById("tut-list-tools");

    const categories = {
        "tab-gaming": ["welcome", "fps_booster", "asset_loader", "potato_mode", "ultimate_power"],
        "tab-memory": ["monster_optimizer", "trim_ram", "purge_standby", "auto_guard"],
        "tab-tools": ["clear_temp", "game_picker", "shader_cleaner", "end_bloatware", "top_procs"]
    };

    TUTORIAL_STEPS.forEach(step => {
        const card = document.createElement("div");
        card.className = "glass-card tut-card-item";

        let actionBtnHtml = "";
        if (step.action_id) {
            actionBtnHtml = `<button class="btn btn-sm btn-surface" onclick="triggerAction('${step.action_id}')">🧪 Try ${step.title}</button>`;
        }

        card.innerHTML = `
            <div class="tut-card-head">
                <h4 style="color: ${step.color};">${step.icon} ${step.title}</h4>
                ${actionBtnHtml}
            </div>
            <div class="tut-detail-line"><strong>🛠️ HOW:</strong> ${step.how}</div>
            <div class="tut-detail-line text-green"><strong>💡 WHY:</strong> ${step.why}</div>
            <div class="tut-detail-line text-amber"><strong>⏱️ WHEN:</strong> ${step.when}</div>
        `;

        if (categories["tab-gaming"].includes(step.id)) listGaming.appendChild(card);
        if (categories["tab-memory"].includes(step.id)) listMemory.appendChild(card);
        if (categories["tab-tools"].includes(step.id)) listTools.appendChild(card);
    });
}

// Console Logging Helpers
function logToConsole(message) {
    const output = document.getElementById("console-output");
    if (!output) return;

    const time = new Date().toLocaleTimeString();
    output.value += `[${time}] ${message}\n`;
    output.scrollTop = output.scrollHeight;
}

function clearConsoleLog() {
    document.getElementById("console-output").value = "";
}

function copyConsoleLog() {
    const output = document.getElementById("console-output");
    navigator.clipboard.writeText(output.value);
    logToConsole("[CONSOLE] Console log text copied to clipboard!");
}
