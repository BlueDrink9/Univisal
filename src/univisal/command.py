
import logging
import pathlib
try:
    from .library import *
    from . import logging_
    from .model import *
    from .motion import *
    from .operators import *
    from . import config
except ImportError:
    from library import *
    import logging_
    from model import *
    from motion import *
    from operators import *
    import config

def handle(cmd):
    if cmd == ":disable":
        setMode(Mode.disabled)
    elif cmd == ":enable":
        setMode(Mode.normal)
    elif cmd == ":getMode":
        return getMode().name
    elif cmd == ":getConfigDir":
        # Get basedir
        return config.getConfigDir()
    else:
        logger.error("Not a valid command: {cmd}".format(cmd))
    return None
