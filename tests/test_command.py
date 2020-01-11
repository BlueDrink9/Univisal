#!/usr/bin/env python
import os
import pytest
import unittest.mock
import sys
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from univisal.model import Mode, isMode, getMode, setMode
from univisal.handleKey import handleKey
from univisal.keys import Keys
from univisal.motion import Motion

def ret_arg(arg):
    return arg

@pytest.fixture(autouse=True)
def init_univisal():
    mockargs=['1', '2']
    with unittest.mock.patch('sys.argv', mockargs), \
    unittest.mock.patch("univisal.message_interface.init_message_interface",
        create=True), \
    unittest.mock.patch("univisal.adapter_maps.load_adapter_maps"), \
    unittest.mock.patch("univisal.adapter_maps.getAdapterMap",
        side_effect=ret_arg), \
    unittest.mock.patch("univisal.adapter_maps.getJoinChar",
            side_effect=ret_arg):
        from univisal.univisal import main
        main()
    univisal.config.config = {}


def test_disable():
    assert getMode() == Mode.normal, "Univisal not set up"
    handleKey(":disable")
    assert getMode() == Mode.disabled, "Disable does not change mode"
    assert handleKey('l') == 'l', "Disabled univisal does not return normal key"
    assert handleKey(Keys.esc.value) == (Keys.esc.value), \
        "Disabled univisal does not return special keys"

def test_enable():
    handleKey(":disable")
    assert getMode() == Mode.disabled, "Disable does not change mode"
    handleKey(":enable")
    assert handleKey('l') == Motion.right.name, "re-enabled univisal does not return motion"

