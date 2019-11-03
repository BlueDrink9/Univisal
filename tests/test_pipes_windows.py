#!/usr/bin/env python
import sys, os
import pytest

# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from univisal.pipes_windows import readPipe, writePipe

# TODO: Thread this so that messages can be read after writing, without
# waiting for connection to finish.
# (Probably try reading first to get fastest results?)

def test_single_char():
    pipe = "pipe_test"
    msg = "t"
    writePipe(msg, pipe)
    result = readPipe(pipe)
    assert result == msg, "A single character"


def test_multi_char():
    pipe = "pipe_test"
    msg = "test"
    writePipe(msg, pipe)
    result = readPipe(pipe)
    assert result == msg, "Multiple characters through the pipe"


def test_multi_msg():
    pipe = "pipe_test"
    for m in range(1, 10):
        msg = "test" + str(m)
        writePipe(msg, pipe)
        result = readPipe(pipe)
        assert result == msg, \
            "Many characters, multiple times quickly through the pipe"


def test_pipe_latency():
    pipe = "pipe_test"
    for m in range(1, 10):
        msg = "test" + str(m)
        writePipe(msg, pipe)
        result = readPipe(pipe)
        assert result == msg, \
            "Many characters, multiple times quickly through the pipe"
        # TODO: time at start and end of writing and reading, make sure it is
        # very small.
        assert False
    # TODO: Overall time should be very low
    assert False


if __name__ == '__main__':
        pytest.main()
