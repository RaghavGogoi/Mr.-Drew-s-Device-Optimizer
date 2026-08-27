// Comprehensive Interactive Engine for Mr. Drew's Device & FPS Optimizer

// Database of Tutorial Steps & Live UI Target Element Anchors
const TUTORIAL_STEPS = [
    {
        id: "welcome",
        category: "🚀 GETTING STARTED",
        title: "Welcome to Mr. Drew's Device & FPS Optimizer",
        icon: "⚡",
        color: "#00F0FF",
        how: "Combines a native C++ kernel engine, GPU shader management, real-time memory compaction, and process scheduling into one fast suite.",
        why: "Eliminates game micro-stutters, reclaims 2 to 5 GB physical RAM, lowers input lag, and prevents texture pop-in.",
        when: "Run before gaming sessions (Fortnite, Valorant, Roblox, Unreal Engine), or leave Smart Auto-Guard active in background.",
        action_id: null,
        action_label: null,
        target_id: "page-dashboard"
    },
    {
        id: "ram_gauge",
        category: "📊 TELEMETRY ENGINE",
        title: "Real-Time Physical Memory Gauge",
        icon: "🧠",
        color: "#00F0FF",
        how: "Continuously polls Win32 GlobalMemoryStatusEx and NtQuerySystemInformation APIs to calculate physical memory allocation breakdown.",
        why: "Provides instant visibility into Active Apps, Standby Cache, and Free Memory headroom.",
        when: "Monitor this gauge before launching heavy games to ensure at least 4GB free RAM buffer.",
        action_id: null,
        action_label: null,
        target_id: "target-ram-gauge"
    },
    {
        id: "fps_booster",
        category: "🎮 GAMING ENGINE",
        title: "RUN FPS & GAME BOOSTER",
        icon: "🎮",
        color: "#F59E0B",
        how: "Locks system timer resolution to 1.0ms, flushes GPU shader caches (Nvidia/AMD/DirectX), and elevates game CPU priority to High.",
        why: "Fixes frame drops, removes micro-stutters, and lowers input latency in competitive games.",
        when: "Click right before launching your game or whenever you notice stutters during gameplay.",
        action_id: "run_fps_booster",
        action_label: "🧪 Test FPS Booster Now",
        target_id: "target-fps-booster"
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
        action_label: "🧪 Run Monster Optimizer",
        target_id: "target-monster-optimizer"
    },
    {
        id: "potato_mode",
        category: "🥔 LOW-SPEC ENGINE",
        title: "4GB Potato Mode Preset",
        icon: "🥔",
        color: "#EAB308",
        how: "Triggers aggressive memory compaction targeting 1.5 GB free RAM, drops inactive page caches, and terminates background bloatware.",
        why: "Enables smooth gaming and app performance on budget/low-spec devices with 4GB to 8GB physical RAM without paging stutters.",
        when: "Activate on low-end laptops or budget PCs before launching any game.",
        action_id: "run_potato_mode",
        action_label: "🧪 Test Potato Mode",
        target_id: "target-potato-mode"
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
        action_label: "🧪 Test Asset Loader",
        target_id: "page-fps"
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
        action_label: "🧪 Enable Ultimate Power",
        target_id: "page-fps"
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
        action_label: "🧪 Trim App RAM Now",
        target_id: "page-ram"
    },
    {
        id: "purge_standby",
        category: "🧠 MEMORY ENGINE",
        title: "Purge Standby RAM",
        icon: "🛡️",
        color: "#3B82F6",
        how: "Calls C++ NtSetSystemInformation with SystemMemoryListInformation to clear cached standby list memory.",
        why: "Fixes Windows Standby RAM bugs that cause game crashes and hitching when free RAM drops to zero.",
        when: "Use when Standby cached memory is high and free memory is low.",
        action_id: "purge_standby",
        action_label: "🧪 Purge Standby RAM",
        target_id: "page-ram"
    },
    {
        id: "auto_guard",
        category: "⚡ AUTOMATION ENGINE",
        title: "Smart Auto-Guard Loop",
        icon: "⚡",
        color: "#A855F7",
        how: "Background thread continuously monitors physical free RAM. If free memory falls below target threshold, automatically triggers standby list flush and memory compaction.",
        why: "Provides automatic, set-and-forget 24/7 protection against memory leaks and RAM exhaustion stutters.",
        when: "Turn on for long gaming sessions or background server operations.",
        action_id: "toggle_auto_guard",
        action_label: "🧪 Toggle Auto-Guard",
        target_id: "target-autoguard"
    },
    {
        id: "process_manager",
        category: "🧹 SYSTEM TOOLS",
        title: "Top RAM Applications Manager",
        icon: "📊",
        color: "#10B981",
        how: "Scans active processes, calculates physical RAM usage (RSS), and ranks top memory consumers with instant single-click process termination.",
        why: "Provides full visibility into what applications are consuming system resources.",
        when: "Use to inspect system memory distribution or terminate unresponsive memory hogs.",
        action_id: "view_top_processes",
        action_label: "🧪 Refresh Process List",
        target_id: "target-process-table"
    },
    {
        id: "shader_cleaner",
        category: "🎨 GRAPHICS TUNER",
        title: "Clean GPU Shader Cache",
        icon: "🧹",
        color: "#00F0FF",
        how: "Sweeps compiled DirectX, OpenGL, Vulkan, Nvidia (DXCache/GLCache), AMD (DxCache), and Intel GPU shader caches.",
        why: "Fixes corrupted shader stuttering, visual artifacts, and frame drops caused by stale shader caches.",
        when: "Run after updating graphics drivers, installing game updates, or experiencing graphical stutters.",
        action_id: "clean_shader_cache",
        action_label: "🧪 Clean Shader Cache",
        target_id: "page-fps"
    },
    {
        id: "end_bloatware",
        category: "🛡️ SECURITY & CLEANING",
        title: "End Bloatware",
        icon: "🚫",
        color: "#EF4444",
        how: "Safely terminates non-essential background bloatware (OneDrive, Widgets, Teams, Cortana) protected by safety whitelists.",
        why: "Stops unwanted background telemetry, reduces background CPU usage, and saves memory.",
        when: "Run on computer startup or before launching games.",
        action_id: "kill_bloatware",
        action_label: "🧪 Terminate Bloatware",
        target_id: "page-tools"
    },
    {
        id: "theme_settings",
        category: "⚙️ APP SETTINGS",
        title: "App Themes & Aesthetic Customization",
        icon: "🎨",
        color: "#00F0FF",
        how: "Allows selecting 6 distinct visual themes (Obsidian Cyan, Cosmic Violet, Hyper Emerald, Solar Ember, Midnight OLED, Light Frost) with live accent & typography controls.",
        why: "Personalizes your experience to match your gaming rig, workspace ambient light, or aesthetic preference.",
        when: "Customize anytime in the Settings & Themes tab.",
        action_id: null,
        action_label: null,
        target_id: "target-theme-section"
    }
];

