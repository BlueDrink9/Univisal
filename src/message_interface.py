#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles sending and receiving messages from adapters via a univi client
"""
import os
from tempfile import gettempdir
print('start')

# If Windows, else assume Unix.
if os.name == "nt":
    from pipes_windows import initPipes, readPipe, writePipe
else:
    from pipes_unix import initPipes, readPipe, writePipe

readpipe, writepipe = initPipes()


def outpt_write(key):
    writePipe(key)


def process_input(data):
    global reading_input
    if len(data) == 0:
        return False
    key = data.rstrip()
    if key == "HUP":
        print("HUP")
        print("end reading")
        reading_input = False
        return False
    output = handleKey(key)
    if output is None:
        if DEBUG:
            output = "Error: No key sent"
        else:
            output = key
    outpt_write(output)
    return True


def init_message_interface():
    global reading_input
    reading_input = True
    while reading_input:
        data = readPipe()
        print(data)
        # If processing returns False, was HUP. End processing.
        if not process_input(data):
            break
