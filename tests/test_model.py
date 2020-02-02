#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
import univisal.model as model
from univisal.model import increaseRepeatCount
from univisal.model import Mode, getMode, setMode

@pytest.mark.parametrize("numbers", [1, 10, 15, 329, 991])
def test_increaseRepeatCount(numbers):
    model.clear_pending()
    # Only inputs one digit at a time, so this iterates them.
    # Using as a string treats numbers like the individual digits.
    for number in str(numbers):
        increaseRepeatCount(int(number))
    # This time using numbers as int, as all digits.
    assert model.getRepeatCount() == numbers, \
        "Repeat count is incorrect after {}".format(numbers)

def test_resetRepeatCount():
    model.__repeat_count = 32847192734
    model.resetRepeatCount()
    assert model.__repeat_count == 0

allModes = [mode for mode in Mode]

@pytest.mark.parametrize("mode", allModes)
def test_setMode(mode):
    setMode(mode)
    assert getMode() == mode


def test_setMode_normal_clears_pending():
    model._pending_motion = "l"
    setMode(Mode.normal)
    assert model._pending_motion is None

nonnormalModes = allModes.copy()
nonnormalModes.remove(Mode.normal)
@pytest.mark.parametrize("mode", nonnormalModes)
def test_setMode_nonnormal_not_clears_pending(mode):
    pending = "l"
    model._pending_motion = pending
    setMode(mode)
    assert model._pending_motion == pending


def test_init_model():
    model.init_model()
    assert model.__outputKeys == []
    assert getMode() == Mode.normal
    # Just one test to make sure clear_pending was called.
    assert not model.expecting_search_letter

@pytest.mark.xfail("Not implemented yet, test unfinished")
def test_init_registers():
    registers = {
    }
    assert model._registers == registers

def test_clear_pending():
    assert not model.expecting_clipboard
    assert not model.expecting_search_letter
    assert model._pending_motion is None
    assert model._captured_clipboard is None
    assert model._search_letter is None
