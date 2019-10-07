#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

def makeUnixPipes():
    # Read http://man7.org/linux/man-pages/man7/fifo.7.html for reference.
    readpipe = gettempdir() + '/univisal.in.fifo'
    writepipe = gettempdir() + '/univisal.out.fifo'
    try:
        os.mkfifo(readpipe)
        os.mkfifo(writepipe)
    except OSError as oe:
        errmsg="""
        Error opening IO pipes {} or {}. They may need to be removed manually, or
        univisal may not have read permissions to the temp directory.
        """.format(readpipe, writepipe)
        if oe.errno != errno.EEXIST:
            sys.stderr.write(errmsg)
            raise
    return readpipe, writepipe

def makePipes():
    readpipe, writepipe = makeUnixPipes()
    return readpipe, writepipe
