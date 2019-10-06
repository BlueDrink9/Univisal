from enum import Enum
class Motion(Enum):
    goLineStart = "goLineStart"
    goLineEnd = "goLineEnd"
    goFileStart = "goFileStart"
    goFileEnd = "goFileEnd"
    goWordPrevious = "goWordPrevious"
    goWordNext = "goWordNext"
    visualStart = "visualStart"
    visualEnd = "visualEnd"
