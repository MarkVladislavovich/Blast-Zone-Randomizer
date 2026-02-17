import json
import os

from BlacklistManager import BlacklistManager

if __name__ == "__main__":
    bl = BlacklistManager()

    bl.toggle("")

    print("Is Nuke blacklisted?", bl.is_blacklisted("Nuke"))

    bl.list_blacklisted()



    # Reinstated as bonus shit 11:14PM, 29/11/2025
    # This was how I tested if blacklisting weapons actually worked before I had the MainUI
    # I essentially changed the Blacklisted: tag directly and saw which was blacklisted

