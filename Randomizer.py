import random


class Randomizer:
    def __init__(self, settings_manager, blacklist_manager):
        self.settings = settings_manager
        self.blacklist = blacklist_manager

    def generate_loadout(self):
        all_weapons = self.blacklist.get_allowed_weapons()

        slot_count = min(self.settings.get_setting("slot_amount"),5)

        if self.settings.get_setting("disable_fifth_slot"):
            slot_count = min(slot_count, 4) # Limits to 4 slots for disabling 5th slot

        allow_reskins = self.settings.get_setting("enable_reskins")
        enable_empty = self.settings.get_setting("enable_empty")
        multi_empty = self.settings.get_setting("multi_empty")
        multi_chance = self.settings.get_setting("multi_chance")

        filtered = [    # Filters weapons based on the settings
            w for w in all_weapons
            if (allow_reskins or not w.get("reskin", False))
                and not w.get("blacklisted", False)
        ]

        # Separates empty shit from non-empty shit
        empty_weapon = [w for w in filtered if w.get("type") == "None"]
        non_empty = [w for w in filtered if w.get("type") != "None"]

        loadout = []

        # Sees what slots are empty
        empty_slots = [False] * slot_count
        if enable_empty and not multi_empty and slot_count > 0:
            # Single picks only 1 random slot
            idx = random.randint(0, slot_count-1)
            empty_slots[idx] = True
        elif enable_empty and multi_empty:
            # Multi allows any slot to be empty
            for i in range(slot_count):
                if random.random() < multi_chance:
                    empty_slots[i] = True
        # Disabled doesn't need code since its off, duh.

        # Fix for the empty slot shit, I can't remember its late. -M 14/11/25 2:31am
        for i in range(slot_count):
            if empty_slots[i] and empty_weapon:
                loadout.append(random.choice(empty_weapon))
            else:
                if non_empty:
                    choice = random.choice(non_empty)
                    loadout.append(choice)
                    non_empty.remove(choice)
                elif empty_weapon:
                    loadout.append(random.choice(empty_weapon))

        # Converts to strings for displaying
        result = []
        for w in loadout:
            if isinstance(w,dict):
                result.append(f"{w['name']} ({w.get('rarity','')})")
            else:
                result.append(str(w))
        return result

    def reroll(self, slot_index):
        loadout = self.generate_loadout()
        if slot_index < len(loadout):
            return loadout[slot_index]
        return "I can't find any :c"


        # The amount of times I had to rewrite this bastard is absurd.