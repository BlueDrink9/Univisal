#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import win32pipe
import pywintypes

def makeWin32Pipe(name):
    # https://docs.microsoft.com/en-us/windows/win32/ipc/named-pipes
    openMode = win32pipe.PIPE_ACCESS_DUPLEX
    pipeMode = win32pipe.PIPE_TYPE_MESSAGE  | win32pipe.PIPE_WAIT
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


def makePipes():
    readpipe = makeWin32Pipe(r'\\.\pipe\univisal.in.fifo')
    writepipe = makeWin32Pipe(r'\\.\pipe\univisal.out.fifo')
    return readpipe, writepipe
