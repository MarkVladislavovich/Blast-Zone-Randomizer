import random
import json
import time
from SettingsManager import SettingsManager

def generate_loadout(all_weapons, slot_count, allow_reskins, allow_empty, multi_empty=False, multi_chance=0.2):
    # Forces slot_count to a maximum of 5
    slot_count = min(slot_count, 5)

    # Filter weapons based on settings
    filtered = [
        w for w in all_weapons
        if (allow_reskins or not w["reskin"])
           and (allow_empty or w.get("type", "weapon") != "None")
           and not w.get("blacklisted", False)
    ]
    # Separate empty and non-empty weapons
    empty_weapon = [w for w in filtered if w.get("type") == "None"]
    non_empty = [w for w in filtered if w.get("type") != "None"]

    # Warns if not enough weapons to fill all slots
    if len(non_empty) == 0 and not (allow_empty or multi_empty):
        print("[ERROR] Not enough weapons to fill all slots with enabled filters.")

    loadout = []

    for _ in range(slot_count):
        print(f"Empty weapons found: {len(empty_weapon)}")
        print(f"Multi-empty: {multi_empty}, Chance: {multi_chance}")

        # Multi-empty logic having a 50% chance to insert an empty weapon if 'multi_empty' is true.
        if multi_empty and empty_weapon and random.random() < multi_chance:
            loadout.append(random.choice(empty_weapon))
        else:
            if non_empty:
                choice = random.choice(non_empty)
                loadout.append(choice)
                non_empty.remove(choice)
            elif empty_weapon:
                loadout.append(random.choice(empty_weapon))

    # Print loadout
    print("\nYour randomized loadout:")
    for weapon in loadout:
        print(f"- {weapon['name']} ({weapon['rarity']})")
        time.sleep(0.5)

    return loadout

# --- Settings Manager Integration ---
if __name__ == "__main__":
    # Loads weapons.
    with open("weapons.json", "r") as f:
        weapons = json.load(f)

    # Loads user settings.
    settings = SettingsManager()
    slot_amount = settings.get_setting("slot_amount") # Reads the slot amount
    allow_reskins = settings.get_setting("enable_reskins")  # Reads the reskin setting
    allow_empty = settings.get_setting("enable_empty") # Reads the empty setting
    multi_empty = settings.get_setting("multi_empty") # Reads the multi-empty settings
    multi_chance = settings.get_setting("multi_chance")  # Reads the multi-chance setting

    # Generates loadout using the settings
    generate_loadout(
        all_weapons=weapons,
        slot_count=slot_amount,
        allow_reskins=allow_reskins,
        allow_empty=allow_empty,
        multi_empty=multi_empty,
        multi_chance=multi_chance
    )
