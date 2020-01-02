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
    from . import adapter_maps
except ImportError:
    from library import *
    import logging_
    from model import *
    from motion import *
    from operators import *
    from remap import resolve_map, resolve_map
    from adapter_maps import getAdapterMap
    import adapter_maps
logger = logging.getLogger(__name__)



def handleKey(key):
    try:
        # nop = No op. Need to send something back to adapter to signal finish.
        # Reduce chance of a typo if returning nop
        nop = "nop"

        keys = resolve_map(key)
        # a map may turn one key into many, which we need to handle
        # individually.
        out = []
        for key in keys:
            # esc regardless of mode, for now. But still permit mappings.
            if key.lower() == "<esc>":
                setMode(Mode.normal)
                out.append(nop)
                continue

            if isMode(Mode.insert):
                out.append(getAdapterMap(key))
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
            else:
                out.append(getAdapterMap(key))

        # Only need nop if it's the only thing being returned.
        if len(out) > 1:
            try:
                out.remove(nop)
            except ValueError:
                pass
        return adapter_maps.getJoinChar().join(out)

    except:
        logger.critical("Unhandled exception", exc_info=True)
        try:
            return getAdapterMap(key)
        except:
            logger.critical("Unhandled exception while mapping adapter", exc_info=True)
            return key
