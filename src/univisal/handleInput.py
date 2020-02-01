try:
    from .library import *
    from .model import Mode, getMode, setMode, isMode
    from . import model
    from .normal import normalCommand
    from . import command
    from .handleKey import handleVimInputKey
    from .adapter_maps import getAdapterMap
except ImportError:
    from library import *
    from model import Mode, getMode, setMode, isMode
    import model
    from normal import normalCommand
    import command
    from handleKey import handleVimInputKey
    from adapter_maps import getAdapterMap
logger = __import__("univisal.logger").logger.get_logger(__name__)

def handleInput(input_):
    logger.debug("handleInput input_: {}".format(input_))
    try:
        # nop = No operation. Need to send something back to adapter to signal finish.
        # Reduce chance of a typo if returning nop
        nop = "nop"

        # For specific commands sent from adapter, e.g. `:disable`.
        # These should be handled specially, before other logic.
        if len(input_) > 1 and input_[0] == ":":
            commandResult = command.handle(input_)
            if commandResult is None:
                return nop
            else:
                return commandResult
            return
        # Disabled: always return input key.
        if isMode(Mode.disabled):
            return input_

        if model.expecting_search_letter:
            model.setSearchLetter(input_)
            normalCommand(model.pending_motion)
            return model.popOutputKeys()

        return handleVimInputKey(input_)
    except:
        return getFallbackOutput(input_)

def getFallbackOutput(input_):
    logger.critical("Unhandled exception handling input", exc_info=True)
    try:
        return getAdapterMap(input_)
    except:
        logger.critical("Unhandled exception while mapping adapter", exc_info=True)
        return input_

