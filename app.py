import sys
import os
import time
import threading
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Ensure working directory is set to script location (prevents UAC System32 dir reset)
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
        self.auto_guard_active = False
        self.auto_guard_thread = None
        self.action_in_progress = False

        # Configure Root Window
        self.title("Mr. Drew's Device Optimizer & Memory Manager")
        self.geometry("960x720")
        self.minsize(850, 640)

        # Apply Modern Dark Palette
        self.COLOR_BG = "#0F172A"       # Deep Slate
        self.COLOR_CARD = "#1E293B"     # Card Background
        self.COLOR_CARD_HOVER = "#334155"# Hover Card
        self.COLOR_TEXT = "#F8FAFC"     # Off-white text
        self.COLOR_MUTED = "#94A3B8"    # Muted text
        self.COLOR_CYAN = "#06B6D4"     # Bright Cyan Accent
        self.COLOR_CYAN_HOVER = "#0891B2"
        self.COLOR_GREEN = "#10B981"    # Emerald Success
        self.COLOR_GREEN_HOVER = "#059669"
        self.COLOR_AMBER = "#F59E0B"    # Amber Warning
        self.COLOR_PURPLE = "#8B5CF6"   # Electric Purple (Monster Mode)
        self.COLOR_PURPLE_HOVER = "#7C3AED"
        self.COLOR_RED = "#EF4444"      # Alert Red
        self.COLOR_RED_HOVER = "#DC2626"
        self.COLOR_BORDER = "#334155"   # Subtle Card Border

        self.configure(bg=self.COLOR_BG)

        # Style Configuration
        self._init_styles()

        # Build UI Sections
        self._create_header()
        self._create_dashboard_cards()
        self._create_ram_progress_bar()
        self._create_action_buttons()
        self._create_console_log()

        # Initial Stats Update & Continuous Refresh Loop
        self._refresh_stats_loop()

    def _init_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure('TFrame', background=self.COLOR_BG)
        self.style.configure('Card.TFrame', background=self.COLOR_CARD, relief='flat')

    def _create_header(self):
        header_frame = tk.Frame(self, bg=self.COLOR_BG, pady=12, padx=24)
        header_frame.pack(fill='x', side='top')

        left_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        left_frame.pack(side='left')

        title_lbl = tk.Label(
            left_frame,
            text="⚡ MR. DREW'S DEVICE OPTIMIZER",
            font=('Segoe UI', 17, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_BG
        )
        title_lbl.pack(anchor='w')

        subtitle_lbl = tk.Label(
            left_frame,
            text="Smart OS & Dynamic RAM Adaptability Engine | Cross-Platform Workload Prep",
            font=('Segoe UI', 9),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        )
        subtitle_lbl.pack(anchor='w', pady=(2, 0))

        # Right side badges
        right_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        right_frame.pack(side='right')

        os_badge_text = f"💻 {self.specs['os_name']} {self.specs['os_release']}"
        os_badge = tk.Label(
            right_frame,
            text=os_badge_text,
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_CYAN,
            bg=self.COLOR_CARD,
            padx=12,
            pady=6,
            relief='solid',
            bd=1,
            highlightthickness=0
        )
        os_badge.pack(side='left', padx=4)

        admin_color = self.COLOR_GREEN if self.specs['is_admin'] else self.COLOR_AMBER
        admin_text = "🛡️ ADMIN ACTIVE" if self.specs['is_admin'] else "⚠️ USER MODE (Click to Elevate)"
        self.admin_badge = tk.Button(
            right_frame,
            text=admin_text,
            font=('Segoe UI', 9, 'bold'),
            fg=admin_color,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=admin_color,
            relief='flat',
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
        card = tk.Frame(parent, bg=self.COLOR_CARD, padx=14, pady=10, highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        card.grid(row=0, column=col, padx=4, sticky='nsew')

        lbl_title = tk.Label(card, text=title, font=('Segoe UI', 8, 'bold'), fg=self.COLOR_MUTED, bg=self.COLOR_CARD)
        lbl_title.pack(anchor='w')

        lbl_val = tk.Label(card, text=value, font=('Segoe UI', 15, 'bold'), fg=accent_color, bg=self.COLOR_CARD)
        lbl_val.pack(anchor='w', pady=(2, 0))

        return lbl_val

    def _create_ram_progress_bar(self):
        prog_frame = tk.Frame(self, bg=self.COLOR_BG, padx=28, pady=8)
        prog_frame.pack(fill='x')

        lbl_row = tk.Frame(prog_frame, bg=self.COLOR_BG)
        lbl_row.pack(fill='x')

        self.ram_status_lbl = tk.Label(
            lbl_row,
            text="Memory Usage Gauge",
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

        # Custom Canvas Progress Bar
        self.progress_canvas = tk.Canvas(prog_frame, height=16, bg="#1E293B", highlightthickness=1, highlightbackground=self.COLOR_BORDER)
        self.progress_canvas.pack(fill='x', pady=5)

    def _create_action_buttons(self):
        actions_frame = tk.Frame(self, bg=self.COLOR_BG, padx=28, pady=4)
        actions_frame.pack(fill='x')

        # Main Row
        top_actions = tk.Frame(actions_frame, bg=self.COLOR_BG)
        top_actions.pack(fill='x', pady=(0, 6))

        # Giant Monster Optimizer Button
        self.btn_monster = tk.Button(
            top_actions,
            text="🔥 RUN MONSTER OPTIMIZER",
            font=('Segoe UI', 11, 'bold'),
            fg="#FFFFFF",
            bg=self.COLOR_PURPLE,
            activebackground=self.COLOR_PURPLE_HOVER,
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=18,
            pady=10,
            command=self._on_run_monster_optimizer
        )
        self.btn_monster.pack(side='left', padx=(0, 6))

        self.btn_trim = tk.Button(
            top_actions,
            text="✂️ Trim App RAM",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=10,
            command=self._on_trim_working_sets
        )
        self.btn_trim.pack(side='left', padx=(0, 6), fill='x', expand=True)

        self.btn_standby = tk.Button(
            top_actions,
            text="🛡️ Purge Standby RAM",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=10,
            command=self._on_purge_standby
        )
        self.btn_standby.pack(side='left', padx=(0, 6), fill='x', expand=True)

        self.btn_temp = tk.Button(
            top_actions,
            text="🧹 Clear Temp Files",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=10,
            command=self._on_clear_temp
        )
        self.btn_temp.pack(side='left', fill='x', expand=True)

        # Secondary Row
        bottom_actions = tk.Frame(actions_frame, bg=self.COLOR_BG)
        bottom_actions.pack(fill='x')

        self.btn_bloatware = tk.Button(
            bottom_actions,
            text="🚫 End Bloatware",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_AMBER,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_AMBER,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=8,
            command=self._on_kill_bloatware
        )
        self.btn_bloatware.pack(side='left', padx=(0, 6), fill='x', expand=True)

        self.btn_top_procs = tk.Button(
            bottom_actions,
            text="📊 Top RAM Apps",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_CYAN,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_CYAN,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=8,
            command=self._on_view_top_processes
        )
        self.btn_top_procs.pack(side='left', padx=(0, 6), fill='x', expand=True)

        self.btn_autoguard = tk.Button(
            bottom_actions,
            text="⚡ Enable Smart Auto-Guard (60s Loop)",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_GREEN,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_GREEN,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=8,
            command=self._toggle_auto_guard
        )
        self.btn_autoguard.pack(side='left', padx=(0, 6), fill='x', expand=True)

        self.btn_refresh = tk.Button(
            bottom_actions,
            text="🔄 Refresh Stats",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=8,
            command=self._on_manual_refresh
        )
        self.btn_refresh.pack(side='left', fill='x', expand=True)

        self.action_buttons = [
            self.btn_monster, self.btn_trim, self.btn_standby, self.btn_temp,
            self.btn_bloatware, self.btn_top_procs, self.btn_refresh
        ]

    def _create_console_log(self):
        console_frame = tk.Frame(self, bg=self.COLOR_BG, padx=28, pady=8)
        console_frame.pack(fill='both', expand=True)

        header_bar = tk.Frame(console_frame, bg=self.COLOR_BG)
        header_bar.pack(fill='x', pady=(0, 4))

        lbl_console = tk.Label(
            header_bar,
            text="Real-Time Optimizer Console & Output Log",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        )
        lbl_console.pack(side='left')

        btn_copy = tk.Button(
            header_bar,
            text="📋 Copy Log",
            font=('Segoe UI', 8, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=8,
            pady=2,
            command=self._on_copy_log
        )
        btn_copy.pack(side='right', padx=(4, 0))

        btn_clear = tk.Button(
            header_bar,
            text="🗑️ Clear Console",
            font=('Segoe UI', 8, 'bold'),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=8,
            pady=2,
            command=self._on_clear_console
        )
        btn_clear.pack(side='right')

        self.log_text = scrolledtext.ScrolledText(
            console_frame,
            bg="#020617",
            fg="#A7F3D0",
            font=('Consolas', 9),
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER
        )
        self.log_text.pack(fill='both', expand=True)

        self._log("System initialized. Monster Optimizer ready.")
        self._log(f"Detected OS: {self.specs['os_name']} {self.specs['os_release']} ({self.specs['os_arch']})")
        self._log(f"Total Physical RAM: {self.specs['total_ram_gb']} GB | Smart Free RAM Target: {self.specs['target_free_gb']} GB")
        if not self.specs['is_admin']:
            if self.specs['os_name'] == 'Windows':
                self._log("Notice: Running in User mode. For kernel Standby RAM purge, click '⚠️ USER MODE' to elevate Administrator privileges.")
            else:
                self._log("Notice: Running as standard user. For elevated cache purging, launch app with sudo / root.")

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

                # Draw Canvas Progress Bar
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
        self.card_total_ram.config(text=f"{self.specs['total_ram_gb']} GB")
        self.card_free_ram.config(text=f"{self.specs['avail_ram_gb']} GB")
        self.card_target_ram.config(text=f"≥ {self.specs['target_free_gb']} GB")
        self.card_cpu.config(text=f"{self.specs['cpu_percent']}%")
        self._log(f"[REFRESH] Free RAM: {self.specs['avail_ram_gb']} GB / Total: {self.specs['total_ram_gb']} GB | CPU: {self.specs['cpu_percent']}%")

    def _on_run_monster_optimizer(self):
        """Handler for Monster Optimizer button."""
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

        btn_close = tk.Button(
            dlg,
            text="Close",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground=self.COLOR_CARD_HOVER,
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=16,
            pady=6,
            command=dlg.destroy
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

    def _on_click_elevate(self):
        if not self.specs['is_admin']:
            if self.specs['os_name'] == 'Windows':
                self._log("Prompting for Administrator elevation (UAC)...")
                relaunched = self.core.relaunch_as_admin()
                if relaunched:
                    self._log("Relaunching application as Administrator...")
                    self.after(800, self.destroy)
                else:
                    messagebox.showwarning("Elevation Cancelled", "Administrator elevation prompt was cancelled or denied.")
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
