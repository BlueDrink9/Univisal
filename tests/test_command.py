#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
from univisal.model import Mode, isMode, getMode, setMode
from univisal.handleInput import handleInput
from univisal.keys import Keys
from univisal.motion import Motion
from tests.mock_setup import init_univisal

@pytest.fixture(autouse=True)
def setUp():
    init_univisal()


def test_disable():
    assert getMode() == Mode.normal, "Univisal not set up"
    handleInput(":disable")
    assert getMode() == Mode.disabled, "Disable does not change mode"
    assert handleInput('l') == 'l', "Disabled univisal does not return normal key"
    assert handleInput(Keys.esc.value) == ("<esc>"), \
        "Disabled univisal does not return special keys"

def test_enable():
    handleInput(":disable")
    assert getMode() == Mode.disabled, "Disable does not change mode"
    handleInput(":enable")
    assert handleInput('l') == Motion.right.value, "re-enabled univisal does not return motion"

def test_getMode():
    assert handleInput(':getMode') == "normal", "getMode doesn't return mode"
    setMode(Mode.insert)
    assert handleInput(':getMode') == "insert", "getMode doesn't return mode in insert mode"
    setMode(Mode.disabled)
    assert handleInput(':getMode') == "disabled", "getMode doesn't return mode when disabled"

def test_getConfigDir():
    from univisal.config import getConfigDir
    assert handleInput(':getConfigDir') == getConfigDir(), "getConfigDir doesn't return path"