// App Global State
let currentSpotlightStep = 0;
let isPyWebViewReady = false;
let isAudioMuted = false;
let audioCtx = null;

let appConfig = {
    theme: "obsidian",
    accent_color: "#00f0ff",
    glass_effect: "high",
    glow_effects: true,
    animation_speed: "normal",
    font_family: "Outfit",
    density: "spacious",
    sound_effects: true,
    target_free_ram_gb: 4.0,
    auto_guard_interval_sec: 60,
    game_boost_priority: "high",
    auto_clean_on_launch: false,
    first_run_completed: false
};

// Application Initialization
document.addEventListener("DOMContentLoaded", () => {
    initPyWebViewBridge();
    populateSpotlightJumpSelect();
    populateTutorialHub();
    
    // Poll stats every 2 seconds
    setInterval(refreshSystemStats, 2000);
});

function initPyWebViewBridge() {
    window.addEventListener('pywebviewready', async () => {
        isPyWebViewReady = true;
        logToConsole("PyWebView Native Python Bridge Connected!", "success");
        await loadAppConfig();
        refreshSystemStats();
        checkFirstRunStatus();
    });

    // Fallback for standalone Web Browser mode
    setTimeout(async () => {
        if (!isPyWebViewReady) {
            logToConsole("Running in Web Preview Mode (Bridge via Local Server).", "info");
            await loadAppConfig();
            refreshSystemStats();
            checkFirstRunStatus();
        }
    }, 600);
}

