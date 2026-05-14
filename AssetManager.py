import sys
import os
import json

from PIL import Image

class AssetManager:
    def __init__(self):
        # This doohickey makes when it runs, assets are in the _MEIPASS
        if getattr(sys,'frozen', False):
            self.base_path = sys._MEIPASS # PyInstallers temporary asset place.
        else:
            # This is when running from IDE
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # Root for saving persistent data
        self.project_root = os.path.abspath(
            os.path.join(self.base_path, "..")
        )

    def resolve(self, relative_path: str):
        # Returns a correct full path for a bundled asset
        # This is to make sure the same code works regardless of if it's in the IDE or compiled EXE.
        return os.path.join(self.base_path, relative_path)

    def load_image(self, filename: str):
        # Loads images from the assets folder.
        path = self.resolve(filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image Missing at {path}")
        return Image.open(path)

    def load_json(self, filename):
        path = self.resolve(filename)   # Uses resolve to ensure filepaths are the same.

        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing JSON at {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, filename: str, data):  # <<< Method 'save_json' may be 'static'
        path = os.path.join(self.project_root, filename)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


            # def blast_coin_miner_:yeas:
            #   if user = have_blastcoins(true)
            #       steal blastcoins
