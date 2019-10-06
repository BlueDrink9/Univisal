import string
import json
from ../../src/adapter_maps import *
from ../../src/library import *

keys = list(string.ascii_letters + \
    string.digits + \
    string.punctuation)
keys.append("esc")

# Plugin folder needs to be added in autokey first.
folder = engine.get_folder("phrases")
for key in keys:
    modifiers = []
    description = key
    if key.upper() != key.lower():
        if key.upper() == key:
            modifiers.append("<shift>")
            description = "shift"+key
    # Use lowercase for hotkey, with modifiers.
    hotkey = getAdapterMap(key.lower())
    phrase = "<script name=univi args={}>".format(key)
    # Actually creates a phrase, apparently.
    # engine.create_hotkey(folder, description, modifiers, key, contents)
    engine.create_hotkey(folder, description, modifiers, hotkey, phrase)

phrase = "<script name=univi args={}>".format("esc")
engine.create_hotkey(folder, "ctrl-bracket", ["<ctrl>"], "[", phrase)
