import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode, getCapturedClipboard
    from . import model
    from . import Motion
    from . import Operator
    from .remap import resolve_map
    from .adapter_maps import getAdapterMap
    from . import adapter_maps
    from . import Keys
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode, getCapturedClipboard
    import model
    import Keys
    import Motion
    import Operator
    from remap import resolve_map
    from adapter_maps import getAdapterMap
    import adapter_maps
logger = logging.getLogger(__name__)


def convertForOutput(action):
    return getAdapterMap(action)
    # return getAdapterMap(action.name)

# Reduce chance of a typo if returning nop
nop = "nop"

def normalCommand(out, key):
    # Command mode does nothing atm, so don't handle this key.
    # if key == ":":
        # setMode(Mode.command)
        # out.append(nop)
    # elif key == "h":
    if key == "h":
        out.append(convertForOutput(Motion.left))
    elif key == "l":
        out.append(convertForOutput(Motion.right))
    elif key == "j":
        out.append(convertForOutput(Motion.down))
    elif key == "k":
        out.append(convertForOutput(Motion.up))
    elif key == "i":
        setMode(Mode.insert)
        out.append(nop)
    elif key == "a":
        setMode(Mode.insert)
        out.append(convertForOutput(Motion.right))
    elif key == "I":
        setMode(Mode.insert)
        out.append(convertForOutput(Motion.goLineStart))
    elif key == "A":
        setMode(Mode.insert)
        out.append(convertForOutput(Motion.goLineEnd))
    elif key == "w":
        out.append(convertForOutput(Motion.goWordNext))
    elif key == "b":
        out.append(convertForOutput(Motion.goWordPrevious))
    elif key == "G":
        out.append(convertForOutput(Motion.goFileEnd))
    # elif key == "gg":
    #     out.append(convertForOutput(Motion.goFileStart))
    elif key == "$":
        out.append(convertForOutput(Motion.goLineEnd))
    elif key == "0":
        # If repeat count in progress, adds to that. Otherwise, BoL.
        if model.repeat_count > 1:
            model.increaseRepeatCount(key)
            out.append(nop)
        else:
            out.append(convertForOutput(Motion.goLineStart))
    elif key in "123456789" and len(key == 1):
        model.increaseRepeatCount(key)
        out.append(nop)
    elif key == "^":
        out.append(convertForOutput(Motion.goLineStart))
    elif key == "x":
        out.append(convertForOutput(Key.delete))
    elif key == "X":
        out.append(convertForOutput(Key.backspace))
    elif key == "f":
        out = seekLetter(out, key)
    elif key == "t":
        out = seekLetter(out, key, stopBeforeLetter=True)
    elif key == "F":
        out = seekLetter(out, key, backwards=True)
    elif key == "T":
        out = seekLetter(out, key, backwards=True, stopBeforeLetter=True)
    elif key == "u":
        out.append(convertForOutput(operator.undo))
    elif key == "<ctrl>r":
        out.append(convertForOutput(operator.redo))
    elif key == "J":
        out.extend([convertForOutput(motion.goEndOfLine),
                    convertForOutput(Keys.delete),
                    convertForOutput(keys.space)
                    ])
    # elif key == "ZZ":
    #     out.extend([convertForOutput(operator.save),
    #         convertForOutput(getAdapterMap(operator.quit)])

    else:
        logger.info("Normal command not found: {}".format(key))
        return key
    if isMode(Mode.operator_pending):
        out.insert(0, Operator.visualStart)
        out.append(0, Operator.visualPause)
        # TODO
    return out


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
            out.append(getAdapterMap(Operator.visualStart))
            if backwards:
                out.append(getAdapterMap(Motion.goLineStart))
            else:
                out.append(getAdapterMap(Motion.goLineEnd))
            model.expecting_clipboard = True
            out.append(Keys.requestSelectedText)
            return out
        else:
            # After f/t and seekLetter.
            # First have to deselect back to previous spot.
            # count from clipboard till index of next letter. TODO
            # Do it count times?
            clipboard = model.getCapturedClipboard()
            if backwards:
                out.append(convertForOutput(Motion.right))
                leftOrRight=Motion.left
                clipboard = clipboard[::-1]  # Reverse.
            else:
                out.append(convertForOutput(Motion.left))
                leftOrRight=Motion.right
            moveCount = getSeekCount(clipboard, model.getSearchLetter())
            if stopBeforeLetter and moveCount > 0:
                moveCount -= 1
            out.append(convertForOutput(leftOrRight) * moveCount)

    return out


def getSeekCount(string, searchLetter):
    try:
        moveCount = string.index(searchLetter)
    except ValueError:
        # Seeked character not in line. Don't move.
        moveCount = 0
    model.expecting_clipboard = False
    return moveCount

