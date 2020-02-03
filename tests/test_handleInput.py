#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
from univisal import model
from univisal.model import Mode, isMode, getMode, setMode
from univisal import handleInput

def raiseError(e=KeyError):
    raise e

def ret_arg(arg):
    return arg

def setup_function():
    model.init_model()

def test_handleInput_with_commandlike_input():
    inpt = ":commandlike"
    expected = "command called"
    errMsg = "commandlike inputs don't call command handler"
    with unittest.mock.patch(
        'univisal.handleInput.handleUnivisalCommand',
            return_value=expected):
        assert handleInput.handleInput(inpt) == expected, errMsg


def test_handleInput_while_disabled():
    test = "input key"
    errMsg = "HandleInput doesn't return input when univisal disabled"
    setMode(Mode.disabled)
    assert handleInput.handleInput(test) == test, errMsg


def test_handleInput_while_expecting_searchletter():
    inpt = "letter to search for"
    expected = "handle search letter"
    errMsg = "handleInput doesn't handle search letter when expecting one"
    with unittest.mock.patch(
        'univisal.handleInput.handleExpectedSearchLetter',
            return_value=expected):
        assert not handleInput.handleInput(inpt) == expected, "testing setup error"
        model.expecting_search_letter = True
        assert handleInput.handleInput(inpt) == expected, errMsg


@unittest.mock.patch('univisal.handleInput.getFallbackOutput',
                     return_value="fallback")
def test_handleInput_gets_fallback(fallbackMock):
    with unittest.mock.patch('univisal.handleInput.handleInputUnsafe',
                             side_effect=raiseError):
        result = handleInput.handleInput("test")
        error_msg = "HandleInput doesn't return fallback if error encountered while handling."
        assert result == fallbackMock(), error_msg

def test_getFallbackOutput_returns_adapter_map():
    mapping = "map"
    with unittest.mock.patch('univisal.handleInput.getAdapterMap',
                             return_value=mapping):
        inpt = "test"
        result = handleInput.getFallbackOutput(inpt)
        error_msg = "getFallbackOutput doesn't return result of getAdapterMap"
        assert result == mapping, error_msg

def test_getFallbackOutput_returns_input_on_error():
    with unittest.mock.patch('univisal.handleInput.getAdapterMap',
                             side_effect=raiseError):
        inpt = "test"
        result = handleInput.getFallbackOutput(inpt)
        error_msg = "getFallbackOutput doesn't return input if error encountered while handling."
        assert result == inpt, error_msg


def test_handleExpectedSearchLetter():
    letter = ':'
    expected = "pending motion"

    with unittest.mock.patch('univisal.handleInput.normalCommand',
                             side_effect=setOuputKeys), \
            unittest.mock.patch('univisal.handleInput.model.getPendingMotion',
                                return_value=expected):
        result = handleInput.handleExpectedSearchLetter(letter)

    assert model.getSearchLetter() == letter, \
        "handleExpectedSearchLetter doesn't set searchLetter"

    assert result == [expected], \
        "handleExpectedSearchLetter doesn't return set output keys"

def setOuputKeys(keys):
    model.extendOutputKeys(keys)
