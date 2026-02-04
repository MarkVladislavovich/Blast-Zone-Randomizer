import datetime

class DebugManager:
    LOG_FILE = "exe_debug_log.txt"  # Stored in working directory

    @staticmethod
    def log(message):
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(DebugManager.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass  # silently ignore logging errors

    # This is really only generated since I don't want to remove its integration.


    # Solved a REALLY annoying bug 11:38PM 29/11/2025:

    # [2025-11-29 23:32:30] Weapons generated: ['Small Bomb (Epic)', 'Fusion Cannon (Legendary)', 'Ice Cube (Uncommon)', 'Bowling Ball (Common)']
    # [2025-11-29 23:32:31] Updating slot 0, weapon: Small Bomb (Epic), disable_fifth_slot=False
    # [2025-11-29 23:32:31] Updating slot 1, weapon: Fusion Cannon (Legendary), disable_fifth_slot=False
    # [2025-11-29 23:32:31] Updating slot 2, weapon: Ice Cube (Uncommon), disable_fifth_slot=False
    # [2025-11-29 23:32:32] Updating slot 3, weapon: Bowling Ball (Common), disable_fifth_slot=False

    # This showed the MainUI and UIManager were doing its job, but the fucking RANDOMIZER wasn't printing a 5th weapon