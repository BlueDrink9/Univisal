#!/usr/bin/env python
target = __import__("../src/pipes_windows.py")
readpipe = target.readpipe
writepipe = target.writepipe


def test_single_char():
    msg = "t"
    writepipe(msg)
    result = readpipe()
    assert result == msg


def test_multi_char():
    msg = "test"
    writepipe(msg)
    result = readpipe()
    assert result == msg


def test_multi_msg():
    for m in range(1, 10):
        msg = "test" + m
        writepipe(msg)
        result = readpipe()
        assert result == msg
