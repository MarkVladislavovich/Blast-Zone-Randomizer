import tkinter as tk
from PIL import Image, ImageTk

from SettingsManager import SettingsManager
from BlacklistManager import BlacklistManager
from Randomizer import Randomizer
from UIManager import UIManager
from AssetManager import AssetManager
from VersionController import VersionController
from PresetManager import PresetManager
from Menu_UI import MenuUI
# from StartupManager import StartupManager

# Also try: Metroplexed BZ Loadout Randomizer!
# URL: https://onecompiler.com/lua/44jrqxf3y
# For another flavour of chaos!

class MainUI:
    def __init__(self, version):

        # Tkinter stuff for background (perhaps a root of some sort :o)
        self.root = tk.Tk()  # Creates the main window
        self.root.title("Blast Zone Randomizer")
        self.root.geometry("900x600")  # window size
        self.root.configure(bg="white")  # background colour

        # Creating managers.
        self.preset_manager = PresetManager("assets/configs/presets.json")
        self.settings_manager = SettingsManager("assets/configs/settings.json")
        self.asset_manager = AssetManager()  # only once
        self.blacklist_manager = BlacklistManager(self.asset_manager, self.preset_manager)
        self.randomizer = Randomizer(self.blacklist_manager, self.settings_manager)

        # Version control shenanigans
        self.version_controller = VersionController()
        self.version = self.version_controller.version

        # Creating the UI Manager
        self.ui_manager = UIManager(
            self,
            self.settings_manager,
            self.blacklist_manager,
            self.randomizer,
            self.asset_manager,
            self.preset_manager
        )

        self.menu_ui = MenuUI(self.root, self.ui_manager)

        self.menu_ui.ui = self

        # Prevents window from scaling
        self.root.resizable(False, False)

        # Creates the big ol Canvas for the whole background
        self.canvas = tk.Canvas(self.root, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)

        title_frame = tk.Frame(self.root, bg="white", bd=4, relief="groove", width=464, height=71)

        # Title part
        title_label = tk.Label(
            title_frame,
            text="Blast Zone Randomizer",
            bg="white",
            fg="black",
            font=("TkDefaultFont", 24, "bold")
        )

        # Packs inside the frame
        title_label.pack(expand=True, fill="both",pady=10, padx=10)

        # Version control stuff!!!!! So you know the version!
        vc = VersionController

        version_label = tk.Label(
            self.root, relief="groove",
            text=f"Version: {self.version}", # shows the numbers
            bg="#e0e0e0",
            fg="black",
            font=("TkDefaultFont", 12)
        )
        version_label.pack()

        self.canvas.create_window(50 + (233-50)/2, 525 + (586-505)/2,      # Centre X & Y
            window=version_label, width=(218-50), height=(586-545))

        self.canvas.create_window(326 + 494/2, 28 + 71/2,
            window=title_frame, width=464, height=71)

        self.canvas.create_window(326 + 514/2, 28 + 71/2,      # X & Y Centre
            window=title_frame, width=464,height=71)

        # Background Image
        self.bg_image = self.asset_manager.load_image("assets/backgrounds/when-the-zone-is-blast.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        # Graphic design is NOT this man's passion! :skull:

        # Weapon Table Logic!
        table_x1, table_y1 = 326, 138
        table_x2, table_y2 = 793, 446
        row_height = (table_y2 - table_y1) // 5
        table_top = 140
        table_bg_colour = "#f0f0f0"
        border_colour = "black"

        self.slot_labels = []
        self.weapon_labels = []

        # Weapons Table
        for i in range(5):
            y1 = table_top + i * row_height
            y2 = y1 + row_height

            # Draws a rectangle row, shocking I know.
            self.canvas.create_rectangle(table_x1, y1, table_x2, y2,
                                         fill=table_bg_colour, outline=border_colour)

            # Then draws a vertical line for the two columns
            mid_x = table_x1 + int(0.25 * (table_x2 - table_x1))
            self.canvas.create_line(mid_x, y1, mid_x, y2, fill=border_colour, width=1)

            # Creates the slot label for the left row
            slot_label = tk.Label(self.root, text=f"Slot {i+1}", bg=table_bg_colour)
            self.canvas.create_window((table_x1 + mid_x)//2,(y1 + y2)//2, window=slot_label)
            self.slot_labels.append(slot_label)

            weapon_label = tk.Label(self.root, text="Weapon Name", bg=table_bg_colour)
            self.canvas.create_window((mid_x + table_x2) // 2, (y1 + y2) // 2, window=weapon_label)
            self.weapon_labels.append(weapon_label)

        # Buttons for the reroll stuffs
        reroll_coord = [
            (803, 142, 60, 60),
            (803, 203, 60, 60),
            (803, 265, 60, 60),
            (803, 327, 60, 60),
            (803, 388, 60, 60),
        ] # not the most efficient, but It'll do.

        self.reroll_buttons = []

        for i, (x, y, w, h) in enumerate(reroll_coord):
            reroll_btn = tk.Button(
                self.root,
                text="↻",
                font=("TkDefaultFont", 20, "bold"),
                command=lambda idx=i: self.ui_manager.reroll_slot(idx)
            )

        # Centers button
            self.canvas.create_window(x + w/2, y + h/2, window=reroll_btn, width=w, height=h)
            self.reroll_buttons.append(reroll_btn)

        self.ui_manager.btn_reroll_slot = self.reroll_buttons
        self.ui_manager.init_ui()

        # Options Panel
        self.options_frame = tk.Frame(self.root, bg="#e0e0e0", width=245, height=520, highlightbackground="black", highlightthickness=1)
        self.options_frame.pack_propagate(False) # < Prevents the option tab from shrinking
        self.canvas.create_window(18 + 245/2, 28 + 450/2 + 20, window=self.options_frame)

        # Settings Icon Placeholder
        settings_button = tk.Button(
            self.canvas,
            relief="groove",
            text="Settings",
            bg="#e0e0e0",
            fg="black",
            font=("TkDefaultFont", 12),
            command=self.ui_manager.open_settings_menu
        )

        settings_panel = self.canvas.create_window(
            852, 64,
            window=settings_button,
            width=70,
            height=70
        )

        self.canvas.tag_raise(settings_panel)




        # Creates the label in the canvas
        # Draws cube after label
        cube = self.canvas.create_rectangle(818, 29, 885, 98, fill="white", outline="black")

        self.canvas.tag_raise(cube)

        # BUTTONS!! --------------------------------------------------------------------------------------------------

        # Reskins
        self.btn_enable_reskin = tk.Button(self.options_frame, text=self.ui_manager.get_rkn_state(), width=40, height=4)
        self.btn_enable_reskin.pack(pady=10)

        # Empty Mode
        self.btn_enable_empty = tk.Button(self.options_frame, text=self.ui_manager.get_emp_state(), width=40, height=4)
        self.btn_enable_empty.pack(pady=10)

        # Multi-Chance Label
        self.multi_label = tk.Label(self.options_frame, text="Multi Chance (0-1):", bg="#e0e0e0", font=("TkDefaultFont",12))
        # self.multi_label = tk.Label(self.options_frame, text= {multi_chance}) Testing to add an icon to show current
        self.multi_label.pack(pady=10)

        # Multi Chance Entry
        self.txt_multi_chance = tk.Entry(self.options_frame, justify="center", font=("TkDefaultFont",12))
        current_value = self.settings_manager.get_setting("Randomizer_Settings", "multi_chance") # Grabs the current multi-chance instead of "0.1"
        self.txt_multi_chance.insert(0, current_value)
        self.txt_multi_chance.pack(pady=20)

        # Apply button so you can actually use the damn feature
        self.btn_apply_multi = tk.Button(
            self.options_frame,
            text="Apply",
            width=10,
            height=1,
            command=self.ui_manager.set_multi_chance
        )
        self.btn_apply_multi.pack(pady=5)

        # 5th slot button
        self.btn_disable_5th = tk.Button(self.options_frame,text=self.ui_manager.get_d5s_state(),
        width=40, height=4, command=self.ui_manager.disable_5th_slot)
        self.btn_disable_5th.pack(pady=10)

        # Blacklist
        self.btn_blacklist = tk.Button(self.options_frame, text="Edit Blacklist", width=40, height=4)
        self.btn_blacklist.pack(pady=10)

        # Scary Generate Button
        self.btn_generate = tk.Button(
            self.root, text="Randomize!", font=("TkDefaultFont",30,"bold"),bg="#4CAF50",fg="white",
            command=self.ui_manager.generate_loadout
        )
        self.btn_generate.place(x=325,y=473,width=500,height=95)

        self.ui_manager.init_ui()

        self.root.mainloop()

        # -------------------------------------------------------------------------------------------------

        # Slowing the result because I felt fancy c:
        # To speed up the speed of showing up Delay=X, higher the slower.
    def display_loadout_slow(self, loadout, delay=250):
        # makes only 1 slot go at a time.
        def update_slot(i=0):
            if i >= len(loadout):
                return

            # Grabs current weapon
            weapon = loadout[i]

            # Converts the raw data into just a name
            if isinstance(weapon, dict):
                text = weapon.get("name", "unknown")
            else:
                text = str(weapon)

            self.weapon_labels[i].config(text=text) # Updates the UI for the slot

            self.root.after(delay, lambda: update_slot(i + 1)) # Makes the next slot delayed

        self.root.after(delay, lambda: update_slot(0)) # Starts the updates

    # Foundation for the Settings Menu
    def open_settings_menu(self):
        pass


    # Functions to make the Randomizer explode when closed
    # def close_explosion_mode

        # is always explode?
            # Fucking explode

        # is not?
            # randomly set chance to explode

    # def holyshit_it_just_exploded

        # User presses close button

        # UI fucking explodes (Play GIF)

        # Plays funny explosion audio

        # Closes application

    # Runs if the file is executed (Why did I even add this? you need the console to see this.)

    def debug_print(self, label, var):
        if self.debug_enabled:
            print(f"[MAIN_UI DEBUG] {label}: {var}")


    if __name__ == "__main__":
        print("[INFO] Opening Randomizer...")


version_controller = VersionController()
ui = MainUI(version=version_controller.version)

# ui.debug_print("Current Preset", ui.preset_manager.current_preset_name)
# ui.debug_print("Blacklist Weapons", ui.blacklist_manager.weapons)

    # This file was such a pain in my ass, I'd be screwed if I did not make a wireframe.