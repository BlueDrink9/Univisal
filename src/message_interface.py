#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles sending and receiving messages from adapters via a univi client
"""
import os
from library import *
import logging
import logging_
import handleKey
logger = logging.getLogger(__name__)

# If Windows, else assume Unix.
if os.name == "nt":
    from pipes_windows import readPipe, writePipe
else:
    from pipes_unix import readPipe, writePipe


def outpt_write(key):
    writePipe(key)

def inpt_read():
    return readPipe()

def process_input(data):
    global reading_input
    if len(data) == 0:
        return False
    key = data.rstrip()
    logger.debug("Key: " + key)
    if key == "HUP":
        logger.info("HUP. End reading.")
        reading_input = False
        return False
    output = handleKey(key)
    logger.debug("Outway: " + output)
    if output is None:
        logger.error("""
        Error: No key sent. Output is None. Returning input key instead.
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
