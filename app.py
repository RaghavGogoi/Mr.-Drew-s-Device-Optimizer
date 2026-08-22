import sys
import os
import time
import threading
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Ensure working directory is set to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import config
from optimizer_core import OptimizerCore
from tutorial_manager import InteractiveTutorialModal, TUTORIAL_STEPS


class DeviceOptimizerApp(tk.Tk):
    """
    Modern Obsidian Glassmorphism Desktop Application for Mr. Drew's Device & FPS Optimizer.
    Features Sidebar Page Navigation, Interactive First-Time Tutorial, and C++ Core integration.
    """
    def __init__(self):
        super().__init__()

        self.core = OptimizerCore()
        self.specs = self.core.get_system_specs()
        self.hw = self.core.get_hardware_details()
        self.auto_guard_active = False
        self.auto_guard_thread = None
        self.action_in_progress = False

        # Configure Root Window
        self.title("⚡ MR. DREW'S DEVICE & FPS OPTIMIZER - OBSIDIAN SUITE")
        self.geometry("1120x840")
        self.minsize(980, 720)

        # Apply Modern Black, Glass & Glint Palette
        self.COLOR_BG = "#030712"            # Pitch Black / Deep Obsidian
        self.COLOR_SIDEBAR = "#070D1B"       # Dark Sidebar Navigation
        self.COLOR_CARD_BG = "#0F172A"       # Deep Translucent Glass
        self.COLOR_CARD_SURFACE = "#1E293B"  # Card Surface
        self.COLOR_BORDER = "#334155"        # Subtle Frosted Border
        self.COLOR_TEXT = "#F8FAFC"          # Crisp White Text
        self.COLOR_MUTED = "#94A3B8"         # Muted Slate
        
        # Glint Accent Colors
        self.COLOR_CYAN = "#00F0FF"          # Cyber Cyan Glint
        self.COLOR_CYAN_BG = "#0284C7"
        self.COLOR_PURPLE = "#A855F7"        # Electric Violet Glint
        self.COLOR_PURPLE_BG = "#7C3AED"
        self.COLOR_GREEN = "#10B981"         # Emerald Matrix Pulse
        self.COLOR_GREEN_BG = "#059669"
        self.COLOR_AMBER = "#F59E0B"         # Amber Gaming Flame
        self.COLOR_AMBER_BG = "#D97706"
        self.COLOR_RED = "#EF4444"           # Alert Red

        self.configure(bg=self.COLOR_BG)

        # Style Configuration
        self._init_styles()

        # Build Main UI Shell
        self._create_header()
        
        # Body Container (Sidebar + Page View)
        self.body_frame = tk.Frame(self, bg=self.COLOR_BG)
        self.body_frame.pack(fill='both', expand=True)

        self._create_sidebar()

        # Page Container
        self.page_container = tk.Frame(self.body_frame, bg=self.COLOR_BG, padx=16, pady=8)
        self.page_container.pack(side='right', fill='both', expand=True)

        self.pages = {}
        self._build_pages()
        self._show_page("dashboard")

        # Bottom Console Log
        self._create_console_log()

        # Check First-Run Status to Trigger Interactive Tutorial
        if config.is_first_run():
            self.after(600, self._open_interactive_tutorial)

        # Stats Update Loop
        self._refresh_stats_loop()

    def _init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TFrame', background=self.COLOR_BG)
        self.style.configure('Treeview',
            background=self.COLOR_CARD_BG,
            foreground=self.COLOR_TEXT,
            fieldbackground=self.COLOR_CARD_BG,
            rowheight=26,
            font=('Segoe UI', 9)
        )
        self.style.configure('Treeview.Heading',
            background=self.COLOR_CARD_SURFACE,
            foreground=self.COLOR_CYAN,
            font=('Segoe UI', 9, 'bold')
        )
        self.style.map('Treeview', background=[('selected', self.COLOR_CYAN_BG)])

    def _create_header(self):
        header_frame = tk.Frame(self, bg=self.COLOR_BG, pady=10, padx=20)
        header_frame.pack(fill='x', side='top')

        left_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        left_frame.pack(side='left')

        title_lbl = tk.Label(
            left_frame,
            text="⚡ MR. DREW'S DEVICE & FPS OPTIMIZER",
            font=('Segoe UI', 17, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_BG
        )
        title_lbl.pack(anchor='w')

        cpp_status = "⚡ C++ ENGINE ACTIVE" if self.hw.get("cpp_engine_active") else "🐍 PYTHON ENGINE"
        subtitle_text = f"{cpp_status} | {self.hw['device_profile']} | GPU: {self.hw['gpu_vendor']}"
        subtitle_lbl = tk.Label(
            left_frame,
            text=subtitle_text,
            font=('Segoe UI', 8),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        )
        subtitle_lbl.pack(anchor='w', pady=(2, 0))

        # Right side badges & Tutorial button
        right_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        right_frame.pack(side='right')

        # Interactive Tutorial Re-access Button
        self.btn_tutorial_header = tk.Button(
            right_frame,
            text="🎓 Interactive Tutorial",
            font=('Segoe UI', 9, 'bold'),
            fg="#FFFFFF",
            bg=self.COLOR_PURPLE,
            activebackground=self.COLOR_PURPLE_BG,
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=10,
            pady=4,
            command=self._open_interactive_tutorial,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        self.btn_tutorial_header.pack(side='left', padx=4)

        os_badge_text = f"💻 {self.specs['os_name']} ({self.hw['cpu_cores_logical']} Cores)"
        os_badge = tk.Label(
            right_frame,
            text=os_badge_text,
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_CYAN,
            bg=self.COLOR_CARD_SURFACE,
            padx=10,
            pady=4,
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        os_badge.pack(side='left', padx=4)

        admin_color = self.COLOR_GREEN if self.specs['is_admin'] else self.COLOR_AMBER
        admin_text = "🛡️ ADMIN ACTIVE" if self.specs['is_admin'] else "⚠️ USER MODE (Elevate)"
        self.admin_badge = tk.Button(
            right_frame,
            text=admin_text,
            font=('Segoe UI', 9, 'bold'),
            fg=admin_color,
            bg=self.COLOR_CARD_SURFACE,
            activebackground=self.COLOR_CARD_BG,
            activeforeground=admin_color,
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
            cursor='hand2',
            padx=10,
            pady=4,
            command=self._on_click_elevate
        )
        self.admin_badge.pack(side='left', padx=4)

    def _create_sidebar(self):
        sidebar = tk.Frame(self.body_frame, bg=self.COLOR_SIDEBAR, width=210, padx=8, pady=12)
        sidebar.pack(side='left', fill='y')

        nav_items = [
            ("dashboard", "🏠  Dashboard", "Overview & Gauge"),
            ("fps_gaming", "🎮  FPS & Gaming", "Stutter & Priority"),
            ("ram_memory", "🧠  RAM & Memory", "Recovery & Guard"),
            ("system_tools", "🧹  System Tools", "Cleaner & Apps"),
            ("tutorial_hub", "🎓  Tutorial & Guide", "How, Why, When"),
            ("settings", "⚙️  Settings & Specs", "App Configuration")
        ]

        self.sidebar_buttons = {}
        for page_id, label, subtext in nav_items:
            btn_frame = tk.Frame(sidebar, bg=self.COLOR_SIDEBAR, pady=4)
            btn_frame.pack(fill='x')

            btn = tk.Button(
                btn_frame,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                fg=self.COLOR_MUTED,
                bg=self.COLOR_SIDEBAR,
                activebackground=self.COLOR_CARD_SURFACE,
                activeforeground=self.COLOR_CYAN,
                relief='flat',
                anchor='w',
                padx=12,
                pady=6,
                cursor='hand2',
                command=lambda pid=page_id: self._show_page(pid)
            )
            btn.pack(fill='x')
            self.sidebar_buttons[page_id] = btn

    def _show_page(self, page_id: str):
        for pid, btn in self.sidebar_buttons.items():
            if pid == page_id:
                btn.config(bg=self.COLOR_CARD_SURFACE, fg=self.COLOR_CYAN)
            else:
                btn.config(bg=self.COLOR_SIDEBAR, fg=self.COLOR_MUTED)

        for pid, frame in self.pages.items():
            if pid == page_id:
                frame.pack(fill='both', expand=True)
            else:
                frame.pack_forget()

    def _make_glint_button(self, parent, text, bg, fg, hover_bg, cmd, font=('Segoe UI', 9, 'bold'), pady=6, padx=10):
        btn = tk.Button(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=bg,
            activebackground=hover_bg,
            activeforeground=fg,
            relief='flat',
            cursor='hand2',
            padx=padx,
            pady=pady,
            command=cmd,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )

        def on_enter(e):
            if str(btn['state']) != 'disabled':
                btn.config(bg=hover_bg, highlightbackground=fg)

        def on_leave(e):
            if str(btn['state']) != 'disabled':
                btn.config(bg=bg, highlightbackground=self.COLOR_BORDER)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn

    def _build_pages(self):
        # 1. Dashboard Page
        page_dash = tk.Frame(self.page_container, bg=self.COLOR_BG)
        self.pages["dashboard"] = page_dash
        self._build_dashboard_page(page_dash)

        # 2. FPS & Gaming Page
        page_fps = tk.Frame(self.page_container, bg=self.COLOR_BG)
        self.pages["fps_gaming"] = page_fps
        self._build_fps_gaming_page(page_fps)

        # 3. RAM & Memory Page
        page_ram = tk.Frame(self.page_container, bg=self.COLOR_BG)
        self.pages["ram_memory"] = page_ram
        self._build_ram_memory_page(page_ram)

        # 4. System Tools Page
        page_tools = tk.Frame(self.page_container, bg=self.COLOR_BG)
        self.pages["system_tools"] = page_tools
        self._build_system_tools_page(page_tools)

        # 5. Tutorial Hub Page
        page_tut = tk.Frame(self.page_container, bg=self.COLOR_BG)
        self.pages["tutorial_hub"] = page_tut
        self._build_tutorial_hub_page(page_tut)

        # 6. Settings Page
        page_set = tk.Frame(self.page_container, bg=self.COLOR_BG)
        self.pages["settings"] = page_set
        self._build_settings_page(page_set)

    def _build_dashboard_page(self, parent):
        # Top Metrics Cards Grid
        cards_frame = tk.Frame(parent, bg=self.COLOR_BG)
        cards_frame.pack(fill='x', pady=(0, 10))
        cards_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='card')

        self.card_total_ram = self._build_card(cards_frame, 0, "TOTAL PHYSICAL RAM", f"{self.specs['total_ram_gb']} GB", self.COLOR_CYAN)
        self.card_free_ram = self._build_card(cards_frame, 1, "CURRENT FREE RAM", f"{self.specs['avail_ram_gb']} GB", self.COLOR_GREEN)
        self.card_target_ram = self._build_card(cards_frame, 2, "SMART TARGET FREE", f"≥ {self.specs['target_free_gb']} GB", self.COLOR_PURPLE)
        self.card_cpu = self._build_card(cards_frame, 3, "CPU UTILIZATION", f"{self.specs['cpu_percent']}%", self.COLOR_AMBER)

        # Memory Progress Gauge
        prog_card = tk.Frame(parent, bg=self.COLOR_CARD_SURFACE, padx=16, pady=12, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        prog_card.pack(fill='x', pady=6)

        lbl_row = tk.Frame(prog_card, bg=self.COLOR_CARD_SURFACE)
        lbl_row.pack(fill='x')

        tk.Label(lbl_row, text="Real-Time Physical Memory Allocation Gauge", font=('Segoe UI', 10, 'bold'), fg=self.COLOR_TEXT, bg=self.COLOR_CARD_SURFACE).pack(side='left')
        self.ram_percent_lbl = tk.Label(lbl_row, text="0%", font=('Segoe UI', 10, 'bold'), fg=self.COLOR_CYAN, bg=self.COLOR_CARD_SURFACE)
        self.ram_percent_lbl.pack(side='right')

        self.progress_canvas = tk.Canvas(prog_card, height=16, bg="#0B132B", highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        self.progress_canvas.pack(fill='x', pady=(6, 0))

        # Quick Action Buttons Panel
        actions_frame = tk.Frame(parent, bg=self.COLOR_BG, pady=8)
        actions_frame.pack(fill='x')

        btn_row = tk.Frame(actions_frame, bg=self.COLOR_BG)
        btn_row.pack(fill='x')

        self._make_glint_button(
            btn_row, "🎮 RUN FPS BOOSTER", self.COLOR_AMBER, "#000000", self.COLOR_AMBER_BG, self._on_run_fps_booster, font=('Segoe UI', 10, 'bold'), pady=8, padx=16
        ).pack(side='left', padx=(0, 6), fill='x', expand=True)

        self._make_glint_button(
            btn_row, "🔥 RUN MONSTER OPTIMIZER", self.COLOR_PURPLE, "#FFFFFF", self.COLOR_PURPLE_BG, self._on_run_monster_optimizer, font=('Segoe UI', 10, 'bold'), pady=8, padx=16
        ).pack(side='left', padx=(0, 6), fill='x', expand=True)

        self._make_glint_button(
            btn_row, "🥔 4GB Potato Mode", self.COLOR_CARD_SURFACE, self.COLOR_TEXT, "#334155", self._on_run_potato_mode, font=('Segoe UI', 10, 'bold'), pady=8, padx=14
        ).pack(side='left', padx=(0, 6), fill='x', expand=True)

        self._make_glint_button(
            btn_row, "🔄 Refresh Stats", self.COLOR_CARD_SURFACE, self.COLOR_CYAN, "#334155", self._on_manual_refresh, font=('Segoe UI', 10, 'bold'), pady=8, padx=14
        ).pack(side='left', fill='x', expand=True)

    def _build_card(self, parent, col, title, value, accent_color):
        card = tk.Frame(parent, bg=self.COLOR_CARD_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        card.grid(row=0, column=col, padx=4, sticky='nsew')

        lbl_title = tk.Label(card, text=title, font=('Segoe UI', 8, 'bold'), fg=self.COLOR_MUTED, bg=self.COLOR_CARD_SURFACE)
        lbl_title.pack(anchor='w')

        lbl_val = tk.Label(card, text=value, font=('Segoe UI', 15, 'bold'), fg=accent_color, bg=self.COLOR_CARD_SURFACE)
        lbl_val.pack(anchor='w', pady=(3, 0))

        return lbl_val

    def _build_fps_gaming_page(self, parent):
        tk.Label(parent, text="🎮 High-FPS & Gaming Latency Engine", font=('Segoe UI', 14, 'bold'), fg=self.COLOR_CYAN, bg=self.COLOR_BG).pack(anchor='w', pady=(0, 10))

        grid = tk.Frame(parent, bg=self.COLOR_BG)
        grid.pack(fill='both', expand=True)
        grid.columnconfigure((0, 1), weight=1)

        # Card 1: FPS & Game Booster
        c1 = self._build_feature_card(grid, 0, 0, "🎮 RUN FPS & GAME BOOSTER", "Locks 1.0ms timer, cleans GPU shader cache, and boosts game CPU priority.", self.COLOR_AMBER, "RUN BOOSTER", self._on_run_fps_booster)
        
        # Card 2: Fast Asset Loader
        c2 = self._build_feature_card(grid, 0, 1, "🚀 Fast Asset Loader", "Elevates Disk I/O priority for fast map/texture read speed.", self.COLOR_GREEN, "ACCELERATE READS", self._on_accelerate_asset_loading)

        # Card 3: 4GB Potato Mode
        c3 = self._build_feature_card(grid, 1, 0, "🥔 4GB Potato Mode", "Aggressive low-RAM preset for budget PCs with 4GB physical RAM.", self.COLOR_TEXT, "ENABLE POTATO PRESET", self._on_run_potato_mode)

        # Card 4: Ultimate Power
        c4 = self._build_feature_card(grid, 1, 1, "⚡ Ultimate Power Mode", "Forces OS power plan into maximum clock speed state.", self.COLOR_GREEN, "FORCE ULTIMATE POWER", self._on_enable_power_plan)

        # Card 5: Game Priority
        c5 = self._build_feature_card(grid, 2, 0, "🎯 Boost Game Priority", "Set high scheduling priority for your active game executable.", self.COLOR_AMBER, "SELECT & BOOST GAME", self._on_open_game_picker)

        # Card 6: GPU Shader Cache
        c6 = self._build_feature_card(grid, 2, 1, "🧹 Clean Shader Cache", "Flushes DirectX, OpenGL, Vulkan, Nvidia & AMD shader caches.", self.COLOR_CYAN, "CLEAN SHADERS", self._on_clean_shader_cache)

    def _build_ram_memory_page(self, parent):
        tk.Label(parent, text="🧠 RAM & Memory Management Engine", font=('Segoe UI', 14, 'bold'), fg=self.COLOR_PURPLE, bg=self.COLOR_BG).pack(anchor='w', pady=(0, 10))

        grid = tk.Frame(parent, bg=self.COLOR_BG)
        grid.pack(fill='both', expand=True)
        grid.columnconfigure((0, 1), weight=1)

        c1 = self._build_feature_card(grid, 0, 0, "🔥 MONSTER OPTIMIZER", "Multi-stage RAM recovery: compacts working sets & purges standby RAM.", self.COLOR_PURPLE, "RUN MONSTER PURGE", self._on_run_monster_optimizer)
        c2 = self._build_feature_card(grid, 0, 1, "✂️ Trim App RAM", "Compacts working set memory of running applications into free RAM.", self.COLOR_CYAN, "TRIM WORKING SETS", self._on_trim_working_sets)
        c3 = self._build_feature_card(grid, 1, 0, "🛡️ Purge Standby RAM", "Calls NT Kernel to flush Standby cached page list memory.", self.COLOR_TEXT, "PURGE STANDBY LIST", self._on_purge_standby)
        c4 = self._build_feature_card(grid, 1, 1, "⚡ Smart Auto-Guard (60s Loop)", "Continuous background daemon checking memory threshold.", self.COLOR_GREEN, "TOGGLE AUTO-GUARD", self._toggle_auto_guard)

    def _build_system_tools_page(self, parent):
        tk.Label(parent, text="🧹 System Tools & Process Manager", font=('Segoe UI', 14, 'bold'), fg=self.COLOR_GREEN, bg=self.COLOR_BG).pack(anchor='w', pady=(0, 10))

        top_bar = tk.Frame(parent, bg=self.COLOR_BG)
        top_bar.pack(fill='x', pady=(0, 8))

        self._make_glint_button(top_bar, "🧹 Clear Temp Files", self.COLOR_CARD_SURFACE, self.COLOR_TEXT, "#334155", self._on_clear_temp, pady=6, padx=12).pack(side='left', padx=(0, 6))
        self._make_glint_button(top_bar, "🚫 End Bloatware", self.COLOR_CARD_SURFACE, self.COLOR_RED, "#334155", self._on_kill_bloatware, pady=6, padx=12).pack(side='left', padx=(0, 6))
        self._make_glint_button(top_bar, "📊 Refresh Top RAM Apps", self.COLOR_CARD_SURFACE, self.COLOR_CYAN, "#334155", self._on_view_top_processes, pady=6, padx=12).pack(side='left')

        # Treeview for Top Processes
        tree_frame = tk.Frame(parent, bg=self.COLOR_CARD_BG, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        tree_frame.pack(fill='both', expand=True)

        self.proc_tree = ttk.Treeview(tree_frame, columns=("pid", "name", "mem_mb"), show='headings')
        self.proc_tree.heading("pid", text="PID")
        self.proc_tree.heading("name", text="Application / Process Name")
        self.proc_tree.heading("mem_mb", text="Physical RAM (MB)")

        self.proc_tree.column("pid", width=100, anchor='center')
        self.proc_tree.column("name", width=380, anchor='w')
        self.proc_tree.column("mem_mb", width=160, anchor='e')

        self.proc_tree.pack(side='left', fill='both', expand=True)
        sb = ttk.Scrollbar(tree_frame, orient='vertical', command=self.proc_tree.yview)
        self.proc_tree.configure(yscroll=sb.set)
        sb.pack(side='right', fill='y')

    def _build_tutorial_hub_page(self, parent):
        tk.Label(parent, text="🎓 Interactive Tutorial & Button Purpose Reference", font=('Segoe UI', 14, 'bold'), fg=self.COLOR_CYAN, bg=self.COLOR_BG).pack(anchor='w', pady=(0, 6))

        hdr_card = tk.Frame(parent, bg=self.COLOR_CARD_SURFACE, padx=16, pady=10, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        hdr_card.pack(fill='x', pady=(0, 10))

        tk.Label(hdr_card, text="Click below to launch the step-by-step interactive tour, or explore every button purpose below:", font=('Segoe UI', 9), fg=self.COLOR_TEXT, bg=self.COLOR_CARD_SURFACE).pack(side='left')
        
        self._make_glint_button(hdr_card, "▶ Launch Step-by-Step Tour", self.COLOR_PURPLE, "#FFFFFF", self.COLOR_PURPLE_BG, self._open_interactive_tutorial, font=('Segoe UI', 9, 'bold'), pady=4, padx=12).pack(side='right')

        # Scrollable list of feature definitions
        tut_canvas_frame = tk.Frame(parent, bg=self.COLOR_BG)
        tut_canvas_frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(tut_canvas_frame, bg=self.COLOR_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(tut_canvas_frame, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas, bg=self.COLOR_BG)

        scroll_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for step in TUTORIAL_STEPS:
            card = tk.Frame(scroll_content, bg=self.COLOR_CARD_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
            card.pack(fill='x', pady=4)

            lbl_t = tk.Label(card, text=f"{step['icon']} {step['title']} [{step['category']}]", font=('Segoe UI', 10, 'bold'), fg=step['color'], bg=self.COLOR_CARD_SURFACE)
            lbl_t.pack(anchor='w')

            tk.Label(card, text=f"🛠️ HOW: {step['how']}", font=('Segoe UI', 9), fg=self.COLOR_TEXT, bg=self.COLOR_CARD_SURFACE, wraplength=700, justify='left').pack(anchor='w', pady=(2, 0))
            tk.Label(card, text=f"💡 WHY: {step['why']}", font=('Segoe UI', 9), fg=self.COLOR_GREEN, bg=self.COLOR_CARD_SURFACE, wraplength=700, justify='left').pack(anchor='w', pady=(1, 0))
            tk.Label(card, text=f"⏱️ WHEN: {step['when']}", font=('Segoe UI', 9), fg=self.COLOR_AMBER, bg=self.COLOR_CARD_SURFACE, wraplength=700, justify='left').pack(anchor='w', pady=(1, 0))

    def _build_settings_page(self, parent):
        tk.Label(parent, text="⚙️ Settings & System Specifications", font=('Segoe UI', 14, 'bold'), fg=self.COLOR_MUTED, bg=self.COLOR_BG).pack(anchor='w', pady=(0, 10))

        card = tk.Frame(parent, bg=self.COLOR_CARD_SURFACE, padx=16, pady=16, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        card.pack(fill='x', pady=6)

        tk.Label(card, text="🎓 Interactive Tutorial State Controls", font=('Segoe UI', 11, 'bold'), fg=self.COLOR_CYAN, bg=self.COLOR_CARD_SURFACE).pack(anchor='w')
        tk.Label(card, text="Reset the first-run tutorial state so the interactive walkthrough plays automatically next time the app opens:", font=('Segoe UI', 9), fg=self.COLOR_MUTED, bg=self.COLOR_CARD_SURFACE).pack(anchor='w', pady=(2, 8))

        self._make_glint_button(card, "🔄 Reset First-Run Tutorial State", self.COLOR_PURPLE, "#FFFFFF", self.COLOR_PURPLE_BG, self._on_reset_tutorial, pady=6, padx=12).pack(anchor='w')

        # Specs Card
        specs_card = tk.Frame(parent, bg=self.COLOR_CARD_SURFACE, padx=16, pady=16, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        specs_card.pack(fill='x', pady=12)

        tk.Label(specs_card, text="💻 Detected Hardware & Operating System", font=('Segoe UI', 11, 'bold'), fg=self.COLOR_GREEN, bg=self.COLOR_CARD_SURFACE).pack(anchor='w')
        
        info_lines = [
            f"• Operating System: {self.specs['os_name']} {self.specs['os_release']} ({self.specs['os_arch']})",
            f"• CPU Cores: {self.hw['cpu_cores_physical']} Physical / {self.hw['cpu_cores_logical']} Logical",
            f"• GPU Vendor: {self.hw['gpu_vendor']}",
            f"• Hardware Device Profile: {self.hw['device_profile']}",
            f"• Native C++ Engine: {'Active (' + os.path.basename(self.core.cpp_exe_path) + ')' if self.core.cpp_exe_path else 'Not compiled (Using Python Core)'}",
            f"• Total Physical Memory: {self.specs['total_ram_gb']} GB",
            f"• Smart Target Free RAM: {self.specs['target_free_gb']} GB"
        ]

        for line in info_lines:
            tk.Label(specs_card, text=line, font=('Segoe UI', 9), fg=self.COLOR_TEXT, bg=self.COLOR_CARD_SURFACE).pack(anchor='w', pady=2)

    def _build_feature_card(self, parent, row, col, title, desc, accent_color, btn_text, cmd):
        card = tk.Frame(parent, bg=self.COLOR_CARD_SURFACE, padx=16, pady=14, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')

        lbl_t = tk.Label(card, text=title, font=('Segoe UI', 11, 'bold'), fg=accent_color, bg=self.COLOR_CARD_SURFACE)
        lbl_t.pack(anchor='w')

        lbl_d = tk.Label(card, text=desc, font=('Segoe UI', 9), fg=self.COLOR_MUTED, bg=self.COLOR_CARD_SURFACE, wraplength=340, justify='left')
        lbl_d.pack(anchor='w', pady=(4, 10))

        btn = self._make_glint_button(card, btn_text, self.COLOR_CARD_BG, accent_color, "#334155", cmd, font=('Segoe UI', 9, 'bold'), pady=6, padx=12)
        btn.pack(anchor='w')

        return card

    def _create_console_log(self):
        console_frame = tk.Frame(self, bg=self.COLOR_BG, padx=16, pady=4)
        console_frame.pack(fill='x', side='bottom')

        header_bar = tk.Frame(console_frame, bg=self.COLOR_BG)
        header_bar.pack(fill='x', pady=(0, 2))

        lbl_console = tk.Label(
            header_bar,
            text="Real-Time Optimizer Console & FPS Performance Log",
            font=('Segoe UI', 8, 'bold'),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        )
        lbl_console.pack(side='left')

        btn_copy = self._make_glint_button(
            header_bar, "📋 Copy Log", self.COLOR_CARD_SURFACE, self.COLOR_TEXT, "#1E293B", self._on_copy_log, font=('Segoe UI', 8, 'bold'), pady=1, padx=6
        )
        btn_copy.pack(side='right', padx=(4, 0))

        btn_clear = self._make_glint_button(
            header_bar, "🗑️ Clear", self.COLOR_CARD_SURFACE, self.COLOR_MUTED, "#1E293B", self._on_clear_console, font=('Segoe UI', 8, 'bold'), pady=1, padx=6
        )
        btn_clear.pack(side='right')

        self.log_text = scrolledtext.ScrolledText(
            console_frame,
            height=4,
            bg="#020617",
            fg="#10B981",
            font=('Consolas', 9),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        self.log_text.pack(fill='x')

        self._log("System & FPS Engine initialized [OBSIDIAN GLASS SUITE].")
        self._log(f"Detected OS: {self.specs['os_name']} {self.specs['os_release']} ({self.specs['os_arch']})")
        if self.hw.get("cpp_engine_active"):
            self._log(f"C++ Native Flusher Engine Active: {os.path.basename(self.core.cpp_exe_path)}")

    def _open_interactive_tutorial(self):
        """Launches the step-by-step interactive tutorial modal dialog."""
        InteractiveTutorialModal(self, on_complete_callback=lambda: self._log("Tutorial completed! All features unlocked."))

    def _on_reset_tutorial(self):
        config.reset_first_run()
        self._log("[TUTORIAL CONFIG] First-run tutorial flag reset! Launching tutorial modal...")
        messagebox.showinfo("Tutorial Reset", "First-run tutorial flag has been reset.\n\nThe interactive tutorial will play now!")
        self._open_interactive_tutorial()

    def _log(self, message: str):
        timestamp = time.strftime("[%H:%M:%S] ")
        full_msg = timestamp + message + "\n"
        self.after(0, self._append_log, full_msg)

    def _append_log(self, full_msg: str):
        self.log_text.insert(tk.END, full_msg)
        self.log_text.see(tk.END)

    def _safe_info(self, title: str, message: str):
        self.after(0, messagebox.showinfo, title, message)

    def _refresh_stats_loop(self):
        def update():
            try:
                self.specs = self.core.get_system_specs()
                self.card_free_ram.config(text=f"{self.specs['avail_ram_gb']} GB")
                self.card_cpu.config(text=f"{self.specs['cpu_percent']}%")

                pct = self.specs['percent_used']
                self.ram_percent_lbl.config(text=f"{pct}% RAM Used ({self.specs['used_ram_gb']} GB / {self.specs['total_ram_gb']} GB)")

                self.progress_canvas.delete("all")
                width = self.progress_canvas.winfo_width()
                height = self.progress_canvas.winfo_height()
                if width > 1:
                    fill_width = (pct / 100.0) * width
                    bar_color = self.COLOR_GREEN if self.specs['avail_ram_gb'] >= self.specs['target_free_gb'] else self.COLOR_AMBER
                    self.progress_canvas.create_rectangle(0, 0, fill_width, height, fill=bar_color, width=0)
            except Exception:
                pass
            self.after(2000, update)

        self.after(500, update)

    def _on_manual_refresh(self):
        self.specs = self.core.get_system_specs()
        self.hw = self.core.get_hardware_details()
        self.card_total_ram.config(text=f"{self.specs['total_ram_gb']} GB")
        self.card_free_ram.config(text=f"{self.specs['avail_ram_gb']} GB")
        self.card_target_ram.config(text=f"≥ {self.specs['target_free_gb']} GB")
        self.card_cpu.config(text=f"{self.specs['cpu_percent']}%")
        self._log(f"[REFRESH] Free RAM: {self.specs['avail_ram_gb']} GB / Total: {self.specs['total_ram_gb']} GB")

    def _on_click_elevate(self):
        if not self.specs['is_admin']:
            self.core.relaunch_as_admin()

    def _on_run_fps_booster(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True

        def worker():
            try:
                self._log("=========================================")
                self._log("🎮 STARTING FPS & GAME BOOSTER ENGINE...")
                res = self.core.run_fps_booster()
                for line in res['logs']:
                    self._log(line)
                self._log("=========================================")
                self._safe_info("FPS Booster Active", f"FPS Optimization Complete!\n\nReclaimed {res['reclaimed_gb']} GB RAM.\n1ms timer locked & GPU shader cache flushed!")
            finally:
                self.action_in_progress = False

        threading.Thread(target=worker, daemon=True).start()

    def _on_accelerate_asset_loading(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True

        def worker():
            try:
                self._log("=========================================")
                self._log("🚀 ACCELERATING GAME ASSET READ & LOAD SPEED...")
                ok, logs = self.core.accelerate_game_asset_loading()
                for line in logs:
                    self._log(line)
                self._log("=========================================")
                self._safe_info("Asset Acceleration", "Game Asset Load Speed Boosted!\n\nHigh Disk I/O Priority & CPU Priority assigned to active game.")
            finally:
                self.action_in_progress = False

        threading.Thread(target=worker, daemon=True).start()

    def _on_run_potato_mode(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True

        def worker():
            try:
                self._log("=========================================")
                self._log("🥔 STARTING 4GB POTATO DEVICE OPTIMIZER...")
                res = self.core.run_potato_device_optimizer()
                for line in res['logs']:
                    self._log(line)
                self._log("=========================================")
                self._safe_info("Potato Mode Active", f"4GB Potato Preset Complete!\n\nReclaimed {res['reclaimed_gb']} GB RAM.")
            finally:
                self.action_in_progress = False

        threading.Thread(target=worker, daemon=True).start()

    def _on_enable_power_plan(self):
        ok, msg = self.core.enable_high_performance_power_plan()
        self._log(f"[POWER PLAN] {msg}")
        if ok:
            messagebox.showinfo("Power Scheme", msg)

    def _on_run_monster_optimizer(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True

        def worker():
            try:
                self._log("=========================================")
                self._log("🔥 STARTING MONSTER OPTIMIZER MODE...")
                res = self.core.run_monster_optimization()
                for line in res['logs']:
                    self._log(line)
                self._log("=========================================")
                self._safe_info("Monster Optimization Complete", f"Reclaimed {res['reclaimed_gb']} GB RAM!\n\nCompacted working sets and purged standby memory.")
            finally:
                self.action_in_progress = False

        threading.Thread(target=worker, daemon=True).start()

    def _on_trim_working_sets(self):
        proc_total, proc_trimmed = self.core.trim_process_working_sets()
        self._log(f"[TRIM RAM] Compacted RAM working sets for {proc_trimmed}/{proc_total} active processes.")

    def _on_purge_standby(self):
        ok, msg = self.core.flush_standby_list(force_even_if_game_running=True)
        self._log(f"[STANDBY PURGE] {msg}")

    def _on_clear_temp(self):
        _, msg = self.core.clear_temp_files()
        self._log(f"[TEMP CLEANER] {msg}")

    def _on_kill_bloatware(self):
        killed = self.core.terminate_bloatware()
        if killed:
            self._log(f"[BLOATWARE PURGE] Terminated {len(killed)} bloatware processes: {', '.join(killed)}")
        else:
            self._log("[BLOATWARE PURGE] No bloatware processes detected.")

    def _on_open_game_picker(self):
        games = self.core.get_running_game_processes()
        top_procs = self.core.get_top_ram_processes(15)

        dlg = tk.Toplevel(self)
        dlg.title("🎯 Select Active Game Process to Boost")
        dlg.geometry("520x420")
        dlg.configure(bg=self.COLOR_BG)

        tk.Label(dlg, text="Select Game / Process to Elevate Priority:", font=('Segoe UI', 11, 'bold'), fg=self.COLOR_CYAN, bg=self.COLOR_BG).pack(padx=16, pady=(16, 8), anchor='w')

        lb = tk.Listbox(dlg, bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT, selectbackground=self.COLOR_CYAN_BG, font=('Segoe UI', 10), relief='flat')
        lb.pack(fill='both', expand=True, padx=16, pady=4)

        procs_list = games + top_procs
        seen = set()
        unique_procs = []
        for p in procs_list:
            if p['pid'] not in seen:
                seen.add(p['pid'])
                unique_procs.append(p)
                lb.insert(tk.END, f"{p['name']} (PID: {p['pid']})")

        def apply_boost():
            sel = lb.curselection()
            if sel:
                idx = sel[0]
                target = unique_procs[idx]
                ok, msg = self.core.boost_game_process(target['pid'], "high")
                self._log(f"[GAME BOOST] {msg}")
                messagebox.showinfo("Game Priority Boosted", msg)
                dlg.destroy()

        self._make_glint_button(dlg, "🎯 Boost Selected Process", self.COLOR_AMBER, "#000000", self.COLOR_AMBER_BG, apply_boost, pady=8, padx=16).pack(pady=12)

    def _on_view_top_processes(self):
        procs = self.core.get_top_ram_processes(20)
        for item in self.proc_tree.get_children():
            self.proc_tree.delete(item)

        for p in procs:
            self.proc_tree.insert('', tk.END, values=(p['pid'], p['name'], f"{p['mem_mb']} MB"))

        self._log(f"[TOP PROCESSES] Refreshed top {len(procs)} physical RAM consuming processes.")

    def _toggle_auto_guard(self):
        if not self.auto_guard_active:
            self.auto_guard_active = True
            self._log("=========================================")
            self._log("⚡ SMART AUTO-GUARD ACTIVATED (60s Monitoring Loop)")
            self._log(f"Auto-Guard will flush RAM whenever free RAM falls below {self.specs['target_free_gb']} GB.")
            self._log("=========================================")

            def loop():
                while self.auto_guard_active:
                    time.sleep(60)
                    if not self.auto_guard_active:
                        break
                    try:
                        cur_specs = self.core.get_system_specs()
                        if cur_specs['avail_ram_bytes'] < cur_specs['target_free_bytes']:
                            self._log(f"[AUTO-GUARD TRIGGER] Free RAM ({cur_specs['avail_ram_gb']} GB) below target ({cur_specs['target_free_gb']} GB). Auto-flushing...")
                            self.core.trim_process_working_sets()
                            self.core.flush_standby_list()
                    except Exception:
                        pass

            self.auto_guard_thread = threading.Thread(target=loop, daemon=True)
            self.auto_guard_thread.start()
            messagebox.showinfo("Auto-Guard Enabled", "Smart Auto-Guard is now running in the background!")
        else:
            self.auto_guard_active = False
            self._log("⚡ SMART AUTO-GUARD DEACTIVATED.")
            messagebox.showinfo("Auto-Guard Disabled", "Smart Auto-Guard de-activated.")

    def _on_clear_console(self):
        self.log_text.delete('1.0', tk.END)

    def _on_copy_log(self):
        content = self.log_text.get('1.0', tk.END)
        self.clipboard_clear()
        self.clipboard_append(content)
        self._log("[CONSOLE] Log text copied to clipboard!")


if __name__ == "__main__":
    app = DeviceOptimizerApp()
    app.mainloop()
