import subprocess

class VersionController:
    def __init__(self):
        self.version = self.get_version() # Method that summons self.version

    def get_version(self):

        try:
            from version import VERSION # import version
            return VERSION # return version
        except ImportError: # if fails
            pass # Pass

        # If previous fails, tries the developer fallback (Git version)
        try:
            version = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                stderr=subprocess.DEVNULL).decode().strip()
            return version
        except Exception:
            return "vX.X.X"