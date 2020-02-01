import logging
try:
    from .library import *
    from . import logger
    from .model import Mode, getMode, setMode, isMode
    from . import model
    from .normal import normalCommand
    from .keys import Keys
    from .motion import Motion
    from .vim_operator import Operator
    from . import command
    from .remap import resolve_map
    from .adapter_maps import getAdapterMap
    from . import adapter_maps
except ImportError:
    from library import *
    import logger
    from model import Mode, getMode, setMode, isMode
    import model
    from normal import normalCommand
    from keys import Keys
    from motion import Motion
    from vim_operator import Operator
    import command
    from remap import resolve_map
    from adapter_maps import getAdapterMap
    import adapter_maps
logger = logging.getLogger(__name__)

# Reduce chance of a typo if returning nop
nop = "nop"
def handleVimInputKey(inputKey):
    mappedKeys = preprocessKey(inputKey)
    # a map may turn one key into many, which we need to handle
    # individually.
    for key in mappedKeys:
        if not isinstance(key, str):
            logger.warning("Error, handled key is not a string: '{}'".format(key))

        # esc regardless of mode, for now. (Still permits mappings.)
        if isEsc(key):
            setMode(Mode.normal)
            addToOutput(nop)
            continue

        if isMode(Mode.insert):
            addToOutput(key)
        elif isMode(Mode.normal):
            normalCommand(key)
        else:
            addToOutput(key)

    return getOutputForAdapter()

def preprocessKey(key):
    logger.debug("handleSingleInputKey key_: {}".format(key))
    keys = resolve_map(key)
    logger.debug("handleSingleInputKey keys after mapping: {}".format(keys))
    return keys

def addToOutput(*keys):
    model.extendOutputKeys(*keys)

def isEsc(key):
    return key.lower() == Keys.esc.value

def getOutputForAdapter():
    return processOutput(model.popOutputKeys())

def processOutput(output):
    # Only need nop if it's the only thing being returned.
    output = stripNoOp(output)
    # Convert enums like operator, motion, key into str.
    output = convertOuputEnumsToStrings(output)
    return adapter_maps.getJoinChar().join(output)

def convertOuputEnumsToStrings(output):
    # Convert enums like operator, motion, key into str.
    for i, action in enumerate(output):
        if not isinstance(action, str):
            output[i] = getAdapterMap(action.value)
    return output

def stripNoOp(output):
    # Only need nop if it's the only thing being returned, and only need one.
    while output.count(nop) > 1:
        output.remove(nop)
    if len(output) > 1:
        try:
            output.remove(nop)
        except ValueError:
            pass
    return output
