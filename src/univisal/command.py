
import logging
try:
    from .library import *
    from . import logging_
    from .model import *
    from .motion import *
    from .operators import *
except ImportError:
    from library import *
    import logging_
    from model import *
    from motion import *
    from operators import *

def handle(cmd):
    if cmd == ":disable":
        setMode(Mode.disabled)
    elif cmd == ":enable":
        setMode(Mode.normal)
    else:
        logger.error("Not a valid command: {cmd}".format(cmd))
