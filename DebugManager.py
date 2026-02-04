import datetime
import os

class DebugManager:
    Debug_Enabled = False # Toggle to activate Debug outputs
    Output_Directory = "debug_output"

    # ----- File Writer -----
    @classmethod
    def _write_file(cls, filename, data):
        if not cls.Debug_Enabled: # Checks if Debug_Enabled is set to False.
            return False

        try:
            os.makedirs(cls.Output_Directory, exist_ok=True)
            path = os.path.join(cls.Output_Directory, filename)

            with open(path, "w", encoding="utf-8") as f:
                f.write(data)       # Opens a file and writes data inside.

            return True
        except Exception:
            return False

    # ----- Functions -----

    def weapon_log(self):
        try:
            weapons = self.randomizer.generate_loadout()
            DebugManager.log(f"Weapons Generated: {weapons}")
        except Exception as e:
            DebugManager.log(f"Randomizer Error: {e}")
            return

        for i, weapon in enumerate(weapons):
            def slot_update(idx=i,w=weapons):
                try:
                    disable = self.settings.get_setting("disable_fifth_slot")
                    DebugManager.log(f"Updating slot {idx}, weapon: {w}, disable_fifth_slot={disable}")

                    if idx == 4 and disable:
                        self.ui.weapon_labels[idx].config(text="[Disabled]")
                    else:
                        self.ui.weapon_labels[idx].config(text=w)
                except Exception as e:
                    DebugManager.log(f"Slot {idx} update error: {e}")

            self.ui.root.after(300 * (i + 1), slot_update())








    # Solved a REALLY annoying bug 11:38PM 29/11/2025:

    # [2025-11-29 23:32:30] Weapons generated: ['Small Bomb (Epic)', 'Fusion Cannon (Legendary)', 'Ice Cube (Uncommon)', 'Bowling Ball (Common)']
    # [2025-11-29 23:32:31] Updating slot 0, weapon: Small Bomb (Epic), disable_fifth_slot=False
    # [2025-11-29 23:32:31] Updating slot 1, weapon: Fusion Cannon (Legendary), disable_fifth_slot=False
    # [2025-11-29 23:32:31] Updating slot 2, weapon: Ice Cube (Uncommon), disable_fifth_slot=False
    # [2025-11-29 23:32:32] Updating slot 3, weapon: Bowling Ball (Common), disable_fifth_slot=False

    # This showed the MainUI and UIManager were doing its job, but the fucking RANDOMIZER wasn't printing a 5th weapon