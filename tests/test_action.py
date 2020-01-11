#!/usr/bin/env python
import os
import pytest
import unittest.mock
import sys
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import univisal
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

def translate_keys(keys):
    """
    Converts a string/list of keypresses according to univisal rules.
    Expands <bs> as a backspace.
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

def test_f():
    assert Keys.requestSelectedText.value in translate_keys("fw")
    result = translate_keys("<clipboard>end of this is w and text")
    assert result == "<right>" * 16

# TODO: F, t, T.
