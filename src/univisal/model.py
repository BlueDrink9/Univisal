# enum from py >= 3.4
from enum import Enum, auto
import string
try:
    pass
except ImportError:
    pass
logger = __import__("univisal.logger").logger.get_logger(__name__)

# Not using terms "edit" or "Ex" because they are less familiar.
class Mode(Enum):
    insert  = auto()
    command = auto()
    visual  = auto()
    normal  = auto()
    disabled  = auto()
    operator_pending  = auto()

__outputKeys = None
_registers = None
_current_mode = None

__repeat_count = None
expecting_clipboard = None
expecting_search_letter = None
_pending_motion = None
_captured_clipboard = None
_search_letter = None

# Declare globals within a function to access them.
def init_model():
    global __outputKeys
    __outputKeys = []
    setMode(Mode.normal)
    init_registers()
    clear_pending()

def init_registers():
    global _registers
    _registers = {}
    for l in string.ascii_letters:
        _registers[l] = ""

def clear_pending():
    global expecting_clipboard, _pending_motion, _captured_clipboard, expecting_search_letter
    resetRepeatCount()
    expecting_clipboard = False
    expecting_search_letter = False
    _pending_motion = None
    _captured_clipboard = None
    _search_letter = None


insertlike_modes = [
        Mode.insert,
        Mode.command,
        ]
def modeIsInsertLike():
    return _current_mode in insertlike_modes

def setMode(m):
    global _current_mode
    checkValidMode(m)
    _current_mode = m
    if isMode(Mode.normal):
        # This is a hidden behavior. Should it really be here?
        clear_pending()
    logger.info("Mode set to '{}'".format(m))

def getMode():
    return _current_mode

def isMode(m):
    checkValidMode(m)
    return _current_mode == m

def checkValidMode(m):
    if not isinstance(m, Mode):
        logger.error("Not a valid mode: '{}'".format(m))

def resetRepeatCount():
    global __repeat_count
    __repeat_count = 0

def getCapturedClipboard():
    global _captured_clipboard
    if _captured_clipboard is None:
        if expecting_clipboard:
            logger.error("Pending clipboard, but none was given \
                        (captured_clipboard is blank).")
        logger.warning("Clipboard was requested, but is None. Returning '' instead.")
        return ''
    out = _captured_clipboard
    _captured_clipboard = None
    return out

def getPendingMotion():
    global _pending_motion
    out = _pending_motion
    _pending_motion = None
    return out

def getSearchLetter(allow_none=False):
    if not (isinstance(_search_letter, str) or \
            (_search_letter is None and allow_none)):
        logger.warning("model._search_letter is not a str. \
                Is '{}', of type {}".format(_search_letter, type(_search_letter)))
    return _search_letter

def setSearchLetter(l):
    global _search_letter, expecting_search_letter
    _search_letter = l
    expecting_search_letter = False

def getRepeatCount():
    if repeatInProgress():
        return __repeat_count
    else:
        return 1

def repeatInProgress():
    return __repeat_count > 0

def increaseRepeatCount(count):
    global __repeat_count
    # Will never be 12 because 12 == 1 2
    if repeatInProgress():
        __repeat_count = 10*__repeat_count + count
    else:
        __repeat_count = count

def popOutputKeys():
    global __outputKeys
    tmp = __outputKeys
    __outputKeys = []
    return tmp

def extendOutputKeys(*keys):
    if isinstance(*keys, str):
        extend = [keys]
    else:
        extend = keys
    __outputKeys.extend(*extend)

def repeatOutputKeys():
    global __outputKeys
    __outputKeys *= getRepeatCount()
