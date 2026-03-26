import sys
import os
import json

from SettingsManager import SettingsManager
from AssetManager import AssetManager
from VersionController import VersionController
from Main_UI import MainUI

class StartupManager:
    def check_pillow(self):
        try:
            from PIL import Image
            return {
                "id": "pillow",
                "label": "Image Library",
                "status": "ok",
                "message": "Installed"
            }
        except Exception:
            return {
                "id": "pillow",
                "label": "Image Library",
                "status": "fail",
                "message": "Pillow Unavailable"
            }

    def check_settings(self):
        try:
            manager = SettingsManager()
            result = manager._load_settings()

            if result == "created":
                return {
                    "id": "settings",
                    "label": "Settings File",
                    "status": "warn",
                    "message": "Missing - Defaults restored"
                }

            return {
                "id": "settings",
                "label": "Settings File",
                "status": "ok",
                "message": "Loaded"
                }

        except Exception:
            return {
                "id": "settings",
                "label": "Settings File",
                "status": "fail",
                "message": "Invalid or Unreadable settings.json"
            }

    def run(self):
        results = []
        results.append(self.check_pillow())
        results.append(self.check_settings())
        return results

    def startup_check(self):
        print("[INFO] Starting Check...")

        # Shows the version stuffs
        version_controller = VersionController()
        print("[INFO] Version: {version_controller.version}")

        # Wakes up AssetManager
        asset_manager = AssetManager()

        # Weapon checks!
        # Load weapons via Asset Manager

        # Settings
        # Load settings via Settings Manager

        # Finish Startup
        # uhh like say "Startup Complete" or some shit





    if __name__ == "__main__":
        print("[INFO] Opening Randomizer...")




        weapons = load_weapons()
        print("[INFO] Weapons Loaded: {lens(weapons)}")

        settings = load_settings()
        print("[INFO] Settings Loaded: {'OK' if settings else 'FAILED']")

        ui = MainUI(version=version_controller.version)

        print("[INFO] UI Initialized...")


