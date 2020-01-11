import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode
    from . import model
    from .normal import normalCommand
    from . import Keys
    from . import Motion
    from . import Operator
    from . import command
    from .remap import resolve_map
    from .adapter_maps import getAdapterMap
    from . import adapter_maps
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode
    import model
    from normal import normalCommand
    import Keys
    import Motion
    import Operator
    import command
    from remap import resolve_map
    from adapter_maps import getAdapterMap
    import adapter_maps
logger = logging.getLogger(__name__)

# Reduce chance of a typo if returning nop
nop = "nop"
def handleKey(key_):
        logger.debug("key_: {}".format(key_))
        keys = resolve_map(key_)
        logger.debug("keys: {}".format(keys))
        # a map may turn one key into many, which we need to handle
        # individually.
        out = []
        for key in keys:
            if not isinstance(key, str):
                logger.warning("Error, handled key is not a string: '{}'", key)
            # esc regardless of mode, for now. (Still permits mappings.)
            if key.lower() == Keys.esc:
                setMode(Mode.normal)
                out.append(nop)
                continue

            if isMode(Mode.insert):
                out.append(getAdapterMap(key))
            elif isMode(Mode.normal):
                out = normalCommand(out, key)
            else:
                out.append(getAdapterMap(key))

        return processOutput(out)


def processOutput(output):
    # Only need nop if it's the only thing being returned.
    if len(output) > 1:
        try:
            output.remove(nop)
        except ValueError:
            pass
    return adapter_maps.getJoinChar().join(output)
