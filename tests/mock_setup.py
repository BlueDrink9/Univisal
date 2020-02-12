#!/usr/bin/env python
import pytest
import unittest.mock
import sys

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


def ret_joinChar():
    return "+"


def init_univisal(with_interface=False):
    mockargs=['1', '2']
    interfaceInit = "univisal.message_interface.readMessagesLoop"
    with unittest.mock.patch('sys.argv', mockargs), \
            unittest.mock.patch("univisal.adapter_maps.loadAdapterMaps",
                                side_effect=mock_adapter_maps), \
            unittest.mock.patch("univisal.adapter_maps.getAdapterMap",
                                side_effect=ret_arg), \
            unittest.mock.patch("univisal.adapter_maps.getJoinChar",
                                side_effect=ret_joinChar):
        if with_interface:
            from univisal.__main__ import main
            main()
            univisal.message_interface.readMessagesLoop()
        else:
            with unittest.mock.patch(interfaceInit, create=True):
                from univisal.__main__ import main
                main()
    univisal.config.configStore = {}
    clear_maps()

def clear_maps():
    univisal.remap.resetMapData()
