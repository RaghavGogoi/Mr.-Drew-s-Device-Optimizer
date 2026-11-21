import sys
import os
import time
import threading
import platform
import subprocess
import json
import webbrowser
from typing import Optional, Dict, Any, List, Tuple

# Ensure working directory is set to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import config
from optimizer_core import OptimizerCore

try:
    import webview
    HAS_WEBVIEW = True
except ImportError:
    HAS_WEBVIEW = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    import pystray
    from PIL import Image, ImageDraw
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False


class Api:
    """
    Python Bridge API exposed to JavaScript in PyWebView frontend.
    Allows HTML5/CSS3/JS UI to trigger high-speed C++ & Python core optimizations.
    """
    def __init__(self):
        self.core = OptimizerCore()

    def get_system_specs(self) -> dict:
        return self.core.get_system_specs()

    def get_hardware_details(self) -> dict:
        return self.core.get_hardware_details()

    def get_top_ram_processes(self, count: int = 15) -> list:
        return self.core.get_top_ram_processes(count)

    def is_first_run(self) -> bool:
        return config.is_first_run()

    def set_first_run_completed(self, completed: bool = True) -> bool:
        return config.set_first_run_completed(completed)

    def reset_first_run(self) -> bool:
        return config.reset_first_run()

    def get_config(self) -> dict:
        return config.load_config()

    def save_config(self, config_dict: dict) -> bool:
        return config.save_config(config_dict)

    def update_setting(self, key: str, value: any) -> bool:
        res = config.update_setting(key, value)
        if key == "run_on_startup":
            self.core.set_run_on_startup(bool(value))
        return res

    def reset_config(self) -> dict:
        return config.reset_to_defaults()

    def set_run_on_startup(self, enable: bool) -> dict:
        ok, msg = self.core.set_run_on_startup(enable)
        config.update_setting("run_on_startup", enable)
        return {"status": ok, "message": msg}

    def is_startup_enabled(self) -> bool:
        return self.core.is_startup_enabled()

    def export_diagnostics(self) -> str:
        specs = self.core.get_system_specs()
        hw = self.core.get_hardware_details()
        cfg = config.load_config()
        diag = [
            "============================================================",
            "  MR. DREW'S DEVICE OPTIMIZER - SYSTEM DIAGNOSTIC REPORT",
            "============================================================",
            f"OS: {specs.get('os_name')} ({specs.get('os_type')})",
            f"Elevation Status: {'Administrator / Root' if specs.get('is_admin') else 'Standard User'}",
            f"Physical RAM: {specs.get('used_ram_gb')} / {specs.get('total_ram_gb')} GB ({specs.get('percent_used')}% used)",
            f"Available RAM: {specs.get('avail_ram_gb')} GB",
            f"Standby / Cache RAM: {specs.get('standby_ram_gb')} GB",
            f"CPU Load: {specs.get('cpu_percent')}% ({hw.get('cpu_cores_logical')} logical cores)",
            f"GPU: {hw.get('gpu_vendor')}",
            f"Device Profile: {hw.get('device_profile')}",
            f"Precision Timer: {specs.get('timer_res_ms')} ms",
            f"Continuous Daemon Active: {self.core.is_continuous_active()}",
            f"Run on Startup: {self.core.is_startup_enabled()}",
            f"Close to Tray: {cfg.get('close_to_tray', True)}",
            f"Active Theme: {cfg.get('theme', 'obsidian')}",
            "============================================================"
        ]
        return "\n".join(diag)

    def get_guide_steps(self) -> list:
        try:
            from tutorial_manager import TUTORIAL_STEPS
            return TUTORIAL_STEPS
        except Exception:
            return []

    # =========================================================================
    # Continuous Optimizer Methods
    # =========================================================================

    def start_continuous_mode(self, interval_sec: int = 30, mode: str = "gaming", target_free_gb: float = 4.0) -> dict:
        """Starts the persistent background continuous optimizer."""
        ok, msg = self.core.start_continuous_mode(interval_sec, mode, target_free_gb)
        config.update_setting("continuous_enabled", True)
        config.update_setting("continuous_mode", mode)
        config.update_setting("continuous_interval_sec", interval_sec)
        return {
            "status": ok,
            "message": msg,
            "continuous_info": self.core.get_continuous_status()
        }

    def stop_continuous_mode(self) -> dict:
        """Stops the persistent background continuous optimizer."""
        ok, msg = self.core.stop_continuous_mode()
        config.update_setting("continuous_enabled", False)
        return {
            "status": ok,
            "message": msg,
            "continuous_info": self.core.get_continuous_status()
        }

    def get_continuous_status(self) -> dict:
        """Returns the current state and telemetry of the continuous optimizer."""
        return self.core.get_continuous_status()

    def toggle_continuous_mode(self, enable: Optional[bool] = None, mode: str = "gaming", interval_sec: int = 30) -> dict:
        """Toggles the continuous optimizer on or off."""
        if enable is None:
            enable = not self.core.is_continuous_active()

        if enable:
            return self.start_continuous_mode(interval_sec, mode)
        else:
            return self.stop_continuous_mode()

    # =========================================================================
    # Action Gateway
    # =========================================================================

    def execute_action(self, action_id: str, extra_arg: any = None) -> dict:
        """Executes system actions and returns structured log response to JS UI."""
        if action_id == "run_fps_booster":
            return self.core.run_fps_booster(extra_arg)
        elif action_id == "accelerate_asset_loading":
            ok, logs = self.core.accelerate_game_asset_loading(extra_arg)
            return {"status": ok, "logs": logs}
        elif action_id == "run_potato_mode":
            return self.core.run_potato_device_optimizer()
        elif action_id == "enable_power_plan":
            ok, msg = self.core.enable_high_performance_power_plan()
            return {"status": ok, "logs": [f"[POWER PLAN] {msg}"]}
        elif action_id == "run_monster_optimizer":
            return self.core.run_monster_optimization()
        elif action_id == "trim_working_sets":
            processed, succeeded = self.core.trim_process_working_sets()
            return {"logs": [f"[TRIM RAM] Compacted memory working sets for {succeeded}/{processed} processes."]}
        elif action_id == "purge_standby":
            ok, msg = self.core.flush_standby_list(force_even_if_game_running=True)
            return {"logs": [f"[STANDBY PURGE] {msg}"]}
        elif action_id == "clear_temp":
            cleaned_bytes, msg = self.core.clear_temp_files()
            return {"logs": [f"[TEMP CLEANER] {msg}"]}
        elif action_id == "clean_shader_cache":
            cleaned_bytes, msg = self.core.clean_gpu_shader_cache()
            return {"logs": [f"[GPU SHADERS] {msg}"]}
        elif action_id == "kill_bloatware":
            killed = self.core.terminate_bloatware()
            if killed:
                return {"logs": [f"[BLOATWARE PURGE] Terminated {len(killed)} processes: {', '.join(killed)}"]}
            else:
                return {"logs": ["[BLOATWARE PURGE] No active bloatware processes detected."]}
        elif action_id == "kill_process":
            if extra_arg and HAS_PSUTIL:
                try:
                    pid = int(extra_arg)
                    proc = psutil.Process(pid)
                    pname = proc.name()
                    proc.kill()
                    return {"logs": [f"[PROCESS MANAGER] Terminated '{pname}' (PID: {pid})."]}
                except Exception as e:
                    return {"logs": [f"[PROCESS ERROR] {str(e)}"]}
            return {"logs": ["[PROCESS MANAGER] Process ID not specified."]}
        elif action_id == "elevate_admin":
            if self.core.is_admin:
                return {"logs": ["[ELEVATION] Optimizer is already running with Administrator / Elevated privileges."]}
            
            ok, msg = self.core.relaunch_as_admin()
            if ok:
                def _close_old_instance():
                    time.sleep(0.4)
                    try:
                        if HAS_WEBVIEW and webview.windows:
                            for w in list(webview.windows):
                                w.destroy()
                    except Exception:
                        pass
                    os._exit(0)

                threading.Thread(target=_close_old_instance, daemon=True).start()
                return {"logs": ["[ELEVATION] Relaunching with Administrator privileges... Closing standard instance."]}
            else:
                return {"logs": [f"[ELEVATION] {msg}"]}
        elif action_id == "reset_tutorial":
            config.reset_first_run()
            return {"logs": ["[CONFIG] Tutorial state reset successfully!"]}
        elif action_id == "open_game_picker":
            games = self.core.get_running_game_processes()
            if games:
                ok, msg = self.core.boost_game_process(games[0]['pid'], "high")
                return {"logs": [f"[GAME BOOST] {msg}"]}
            else:
                return {"logs": ["[GAME BOOST] No active game detected. Priority protection active for your next game."]}
        
        return {"logs": [f"Executed: {action_id}"]}


