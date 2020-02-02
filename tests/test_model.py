#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
import univisal.model as model
from univisal.model import increaseRepeatCount

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


allModes = [mode for mode in model.Mode]
@pytest.mark.parametrize("mode", allModes)
def test_setMode(mode):
    model.setMode(mode)
    assert model.getMode() == mode


