import sys
import os
import time
import threading
import platform
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Import our core optimizer module
try:
    from optimizer_core import OptimizerCore
except ImportError:
    # If called from different path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from optimizer_core import OptimizerCore


class DeviceOptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.core = OptimizerCore()
        self.specs = self.core.get_system_specs()
        self.auto_guard_active = False
        self.auto_guard_thread = None

        # Configure Root Window
        self.title("Mr. Drew's Device Optimizer & Memory Manager")
        self.geometry("920x680")
        self.minsize(800, 600)

        # Apply Modern Color Palette
        self.COLOR_BG = "#0F172A"       # Deep Slate
        self.COLOR_CARD = "#1E293B"     # Card Background
        self.COLOR_TEXT = "#F8FAFC"     # Off-white text
        self.COLOR_MUTED = "#94A3B8"    # Muted text
        self.COLOR_CYAN = "#06B6D4"     # Bright Cyan Accent
        self.COLOR_GREEN = "#10B981"    # Emerald Success
        self.COLOR_AMBER = "#F59E0B"    # Amber Warning
        self.COLOR_PURPLE = "#8B5CF6"   # Electric Purple (Monster Mode)
        self.COLOR_RED = "#EF4444"      # Alert Red

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

        # Frame Styles
        self.style.configure('TFrame', background=self.COLOR_BG)
        self.style.configure('Card.TFrame', background=self.COLOR_CARD, relief='flat')

        # Label Styles
        self.style.configure('Header.TLabel', background=self.COLOR_BG, foreground=self.COLOR_TEXT, font=('Segoe UI', 18, 'bold'))
        self.style.configure('SubHeader.TLabel', background=self.COLOR_BG, foreground=self.COLOR_MUTED, font=('Segoe UI', 10))
        self.style.configure('CardTitle.TLabel', background=self.COLOR_CARD, foreground=self.COLOR_MUTED, font=('Segoe UI', 9, 'bold'))
        self.style.configure('CardValue.TLabel', background=self.COLOR_CARD, foreground=self.COLOR_TEXT, font=('Segoe UI', 16, 'bold'))

    def _create_header(self):
        header_frame = tk.Frame(self, bg=self.COLOR_BG, pady=15, padx=20)
        header_frame.pack(fill='x', side='top')

        left_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        left_frame.pack(side='left')

        title_lbl = tk.Label(
            left_frame,
            text="⚡ MR. DREW'S DEVICE OPTIMIZER",
            font=('Segoe UI', 16, 'bold'),
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
        subtitle_lbl.pack(anchor='w')

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
            pady=6
        )
        os_badge.pack(side='left', padx=5)

        admin_color = self.COLOR_GREEN if self.specs['is_admin'] else self.COLOR_AMBER
        admin_text = "🛡️ ADMIN ACTIVE" if self.specs['is_admin'] else "⚠️ USER MODE (Click to Elevate)"
        admin_badge = tk.Button(
            right_frame,
            text=admin_text,
            font=('Segoe UI', 9, 'bold'),
            fg=admin_color,
            bg=self.COLOR_CARD,
            activebackground="#334155",
            activeforeground=admin_color,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=6,
            command=self._on_click_elevate
        )
        admin_badge.pack(side='left', padx=5)

    def _create_dashboard_cards(self):
        cards_frame = tk.Frame(self, bg=self.COLOR_BG, padx=20)
        cards_frame.pack(fill='x', pady=5)

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
        card = tk.Frame(parent, bg=self.COLOR_CARD, padx=15, pady=12, highlightthickness=1, highlightbackground="#334155")
        card.grid(row=0, column=col, padx=6, sticky='nsew')

        lbl_title = tk.Label(card, text=title, font=('Segoe UI', 8, 'bold'), fg=self.COLOR_MUTED, bg=self.COLOR_CARD)
        lbl_title.pack(anchor='w')

        lbl_val = tk.Label(card, text=value, font=('Segoe UI', 15, 'bold'), fg=accent_color, bg=self.COLOR_CARD)
        lbl_val.pack(anchor='w', pady=(4, 0))

        return lbl_val

    def _create_ram_progress_bar(self):
        prog_frame = tk.Frame(self, bg=self.COLOR_BG, padx=26, pady=10)
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
        self.progress_canvas = tk.Canvas(prog_frame, height=14, bg="#334155", highlightthickness=0)
        self.progress_canvas.pack(fill='x', pady=6)

    def _create_action_buttons(self):
        actions_frame = tk.Frame(self, bg=self.COLOR_BG, padx=26, pady=5)
        actions_frame.pack(fill='x')

        # Left: Giant Monster Optimizer Button
        btn_monster = tk.Button(
            actions_frame,
            text="🔥 RUN MONSTER OPTIMIZER",
            font=('Segoe UI', 12, 'bold'),
            fg="#FFFFFF",
            bg=self.COLOR_PURPLE,
            activebackground="#7C3AED",
            activeforeground="#FFFFFF",
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=12,
            command=self._on_run_monster_optimizer
        )
        btn_monster.pack(side='left', fill='y', padx=(0, 10))

        # Right: Quick Action Grid
        right_actions = tk.Frame(actions_frame, bg=self.COLOR_BG)
        right_actions.pack(side='left', fill='both', expand=True)

        top_row = tk.Frame(right_actions, bg=self.COLOR_BG)
        top_row.pack(fill='x', pady=(0, 5))

        btn_temp = tk.Button(
            top_row,
            text="🧹 Clear Temp Files",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground="#334155",
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=6,
            command=self._on_clear_temp
        )
        btn_temp.pack(side='left', padx=(0, 5), fill='x', expand=True)

        btn_standby = tk.Button(
            top_row,
            text="🛡️ Purge Standby RAM",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_TEXT,
            bg=self.COLOR_CARD,
            activebackground="#334155",
            activeforeground=self.COLOR_TEXT,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=6,
            command=self._on_purge_standby
        )
        btn_standby.pack(side='left', padx=(0, 5), fill='x', expand=True)

        bottom_row = tk.Frame(right_actions, bg=self.COLOR_BG)
        bottom_row.pack(fill='x')

        # Auto Guard Toggle Button
        self.btn_autoguard = tk.Button(
            bottom_row,
            text="⚡ Enable Smart Auto-Guard (60s Loop)",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_CYAN,
            bg=self.COLOR_CARD,
            activebackground="#334155",
            activeforeground=self.COLOR_CYAN,
            relief='flat',
            cursor='hand2',
            padx=12,
            pady=6,
            command=self._toggle_auto_guard
        )
        self.btn_autoguard.pack(side='left', fill='x', expand=True)

    def _create_console_log(self):
        console_frame = tk.Frame(self, bg=self.COLOR_BG, padx=26, pady=10)
        console_frame.pack(fill='both', expand=True)

        lbl_console = tk.Label(
            console_frame,
            text="Real-Time Optimizer Log Output",
            font=('Segoe UI', 9, 'bold'),
            fg=self.COLOR_MUTED,
            bg=self.COLOR_BG
        )
        lbl_console.pack(anchor='w', pady=(0, 4))

        self.log_text = scrolledtext.ScrolledText(
            console_frame,
            bg="#020617",
            fg="#A7F3D0",
            font=('Consolas', 9),
            relief='flat',
            highlightthickness=1,
            highlightbackground="#1E293B"
        )
        self.log_text.pack(fill='both', expand=True)

        self._log("System initialized. Monster Optimizer ready.")
        self._log(f"Detected OS: {self.specs['os_name']} {self.specs['os_release']} ({self.specs['os_arch']})")
        self._log(f"Total Physical RAM: {self.specs['total_ram_gb']} GB | Smart Free RAM Target: {self.specs['target_free_gb']} GB")
        if not self.specs['is_admin'] and self.specs['os_name'] == 'Windows':
            self._log("Notice: Running in User mode. For kernel Standby RAM purge, run application as Administrator.")

    def _log(self, message: str):
        timestamp = time.strftime("[%H:%M:%S] ")
        self.log_text.insert(tk.END, timestamp + message + "\n")
        self.log_text.see(tk.END)

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
                if width > 1:
                    fill_width = (pct / 100.0) * width
                    bar_color = self.COLOR_GREEN if self.specs['avail_ram_gb'] >= self.specs['target_free_gb'] else self.COLOR_AMBER
                    self.progress_canvas.create_rectangle(0, 0, fill_width, 14, fill=bar_color, width=0)
            except Exception:
                pass
            self.after(2000, update)

        self.after(500, update)

    def _on_run_monster_optimizer(self):
        """Handler for Monster Optimizer button."""
        def worker():
            self._log("=========================================")
            self._log("🔥 STARTING MONSTER OPTIMIZER...")
            res = self.core.run_monster_optimization()
            for line in res['logs']:
                self._log(line)
            self._log("=========================================")
            messagebox.showinfo("Monster Optimizer Complete", f"Successfully reclaimed {res['reclaimed_gb']} GB ({res['reclaimed_mb']} MB) of RAM!")

        threading.Thread(target=worker, daemon=True).start()

    def _on_clear_temp(self):
        def worker():
            self._log("Cleaning temporary files...")
            bytes_cleaned, msg = self.core.clear_temp_files()
            self._log(msg)

        threading.Thread(target=worker, daemon=True).start()

    def _on_click_elevate(self):
        if not self.specs['is_admin']:
            self._log("Prompting for Administrator elevation (UAC)...")
            relaunched = self.core.relaunch_as_admin()
            if relaunched:
                self._log("Relaunching application as Administrator...")
                self.after(800, self.destroy)
            else:
                messagebox.showwarning("Elevation Failed", "Administrator elevation was cancelled or denied.")
        else:
            messagebox.showinfo("Administrator Privileges", "Application is already running with full Administrator privileges.")

    def _on_purge_standby(self):
        if not self.specs['is_admin'] and self.specs['os_name'] == 'Windows':
            res = messagebox.askyesno(
                "Administrator Privileges Required",
                "Flushing the Windows Standby Memory list requires Administrator privileges.\n\n"
                "Would you like to restart the optimizer as Administrator now?"
            )
            if res:
                self._on_click_elevate()
                return

        def worker():
            self._log("Purging Standby RAM list...")
            success, msg = self.core.flush_standby_list()
            if success:
                self._log(f"SUCCESS: {msg}")
            else:
                self._log(f"WARNING: {msg}")

        threading.Thread(target=worker, daemon=True).start()

    def _toggle_auto_guard(self):
        if not self.auto_guard_active:
            self.auto_guard_active = True
            self.btn_autoguard.config(text="🛑 Stop Auto-Guard (Active)", fg=self.COLOR_RED)
            self._log("Smart Auto-Guard activated. Monitoring free RAM every 60 seconds...")

            def auto_guard_loop():
                while self.auto_guard_active:
                    specs = self.core.get_system_specs()
                    if specs['avail_ram_bytes'] < specs['target_free_bytes']:
                        self._log(f"[AUTO-GUARD TRIGGERED] Free RAM ({specs['avail_ram_gb']} GB) dropped below threshold ({specs['target_free_gb']} GB).")
                        self.core.flush_standby_list()
                        self.core.trim_process_working_sets()
                    time.sleep(60)

            self.auto_guard_thread = threading.Thread(target=auto_guard_loop, daemon=True)
            self.auto_guard_thread.start()
        else:
            self.auto_guard_active = False
            self.btn_autoguard.config(text="⚡ Enable Smart Auto-Guard (60s Loop)", fg=self.COLOR_CYAN)
            self._log("Smart Auto-Guard stopped.")


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
