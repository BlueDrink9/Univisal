# enum from py >= 3.4
from enum import Enum
import string
class Mode(Enum):
    normal  = 0
    insert  = 1
    visual  = 2
    command = 3

def setMode(m):
    global mode
    mode = m

def getMode(m):
    global mode
    return mode

# TODO: Refresh memory of python global usage.
global mode
global repeat_count
global registers
registers = {}
mode = Mode.normal
# for l in string.ascii_letters:
#     registers[l] = ""

