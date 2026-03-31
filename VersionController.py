import subprocess

class VersionController:
    def __init__(self):
        self.version = self.get_version()

    def get_version(self):

        # import version
            # return version

        # if fails
            # Pass

        # If previous fails, tries the developer fallback (Git version)
        try:
            version = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                stderr=subprocess.DEVNULL).decode().strip()
            return version
        except Exception:
            return "vX.X.X"