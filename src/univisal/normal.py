import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode, getCapturedClipboard
    from . import model
    from . import config
    from .motion import Motion
    from .operator import Operator
    from .remap import resolve_map
    from .keys import Keys
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode, getCapturedClipboard
    import model
    import config
    from keys import Keys
    from motion import Motion
    from operator import Operator
    from remap import resolve_map
logger = logging.getLogger(__name__)


# Reduce chance of a typo if returning nop
nop = "nop"

def normalCommand(out, key):
    # Command mode does nothing atm, so don't handle this key.
    # if key == ":":
        # setMode(Mode.command)
        # out.append(nop)
    # elif key == "h":
    if key == "h":
        out.append(Motion.left)
    elif key == "l":
        out.append(Motion.right)
    elif key == "j":
        out.append(Motion.down)
    elif key == "k":
        out.append(Motion.up)
    elif key == "i":
        setMode(Mode.insert)
        out.append(nop)
    elif key == "a":
        setMode(Mode.insert)
        out.append(Motion.right)
    elif key == "I":
        setMode(Mode.insert)
        out.append(Motion.goLineStart)
    elif key == "A":
        setMode(Mode.insert)
        out.append(Motion.goLineEnd)
    elif key == "w":
        out.append(Motion.goWordNext)
    elif key == "b":
        out.append(Motion.goWordPrevious)
    elif key == "G":
        out.append(Motion.goFileEnd)
    # elif key == "gg":
    #     out.append(Motion.goFileStart)
    elif key == "$":
        out.append(Motion.goLineEnd)
    elif key == "0":
        # If repeat count in progress, adds to that. Otherwise, BoL.
        if model.repeatInProgress():
            model.increaseRepeatCount(int(key))
            out.append(nop)
        else:
            out.append(Motion.goLineStart)
    elif key in "123456789" and len(key) == 1:
        model.increaseRepeatCount(int(key))
        out.append(nop)
    elif key == "^":
        out.append(Motion.goLineStart)
    elif key == "x":
        out.append(Keys.delete)
    elif key == "X":
        out.append(Keys.backspace)
    elif key == "f":
        out = seekLetter(out, key)
    elif key == "t":
        out = seekLetter(out, key, stopBeforeLetter=True)
    elif key == "F":
        out = seekLetter(out, key, backwards=True)
    elif key == "T":
        out = seekLetter(out, key, backwards=True, stopBeforeLetter=True)
    elif key == "u":
        out.append(Operator.undo)
    elif key == "<ctrl>r":
        out.append(Operator.redo)
    elif key == "J":
        out.extend([Motion.goEndOfLine,
                    Keys.delete,
                    Keys.space
                    ])
    # elif key == "ZZ":
    #     out.extend([operator.save,
    #         operator.quit])

    else:
        return unfoundKeyFallback(key)
    # TODO
    if isMode(Mode.operator_pending):
        out.insert(0, Operator.visualStart)
        out.append(0, Operator.visualPause)
        # TODO
    return out * model.getRepeatCount()

def unfoundKeyFallback(key):
    logger.info("Normal command not found: {}".format(key))
    if config.getConfigOption("swallow_unused_normal_keys"):
        return ""
    else:
        return key


def seekLetter(out, key, backwards=False, stopBeforeLetter=False):
    searchLetter = model.getSearchLetter(allow_none=True)
    if searchLetter is None:
        # Haven't specified which char to search for yet.
        model._pending_motion = key
        model.expecting_search_letter = True
        out.append(nop)
        return out
    else:
        if not model.expecting_clipboard:
            # Request clipboard and return.
            out = requestClipboard(out, backwards)
        else:
            # After f/t and seekLetter.
            # First have to deselect back to previous spot.
            # count from clipboard till index of next letter. TODO
            # Do it count times?
            out = getMovements(backwards, out, stopBeforeLetter)

    return out

def getMovements(backwards, out, stopBeforeLetter):
    # First have to deselect back to previous spot.
    # count from clipboard till index of next letter. TODO
    # Do it count times?
    clipboard = model.getCapturedClipboard()
    if backwards:
        out.append(Motion.right)  # deselect
        leftOrRight=Motion.left
        clipboard = clipboard[::-1]  # Reverse.
    else:
        out.append(Motion.left)  # deselect
        leftOrRight=Motion.right

    moveCount = getSeekCount(clipboard, model.getSearchLetter())
    if stopBeforeLetter and moveCount > 0:
        moveCount -= 1
    out.append(leftOrRight * moveCount)
    return out

def requestClipboard(out, backwards):
    # Request clipboard and return.
    out.append(Operator.visualStart)
    if backwards:
        out.append(Motion.goLineStart)
    else:
        out.append(Motion.goLineEnd)
    model.expecting_clipboard = True
    out.append(Keys.requestSelectedText)
    return out


def getSeekCount(string, searchLetter):
    try:
        moveCount = string.index(searchLetter)
    except ValueError:
        # Seeked character not in line. Don't move.
        moveCount = 0
    model.expecting_clipboard = False
    return moveCount

