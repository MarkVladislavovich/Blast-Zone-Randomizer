# This will allow BlacklistManager to load and save Presets


# Presets will be structured like this:
# | Preset Name | Load | Save | Delete |

class PresetManager:
    def __init__(self, preset_file="presets.json"):
        self.preset_file = preset_file
        self.presets = {}
        self.current_preset_name = "Default"
        self.load_presets()


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
        # Recycle the def clear_blacklist from BlacklistManager
        pass

    def save_preset(self):
        # Ask for Confirmation
            # Y: Override Preset list
            # N: Pass
        pass

    def delete_preset(self):
        # Ask for Confirmation
            # Y: Delete data + Remove Preset from list
            # N: Pass
        pass

    def add_weapon_to_preset(self):
        # Weapon box is ticked
        # Add weapon to list
        pass

    def remove_weapon_from_preset(self):
        # Weapon is unticked from box
        # Remove weapon from list
        pass


    if __name__ == "__main__":
        print("[DEBUG START] PresetManager Test...")

pm = PresetManager("presets.json")
print(f"[FINAL PRESET DEBUG] Loaded Presets: {pm.presets}")
print(f"[FINAL PRESET DEBUG] Active Preset: {pm.current_preset_name}")
print(f"[FINAL PRESET DEBUG] Active Blacklist {pm.active_preset()}")



