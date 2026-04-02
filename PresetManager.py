# This will allow BlacklistManager to load and save Presets


# Presets will be structured like this:
# | Preset Name | Load | Save | Delete |

# Active Preset

    # Check what preset is currently being used

# Change the Preset

    # See what Preset (5 Slots) was interacted with

    # Save current Preset to its slot

    # Load selected Preset

# Create new Preset

    # Ask for Preset Name

    # Save currently applied Blacklist tags

    # Add new Preset to list w/ Name

# Reset Preset
# Recycle the def clear_blacklist from BlacklistManager

# Save Preset

    # Ask for Confirmation
        # Y
            # Override Preset list
        # N
            # Pass

# Delete Preset

    # Ask for Confirmation
        # Y
            # Delete data
            # Remove Preset from list
        # N
            # Pass

# Add item to Preset

    # Weapon box is ticked
    # Add weapon to list

# Remove item from Preset

    # Weapon is unticked from box
    # Remove weapon from list

