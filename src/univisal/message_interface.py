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


def readMessagesLoop():
    while True:
        data = inpt_read()
        logger.debug("data :'{}'".format(data))
        # logger.debug("Data: " + data)
        output = process_input(data)
        if output:
            outpt_write(output)
        else:
            # If processing returns None, was HUP. End processing.
            break


def process_input(data):
    if len(data) == 0:
        output = ""
    key = data.rstrip()
    logger.debug("Key: " + key)
    if key == "HUP":
        logger.info("HUP. End reading.")
        return None
    try:
        output = handleInput(key)
    except:
        logger.critical("Unhandled exception", exc_info=True)
        output = key
    logger.debug("Output: " + output)
    if not isinstance(output, str):
        logger.error("""
        Error: No key outputted. Output is not str. Returning input key instead.
        """)
        output = key
    return output
