import json
import os

from BlacklistManager import BlacklistManager

if __name__ == "__main__":
    bl = BlacklistManager()

    # Toggle blacklist for a weapon
    bl.toggle("")

    # Check if a specific weapon is blacklisted
    print("Is Nuke blacklisted?", bl.is_blacklisted("Nuke"))

    # List all currently blacklisted weapons
    bl.list_blacklisted()

    # Clear all blacklist entries
    # bl.clear_blacklist()

