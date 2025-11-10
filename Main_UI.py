import tkinter as tk
from PIL import Image, ImageTk

class MainUI:
    def __init__(self):
        self.root = tk.Tk() # Creates the main window
        self.root.title("Blast Zone Randomizer")
        self.root.geometry("900x600") # Sets the window size
        self.root.configure(bg="white") # Sets the background colour

        # Creates the Canvas for the whole background
        self.canvas = tk.Canvas(self.root, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)

        # TEMPORARY MS-PAINT REFERENCE IMAGE
        self.bg_image = Image.open("Blast Zone Randomizer Wireframe.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Table Logic!
        table_x1, table_y1 = 326, 138
        table_x2, table_y2 = 793, 446
        row_height = (table_y2 - table_y1) // 5
        table_top = 140
        table_bg_colour = "#f0f0f0"
        border_colour = "black"

        self.slot_labels = []
        self.weapon_labels = []


        for i in range(5):
            y1 = table_top + i * row_height
            y2 = y1 + row_height

            # Draws a rectangle row.
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

        self.root.mainloop()

# Runs if the file is executed:
if __name__ == "__main__":
    ui = MainUI()