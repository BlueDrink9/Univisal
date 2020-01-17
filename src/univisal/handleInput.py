import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode
    from . import model
    from .normal import normalCommand
    from . import command
    from .handleKey import handleSingleInputKey
    from .adapter_maps import getAdapterMap
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode
    import model
    from normal import normalCommand
    import command
    from handleKey import handleSingleInputKey
    from adapter_maps import getAdapterMap
logger = logging.getLogger(__name__)

def handleInput(input_):
    logger.debug("handleInput input_: {}".format(input_))
    try:
        # nop = No operation. Need to send something back to adapter to signal finish.
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

        if model.expecting_search_letter:
            model.setSearchLetter(input_)
            return normalCommand([], model.pending_motion)

        return handleSingleInputKey(input_)
    except:
        return getFallbackOutput(input_)

def getFallbackOutput(input_):
    logger.critical("Unhandled exception handling input", exc_info=True)
    try:
        return getAdapterMap(input_)
    except:
        logger.critical("Unhandled exception while mapping adapter", exc_info=True)
        return input_
