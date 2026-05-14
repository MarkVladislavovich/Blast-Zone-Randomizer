import json
import os


def deep_merge(default, incoming): # This is for _load_settings for the new nested format.
    # This basically makes sure the missing keys are filled in without flattening nested settings.
    for key, value in default.items():

        if key not in incoming:  # If the key isn't in file, it'll inject the missing parts with the defaults.
            incoming[key] = value

        # Makes sure if both values are dictionaries, it'll merge them properly
        elif isinstance(value, dict) and isinstance(incoming[key], dict):
            deep_merge(value, incoming[key])

    return incoming

class SettingsManager:
    def __init__(self, file_path="configs/settings.json"):
        self.file_path = file_path
        self.settings = self._load_settings()


        self.ui = None
        self.empty_colours = {}

        # allows UI to bind
        # Lets Main_UI work with UI controls
    def bind_ui(self, ui, empty_colours):
        self.ui = ui
        self.empty_colours = empty_colours

    def _load_settings(self):
        # Loads settings from JSON file, create default if missing, or you stuffed something up
        defaults = {
            "Randomizer_Settings": {
                "enable_reskins": True,
                "enable_empty": False,
                "multi_empty": False,
                "multi_chance": 0.5,
                "slot_amount": 5,
                "disable_fifth_slot": False
            },
            "UI_Effects": {
                "fish_mode": False,
                "explosion_mode": False,
                "always_explode": False
            },
            "Misc_Settings": {
                "true_scaling": False,
                "hotkey_slot": 1
            }
        }

        if not os.path.exists(self.file_path):
            # Default settings
            self.settings = defaults
            self._save_settings()
            # print(f"[INFO] Created default settings at {self.file_path}")
            return defaults
        try:
            with open(self.file_path, "r") as f:
                settings = json.load(f)

            settings = deep_merge(defaults, settings)

            self.settings = settings
            self._save_settings()
            return settings

        except json.JSONDecodeError:
            # print("[ERROR] Unable to parse settings.json. Reverting to default.")
            self.settings = defaults
            self._save_settings()
            return defaults

    def _save_settings(self):
        # Writes current settings into a JSON file.
        with open(self.file_path, "w") as f: # noinspection PyTypeChecker
            json.dump(self.settings, f, indent=4)

    def get_setting(self, section, key):
        # Grabs and returns the value of a setting
        return self.settings.get(section,{}).get(key)

    def set_setting(self, section, key, value):
        if section not in self.settings:
            self.settings[section] = {}

        self.settings[section][key] = value
        self._save_settings()

    def list_settings(self):
        # Prints all the settings for debugging
        print("\n\nCurrent Settings:")
        for key, value in self.settings.items():
            print(f"- {key}: {value}")
        return self.settings