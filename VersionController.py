import subprocess


class VersionController:
    def __init__(self):
        self.version = self.get_git_version()

    def get_git_version(self):
        # Tries to grab the latest Git tag, if fails reverts to default
        try:
            version = subprocess.check_output(
                ["git", "describe", "--tags", "--abbrev=0"],
                stderr=subprocess.DEVNULL).decode().strip()

            return version

        except Exception:
            return "v0.0.0"
