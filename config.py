import sys
import os
import json
import copy
from typing import Dict, Any

if getattr(sys, "frozen", False):
    CONFIG_PATH = os.path.join(os.path.dirname(sys.executable), "config.json")
else:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "first_run_completed": True,
    "tos_accepted": True,
    
    # Daemon & Performance Settings
    "continuous_enabled": False,
    "continuous_interval_sec": 30,
    "continuous_mode": "gaming",  # gaming, balanced, potato
    "target_free_ram_gb": 4.0,
    "continuous_timer_lock": True,
    "continuous_game_boost": True,
    "continuous_ram_guard": True,
    "auto_clean_standby_threshold_gb": 4.0,
    "run_on_startup": False,
    "close_to_tray": True,
    "notify_on_optimization": True,
    "low_power_mode": False,
    "custom_game_whitelist": ["Valorant.exe", "cs2.exe", "FortniteClient-Win64-Shipping.exe", "GTA5.exe", "Cyberpunk2077.exe", "League of Legends.exe", "Dota2.exe"],

    # Creative Design System & Themes
    "theme": "obsidian",
    "accent_color": "#00f0ff",
    "accent_secondary": "#a855f7",
    "custom_accent_active": False,
    "gradient_mode_active": True,
    
    # Dynamic Palette Swatches List
    "custom_palette_swatches": [
        "#00f0ff", "#10b981", "#c084fc", "#f59e0b", 
        "#fcee0a", "#ff2a85", "#ff1e42", "#38bdf8",
        "#00ff66", "#e11d48", "#8b5cf6", "#ff7300"
    ],
    
    # 14 Background Canvas Designs
    "bg_design": "matrix",         # matrix, tron_grid, vaporwave, tunnel, starfield, hex_shield, circuit, aurora, neural, wireframe, dna, visualizer, bokeh, solid
    "bg_fx_intensity": 0.70,       # 0.20 to 1.00
    "bg_fx_speed": 1.0,            # 0.0 to 3.0
    "bg_animated": True,
    "glow_effects": True,
    "glow_opacity": "0.22",
    
    # Glassmorphic Card Aesthetics
    "card_glass_opacity": "0.68",
    "glass_effect": "16px",
    "card_border_style": "glow",
    "card_hover_fx": "tilt",
    "corner_radius": "16px",
    
    # Typography & Interface
    "font_family": "'Outfit', sans-serif",
    "ui_density": "spacious",
    "text_glow": True,
    
    # Audio Soundscapes
    "sound_effects": True,
    "sound_theme": "cyber",
    "sound_volume": 0.08,

    # User Account & Profile System (Guest by default)
    "user_account": {
        "username": "Guest User",
        "avatar": "🎮",
        "account_type": "guest",
        "is_guest": True,
        "created_at": "2026-11-25",
        "pin_protected": False,
        "pin_code": "",
        "total_optimizations": 0,
        "total_ram_reclaimed_gb": 0.0,
        "custom_profiles": [
            {
                "id": "profile_guest",
                "name": "Guest Profile (Default)",
                "icon": "🎮",
                "mode": "gaming",
                "theme": "obsidian"
            },
            {
                "id": "profile_esports",
                "name": "Esports High-FPS Rig",
                "icon": "⚡",
                "mode": "gaming",
                "theme": "cyberpunk"
            },
            {
                "id": "profile_eco",
                "name": "Silent Eco & Battery",
                "icon": "🌱",
                "mode": "potato",
                "theme": "emerald"
            }
        ],
        "active_profile_id": "profile_guest"
    },

    # Security & Integrity Settings
    "security_settings": {
        "process_whitelist_enforced": True,
        "strict_path_validation": True,
        "prevent_critical_termination": True,
        "detect_suspicious_processes": True,
        "app_lock_enabled": False
    },

    # Local Reports & Suggestion History
    "feedback_history": []
}

