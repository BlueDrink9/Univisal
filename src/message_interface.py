#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles sending and receiving messages from adapters via a univi client
"""
import os
import sys
import errno
from tempfile import gettempdir

sys.path.append('pipes')
# If Windows, else assume Unix.
if os.name == "nt":
    from windows import makePipes
else:
    from unix import makePipes

readpipe, writepipe = makePipes()


def outpt_write(key):
    print(key)
    outpt = open(writepipe, "w")
    outpt.write(key)
    outpt.close()


def init_message_interface():
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
