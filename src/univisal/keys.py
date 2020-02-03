# enum from py >= 3.4
from enum import Enum

class Keys(Enum):
    delete  = "<del>"
    backspace  = "<bs>"
    space  = "<space>"
    esc  = "<esc>"
    multikey_join_char = "<multikey_join_char>"
    requestSelectedText = "<requestSelectedText>"
    # nop = No operation. Need to send something back to adapter to signal finish.
    # Reduce chance of a typo if returning nop
    nop = "nop"
