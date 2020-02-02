#!/usr/bin/env python
import pytest
import unittest.mock

from univisal import handleInput

def raiseError(e=KeyError):
    raise e

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
