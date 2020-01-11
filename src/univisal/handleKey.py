import logging
try:
    from .library import *
    from . import logging_
    from .model import Mode, getMode, setMode, isMode
    from . import model
    from .normal import normal_command
    from .keys import Keys
    from .motion import *
    from .operators import *
    from . import command
    from .remap import resolve_map
    from .adapter_maps import getAdapterMap
    from . import adapter_maps
except ImportError:
    from library import *
    import logging_
    from model import Mode, getMode, setMode, isMode
    import model
    from normal import normal_command
    from keys import Keys
    from motion import *
    from operators import *
    import command
    from remap import resolve_map
    from adapter_maps import getAdapterMap
    import adapter_maps
logger = logging.getLogger(__name__)

# TODO rename file, separate out handling of command vs key.
# def handleInput()

def handleKey(key_):
    try:
        # nop = No op. Need to send something back to adapter to signal finish.
        # Reduce chance of a typo if returning nop
        nop = "nop"

        # For specific commands sent from adapter, e.g. `:disable`.
        # These should be handled specially, before other logic.
        # Still expect key_ to be a list.
        if len(key_) > 1 and key_[0] == ":":
            out = command.handle(key_)
            if out is None:
                return nop
            else:
                return out
        # Disabled: always return input key.
        if isMode(Mode.disabled):
            return key_

        if model.pending_clipboard:
            if model.captured_clipboard is None:
                logger.error("Pending clipboard, but none was given \
                        (captured_clipboard is blank). \ key: '{}'".format(cmd))
            return normalCommand(model.pending_motion)

        keys = resolve_map(key_)
        # a map may turn one key into many, which we need to handle
        # individually.
        out = []
        for key in keys:
            if not isinstance(key, str):
                logger.warning("Error, handled key is not a string: '{}'", key)
            # esc regardless of mode, for now. (Still permits mappings.)
            if key.lower() == Keys.esc.value:
                setMode(Mode.normal)
                out.append(nop)
                continue

            if isMode(Mode.insert):
                out.append(getAdapterMap(key))
            elif isMode(Mode.normal):
                action = normalCommand(out, key)
                if action is None:
                    out.append(getAdapterMap(key))
                else:
                    out.append(getAdapterMap(action))
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
            return getAdapterMap(key_)
        except:
            logger.critical("Unhandled exception while mapping adapter", exc_info=True)
            return key_
