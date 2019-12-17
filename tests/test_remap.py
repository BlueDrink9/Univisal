#!/usr/bin/env python
import os
import pytest
import sys
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from univisal.remap import *
from univisal.model import *
from univisal.handleKey import handleKey


@pytest.fixture(scope="function")
def clear_maps():
    imaps = {}
    nmaps = {}
    vmaps = {}
    cmaps = {}

def translate_keys(keys):
    """
    Pass in a string if no special keys, else pass in a list.
    """
    out = []
    for char in keys:
        out += handleKey(char)
    print(out)
    while "<bs>" in out:
        index = out.index("<bs>")
        out.pop(index)
        out.pop(index - 1)
    # need to iteratively replace <bs> with removed char
    return ''.join(out)


@pytest.mark.parametrize("maps, test, expected, error_msg", [
    ({"map": "pam"},
        "complimapcated",
        "complipamcated",
        "fails map in middle of a word with one starting letter early"),
    ({"map": "pam"},
        "complimacated",
        "complimacated",
        "fails map where 2/3 match"),
    pytest.param({"map": "pam"},
        "complimamapcated",
        "complimapamcated",
        "fails map where map starts while same map is in progress", marks=pytest.mark.xfail),
    ({"jaj": "new"},
        "complijajcated",
        "complinewcated",
        "fails map where map finishes with starting char of same map"),
    ({"jaja": "new"},
        "complijajajajacated",
        "complinewnewcated",
        "fails map where map starts while same map is in progress, and \
                in-progress map should finish"),
    ])
def test_imap(caplog, maps, test, expected, error_msg):
    caplog.set_level(logging.DEBUG)
    setMode(Mode.insert)
    for m in maps:
        imap(m, maps[m])
    assert translate_keys(test) == expected, error_msg
    # Remove imaps again
    for m in maps:
        imap(m)

def test_imap_to_esc(caplog):
    caplog.set_level(logging.DEBUG)

    setMode(Mode.insert)
    test = "I want jj"
    expected = "I want <esc>"
    imap("jj", "<esc>")
    assert translate_keys(test) == expected
    assert isMode(Mode.normal)
    imap("jj")

    test = "I want jk"
    expected = "I want <esc>"
    imap("jk", "<esc>")
    assert translate_keys(test) == expected
    assert isMode(Mode.normal)
    imap("jk")

    setMode(Mode.insert)
    expected = "<bs><bs><esc>"
    imap("jk", "<esc>")
    handleKey("j")
    assert handleKey("k" == expected), "one key at a time doesn't trigger map"
    assert isMode(Mode.normal)
    imap("jk")
