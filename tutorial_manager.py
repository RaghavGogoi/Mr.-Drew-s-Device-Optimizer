import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Callable, Optional
import config


# Comprehensive Database of All Features: HOW, WHY, and WHEN
TUTORIAL_STEPS: List[Dict[str, Any]] = [
    {
        "id": "welcome",
        "category": "🚀 GETTING STARTED",
        "title": "⚡ Welcome to Mr. Drew's Device & FPS Optimizer",
        "icon": "⚡",
        "color": "#00F0FF",
        "how": "Combines a native C++ NT Kernel engine, GPU shader management, real-time memory compaction, and process priority tuning into one super-fast suite.",
        "why": "Eliminates game micro-stutters, reclaims 2 to 5 GB physical RAM, lowers input lag, and prevents texture pop-in during heavy workloads.",
        "when": "Run before starting gaming sessions (Fortnite, Valorant, Roblox, Unreal Engine), when memory is high, or let Smart Auto-Guard run in background."
    },
    {
        "id": "fps_booster",
        "category": "🎮 GAMING ENGINE",
        "title": "🎮 RUN FPS & GAME BOOSTER",
        "icon": "🎮",
        "color": "#F59E0B",
        "how": "Invokes C++ native `timeBeginPeriod` to lock system timer resolution to 1.0ms, flushes GPU shader caches (Nvidia/AMD/Intel), and elevates game CPU priority.",
        "why": "Fixes frame drops, removes micro-stutters, and lowers input latency in competitive games.",
        "when": "Click right before launching your game or whenever you notice stutters during gameplay."
    },
    {
        "id": "asset_loader",
        "category": "🎮 GAMING ENGINE",
        "title": "🚀 Fast Asset Loader",
        "icon": "🚀",
        "color": "#10B981",
        "how": "Sets Disk I/O priority to High (`ProcessIoPriorityHigh`) for active games and protects loaded game assets from RAM working-set eviction.",
        "why": "Drastically accelerates map loading, texture streaming, and 3D asset rendering; stops texture pop-in.",
        "when": "Use when loading big open-world games, map transitions, or heavy Roblox / Unreal Engine projects."
    },
    {
        "id": "potato_mode",
        "category": "🥔 LOW-SPEC ENGINE",
        "title": "🥔 4GB Potato Mode",
        "icon": "🥔",
        "color": "#EAB308",
        "how": "Triggers aggressive low-RAM memory compaction targeting 1.5 GB free RAM, drops inactive page caches, and terminates background telemetry.",
        "why": "Enables smooth gaming and app performance on budget/low-spec devices with 4GB to 8GB physical RAM without paging file stutters.",
        "when": "Activate on low-end laptops or budget PCs before launching any game."
    },
    {
        "id": "ultimate_power",
        "category": "⚡ POWER ENGINE",
        "title": "⚡ Ultimate Power Mode",
        "icon": "⚡",
        "color": "#10B981",
        "how": "Forces Windows OS power scheme to High / Ultimate Performance (`8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c`), disabling CPU core parking and power throttle.",
        "why": "Ensures CPU cores run at peak clock speeds without sudden frequency drops during demanding scenes.",
        "when": "Enable when gaming, video editing, or rendering on desktop or plugged-in laptops."
    },
    {
        "id": "monster_optimizer",
        "category": "🧠 MEMORY ENGINE",
        "title": "🔥 RUN MONSTER OPTIMIZER",
        "icon": "🔥",
        "color": "#A855F7",
        "how": "Multi-stage deep RAM recovery: compacts background working sets via `EmptyWorkingSet`, flushes kernel standby page list, and sweeps temp memory.",
        "why": "Recovers the maximum possible physical memory (up to 3-6 GB RAM) in one click without closing critical system apps.",
        "when": "Use when overall RAM usage exceeds 80%, or before running memory-heavy applications."
    },
    {
        "id": "trim_ram",
        "category": "🧠 MEMORY ENGINE",
        "title": "✂️ Trim App RAM",
        "icon": "✂️",
        "color": "#00F0FF",
        "how": "Iterates through non-critical user applications and compacts their active working set memory into physical free RAM.",
        "why": "Instantly reclaims RAM held hostage by web browsers (Chrome, Edge) and background software (Discord, Spotify).",
        "when": "Use while multitasking when you want to free RAM without quitting open applications."
    },
    {
        "id": "purge_standby",
        "category": "🧠 MEMORY ENGINE",
        "title": "🛡️ Purge Standby RAM",
        "icon": "🛡️",
        "color": "#3B82F6",
        "how": "Calls C++ `NtSetSystemInformation` with `SystemMemoryListInformation` (or POSIX `drop_caches` on Linux/macOS) to clear cached standby list memory.",
        "why": "Fixes Windows Standby RAM bugs that cause game crashes and hitching when free RAM drops to zero.",
        "when": "Use when Standby cached memory is high and free memory is low."
    },
    {
        "id": "clear_temp",
        "category": "🧹 CLEANING ENGINE",
        "title": "🧹 Clear Temp Files",
        "icon": "🧹",
        "color": "#EC4899",
        "how": "Recursively cleans `%TEMP%`, `%SystemRoot%\\Temp`, log caches, and leftover installer clutter while bypassing locked files safely.",
        "why": "Frees up gigabytes of SSD/HDD drive space and removes system clutter.",
        "when": "Run weekly or whenever drive space is tight."
    },
    {
        "id": "game_picker",
        "category": "🎯 PRIORITY TUNER",
        "title": "🎯 Boost Game Priority",
        "icon": "🎯",
        "color": "#F59E0B",
        "how": "Lets you pick your active game process and elevates its OS scheduling priority class to High Priority.",
        "why": "Guarantees that the CPU allocates maximum execution clock cycles to your game over background threads.",
        "when": "Use whenever playing competitive multiplayer games or resource-demanding titles."
    },
    {
        "id": "shader_cleaner",
        "category": "🎨 GRAPHICS TUNER",
        "title": "🧹 Clean Shader Cache",
        "icon": "🧹",
        "color": "#00F0FF",
        "how": "Sweeps compiled DirectX, OpenGL, Vulkan, Nvidia (`DXCache`/`GLCache`), AMD (`DxCache`), and Intel GPU shader caches.",
        "why": "Fixes corrupted shader stuttering, visual artifacts, and frame drops caused by stale shader caches.",
        "when": "Run after updating graphics drivers, installing game updates, or experiencing graphical stutters."
    },
    {
        "id": "end_bloatware",
        "category": "🛡️ SECURITY & CLEANING",
        "title": "🚫 End Bloatware",
        "icon": "🚫",
        "color": "#EF4444",
        "how": "Safely terminates non-essential background bloatware (`OneDrive`, `Widgets`, `Teams`, `Cortana`) protected by safety whitelists.",
        "why": "Stops unwanted background telemetry, reduces background CPU usage, and saves memory.",
        "when": "Run on computer startup or before launching games."
    },
    {
        "id": "top_procs",
        "category": "📊 SYSTEM ANALYTICS",
        "title": "📊 Top RAM Apps",
        "icon": "📊",
        "color": "#10B981",
        "how": "Scans active processes, calculates physical RAM usage (RSS), and ranks top memory consumers in real-time.",
        "why": "Provides full visibility into what applications are consuming system resources.",
        "when": "Use to inspect system memory distribution or identify memory hogs."
    },
    {
        "id": "auto_guard",
        "category": "⚡ AUTOMATION ENGINE",
        "title": "⚡ Smart Auto-Guard (60s Loop)",
        "icon": "⚡",
        "color": "#A855F7",
        "how": "Background thread continuously monitors physical free RAM. If free memory falls below target threshold, automatically triggers standby list flush and memory compaction.",
        "why": "Provides automatic, set-and-forget 24/7 protection against memory leaks and RAM exhaustion stutters.",
        "when": "Turn on for long gaming sessions or background server operations."
    }
]


