from enum import Enum, auto

def delete():
    pass

class Operator(Enum):
    delete = auto()
    change = auto()
    yank = auto()
