import importlib
importlib.import_module("model")

def handleKey(key):
    if mode == mode.Insert:
        return key
    if key == "m":
        return "m"
    elif key == "d":
        return "d"
    else:
        return key
