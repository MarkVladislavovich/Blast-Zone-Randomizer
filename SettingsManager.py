import json
import os


class SettingsManager:
    def __init__(self, file_path="settings.json"):
        self.file_path = file_path
        self.settings = self._load_settings()

        # --- [ INTERNAL ] ---
    def _load_settings(self):
        # Loads settings from JSON file, create default if missing, or you stuffed something up
        defaults = {
            "enable_reskins": False,
            "enable_empty": False,
            "multi_empty": False,
            "multi_chance": 0.2,
            "slot_amount": 4,
            "hotkey_slot": 1
        }

        if not os.path.exists(self.file_path):
            # Default settings
            self.settings = defaults
            self._save_settings()
            print(f"[INFO] Created default settings at {self.file_path}")
            return defaults
        try:
            with open(self.file_path, "r") as f:
                settings = json.load(f)
            # Merges the missing keys
            for key, value in defaults.items():
                if key not in settings:
                    settings[key] = value

            self.settings = settings
            self._save_settings()
            return settings

        except json.JSONDecodeError:
            print("[ERROR] Unable to parse settings.json. Reverting to default.")
            self.settings = defaults
            self._save_settings()
            return defaults

    def _save_settings(self):
        # Writes current settings into a JSON file.
        with open(self.file_path, "w") as f: # noinspection PyTypeChecker
            json.dump(self.settings, f, indent=4)


        # --- [ EXTERNAL ] ---
    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
       self.settings[key] = value
       self._save_settings()

    def list_settings(self):
        # Prints all the settings for debugging
        print("n\nCurrent Settings:")
        for key, value in self.settings.items():
            print(f"- {key}: {value}")
        return self.settings

    # Handles Multi-Empty function and updates accordingly.
    # Cycles between three states: Red > Green > Gold > Red.
    def cycle_empty_mode(self):

        empty = self.settings.get_setting("enable_empty")
        multi = self.settings.get_setting("multi_empty")

        if not empty and not multi:
            # Red >>> Green
            self.settings["enable_empty"] = True
            self.settings["multi_empty"] = False
            mode = "Empty"
        elif empty and not multi:
            # Green >>> Gold
            self.settings["enable_empty"] = True
            self.settings["multi_empty"] = True
            mode = "Multi-Empty"
        else:
            # Gold >>> Red
            self.settings["enable_empty"] = False
            self.settings["multi_empty"] = False
            mode = "Disabled"

        self.ui.btn_enable_empty.config(text=f"Empty Mode: {mode}")

        self.ui.btn_enable_empty.config(highlightbackground=self.empty_colours[mode], highlightthickness=4)

