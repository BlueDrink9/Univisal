import string
import json
script_maps = { "alt": "<alt>",
                "alt_gr": "<alt_gr>",
                "backspace": "<backspace>",
                "capslock": "<capslock>",
                "ctrl": "<ctrl>",
                "delete": "<delete>",
                "up": "<up>",
                "down": "<down>",
                "right": "<right>",
                "left": "<left>",
                "return": "<enter>",
                "esc": "<escape>",
                # "f1-f12": "<f1>-\<f12>",
                "home": "<home>",
                "end": "<end>",
                "insert": "<insert>",
                "menu": "<menu>",
                "np_add": "<np_add>",
                "np_delete": "<np_delete>",
                "np_divide": "<np_divide>",
                "np_down": "<np_down>",
                "np_up": "<np_up>",
                "np_left": "<np_left>",
                "np_right": "<np_right>",
                "np_end": "<np_end>",
                "np_home": "<np_home>",
                "np_insert": "<np_insert>",
                "np_multiply": "<np_multiply>",
                "np_page_down": "<np_page_down>",
                "np_page_up": "<np_page_up>",
                "np_subtract": "<np_subtract>",
                "numlock": "<numlock>",
                "page_down": "<page_down>",
                "page_up": "<page_up>",
                "pause": "<pause>",
                "print_screen": "<print_screen>",
                "scroll_lock": "<scroll_lock>",
                "shift": "<shift>",
                # "space": "(space character)",
                "super": "<super>",
                "tab": "<tab>"
                }

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def mapPluginInputKey(key):
    if key in script_maps:
        return script_maps[key]
    else:
        return key

keys = list(string.ascii_letters + \
    string.digits + \
    string.punctuation)
keys.append("esc")

# Plugin folder needs to be added in autokey first.
folder = engine.get_folder("phrases")
for key in keys:
    modifiers = []
    if key.upper() != key.lower():
        if key.upper() == key:
            modifiers.append("<shift>")
    # Use lowercase for hotkey, with modifiers.
    hotkey = mapPluginInputKey(key.lower())
    phrase = "<script name=univi args={}>".format(key)
    # Actually creates a phrase, apparently.
    # engine.create_hotkey(folder, description, modifiers, key, contents)
    engine.create_hotkey(folder, key, modifiers, hotkey, phrase)
