#!/usr/bin/env python
import os
import pytest
import unittest.mock
import sys
import logging
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
import univisal
import univisal.model as model
from univisal.model import increaseRepeatCount

@pytest.mark.parametrize("numbers", [1, 10, 15, 329, 991])
def test_increaseRepeatCount(numbers):
    model.repeat_count = 0
    # Only inputs one digit at a time, so this iterates them.
    for number in str(numbers):
        increaseRepeatCount(int(number))
    assert model.repeat_count == numbers, \
        "Repeat count is incorrect after {}".format(numbers)


