from json import loads as json_load
import logging
try:
    from .library import *
    from . import logging_
    from .model import *
    from .motion import *
    from .operators import *
    from .remap import resolve_map
    from .adapter_maps import getAdapterMap
except ImportError:
    from library import *
    import logging_
    from model import *
    from motion import *
    from operators import *
    from remap import resolve_imap, resolve_nmap
    from adapter_maps import getAdapterMap
logger = logging.getLogger(__name__)



def handleKey(key):
    try:
        # Reduce chance of a typo if returning nop
        nop = "nop"

        key = resolve_map(key)
        # esc regardless of mode, for now. But still permit mappings.
        if key.lower() == "<esc>":
            setMode(Mode.normal)
            # No op. Need to send something back to signal finish.
            return nop

        if isMode(Mode.insert):
            return getAdapterMap(key)
        elif key == "h":
            return getAdapterMap(Motion.left.name)
        elif key == "l":
            return getAdapterMap(Motion.right.name)
        elif key == "j":
            return getAdapterMap(Motion.down.name)
        elif key == "k":
            return getAdapterMap(Motion.up.name)
        elif key == "0":
            return getAdapterMap(Motion.goLineStart.name)
        elif key == "$":
            return getAdapterMap(Motion.goLineEnd.name)
        elif key == "i":
            setMode(Mode.insert)
            return nop
        elif key == "a":
            setMode(Mode.insert)
            return getAdapterMap(Motion.right.name)
        elif key == "I":
            setMode(Mode.insert)
            return getAdapterMap(Motion.goLineStart.name)
        elif key == "A":
            setMode(Mode.insert)
            return getAdapterMap(Motion.goLineEnd.name)
        elif key == "w":
            return getAdapterMap(Motion.goWordNext.name)
        elif key == "b":
            return getAdapterMap(Motion.goWordPrevious.name)
        else:
            return getAdapterMap(key)
    except:
        logger.critical("Unhandled exception", exc_info=True)
        try:
            return getAdapterMap(key)
        except:
            logger.critical("Unhandled exception while mapping adapter", exc_info=True)
            return key
