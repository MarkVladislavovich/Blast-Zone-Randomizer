# This will allow BlacklistManager to load and save Presets


# Presets will be structured like this:
# | Preset Name | Load | Save | Delete |

class PresetManager:
    def active_preset(self):

        # Check what preset is currently being used
        pass

    def change_preset(self):

        # See what Preset (5 Slots) was interacted with

        # Save current Preset to its slot

        # Load selected Preset
        pass

    def create_preset(self):

    # Ask for Preset Name

    # Save currently applied Blacklist tags

    # Add new Preset to list w/ Name
        pass

    def reset_preset(self):
        # Recycle the def clear_blacklist from BlacklistManager
        pass

    def save_preset(self):

    # Ask for Confirmation
        # Y
            # Override Preset list
        # N
            # Pass
        pass

    def delete_preset(self):

    # Ask for Confirmation
        # Y
            # Delete data
            # Remove Preset from list
        # N
            # Pass
        pass

    def add_weapon_to_preset(self):

    # Weapon box is ticked
    # Add weapon to list
        pass

    def remove_weapon_from_preset(self):

    # Weapon is unticked from box
    # Remove weapon from list
        pass

