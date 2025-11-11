import random

class Randomizer:
    def __init__(self, settings_manager, blacklist_manager):
        self.settings = settings_manager
        self.blacklist = blacklist_manager

    def generate_loadout(self):
        all_weapons = self.blacklist.get_allowed_weapons()

        slot_count = min(self.settings.get_setting("slot_amount"),5)
        allow_reskins = self.settings.get_setting("enable_reskins")
        allow_empty = self.settings.get_setting("enable_empty")
        multi_empty = self.settings.get_setting("multi_empty")
        multi_chance = self.settings.get_setting("multi_chance")

        filtered = [    # Filter weapons based on the settings
            w for w in all_weapons
            if (allow_reskins or not w.get("reskin", False))
                and (allow_empty or w.get("type", "weapon") != "None")  # <<< Use get() for optional "type"
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

        result = []
        for w in loadout:
            if isinstance(w,dict):
                result.append(f"{w['name']} ({w.get('rarity','')})")
            else:
                result.append(str(w))
        return result