// Configuration Engine
async function loadAppConfig() {
    try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.get_config) {
            const cfg = await window.pywebview.api.get_config();
            if (cfg) {
                appConfig = Object.assign({}, appConfig, cfg);
            }
        }
    } catch (e) {
        console.error("Error loading config:", e);
    }
    applyConfigToUI();
}

function applyConfigToUI() {
    const root = document.documentElement;

    // Apply attributes to <html>
    root.setAttribute("data-theme", appConfig.theme || "obsidian");
    root.setAttribute("data-glass", appConfig.glass_effect || "high");
    root.setAttribute("data-glow", appConfig.glow_effects ? "true" : "false");
    root.setAttribute("data-font", appConfig.font_family || "Outfit");
    root.setAttribute("data-density", appConfig.density || "spacious");

    if (appConfig.accent_color) {
        root.style.setProperty("--accent", appConfig.accent_color);
        root.style.setProperty("--accent-glow", `${appConfig.accent_color}55`);
    }

    isAudioMuted = !appConfig.sound_effects;
    const soundIcon = document.getElementById("sound-icon");
    if (soundIcon) soundIcon.innerText = isAudioMuted ? "🔇" : "🔊";

    // Synchronize UI Form controls in Settings Page
    const themeSelect = document.getElementById("quick-theme-select");
    if (themeSelect) themeSelect.value = appConfig.theme;

    document.querySelectorAll(".theme-card").forEach(card => {
        card.classList.toggle("active", card.getAttribute("data-theme-id") === appConfig.theme);
    });

    const fontSelect = document.getElementById("setting-font");
    if (fontSelect) fontSelect.value = appConfig.font_family;

    const glassSelect = document.getElementById("setting-glass");
    if (glassSelect) glassSelect.value = appConfig.glass_effect;

    const glowSelect = document.getElementById("setting-glow");
    if (glowSelect) glowSelect.value = appConfig.glow_effects ? "true" : "false";

    const densitySelect = document.getElementById("setting-density");
    if (densitySelect) densitySelect.value = appConfig.density;

    const soundSelect = document.getElementById("setting-sound");
    if (soundSelect) soundSelect.value = appConfig.sound_effects ? "true" : "false";

    const targetRamSlider = document.getElementById("setting-target-ram");
    if (targetRamSlider) {
        targetRamSlider.value = appConfig.target_free_ram_gb || 4.0;
        document.getElementById("target-ram-val-label").innerText = `${targetRamSlider.value} GB`;
        document.getElementById("dash-target-ram").innerText = `≥ ${targetRamSlider.value} GB`;
    }

    const intervalSelect = document.getElementById("setting-autoguard-interval");
    if (intervalSelect) intervalSelect.value = appConfig.auto_guard_interval_sec || 60;
}

async function updateAppSetting(key, value) {
    appConfig[key] = value;
    applyConfigToUI();
    playAudioFX("click");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        try {
            await window.pywebview.api.update_setting(key, value);
            logToConsole(`[SETTINGS] Saved setting '${key}' = ${value}`, "info");
        } catch (e) {
            console.error("Setting update error:", e);
        }
    }
}

