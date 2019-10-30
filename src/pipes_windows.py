#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# From module pywin32
import pywintypes, win32pipe, win32file
import time
import sys

def readPipe():
    readpipeName = r'\\.\pipe\univisal.in.fifo'
    while True:
        try:
            pipe = open(readpipeName,"r")
            msg = pipe.read()
            return msg
        except FileNotFoundError:
            # XXX log
            # print("Pipe not found for reading")
            pass


def makeWritePipe(name):
    writepipeh = win32pipe.CreateNamedPipe(
        name,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    return writepipeh


def writePipe(pipe, msg):
    writepipeName = r'\\.\pipe\univisal.out.fifo'
    # Have to close pipe to finish sending message, meaning you have to re-open
    # it here.
    # There may be an alternative to having to totally re-open the pipe. Look
    # for named pipe code loops that don't fully close it.
    pipe = makeWritePipe(writepipeName)
    try:
        print("waiting for client")
        win32pipe.ConnectNamedPipe(pipe, None)
        print("got client")

        # count = 0
        # while count < 10:
        #     print(f"writing message {count}")
        # convert to bytes
        some_data = str.encode(f"{msg}")
        win32file.WriteFile(pipe, some_data)

        print("finished now")
    finally:
        win32file.CloseHandle(pipe)
        pass
