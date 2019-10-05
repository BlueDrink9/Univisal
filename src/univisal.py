#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import socket
from threading import Thread
import sys
import os
import errno
from tempfile import gettempdir
# Available since 3.1
# import importlib
def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

from handleKey import *

# def handle(pipe):
#     return

readpipe = gettempdir() + '/univisal.in.fifo'
try:
    os.mkfifo(readpipe)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

# handle(readpipe)

reading = True
while reading:
    # print("Opening {}".format(readpipe))
    with open(readpipe) as inpt:
        while True:
            data = inpt.read()
            if len(data) == 0:
                break
            key = data.rstrip()
            print(data)
            if key == "HUP":
                print("HUP")
                print("end reading")
                reading = False
                break
            output = handleKey(key)
            print(output)
            # outpt_write(output)
