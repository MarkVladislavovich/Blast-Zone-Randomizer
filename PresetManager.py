import json
import os

# This will allow BlacklistManager to load and save Presets
from PIL.JpegPresets import presets

# Presets will be structured like this:
# | Preset Name | Load | Save | Delete |

class PresetManager:
    def __init__(self, preset_file="assets/configs/presets.json"):
        self.preset_file = preset_file
        self.presets = {}
        self.load_presets()

        if "Default" not in self.presets: # Failsafe that loads the default if it cannot find a Preset.
            self.presets["Default"] = {"blacklisted": []}

        self.current_preset_name = "Default"


    def load_presets(self):
        import json # loads the presets stored in presets.json
        try:
            with open(self.preset_file, "r") as f:
                self.presets = json.load(f)
        except FileNotFoundError:
            # If it cant find the file, it'll default.
            self.presets = {"Default": {"blacklisted": []}}

    def active_preset(self):
        # Check what preset is currently being used
        return self.presets.get(self.current_preset_name, {"blacklisted": []})

    def change_preset(self):
        # See what Preset (5 Slots) was interacted with
        # Save current Preset to its slot
        # Load selected Preset
        pass

    def create_preset(self):
        # Ask for Preset Name
        # Save currently applied Blacklist tags
        # Add new Preset to list w/ Name
        pass

    def reset_preset(self):
        self.active_preset()["blacklisted"] = []
        self._save_preset()

    def _save_preset(self):
        # Ask for Confirmation
            # Y: Override Preset list
            # N: Pass
        with open(self.preset_file, "w", encoding="utf-8") as f:
            json.dump(self.presets, f, indent=4)

    def delete_preset(self, preset_name: str):
        # Ask for Confirmation
        if preset_name in self.presets:
            del self.presets[preset_name]
            self._save_preset()
        else:
            print(f"[PRESET DEBUG] Preset: {preset_name} not found.")

    def add_weapon_to_preset(self, weapon_name: str):
        # Makes sure its editing the current preset
        preset = self.active_preset()
        blacklist = preset.get("blacklisted", [])
        if weapon_name not in blacklist:
            blacklist.append(weapon_name) # Adds weapon to list
            preset["blacklisted"] = blacklist
            self._save_preset() # Saves it to the current preset

    def remove_weapon_from_preset(self, weapon_name: str):
        # Weapon is unticked from box
        preset = self.active_preset()
        blacklist = preset.get("blacklisted", [])
        if weapon_name in blacklist:
            blacklist.remove(weapon_name)
            preset["blacklisted"] = blacklist
            self._save_preset()

    def is_blacklisted(self, weapon_name: str):
        # Checks if a weapon is currently in the blacklist preset
        preset = self.active_preset()
        blacklist = preset.get("blacklisted", [])
        return weapon_name in blacklist


    if __name__ == "__main__":
        print("[DEBUG START] PresetManager Test...")

pm = PresetManager("assets/configs/presets.json")
#print(f"[PRESET DEBUG1] Loaded Presets: {pm.presets}")
#print(f"[PRESET DEBUG2] Active Preset: {pm.current_preset_name}")
#print(f"[PRESET DEBUG3] Active Blacklist {pm.active_preset()}")



