import univisal
from univisal.handleInput import handleInput

def translate_backspace(out):
    """
    Converts a string/list of keypresses according to univisal rules.
    Expands <bs> as a backspace.
    Pass in a string if no special keys, else pass in a list.
    """
    lookup = "<multikey_join_char>"
    joinChar = univisal.adapter_maps.getAdapterMap(lookup)
    if joinChar == lookup:
        joinChar = ''
    bs = ("<bs>" + joinChar)
    try:
        index = out.index(bs)
    except ValueError:
        bs = "<bs>"
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
        out += handleResult
    out = ''.join(out)
    print(out)
    # Simulate sending the backspaces
    while "<bs>" in out:
        # need to iteratively replace <bs> with removed char
        out = translate_backspace(out)
    return ''.join(out)

def translate_keys(keys):
    # TODO: Handle visual selection, clipboard.
    out = []
    for char in keys:
        out += handleInput(char)
    out = ''.join(out)
    # Simulate sending the backspaces
    while "<bs>" in out:
        index = out.index("<bs>")
        out = out[:index -1] + out[index + len("<bs>"):]
    # need to iteratively replace <bs> with removed char
    return ''.join(out)

