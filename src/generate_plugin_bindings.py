#!/usr/bin/env python

import string
import os
import sys

input_key_prefix=""
input_key_suffix="::"
run_command_prefix="univiResultFromKey(\""
run_command_suffix="\")"
fileext = ".ahk"


def mapPluginInputKey(key):
    return key

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

f=open(get_script_path() + "/../plugins/bindings%s" % fileext, "w+")

# Standard input keys
keys = string.ascii_letters + \
        string.digits + \
        "Esc" + \
        string.punctuation
for key in keys:
    f.write(input_key_prefix + mapPluginInputKey(key) + input_key_suffix + \
            run_command_prefix + key + run_command_suffix + "\n")
