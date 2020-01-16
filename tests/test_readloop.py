#!/usr/bin/env python
import os
import pytest
import unittest.mock
import sys
import logging
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import univisal
from univisal.keys import Keys
from univisal.motion import Motion
from tests.mock_setup import init_univisal

@pytest.fixture(autouse=True)
def init_store():
    global inI, outI, outpts, inpts
    inI=-1
    outI=-1
    outpts=[]
    inpts=[]

outpts=[]
outI=-1
def addOutput(key):
    global outpts
    outpts.append(key)
inpts=[]
inI=-1
def setInputs(keys):
    global inpts
    inpts=keys

def mock_write(key):
    addOutput(key)
def mock_read():
    global inI
    inI += 1
    return inpts[inI]


def init_loop():
    # caplog.set_level(logging.DEBUG)
    with unittest.mock.patch("univisal.message_interface.outpt_write",
                     side_effect=mock_write), \
            unittest.mock.patch("univisal.message_interface.inpt_read",
                                side_effect=mock_read):
        init_univisal(with_interface=True)

def loop(keys):
    # Copy to stop HUP ending up in failure output.
    send = keys.copy()
    # Stop the loop at the end of the input keys.
    send.append("HUP")
    setInputs(send)
    init_loop()


@pytest.mark.parametrize("keys, expected", [
    (["l"], Motion.right.value),
    (["l", 'l'], Motion.right.value * 2),
    ])
def test_loop(keys, expected):
    if not isinstance(keys, list):
        keys = [keys]
    loop(keys)
    assert ''.join(outpts)==expected, "Main loop failed with keys {}".format(keys)
