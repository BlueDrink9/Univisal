#!/usr/bin/env python
import os
import pytest
import sys
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from univisal.remap import *
from univisal.model import *
from univisal.handleKey import handleKey

def translate_keys(keys):
    """
    Pass in a string if no special keys, else pass in a list.
    """
    out = []
    for char in keys:
        # out.append(handleKey(char))
        out += resolve_map(char)
        # out += handleKey(char)
    print(out)
    while "<bs>" in out:
        index = out.index("<bs>")
        out.pop(index)
        out.pop(index - 1)
    # need to iteratively replace <bs> with removed char
    return ''.join(out)

def test_imap(caplog):
    caplog.set_level(logging.DEBUG)

    setMode(Mode.insert)
    # test = "I want jj"
    # expected = "I want <esc>"
    # imap("jj", "<esc>")
    # assert translate_keys(test) == expected
    # assert isMode(Mode.normal)
    # imap("jj")
    # setMode(Mode.insert)

    # test = "I want jk"
    # expected = "I want <esc>"
    # imap("jk", "<esc>")
    # assert translate_keys(test) == expected
    # assert isMode(Mode.normal)
    # imap("jk")
    # setMode(Mode.insert)

    imap("map", "pam")
    test = "complimapcated"
    expected = "complipamcated"
    assert translate_keys(test) == expected
    # No imap
    test = "complimacated"
    expected = "complimacated"
    assert translate_keys(test) == expected
