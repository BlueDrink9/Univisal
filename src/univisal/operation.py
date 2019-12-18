from enum import Enum, auto
class Operation(Enum):
    delete = auto()
    copy = auto()
    yank = auto()
    change = auto()
