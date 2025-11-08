

class UIManager:
    def __init__(self, settings_manager, blacklist_manager, randomizer):
        self.settings = settings_manager
        self.blacklist = blacklist_manager
        self.randomizer = randomizer

    # --- [UI Elements] ---
        self.slots = [{
            "weapon": None,
            "label": None,  # Tkinter Label to display name & rarity
            "reroll_btn": None
        } for _ in range(5)]

        # Buttons
        self.btn_enable_reskin = None # Toggles the enable_reskins.
        self.btn_enable_empty = None # Toggles enable_empty & multi_empty.
        self.btn_reroll_slot = [None] * 5 # Manages the slot rerolling.
        self.btn_blacklist = None # Opens the blacklist UI.
        self.btn_generate = None # Generates a new loadout.

    # Input Fields
        self.txt_multi_chance = None # Allows input for 0-1 for the Multi-chance.

    # UI Initialization.
        self._setup_ui()

    # [Button Actions]

    # Changes & Updates reskin button display.
def toggle_reskin(self):
    self.settings.enable_reskins = not self.settings.enable_reskins
    self.btn_enable_reskin.config(text=f"Reskins: {'ON' if self.settings.enable_reskins else 'OFF'}")


    self.empty_states = ['disabled', 'empty', 'multi-empty']
    self.empty_index = 0

    # Cycles through empty / multi-empty / disabled.
def toggle_empty(self):
    self.empty_index = (self.empty_index + 1) % len(self.empty_states)
    state = self.empty_states[self.empty_index]
    self.settings.empty_mode = state
    self.btn_enable_empty.config(text=f"Empty Mode: {state}")

def set_multi_chance(self):
    try:
        value = float(self.txt_multi_chance.get())
        if 0 <= value <= 1:
            self.settings.multi_chance = value
        else:
            raise ValueError
    except ValueError:
        self.txt_multi_chance.delete(0,'end')
        self.txt_multi_chance.insert(0, str(self.settings.multi_chance))

def reroll_slot(self):
    # rerolls one specific slot on the randomizer.
    pass

def generate_loadout(self):
    # Initiates the Randomizer.py function.
    pass

def open_blacklist(self):
    # opens the blacklist UI for editing.
    pass

# [Internal UI Setup]

def _setup_ui(self):
    # Positions the buttons, text inputs and slot segments.
    # Layout code uses a GUI Framework (Tkinter.)
    pass