def set_windows_app_icon(icon_ico_path):
    """Sets Win32 HWND icons (WM_SETICON) for top-left title bar corner and taskbar icon on Windows."""
    if platform.system().lower() != "windows" or not os.path.exists(icon_ico_path):
        return
    try:
        import ctypes
        from ctypes import wintypes
        
        myappid = "mrdrew.deviceoptimizer.app.2.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x0010

        h_icon_big = ctypes.windll.user32.LoadImageW(
            None, icon_ico_path, IMAGE_ICON, 64, 64, LR_LOADFROMFILE
        )
        h_icon_small = ctypes.windll.user32.LoadImageW(
            None, icon_ico_path, IMAGE_ICON, 32, 32, LR_LOADFROMFILE
        )

        def enum_windows_callback(hwnd, lParam):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                if "Mr. Drew's Device Optimizer" in buff.value or "Device Optimizer" in buff.value:
                    if h_icon_big:
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, h_icon_big)
                    if h_icon_small:
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, h_icon_small)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        
        def apply_loop():
            for _ in range(8):
                time.sleep(0.4)
                try:
                    ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
                except Exception:
                    pass

        threading.Thread(target=apply_loop, daemon=True).start()
    except Exception:
        pass


def setup_system_tray(window, api, core):
    """Initializes system tray icon in background for Run in Background / Close to Tray support."""
    if not HAS_TRAY:
        return None

    try:
        logo_png = os.path.join(SCRIPT_DIR, "gui", "assets", "logo.png")
        if os.path.exists(logo_png):
            image = Image.open(logo_png)
        else:
            image = Image.new('RGB', (64, 64), color=(3, 7, 18))
            d = ImageDraw.Draw(image)
            d.polygon([(34, 8), (14, 36), (30, 36), (28, 56), (50, 28), (34, 28)], fill=(0, 240, 255))

        def on_open_window(icon, item):
            if window:
                try:
                    window.show()
                    window.restore()
                except Exception:
                    pass

        def on_toggle_continuous(icon, item):
            if core.is_continuous_active():
                core.stop_continuous_mode()
            else:
                cfg = config.load_config()
                core.start_continuous_mode(
                    interval_sec=cfg.get("continuous_interval_sec", 30),
                    mode=cfg.get("continuous_mode", "gaming"),
                    target_free_gb=cfg.get("target_free_ram_gb", 4.0)
                )

        def on_quick_purge(icon, item):
            core.run_monster_optimizer()

        def on_quit_app(icon, item):
            window._force_quit = True
            core.stop_continuous_mode()
            icon.stop()
            try:
                window.destroy()
            except Exception:
                pass
            os._exit(0)

        menu = pystray.Menu(
            pystray.MenuItem("Open Optimizer", on_open_window, default=True),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Toggle Continuous Optimizer", on_toggle_continuous),
            pystray.MenuItem("Instant RAM Purge", on_quick_purge),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit Optimizer Completely", on_quit_app)
        )

        tray = pystray.Icon("MrDrewOptimizer", image, "Mr. Drew's Device Optimizer", menu=menu)
        threading.Thread(target=tray.run, daemon=True).start()
        return tray
    except Exception as e:
        print(f"[TRAY INFO] System tray initialization skipped: {e}")
        return None


