import tkinter
import tkinter as tk
# from DebugManager import DebugManager


class UIManager:
    def __init__(self, main_ui, settings_manager, blacklist_manager, randomizer, asset_manager, preset_manager):
        self.blacklist_vars = None
        self.ui = main_ui
        self.settings = settings_manager
        self.blacklist = blacklist_manager
        self.randomizer = randomizer
        self.asset_manager = asset_manager
        self.preset_manager = preset_manager

        # Placeholder for future images
        self.weapon_images = []

        # Tracking for what empty mode is being used.
        self.empty_states = ['Disabled', 'Single', 'Multi-Empty']
        self.empty_index = 0 # < Dumbas remember to make this exactly in starting mode

        # Logic for colouring on the funny empty button
        self.empty_colours = {
            "Disabled": "red",  # No empty slots
            "Single": "green",   # Single Empty mode
            "Multi-Empty": "gold"   # Multi-empty mode
        }
        # Prevents early button links
        self.ui_initialized = False

        # reroll buttons
        self.blacklist_window = None


    def init_ui(self):
        # Links the buttons to the appropriate command.
        self.ui_initialized = True

        if hasattr(self.ui, 'btn_enable_reskin'):
            self.ui.btn_enable_reskin.config(command=self.toggle_reskin)
        if hasattr(self.ui, 'btn_enable_empty'):
            self.ui.btn_enable_empty.config(command=self.toggle_empty)
        if hasattr(self.ui, 'btn_generate'):
            self.ui.btn_generate.config(command=self.generate_loadout)
        if hasattr(self.ui, 'btn_blacklist'):
            self.ui.btn_blacklist.config(command=self.open_blacklist)
        if hasattr(self.ui, 'btn_disable_5th'):
            self.ui.btn_disable_5th.config(command=self.disable_5th_slot)

        for i, btn in enumerate(getattr(self.ui, 'btn_reroll_slot', [])):
            if btn:
                btn.config(command=self.make_reroll_func(i))

    def make_reroll_func(self, slot_index):
        def reroll():
            self.reroll_slot(slot_index)
        return reroll

        # Button Actions

    def get_rkn_state(self):
        value = self.settings.get_setting('enable_reskins')
        # print(f"[DEBUG] enable_reskin = {value}")
        return f"Reskins: {'ON' if value else 'OFF'}"
    # This returns the current value for Reskins inside the Settings

    def toggle_reskin(self): # Flips boolean
        new_value = not self.settings.get_setting("enable_reskins")
        self.settings.set_setting("enable_reskins", new_value)

        # Updato buton text
        if hasattr(self.ui, 'btn_enable_reskin'):
            self.ui.btn_enable_reskin.config(
                text=f"Reskins: {'ON' if new_value else 'OFF'}"
            )

    def get_emp_state(self):
        enable = self.settings.get_setting("enable_empty")
        multi = self.settings.get_setting("multi_empty")

        if not enable:
            label = "Disabled"
        elif enable and not multi:
            label = "Single"
        else:
            label = "Multi-Empty"

        # print(f"[DEBUG] Empty Mode: enable_empty={enable}, multi_empty={multi} > {label}")
        return f"Empty Mode: {label}"

    def toggle_empty(self): # Cycles index
        current_label = self.get_emp_state().split(": ")[1] # Disabled

        # Updates JSON-backed so the randomizer can actually see the damn values
        if current_label == "Disabled":
            # Cycles to Single
            self.settings.set_setting("enable_empty", True)
            self.settings.set_setting("multi_empty", False)
        elif current_label == "Single":
            # Cycles to Multi
            self.settings.set_setting("enable_empty", True)
            self.settings.set_setting("multi_empty", True)
        elif current_label == "Multi-Empty":
            # Cycles back to Disabled
            self.settings.set_setting("enable_empty", False)
            self.settings.set_setting("multi_empty", False)

        self.ui.btn_enable_empty.config(text=self.get_emp_state())
        self.ui.root.update()

        # Old Boarder colour updating code for the recycled colour swapping idea
        # colour = self.empty_colours[state]
        # self.ui.btn_enable_empty.config(
           # highlightbackground=colour,
           # highlightthickness=4
        # )

    def set_multi_chance(self):
        try:
            value = float(self.ui.txt_multi_chance.get()) # Reads the input as a float.

            # Locks values between 0 and 1 + Rounds to nearest 0.1 increment
            value = max(0.0, min(1.0, value))
            value = round(value * 10) / 10.0

            self.settings.set_setting("multi_chance", value)

            # Ensures the input fields is a rounded value.
            self.ui.txt_multi_chance.delete(0, 'end')
            self.ui.txt_multi_chance.insert(0, str(value))

        except ValueError:
            current = self.settings.get_setting("multi_chance")
            self.ui.txt_multi_chance.delete(0, 'end')
            self.ui.txt_multi_chance.insert(0, str(self.settings.multi_chance))

    def reroll_slot(self, slot_index):
        # Rerolls a specific slot when pressed.
        current_loadout = [label.cget("text") for label in self.ui.weapon_labels]

        # Rerolls using the current_loadout to avoid duplicates
        weapon = self.randomizer.reroll(slot_index, current_loadout)

        # ui stuff
        self.ui.weapon_labels[slot_index].config(text=weapon)

    def generate_loadout(self):
        # First, show placeholder text for all slots
        for i, label in enumerate(self.ui.weapon_labels):
            if i == 4 and self.settings.get_setting("disable_fifth_slot"):
                label.config(text="[Disabled]")
            else:
                label.config(text="Randomizing. . .")

        # Function that updates slots after delay
        def _generate():
            try:
                weapons = self.randomizer.generate_loadout()
                # DebugManager.log(f"Weapons generated: {weapons}")
            except Exception as e:
                # DebugManager.log(f"Randomizer error: {e}")
                return

            for i, weapon in enumerate(weapons):
                def update_slot(idx=i, w=weapon):
                    try:
                        disable = self.settings.get_setting("disable_fifth_slot")
                        # DebugManager.log(f"Updating slot {idx}, weapon: {w}, disable_fifth_slot={disable}")

                        if idx == 4 and disable:
                            self.ui.weapon_labels[idx].config(text="[Disabled]")
                        else:
                            self.ui.weapon_labels[idx].config(text=w)
                    except Exception as e:
                        # DebugManager.log(f"Slot {idx} update error: {e}")
                        pass

                self.ui.root.after(300 * (i + 1), update_slot)

        # Start the generator in a separate thread
        import threading
        threading.Thread(target=_generate, daemon=True).start()


    def get_d5s_state(self):
        value = self.settings.get_setting('disable_fifth_slot')
        # print(f"[DEBUG] disable_fifth_slot = {value}")
        return f"5th Slot: {'Disabled' if value else 'Enabled'}"
    # This returns the current value for Disable Fifth Slot inside the Settings

    def disable_5th_slot(self):
        # Flips the current setting
        new_value = not self.settings.get_setting("disable_fifth_slot")
        self.settings.set_setting("disable_fifth_slot", new_value)

        # UI updater thingamabob
        if hasattr(self.ui, 'btn_disable_5th'): # Updates text
            self.ui.btn_disable_5th.config(
                text=self.get_d5s_state(),
            )
            self.ui.root.update_idletasks()

    def open_blacklist(self):
        # Loads the preset & the library
        weapon_library = self.blacklist.weapons
        active_blacklist = self.preset_manager.active_preset().get("blacklisted", [])

        # First creates the new window
        self.blacklist_window = tkinter.Toplevel(self.ui.root)
        self.blacklist_window.title = "Edit Blacklist"
        self.blacklist_window.geometry("450x550")
        self.blacklist_window.configure(bg="white")

        # Prevents window from scaling
        self.blacklist_window.resizable(False, True)

        # Gives the big ol fancy heading text
        (tk.Label(self.blacklist_window, text="Enable/Disable Weapons",
                  font=("TkDefaultFont", 16, "bold"), bg="white").pack(pady=10))

        # List that has the scroll list
        container = tk.Frame(self.blacklist_window, width=420)
        container.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Canvas
        canvas = tk.Canvas(container, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        # Scroll Bar
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable frame
        scroll_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")

        # updates scroll region when the frame changes
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.blacklist_vars = {} # Initializing to sore some booleans

        # Boxes for the weapons
        for weapon in weapon_library:
            if weapon.get("type") == "None":
                continue    # Skips the placeholder

            # the current blacklist taken from BlacklistManager
            var = tk.BooleanVar(value=weapon["name"] in active_blacklist)
            chk = tk.Checkbutton(scroll_frame,
                                 text=weapon["name"],
                                 variable=var,
                                 bg="white",
                                 anchor="w",
                                 font=("TkDefaultFont", 12))
            chk.pack(fill="x", padx=10)

            self.blacklist_vars[weapon["name"]] = var

            # [REFACTOR] CHANGE TO WEAPONS.JSON TO DISPLAY ALL ENTRIES

        # Bottom fram buton
        button_frame = tk.Frame(self.blacklist_window, bg="white")
        button_frame.pack(fill="x", side="bottom", pady=10)

        tk.Button(self.blacklist_window,text="Save",font=("TkDefaultFont", 14, "bold"),bg="#4CAF50",
                  fg="white",command=self.save_blacklist).pack(pady=10)
        tk.Button(self.blacklist_window,text="Clear",font=("TkDefaultFont", 14, "bold"),bg="#f44336",
                  fg="white",command=self.clear_blacklist).pack(pady=10)

    def save_blacklist(self):
        # Checkbox stuff
        for name, var in self.blacklist_vars.items():
            if var.get() is False: # Checks if item should be blacklisted
                self.preset_manager.remove_weapon_from_preset(name)
            else:
                self.preset_manager.add_weapon_to_preset(name)

        # close window
        self.blacklist_window.destroy()

    def clear_blacklist(self):
        # Clears... the blacklist...
        self.blacklist.clear_blacklist()
        for var in self.blacklist_vars.values():
            var.set(False)