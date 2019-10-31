from json import loads as json_load
from library import *
import logging
import logging_

from model import *
from motion import *
from operators import *
from adapter_maps import getAdapterMap


def handleKey(key):
    if key.lower() == "esc":
        setMode(Mode.normal)
        # No op. Need to send something back to signal finish.
        return "nop"
    if getMode() == Mode.insert:
        return key
    elif key == "h":
        return getAdapterMap(Motion.goLeft.name)
    elif key == "l":
        return getAdapterMap(Motion.goRight.name)
    elif key == "j":
        return getAdapterMap(Motion.goDown.name)
    elif key == "k":
        return getAdapterMap(Motion.goUp.name)
    if key == "0":
        return getAdapterMap(Motion.goLineStart.name)
    if key == "$":
        return getAdapterMap(Motion.goLineEnd.name)
    elif key == "i":
        setMode(Mode.insert)
        return "nop"
    elif key == "a":
        # TODO: Add motion
        setMode(Mode.insert)
        return "nop"
    elif key == "I":
        setMode(Mode.insert)
        return getAdapterMap(Motion.goLineStart.name)
    elif key == "A":
        setMode(Mode.insert)
        return getAdapterMap(Motion.goLineEnd.name)
    elif key == "w":
        return getAdapterMap(Motion.goWordNext.name)
    elif key == "b":
        return getAdapterMap(Motion.goWordPrevious.name)
    else:
        return key
