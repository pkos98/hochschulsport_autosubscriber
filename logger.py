def log(msg, level="info"):
    level_prefix = "" if level == "info" else level
    print("[DEBUG] " + level_prefix + " " + msg)