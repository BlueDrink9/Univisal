from enum import Enum, auto
class Motion(Enum):
    goLineStart = auto()
    goLineEnd = auto()
    goFileStart = auto()
    goFileEnd = auto()
    goWordPrevious = auto()
    goWordNext = auto()
    visualStart = auto()
    visualEnd = auto()
