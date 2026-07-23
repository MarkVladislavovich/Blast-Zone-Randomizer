import tkinter as tk
from PIL import Image, ImageTk

class MenuUI:
    def __init__(self, root, ui_manager, asset_manager):
        self.root = root
        self.ui_manager = ui_manager
        self.asset_manager = asset_manager

        self.blacklist_window = None
        self.blacklist_vars = {}

    # Blacklist Menu Stuff

 # ------------- Blacklist stuff

    def open_blacklist(self):
        weapon_library, active_blacklist = self.ui_manager.get_blacklist_data()

        # First creates the new window
        self.blacklist_window = tk.Toplevel(self.root)
        self.blacklist_window.title("Edit Blacklist")
        self.blacklist_window.geometry("450x550")
        self.blacklist_window.configure(bg="white")
        # Prevents window from scaling
        self.blacklist_window.resizable(False, True)

        # Gives the big ol fancy heading text
        (tk.Label(self.blacklist_window, text="Disable Weapons",
                  font=("TkDefaultFont", 16, "bold"), bg="white").pack(pady=10))

        # List that has the scroll list
        container = tk.Frame(self.blacklist_window, width=420)
        container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Canvas
        canvas = tk.Canvas(container, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        # Scroll Bar
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Scrollable frame
        scroll_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # updates scroll region when the frame changes
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.blacklist_vars = {}  # Initialising to sore some booleans

        # Boxes for the weapons
        for weapon in weapon_library:
            if weapon.get("type") == "None":
                continue  # Skips the placeholder

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

        # Bottom fram buton
        button_frame = tk.Frame(self.blacklist_window, bg="white")
        button_frame.pack(fill="x", side="bottom", pady=10)

        tk.Button(self.blacklist_window, text="Save", font=("TkDefaultFont", 14, "bold"), bg="#4CAF50",
                  fg="white", command=self.save_blacklist).pack(pady=10)
        tk.Button(self.blacklist_window, text="Clear", font=("TkDefaultFont", 14, "bold"), bg="#f44336",
                  fg="white", command=self.clear_blacklist).pack(pady=10)

    def save_blacklist(self):
        selected = {
            name for name, var in self.blacklist_vars.items()
            if var.get()
        }
        self.ui_manager.save_blacklist(selected)
        self.blacklist_window.destroy()

    def clear_blacklist(self):
        self.ui_manager.clear_blacklist()
        for var in self.blacklist_vars.values():
            var.set(False)


 # ------------- Settings menu stuff

    def open_settings_menu(self):
        if hasattr(self, "settings_window") and self.settings_window.winfo_exists():
            return  # Prevents duplications

        self.settings_window = tk.Toplevel(self.ui.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("500x400")
        self.settings_window.resizable(False, False)

        tk.Label(self.settings_window, text="This feature will be available soon.").pack(pady=20)

    # Settings Menu Stuff

    def open_settings_menu(self):

        if hasattr(self, "settings_window") and self.settings_window.winfo_exists():
            return  # Prevents duplications

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x500")
        self.settings_window.resizable(False,False)


        # Creating the background

        self.settings_canvas = tk.Canvas(
            self.settings_window,
            width=400,
            height=500,
            highlightthickness=0,
        )
        self.settings_canvas.pack(fill="both", expand=True)

        bg_label = tk.Label(self.settings_window)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Creating the headings

        # General Settings Heading
        tk.Label(self.settings_window,text="General Settings",font=("TkDefaultFont", 12, "bold")
                 ,borderwidth=1,relief="solid").place(x=5,y=3,width=170,height=40) # Heading
        tk.Label(self.settings_window, borderwidth=1, relief="solid").place(x=5, y=46,width=170,height=320) # Body

        # Background Settings
        tk.Label(self.settings_window, text="Background Settings", font=("TkDefaultFont", 12, "bold")
                 , borderwidth=1, relief="solid").place(x=179, y=3,width=215,height=40) # Heading
        tk.Label(self.settings_window, borderwidth=1, relief="solid").place(x=179, y=46, width=215,height=320) # Body


        # UI Settings Heading
        tk.Label(self.settings_window, text="UI Settings", font=("TkDefaultFont", 12, "bold")
                 , borderwidth=1, relief="solid").place(x=179, y=355,width=215,height=40) # Heading
        (tk.Label(self.settings_window, borderwidth=1, relief="solid")
         .place(x=179, y=398, width=215,height=100)) # Body

        # Hotkey Settings Heading
        tk.Label(self.settings_window, text="Hotkey Settings", font=("TkDefaultFont", 12, "bold")
                 , borderwidth=1, relief="solid").place(x=5, y=355,width=170,height=40) # Heading
        (tk.Label(self.settings_window, borderwidth=1, relief="solid")
         .place(x=5, y=398, width=170,height=100)) # Body

        # --------------------------------------

        # Weapon Icon Button (Maybe?)
        self.btn_WeaponIcon = tk.Button(
            self.settings_window,
            text="Weapon Icons")    # Add 'command=self.TEMP' when it is ready.
        self.btn_WeaponIcon.place( # Edits placement
            x=8, y=48, width=165, height=50)

        # --------------------------------------

        # Background selection List

        # List should source from assets/backgrounds

        # List should be scrollable to allow for as many backgrounds as the user wants.