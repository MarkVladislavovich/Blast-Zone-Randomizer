import sys
import os
import json
from PIL import Image

class AssetManager:
    def __init__(self):
        # This doohickey makes when it runs, assets are in the _MEIPASS
        if getattr(sys,'frozen', False):
            self.base_path = sys._MEIPASS # <<< Cannot find reference '_MEIPASS' in '__init__.pyi'
        else:
            # This is when running from IDE
            self.base_path = os.path.dirname(os.path.abspath(__file__))

    def resolve(self, relative_path: str):
        # Returns a correct full path for a bundled asset
        return os.path.join(self.base_path, relative_path)

    def load_image(self, filename: str):
        # Loads image from the bundle or local path.
        path = self.resolve(filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image Missing at {path}")
        return Image.open(path)

    def load_json(self, filename):
        # Sees what path to use based if the thing is frozen (EXE) or not
        if getattr(sys, 'frozen', False):
            path = os.path.join(sys._MEIPASS, filename)  # Uses temp folder
        else:
            path = self.resolve(filename)  # IDE path

        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing JSON at {path}")

        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_json(self, filename: str, data):  # <<< Method 'save_json' may be 'static'
        # Always saves the to the working directory instead of MEIPASS.
        path = os.path.join(os.getcwd(), filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

            # def blast_coin_miner_:yeas:
            #   if user = have_blastcoins(true)
            #       steal blastcoins
