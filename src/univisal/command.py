
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
    elif ":clipboard:" in cmd:
        if not model.clipboard_pending:
            logger.warning("Received command ':clipboard', \
                    but not expecding it.  cmd: '{}'".format(cmd))
        l = len(":clipboard:")
        cmd = cmd[l:]
        captured_clipboard = cmd
        return normalCommand(model.cmd)
    else:
        logger.error("Not a valid command: {cmd}".format(cmd))
    return None
