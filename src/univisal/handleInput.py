try:
    from .library import *
    from .model import Mode, getMode, setMode, isMode
    from . import model
    from .normal import normalCommand
    from . import command
    from .handleKey import handleVimInputKey
    from .adapter_maps import getAdapterMap
    from .keys import Keys
except ImportError:
    from library import *
    from model import Mode, getMode, setMode, isMode
    import model
    from normal import normalCommand
    import command
    from handleKey import handleVimInputKey
    from adapter_maps import getAdapterMap
    from keys import Keys
logger = __import__("univisal.logger").logger.get_logger(__name__)

def handleInput(input_):
    logger.debug("handleInput input_: {}".format(input_))
    try:
        return handleInputUnsafe(input_)
    except:
        return getFallbackOutput(input_)

def handleInputUnsafe(input_):
    inputIsCommandlike = len(input_) > 1 and input_[0] == ":"
    if inputIsCommandlike:
        # For specific commands sent from adapter, e.g. `:disable`.
        # These should be handled specially, before other logic.
        return handleUnivisalCommand(input_)
    # Disabled: always return input key.
    if isMode(Mode.disabled):
        return input_
    if model.expecting_search_letter:
        return handleExpectedSearchLetter(input_)

    # The default response
    return handleVimInputKey(input_)

def handleUnivisalCommand(input_):
    # For specific commands sent from adapter, e.g. `:disable`.
    # These should be handled specially, before other logic.
    commandResult = command.handle(input_)
    if commandResult is None:
        return Keys.nop
    else:
        return commandResult

def handleExpectedSearchLetter(input_):
    model.setSearchLetter(input_)
    normalCommand(model.getPendingMotion())
    return model.popOutputKeys()

def getFallbackOutput(input_):
    logger.critical("Unhandled exception handling input", exc_info=True)
    try:
        return getAdapterMap(input_)
    except:
        logger.critical("Unhandled exception while mapping adapter", exc_info=True)
        return input_

