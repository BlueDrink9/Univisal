#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import win32pipe
import win32file
import pywintypes

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


def makePipes():
    readpipe = r'\\.\pipe\univisal.in.fifo'
    writepipe = r'\\.\pipe\univisal.out.fifo'
    readpipeh = makeWin32Pipe(readpipe)
    writepipeh = makeWin32Pipe(writepipe)
    print(readpipe)
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
    win32file.WriteFile(readpipeh, bytes("test", "UTF-8"))
    win32file.WriteFile(readpipe, bytes("test", "UTF-8"))
    print(readpipe)
    return readpipe, writepipe


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


def writePipe(handle, message):
    # win32file.WriteFile(handle, bytes(message, "UTF-8"))
    win32file.WriteFile(handle, message)
    return out
