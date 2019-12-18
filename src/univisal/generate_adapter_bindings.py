#!/usr/bin/env python

import string
import os
import sys
# For expand_escapes
import codecs
try:
    from .library import *
    from . import logging_
    from .adapter_maps import *
    from . import motion, operation
except ImportError:
    from library import *
    import logging_
    from adapter_maps import *
    import motion, operation

# Hack to get python to store literal '%s' in string. "%ss% % '%'
# d::univiResultFromKey("d")
cmdformat_ahk = "%ss::univiResultFromKey(\"%ss\")" % ('%', '%')
# d
#   xdotool key $(univi_handleKey 'd')
cmdformat_sxhkd = "%ss\n\txdotool key $(univi_handleKey %ss)" % ('%', '%')

def expand_escapes(string):
    return codecs.escape_decode(bytes(string, "utf-8"))[0].decode("utf-8")

if len(sys.argv) != 3:
    print("Usage: generate_adapter_bindings.py adapter string")
    print("Args:")
    print("'adapter': name generated bindings will write as")
    print("""'string' : a printf-formatted string.
          It is the command to generate for the adapter,
          with %s in two places: Binding and send position.
          There are examples in the source
          """)
    sys.exit(1)

adapter = expand_escapes(str(sys.argv[1]))
cmdformat = expand_escapes(str(sys.argv[2]))
adapter_maps = load_adapter_maps(adapter)

generated_file=open(get_script_path() + \
                    "/../../adapters/{}/bindings.{}".format(adapter, adapter), "w")


# Standard input keys
keys = list(string.ascii_letters + \
    string.digits)

# Punctuation needs special handling, since shift is involved and it may change
# depending on keyboard layout.
    # + \
    # string.punctuation)
# This is designed to suit US international QWERTY symbol location.
unshifted_symbols = r",./;'[]-=`"
symbols = []
shifted_symbols =          r'~!@#$%^&*()_+{}:<>?'
shifted_symbols_base_key = list(r"`1234567890-=[];,./")
shifted_symbols_base_key += "\\\\"
shifted_symbols_base_key += "\\'"
shifted_symbols_base_key += '\\"'
for i, symbol in enumerate(shifted_symbols_base_key):
    symbols.append("<shift>" + getJoinChar() + symbol)
symbols += list(unshifted_symbols)
keys += symbols
# Symbols and capitals need shift.
for key in keys:
    if (key.isalpha() and key == key.upper()):
        key = "<shift>" + getJoinChar() + key

def isSpecialMap(key):
    if key == "<multikey_join_char>":
        return True
    enums = [motion.Motion, operation.Operation]
    for enum in enums:
        for e in enum:
            print(e.name)
            if e.name == key:
                return True
    return False

# Add any keys in the adapter map that may have been missed.
for key in adapter_maps:
    if key not in keys and not isSpecialMap(key):
        keys.append(key)
# Remove modifiers that shouldn't be bound as single keys, and chars that cause
# errors.
keys_to_remove=[
        "<super>", "<ctrl>", "<shift>", "<alt>", "<esc>",
        "\\", "\'", '\"', "'", '"',
        ]
for k in keys_to_remove:
    try:
        keys.remove(k)
        if k in shifted_symbols_base_key:
            keys.remove("<shift>" + getJoinChar() + symbol)
    except ValueError:
        pass
# Append any special keys. These will be at the end of the bindings, and may
# require special attention/modification.
keys_to_add=[
        "\\\\", "\\'", '\\"',
        ]
for k in keys_to_add:
    keys.append(k)

for key in keys:
    # Doing a double escape, to expand the formatting stored in the variable.
    # May be easier to use python's Template module though.
    generated_file.write(f"{cmdformat}\n" % (getAdapterMap(key), key))

generated_file.close()