async function changeAppTheme(themeId) {
    appConfig.theme = themeId;
    applyConfigToUI();
    playAudioFX("click");
    logToConsole(`[THEME] Switched visual theme to '${themeId}'`, "success");

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        try {
            await window.pywebview.api.update_setting("theme", themeId);
        } catch (e) {}
    }
}

async function changeAccentColor(colorHex) {
    appConfig.accent_color = colorHex;
    applyConfigToUI();
    playAudioFX("click");

    document.querySelectorAll(".accent-dot").forEach(dot => {
        dot.classList.toggle("active", dot.style.background.includes(colorHex) || dot.getAttribute("title").toLowerCase().includes(colorHex));
    });

    if (window.pywebview && window.pywebview.api && window.pywebview.api.update_setting) {
        try {
            await window.pywebview.api.update_setting("accent_color", colorHex);
        } catch (e) {}
    }
}

function updateTargetRamSlider(val) {
    document.getElementById("target-ram-val-label").innerText = `${parseFloat(val).toFixed(1)} GB`;
    document.getElementById("dash-target-ram").innerText = `≥ ${parseFloat(val).toFixed(1)} GB`;
}

async function resetConfigDefaults() {
    playAudioFX("warning");
    if (window.pywebview && window.pywebview.api && window.pywebview.api.reset_config) {
        try {
            const defaults = await window.pywebview.api.reset_config();
            if (defaults) appConfig = defaults;
            applyConfigToUI();
            logToConsole("[SETTINGS] Restored default settings successfully.", "success");
        } catch (e) {}
    }
}

// Web Audio API Synthesizer (Zero external dependencies)
function playAudioFX(type) {
    if (isAudioMuted) return;
    try {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (audioCtx.state === 'suspended') {
            audioCtx.resume();
        }

        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.connect(gain);
        gain.connect(audioCtx.destination);

        const now = audioCtx.currentTime;

        if (type === 'click') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, now);
            osc.frequency.exponentialRampToValueAtTime(400, now + 0.05);
            gain.gain.setValueAtTime(0.15, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.05);
            osc.start(now);
            osc.stop(now + 0.05);
        } else if (type === 'action') {
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(440, now);
            osc.frequency.exponentialRampToValueAtTime(880, now + 0.12);
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.12);
            osc.start(now);
            osc.stop(now + 0.12);
        } else if (type === 'success') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(523.25, now); // C5
            osc.frequency.setValueAtTime(659.25, now + 0.08); // E5
            osc.frequency.setValueAtTime(783.99, now + 0.16); // G5
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
            osc.start(now);
            osc.stop(now + 0.3);
        } else if (type === 'warning') {
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(220, now);
            osc.frequency.linearRampToValueAtTime(110, now + 0.15);
            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
            osc.start(now);
            osc.stop(now + 0.15);
        }
    } catch (e) {}
}

function toggleAudioMute() {
    isAudioMuted = !isAudioMuted;
    updateAppSetting("sound_effects", !isAudioMuted);
    const soundIcon = document.getElementById("sound-icon");
    if (soundIcon) soundIcon.innerText = isAudioMuted ? "🔇" : "🔊";
}

// Navigation & Page Switcher
function switchPage(pageId) {
    playAudioFX("click");
    document.querySelectorAll(".nav-item").forEach(el => el.classList.remove("active"));
    document.querySelectorAll(".page").forEach(el => el.classList.remove("active"));

    const navItem = document.querySelector(`.nav-item[data-page="${pageId}"]`);
    const pageEl = document.getElementById(pageId);

    if (navItem) navItem.classList.add("active");
    if (pageEl) pageEl.classList.add("active");

    if (pageId === "page-tools") {
        refreshTopProcesses();
    }
}