class InteractiveTutorialModal(tk.Toplevel):
    """
    Modern, interactive step-by-step tutorial modal dialog.
    Allows skipping at any time, browsing steps, and saving completion state.
    """
    def __init__(self, parent, on_complete_callback: Optional[Callable[[], None]] = None):
        super().__init__(parent)
        self.parent = parent
        self.on_complete_callback = on_complete_callback
        self.current_step = 0
        self.total_steps = len(TUTORIAL_STEPS)

        self.title("🎓 INTERACTIVE TUTORIAL - MR. DREW'S DEVICE OPTIMIZER")
        self.geometry("780x620")
        self.minsize(700, 560)
        self.resizable(True, True)

        # Style Palette
        self.BG_MAIN = "#030712"
        self.BG_CARD = "#0F172A"
        self.BG_INNER = "#1E293B"
        self.COLOR_BORDER = "#334155"
        self.TEXT_PRIMARY = "#F8FAFC"
        self.TEXT_MUTED = "#94A3B8"
        self.CYAN = "#00F0FF"

        self.configure(bg=self.BG_MAIN)
        self.transient(parent)
        self.grab_set()

        # Keyboard bindings
        self.bind("<Left>", lambda e: self._prev_step())
        self.bind("<Right>", lambda e: self._next_step())
        self.bind("<Escape>", lambda e: self._skip_tutorial())

        self._build_ui()
        self._update_step_display()

        # Center modal over parent window
        self.update_idletasks()
        try:
            px = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
            py = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
            self.geometry(f"+{max(0, px)}+{max(0, py)}")
        except Exception:
            pass

    def _build_ui(self):
        # Header bar
        header = tk.Frame(self, bg=self.BG_MAIN, padx=24, pady=16)
        header.pack(fill='x', side='top')

        lbl_top = tk.Label(
            header,
            text="🎓 INTERACTIVE STEP-BY-STEP GUIDED TOUR",
            font=('Segoe UI', 12, 'bold'),
            fg=self.CYAN,
            bg=self.BG_MAIN
        )
        lbl_top.pack(side='left')

        self.lbl_progress = tk.Label(
            header,
            text=f"Step 1 of {self.total_steps}",
            font=('Segoe UI', 10, 'bold'),
            fg=self.TEXT_MUTED,
            bg=self.BG_MAIN
        )
        self.lbl_progress.pack(side='right')

        # Visual Progress Bar Canvas
        prog_frame = tk.Frame(self, bg=self.BG_MAIN, padx=24)
        prog_frame.pack(fill='x')

        self.progress_canvas = tk.Canvas(prog_frame, height=6, bg="#0B132B", highlightthickness=0)
        self.progress_canvas.pack(fill='x')

        # Main Card Content Container
        self.card_frame = tk.Frame(
            self,
            bg=self.BG_CARD,
            padx=28,
            pady=24,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        self.card_frame.pack(fill='both', expand=True, padx=24, pady=16)

        # Step Category Badge
        self.lbl_cat = tk.Label(
            self.card_frame,
            text="CATEGORY",
            font=('Segoe UI', 9, 'bold'),
            fg=self.CYAN,
            bg=self.BG_CARD
        )
        self.lbl_cat.pack(anchor='w')

        # Step Title
        self.lbl_title = tk.Label(
            self.card_frame,
            text="Step Title",
            font=('Segoe UI', 18, 'bold'),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD,
            wraplength=680,
            justify='left'
        )
        self.lbl_title.pack(anchor='w', pady=(4, 16))

        # Three Detailed Blocks: HOW, WHY, WHEN
        self.block_how = self._create_info_block(self.card_frame, "🛠️ HOW IT WORKS (Technical Engine):", "#00F0FF")
        self.block_why = self._create_info_block(self.card_frame, "💡 WHY USE IT (Performance Benefit):", "#10B981")
        self.block_when = self._create_info_block(self.card_frame, "⏱️ WHEN TO USE IT (Best Scenario):", "#F59E0B")

        # Bottom Control Bar
        footer = tk.Frame(self, bg=self.BG_MAIN, padx=24, pady=16)
        footer.pack(fill='x', side='bottom')

        self.btn_skip = tk.Button(
            footer,
            text="⏭️ Skip Tutorial",
            font=('Segoe UI', 10, 'bold'),
            fg="#EF4444",
            bg="#1E293B",
            activebackground="#7F1D1D",
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=14,
            pady=8,
            command=self._skip_tutorial
        )
        self.btn_skip.pack(side='left')

        right_btns = tk.Frame(footer, bg=self.BG_MAIN)
        right_btns.pack(side='right')

        self.btn_prev = tk.Button(
            right_btns,
            text="◀ Previous",
            font=('Segoe UI', 10, 'bold'),
            fg=self.TEXT_PRIMARY,
            bg="#1E293B",
            activebackground="#334155",
            activeforeground=self.TEXT_PRIMARY,
            relief='flat',
            cursor='hand2',
            padx=14,
            pady=8,
            command=self._prev_step
        )
        self.btn_prev.pack(side='left', padx=(0, 8))

        self.btn_next = tk.Button(
            right_btns,
            text="Next Step ▶",
            font=('Segoe UI', 10, 'bold'),
            fg="#000000",
            bg=self.CYAN,
            activebackground="#0284C7",
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=16,
            pady=8,
            command=self._next_step
        )
        self.btn_next.pack(side='left')

    def _create_info_block(self, parent, header_text, accent_color):
        frame = tk.Frame(
            parent,
            bg=self.BG_INNER,
            padx=16,
            pady=10,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        frame.pack(fill='x', pady=6)

        hdr = tk.Label(
            frame,
            text=header_text,
            font=('Segoe UI', 9, 'bold'),
            fg=accent_color,
            bg=self.BG_INNER
        )
        hdr.pack(anchor='w')

        body = tk.Label(
            frame,
            text="Content text...",
            font=('Segoe UI', 9),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_INNER,
            wraplength=660,
            justify='left'
        )
        body.pack(anchor='w', pady=(3, 0))

        return body

    def _update_step_display(self):
        step_data = TUTORIAL_STEPS[self.current_step]

        self.lbl_progress.config(text=f"Step {self.current_step + 1} of {self.total_steps}")
        self.lbl_cat.config(text=step_data["category"], fg=step_data["color"])
        self.lbl_title.config(text=step_data["title"])

        self.block_how.config(text=step_data["how"])
        self.block_why.config(text=step_data["why"])
        self.block_when.config(text=step_data["when"])

        # Update visual progress bar width
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        if width <= 1:
            width = 730
        pct = (self.current_step + 1) / float(self.total_steps)
        self.progress_canvas.create_rectangle(0, 0, width * pct, 6, fill=step_data["color"], width=0)

        # Update button states
        self.btn_prev.config(state='normal' if self.current_step > 0 else 'disabled')
        if self.current_step == self.total_steps - 1:
            self.btn_next.config(text="🎓 Finish & Open App", bg="#10B981", fg="#000000")
        else:
            self.btn_next.config(text="Next Step ▶", bg=self.CYAN, fg="#000000")

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self._update_step_display()

    def _next_step(self):
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self._update_step_display()
        else:
            self._finish_tutorial()

    def _skip_tutorial(self):
        config.set_first_run_completed(True)
        if self.on_complete_callback:
            self.on_complete_callback()
        self.destroy()

    def _finish_tutorial(self):
        config.set_first_run_completed(True)
        if self.on_complete_callback:
            self.on_complete_callback()
        self.destroy()
