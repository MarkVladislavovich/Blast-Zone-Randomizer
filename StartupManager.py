import sys
import os
import json

from SettingsManager import SettingsManager


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


