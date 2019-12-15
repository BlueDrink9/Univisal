#! /usr/bin/env python3
"""
Autokey needs to be running.
autokey-run should be in your path, otherwise it is in the main autokey
folder.
Usage:
Add this script into autokey under the description "bindings" then run:  autokey-run -s [path/to/bindings.py]
"""
# import autokey.iomediator
# import autokey.configmanager
# import autokey.scripting
# import autokey.scripting_highlevel as hl
# system = autokey.scripting.System()
# create_hotkey = autokey.scripting.Engine.create_hotkey

def bind(keypress, univi_key):
    # This both forms the required list, and 
    split = keypress.split("+")
    modifiers = []
    key = keypress
    if len(split) > 1:
        # Keypress is combined modifier, need to change to tuple.
        # Assuming all keys except last are modifiers.
        key = split[-1]
        modifiers = split[:-1]
    if keypress == keypress.Upper():
        modifiers.append("<shift>")
    hotkeys = (modifiers, key)
    folder = engine.create_folder("autokey_univisal", temporary=True)
    folder = engine.create_folder("autokey_univisal")
    name = univi_key
    contents = "<script name=univi args={}>".format{univi_key}
    engine.create_phrase(folder, name, contents, hotkey=hotkeys, temporary = True)
