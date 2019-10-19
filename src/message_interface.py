#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles sending and receiving messages from adapters via a univi client
"""
import os
import sys
import errno
from tempfile import gettempdir
print('start')

# If Windows, else assume Unix.
if os.name == "nt":
    from pipes_windows import makePipes, readPipe, writePipe
else:
    from pipes_unix import makePipes

readpipe, writepipe = makePipes()


def outpt_write(key):
    print(key)
    outpt = open(writepipe, "w")
    outpt.write(key)
    outpt.close()


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
    while False:
        print('writing')
        f = open(r'\\.\pipe\univisal', 'w', 0)
        f.write("direct write")
        f.close

    reading_input = True
    while reading_input:
        if os.name == "nt":
            print("here")
            # writePipe(readpipe, "Hello")
            data = readPipe(readpipe)
            print(data)
            process_input(data)
        else:
            # print("Opening {}".format(readpipe))
            with open(readpipe, 'rb') as inpt:
                while True:
                    print(readpipe)
                    data = inpt.read()
                    print(data)
                    if not process_input(data):
                        break
