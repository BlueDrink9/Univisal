import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode
    from . import model
    from .normal import normalCommand
    from . import command
    from .handleKey import handleKey
    from .adapter_maps import getAdapterMap
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode
    import model
    from normal import normalCommand
    import command
    from handleKey import handleKey
    from adapter_maps import getAdapterMap
logger = logging.getLogger(__name__)

def handleInput(input_):
    logger.debug("input_: {}".format(input_))
    try:
        # nop = No op. Need to send something back to adapter to signal finish.
        # Reduce chance of a typo if returning nop
        nop = "nop"

        # For specific commands sent from adapter, e.g. `:disable`.
        # These should be handled specially, before other logic.
        if len(input_) > 1 and input_[0] == ":":
            out = command.handle(input_)
            if out is None:
                return nop
            else:
                return out
        # Disabled: always return input key.
        if isMode(Mode.disabled):
            return input_

        if model.pending_clipboard:
            if model.captured_clipboard is None:
                logger.error("Pending clipboard, but none was given \
                        (captured_clipboard is blank). \ key: '{}'".format(input_))
            return normalCommand([], model.pending_motion)

        print('input_', input_)
        return handleKey(input_)
    except:
        logger.critical("Unhandled exception", exc_info=True)
        try:
            return getAdapterMap(input_)
        except:
            logger.critical("Unhandled exception while mapping adapter", exc_info=True)
            return input_
