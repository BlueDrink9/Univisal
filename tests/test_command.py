#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
from univisal import command
from univisal import model
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


@pytest.mark.parametrize("mode, expected", [
    (Mode.normal, "normal"),
    (Mode.insert, "insert"),
    (Mode.disabled, "disabled"),
    ])
def test_getMode(mode, expected):
    setMode(mode)
    error_msg = "getMode doesn't return mode in {} mode".format(expected)

def test_getConfigDir():
    from univisal.config import getConfigDir
    assert handleInput(':getConfigDir') == getConfigDir(), "getConfigDir doesn't return path"


# Have to mock the function as it is within the scope called.
@unittest.mock.patch('univisal.command.normalCommand')
@unittest.mock.patch('univisal.command.processOutput')
def test_handlePendingClipboard_strips_correct_text(mock1, mock2):
    clipboard = " copied text::"
    cmd = ":clipboard:" + clipboard

    command.handlePendingClipboard(cmd)

    assert model.captured_clipboard == clipboard