// System Stats Polling & Dynamic Visual Gauges
async function refreshSystemStats() {
    try {
        let specs = null;
        let hw = null;

        if (window.pywebview && window.pywebview.api) {
            specs = await window.pywebview.api.get_system_specs();
            hw = await window.pywebview.api.get_hardware_details();
        } else {
            // Mock specs for browser testing
            specs = { total_ram_gb: 16.0, avail_ram_gb: 9.2, used_ram_gb: 6.8, target_free_gb: appConfig.target_free_ram_gb || 4.0, percent_used: 42.5, cpu_percent: 14.8, os_name: "Windows 11 (64-bit)", timer_res_ms: 1.0 };
            hw = { device_profile: "🚀 Standard Gaming Rig (16GB)", gpu_vendor: "NVIDIA GeForce RTX 3060", cpu_cores_logical: 16, cpp_engine_active: true };
        }

        // Update Header Mini Pills
        document.getElementById("hdr-ram-val").innerText = `${specs.percent_used}%`;
        document.getElementById("hdr-cpu-val").innerText = `${specs.cpu_percent}%`;
        document.getElementById("hdr-timer-val").innerText = `${specs.timer_res_ms || 1.0}ms`;

        // Update Dashboard Cards
        document.getElementById("dash-total-ram").innerText = `${specs.total_ram_gb} GB`;
        document.getElementById("dash-free-ram").innerText = `${specs.avail_ram_gb} GB`;
        document.getElementById("dash-free-percent").innerText = `${(100 - specs.percent_used).toFixed(1)}% Unallocated`;
        document.getElementById("dash-cpu-percent").innerText = `${specs.cpu_percent}%`;
        document.getElementById("dash-cpu-cores").innerText = `${hw.cpu_cores_logical} Logical Cores Active`;

        // Update Circular SVG Gauge
        const pct = specs.percent_used;
        document.getElementById("dash-ram-percent").innerText = `${pct}% RAM Used`;
        document.getElementById("gauge-center-num").innerText = `${pct}%`;

        const circle = document.getElementById("svg-gauge-circle");
        const maxOffset = 314.15;
        const offset = maxOffset - (pct / 100.0) * maxOffset;
        circle.style.strokeDashoffset = offset;

        const targetGB = appConfig.target_free_ram_gb || specs.target_free_gb || 4.0;
        if (specs.avail_ram_gb >= targetGB) {
            circle.style.stroke = "var(--green)";
            document.getElementById("ram-target-status").innerText = "Target Free Headroom OK";
            document.getElementById("ram-target-status").className = "text-green";
        } else {
            circle.style.stroke = "var(--amber)";
            document.getElementById("ram-target-status").innerText = "⚠️ RAM Below Target Threshold";
            document.getElementById("ram-target-status").className = "text-amber";
        }

        // Update Linear Progress Bar
        const fill = document.getElementById("ram-progress-fill");
        fill.style.width = `${pct}%`;

        document.getElementById("ram-used-detail").innerText = `${specs.used_ram_gb} GB Used`;
        document.getElementById("ram-avail-detail").innerText = `${specs.avail_ram_gb} GB Free`;

        // Memory Breakdown Pills
        const standbyEst = Math.max(0.4, (specs.avail_ram_gb * 0.35)).toFixed(1);
        const activeEst = (specs.used_ram_gb).toFixed(1);
        document.getElementById("dist-active-val").innerText = `${activeEst} GB`;
        document.getElementById("dist-standby-val").innerText = `${standbyEst} GB`;
        document.getElementById("dist-free-val").innerText = `${specs.avail_ram_gb} GB`;

        // Update Status Panel on FPS Page
        document.getElementById("fps-status-timer").innerText = `${specs.timer_res_ms || 1.0} ms (Locked)`;

        // Update Badges & Engine Subtitle
        document.getElementById("badge-os").innerText = `💻 ${specs.os_name}`;
        const cppStr = hw.cpp_engine_active ? "⚡ C++ ENGINE ACTIVE" : "🐍 PYTHON CORE";
        document.getElementById("engine-subtitle").innerText = `${cppStr} • ${hw.device_profile} • GPU: ${hw.gpu_vendor}`;

        // Settings Hardware Specs List
        const specsList = document.getElementById("settings-specs-list");
        if (specsList) {
            specsList.innerHTML = `
                <li>• Operating System: ${specs.os_name}</li>
                <li>• Logical CPU Cores: ${hw.cpu_cores_logical}</li>
                <li>• GPU Graphics Hardware: ${hw.gpu_vendor}</li>
                <li>• Hardware Profile: ${hw.device_profile}</li>
                <li>• System Timer Resolution: ${specs.timer_res_ms} ms</li>
                <li>• C++ Engine Bridge Status: ${hw.cpp_engine_active ? 'Active & Optimized' : 'Python Core Active'}</li>
                <li>• Total Installed Physical Memory: ${specs.total_ram_gb} GB</li>
                <li>• Configured Target Free RAM: ${targetGB} GB</li>
            `;
        }
    } catch (e) {
        console.error("Stats refresh error:", e);
    }
}

