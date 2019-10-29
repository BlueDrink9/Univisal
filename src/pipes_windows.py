#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import pywintypes, win32pipe, win32file

def makeWin32Pipe(name):
    # https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes
    openMode = win32pipe.PIPE_ACCESS_DUPLEX
    openMode = win32pipe.PIPE_ACCESS_OUTBOUND
    # write/read messages, not bytes. Blocking.
    pipeMode = win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE \
            | win32pipe.PIPE_NOWAIT
            # | win32pipe.PIPE_WAIT
    sa = pywintypes.SECURITY_ATTRIBUTES()
    sa.SetSecurityDescriptorDacl ( 1, None, 0 )
    pipe_handle = win32pipe.CreateNamedPipe(name,
                                            openMode,
                                            pipeMode,
                                            win32pipe.PIPE_UNLIMITED_INSTANCES,
                                            0,
                                            0,
                                            2000,
                                            sa)
    return pipe_handle

makeWritePipe():
    writepipe = r'\\.\pipe\univisal.out.fifo'
    writepipeh = win32pipe.CreateNamedPipe(
        writepipe,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    return writepipeh

def makePipes():
    readpipe = r'\\.\pipe\univisal.in.fifo'
    writepipe = r'\\.\pipe\univisal.out.fifo'
    readpipeh = makeWin32Pipe(readpipe)
    # print(readpipe)
    # win32file.CreateFile(
    #         readpipe,
    #         win32file.GENERIC_READ | win32file.GENERIC_WRITE,
    #         0,
    #         None,
    #         win32file.OPEN_EXISTING,
    #         0,
    #         None,
    #         )
    # win32pipe.ConnectNamedPipe(readpipeh, None)
    # win32pipe.ConnectNamedPipe(writepipeh, None)
    # win32pipe.ConnectNamedPipe(readpipe, None)
    # win32pipe.ConnectNamedPipe(writepipe, None)
    # win32file.WriteFile(readpipeh, bytes("test", "UTF-8"))
    # win32file.WriteFile(readpipe, bytes("test", "UTF-8"))
    # print(readpipe)
    writepipeh = makeWritePipe()
    return readpipeh, writepipeh


def readPipe(handle):
    bufSize = 2000
    #The result is a tuple of (hr, string/PyOVERLAPPEDReadBuffer), where hr may
    # be 0, ERROR_MORE_DATA or ERROR_IO_PENDING. If the overlapped param is not
    # None, then the result is a PyOVERLAPPEDReadBuffer. Once the overlapped IO
    # operation has completed, you can convert this to a string (str(object))to
    # obtain the data. While the operation is in progress, you can use the slice
    # operations (object[:end]) to obtain the data read so far. You must use the
    # OVERLAPPED API functions to determine how much of the data is valid.
    out = win32file.ReadFile(handle, bufSize)
    return str(out[1])


# def writePipe(handle, message):
#     # win32file.WriteFile(handle, bytes(message, "UTF-8"))
#     win32file.WriteFile(handle, message)
#     return out

import time
import sys

# pipename=r'\\.\pipe\mypipe'

def writePipe(pipe, msg):
    # print("pipe server")
    # pipe = win32pipe.CreateNamedPipe(
    #     pipename,
    #     win32pipe.PIPE_ACCESS_DUPLEX,
    #     win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    #     1, 65536, 65536,
    #     0,
    #     None)

    # Have to close pipe to finish sending message, meaning you have to re-open
    # it here.
    # There may be an alternative to having to totally re-open the pipe. Look
    # for named pipe code loops that don't fully close it.
    pipe = makeWritePipe()
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
