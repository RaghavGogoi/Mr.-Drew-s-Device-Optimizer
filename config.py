import os
import json
from typing import Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "first_run_completed": False,
    "auto_guard_enabled": False,
    "auto_guard_interval_sec": 60,
    "theme": "obsidian",
    "sound_effects": True,
    "high_priority_game": ""
}


def load_config() -> Dict[str, Any]:
    """Loads configuration from config.json, creating defaults if missing."""
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all default keys exist
            config = DEFAULT_CONFIG.copy()
            config.update(data)
            return config
    except Exception:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any]) -> bool:
    """Saves configuration dictionary to config.json safely."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception:
        return False


def is_first_run() -> bool:
    """Returns True if the app is being run for the first time."""
    cfg = load_config()
    return not cfg.get("first_run_completed", False)


def set_first_run_completed(completed: bool = True) -> bool:
    """Updates the first_run_completed flag in config.json."""
    cfg = load_config()
    cfg["first_run_completed"] = completed
    return save_config(cfg)


def reset_first_run() -> bool:
    """Resets first run status to True so tutorial plays again on next launch."""
    return set_first_run_completed(False)
