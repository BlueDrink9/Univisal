import univisal
from univisal.keys import Keys
from univisal.handleInput import handleInput

nop="nop"
def translate_backspace(out):
    """
    Converts a string/list of keypresses according to univisal rules.
    Expands <bs> as a backspace.
    Pass in a string if no special keys, else pass in a list.
    """
    lookup = Keys.multikey_join_char.value
    joinChar = univisal.adapter_maps.getAdapterMap(lookup)
    if joinChar == lookup:  # Failed lookup.
        joinChar = ''
    bs = (Keys.backspace.value + joinChar)
    try:
        index = out.index(bs)
    except ValueError:
        bs = Keys.backspace.value
        index = out.index(bs)
    out = out[:index -1] + out[index + len(bs):]
    return out

def translate_keys(keys):
    """
    Pass in a string if no special keys, else pass in a list.
    """
    out = []
    for char in keys:
        handleResult = handleInput(char)
        out.append(handleResult)
    while nop in out:
        out.remove(nop)
    out = ''.join(out)
    # Simulate sending the backspaces. Do with string, not array, to ensure
    # normal commands not affected.
    while Keys.backspace.value in out:
        # need to iteratively replace <bs> with removed char
        out = translate_backspace(out)
    return ''.join(out)