def load_config() -> Dict[str, Any]:
    """Loads configuration from config.json, merging with defaults if missing."""
    if not os.path.exists(CONFIG_PATH):
        defaults = copy.deepcopy(DEFAULT_CONFIG)
        save_config(defaults)
        return defaults
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = copy.deepcopy(DEFAULT_CONFIG)
            merged.update(data)
            return merged
    except Exception:
        return copy.deepcopy(DEFAULT_CONFIG)

def save_config(config_dict: Dict[str, Any]) -> bool:
    """Saves dictionary to config.json."""
    try:
        parent = os.path.dirname(os.path.abspath(CONFIG_PATH))
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config_dict, f, indent=4)
        return True
    except Exception:
        return False

def update_setting(key: str, value: Any) -> bool:
    """Updates a single setting key."""
    cfg = load_config()
    cfg[key] = value
    return save_config(cfg)

def reset_to_defaults() -> Dict[str, Any]:
    """Resets entire configuration to factory default state."""
    defaults = copy.deepcopy(DEFAULT_CONFIG)
    save_config(defaults)
    return defaults

def is_first_run() -> bool:
    return not load_config().get("first_run_completed", False)

def set_first_run_completed(completed: bool = True) -> bool:
    return update_setting("first_run_completed", completed)

def reset_first_run() -> bool:
    return update_setting("first_run_completed", False)

# User Account & Profile Helpers
def get_account_info() -> Dict[str, Any]:
    """Retrieves current user account details and profile states."""
    cfg = load_config()
    account = cfg.get("user_account", {})
    if not isinstance(account, dict):
        account = copy.deepcopy(DEFAULT_CONFIG["user_account"])
    if "is_guest" not in account:
        account["is_guest"] = account.get("account_type", "guest") == "guest"
    return account

def update_account_info(account_dict: Dict[str, Any]) -> bool:
    """Updates account profile settings (username, avatar, pin, active profile)."""
    cfg = load_config()
    current = cfg.get("user_account", copy.deepcopy(DEFAULT_CONFIG["user_account"]))
    current.update(account_dict)
    cfg["user_account"] = current
    return save_config(cfg)

def record_optimization_stat(reclaimed_gb: float = 0.0) -> bool:
    """Increments total optimizations and lifetime memory freed counters."""
    cfg = load_config()
    account = cfg.get("user_account", copy.deepcopy(DEFAULT_CONFIG["user_account"]))
    account["total_optimizations"] = account.get("total_optimizations", 0) + 1
    current_reclaimed = account.get("total_ram_reclaimed_gb", 0.0)
    account["total_ram_reclaimed_gb"] = round(current_reclaimed + max(0.0, reclaimed_gb), 2)
    cfg["user_account"] = account
    return save_config(cfg)

def switch_profile(profile_id: str) -> Dict[str, Any]:
    """Switches active profile and applies profile settings (theme, continuous mode)."""
    cfg = load_config()
    account = cfg.get("user_account", copy.deepcopy(DEFAULT_CONFIG["user_account"]))
    profiles = account.get("custom_profiles", [])
    selected = None
    for p in profiles:
        p_id = p.get("id", "")
        if p_id == profile_id or p_id == f"profile_{profile_id}" or (profile_id and profile_id in p_id):
            selected = p
            break
    if selected:
        account["active_profile_id"] = selected.get("id")
        if "theme" in selected:
            cfg["theme"] = selected["theme"]
        if "mode" in selected:
            cfg["continuous_mode"] = selected["mode"]
        cfg["user_account"] = account
        save_config(cfg)
        return {"status": True, "profile": selected, "config": cfg}
    return {"status": False, "message": "Profile not found"}

def save_feedback_entry(entry: Dict[str, Any]) -> bool:
    """Saves a user feedback or bug report to local history."""
    cfg = load_config()
    history = cfg.get("feedback_history", [])
    import time
    entry["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    history.insert(0, entry)
    cfg["feedback_history"] = history[:50]  # keep latest 50 entries
    return save_config(cfg)

def get_feedback_history() -> list:
    """Returns local feedback submission history."""
    cfg = load_config()
    return cfg.get("feedback_history", [])
