import sys
import os
import json

from SettingsManager import SettingsManager
from AssetManager import AssetManager
from VersionController import VersionController
# from Main_UI import MainUI

class StartupManager:
    def check_pillow(self):
        self.asset_manager = AssetManager()

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
            manager = SettingsManager(self.asset_manager)
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
        return [
            self.check_pillow(),
            self.check_settings()
        ]

    def startup_check(self):
        print("[INFO] Starting Check...")

        # Shows the version stuffs
        version_controller = VersionController()
        print(f"[INFO] Version: {version_controller.version}")

        # Weapon checks!
        try:
            weapons = self.asset_manager.load_json("configs/weapons.json")
            print(f"[INFO] Weapons Loaded: {len(weapons)}")
        except FileNotFoundError as w_err:
            print(f"[ERROR] Weapons Not Loaded: {w_err}")
            weapons = []

        # Settings
        try:
            settings = self.asset_manager.load_json("configs/settings.json")
            print(f"[INFO] Settings Loaded: {settings}")
        except FileNotFoundError as s_err:
            print(f"[ERROR] Settings Not Loaded: {s_err}")

        # Finish Startup
        print("[INFO] Start check complete...")
        return weapons, settings, version_controller.version


# These scripts were for downloading the randomisers dependencies but --onefile completely makes these redundant.
# They only exist here as history of how you should not be an idiot and do your research beforehand.


