#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
from univisal import message_interface
from univisal.message_interface import process_input, tryHandle

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


def test_process_input_returns_blank_with_no_input():
    assert process_input('') == ''


def test_process_input_returns_on_HUP():
    assert process_input('HUP') == None


@pytest.mark.parametrize("test", [
    "l", "multichar", " ",
])
def test_process_input_returns_a_result(test):
    errmsg = "process input returns wrong value with input '{}'".format(test)
    with unittest.mock.patch(
        'univisal.message_interface.tryHandle',
            side_effect=ret_arg):
        assert process_input(test) == test, errmsg


@pytest.mark.parametrize("test", [
    "output", "", " ",
])
def test_tryHandle_calls_handle(test):
    with unittest.mock.patch(
        'univisal.message_interface.handleInput',
            return_value=test+"salt"):
        assert tryHandle(test) == test+"salt"


def test_tryHandle_with_exception():
    test = "input"
    with unittest.mock.patch(
        'univisal.message_interface.handleInput',
            side_effect=raiseError):
        assert tryHandle(test) == test


@pytest.mark.parametrize("output", [
    ["output"], [], {}, 5,
])
def test_tryHandle_with_nonstr_output(output):
    test = "input"
    with unittest.mock.patch(
        'univisal.message_interface.handleInput',
            return_value=output):
        assert tryHandle(test) == test
