#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
from univisal import message_interface

def raiseError(e=KeyError):
    raise e

def ret_arg(arg):
    return arg


def mock_read():
    return mock_messages.pop(0)
def mock_write(key):
    message_output.append(key)
@unittest.mock.patch('univisal.message_interface.inpt_read',
                     side_effect=mock_read)
@unittest.mock.patch('univisal.message_interface.outpt_write',
                     side_effect=mock_write)
def test_readMessagesLoop(mock_read, mock_write):
    global mock_messages, message_output
    message_output = []
    # None to finish (would normally be returned by process_input, but that's
    # mocked to return read data.
    mock_messages = ["t", "a", None]
    expected = mock_messages[:-1].copy()
    errMsg = "Messages loop doesn't write correct sequence"
    with unittest.mock.patch(
        'univisal.message_interface.process_input',
            side_effect=ret_arg):
        message_interface.readMessagesLoop()
    assert message_output == expected, errMsg
