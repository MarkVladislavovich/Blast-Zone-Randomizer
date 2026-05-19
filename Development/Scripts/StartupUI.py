import tkinter as tk
from AssetManager import AssetManager
from PIL import Image, ImageTk


class StartupUI(tk.Frame):
    def __init__(self):

        # Manager Shenanigans
        self.asset_manager = AssetManager()

        # Tkinter stuff for background (recycled from Main UI)
        self.root = tk.Tk()  # Creates the main window
        self.root.title("Startup UI")
        self.root.geometry("400x500")  # window size
        self.root.configure(bg="white") # background colour
        self.root.resizable(False,False) # Prevents resizing

        # Creates the background
        self.canvas = tk.Canvas(self.root, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Title stuff
        title_frame = tk.Frame(self.root, bg="white", bd=3, relief="groove", width=300, height=50)
        title_label = tk.Label(
            title_frame,
            text="Startup Menu",
            bg="white",
            fg="black",
            font=("TkDefaultFont", 18, "bold"),
        )
        title_label.pack(expand=True, fill="both", padx=115, pady=15)

        # Puts the title onto the canvas
        self.canvas.create_window(
            200,       # X Centre
            36,        # Y Pos
            window=title_frame,
        )

        # Status Bar
        title_frame = tk.Frame(self.root, bg="white", bd=3, relief="groove", width=300, height=50)
        title_label = tk.Label(
            title_frame,
            text="[Status]",
            bg="white",
            fg="black",
            font=("TkDefaultFont", 14),
        )
        title_label.pack(expand=False, fill="both", padx=160, pady=6)

        # Puts the status onto the canvas
        self.canvas.create_window(
            200,  # X Centre
            94,  # Y Pos
            window=title_frame,
        )

        # Background Image
        self.bg_image = self.asset_manager.load_image("BlastZone_PreStartUI_Wireframe.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        # Graphic design is NOT this man's passion! :skull:

        self.root.mainloop()

if __name__ == "__main__":
    ui = StartupUI()


# These scripts were for downloading the randomisers dependencies but --onefile completely makes these redundant.
# They only exist here as history of how you should not be an idiot and do your research beforehand.