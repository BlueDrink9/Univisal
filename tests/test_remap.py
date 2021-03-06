#!/usr/bin/env python
import pytest
import unittest
import logging

import univisal
from univisal import remap
from univisal.remap import imap, nmap
from univisal.model import Mode, isMode, setMode, getMode
from univisal.motion import Motion
from univisal.keys import Keys
from univisal.handleInput import handleInput
from tests.mock_setup import init_univisal, clear_maps, mock_adapter_maps
from tests.translate_output import translate_keys


def setup_function():
    remap.resetMapData()

def teardown_function():
    remap.resetMapData()

allMappedModes = [Mode.insert, Mode.normal, Mode.visual, Mode.command]


def test_resetMapData():
    remap.resetMapData()
    assert remap.maps == {
        Mode.insert: {},
        Mode.normal: {},
        Mode.visual: {},
        Mode.command: {},
    }
    assert remap.current_mode is None
    assert remap.current_maps is None
    assert remap.maps_in_progress == {}


def test_remap():
    k, v = "sequence", "result"
    remap.remap(remap.maps[Mode.normal], k, v)
    assert remap.maps[Mode.normal] == {k: v}

def test_remap_from_dict():
    maps = {"sequence": "result"}
    remap.addMapsFromDict(Mode.normal, maps)
    assert remap.maps[Mode.normal] == maps


@pytest.mark.parametrize("mode", allMappedModes)
def test_set_current_maps_for_mode(mode):
    remap.maps = {
        Mode.insert: {'ins': 'ert'},
        Mode.normal: {'nor': 'mal'},
        Mode.visual: {'vis': 'ual'},
        Mode.command: {'com': 'mand'},
    }
    setMode(mode)
    remap.set_current_maps_for_mode()
    assert remap.current_maps == remap.maps[mode]


@pytest.mark.parametrize("mode", allMappedModes)
def test_updateCurrentMode(mode):
    setMode(mode)
    remap.updateCurrentMode()
    assert remap.current_mode == mode




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

@unittest.mock.patch("univisal.adapter_maps.loadAdapterMaps",
            side_effect=mock_adapter_maps)
@pytest.mark.parametrize("maps, test, expected, error_msg", [
    ({"rep": "set"},
        "a rep and a rep plus one rep",
        "a set and a set plus one set",
        "fails map when joinchar is not blank."),
    ])
def test_map_with_joinchar(caplog, maps, test, expected, error_msg):
    caplog.set_level(logging.DEBUG)
    univisal.adapter_maps.adapter_maps = {Keys.multikey_join_char.value: "+"}
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

def test_mode_change_clears_maps_in_progress(caplog):
    caplog.set_level(logging.DEBUG)
    iLhs="savag"
    iRhs="role"
    imap(iLhs, iRhs)
    nmap("g", "l")
    setMode(Mode.insert)
    # maps_in_progress should be iLhs minus end char (sava)
    insertExpected = (iLhs[:-1])
    assert translate_keys(insertExpected) == insertExpected
    assert not maps_in_progress_is_blank()
    setMode(Mode.normal)
    # Need to send one more key to trigger the map check.
    translate_keys("l")
    assert maps_in_progress_is_blank()

def test_mode_change_not_affects_remaps(caplog):
    caplog.set_level(logging.DEBUG)
    iLhs="savag"
    iRhs="role"
    imap(iLhs, iRhs)
    nmap("g", "l")
    setMode(Mode.insert)
    # maps_in_progress should be iLhs minus end char (sava)
    insertExpected = (iLhs[:-1])
    assert translate_keys(insertExpected) == insertExpected
    assert not maps_in_progress_is_blank()
    setMode(Mode.normal)
    assert translate_keys("g") == Motion.right.value
    setMode(Mode.insert)
    assert translate_keys("g") == "g"
    assert translate_keys(iLhs) == iRhs

def maps_in_progress_is_blank():
    return len(univisal.remap.maps_in_progress) == 0

@pytest.mark.xfail(reason = "multi-char nmap won't work because \
        you can't backspace a normal command")
def test_multichar_nmap(caplog):
    caplog.set_level(logging.DEBUG)
    setMode(Mode.normal)
    expected = Motion.right.value * 2
    assert handleInput("ll") == expected
    nmap("x", "ll")
    assert handleInput("x") == expected, "multichar nmap doesn't work"
