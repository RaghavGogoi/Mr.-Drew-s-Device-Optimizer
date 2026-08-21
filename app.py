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

from optimizer_core import OptimizerCore


class DeviceOptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.core = OptimizerCore()
        self.specs = self.core.get_system_specs()
        self.hw = self.core.get_hardware_details()
        self.auto_guard_active = False
        self.auto_guard_thread = None
        self.action_in_progress = False

        # Configure Root Window
        self.title("⚡ MR. DREW'S DEVICE & FPS OPTIMIZER - OBSIDIAN EDITION")
        self.geometry("1060x820")
        self.minsize(920, 700)

        # Apply Modern Black, Glass & Glint Palette
        self.COLOR_BG = "#030712"            # Pitch Black / Deep Obsidian
        self.COLOR_CARD_BG = "#0B132B"       # Deep Translucent Glass
        self.COLOR_CARD_SURFACE = "#111827"  # Card Surface
        self.COLOR_BORDER = "#1E293B"        # Subtle Frosted Border
        self.COLOR_BORDER_GLINT = "#334155"  # Active Glint Border
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

        # Build UI Sections
        self._create_header()
        self._create_dashboard_cards()
        self._create_ram_progress_bar()
        self._create_action_sections()
        self._create_console_log()

        # One-Time Admin Elevation Check on Startup
        self._check_one_time_elevation()

        # Initial Stats Update & Continuous Refresh Loop
        self._refresh_stats_loop()

    def _init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TFrame', background=self.COLOR_BG)

    def _create_header(self):
        header_frame = tk.Frame(self, bg=self.COLOR_BG, pady=12, padx=24)
        header_frame.pack(fill='x', side='top')

        left_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        left_frame.pack(side='left')

        title_lbl = tk.Label(
            left_frame,
            text="⚡ MR. DREW'S DEVICE & FPS OPTIMIZER",
            font=('Segoe UI', 18, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_BG
        )
        title_lbl.pack(anchor='w')

        subtitle_text = f"Smart OS Engine | {self.hw['device_profile']} | GPU: {self.hw['gpu_vendor']}"
        subtitle_lbl = tk.Label(
            left_frame,
            text=subtitle_text,
            font=('Segoe UI', 9),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        )
        subtitle_lbl.pack(anchor='w', pady=(2, 0))

        # Right side badges
        right_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        right_frame.pack(side='right')

        os_badge_text = f"💻 {self.specs['os_name']} ({self.hw['cpu_cores_logical']} Cores)"
        os_badge = tk.Label(
            right_frame,
            text=os_badge_text,
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_CYAN,
            bg=self.COLOR_CARD_SURFACE,
            padx=12,
            pady=6,
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        os_badge.pack(side='left', padx=4)

        admin_color = self.COLOR_GREEN if self.specs['is_admin'] else self.COLOR_AMBER
        admin_text = "🛡️ ADMIN ACTIVE" if self.specs['is_admin'] else "⚠️ USER MODE (Click to Elevate)"
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
            padx=12,
            pady=6,
            command=self._on_click_elevate
        )
        self.admin_badge.pack(side='left', padx=4)

    def _create_dashboard_cards(self):
        cards_frame = tk.Frame(self, bg=self.COLOR_BG, padx=24)
        cards_frame.pack(fill='x', pady=4)

        cards_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform='card')

        # Card 1: Total RAM
        self.card_total_ram = self._build_card(cards_frame, 0, "TOTAL PHYSICAL RAM", f"{self.specs['total_ram_gb']} GB", self.COLOR_CYAN)

        # Card 2: Free RAM
        self.card_free_ram = self._build_card(cards_frame, 1, "CURRENT FREE RAM", f"{self.specs['avail_ram_gb']} GB", self.COLOR_GREEN)

        # Card 3: Target Free Threshold
        self.card_target_ram = self._build_card(cards_frame, 2, "SMART TARGET FREE", f"≥ {self.specs['target_free_gb']} GB", self.COLOR_PURPLE)

        # Card 4: CPU Usage
        self.card_cpu = self._build_card(cards_frame, 3, "CPU UTILIZATION", f"{self.specs['cpu_percent']}%", self.COLOR_AMBER)

    def _build_card(self, parent, col, title, value, accent_color):
        card = tk.Frame(parent, bg=self.COLOR_CARD_SURFACE, padx=14, pady=10, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        card.grid(row=0, column=col, padx=4, sticky='nsew')

        lbl_title = tk.Label(card, text=title, font=('Segoe UI', 8, 'bold'), fg=self.COLOR_MUTED, bg=self.COLOR_CARD_SURFACE)
        lbl_title.pack(anchor='w')

        lbl_val = tk.Label(card, text=value, font=('Segoe UI', 16, 'bold'), fg=accent_color, bg=self.COLOR_CARD_SURFACE)
        lbl_val.pack(anchor='w', pady=(3, 0))

        return lbl_val

    def _create_ram_progress_bar(self):
        prog_frame = tk.Frame(self, bg=self.COLOR_BG, padx=28, pady=4)
        prog_frame.pack(fill='x')

        lbl_row = tk.Frame(prog_frame, bg=self.COLOR_BG)
        lbl_row.pack(fill='x')

        self.ram_status_lbl = tk.Label(
            lbl_row,
            text="Real-Time Physical Memory Gauge",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_BG
        )
        self.ram_status_lbl.pack(side='left')

        self.ram_percent_lbl = tk.Label(
            lbl_row,
            text="0%",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_CYAN,
            bg=self.COLOR_BG
        )
        self.ram_percent_lbl.pack(side='right')

        # Custom Canvas Progress Bar with Glint Border
        self.progress_canvas = tk.Canvas(prog_frame, height=14, bg="#0B132B", highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        self.progress_canvas.pack(fill='x', pady=4)

    def _make_glint_button(self, parent, text, bg, fg, hover_bg, cmd, font=('Segoe UI', 9, 'bold'), pady=6, padx=10):
        """Creates a modern button with interactive glint hover highlights."""
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

    def _create_action_sections(self):
        actions_frame = tk.Frame(self, bg=self.COLOR_BG, padx=24, pady=2)
        actions_frame.pack(fill='x')

        # ROW 1: GAMING & ASSET ACCELERATION ROW
        row_fps = tk.Frame(actions_frame, bg=self.COLOR_BG)
        row_fps.pack(fill='x', pady=(0, 4))

        self.btn_fps = self._make_glint_button(
            row_fps,
            "🎮 RUN FPS & GAME BOOSTER",
            self.COLOR_AMBER,
            "#000000",
            self.COLOR_AMBER_BG,
            self._on_run_fps_booster,
            font=('Segoe UI', 10, 'bold'),
            pady=7,
            padx=14
        )
        self.btn_fps.pack(side='left', padx=(0, 4))

        self.btn_asset_loader = self._make_glint_button(
            row_fps,
            "🚀 Fast Asset Loader",
            self.COLOR_GREEN,
            "#000000",
            self.COLOR_GREEN_BG,
            self._on_accelerate_asset_loading,
            font=('Segoe UI', 9, 'bold'),
            pady=7,
            padx=10
        )
        self.btn_asset_loader.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_potato = self._make_glint_button(
            row_fps,
            "🥔 4GB Potato Mode",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            self._on_run_potato_mode,
            pady=7,
            padx=10
        )
        self.btn_potato.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_power = self._make_glint_button(
            row_fps,
            "⚡ Ultimate Power",
            self.COLOR_CARD_SURFACE,
            self.COLOR_GREEN,
            "#1E293B",
            self._on_enable_power_plan,
            pady=7,
            padx=10
        )
        self.btn_power.pack(side='left', fill='x', expand=True)

        # ROW 2: RAM & MONSTER MATRIX ROW
        row_ram = tk.Frame(actions_frame, bg=self.COLOR_BG)
        row_ram.pack(fill='x', pady=(0, 4))

        self.btn_monster = self._make_glint_button(
            row_ram,
            "🔥 RUN MONSTER OPTIMIZER",
            self.COLOR_PURPLE,
            "#FFFFFF",
            self.COLOR_PURPLE_BG,
            self._on_run_monster_optimizer,
            font=('Segoe UI', 10, 'bold'),
            pady=7,
            padx=14
        )
        self.btn_monster.pack(side='left', padx=(0, 4))

        self.btn_trim = self._make_glint_button(
            row_ram,
            "✂️ Trim App RAM",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            self._on_trim_working_sets,
            pady=7,
            padx=10
        )
        self.btn_trim.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_standby = self._make_glint_button(
            row_ram,
            "🛡️ Purge Standby RAM",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            self._on_purge_standby,
            pady=7,
            padx=10
        )
        self.btn_standby.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_temp = self._make_glint_button(
            row_ram,
            "🧹 Clear Temp Files",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            self._on_clear_temp,
            pady=7,
            padx=10
        )
        self.btn_temp.pack(side='left', fill='x', expand=True)

        # ROW 3: UTILITIES & SYSTEM GUARDS
        row_utils = tk.Frame(actions_frame, bg=self.COLOR_BG)
        row_utils.pack(fill='x')

        self.btn_game_picker = self._make_glint_button(
            row_utils,
            "🎯 Boost Game Priority",
            self.COLOR_CARD_SURFACE,
            self.COLOR_AMBER,
            "#1E293B",
            self._on_open_game_picker,
            pady=6,
            padx=8
        )
        self.btn_game_picker.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_shader = self._make_glint_button(
            row_utils,
            "🧹 Clean Shader Cache",
            self.COLOR_CARD_SURFACE,
            self.COLOR_CYAN,
            "#1E293B",
            self._on_clean_shader_cache,
            pady=6,
            padx=8
        )
        self.btn_shader.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_bloatware = self._make_glint_button(
            row_utils,
            "🚫 End Bloatware",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            self._on_kill_bloatware,
            pady=6,
            padx=8
        )
        self.btn_bloatware.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_top_procs = self._make_glint_button(
            row_utils,
            "📊 Top RAM Apps",
            self.COLOR_CARD_SURFACE,
            self.COLOR_CYAN,
            "#1E293B",
            self._on_view_top_processes,
            pady=6,
            padx=8
        )
        self.btn_top_procs.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_autoguard = self._make_glint_button(
            row_utils,
            "⚡ Enable Smart Auto-Guard (60s Loop)",
            self.COLOR_CARD_SURFACE,
            self.COLOR_GREEN,
            "#1E293B",
            self._toggle_auto_guard,
            pady=6,
            padx=8
        )
        self.btn_autoguard.pack(side='left', padx=(0, 4), fill='x', expand=True)

        self.btn_refresh = self._make_glint_button(
            row_utils,
            "🔄 Refresh Stats",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            self._on_manual_refresh,
            pady=6,
            padx=8
        )
        self.btn_refresh.pack(side='left', fill='x', expand=True)

        self.action_buttons = [
            self.btn_fps, self.btn_asset_loader, self.btn_potato, self.btn_power,
            self.btn_monster, self.btn_trim, self.btn_standby, self.btn_temp,
            self.btn_game_picker, self.btn_shader, self.btn_bloatware,
            self.btn_top_procs, self.btn_autoguard, self.btn_refresh
        ]

    def _create_console_log(self):
        console_frame = tk.Frame(self, bg=self.COLOR_BG, padx=28, pady=4)
        console_frame.pack(fill='both', expand=True)

        header_bar = tk.Frame(console_frame, bg=self.COLOR_BG)
        header_bar.pack(fill='x', pady=(0, 4))

        lbl_console = tk.Label(
            header_bar,
            text="Real-Time Optimizer Console & FPS Performance Log",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        )
        lbl_console.pack(side='left')

        btn_copy = self._make_glint_button(
            header_bar,
            "📋 Copy Log",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            self._on_copy_log,
            font=('Segoe UI', 8, 'bold'),
            pady=2,
            padx=8
        )
        btn_copy.pack(side='right', padx=(4, 0))

        btn_clear = self._make_glint_button(
            header_bar,
            "🗑️ Clear Console",
            self.COLOR_CARD_SURFACE,
            self.COLOR_MUTED,
            "#1E293B",
            self._on_clear_console,
            font=('Segoe UI', 8, 'bold'),
            pady=2,
            padx=8
        )
        btn_clear.pack(side='right')

        self.log_text = scrolledtext.ScrolledText(
            console_frame,
            bg="#020617",
            fg="#10B981",
            font=('Consolas', 9),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        self.log_text.pack(fill='both', expand=True)

        self._log("System & FPS Engine initialized [OBSIDIAN GLASS EDITION].")
        self._log(f"Detected OS: {self.specs['os_name']} {self.specs['os_release']} ({self.specs['os_arch']})")
        self._log(f"Hardware Profile: {self.hw['device_profile']} | GPU: {self.hw['gpu_vendor']}")
        self._log(f"Total Physical RAM: {self.specs['total_ram_gb']} GB | Smart Free Target: {self.specs['target_free_gb']} GB")
        if self.specs['is_potato_pc']:
            self._log("Notice: 4GB Potato Device detected! '🥔 4GB Potato Mode' preset is recommended for smooth gaming.")

    def _log(self, message: str):
        """Thread-safe logging helper."""
        timestamp = time.strftime("[%H:%M:%S] ")
        full_msg = timestamp + message + "\n"
        self.after(0, self._append_log, full_msg)

    def _append_log(self, full_msg: str):
        self.log_text.insert(tk.END, full_msg)
        self.log_text.see(tk.END)

    def _safe_info(self, title: str, message: str):
        self.after(0, messagebox.showinfo, title, message)

    def _safe_warning(self, title: str, message: str):
        self.after(0, messagebox.showwarning, title, message)

    def _set_buttons_state(self, state: str):
        """Enable or disable interactive action buttons."""
        def apply():
            for btn in self.action_buttons:
                btn.config(state=state)
        self.after(0, apply)

    def _refresh_stats_loop(self):
        """Continuously update system RAM and CPU statistics in GUI."""
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
        self._log(f"[REFRESH] Free RAM: {self.specs['avail_ram_gb']} GB / Total: {self.specs['total_ram_gb']} GB | Profile: {self.hw['device_profile']}")

    def _on_run_fps_booster(self):
        """Handler for 🎮 FPS & Game Booster button."""
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

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
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_accelerate_asset_loading(self):
        """Handler for 🚀 Fast Asset Loader button."""
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("=========================================")
                self._log("🚀 ACCELERATING GAME ASSET READ & LOAD SPEED...")
                ok, logs = self.core.accelerate_game_asset_loading()
                for line in logs:
                    self._log(line)
                self._log("=========================================")
                self._safe_info("Game Asset Acceleration Complete", "Game Asset Load Speed Boosted!\n\nHigh Disk I/O Priority & CPU Priority assigned to active game.\nShader cache flushed & game asset memory protected from eviction.")
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_run_potato_mode(self):
        """Handler for 🥔 4GB Potato Mode button."""
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("=========================================")
                self._log("🥔 STARTING 4GB POTATO DEVICE OPTIMIZER...")
                res = self.core.run_potato_device_optimizer()
                for line in res['logs']:
                    self._log(line)
                self._log("=========================================")
                self._safe_info("Potato PC Optimizer Complete", f"Successfully reclaimed {res['reclaimed_gb']} GB ({res['reclaimed_mb']} MB) RAM!\nPotato Device optimization complete.")
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_enable_power_plan(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("Configuring High Performance Power Plan...")
                ok, msg = self.core.enable_high_performance_power_plan()
                self._log(f"[POWER PLAN] {msg}")
                self._safe_info("Power Plan Status", msg)
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_clean_shader_cache(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("Flushing GPU DirectX, OpenGL & Vulkan shader caches...")
                bytes_cleaned, msg = self.core.clean_gpu_shader_cache()
                self._log(f"[GPU SHADER CLEANER] {msg}")
                self._safe_info("Shader Cache Flushed", msg)
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_open_game_picker(self):
        procs = self.core.get_top_ram_processes(25)

        dlg = tk.Toplevel(self)
        dlg.title("Select Active Game / App to Boost")
        dlg.geometry("540x420")
        dlg.configure(bg=self.COLOR_BG)
        dlg.transient(self)
        dlg.grab_set()

        lbl_header = tk.Label(
            dlg,
            text="🎯 Select Active Game / Application to Boost Priority",
            font=('Segoe UI', 11, 'bold'),
            fg=self.COLOR_AMBER,
            bg=self.COLOR_BG,
            pady=10
        )
        lbl_header.pack()

        frame_list = tk.Frame(dlg, bg=self.COLOR_BG, padx=15, pady=5)
        frame_list.pack(fill='both', expand=True)

        listbox = tk.Listbox(
            frame_list,
            bg="#020617",
            fg="#F8FAFC",
            selectbackground=self.COLOR_AMBER,
            selectforeground="#000000",
            font=('Consolas', 10),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        listbox.pack(fill='both', expand=True)

        proc_map = {}
        for idx, p in enumerate(procs):
            display_str = f"PID: {p['pid']:<6} | RAM: {p['mem_mb']:<6.1f} MB | {p['name']}"
            listbox.insert(tk.END, display_str)
            proc_map[idx] = p

        def apply_boost():
            sel = listbox.curselection()
            if not sel:
                messagebox.showwarning("No Selection", "Please select a process from the list.")
                return
            proc_info = proc_map[sel[0]]
            ok, msg = self.core.boost_game_process(proc_info['pid'], "high")
            if ok:
                self._log(f"[GAME BOOST SUCCESS] {msg}")
                messagebox.showinfo("Game Priority Boosted", msg)
            else:
                self._log(f"[GAME BOOST WARNING] {msg}")
                messagebox.showwarning("Boost Notice", msg)
            dlg.destroy()

        btn_box = tk.Frame(dlg, bg=self.COLOR_BG, pady=10)
        btn_box.pack()

        btn_boost = self._make_glint_button(
            btn_box,
            "🚀 Boost Selected Process Priority",
            self.COLOR_AMBER,
            "#000000",
            self.COLOR_AMBER_BG,
            apply_boost,
            font=('Segoe UI', 10, 'bold'),
            pady=6,
            padx=16
        )
        btn_boost.pack(side='left', padx=5)

        btn_close = self._make_glint_button(
            btn_box,
            "Cancel",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            dlg.destroy,
            pady=6,
            padx=14
        )
        btn_close.pack(side='left', padx=5)

    def _on_run_monster_optimizer(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("=========================================")
                self._log("🔥 STARTING MONSTER OPTIMIZER...")
                res = self.core.run_monster_optimization()
                for line in res['logs']:
                    self._log(line)
                self._log("=========================================")
                self._safe_info("Monster Optimizer Complete", f"Successfully reclaimed {res['reclaimed_gb']} GB ({res['reclaimed_mb']} MB) of RAM!")
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_trim_working_sets(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("Compacting active process working sets...")
                total, trimmed = self.core.trim_process_working_sets()
                msg = f"Compacted working sets for {trimmed}/{total} processes."
                self._log(f"[TRIM COMPLETED] {msg}")
                self._safe_info("RAM Compaction Complete", msg)
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_clear_temp(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("Cleaning temporary files from system and user directories...")
                bytes_cleaned, msg = self.core.clear_temp_files()
                self._log(f"[TEMP CLEANER] {msg}")
                self._safe_info("Disk Temp Cleanup Complete", msg)
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_purge_standby(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("Purging Standby RAM list cache...")
                success, msg = self.core.flush_standby_list()
                if success:
                    self._log(f"[STANDBY SUCCESS] {msg}")
                    self._safe_info("Standby RAM Purged", msg)
                else:
                    self._log(f"[STANDBY WARNING] {msg}")
                    self._safe_warning("Standby RAM Purge Notice", msg)
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_kill_bloatware(self):
        if self.action_in_progress:
            return
        self.action_in_progress = True
        self._set_buttons_state('disabled')

        def worker():
            try:
                self._log("Scanning for default background bloatware processes...")
                killed = self.core.terminate_bloatware()
                if killed:
                    msg = f"Terminated {len(killed)} background bloatware process(es): {', '.join(killed)}"
                    self._log(f"[BLOATWARE PURGED] {msg}")
                    self._safe_info("Bloatware Purged", msg)
                else:
                    self._log("[BLOATWARE CHECK] No active bloatware detected.")
                    self._safe_info("Bloatware Status", "No active default bloatware processes detected.")
            finally:
                self.action_in_progress = False
                self._set_buttons_state('normal')

        threading.Thread(target=worker, daemon=True).start()

    def _on_view_top_processes(self):
        procs = self.core.get_top_ram_processes(15)

        dlg = tk.Toplevel(self)
        dlg.title("Top Memory-Consuming Processes")
        dlg.geometry("520x400")
        dlg.configure(bg=self.COLOR_BG)
        dlg.transient(self)
        dlg.grab_set()

        lbl_header = tk.Label(
            dlg,
            text="📊 Top Memory-Consuming Apps",
            font=('Segoe UI', 12, 'bold'),
            fg=self.COLOR_CYAN,
            bg=self.COLOR_BG,
            pady=10
        )
        lbl_header.pack()

        frame_list = tk.Frame(dlg, bg=self.COLOR_BG, padx=15, pady=5)
        frame_list.pack(fill='both', expand=True)

        txt_procs = scrolledtext.ScrolledText(
            frame_list,
            bg="#020617",
            fg="#F8FAFC",
            font=('Consolas', 9),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        txt_procs.pack(fill='both', expand=True)

        txt_procs.insert(tk.END, f"{'PID':<8} {'RAM (MB)':<12} {'PROCESS NAME'}\n")
        txt_procs.insert(tk.END, "-" * 48 + "\n")
        for p in procs:
            txt_procs.insert(tk.END, f"{p['pid']:<8} {p['mem_mb']:<12.1f} {p['name']}\n")

        btn_close = self._make_glint_button(
            dlg,
            "Close",
            self.COLOR_CARD_SURFACE,
            self.COLOR_TEXT,
            "#1E293B",
            dlg.destroy,
            pady=6,
            padx=16
        )
        btn_close.pack(pady=10)

    def _toggle_auto_guard(self):
        if not self.auto_guard_active:
            self.auto_guard_active = True
            self.btn_autoguard.config(text="🛑 Stop Auto-Guard (Active)", fg=self.COLOR_RED)
            self._log("Smart Auto-Guard activated. Monitoring free RAM every 60 seconds...")

            def auto_guard_loop():
                counter = 0
                while self.auto_guard_active:
                    time.sleep(1)
                    counter += 1
                    if counter >= 60:
                        counter = 0
                        if not self.auto_guard_active:
                            break
                        specs = self.core.get_system_specs()
                        if specs['avail_ram_bytes'] < specs['target_free_bytes']:
                            self._log(f"[AUTO-GUARD TRIGGERED] Free RAM ({specs['avail_ram_gb']} GB) dropped below target ({specs['target_free_gb']} GB).")
                            self.core.flush_standby_list()
                            self.core.trim_process_working_sets()

            self.auto_guard_thread = threading.Thread(target=auto_guard_loop, daemon=True)
            self.auto_guard_thread.start()
        else:
            self.auto_guard_active = False
            self.btn_autoguard.config(text="⚡ Enable Smart Auto-Guard (60s Loop)", fg=self.COLOR_GREEN)
            self._log("Smart Auto-Guard stopped.")

    def _check_one_time_elevation(self):
        """Check Admin status on startup without auto-closing the window."""
        if self.specs['os_name'] == 'Windows':
            if self.specs['is_admin']:
                self._log("[ADMIN STATUS] Application is running with full Administrator privileges.")
            else:
                self._log("[ADMIN STATUS] Application is running in User Mode. Click '⚠️ USER MODE' badge to elevate anytime.")

    def _on_click_elevate(self):
        if not self.specs['is_admin']:
            if self.specs['os_name'] == 'Windows':
                self._log("Prompting for Administrator elevation (UAC)...")
                relaunched = self.core.relaunch_as_admin()
                if relaunched:
                    self._log("Administrator elevation requested! Elevated window spawning...")
                    self.after(1500, self.destroy)
                else:
                    self.core.uac_denied = True
                    messagebox.showwarning("Elevation Notice", "Administrator elevation prompt was cancelled or denied. Continuing in User Mode.")
            else:
                messagebox.showinfo("Elevation Instructions", "On Linux/macOS, please re-launch the application in terminal using:\n\nsudo python3 app.py\nor\nsudo ./run.sh")
        else:
            messagebox.showinfo("Administrator Privileges", "Application is already running with full Administrator privileges.")

    def _on_clear_console(self):
        self.log_text.delete('1.0', tk.END)
        self._log("Console log cleared.")

    def _on_copy_log(self):
        content = self.log_text.get('1.0', tk.END)
        self.clipboard_clear()
        self.clipboard_append(content)
        messagebox.showinfo("Log Copied", "Console log copied to clipboard!")


def main():
    app = DeviceOptimizerApp()
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        try:
            with open("optimizer_error.log", "a") as f:
                f.write(err_msg + "\n")
        except Exception:
            pass
        try:
            messagebox.showerror("Optimizer Error", f"An error occurred:\n\n{err_msg}")
        except Exception:
            pass
