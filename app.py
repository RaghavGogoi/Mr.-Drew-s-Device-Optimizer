import sys
import os
import time
import threading
import platform
import subprocess
import json
import webbrowser

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


class Api:
    """
    Python Bridge API exposed to JavaScript in PyWebView frontend.
    Allows HTML5/CSS3/JS UI to trigger high-speed C++ & Python core optimizations.
    """
    def __init__(self):
        self.core = OptimizerCore()
        self.auto_guard_active = False
        self.auto_guard_thread = None

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
            return {"logs": [f"[TRIM WORKING SETS] Compacted memory for {succeeded}/{processed} processes."]}
        elif action_id == "purge_standby":
            ok, msg = self.core.flush_standby_list(force_even_if_game_running=True)
            return {"logs": [f"[STANDBY PURGE] {msg}"]}
        elif action_id == "clear_temp":
            cleaned_bytes, msg = self.core.clear_temp_files()
            return {"logs": [f"[TEMP CLEANER] {msg}"]}
        elif action_id == "clean_shader_cache":
            cleaned_bytes, msg = self.core.clean_gpu_shader_cache()
            return {"logs": [f"[GPU SHADER CLEANER] {msg}"]}
        elif action_id == "kill_bloatware":
            killed = self.core.terminate_bloatware()
            if killed:
                return {"logs": [f"[BLOATWARE PURGE] Terminated {len(killed)} bloat processes: {', '.join(killed)}"]}
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
                    return {"logs": [f"[PROCESS MANAGER ERROR] {str(e)}"]}
            return {"logs": ["[PROCESS MANAGER] Process ID not specified."]}
        elif action_id == "toggle_auto_guard":
            if not self.auto_guard_active:
                self.auto_guard_active = True
                def loop():
                    while self.auto_guard_active:
                        time.sleep(60)
                        if not self.auto_guard_active:
                            break
                        try:
                            specs = self.core.get_system_specs()
                            if specs['avail_ram_bytes'] < specs['target_free_bytes']:
                                self.core.trim_process_working_sets()
                                self.core.flush_standby_list()
                        except Exception:
                            pass
                self.auto_guard_thread = threading.Thread(target=loop, daemon=True)
                self.auto_guard_thread.start()
                return {"logs": ["⚡ SMART AUTO-GUARD ACTIVATED (60s Monitoring Loop)."]}
            else:
                self.auto_guard_active = False
                return {"logs": ["⚡ SMART AUTO-GUARD DEACTIVATED."]}
        elif action_id == "reset_tutorial":
            config.reset_first_run()
            return {"logs": ["[TUTORIAL CONFIG] First-run tutorial flag reset!"]}
        elif action_id == "open_game_picker":
            games = self.core.get_running_game_processes()
            if games:
                ok, msg = self.core.boost_game_process(games[0]['pid'], "high")
                return {"logs": [f"[GAME BOOST] {msg}"]}
            else:
                return {"logs": ["[GAME BOOST] No active game detected. Pre-configured asset loader protection."]}
        
        return {"logs": [f"Unknown action: {action_id}"]}


def set_windows_app_icon(icon_ico_path):
    """Sets Win32 HWND icons (WM_SETICON) for top-left title bar corner and taskbar icon."""
    if platform.system().lower() != "windows" or not os.path.exists(icon_ico_path):
        return
    try:
        import ctypes
        from ctypes import wintypes
        
        # Register AppUserModelID so Windows Taskbar displays custom app icon
        myappid = "mrdrew.deviceoptimizer.app.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x0010

        h_icon_big = ctypes.windll.user32.LoadImageW(
            None, icon_ico_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE
        )
        h_icon_small = ctypes.windll.user32.LoadImageW(
            None, icon_ico_path, IMAGE_ICON, 16, 16, LR_LOADFROMFILE
        )

        def enum_windows_callback(hwnd, lParam):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                if "Mr. Drew's Device & FPS Optimizer" in buff.value:
                    if h_icon_big:
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, h_icon_big)
                    if h_icon_small:
                        ctypes.windll.user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, h_icon_small)
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        
        def apply_loop():
            for _ in range(12):
                time.sleep(0.4)
                ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)

        threading.Thread(target=apply_loop, daemon=True).start()
    except Exception:
        pass


def start_local_http_server(port=8080):
    """Fallback local HTTP server if PyWebView runs in headless/browser mode."""
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

    print("⚡ Starting Mr. Drew's Device & FPS Optimizer (HTML5/CSS3/JS Web UI)...")
    set_windows_app_icon(icon_ico)

    if HAS_WEBVIEW:
        try:
            window = webview.create_window(
                "Mr. Drew's Device & FPS Optimizer",
                url=html_path,
                js_api=api,
                width=1160,
                height=840,
                min_size=(980, 720),
                background_color="#030712"
            )
            webview.start(debug=False)
            return
        except Exception as e:
            print(f"[WEBVIEW WARNING] Native WebView window launch failed: {e}")
            print("[WEBVIEW FALLBACK] Launching local Web Server & Browser Window...")

    # Fallback to local HTTP server + default browser launch
    port = 8080
    t = threading.Thread(target=start_local_http_server, args=(port,), daemon=True)
    t.start()
    time.sleep(0.5)
    webbrowser.open(f"http://127.0.0.1:{port}/index.html")
    print(f"Server running at http://127.0.0.1:{port}/index.html. Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Application stopped.")


if __name__ == "__main__":
    main()
