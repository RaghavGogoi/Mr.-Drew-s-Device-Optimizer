import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any, Callable, Optional
import config

# Comprehensive Database of All Features: HOW, WHY, and WHEN
TUTORIAL_STEPS: List[Dict[str, Any]] = [
    {
        "id": "welcome",
        "category": "🚀 GETTING STARTED",
        "title": "Welcome to Mr. Drew's Device & FPS Optimizer",
        "icon": "⚡",
        "color": "#00F0FF",
        "how": "Combines a native C++ engine, GPU shader management, real-time memory compaction, and process priority tuning into one fast suite.",
        "why": "Eliminates game micro-stutters, reclaims 2 to 5 GB physical RAM, lowers input lag, and prevents texture pop-in.",
        "when": "Run before starting gaming sessions (Fortnite, Valorant, Roblox, Unreal Engine), or run Smart Auto-Guard in the background.",
        "action_id": None,
        "action_label": None
    },
    {
        "id": "fps_booster",
        "category": "🎮 GAMING ENGINE",
        "title": "RUN FPS & GAME BOOSTER",
        "icon": "🎮",
        "color": "#F59E0B",
        "how": "Locks system timer resolution to 1.0ms, flushes GPU shader caches (Nvidia/AMD/DirectX), and elevates game process CPU priority to High.",
        "why": "Fixes frame drops, removes micro-stutters, and lowers input latency in competitive games.",
        "when": "Click right before launching your game or whenever you notice stutters during gameplay.",
        "action_id": "run_fps_booster",
        "action_label": "🧪 Try FPS Booster Now"
    },
    {
        "id": "asset_loader",
        "category": "🎮 GAMING ENGINE",
        "title": "Fast Asset Loader",
        "icon": "🚀",
        "color": "#10B981",
        "how": "Sets Disk I/O priority to High (ProcessIoPriorityHigh) for active game processes and protects loaded game assets from RAM eviction.",
        "why": "Accelerates map loading, texture streaming, and 3D asset rendering; stops texture pop-in.",
        "when": "Use when loading open-world games, map transitions, or heavy Roblox / Unreal Engine projects.",
        "action_id": "accelerate_asset_loading",
        "action_label": "🧪 Test Asset Loader"
    },
    {
        "id": "potato_mode",
        "category": "🥔 LOW-SPEC ENGINE",
        "title": "4GB Potato Mode",
        "icon": "🥔",
        "color": "#EAB308",
        "how": "Triggers aggressive memory compaction targeting 1.5 GB free RAM, drops inactive page caches, and terminates background bloatware.",
        "why": "Enables smooth gaming and app performance on budget/low-spec devices with 4GB to 8GB physical RAM without paging stutters.",
        "when": "Activate on low-end laptops or budget PCs before launching any game.",
        "action_id": "run_potato_mode",
        "action_label": "🧪 Test Potato Mode"
    },
    {
        "id": "ultimate_power",
        "category": "⚡ POWER ENGINE",
        "title": "Ultimate Power Mode",
        "icon": "⚡",
        "color": "#10B981",
        "how": "Forces Windows OS power scheme to High / Ultimate Performance, disabling CPU core parking and power throttling.",
        "why": "Ensures CPU cores run at peak clock speeds without sudden frequency drops during demanding scenes.",
        "when": "Enable when gaming, video editing, or rendering on desktop or plugged-in laptops.",
        "action_id": "enable_power_plan",
        "action_label": "🧪 Enable Ultimate Power"
    },
    {
        "id": "monster_optimizer",
        "category": "🧠 MEMORY ENGINE",
        "title": "RUN MONSTER OPTIMIZER",
        "icon": "🔥",
        "color": "#A855F7",
        "how": "Multi-stage deep RAM recovery: compacts background working sets via EmptyWorkingSet, flushes kernel standby page list, and sweeps temp memory.",
        "why": "Recovers the maximum possible physical memory (up to 3-6 GB RAM) in one click without closing critical system apps.",
        "when": "Use when overall RAM usage exceeds 80%, or before running memory-heavy applications.",
        "action_id": "run_monster_optimizer",
        "action_label": "🧪 Run Monster Optimizer"
    },
    {
        "id": "trim_ram",
        "category": "🧠 MEMORY ENGINE",
        "title": "Trim App RAM",
        "icon": "✂️",
        "color": "#00F0FF",
        "how": "Iterates through non-critical user applications and compacts their active working set memory into physical free RAM.",
        "why": "Instantly reclaims RAM held hostage by web browsers (Chrome, Edge) and background software (Discord, Spotify).",
        "when": "Use while multitasking when you want to free RAM without quitting open applications.",
        "action_id": "trim_working_sets",
        "action_label": "🧪 Trim App RAM Now"
    },
    {
        "id": "purge_standby",
        "category": "🧠 MEMORY ENGINE",
        "title": "Purge Standby RAM",
        "icon": "🛡️",
        "color": "#3B82F6",
        "how": "Calls C++ NtSetSystemInformation with SystemMemoryListInformation (or POSIX drop_caches on Linux/macOS) to clear cached standby list memory.",
        "why": "Fixes Windows Standby RAM bugs that cause game crashes and hitching when free RAM drops to zero.",
        "when": "Use when Standby cached memory is high and free memory is low.",
        "action_id": "purge_standby",
        "action_label": "🧪 Purge Standby RAM"
    },
    {
        "id": "clear_temp",
        "category": "🧹 CLEANING ENGINE",
        "title": "Clear Temp Files",
        "icon": "🧹",
        "color": "#EC4899",
        "how": "Recursively cleans %TEMP%, %SystemRoot%\\Temp, log caches, and leftover installer clutter while bypassing locked files safely.",
        "why": "Frees up gigabytes of SSD/HDD drive space and removes system clutter.",
        "when": "Run weekly or whenever drive space is tight.",
        "action_id": "clear_temp",
        "action_label": "🧪 Clear Temp Files"
    },
    {
        "id": "game_picker",
        "category": "🎯 PRIORITY TUNER",
        "title": "Boost Game Priority",
        "icon": "🎯",
        "color": "#F59E0B",
        "how": "Lets you pick your active game process and elevates its OS scheduling priority class to High Priority.",
        "why": "Guarantees that the CPU allocates maximum execution clock cycles to your game over background threads.",
        "when": "Use whenever playing competitive multiplayer games or resource-demanding titles.",
        "action_id": "open_game_picker",
        "action_label": "🧪 Select & Boost Game"
    },
    {
        "id": "shader_cleaner",
        "category": "🎨 GRAPHICS TUNER",
        "title": "Clean Shader Cache",
        "icon": "🧹",
        "color": "#00F0FF",
        "how": "Sweeps compiled DirectX, OpenGL, Vulkan, Nvidia (DXCache/GLCache), AMD (DxCache), and Intel GPU shader caches.",
        "why": "Fixes corrupted shader stuttering, visual artifacts, and frame drops caused by stale shader caches.",
        "when": "Run after updating graphics drivers, installing game updates, or experiencing graphical stutters.",
        "action_id": "clean_shader_cache",
        "action_label": "🧪 Clean Shader Cache"
    },
    {
        "id": "end_bloatware",
        "category": "🛡️ SECURITY & CLEANING",
        "title": "End Bloatware",
        "icon": "🚫",
        "color": "#EF4444",
        "how": "Safely terminates non-essential background bloatware (OneDrive, Widgets, Teams, Cortana) protected by safety whitelists.",
        "why": "Stops unwanted background telemetry, reduces background CPU usage, and saves memory.",
        "when": "Run on computer startup or before launching games.",
        "action_id": "kill_bloatware",
        "action_label": "🧪 Terminate Bloatware"
    },
    {
        "id": "top_procs",
        "category": "📊 SYSTEM ANALYTICS",
        "title": "Top RAM Apps",
        "icon": "📊",
        "color": "#10B981",
        "how": "Scans active processes, calculates physical RAM usage (RSS), and ranks top memory consumers in real-time.",
        "why": "Provides full visibility into what applications are consuming system resources.",
        "when": "Use to inspect system memory distribution or identify memory hogs.",
        "action_id": "view_top_processes",
        "action_label": "🧪 View Top RAM Apps"
    },
    {
        "id": "auto_guard",
        "category": "⚡ AUTOMATION ENGINE",
        "title": "Smart Auto-Guard (60s Loop)",
        "icon": "⚡",
        "color": "#A855F7",
        "how": "Background thread continuously monitors physical free RAM. If free memory falls below target threshold, automatically triggers standby list flush and memory compaction.",
        "why": "Provides automatic, set-and-forget 24/7 protection against memory leaks and RAM exhaustion stutters.",
        "when": "Turn on for long gaming sessions or background server operations.",
        "action_id": "toggle_auto_guard",
        "action_label": "🧪 Toggle Auto-Guard"
    }
]


