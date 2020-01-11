from enum import Enum, auto
class Motion(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()
    goLineStart = auto()
    goLineEnd = auto()
    goFileStart = auto()
    goFileEnd = auto()
    goWordPrevious = auto()
    goWordNext = auto()
