import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode, getCapturedClipboard
    from . import model
    from .motion import *
    from .operators import *
    from . import command
    from .remap import resolve_map
    from .adapter_maps import getAdapterMap
    from . import adapter_maps
    from .keys import Keys
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode, getCapturedClipboard
    import model
    from keys import Keys
    from motion import *
    from operators import *
    import command
    from remap import resolve_map
    from adapter_maps import getAdapterMap
    import adapter_maps
logger = logging.getLogger(__name__)


def normalCommand(out, key):
    if key == ":":
        setMode(Mode.command)
        out.append(nop)
    elif key == "h":
        out.append(getAdapterMap(Motion.left.name))
    elif key == "l":
        out.append(getAdapterMap(Motion.right.name))
    elif key == "j":
        out.append(getAdapterMap(Motion.down.name))
    elif key == "k":
        out.append(getAdapterMap(Motion.up.name))
    elif key == "0":
        out.append(getAdapterMap(Motion.goLineStart.name))
    elif key == "$":
        out.append(getAdapterMap(Motion.goLineEnd.name))
    elif key == "i":
        setMode(Mode.insert)
        out.append(nop)
    elif key == "a":
        setMode(Mode.insert)
        out.append(getAdapterMap(Motion.right.name))
    elif key == "I":
        setMode(Mode.insert)
        out.append(getAdapterMap(Motion.goLineStart.name))
    elif key == "A":
        setMode(Mode.insert)
        out.append(getAdapterMap(Motion.goLineEnd.name))
    elif key == "w":
        out.append(getAdapterMap(Motion.goWordNext.name))
    elif key == "b":
        out.append(getAdapterMap(Motion.goWordPrevious.name))
    elif key == "f":
        if model.clipboard_pending:
            # count from clipboard till index of next letter. TODO
            # Do it count times?
            # indexOf(model.getCapturedClipboard(), model.search_letter)
            pass
            model.clipboard_pending = False
        else:
            out.append(getAdapterMap(Operator.visualStart.name))
            out.append(getAdapterMap(Motion.goLineEnd.name))
            out.append(getAdapterMap(Operator.visualEnd.name))
            out.append(Keys.requestSelectedText)
            model.clipboard_pending = True
    else:
        logger.info("Normal command not found: {}".format(key))
        return None
    return out
