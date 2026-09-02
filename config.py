import os
import json
from typing import Dict, Any

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
    "sound_volume": 0.08
}

def load_config() -> Dict[str, Any]:
    """Loads configuration from config.json, merging with defaults if missing."""
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(data)
            return merged
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config_dict: Dict[str, Any]) -> bool:
    """Saves dictionary to config.json."""
    try:
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
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG.copy()

def is_first_run() -> bool:
    return not load_config().get("first_run_completed", False)

def set_first_run_completed(completed: bool = True) -> bool:
    return update_setting("first_run_completed", completed)

def reset_first_run() -> bool:
    return update_setting("first_run_completed", False)
