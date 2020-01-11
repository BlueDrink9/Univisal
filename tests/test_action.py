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
from univisal.motion import Motion
from tests.mock_setup import init_univisal
from tests.translate_output import translate_keys

@pytest.fixture(autouse=True)
def setUp():
    init_univisal()


@pytest.mark.parametrize("motion, expected, error_msg", [
    ("l",
        # getAdapterMap(motion.goRight.name),
        (Motion.right.name),
        "l returns wrong thing"),
    ])
def test_basic_motions(motion, expected, error_msg):
    result = handleInput(motion)
    assert result == expected, error_msg

def test_f():
    assert Keys.requestSelectedText.value in translate_keys("fw")
    result = translate_keys("<clipboard>end of this is w and text")
    assert result == "<right>" * 16

# TODO: F, t, T.
