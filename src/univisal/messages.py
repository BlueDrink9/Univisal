#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""
Adapter between the messaging system and univisal
"""
import os
try:
    # If Windows, else assume Unix.
    if os.name == "nt":
        from .pipes_windows import readPipe, writePipe
    else:
        from .pipes_unix import readPipe, writePipe
except ImportError:
    # If Windows, else assume Unix.
    if os.name == "nt":
        from pipes_windows import readPipe, writePipe
    else:
        from pipes_unix import readPipe, writePipe

#TODO: Consider using threading for message waiting.
# https://blog.miguelgrinberg.com/post/how-to-make-python-wait
# Alternatively, maybe use an asyncio queue? Yeah, that could be
# elegant...

def read_message():
    return readPipe()

def write_message(msg):
    writePipe(msg)
