# enum from py >= 3.4
from enum import Enum, auto
import string
import logging
try:
    from . import logging_
except ImportError:
    import logging_
logger = logging.getLogger(__name__)

# Not using terms "edit" or "Ex" because they are less familiar.
class Mode(Enum):
    insert  = auto()
    command = auto()
    visual  = auto()
    normal  = auto()
    disabled  = auto()
    operator_pending  = auto()

_current_mode = None
_registers = None
_search_letter = None
_pending_motion = None
_captured_clipboard = None
pending_clipboard = None
pending_search_letter = None
repeat_count = None

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
        clear_pending()

def getMode():
    return _current_mode

def isMode(m):
    checkValidMode(m)
    return _current_mode == m

def checkValidMode(m):
    if not isinstance(m, Mode):
        logger.error("Not a valid mode: '{}'".format(m))

# Declare globals within a function to access them.
def init_model():
    global _registers
    setMode(Mode.normal)
    registers = {}
    for l in string.ascii_letters:
        registers[l] = ""
    clear_pending()

def clear_pending():
    global repeat_count, pending_clipboard, _pending_motion, _captured_clipboard, pending_search_letter
    repeat_count = 1
    pending_clipboard = False
    pending_search_letter = None
    pending_motion = None
    captured_clipboard = None

def getCapturedClipboard():
    global _captured_clipboard
    if _captured_clipboard is None:
        if pending_clipboard:
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
    global _search_letter, pending_search_letter
    _search_letter = l
    pending_search_letter = None
