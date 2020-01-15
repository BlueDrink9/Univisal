
import logging
import pathlib
try:
    from .library import *
    from . import logging_
    from .normal import normalCommand
    from .model import *
    from .motion import Motion
    from .operator import Operator
    from .handleKey import processOutput
    from . import config
except ImportError:
    from library import *
    import logging_
    from normal import normalCommand
    from model import *
    from motion import Motion
    from operator import Operator
    from handleKey import processOutput
    import config

def handle(cmd):
    if cmd == ":disable":
        setMode(Mode.disabled)
    elif cmd == ":enable":
        setMode(Mode.normal)
    elif cmd == ":getMode":
        return getMode().name
    elif cmd == ":getConfigDir":
        return config.getConfigDir()
    elif ":clipboard:" in cmd:
        return handlePendingClipboard(cmd)
    else:
        logger.error("Not a valid command: {cmd}".format(cmd))
    return None

def handlePendingClipboard(cmd):
    if not model.expecting_clipboard:
        logger.warning("Received command ':clipboard', \
                but not expecding it.  cmd: '{}'".format(cmd))
    if model.pending_motion is None:
        logger.warning("Received command ':clipboard', \
                but no pending motion.  cmd: '{}'".format(cmd))
    l = len(":clipboard:")
    cmd = cmd[l:]
    captured_clipboard = cmd
    commandOut = normalCommand([], model.getPendingMotion())
    return processOutput(commandOut)
