#!/usr/bin/env python
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
            # AHK pipe sends in utf-16 for some AHK versions.
            pipe = open(readpipeName,"rb")
            raw = pipe.read()
            try:
                msg = raw.decode("utf-8")
            except UnicodeDecodeError:
                msg = raw.decode("utf-16")
            logger.debug("Read '{}' from univisal input pipe".format(msg))
            reading = False
            return str(msg)
        except FileNotFoundError:
            # Pipe not open. Keep trying.
            # logger.debug("Pipe not found for reading, trying again", exc_info=True)
            pass


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
