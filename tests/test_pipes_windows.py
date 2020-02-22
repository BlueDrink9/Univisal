#!/usr/bin/env python
import os
import pytest
import sys
import threading
import time

if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests", allow_module_level=True)

# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from univisal.pipes_windows import readPipe, writePipe

def round_trip_msg(msg, pipe=None):
    if pipe is None:
        # TODO make this a unique generation to prevent 1 broken test holding
        # up another one.
        pipe = "pipe_test"
    x = threading.Thread(target=writePipe, args=(msg, pipe))
    x.start()
    time.sleep(0.01)
    # writePipe(msg, pipe)
    result = readPipe(pipe)
    return result


def test_single_char():
    msg = "t"
    result = round_trip_msg(msg)
    assert result == msg, "A single character"


def test_multi_char():
    msg = "test"
    result = round_trip_msg(msg)
    assert result == msg, "Multiple characters through the pipe"


def test_multi_msg():
    pipe = "pipe_test"
    for m in range(1, 30):
        msg = "test" + str(m)
        result = round_trip_msg(msg, pipe)
        assert result == msg, \
            "Many characters, multiple times quickly through the pipe"


@pytest.mark.skipif("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true",
        reason="Skipping this test on Travis CI.")
def test_pipe_latency():
    pipe = "pipe_test"
    pretime = time.time()
    n = 30
    for m in range(1, n):
        msg = "test" + str(m)
        trippretime = time.time()
        result = round_trip_msg(msg, pipe)
        tripposttime = time.time()
        assert result == msg, \
            "Many characters, multiple times quickly through the pipe"
        # Make sure round trip takes less than 0.011 ms (0.01 is a sleep in the
        # trip anyway)
        assert tripposttime - trippretime < 0.015
    posttime = time.time()
    # Make sure total trip takes less than 0.01 ms per round plus a few extra
    # ms
    assert posttime - pretime < 0.01 * n + 0.10


if __name__ == '__main__':
        pytest.main()
