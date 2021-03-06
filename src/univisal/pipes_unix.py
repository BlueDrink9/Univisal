#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import os
import errno
import sys
from tempfile import gettempdir
try:
    from .library import *
except ImportError:
    from library import *
logger = __import__("univisal.logger").logger.get_logger(__name__)

def makePipes():
    # Read http://man7.org/linux/man-pages/man7/fifo.7.html for reference.
    try:
        if os.path.exists(readpipe):
              os.remove(readpipe)
        if os.path.exists(writepipe):
              os.remove(writepipe)
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
    # return readpipe, writepipe


readpipe = gettempdir() + '/univisal.in.fifo'
writepipe = gettempdir() + '/univisal.out.fifo'
makePipes()
# readpipe, writepipe = makePipes()


def writePipe(msg):
    global writepipe
    outpt = open(writepipe, "w")
    outpt.write(msg)
    outpt.close()


def readPipe():
    global readpipe
    with open(readpipe, 'rb') as inpt:
        while True:
            data = inpt.read().decode()
            return data
            # if not process_input(data):
            #     break
            #
            # TODO: Does the unix readpipe loop need a sleep?