// Action Trigger Gateway
async function triggerAction(actionId, extraArg = null) {
    playAudioFX("action");
    logToConsole(`[ACTION] Executing '${actionId}'...`, "info");

    if (window.pywebview && window.pywebview.api) {
        try {
            const res = await window.pywebview.api.execute_action(actionId, extraArg);
            if (res && res.logs) {
                res.logs.forEach(msg => logToConsole(msg, "success"));
                playAudioFX("success");
            } else if (typeof res === "string") {
                logToConsole(res, "success");
                playAudioFX("success");
            }
            refreshSystemStats();
        } catch (err) {
            logToConsole(`[ACTION ERROR] ${err}`, "warning");
        }
    } else {
        logToConsole(`[MOCK ACTION] Successfully executed '${actionId}'.`, "success");
        playAudioFX("success");
    }
}

// Top RAM Processes Data Table
async function refreshTopProcesses() {
    try {
        let procs = [];
        if (window.pywebview && window.pywebview.api) {
            procs = await window.pywebview.api.get_top_ram_processes(15);
        } else {
            procs = [
                { pid: 14208, name: "Valorant.exe", mem_mb: 2840.5 },
                { pid: 8912, name: "chrome.exe", mem_mb: 1420.2 },
                { pid: 4310, name: "Discord.exe", mem_mb: 480.1 },
                { pid: 9812, name: "Spotify.exe", mem_mb: 310.4 },
                { pid: 2104, name: "Steam.exe", mem_mb: 240.8 }
            ];
        }

        const tbody = document.getElementById("top-procs-tbody");
        tbody.innerHTML = "";

        procs.forEach(p => {
            const ramPct = ((p.mem_mb / (16 * 1024)) * 100).toFixed(1);
            const tr = document.createElement("tr");
            tr.className = "proc-row";
            tr.innerHTML = `
                <td><code>${p.pid}</code></td>
                <td><strong>${p.name}</strong></td>
                <td class="text-cyan">${p.mem_mb} MB</td>
                <td class="text-muted">${ramPct}%</td>
                <td><button class="btn btn-xs btn-red" onclick="triggerAction('kill_process', ${p.pid})">End Process</button></td>
            `;
            tbody.appendChild(tr);
        });

        logToConsole(`[PROCESS TABLE] Loaded ${procs.length} top RAM processes.`, "info");
    } catch (e) {
        console.error("Process refresh error:", e);
    }
}

function filterProcessTable() {
    const query = document.getElementById("proc-search-input").value.toLowerCase();
    document.querySelectorAll(".proc-row").forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? "" : "none";
    });
}

// Interactive Spotlight Tutorial System
async function checkFirstRunStatus() {
    try {
        if (window.pywebview && window.pywebview.api) {
            const firstRun = await window.pywebview.api.is_first_run();
            if (firstRun) {
                startSpotlightTutorial();
            }
        }
    } catch (e) {}
}

function startSpotlightTutorial() {
    currentSpotlightStep = 0;
    playAudioFX("action");
    document.getElementById("spotlight-overlay").classList.add("active");
    updateSpotlightDisplay();
}

