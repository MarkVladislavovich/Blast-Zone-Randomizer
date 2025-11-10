import tkinter as tk
from PIL import Image, ImageTk

class UIManager:
    def __init__(self):
        self.root = tk.Tk() # Creates the main window
        self.root.title("Blast Zone Randomizer")
        self.root.geometry("900x600") # Sets the window size
        self.root.configure(bg="white") # Sets the background colour


        # TEMPORARY MS-PAINT REFERENCE IMAGE
        self.bg_image = Image.open("Blast Zone Randomizer Wireframe")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # --- Canvas --
        self.canvas = tk.Canvas(self.root,width=900, height=600)
        self.canvas.pack(fill="both", expand=True)

        # --- Background Image ---
        self.canvas.create_image(0,0, image=self.bg_photo, anchor="nw")

        # --- Weapon Slots ---
        self.slot1_label = tk.Label(self.root, text="Slot 1", bg="white")
        self.canvas.create_window(630, 173, window=self.slot1_label)

        self.slot1_weapon_label = tk.Label(self.root, text="Weapon Name", bg="white")
        self.canvas.create_window(404,177, window=self.slot1_weapon_label)

        self.root.mainloop()

# Runs if the file is executed:
if __name__ == "__main__":
    ui = UIManager()