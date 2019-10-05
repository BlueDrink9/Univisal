#!/usr/bin/env python

import string
import os
import sys
# For expand_escapes
import codecs

# Hack to get python to store literal '%s' in string. "%ss% % '%'
# d::univiResultFromKey("d")
cmdformat_ahk = "%ss::univiResultFromKey(\"%ss\")" % ('%', '%')
# d
#   xdotool key $(univi_handleKey 'd')
cmdformat_sxhkd = "%ss\n\txdotool key $(univi_handleKey %ss)" % ('%', '%')

def expand_escapes(string):
    return codecs.escape_decode(bytes(string, "utf-8"))[0].decode("utf-8")

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

if len(sys.argv) != 2:
    print("Usage: generate_plugin_bindings.py [string]")
    print("[string] is a printf-formatted string. \
          It is the command to generate for the plugin, \
          with %ss in two places: Binding and send position" % ('%'))
    print("There are examples in the source")
    sys.exit(1)

cmdformat = expand_escapes(str(sys.argv[1]))
# cmdformat = cmdformat_ahk
# cmdformat = cmdformat_sxhkd

f=open(get_script_path() + "/../plugins/generated_bindings", "w+")

# Standard input keys
keys = string.ascii_letters + \
        string.digits + \
        "Esc" + \
        string.punctuation
for key in keys:
    # Doing a double escape, to expand the formatting stored in the variable.
    # May be easier to use the Template module though.
    f.write(f"{cmdformat}\n" % (key, key))
f.close()