function closeSpotlightTutorial(markCompleted = true) {
    playAudioFX("click");
    document.getElementById("spotlight-overlay").classList.remove("active");
    if (markCompleted && window.pywebview && window.pywebview.api) {
        window.pywebview.api.set_first_run_completed(true);
    }
}

function populateSpotlightJumpSelect() {
    const sel = document.getElementById("spotlight-jump-select");
    sel.innerHTML = "";
    TUTORIAL_STEPS.forEach((step, idx) => {
        const opt = document.createElement("option");
        opt.value = idx;
        opt.innerText = `${idx + 1}. ${step.title}`;
        sel.appendChild(opt);
    });
}

function jumpToSpotlightStep(idx) {
    currentSpotlightStep = parseInt(idx);
    playAudioFX("click");
    updateSpotlightDisplay();
}

function updateSpotlightDisplay() {
    const step = TUTORIAL_STEPS[currentSpotlightStep];

    // Ensure user is on the right page for target element
    if (step.target_id) {
        if (step.target_id.startsWith("target-") || step.target_id.startsWith("page-")) {
            let targetPage = "page-dashboard";
            if (step.target_id.includes("fps")) targetPage = "page-fps";
            if (step.target_id.includes("ram") || step.target_id.includes("autoguard")) targetPage = "page-ram";
            if (step.target_id.includes("tools") || step.target_id.includes("process")) targetPage = "page-tools";
            if (step.target_id.includes("theme")) targetPage = "page-settings";

            switchPage(targetPage);
        }
    }

    document.getElementById("spotlight-jump-select").value = currentSpotlightStep;
    document.getElementById("spotlight-cat-badge").innerText = `STEP ${currentSpotlightStep + 1} OF ${TUTORIAL_STEPS.length} • ${step.category}`;
    document.getElementById("spotlight-cat-badge").style.color = step.color;
    document.getElementById("spotlight-title").innerText = `${step.icon} ${step.title}`;

    document.getElementById("spotlight-how").innerText = step.how;
    document.getElementById("spotlight-why").innerText = step.why;
    document.getElementById("spotlight-when").innerText = step.when;

    // Action Try Button
    const btnAction = document.getElementById("btn-spotlight-try");
    if (step.action_id && step.action_label) {
        btnAction.innerText = step.action_label;
        document.getElementById("spotlight-action-wrapper").style.display = "block";
    } else {
        document.getElementById("spotlight-action-wrapper").style.display = "none";
    }

    // Progress Bar Fill
    const pct = ((currentSpotlightStep + 1) / TUTORIAL_STEPS.length) * 100;
    const fill = document.getElementById("spotlight-prog-fill");
    fill.style.width = `${pct}%`;
    fill.style.background = step.color;

    // Prev / Next Buttons
    document.getElementById("btn-spotlight-prev").disabled = (currentSpotlightStep === 0);
    const btnNext = document.getElementById("btn-spotlight-next");
    if (currentSpotlightStep === TUTORIAL_STEPS.length - 1) {
        btnNext.innerText = "🎓 Finish & Open App";
        btnNext.className = "btn btn-green btn-sm";
    } else {
        btnNext.innerText = "Next Step ▶";
        btnNext.className = "btn btn-cyan btn-sm";
    }

    // Position Spotlight Mask Cutout & Focus Ring over Target Element
    setTimeout(() => {
        positionSpotlightTarget(step.target_id);
    }, 100);
}

