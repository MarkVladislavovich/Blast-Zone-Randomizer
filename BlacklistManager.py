import json
import os
import time

class BlacklistManager:
    def __init__(self, file_path="weapons.json"):
        self.file_path = file_path
        self.weapons = self._load_weapons()  # call internal method to load weapons

        # --- [ INTERNAL ] ---
        # Loads weapons from the JSON.
    def _load_weapons(self):
        if not os.path.exists(self.file_path):
            print(f"[ERROR] File missing: {self.file_path}")
            return []
        with open(self.file_path, "r") as f:
            weapons = json.load(f)
        print(f"Successfully loaded {len(weapons)} from {self.file_path}")
        return weapons

        # Saves updates back to the file.
    def _save_weapons(self):
        with open(self.file_path, "w") as f: # noinspection PyTypeChecker
            json.dump(self.weapons, f, indent=4)

        # --- [ EXTERNAL ] ---
        # Tells a weapon to change its blacklisted state
    def toggle(self, name):
        for w in self.weapons:
            if w["name"].lower() == name.lower():
                w["blacklisted"] = not w.get("blacklisted", False)
                self._save_weapons()
                status = "blacklisted" if w["blacklisted"] else "un-blacklisted"
                print(f"{w['name']} is now {status}.")
                return w["blacklisted"]
        print(f"[ERROR] Weapon '{name}' not found.")
        return None

        # Lists all currently blacklisted weapons.
    def list_blacklisted(self):
        blacklisted = [w["name"] for w in self.weapons if w.get("blacklisted", False)]
        if not blacklisted:
            print("No weapons currently blacklisted.")
        else:
            print("\nCurrently blacklisted weapons:")
            for name in blacklisted:
                print(f"- {name}")
                time.sleep(0.5)
        return blacklisted

        # [DEBUGGING] Checks if a weapon is blacklisted
    def is_blacklisted(self, name):
        for w in self.weapons:
            if w["name"].lower() == name.lower():
                return w.get("blacklisted", False)
        print(f"[ERROR] Weapon '{name}' not found.")
        return None

    # Clears blacklist.... duh
    def clear_blacklist(self):
        for w in self.weapons:
            w["blacklisted"] = False
        self._save_weapons()
        print("Blacklist successfully cleared.")

    # Method for Randomizer
    def get_allowed_weapons(self):
        # Gives back the weapons that are not currently blacklisted
        return[w for w in self.weapons if not w.get("blacklisted", False)]
