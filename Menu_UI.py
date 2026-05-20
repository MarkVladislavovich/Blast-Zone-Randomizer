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
        img = self.asset_manager.load_image(
            "Development/Wireframes/BlastZone_Settings_Wireframe.png"
        )

        # Creating the background

        self.bg_image = ImageTk.PhotoImage(img)

        bg_label = tk.Label(self.settings_window, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Creating the headings

        # General Settings Heading
        tk.Label(self.settings_window,text="General Settings",font=("TkDefaultFont", 12, "bold")
                 ,width=16,height=2,borderwidth=1,relief="solid").place(x=5,y=3)

        # Background Settings Heading
        tk.Label(self.settings_window, text="Background Settings", font=("TkDefaultFont", 12, "bold")
                 , width=21, height=2, borderwidth=1, relief="solid").place(x=179, y=3)

        # UI Settings Heading
        tk.Label(self.settings_window, text="UI Settings", font=("TkDefaultFont", 12, "bold")
                 , width=21, height=2, borderwidth=1, relief="solid").place(x=179, y=355)

        # Hotkey Settings Heading
        tk.Label(self.settings_window, text="Hotkey Settings", font=("TkDefaultFont", 12, "bold")
                 , width=16, height=2, borderwidth=1, relief="solid").place(x=5, y=355)

        # General Settings Body
        tk.Label(self.settings_window, width=23, height=20, borderwidth=1, relief="solid").place(x=5, y=46)

        # Background Settings Body
        tk.Label(self.settings_window, width=30, height=20, borderwidth=1, relief="solid").place(x=179, y=46)