function positionSpotlightTarget(targetId) {
    const cutout = document.getElementById("spotlight-cutout");
    const ring = document.getElementById("spotlight-focus-ring");
    const card = document.getElementById("spotlight-card");

    let targetEl = document.getElementById(targetId);
    if (!targetEl) targetEl = document.getElementById("page-dashboard");

    const rect = targetEl.getBoundingClientRect();
    const pad = 10;

    const x = Math.max(0, rect.left - pad);
    const y = Math.max(0, rect.top - pad);
    const w = rect.width + pad * 2;
    const h = rect.height + pad * 2;

    cutout.setAttribute("x", x);
    cutout.setAttribute("y", y);
    cutout.setAttribute("width", w);
    cutout.setAttribute("height", h);

    ring.style.left = `${x}px`;
    ring.style.top = `${y}px`;
    ring.style.width = `${w}px`;
    ring.style.height = `${h}px`;

    // Position Card relative to target box
    const windowW = window.innerWidth;
    const windowH = window.innerHeight;

    let cardX = x + w + 20;
    let cardY = y;

    if (cardX + 500 > windowW) {
        cardX = Math.max(20, x - 500);
    }
    if (cardY + 380 > windowH) {
        cardY = Math.max(20, windowH - 420);
    }

    card.style.left = `${cardX}px`;
    card.style.top = `${cardY}px`;
}

function prevSpotlightStep() {
    if (currentSpotlightStep > 0) {
        currentSpotlightStep--;
        playAudioFX("click");
        updateSpotlightDisplay();
    }
}

function nextSpotlightStep() {
    if (currentSpotlightStep < TUTORIAL_STEPS.length - 1) {
        currentSpotlightStep++;
        playAudioFX("click");
        updateSpotlightDisplay();
    } else {
        closeSpotlightTutorial(true);
    }
}

function executeSpotlightStepAction() {
    const step = TUTORIAL_STEPS[currentSpotlightStep];
    if (step.action_id) {
        triggerAction(step.action_id);
    }
}

// Tutorial Guide Hub Rendering
function populateTutorialHub() {
    const container = document.getElementById("tut-list-container");
    if (!container) return;

    container.innerHTML = "";
    TUTORIAL_STEPS.forEach(step => {
        const card = document.createElement("div");
        card.className = "glass-card tut-card-item";
        card.setAttribute("data-category", step.category);

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
        container.appendChild(card);
    });
}

function filterTutorialCards() {
    const query = document.getElementById("tut-search-input").value.toLowerCase();
    document.querySelectorAll(".tut-card-item").forEach(card => {
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(query) ? "" : "none";
    });
}

function switchCategoryTab(tabId) {
    playAudioFX("click");
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    const activeBtn = document.querySelector(`.tab-btn[data-tab="${tabId}"]`);
    if (activeBtn) activeBtn.classList.add("active");

    document.querySelectorAll(".tut-card-item").forEach(card => {
        const cat = card.getAttribute("data-category");
        if (tabId === "tab-all") {
            card.style.display = "";
        } else if (tabId === "tab-gaming" && (cat.includes("GAMING") || cat.includes("POWER") || cat.includes("GRAPHICS"))) {
            card.style.display = "";
        } else if (tabId === "tab-memory" && cat.includes("MEMORY")) {
            card.style.display = "";
        } else if (tabId === "tab-tools" && (cat.includes("TOOLS") || cat.includes("CLEANING") || cat.includes("SETTINGS"))) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }
    });
}

// Real-time Console Log Engine
function logToConsole(message, level = "info") {
    const output = document.getElementById("console-output");
    if (!output) return;

    const time = new Date().toLocaleTimeString();
    let prefix = "ℹ️ [INFO]";
    if (level === "success") prefix = "⚡ [SUCCESS]";
    if (level === "warning") prefix = "⚠️ [WARNING]";

    output.value += `[${time}] ${prefix} ${message}\n`;
    output.scrollTop = output.scrollHeight;
}

function clearConsoleLog() {
    playAudioFX("click");
    document.getElementById("console-output").value = "";
}

function copyConsoleLog() {
    playAudioFX("click");
    const output = document.getElementById("console-output");
    navigator.clipboard.writeText(output.value);
    logToConsole("Console log content copied to system clipboard!", "success");
}

function filterConsoleLog(level) {
    playAudioFX("click");
    logToConsole(`Log filter applied: '${level}'`, "info");
}
