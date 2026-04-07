import json
import os
from AssetManager import AssetManager

class BlacklistManager:
    def __init__(self, asset_manager: AssetManager, file_path="weapons.json"):
        self.asset_manager = asset_manager
        self.file_path = asset_manager.resolve(file_path)
        self.weapons = self._load_weapons()  # call internal method to load weapons

        print(f"[BLACKLIST DEBUG] Path: {self.file_path}")
        print(f"[BLACKLIST DEBUG] Exists: {os.path.exists(self.file_path)}")

    # Loads weapons from the JSON.
    def _load_weapons(self):
        if not os.path.exists(self.file_path):
            # print(f"[ERROR] {self.file_path} not found, creating empty list.")
            self.weapons = []
            self._save_weapons()
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

        # Saves updates back to the file.
    def _save_weapons(self):
        # Saves into the same working directory
        save_name = os.path.basename(self.file_path)
        save_path = os.path.join(os.getcwd(), save_name)

        with open(save_path, "w", encoding='utf-8') as f: # noinspection PyTypeChecker
            json.dump(self.weapons, f, indent=4)

    # Tells a weapon to change its blacklisted state
    def toggle(self, name: str) -> bool | None:
        for w in self.weapons:
            if w["name"].lower() == name.lower():
                w["blacklisted"] = not w.get("blacklisted", False)
                self._save_weapons()
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
        if full_list:
            return self.weapons

        # for weapons inside self.weapons
            # get the weapon name

        # and if not a name
            # print a warning for debugging
            # continue

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




