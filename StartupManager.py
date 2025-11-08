import json
import os
import sys
from SettingsManager import SettingsManager

# First checks if Settings.json is not missing.
def check_settings():
    print("[STARTUP] Locating settings.json...")
    settings = SettingsManager("settings.json")
    if os.path.exists("settings.json"):
        print("[INFO] setting.json found!")
    else:
        print("[WARNING] settings.json failed to validate, reset to defaults.")
    return settings

# Then checks if weapons.json is not missing.
def load_weapons(file_path="weapons.json"):
    if not os.path.exists(file_path): # Failsafe 1 for if file is not found.
        print(f"[ERROR] Missing file: {file_path}")
        print("Make sure all files are validated.")
        print("Press Enter to exit...")
        sys.exit(1)
    try:
        # Attempting to open & parse the weapon.json file.
        with open(file_path, "r") as f:
            weapons = json.load(f)
        print(f"Successfully loaded {len(weapons)} weapons successfully")
        return weapons

    except json.JSONDecodeError as e: # Failsafe 2 for if the .json is an invalid format
        print(f"[ERROR] Could not parse JSON: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    load_weapons()

