
import pathlib
try:
    from .library import *
    from .normal import normalCommand
    from .import model
    from .model import setMode, getMode, Mode
    from .motion import Motion
    from .vim_operator import Operator
    from .handleKey import processOutput
    from . import config
except ImportError:
    from library import *
    from normal import normalCommand
    import model
    from model import setMode, getMode, Mode
    from motion import Motion
    from vim_operator import Operator
    from handleKey import processOutput
    import config
logger = __import__("univisal.logger").logger.get_logger(__name__)

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
        # TODO: Raise InvalidCommandError and catch in caller.
    return None


def handlePendingClipboard(cmd):
    verifyPendingClipboard(cmd)
    l = len(":clipboard:")
    cmd = cmd[l:]
    model.captured_clipboard = cmd
    commandOut = normalCommand(model.getPendingMotion())
    return processOutput(commandOut)

def verifyPendingClipboard(cmd):
    if not model.expecting_clipboard:
        logger.warning("Received command ':clipboard', \
                but not expecding it.  cmd: '{}'".format(cmd))
    if model.getPendingMotion() is None:
        logger.warning("Received command ':clipboard', \
                but no pending motion.  cmd: '{}'".format(cmd))

