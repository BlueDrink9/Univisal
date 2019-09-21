from model import *
from motion import *
from operators import *

def handleKey(key):
    if key.lower() == "esc":
        setMode(Mode.normal)
        # No op. Need to send something back via socket.
        return "NOP"
    if getMode() == Mode.insert:
        return key
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
        setMode(Mode.insert)
        return getPluginBinding("goLineStart")
    elif key == "A":
        setMode(Mode.insert)
        return getPluginBinding("goLineEnd")
    else:
        return key
