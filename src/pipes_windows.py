#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# From module pywin32
import pywintypes, win32pipe, win32file
import time
import sys
from library import *
import logging
import logging_
logger = logging.getLogger(__name__)

def readPipe():
    readpipeName = r'\\.\pipe\univisal.in.fifo'
    reading = True
    while reading:
        msg = None
        try:
            pipe = open(readpipeName,"r")
            msg = pipe.read()
            logger.debug("Read '{}' from univisal input pipe".format(msg))
            # The current system with how the AHK adapter writes to the pipe
            # results in a weird extra space after every character when read by
            # python. This is some unfortunate adapter-specific check for the
            # BOM added by the AHK adapter, which then strips the extra spaces
            # and the BOM.
            if msgIsFromAHK(msg):
                msg = AHKMsgProcess(msg)
            reading = False
            return str(msg)
        except FileNotFoundError:
            # Pipe not open. Keep trying.
            # logger.debug("Pipe not found for reading, trying again", exc_info=True)
            pass

def msgIsFromAHK(msg):
    # return msg[0] == chr(0xfeff) or msg[0:2] == chr(239) + chr(187) + chr(191)
    # It's this on my system, but this feels very fragile.
    logger.debug("msg[:2] '{}' ".format(msg[:2] == "ÿþ"))
    # return msg[:2] == "ÿþ"
    return True

def AHKMsgProcess(msg):
    # strip BOM.
    msg = msg[2:]
    # if msg[0] == chr(0xfeff):
    #     msg = msg[1:]
    # elif msg[0:2] == chr(239) + chr(187) + chr(191):
    #     msg = msg[3:]
    # Remove every second char (which is a space coming from AHK).
    msg = msg[::2]
    logger.debug("Read '{}' from univisal input pipe".format(msg))
    return msg

def makeWritePipe():
    name = r'\\.\pipe\univisal.out.fifo'
    writepipeh = win32pipe.CreateNamedPipe(
        name,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    return writepipeh


def writePipe(msg):
    return
    # Have to close pipe to finish sending message, meaning you have to re-open
    # it here.
    # There may be an alternative to having to totally re-open the pipe. Look
    # for named pipe code loops that don't fully close it.
    pipe = makeWritePipe()
    try:
        logger.info("Waiting for pipe to be read")
        win32pipe.ConnectNamedPipe(pipe, None)
        logger.info("Got pipe client")
        # count = 0
        # while count < 10:
        #     print(f"writing message {count}")
        # convert to bytes
        some_data = str.encode(f"{msg}")
        win32file.WriteFile(pipe, some_data)
        logger.info("Finished writing to pipe")
    finally:
        win32file.CloseHandle(pipe)
        pass
