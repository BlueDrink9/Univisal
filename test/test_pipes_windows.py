#!/usr/bin/env python
target = __import__("../src/pipes_windows.py")
readPipe = target.readPipe
writePipe = target.writePipe


def test_single_char():
    msg = "t"
    writePipe(msg, "pipe_test")
    result = readPipe("pipe_test")
    assert result == msg


def test_multi_char():
    msg = "test"
    writePipe(msg, "pipe_test")
    result = readPipe("pipe_test")
    assert result == msg


def test_multi_msg():
    for m in range(1, 10):
        msg = "test" + m
        writePipe(msg, "pipe_test")
        result = readPipe("pipe_test")
        assert result == msg
