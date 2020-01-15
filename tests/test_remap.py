#!/usr/bin/env python
import os
import pytest
import sys
import unittest
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import univisal
from univisal.remap import *
from univisal.model import *
from univisal.motion import Motion
from univisal.keys import Keys
from univisal.handleInput import handleInput
from tests.mock_setup import init_univisal, clear_maps, mock_adapter_maps
from tests.translate_output import translate_keys


@pytest.fixture(scope="function")
def setUp():
    clear_maps()


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
    handleInput("j")
    assert handleInput("k") == expected, "one key at a time doesn't trigger map"
    assert isMode(Mode.normal)
    imap("jk")

@unittest.mock.patch("univisal.adapter_maps.load_adapter_maps",
            side_effect=mock_adapter_maps)
@pytest.mark.parametrize("maps, test, expected, error_msg", [
    ({"rep": "set"},
        "a rep and a rep plus one rep",
        "a set and a set plus one set",
        "fails map when joinchar is not blank."),
    ])
def test_map_with_joinchar(caplog, maps, test, expected, error_msg):
    caplog.set_level(logging.DEBUG)
    assert univisal.adapter_maps.getJoinChar() != ""
    setMode(Mode.insert)
    for m in maps:
        imap(m, maps[m])
    assert translate_keys(test) == expected, error_msg
    # Remove imaps again
    for m in maps:
        imap(m)

def test_imap_esc_followup(caplog):
    imap("jk", Keys.esc.value)
    setMode(Mode.insert)
    result = translate_keys("jkl")
    assert getMode() == Mode.normal
    assert result == Motion.right.value


def test_basic_nmap(caplog):
    caplog.set_level(logging.DEBUG)
    setMode(Mode.normal)
    expected = Motion.right.value
    assert handleInput("l") == expected
    nmap("x", "l")
    assert handleInput("x") == expected, "basic nmap doesn't work"

@pytest.mark.xfail(reason = "multi-char nmap won't work because \
        you can't backspace a normal command")
def test_multichar_nmap(caplog):
    caplog.set_level(logging.DEBUG)
    setMode(Mode.normal)
    expected = Motion.right.value * 2
    assert handleInput("ll") == expected
    nmap("x", "ll")
    assert handleInput("x") == expected, "multichar nmap doesn't work"
