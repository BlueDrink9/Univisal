#!/usr/bin/env python

import string
import os
import sys
# For expand_escapes
import codecs
try:
    from .library import *
    from . import logging_
    from .adapter_maps import getAdapterMap
except ImportError:
    from library import *
    import logging_
    from adapter_maps import *

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
script_maps = load_adapter_maps(adapter)

generated_file=open(get_script_path() + \
                    "/../../adapters/{}/bindings.{}".format(adapter, adapter), "w")

# Standard input keys
keys = list(string.ascii_letters + \
    string.digits + \
    string.punctuation)
# Append any special keys. These will be at the end of the bindings, and may
# require special attention/modification.
keys.append("esc")
# Put backslash at the end because it might be an escape char for the adapter.
keys.remove("\\")
keys.append("\\")
for key in keys:
    # Doing a double escape, to expand the formatting stored in the variable.
    # May be easier to use python's Template module though.
    generated_file.write(f"{cmdformat}\n" % (getAdapterMap(key), key))

generated_file.close()
