import sys
import platform
from pathlib import Path

def get_app_data_dir() -> Path:
    system = platform.system()
    if system == "Windows":
        return Path.home() / "AppData" / "Roaming" / "SmartTranslateAi"
    elif system == "Darwin":
        return Path.home() / "Library" / "Application Support" / "SmartTranslateAi"
    else:
        return Path.home() / ".config" / "smarttranslateai"

def is_android() -> bool:
    return "android" in platform.system().lower() or hasattr(sys, 'getandroidapilevel')