"""
=============================================================================
MR. DREW'S DEVICE OPTIMIZER - COMPREHENSIVE AUTOMATED TEST SUITE
=============================================================================
Verifies OptimizerCore, Api Bridge, Config Persistence, and Native C++ Engine.
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
import subprocess

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config
from optimizer_core import OptimizerCore, SYSTEM_WHITELIST, KNOWN_GAME_PROCESSES
from app import Api

_ORIGINAL_CONFIG_PATH = config.CONFIG_PATH
_TEST_TEMP_DIR = None


def setUpModule():
    """Isolate config.json writes to a temporary directory outside %TEMP% during test execution."""
    global _TEST_TEMP_DIR
    _TEST_TEMP_DIR = tempfile.mkdtemp(prefix=".test_cfg_", dir=PROJECT_ROOT)
    config.CONFIG_PATH = os.path.join(_TEST_TEMP_DIR, "config.json")
    config.reset_to_defaults()


def tearDownModule():
    """Restore original config path and remove temporary test directory."""
    config.CONFIG_PATH = _ORIGINAL_CONFIG_PATH
    if _TEST_TEMP_DIR and os.path.exists(_TEST_TEMP_DIR):
        shutil.rmtree(_TEST_TEMP_DIR, ignore_errors=True)


class TestConfig(unittest.TestCase):
    """Verifies configuration loading, updating, and saving."""

    def test_load_config(self):
        cfg = config.load_config()
        self.assertIsInstance(cfg, dict)
        self.assertIn("theme", cfg)
        self.assertIn("continuous_interval_sec", cfg)

    def test_update_and_save_setting(self):
        original_theme = config.load_config().get("theme", "obsidian")
        try:
            ok = config.update_setting("theme", "emerald")
            self.assertTrue(ok)
            updated_cfg = config.load_config()
            self.assertEqual(updated_cfg.get("theme"), "emerald")
        finally:
            config.update_setting("theme", original_theme)


class TestOptimizerCore(unittest.TestCase):
    """Verifies optimization routines, system metrics, and safety whitelists."""

    @classmethod
    def setUpClass(cls):
        cls.core = OptimizerCore()

    def test_system_specs(self):
        specs = self.core.get_system_specs()
        self.assertIsInstance(specs, dict)
        self.assertIn("total_ram_gb", specs)
        self.assertIn("avail_ram_gb", specs)
        self.assertIn("percent_used", specs)
        self.assertIn("cpu_percent", specs)
        self.assertIn("standby_ram_gb", specs)
        self.assertGreater(specs["total_ram_gb"], 0)
        self.assertGreater(specs["avail_ram_gb"], 0)
        self.assertGreaterEqual(specs["standby_ram_gb"], 0)

    def test_hardware_details_and_caching(self):
        hw = self.core.get_hardware_details()
        self.assertIsInstance(hw, dict)
        self.assertIn("cpu_cores_logical", hw)
        self.assertIn("gpu_vendor", hw)
        self.assertIn("device_profile", hw)
        self.assertGreater(hw["cpu_cores_logical"], 0)

        # Verify caching: second call should be fast and consistent
        hw2 = self.core.get_hardware_details()
        self.assertEqual(hw["gpu_vendor"], hw2["gpu_vendor"])

    def test_timer_resolution(self):
        cur_res, min_res = self.core.get_timer_resolution_ms()
        self.assertGreater(cur_res, 0.0)
        self.assertGreater(min_res, 0.0)

    def test_standby_ram_bytes(self):
        standby_bytes = self.core.get_standby_ram_bytes()
        self.assertIsInstance(standby_bytes, int)
        self.assertGreaterEqual(standby_bytes, 0)

    def test_top_ram_processes(self):
        procs = self.core.get_top_ram_processes(count=5)
        self.assertIsInstance(procs, list)
        if procs:
            first = procs[0]
            self.assertIn("pid", first)
            self.assertIn("name", first)
            self.assertIn("mem_mb", first)
            self.assertGreater(first["mem_mb"], 0)

    def test_system_whitelist_protection(self):
        os_name = self.core.os_type
        whitelist = SYSTEM_WHITELIST.get(os_name, set())
        self.assertIn("explorer.exe" if os_name == "windows" else "systemd" if os_name == "linux" else "finder", whitelist)
        self.assertIn("deviceoptimizer.exe" if os_name == "windows" else "python3" if os_name == "linux" else "python3", whitelist)

    def test_shader_cache_cleaning(self):
        cleaned_bytes, msg = self.core.clean_gpu_shader_cache()
        self.assertIsInstance(cleaned_bytes, int)
        self.assertIsInstance(msg, str)
        self.assertGreaterEqual(cleaned_bytes, 0)

    def test_temp_file_cleaning(self):
        cleaned_bytes, msg = self.core.clear_temp_files()
        self.assertIsInstance(cleaned_bytes, int)
        self.assertIsInstance(msg, str)
        self.assertGreaterEqual(cleaned_bytes, 0)

    def test_trim_process_working_sets(self):
        processed, succeeded = self.core.trim_process_working_sets()
        self.assertGreaterEqual(processed, 0)
        self.assertGreaterEqual(succeeded, 0)

    def test_high_performance_power_plan(self):
        ok, msg = self.core.enable_high_performance_power_plan()
        self.assertTrue(ok)
        self.assertIsInstance(msg, str)

    def test_continuous_mode_lifecycle(self):
        ok, msg = self.core.start_continuous_mode(interval_sec=5, mode="gaming")
        self.assertTrue(ok)
        self.assertTrue(self.core.is_continuous_active())

        status = self.core.get_continuous_status()
        self.assertTrue(status["is_running"])
        self.assertEqual(status["mode"], "gaming")

        ok_stop, stop_msg = self.core.stop_continuous_mode()
        self.assertTrue(ok_stop)
        self.assertFalse(self.core.is_continuous_active())


class TestApiBridge(unittest.TestCase):
    """Verifies that all API methods exposed to PyWebView return expected structures."""

    @classmethod
    def setUpClass(cls):
        cls.api = Api()

    def test_api_system_specs(self):
        specs = self.api.get_system_specs()
        self.assertIn("total_ram_gb", specs)
        self.assertIn("avail_ram_gb", specs)

    def test_api_diagnostics(self):
        diag = self.api.export_diagnostics()
        self.assertIsInstance(diag, str)
        self.assertIn("MR. DREW'S DEVICE OPTIMIZER", diag)
        self.assertIn("Physical RAM", diag)

    def test_api_guide_steps(self):
        steps = self.api.get_guide_steps()
        self.assertIsInstance(steps, list)
        self.assertGreaterEqual(len(steps), 10)
        first = steps[0]
        self.assertIn("title", first)
        self.assertIn("how", first)
        self.assertIn("why", first)
        self.assertIn("when", first)

    def test_api_execute_actions(self):
        res1 = self.api.execute_action("trim_working_sets")
        self.assertIn("logs", res1)

        res2 = self.api.execute_action("clean_shader_cache")
        self.assertIn("logs", res2)

        res3 = self.api.execute_action("boost_process", os.getpid())
        self.assertIn("logs", res3)

    def test_monster_alias(self):
        res = self.api.core.run_monster_optimizer()
        self.assertIn("logs", res)
        self.assertIn("reclaimed_mb", res)

    def test_rest_api_server_endpoints(self):
        import urllib.request
        from app import start_local_http_server
        port = start_local_http_server(self.api, preferred_port=8990)
        self.assertGreater(port, 0)

        # Test GET /api/specs
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/specs")
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("total_ram_gb", data)

        # Test GET /api/config
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/config")
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("theme", data)

        # Test POST /api/execute_action
        post_data = json.dumps({"action_id": "trim_working_sets", "extra_arg": None}).encode("utf-8")
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/execute_action", data=post_data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("logs", data)

        # Test GET /api/account
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/account", timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            account_data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("username", account_data)

        # Test GET /api/security_audit
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/security_audit", timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            sec_data = json.loads(resp.read().decode("utf-8"))
            self.assertIn("security_score", sec_data)
            self.assertIn("security_grade", sec_data)

        # Test POST /api/feedback
        fb_post = json.dumps({"type": "bug", "title": "Test Bug", "description": "Unit test report"}).encode("utf-8")
        fb_req = urllib.request.Request(f"http://127.0.0.1:{port}/api/feedback", data=fb_post, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(fb_req, timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            fb_res = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(fb_res.get("status"))

        # Test GET /api/feedback_history
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/feedback_history", timeout=5) as resp:
            self.assertEqual(resp.status, 200)
            history_data = json.loads(resp.read().decode("utf-8"))
            self.assertIsInstance(history_data, list)
            self.assertGreaterEqual(len(history_data), 1)


class TestUserAccountAndSecurity(unittest.TestCase):
    """Verifies guest-first account system, security audit, and feedback management."""

    def setUp(self):
        self.core = OptimizerCore()
        self.api = Api()

    def test_guest_account_default(self):
        info = config.get_account_info()
        self.assertIsInstance(info, dict)
        self.assertIn("username", info)
        self.assertIn("avatar", info)
        self.assertIn("is_guest", info)
        self.assertTrue(info["is_guest"])
        self.assertIn("total_optimizations", info)
        self.assertIn("total_ram_reclaimed_gb", info)

    def test_update_account_info(self):
        original = config.get_account_info().copy()
        try:
            ok = config.update_account_info({"username": "CyberAgent", "avatar": "⚡"})
            self.assertTrue(ok)
            updated = config.get_account_info()
            self.assertEqual(updated["username"], "CyberAgent")
            self.assertEqual(updated["avatar"], "⚡")
        finally:
            config.update_account_info(original)

    def test_record_optimization_stat(self):
        before = config.get_account_info()
        before_runs = before.get("total_optimizations", 0)
        before_ram = before.get("total_ram_reclaimed_gb", 0.0)

        config.record_optimization_stat(1.25)
        after = config.get_account_info()
        self.assertEqual(after.get("total_optimizations"), before_runs + 1)
        self.assertAlmostEqual(after.get("total_ram_reclaimed_gb"), before_ram + 1.25, places=1)

    def test_switch_profile(self):
        res = config.switch_profile("esports")
        self.assertTrue(res["status"])
        self.assertIn(config.get_account_info().get("active_profile_id"), ["esports", "profile_esports"])

        # Switch back to guest default
        res_back = config.switch_profile("guest")
        self.assertTrue(res_back["status"])
        self.assertIn(config.get_account_info().get("active_profile_id"), ["guest", "default", "profile_guest"])

    def test_audit_system_security(self):
        audit = self.core.audit_system_security()
        self.assertIsInstance(audit, dict)
        self.assertIn("security_score", audit)
        self.assertIn("security_grade", audit)
        self.assertIn("checks", audit)
        self.assertIn("suspicious_processes", audit)
        self.assertGreaterEqual(audit["security_score"], 60)
        self.assertIn(audit["security_grade"], ["A+", "A", "B", "C"])
        self.assertGreaterEqual(len(audit["checks"]), 4)

        check_names = [c["name"] for c in audit["checks"]]
        self.assertIn("Process Whitelist Immunity", check_names)
        self.assertIn("Path Sanitization & Traversal Barrier", check_names)
        self.assertIn("Real-Time Antivirus Protection", check_names)

    def test_path_sanitization_barrier(self):
        # Must reject parent directory traversal
        self.assertFalse(self.core._is_safe_clean_path("../system32"))
        self.assertFalse(self.core._is_safe_clean_path("C:\\Windows\\..\\Windows"))
        self.assertFalse(self.core._is_safe_clean_path(""))
        # Must reject root
        self.assertFalse(self.core._is_safe_clean_path("C:\\"))
        self.assertFalse(self.core._is_safe_clean_path("C:\\Windows"))
        # Must allow valid temp folder
        temp_dir = os.environ.get("TEMP", "")
        if temp_dir and os.path.exists(temp_dir):
            self.assertTrue(self.core._is_safe_clean_path(temp_dir))

    def test_feedback_save_and_retrieve(self):
        entry = {
            "type": "feature",
            "title": "Add Auto-Game Priority",
            "description": "Automatically prioritize Steam games on launch.",
            "category": "Gaming",
            "severity": "Enhancement"
        }
        ok = config.save_feedback_entry(entry)
        self.assertTrue(ok)
        history = config.get_feedback_history()
        self.assertIsInstance(history, list)
        self.assertGreaterEqual(len(history), 1)
        self.assertEqual(history[0]["title"], "Add Auto-Game Priority")
        self.assertIn("timestamp", history[0])


class TestNativeEngine(unittest.TestCase):
    """Verifies that the compiled C++ executable and shared library handle functions correctly."""

    def test_cpp_binary_help(self):
        binary = os.path.join(PROJECT_ROOT, "DeviceOptimizer.exe" if sys.platform == "win32" else "DeviceOptimizer")
        if not os.path.exists(binary):
            self.skipTest("C++ binary not found.")
        
        proc = subprocess.run([binary, "--help"], capture_output=True, text=True, timeout=5)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Usage: DeviceOptimizer", proc.stdout)

    def test_cpp_binary_version(self):
        binary = os.path.join(PROJECT_ROOT, "DeviceOptimizer.exe" if sys.platform == "win32" else "DeviceOptimizer")
        if not os.path.exists(binary):
            self.skipTest("C++ binary not found.")
        
        proc = subprocess.run([binary, "--version"], capture_output=True, text=True, timeout=5)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Native Engine", proc.stdout)

    def test_cpp_dll_in_process_bridge(self):
        if sys.platform != "win32":
            self.skipTest("DLL bridge tests are Windows-specific.")
        core = OptimizerCore()
        if not core.cpp_dll:
            self.skipTest("device_optimizer.dll not found or could not be loaded.")
        
        self.assertIsNotNone(core.cpp_dll)
        hw = core.get_hardware_details()
        self.assertTrue(hw.get("cpp_dll_active", False))

        # Test C_GetMemoryMetrics
        specs = core.get_system_specs()
        self.assertGreater(specs["total_ram_gb"], 0)
        self.assertGreater(specs["avail_ram_gb"], 0)
        self.assertGreater(specs["standby_ram_gb"], 0)

        # Test C_GetTopProcessesJson
        procs = core.get_top_ram_processes(count=3)
        self.assertIsInstance(procs, list)
        self.assertGreaterEqual(len(procs), 1)
        self.assertIn("name", procs[0])
        self.assertIn("mem_mb", procs[0])

        # Test C_LockHighPrecisionTimer
        timer_ok = core.set_windows_timer_resolution(True)
        self.assertTrue(timer_ok)
        cur, min_r = core.get_timer_resolution_ms()
        self.assertGreater(cur, 0.0)
        self.assertGreater(min_r, 0.0)


if __name__ == "__main__":
    unittest.main()
