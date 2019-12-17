# enum from py >= 3.4
from enum import Enum, auto
import string

# Not using terms "edit" or "Ex" because they are less familiar.
class Mode(Enum):
    insert  = auto()
    command = auto()
    visual  = auto()
    normal  = auto()
    operator_pending  = auto()

mode = None

def setMode(m):
    global mode
    mode = m

def getMode():
    global mode
    return mode

def isMode(m):
    global mode
    return mode == m

# Declare globals within a function to access them.
def init_model():
    global repeat_count
    global registers
    setMode(Mode.normal)
    registers = {}
    for l in string.ascii_letters:
        registers[l] = ""
    repeat_count = 1

