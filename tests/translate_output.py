import univisal
from univisal.keys import Keys
from univisal.handleInput import handleInput

nop="nop"

def translate_keys(keys):
    """
    Pass in a string if no special keys, else pass in a list.
    """
    out = []
    for char in keys:
        handleResult = handleInput(char)
        out.append(handleResult)
    out = trimNop(out)
    out = ''.join(out)
    # Simulate sending the backspaces. Do with string, not array, to ensure
    # normal commands not affected.
    while Keys.backspace.value in out:
        # need to iteratively replace <bs> with removed char
        out = translate_backspace(out)
    out = trimJoinChar(out)
    return ''.join(out)

def trimNop(out):
    while nop in out:
        out.remove(nop)
    return out

def trimJoinChar(out):
    joinChar = univisal.adapter_maps.getJoinChar()
    out = out.replace(joinChar, "")
    return out

def translate_backspace(out):
    """
    Converts a string/list of keypresses according to univisal rules.
    Expands <bs> as a backspace.
    Pass in a string if no special keys, else pass in a list.
    """
    joinChar = univisal.adapter_maps.getJoinChar()
    bs = (Keys.backspace.value + joinChar)
    try:
        index = out.index(bs)
    except ValueError:
        bs = Keys.backspace.value
        index = out.index(bs)
    out = out[:index -1] + out[index + len(bs):]
    return out
