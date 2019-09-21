# enum from py >= 3.4
from enum import Enum
import string
# Unique ensures values aren't duplicated.
@unique
class Mode(enum):
    normal  = 0
    insert  = 1
    visual  = 2
    command = 3

global mode
global repeat_count
global registers
registers = {}
mode = Mode.normal
# for l in string.ascii_letters:
#     registers[l] = ""

