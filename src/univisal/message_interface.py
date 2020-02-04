#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Handles sending and receiving messages from adapters via a univi client.
Messages are abstracted.
"""
import time
try:
    from .library import *
    from .handleInput import handleInput
    from .messages import read_message, write_message
except ImportError:
    from library import *
    from handleInput import handleInput
    from messages import read_message, write_message
logger = __import__("univisal.logger").logger.get_logger(__name__)

# Time to sleep between handling keypresses.
# Answers here suggest ~100 ms is the minimum latency time for most people
# to consciously percieve.
# https://stackoverflow.com/questions/4098678/average-inter-keypress-time-when-typing
# A 60 WPM average typist has a ~170 ms gap, but top programmers will be
# faster.
# Of course, univisal's delay is added to all the other delays involved in
# human-computer IO, so we can't use up the whole 100 ms.
# https://pavelfatin.com/typing-with-pleasure/
# Also, there is evidence cited in Fatin's article to suggest even tiny
# amounts of latency matter.
# For these reasons, I'm keeping this fairly low.
# TODO: Allow configuration.
INPUT_RATE_DETECTION_GAP_MS=30


def readMessagesLoop():
    while True:
        data = read_message()
        logger.debug("data :'{}'".format(data))
        # logger.debug("Data: " + data)
        output = process_input(data)
        if output:
            write_message(output)
        else:
            # If processing returns None, was HUP. End processing.
            break
        # Reduce busywaiting.
        time.sleep(INPUT_RATE_DETECTION_GAP_MS/1000)


def process_input(data):
    if len(data) == 0:
        return ""
    # I can't remember why I was stripping whitespace.
    # stripped_data = data.rstrip()
    # if len(stripped_data) > 0:
    #     key = stripped_data
    # else:
    #     # Key may have been a space or tab.
    #     key = data
    key = data
    logger.debug("Key: " + key)
    if key == "HUP":
        logger.info("HUP. End reading.")
        return None
    output = tryHandle(key)
    return output


def tryHandle(key):
    try:
        output = handleInput(key)
    except:
        logger.critical("Unhandled exception", exc_info=True)
        output = key
    if not isinstance(output, str):
        logger.error("""
        Error: No key outputted. Output is not str. Returning input key instead.
        """)
        output = key
    logger.debug("Output: {}".format(output))
    return output
