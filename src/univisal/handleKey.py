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
logger = __import__("univisal.logger").logger.get_logger(__name__)

def handleVimInputKey(inputKey):
    mappedKeys = preprocessKey(inputKey)
    # a map may turn one key into many, which we need to handle
    # individually.
    for key in mappedKeys:
        if not isinstance(key, str):
            logger.warning("Error, handled key is not a string: '{}'".format(key))

        # esc regardless of mode, for now. (Still permits mappings.)
        if isEsc(key):
            # When entering normal from insert mode, cursor moves one to the
            # left to be 'on' the right key. In visual, just ends the
            # selection.
            if not isMode(Mode.normal):
                addToOutput(Motion.left)
            setMode(Mode.normal)
            continue

        if isMode(Mode.insert):
            addToOutput(key)
        elif isMode(Mode.normal):
            normalCommand(key)
        else:
            addToOutput(key)

    applyPendingVimModifications()
    keysForOutput = model.popOutputKeys()
    formattedOut = formatOutputForAdapter(keysForOutput)
    return formattedOut

def preprocessKey(key):
    logger.debug("handleSingleInputKey key_: {}".format(key))
    keys = resolve_map(key)
    logger.debug("handleSingleInputKey keys after mapping: {}".format(keys))
    return keys

def addToOutput(*keys):
    model.extendOutputKeys(*keys)

def isEsc(key):
    return key.lower() == Keys.esc.value

def applyPendingVimModifications():
    model.repeatOutputKeys()
    model.applyPendingOperator()

def formatOutputForAdapter(output):
    # Only need nop if it's the only thing being returned.
    output = stripNoOp(output)
    if len(output) == 0:
        output.append(Keys.nop)
    # Convert enums like operators, motions, keys into str.
    output = convertOuputEnumsToStrings(output)
    return joinForAdapter(output)

def joinForAdapter(output):
    return adapter_maps.getJoinChar().join(output)

def convertOuputEnumsToStrings(output):
    # Convert enums like operator, motion, key into str.
    for i, action in enumerate(output):
        if not isinstance(action, str):
            output[i] = getAdapterMap(action.value)
    return output

def stripNoOp(output):
    # Only need nop if it's the only thing being returned, and only need one.
    nop = Keys.nop
    while output.count(nop) > 1:
        output.remove(nop)
    if len(output) > 1:
        try:
            output.remove(nop)
        except ValueError:
            pass
    return output
