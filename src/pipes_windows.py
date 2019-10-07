#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import win32pipe
import pywintypes

def makeWin32Pipe(name):
    # https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes
    openMode = win32pipe.PIPE_ACCESS_DUPLEX
    # write/read messages, not bytes. Blocking.
    pipeMode = win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE \
            | win32pipe.PIPE_WAIT
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
    makeWin32Pipe(readpipe)
    makeWin32Pipe(writepipe)
    return readpipe, writepipe


def readPipe(handle):
    bufSize = 2000
    timeout = 1
    out = win32pipe.CallNamedPipe(handle, bytes("", "UTF-8"), bufSize, timeout)
    return out


def writePipe(handle, message):
    bufSize = 0
    timeout = 1
    out = win32pipe.CallNamedPipe(handle, message, bufSize, timeout)
    return out
