# enum from py >= 3.4
from enum import Enum

class Motion(Enum):
    up = "<up>"
    down = "<down>"
    left = "<left>"
    right = "<right>"
    goLineStart = "<goLineStart>"
    goLineEnd = "<goLineEnd>"
    goFileStart = "<goFileStart>"
    goFileEnd = "<goFileEnd>"
    goWordPrevious = "<goWordPrevious>"
    goWordNext = "<goWordNext>"