class InteractiveTutorialModal(tk.Toplevel):
    """
    Modern, non-repetitive interactive step-by-step tutorial modal dialog.
    Allows quick step selection, live feature testing directly from the modal, and saving completion state.
    """
    def __init__(self, parent, on_complete_callback: Optional[Callable[[], None]] = None, action_callback: Optional[Callable[[str], None]] = None):
        super().__init__(parent)
        self.parent = parent
        self.on_complete_callback = on_complete_callback
        self.action_callback = action_callback
        self.current_step = 0
        self.total_steps = len(TUTORIAL_STEPS)

        self.title("🎓 INTERACTIVE TUTORIAL - MR. DREW'S DEVICE OPTIMIZER")
        self.geometry("820x640")
        self.minsize(740, 580)
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
        header = tk.Frame(self, bg=self.BG_MAIN, padx=20, pady=12)
        header.pack(fill='x', side='top')

        lbl_top = tk.Label(
            header,
            text="🎓 INTERACTIVE STEP-BY-STEP GUIDED TOUR",
            font=('Segoe UI', 11, 'bold'),
            fg=self.CYAN,
            bg=self.BG_MAIN
        )
        lbl_top.pack(side='left')

        # Dropdown Step Selector to prevent repetitive linear clicking
        jump_frame = tk.Frame(header, bg=self.BG_MAIN)
        jump_frame.pack(side='right')

        tk.Label(jump_frame, text="Jump to Topic:", font=('Segoe UI', 9), fg=self.TEXT_MUTED, bg=self.BG_MAIN).pack(side='left', padx=(0, 6))
        
        self.step_titles = [f"{i+1}. {step['title']}" for i, step in enumerate(TUTORIAL_STEPS)]
        self.step_combo = ttk.Combobox(jump_frame, values=self.step_titles, state="readonly", width=32, font=('Segoe UI', 9))
        self.step_combo.current(0)
        self.step_combo.bind("<<ComboboxSelected>>", self._on_combo_select)
        self.step_combo.pack(side='left')

        # Visual Progress Bar Canvas
        prog_frame = tk.Frame(self, bg=self.BG_MAIN, padx=20)
        prog_frame.pack(fill='x')

        self.progress_canvas = tk.Canvas(prog_frame, height=6, bg="#0B132B", highlightthickness=0)
        self.progress_canvas.pack(fill='x')

        # Main Card Content Container
        self.card_frame = tk.Frame(
            self,
            bg=self.BG_CARD,
            padx=24,
            pady=20,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        self.card_frame.pack(fill='both', expand=True, padx=20, pady=12)

        # Top Category & Title Row
        title_row = tk.Frame(self.card_frame, bg=self.BG_CARD)
        title_row.pack(fill='x')

        self.lbl_cat = tk.Label(
            title_row,
            text="CATEGORY",
            font=('Segoe UI', 9, 'bold'),
            fg=self.CYAN,
            bg=self.BG_CARD
        )
        self.lbl_cat.pack(anchor='w')

        self.lbl_title = tk.Label(
            title_row,
            text="Step Title",
            font=('Segoe UI', 16, 'bold'),
            fg=self.TEXT_PRIMARY,
            bg=self.BG_CARD,
            wraplength=700,
            justify='left'
        )
        self.lbl_title.pack(anchor='w', pady=(2, 10))

        # Three Detailed Blocks: HOW, WHY, WHEN
        self.block_how = self._create_info_block(self.card_frame, "🛠️ HOW IT WORKS (Technical Engine):", "#00F0FF")
        self.block_why = self._create_info_block(self.card_frame, "💡 WHY USE IT (Performance Benefit):", "#10B981")
        self.block_when = self._create_info_block(self.card_frame, "⏱️ WHEN TO USE IT (Best Scenario):", "#F59E0B")

        # Interactive "Try Button Now" Action Bar inside Tutorial Step Card
        self.action_bar = tk.Frame(self.card_frame, bg=self.BG_CARD, pady=8)
        self.action_bar.pack(fill='x')

        self.btn_try_action = tk.Button(
            self.action_bar,
            text="🧪 Try Feature Now",
            font=('Segoe UI', 9, 'bold'),
            fg="#000000",
            bg="#10B981",
            activebackground="#059669",
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=14,
            pady=6,
            command=self._execute_step_action
        )
        self.btn_try_action.pack(side='left')

        # Bottom Control Bar
        footer = tk.Frame(self, bg=self.BG_MAIN, padx=20, pady=12)
        footer.pack(fill='x', side='bottom')

        self.btn_skip = tk.Button(
            footer,
            text="⏭️ Skip Tutorial",
            font=('Segoe UI', 9, 'bold'),
            fg="#EF4444",
            bg="#1E293B",
            activebackground="#7F1D1D",
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=14,
            pady=6,
            command=self._skip_tutorial
        )
        self.btn_skip.pack(side='left')

        right_btns = tk.Frame(footer, bg=self.BG_MAIN)
        right_btns.pack(side='right')

        self.btn_prev = tk.Button(
            right_btns,
            text="◀ Previous",
            font=('Segoe UI', 9, 'bold'),
            fg=self.TEXT_PRIMARY,
            bg="#1E293B",
            activebackground="#334155",
            activeforeground=self.TEXT_PRIMARY,
            relief='flat',
            cursor='hand2',
            padx=14,
            pady=6,
            command=self._prev_step
        )
        self.btn_prev.pack(side='left', padx=(0, 8))

        self.btn_next = tk.Button(
            right_btns,
            text="Next Step ▶",
            font=('Segoe UI', 9, 'bold'),
            fg="#000000",
            bg=self.CYAN,
            activebackground="#0284C7",
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=16,
            pady=6,
            command=self._next_step
        )
        self.btn_next.pack(side='left')

    def _create_info_block(self, parent, header_text, accent_color):
        frame = tk.Frame(
            parent,
            bg=self.BG_INNER,
            padx=14,
            pady=8,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        frame.pack(fill='x', pady=4)

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
            wraplength=720,
            justify='left'
        )
        body.pack(anchor='w', pady=(2, 0))

        return body

    def _update_step_display(self):
        step_data = TUTORIAL_STEPS[self.current_step]

        self.step_combo.current(self.current_step)
        self.lbl_cat.config(text=f"STEP {self.current_step + 1} OF {self.total_steps}  •  {step_data['category']}", fg=step_data["color"])
        self.lbl_title.config(text=f"{step_data['icon']} {step_data['title']}")

        self.block_how.config(text=step_data["how"])
        self.block_why.config(text=step_data["why"])
        self.block_when.config(text=step_data["when"])

        # Update Interactive Action Button
        if step_data.get("action_id") and step_data.get("action_label"):
            self.btn_try_action.config(text=step_data["action_label"], state='normal')
            self.btn_try_action.pack(side='left')
        else:
            self.btn_try_action.pack_forget()

        # Update visual progress bar width
        self.progress_canvas.delete("all")
        width = self.progress_canvas.winfo_width()
        if width <= 1:
            width = 780
        pct = (self.current_step + 1) / float(self.total_steps)
        self.progress_canvas.create_rectangle(0, 0, width * pct, 6, fill=step_data["color"], width=0)

        # Update button states
        self.btn_prev.config(state='normal' if self.current_step > 0 else 'disabled')
        if self.current_step == self.total_steps - 1:
            self.btn_next.config(text="🎓 Finish & Open App", bg="#10B981", fg="#000000")
        else:
            self.btn_next.config(text="Next Step ▶", bg=self.CYAN, fg="#000000")

    def _on_combo_select(self, event):
        idx = self.step_combo.current()
        if 0 <= idx < self.total_steps:
            self.current_step = idx
            self._update_step_display()

    def _execute_step_action(self):
        step_data = TUTORIAL_STEPS[self.current_step]
        action_id = step_data.get("action_id")
        if action_id and self.action_callback:
            self.action_callback(action_id)

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
