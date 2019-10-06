#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import socket
from threading import Thread
import sys
import os
import errno
from tempfile import gettempdir
from library import *
# Available since 3.1
# import importlib
#

from handleKey import *

if len(sys.argv) != 2:
    print("Usage: univisal.py adapter")
    print("""'adapter' is a string corresponding to a folder in ../adapters
    that contains a json 'mappings.json'."
    """)
    sys.exit(1)

adapterdir = get_script_path() + "/../" + str(sys.argv[1])

readpipe = gettempdir() + '/univisal.in.fifo'
writepipe = gettempdir() + '/univisal.out.fifo'
try:
    os.mkfifo(readpipe)
    os.mkfifo(writepipe)
except OSError as oe:
    errmsg="""
    Error opening IO pipes {} or {}. They may need to be removed manually, or
    univisal may not have read permissions to the temp directory.
    """.format(readpipe, writepipe)
    if oe.errno != errno.EEXIST:
        sys.stderr.write(errmsg)
        raise

# handle(readpipe)
#
def outpt_write(key):
    print(key)
    outpt = open(writepipe, "w")
    outpt.write(key)
    outpt.close()

# Read http://man7.org/linux/man-pages/man7/fifo.7.html for reference.
reading = True
while reading:
    # print("Opening {}".format(readpipe))
    with open(readpipe) as inpt:
        while True:
            data = inpt.read()
            if len(data) == 0:
                break
            key = data.rstrip()
            if key == "HUP":
                print("HUP")
                print("end reading")
                reading = False
                break
            output = handleKey(key)
            if output is None:
                if DEBUG:
                    output = "Error: No key sent"
                else:
                    output = key
            outpt_write(output)
