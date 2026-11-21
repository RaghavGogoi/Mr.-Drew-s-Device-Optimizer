#!/usr/bin/env python3
"""
=============================================================================
MR. DREW'S DEVICE OPTIMIZER - UNIVERSAL CROSS-PLATFORM LAUNCHER
=============================================================================
Compatible with Windows, Linux, and macOS.
"""

import sys
import os
import platform
import subprocess

def print_banner():
    os_name = platform.system()
    print("=" * 64)
    print("   [+] MR. DREW'S DEVICE OPTIMIZER - UNIVERSAL LAUNCHER [+]")
    print(f"   Detected OS: {os_name} ({platform.release()}) | Python: {platform.python_version()}")
    print("=" * 64)

def check_dependencies():
    """Verify required python packages are installed."""
    required = ["psutil", "pywebview", "pystray", "PIL"]
    missing = []
    
    for pkg in required:
        try:
            if pkg == "pywebview":
                import webview
            elif pkg == "PIL":
                import PIL
            else:
                __import__(pkg)
        except ImportError:
            missing.append(pkg)
            
    if missing:
        print(f"[INFO] Missing dependencies: {', '.join(missing)}")
        print("[INFO] Attempting auto-installation via pip...")
        try:
            req_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
            if os.path.exists(req_file):
                cmd = [sys.executable, "-m", "pip", "install", "-r", req_file]
            else:
                cmd = [sys.executable, "-m", "pip", "install"] + missing
            subprocess.check_call(cmd)
            print("[SUCCESS] Dependencies successfully installed!")
        except Exception as e:
            print(f"[ERROR] Failed to install dependencies: {e}")
            print("Please run manually: pip install -r requirements.txt")

def compile_native_engine_if_available():
    """Compiles both standalone C++ executable and native shared library using g++ if present."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    main_cpp = os.path.join(base_dir, "main.cpp")
    
    if not os.path.exists(main_cpp):
        return
        
    system = platform.system().lower()
    binary_name = "DeviceOptimizer.exe" if system == "windows" else "DeviceOptimizer"
    binary_path = os.path.join(base_dir, binary_name)
    main_exe_path = os.path.join(base_dir, "main.exe") if system == "windows" else os.path.join(base_dir, "main")
    dll_name = "device_optimizer.dll" if system == "windows" else "libdevice_optimizer.so"
    dll_path = os.path.join(base_dir, dll_name)
    
    try:
        subprocess.check_call(["g++", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        return

    cpp_mtime = os.path.getmtime(main_cpp)
    need_exe = not os.path.exists(binary_path) or os.path.getmtime(binary_path) < cpp_mtime
    need_dll = not os.path.exists(dll_path) or os.path.getmtime(dll_path) < cpp_mtime

    if need_exe:
        try:
            print(f"[INFO] Compiling native C++ engine ({binary_name})...")
            if system == "windows":
                compile_cmd = ["g++", "-O3", "-std=c++17", main_cpp, "-o", binary_path, "-static", "-lpsapi", "-lwinmm", "-lpowrprof"]
            else:
                compile_cmd = ["g++", "-O3", "-std=c++17", main_cpp, "-o", binary_path]
            subprocess.check_call(compile_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if system == "windows":
                import shutil
                shutil.copyfile(binary_path, main_exe_path)
            else:
                os.chmod(binary_path, 0o755)
            print(f"[SUCCESS] Native C++ engine compiled successfully!")
        except Exception as e:
            print(f"[WARNING] Native C++ executable compilation failed: {e}")

    if need_dll:
        try:
            print(f"[INFO] Compiling native C++ shared library ({dll_name})...")
            if system == "windows":
                compile_cmd = ["g++", "-DBUILD_DLL", "-O3", "-std=c++17", "-shared", main_cpp, "-o", dll_path, "-static", "-lpsapi", "-lwinmm", "-lpowrprof"]
            else:
                compile_cmd = ["g++", "-DBUILD_DLL", "-O3", "-std=c++17", "-shared", "-fPIC", main_cpp, "-o", dll_path]
            subprocess.check_call(compile_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[SUCCESS] Native C++ shared library compiled successfully!")
        except Exception as e:
            print(f"[WARNING] Native C++ shared library compilation failed: {e}")

def main():
    if "--minimized" not in sys.argv:
        print_banner()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    
    check_dependencies()
    compile_native_engine_if_available()
    
    try:
        import app
        app.main()
    except KeyboardInterrupt:
        print("\n[INFO] Optimizer closed by user.")
    except Exception as e:
        print(f"[ERROR] Launch failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
