#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles sending and receiving messages from adapters via a univi client
"""
import logging
import os
try:
    from .library import *
    from . import logging_
    from .handleInput import handleInput
    # If Windows, else assume Unix.
    if os.name == "nt":
        from .pipes_windows import readPipe, writePipe
    else:
        from .pipes_unix import readPipe, writePipe
except ImportError:
    from handleInput import handleInput
    from library import *
    import logging_
    # If Windows, else assume Unix.
    if os.name == "nt":
        from pipes_windows import readPipe, writePipe
    else:
        from pipes_unix import readPipe, writePipe
logger = logging.getLogger(__name__)



def outpt_write(key):
    writePipe(key)

def inpt_read():
    return readPipe()

def process_input(data):
    global reading_input
    if len(data) == 0:
        output = ""
    key = data.rstrip()
    logger.debug("Key: " + key)
    if key == "HUP":
        logger.info("HUP. End reading.")
        reading_input = False
        return False
    try:
        output = handleInput(key)
    except:
        logger.critical("Unhandled exception", exc_info=True)
        output = key
    logger.debug("Output: " + output)
    if not isinstance(output, str):
        logger.error("""
        Error: No key sent. Output is not str. Returning input key instead.
        """)
        output = key
    outpt_write(output)
    return True


def init_message_interface():
    global reading_input
    reading_input = True
    while reading_input:
        data = inpt_read()
        logger.debug("data :'{}'".format(data))
        # logger.debug("Data: " + data)
        # If processing returns False, was HUP. End processing.
        if not process_input(data):
            break
