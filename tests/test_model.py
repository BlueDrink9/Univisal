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


allModes = [mode for mode in Mode]

@pytest.mark.parametrize("mode", allModes)
def test_setMode(mode):
    setMode(mode)
    assert getMode() == mode


def test_setMode_normal_clears_pending():
    model._pending_motion = "l"
    setMode(Mode.normal)
    assert model._pending_motion == None

nonnormalModes = allModes.copy()
nonnormalModes.remove(Mode.normal)
@pytest.mark.parametrize("mode", nonnormalModes)
def test_setMode_nonnormal_not_clears_pending(mode):
    pending = "l"
    model._pending_motion = pending
    setMode(mode)
    assert model._pending_motion == pending

