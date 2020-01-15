#!/usr/bin/env python
import os
import pytest
import unittest.mock
import sys
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import univisal
from univisal.model import Mode, isMode, getMode, setMode
from univisal.handleInput import handleInput
from univisal.keys import Keys

def mock_adapter_maps(_):
    univisal.adapter_maps.adapter_maps = {
            "<multikey_join_char>": "+",
            }

def ret_arg(arg):
    return arg

def init_univisal():
    mockargs=['1', '2']
    with unittest.mock.patch('sys.argv', mockargs), \
    unittest.mock.patch("univisal.message_interface.init_message_interface",
        create=True), \
    unittest.mock.patch("univisal.adapter_maps.load_adapter_maps",
            side_effect=mock_adapter_maps), \
    unittest.mock.patch("univisal.adapter_maps.getAdapterMap",
        side_effect=ret_arg), \
    unittest.mock.patch("univisal.adapter_maps.getJoinChar",
            side_effect=ret_arg):
        from univisal.univisal import main
        main()
    univisal.config.config = {}
    clear_maps()

def clear_maps():
    imaps = {}
    nmaps = {}
    vmaps = {}
    cmaps = {}
