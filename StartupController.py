import sys
import subprocess
from csv import excel

# Tries to import tkinter for text, if not there I guess its console time
TK_AVAILABLE = False
try:
    import tkinter as _tk
    from tkinter import messagebox as _messagebox
    TK_AVAILABLE = True
except Exception:
    TK_AVAILABLE = False

def _run_subprocess(cmd, timeout=None):
    # Runs a subprocess command
    # returns True or False.

    try:
        completed = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return True, completed.stdout + completed.stderr
    except subprocess.CalledProcessError as e:
        return False, (e.stdout or "") + (e.stderr or "")
    except Exception as e:
        return False, str(e)

def ask_permission(title, message, default=False):

    # Ask if you want to proceed with installation.
    # and returns either True or False

    if TK_AVAILABLE:
        root = _tk.Tk()
        root.withdraw()
        answer = _messagebox.askyesno(title, message)
        root.destroy()
        return bool(answer)
    else:
        default_str = "Y/n" if default else "y/N"
        try:
            resp = input(f"{title}\n{message}\n[{default_str}] ").strip().lower()
        except Exception:
            return default
        if resp == "":
            return default
        return resp.startswith("y")

def pillow_install_check():
    # Checks if pillow is installed.
    try:
        from PIL import Image
        return True
    except Exception:
        return False

def pillow_prompt():
    # If pillow is missing, asks if they want to download it.
    if pillow_install_check():
        print("[INFO] Pillow already installed.")
        return True

    title = "Pillow not Found"
    message = (
        "Hey uh, Pillow is kinda required for the UI.\n\n"
        "Would you like to install Pillow automatically?"
    )

    if not ask_permission(title, message, default=True):
        print("[INFO] Pillow installation canceled.")
        return False

    # Tries common windows python points
    possible_python_cmds = [
        [sys.executable, "-m", "pip", "install", "Pillow"],  # most reliable ones
        ["py", "-m", "pip", "install", "Pillow"],  # fallback options
        ["python", "-m", "pip", "install", "Pillow"]  # last resort
    ]

    for cmd in possible_python_cmds:
        print(f"[INFO] Attempting installation: {' '.join(cmd)}")
        ok, output = _run_subprocess(cmd)
        print(output)

        if ok:
            # Re-checks import
            if pillow_install_check():
                print("[INFO] Pillow install successful, yippe!")
                return True

    print("[INFO] Pillow install failed.")
    return False

if __name__ == "__main__":
    # Manual test
    print("Testing InstallationManager (Windows Version)")
    print("Pillow Installed:", pillow_install_check())

    if not pillow_install_check():
        result = pillow_prompt()
        print("Install Result:", result)