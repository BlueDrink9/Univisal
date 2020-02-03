# enum from py >= 3.4
from enum import Enum, auto

# TODO: enums with the same value are aliased to the same thing. Consider
# looking for a better way to store this. `Aenum`?
class Operator(Enum):
    delete = "<delete>"
    change = "<delete>"
    yank = "<yank>"
    # Start: hold shift down. Pause: release shift. End: deselect. Note that ending
    # may be done directionally instead.
    visualStart = "<visualStart>"
    visualPause = "<visualPause>"
    # visualEnd = "<visualEnd>"
    # Always end visual as if it had extended to the right.
    # I can't think of an easy way to tell if it extended right or left, at least
    # not without copying the text a lot.
    visualEnd = "<right>"
    # These may use ctrl, may use something else. So let adapter map them.
    undo = "<undo>"
    redo = "<redo>"
