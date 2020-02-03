try:
    from .library import *
    from .model import Mode, getMode, setMode, isMode, getCapturedClipboard
    from . import model
    from . import config
    from .motion import Motion
    from .vim_operator import Operator
    from .remap import resolve_map
    from .keys import Keys
except ImportError:
    from library import *
    from model import Mode, getMode, setMode, isMode, getCapturedClipboard
    import model
    import config
    from keys import Keys
    from motion import Motion
    from vim_operator import Operator
    from remap import resolve_map
logger = __import__("univisal.logger").logger.get_logger(__name__)

def normalCommand(key):
    # Command mode does nothing atm, so don't handle this key.
    # if key == ":":
        # setMode(Mode.command)
        # addToOutput(Keys.nop)
    # elif key == "h":
    if key == "0":
        # If repeat count in progress, adds to that. Otherwise, BoL.
        if model.repeatInProgress():
            model.increaseRepeatCount(int(key))
            addToOutput(Keys.nop)
        else:
            doMotionOrSelection(Motion.goLineStart)
    elif key in "123456789" and len(key) == 1:
        model.increaseRepeatCount(int(key))
        addToOutput(Keys.nop)
    elif key == "i":
        setMode(Mode.insert)
        addToOutput(Keys.nop)
    elif key == "a":
        setMode(Mode.insert)
        doMotionOrSelection(Motion.right)
    elif key == "I":
        setMode(Mode.insert)
        doMotionOrSelection(Motion.goLineStart)
    elif key == "A":
        setMode(Mode.insert)
        doMotionOrSelection(Motion.goLineEnd)
    elif key == "h":
        doMotionOrSelection(Motion.left)
    elif key == "l":
        doMotionOrSelection(Motion.right)
    elif key == "j":
        doMotionOrSelection(Motion.down)
    elif key == "k":
        doMotionOrSelection(Motion.up)
    elif key == "w":
        doMotionOrSelection(Motion.goWordNext)
    elif key == "b":
        doMotionOrSelection(Motion.goWordPrevious)
    elif key == "G":
        doMotionOrSelection(Motion.goFileEnd)
    # elif key == "gg":
    #     doMotionOrSelection(Motion.goFileStart)
    elif key == "$":
        doMotionOrSelection(Motion.goLineEnd)
    elif key == "^":
        doMotionOrSelection(Motion.goLineStart)
    elif key == "x":
        doAction(Keys.delete)
    elif key == "X":
        doAction(Keys.backspace)
    elif key == "f":
        doMotionOrSelection(seekLetter(key))
    elif key == "t":
        doMotionOrSelection(seekLetter(key, stopBeforeLetter=True))
    elif key == "F":
        doMotionOrSelection(seekLetter(key, backwards=True))
    elif key == "T":
        doMotionOrSelection(seekLetter(key, backwards=True, stopBeforeLetter=True))
    elif key == "u":
        doVimOperator(Operator.undo)
    elif key == "<ctrl>r":
        doVimOperator(Operator.redo)
    elif key == "J":
        doAction([Motion.goEndOfLine,
                    Keys.delete,
                    Keys.space,
                    ])
    elif key == "d":
        doVimOperator(Operator.delete)
    elif key == "y":
        doVimOperator(Operator.yank)
    elif key == "c":
        doVimOperator(Operator.delete)
        setMode(Mode.insert)
    # elif key == "ZZ":
    #     out.extend([operator.save,
    #         operator.quit])

    else:
        addToOutput(unfoundKeyFallback(key))
    return

def doMotionOrSelection(motion):
    if model.pending_operator:
        addToOutput(*doSelection(motion))
        model.apply_pending_operator=True
    else:
        addToOutput(motion)

def doSelection(motion):
    return Operator.visualStart, motion, Operator.visualPause

def doAction(action):
    addToOutput(action)

def doVimOperator(op):
    if isMode(Mode.visual):
        addToOutput(op)
        setMode(Mode.normal)
        return
    elif model.pending_operator:
        if op == model.pending_operator:
            addToOutput(Motion.selectCurrentLine)
        else:
            setMode(Mode.normal)
        addToOutput(op)
        return
    else:
        addToOutput(Keys.nop)
        model.pending_operator = op

def addToOutput(*keys):
    model.extendOutputKeys(*keys)

def unfoundKeyFallback(key):
    logger.info("Normal command not found: {}".format(key))
    if config.getConfigOption("swallow_unused_normal_keys"):
        return ""
    else:
        return key


def seekLetter(key, backwards=False, stopBeforeLetter=False):
    searchLetter = model.getSearchLetter(allow_none=True)
    if searchLetter is None:
        # Haven't specified which char to search for yet.
        model._pending_motion = key
        model.expecting_search_letter = True
        return Keys.nop
    else:
        if not model.expecting_clipboard:
            # Request clipboard and return.
            return requestClipboard(backwards)
        else:
            # After f/t and seekLetter.
            # First have to deselect back to previous spot.
            # count from clipboard till index of next letter. TODO
            # Do it count times?
            return getMovements(backwards, stopBeforeLetter)


def getMovements(backwards, stopBeforeLetter):
    # First have to deselect back to previous spot.
    # count from clipboard till index of next letter. TODO
    # Do it count times?
    movements = []
    clipboard = model.getCapturedClipboard()
    if backwards:
        movements.append(Motion.right)  # deselect
        leftOrRight=Motion.left
        clipboard = clipboard[::-1]  # Reverse.
    else:
        movements.append(Motion.left)  # deselect
        leftOrRight=Motion.right

    moveCount = getSeekCount(clipboard, model.getSearchLetter())
    if stopBeforeLetter and moveCount > 0:
        moveCount -= 1
    movements.append(leftOrRight * moveCount)
    return movements

def requestClipboard(backwards):
    requestKeys = []
    # Request clipboard and return.
    requestKeys.append(Operator.visualStart)
    if backwards:
        requestKeys.append(Motion.goLineStart)
    else:
        requestKeys.append(Motion.goLineEnd)
    model.expecting_clipboard = True
    requestKeys.append(Keys.requestSelectedText)
    return requestKeys


def getSeekCount(string, searchLetter):
    try:
        moveCount = string.index(searchLetter)
    except ValueError:
        # Seeked character not in line. Don't move.
        moveCount = 0
    model.expecting_clipboard = False
    return moveCount

