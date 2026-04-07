import json
import os
from AssetManager import AssetManager

class BlacklistManager:
    def __init__(self, asset_manager: AssetManager, preset_manager, file_path="weapons.json"):
        self.asset_manager = asset_manager
        self.file_path = asset_manager.resolve(file_path)
        self.preset_manager = preset_manager
        self.weapons = self._load_weapons()  # call internal method to load weapons

        print(f"[BLACKLIST DEBUG] Exists: {os.path.exists(self.file_path)} | Path: {self.file_path}")

    # Loads weapons from the JSON.
    def _load_weapons(self):
        if not os.path.exists(self.file_path):
            # print(f"[ERROR] {self.file_path} not found, creating empty list.")
            self.weapons = []
            return self.weapons

        try:
            with open(self.file_path, "r", encoding='utf-8') as f:
                self.weapons = json.load(f)
            if not isinstance(self.weapons, list):
                print(f"[BLACKLIST DEBUG] Warning: why is weapons.json a list!!")
                self.weapons = []

        except json.JSONDecodeError as e:
            print(f"[ERROR] failed to load {self.file_path}: {e}")
            self.weapons = []

        # print (f"[LOAD_WEAPON DEBUG] Weapons Loaded: {[w.get('name') for w in self.weapons]}")
        return self.weapons


    # Tells a weapon to change its blacklisted state
    def toggle(self, name: str) -> bool | None:
        for w in self.weapons:
            if w["name"].lower() == name.lower():
                w["blacklisted"] = not w.get("blacklisted", False)
                status = "blacklisted" if w["blacklisted"] else "un-blacklisted"
                # print(f"{w['name']} is now {status}.")
                return w["blacklisted"]
        # print(f"[ERROR] Weapon '{name}' not found.")
        return None

        # Lists all currently blacklisted weapons.
    # def list_blacklisted(self):
#        blacklisted = [w["name"] for w in self.weapons if w.get("blacklisted", False)]
#        if not blacklisted:
#            print("No weapons currently blacklisted.")
#        else:
#            print("\nCurrently blacklisted weapons:")
#            for name in blacklisted:
#                print(f"- {name}")
#        return blacklisted
        # This is entirely useless for the Exe releases.

    # Clears blacklist.... duh
    def clear_blacklist(self):
        for w in self.weapons:
            w["blacklisted"] = False
        self._save_weapons()
        # print("Blacklist successfully cleared.")

    # Method for Randomizer
    def get_allowed_weapons(self, full_list=False):
        # Gives back the weapons that are not currently blacklisted
        print(f"[ALLOWED DEBUG] Total weapons in manager: {len(self.weapons)}")
        print(f"[ALLOWED DEBUG] Active preset: {self.preset_manager.current_preset_name}")
        print(f"[ALLOWED DEBUG] Blacklist: {self.preset_manager.active_preset().get('blacklisted', [])}")
        if full_list:
            return self.weapons

        allowed = []

        for w in self.weapons:
            name = w.get("name")
            if not name:
                print(f"[FILTER ERROR] Weapon name missing: {w}")
                continue

            if self.preset_manager.is_blacklisted(name):
                continue

            allowed.append(w)
            print(f"[ALLOWED DEBUG] Weapons Loaded: {[w.get('name', '<MISSING NAME.') for w in allowed]}")

        return allowed


        # if not in blacklist
            #append

        # then return


#    def blacklist_manager_debug_mode(self):
#        print("[DEBUG START] BlacklistManager Test")
#        print(f"[BLACKLIST DEBUG] Weapons Loaded: {[w['name'] for w in bm.weapons]}")




    if __name__ == "__main__":
        print("[DEBUG START] BlacklistManager Test")


from AssetManager import AssetManager
am = AssetManager()
bm = BlacklistManager(am, "weapons.json")

expected_loaded = 70
loaded = len(bm.weapons)
print(f"[BLACKLIST DEBUG] Weapons Loaded: {loaded} out of {expected_loaded}.")




