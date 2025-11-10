class UIManager:
    def __init__(self, main_ui, settings_manager, blacklist_manager, randomizer):
        self.ui = main_ui
        self.settings = settings_manager
        self.blacklist = blacklist_manager
        self.randomizer = randomizer

        # Tracking for what empty mode is being used.
        self.empty_states = ['Disabled', 'empty', 'multi-empty']
        self.empty_index = 0

        # Logic for button inputs.
        if hasattr(self.ui, 'btn_enable_reskin'):
            self.ui.btn_enable_reskin.config(command=self.toggle_reskin)
        if hasattr(self.ui, 'btn_enable_empty'):
            self.ui.btn_enable_empty.config(command=self.toggle_empty)
        if hasattr(self.ui, 'btn_generate'):
            self.ui.btn_generate.config(command=self.generate_loadout)
        if hasattr(self.ui, 'btn_blacklist'):
            self.ui.btn_blacklist.config(command=self.open_blacklist)

        # reroll buttons
        for i, btn in enumerate(getattr(self.ui, 'btn_reroll_slot', [])):
            if btn:
                btn.config(command=self.make_reroll_func(i))

    def make_reroll_func(self, slot_index):
        def reroll():
            self.reroll_slot(slot_index)
        return reroll()

        # Button Actions
    def toggle_reskin(self):
        self.settings.enable_reskins = not self.settings.enable_reskins
        if hasattr(self.ui, 'btn_enable_reskin'):
            self.ui.btn_enable_reskin.config(
                text=f"Reskins: {'ON' if self.settings.enable_reskins else 'OFF'}"
            )

    def toggle_empty(self):
        self.empty_index = (self.empty_index + 1) % len(self.empty_states)
        state = self.empty_states[self.empty_index]
        self.settings.empty_mode = state
        if hasattr(self.ui, 'btn_enable_empty'):
            self.ui.btn_enable_empty.config(text=f"Empty Mode: {state}")

    def set_multi_chance(self):
        try:
            value = float(self.ui.txt_multi_chance.get()) # Reads the input as a float.

            # Locks values between 0 and 1 + Rounds to nearest 0.1 increment
            value = max(0.0, min(1.0, value))
            value = round(value * 10) / 10.0

            self.settings.multi_chance = value # Updates the setting

            # Ensures the input fields is a rounded value.
            self.ui.txt_multi_chance.delete(0, 'end')
            self.ui.txt_multi_chance.insert(0, str(value))

        except ValueError:
            self.ui.txt_multi_chance.delete(0, 'end')
            self.ui.txt_multi_chance.insert(0, str(self.settings.multi_chance))

    def reroll_slot(self, slot_index):
        # Rerolls a specific slot when pressed.
        weapon = self.randomizer.reroll(slot_index)
        self.ui.weapon_labels[slot_index].config(text=weapon)

    def generate_loadout(self):
        weapons = self.randomizer.generate.loadout()
        for i, weapon in enumerate(weapons):
            self.ui.weapon_labels[i].config(text=weapon)

    def open_blacklist(self):
        pass