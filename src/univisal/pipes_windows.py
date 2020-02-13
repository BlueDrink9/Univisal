#!/usr/bin/env python
import pywintypes, win32pipe, win32file
import time
import sys
try:
    from .library import *
except ImportError:
    from library import *
logger = __import__("univisal.logger").logger.get_logger(__name__)

def readPipe(pipename="univisal.in.fifo"):
    # Even in raw strings, backslashes escape quotes.
    pipeBase = r'\\.\pipe' + '\\'
    readpipeName = pipeBase + pipename
    reading = True
    logger.debug("Opening univisal input pipe {}".format(readpipeName))
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
                # try:
                #     msg = raw.decode("utf-16")
                # except UnicodeDecodeError:
                #     msg = raw.decode("Latin-1")
            logger.debug("Read '{}' from univisal input pipe".format(msg))
            reading = False
            return str(msg)
        except FileNotFoundError:
            # Pipe not open. Keep trying.
            # logger.debug("Pipe not found for reading, trying again", exc_info=True)
            # Sleep to reduce busywaiting.
            # Using threading and Events may be a better solution, but given
            # how frequently and low-latency we may need this to fire, may not
            # work as well.
            time.sleep(0.01)
        except OSError as exc:
            # Invalid argument error.
            # I think it occurs when the file doesn't exist... but it may occur
            # for good reasons to. #XXX
            if exc.errno == 22:
                warntext = """While reading pipe, read failed with error
                'invalid argument'.
                Trying again."""
                logger.warning(warntext, exc_info=True)
                pass
            else:
                raise  # re-raise previously caught exception


def makeWritePipe(pipename):
    # Even in raw strings, backslashes escape quotes.
    pipeBase = r'\\.\pipe' + '\\'
    writepipeName = pipeBase + pipename
    writepipeh = win32pipe.CreateNamedPipe(
        writepipeName,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    return writepipeh


def writePipe(msg, pipename="univisal.out.fifo"):
    # Have to close pipe to finish sending message, meaning you have to re-open
    # it here.
    # There may be an alternative to having to totally re-open the pipe. Look
    # for named pipe code loops that don't fully close it.
    pipe = makeWritePipe(pipename)
    try:
        logger.info("Waiting for output pipe to be read")
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
