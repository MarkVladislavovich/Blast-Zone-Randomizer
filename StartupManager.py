import json
import os
import sys
from SettingsManager import SettingsManager


# --- Pillow Check --- (NEEDED FOR UI)
def check_pillow():
    # Checks if Pillow is installed, if not PillowAutoInstaller triggers an install prompt.
    try:
        from PIL import Image, ImageTk
        print("[INFO] Successfully located Pillow Library.")
        return True
    except ImportError:
        print("[ERROR] Pillow library unable to be located.")
        try:
            from PillowAutoInstaller import pillow_prompt
            installed = pillow_prompt() # Returns true if the installation successfully succeeds.
            if installed:
                print("[INFO] Pillow installed successfully, Thank you! continuing startup... ")
                return True
            else:
                print("[ERROR] Pillow Installation Cancelled. Exiting...")
                sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Failed to run Pillow installer: {e}")
            sys.exit(1)

# --- Settings Check ---

def check_settings(): # Checks if the Settings.json file is not missing
    print("[STARTUP] Locating settings.json...")
    if not os.path.exists("settings.json"):
        print("[WARNING] settings.json failed to validate, reset to defaults.")
    settings = SettingsManager("settings.json")
    print("[INFO] settings.json loaded!")
    return settings

# --- Weapon List Check ---

# Then checks if weapons.json is not missing.
def load_weapons(file_path="weapons.json"):
    print("[STARTUP] Locating weapons.json...")
    if not os.path.exists(file_path): # Failsafe 1 for if file is not found.
        print(f"[ERROR] Missing file: {file_path}")
        print("Make sure all files are validated.")
        print("Press Enter to exit...")
        sys.exit(1)
    try:
        # Attempting to open & parse the weapon.json file.
        with open(file_path, "r") as f:
            weapons = json.load(f)
        print(f"[INFO] Successfully loaded {len(weapons)} weapons successfully!")
        return weapons

    except json.JSONDecodeError as e: # Failsafe 2 for if the .json is an invalid format
        print(f"[ERROR] Could not parse JSON: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

# --- Startup Sequence ---

def startup_checks():
    check_pillow()  # Checks Pillow.
    settings = check_settings()  # Then loads Settings.
    weapons = load_weapons()  # Immediately after loads Weapons.
    return settings, weapons

if __name__ == "__main__":
    settings, weapons = startup_checks()

