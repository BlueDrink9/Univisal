import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode, getCapturedClipboard
    from . import model
    from .motion import *
    from .operators import *
    from .remap import resolve_map
    from .adapter_maps import getAdapterMap
    from . import adapter_maps
    from .keys import Keys
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode, getCapturedClipboard
    import model
    from keys import Keys
    from motion import *
    from operators import *
    from remap import resolve_map
    from adapter_maps import getAdapterMap
    import adapter_maps
logger = logging.getLogger(__name__)


# Reduce chance of a typo if returning nop
nop = "nop"

def normalCommand(out, key):
    if key == ":":
        setMode(Mode.command)
        out.append(nop)
    elif key == "h":
        out.append(getAdapterMap(Motion.left.name))
    elif key == "l":
        out.append(getAdapterMap(Motion.right.name))
    elif key == "j":
        out.append(getAdapterMap(Motion.down.name))
    elif key == "k":
        out.append(getAdapterMap(Motion.up.name))
    elif key == "0":
        out.append(getAdapterMap(Motion.goLineStart.name))
    elif key == "$":
        out.append(getAdapterMap(Motion.goLineEnd.name))
    elif key == "i":
        setMode(Mode.insert)
        out.append(nop)
    elif key == "a":
        setMode(Mode.insert)
        out.append(getAdapterMap(Motion.right.name))
    elif key == "I":
        setMode(Mode.insert)
        out.append(getAdapterMap(Motion.goLineStart.name))
    elif key == "A":
        setMode(Mode.insert)
        out.append(getAdapterMap(Motion.goLineEnd.name))
    elif key == "w":
        out.append(getAdapterMap(Motion.goWordNext.name))
    elif key == "b":
        out.append(getAdapterMap(Motion.goWordPrevious.name))
    elif key == "f" or key == "t":
        if model.pending_clipboard:
            # After f/t.
            # First have to deselect back to previous spot.
            out.append(getAdapterMap(Motion.left.name))
            # count from clipboard till index of next letter. TODO
            # Do it count times?
            clipboard = model.getCapturedClipboard()
            moveCount = getSeekCount(clipboard, model.getSearchLetter())
            if key == 't' and moveCount > 0:
                moveCount -= 1
            out.append(getAdapterMap(Motion.right.name) * moveCount)
            return out
        else:
            out.append(getAdapterMap(Operator.visualStart.name))
            out.append(getAdapterMap(Motion.goLineEnd.name))
            out.append(getAdapterMap(Operator.visualEnd.name))
            out.append(Keys.requestSelectedText.value)
            model.pending_motion = key
            model.pending_clipboard = True
    elif key == "F" or key == "T":
        if model.pending_clipboard:
            # After f/t.
            # First have to deselect back to previous spot.
            out.append(getAdapterMap(Motion.right.name))
            # count from clipboard till index of next letter. TODO
            # Do it count times?
            clipboard = model.getCapturedClipboard()[::-1]  # Reverse.
            moveCount = getSeekCount(clipboard, model.getSearchLetter())
            if key == 'T' and moveCount > 0:
                moveCount -= 1
            out.append(getAdapterMap(Motion.left.name) * moveCount)
            return out
        else:
            out.append(getAdapterMap(Operator.visualStart.name))
            out.append(getAdapterMap(Motion.goLineStart.name))
            out.append(getAdapterMap(Operator.visualEnd.name))
            out.append(Keys.requestSelectedText.value)
            model.pending_motion = key
            model.pending_clipboard = True
    else:
        logger.info("Normal command not found: {}".format(key))
        return key
    return out

def getSeekCount(string, searchLetter):
    try:
        moveCount = string.index(searchLetter)
    except ValueError:
        # Seeked character not in line. Don't move.
        moveCount = 0
    model.pending_clipboard = False
    return moveCount

