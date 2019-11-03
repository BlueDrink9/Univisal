from json import loads as json_load
from library import *
import logging
import logging_
logger = logging.getLogger(__name__)

from model import *
from motion import *
from operators import *
from adapter_maps import getAdapterMap


def handleKey(key):
    # Reduce chance of a typo if returning nop
    nop = "nop"
    if key.lower() == "esc":
        setMode(Mode.normal)
        # No op. Need to send something back to signal finish.
        return nop
    if getMode() == Mode.insert:
        return key
    elif key == "h":
        return getAdapterMap(Motion.left.name)
    elif key == "l":
        return getAdapterMap(Motion.right.name)
    elif key == "j":
        return getAdapterMap(Motion.down.name)
    elif key == "k":
        return getAdapterMap(Motion.up.name)
    if key == "0":
        return getAdapterMap(Motion.goLineStart.name)
    if key == "$":
        return getAdapterMap(Motion.goLineEnd.name)
    elif key == "i":
        setMode(Mode.insert)
        return nop
    elif key == "a":
        setMode(Mode.insert)
        return getAdapterMap(Motion.goRight.name)
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
