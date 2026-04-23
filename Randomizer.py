import random
from DebugManager import DebugManager # Used in Line 63 for printing output from Randomizer

class Randomizer:
    def __init__(self, blacklist_manager, settings_manager):
        self.blacklist = blacklist_manager
        self.settings = settings_manager

    def generate_loadout(self):
        all_weapons = self.blacklist.get_allowed_weapons()

        # Always generate 5 slots since this bastard got me stuck for several days.
        slot_count = 5

        allow_reskins = self.settings.get_setting("enable_reskins")
        enable_empty = self.settings.get_setting("enable_empty")
        multi_empty = self.settings.get_setting("multi_empty")
        multi_chance = self.settings.get_setting("multi_chance")

        filtered = [    # Filters weapons based on the settings
            w for w in all_weapons
            if (allow_reskins or not w.get("reskin", False))
        ]
        # Separates empty shit from non-empty stuff
        empty_weapon = [w for w in filtered if isinstance(w, dict) and w.get("type") == "None"]
        non_empty = [w for w in filtered if isinstance(w, dict) and w.get("type") != "None"]

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

        # Fix for the empty slot shit, I can't remember its late, im tired. -M 14/11/25 2:31am
        for i in range(slot_count):
            # Handle 5th slot disabled
            if i == 4 and self.settings.get_setting("disable_fifth_slot"):
                loadout.append("[Disabled]")
                continue

            if empty_slots[i] and empty_weapon:
                loadout.append(random.choice(empty_weapon))
            else:
                if non_empty:
                    choice = random.choice(non_empty)
                    loadout.append(choice)
                    non_empty.remove(choice)
                elif empty_weapon:
                    loadout.append(random.choice(empty_weapon))

        # Logs the result for the debugger         <<<< After DebugManager is made please toggle this me
       # DebugManager.log(f"[Randomizer] loadout={loadout}")

        # Used to Converts to strings for displaying
        return loadout

    def reroll(self, slot_index, current_loadout):

        if slot_index == 4 and self.settings.get_setting("disable_fifth_slot"):
            return "…ᘛ⁐̤ᕐᐷ"

        allow_reskins = self.settings.get_setting("enable_reskins")
        enable_empty = self.settings.get_setting("enable_empty")
        multi_empty = self.settings.get_setting("multi_empty")

        # Gives weapon list again
        all_weapons = self.blacklist.get_allowed_weapons()

        filtered = [
            w for w in all_weapons
            if (allow_reskins or not w.get("reskin", False))
                and not w.get("blacklisted", False)
        ] # This separates all the blacklisted weapons and Reskin weapons based on settings.

        # Separates empties
        non_empty = [w for w in filtered if w.get("type") != "None"]
        empty_weapon = [w for w in filtered if w.get("type") == "None"] if enable_empty else []

        # builds list so reroll doesn't stupidly choose another item already in the list
        empty_names = [f"{w['name']} ({w.get('rarity', '')})" for w in empty_weapon]

        # Funny easter egg
        if slot_index >= len(current_loadout) or current_loadout[slot_index] == "[DISABLED]":
            return "…ᘛ⁐̤ᕐᐷ"
        if not enable_empty and current_loadout[slot_index] in empty_names:
            return "…ᘛ⁐̤ᕐᐷ"

        other_items = []
        for i, item in enumerate(current_loadout):
            if i == slot_index:
                continue

            if multi_empty and item in empty_names:
                # Fixes Multi-Empty
                continue
            if item != "[DISABLED]":
                other_items.append(item)

        # Filters already used items to avoid duplicates
        available_items = []
        for w in non_empty + empty_weapon:
            w_name = f"{w['name']} ({w.get('rarity','')})" if isinstance(w, dict) else str(w)
            if w_name not in other_items:
                available_items.append(w)

        if not available_items:
            # Fallback incase the pool is empty
            return current_loadout[slot_index]

        # Picks new item that is not in the table already
        choice = random.choice(available_items)
        result = f"{choice['name']} ({choice.get('rarity','')})" if isinstance(choice, dict) else str(choice)

        return result

    # Also yes this is the randomizer logic re-used.

    if __name__ == "__main__":
        from BlacklistManager import BlacklistManager
        from PresetManager import PresetManager
        from SettingsManager import SettingsManager
        from AssetManager import AssetManager
        from Randomizer import Randomizer

        # Creating managers for testing
        asset_manager = AssetManager()
        settings_manager = SettingsManager("settings.json")
        preset_manager = PresetManager("preset.json")
        blacklist_manager = BlacklistManager(asset_manager, preset_manager)

        randomiser = Randomizer(blacklist_manager, settings_manager)

        loadout = randomiser.generate_loadout()
        #print("[RANDOMIZER TEST] Generated Loadout:")
        #print("\n".join(f"Slot {i}: {weapon}" for i, weapon in enumerate(loadout, start=1)))



        # …ᘛ⁐̤ᕐᐷ