def start_local_http_server(port=8080):
    """Fallback local HTTP server if PyWebView runs in browser mode."""
    import http.server
    import socketserver
    
    gui_dir = os.path.join(SCRIPT_DIR, "gui")
    os.chdir(gui_dir)
    handler = http.server.SimpleHTTPRequestHandler
    
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True
        
    with ReusableTCPServer(("127.0.0.1", port), handler) as httpd:
        httpd.serve_forever()


def main():
    api = Api()
    html_path = os.path.join(SCRIPT_DIR, "gui", "index.html")
    icon_ico = os.path.join(SCRIPT_DIR, "gui", "assets", "logo.ico")

    is_minimized_launch = "--minimized" in sys.argv

    print("[+] Starting Mr. Drew's Device Optimizer (Cross-Platform)...")
    if platform.system().lower() == "windows":
        set_windows_app_icon(icon_ico)

    # Check if continuous mode was enabled in config
    cfg = config.load_config()
    if cfg.get("continuous_enabled", False):
        api.start_continuous_mode(
            interval_sec=cfg.get("continuous_interval_sec", 30),
            mode=cfg.get("continuous_mode", "gaming"),
            target_free_gb=cfg.get("target_free_ram_gb", 4.0)
        )

    if HAS_WEBVIEW:
        try:
            window = webview.create_window(
                "Mr. Drew's Device Optimizer",
                url=html_path,
                js_api=api,
                width=1140,
                height=800,
                min_size=(920, 640),
                background_color="#030712",
                hidden=is_minimized_launch
            )

            window._force_quit = False
            tray_instance = setup_system_tray(window, api, api.core)

            def on_closing():
                curr_cfg = config.load_config()
                if curr_cfg.get("close_to_tray", True) and not getattr(window, "_force_quit", False):
                    window.hide()
                    return False  # Prevent window destruction, keep running in background!

                # Otherwise, quit completely
                api.core.stop_continuous_mode()
                if tray_instance:
                    try:
                        tray_instance.stop()
                    except Exception:
                        pass
                return True

            window.events.closing += on_closing
            webview.start(debug=False)
            return
        except Exception as e:
            print(f"[WEBVIEW WARNING] Native window launch failed: {e}")
            print("[WEBVIEW FALLBACK] Launching local browser interface...")

    # Fallback to local HTTP server + default browser launch
    port = 8080
    t = threading.Thread(target=start_local_http_server, args=(port,), daemon=True)
    t.start()
    
    url = f"http://127.0.0.1:{port}"
    print(f"[+] Local Web GUI running at: {url}")
    if not is_minimized_launch:
        webbrowser.open(url)
        
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] Optimizer stopped.")


if __name__ == "__main__":
    main()
