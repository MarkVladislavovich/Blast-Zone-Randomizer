import random
import json
import time
from SettingsManager import SettingsManager

class Randomizer:
    def __init__(self, settings_manager, blacklist_manager):
        self.settings = settings_manager
        self.blacklist = blacklist_manager

    def generate_loadout(self):
        all_weapons = self.blacklist.get_allowed_weapons()

        slot_count = min(self.settings.slot_amount, 5)  # Forces slot_count to a maximum of 5
        allow_reskins = self.settings.enable_reskins
        allow_empty = self.settings.enable_empty
        multi_empty = self.settings.multi_empty
        multi_chance = self.settings.multi_chance

        filtered = [    # Filter weapons based on the settings
            w for w in all_weapons
            if (allow_reskins or not w["reskin"])
            and (allow_empty or w.get("type", "weapon") != "None")
            and not w.get("blacklisted", False)
    ]
        # Separates empty shit from non-empty shit
        empty_weapon = [w for w in filtered if w.get("type") == "None"]
        non_empty = [w for w in filtered if w.get("type") != "None"]

        loadout = []

        for _ in range(slot_count):
            if multi_empty and empty_weapon and random.random() < multi_chance:
                loadout.append(random.choice(empty_weapon))

            else:
                if non_empty:
                    choice = random.choice(non_empty)
                    loadout.append(choice["name"])
                    non_empty.remove(choice)
                elif empty_weapon:
                    loadout.append(random.choice(empty_weapon)["name"])

        return loadout