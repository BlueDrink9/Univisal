# enum from py >= 3.4
from enum import Enum, auto
import string

# Not using terms "edit" or "Ex" because they are less familiar.
class Mode(Enum):
    insert  = auto()
    command = auto()
    visual  = auto()
    normal  = auto()
    disabled  = auto()
    operator_pending  = auto()

_current_mode = None
pending_clipboard = None
pending_motion = None
captured_clipboard = None
registers = None
repeat_count = None

insertlike_modes = [
        Mode.insert,
        Mode.command,
        ]
def modeIsInsertLike():
    return _current_mode in insertlike_modes

def setMode(m):
    global _current_mode
    _current_mode = m

def getMode():
    return _current_mode

def isMode(m):
    return _current_mode == m

# Declare globals within a function to access them.
def init_model():
    global repeat_count, registers
    global pending_clipboard, pending_motion, captured_clipboard
    setMode(Mode.normal)
    registers = {}
    for l in string.ascii_letters:
        registers[l] = ""
    repeat_count = 1
    pending_clipboard = False
    pending_motion = None
    captured_clipboard = None

def getCapturedClipboard():
    global captured_clipboard
    out = captured_clipboard
    captured_clipboard = None
    return out

def getPendingMotion():
    global pending_motion
    out = pending_motion
    pending_motion = None
    return out
