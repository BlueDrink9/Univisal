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
    out = ''.join(out)
    # Simulate sending the backspaces
    while "<bs>" in out:
        index = out.index("<bs>")
        out = out[:index -1] + out[index + len("<bs>"):]
    # need to iteratively replace <bs> with removed char
    return ''.join(out)


@pytest.mark.parametrize("maps, test, expected, error_msg", [
    ({"map": "pam"},
        "complimacated",
        "complimacated",
        "fails map where 2/3 match"),
    ({"j": "a"},
        "j",
        "a",
        "fails single-char map"),
    ({"map": "pam"},
        "eamapsy",
        "eapamsy",
        "fails simple map in middle of sequence"),
    ({"map": "pam"},
        "complimapcated",
        "complipamcated",
        "fails map in middle of a word with one starting letter early"),
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



@pytest.mark.parametrize("maps, test, expected, error_msg", [
    ({"jj": "<esc>"},
        "I want jj",
        "I want ",
        "jj imapped to escape doesn't expand properly"),
    ({"jk": "<esc>"},
        "I want jk",
        "I want ",
        "jk imapped to escape doesn't expand properly"),
    ])
def test_imap_to_esc(caplog, maps, test, expected, error_msg):
    caplog.set_level(logging.DEBUG)
    setMode(Mode.insert)
    for m in maps:
        imap(m, maps[m])
    assert translate_keys(test) == expected, error_msg
    assert isMode(Mode.normal)
    # Remove imaps again
    for m in maps:
        imap(m)

def test_imap_to_esc_one_at_a_time(caplog):
    caplog.set_level(logging.DEBUG)
    setMode(Mode.insert)
    expected = "<bs>"
    imap("jk", "<esc>")
    handleKey("j")
    assert handleKey("k") == expected, "one key at a time doesn't trigger map"
    assert isMode(Mode.normal)
    imap("jk")