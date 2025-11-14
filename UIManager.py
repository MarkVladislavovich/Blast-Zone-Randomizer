import time
import threading # To stop UI from freezing


class UIManager:
    def __init__(self, main_ui, settings_manager, blacklist_manager, randomizer):
        self.ui = main_ui
        self.settings = settings_manager
        self.blacklist = blacklist_manager
        self.randomizer = randomizer

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

        for i, btn in enumerate(getattr(self.ui, 'btn_reroll_slot', [])):
            if btn:
                btn.config(command=self.make_reroll_func(i))

    def make_reroll_func(self, slot_index):
        def reroll():
            self.reroll_slot(slot_index)
        return reroll

        # Button Actions

    def toggle_reskin(self): # Flips boolean
        new_value = not self.settings.get_setting("enable_reskins")
        self.settings.set_setting("enable_reskins", new_value)

        # Updato buton text
        if hasattr(self.ui, 'btn_enable_reskin'):
            self.ui.btn_enable_reskin.config(
                text=f"Reskins: {'ON' if new_value else 'OFF'}"
            )

    def toggle_empty(self): # Cycles index
        self.empty_index = (self.empty_index + 1) % len(self.empty_states)
        state = self.empty_states[self.empty_index]

        # Updates JSON-backed so the randomizer can actually see the damn values
        if state == "Disabled":
            self.settings.set_setting("enable_empty", False)
            self.settings.set_setting("multi_empty", False)
        elif state == "Single":
            self.settings.set_setting("enable_empty", True)
            self.settings.set_setting("multi_empty", False)
        elif state == "Multi-Empty":
            self.settings.set_setting("enable_empty", True)
            self.settings.set_setting("multi_empty", True)


        self.settings.empty_mode = state # Updates thy settings

        self.ui.btn_enable_empty.config(text=f"Empty Mode: {state}")

        # Boarder colour updating
        colour = self.empty_colours[state]
        self.ui.btn_enable_empty.config(
            highlightbackground=colour,
            highlightthickness=4
        )


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
        weapon = self.randomizer.reroll(slot_index)
        self.ui.weapon_labels[slot_index].config(text=weapon)

    def generate_loadout(self):
        # Creates placeholder text
        for label in self.ui.weapon_labels:
            label.config(text="Randomizing. . .")

        def _generate():
            weapons = self.randomizer.generate_loadout() # Gives a list of 5 weapons.

                # This stuff updates the table in Main_UI
            for i, weapon in enumerate(weapons):
                time.sleep(0.3)
                if i < len(self.ui.weapon_labels):
                    self.ui.weapon_labels[i].config(text=weapon)

        threading.Thread(target=_generate, daemon=True).start()

    def open_blacklist(self):
        pass