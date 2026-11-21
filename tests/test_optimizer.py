"""
=============================================================================
MR. DREW'S DEVICE OPTIMIZER - COMPREHENSIVE AUTOMATED TEST SUITE
=============================================================================
Verifies OptimizerCore, Api Bridge, Config Persistence, and Native C++ Engine.
"""

import os
import sys
import unittest
import subprocess

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config
from optimizer_core import OptimizerCore, SYSTEM_WHITELIST, KNOWN_GAME_PROCESSES
from app import Api


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


class TestNativeEngine(unittest.TestCase):
    """Verifies that the compiled C++ executable handles flags correctly."""

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


if __name__ == "__main__":
    unittest.main()
