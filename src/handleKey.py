# import importlib
# importlib.import_module("model")
# importlib.import_module("motion")
# importlib.import_module("operators")

def handleKey(key):
    if getMode() == Mode.insert:
        return key
    if key.lower() == "esc":
        setMode(Mode.normal)
    if key == "0":
        return getPluginBinding("goLineStart")
    if key == "$":
        return getPluginBinding("goLineEnd")
    elif key == "i":
        setMode(Mode.insert)
    elif key == "a":
        # TODO: Add motion
        setMode(Mode.insert)
    elif key == "I":
        return getPluginBinding("goLineStart")
        setMode(Mode.insert)
    elif key == "A":
        setMode(Mode.insert)
        return getPluginBinding("goLineEnd")
    else:
        return key
