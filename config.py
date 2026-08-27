import os
import json
from typing import Dict, Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "first_run_completed": False,
    "tos_accepted": False,
    "auto_guard_enabled": False,
    "auto_guard_interval_sec": 60,
    "theme": "obsidian",  # obsidian, cosmic, emerald, amber, oled, frost
    "accent_color": "#00f0ff",
    "glass_effect": "high",  # high, subtle, none
    "glow_effects": True,
    "animation_speed": "normal",  # normal, fast, reduced
    "font_family": "Outfit",  # Outfit, Inter, JetBrains Mono
    "density": "spacious",  # spacious, compact
    "sound_effects": True,
    "target_free_ram_gb": 4.0,
    "game_boost_priority": "high",  # high, realtime
    "auto_clean_on_launch": False,
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
            config_data = DEFAULT_CONFIG.copy()
            config_data.update(data)
            return config_data
    except Exception:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(config_dict: Dict[str, Any]) -> bool:
    """Saves configuration dictionary to config.json safely."""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=4)
        return True
    except Exception:
        return False


def update_setting(key: str, value: Any) -> bool:
    """Updates a single setting key in config.json."""
    cfg = load_config()
    cfg[key] = value
    return save_config(cfg)


def reset_to_defaults() -> Dict[str, Any]:
    """Resets configuration to default settings."""
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()


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

