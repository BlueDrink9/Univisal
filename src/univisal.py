#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
# Available since 3.1
# import importlib


from message_interface import init_message_interface
from library import *
from adapter_maps import *
from handleKey import *

if len(sys.argv) != 2:
    print("Usage: univisal.py adapter")
    print("""'adapter' is a string corresponding to a folder in ../adapters
    that contains a json 'mappings.json'."
    """)
    sys.exit(1)

load_adapter_maps(sys.argv[1])

init_message_interface()
