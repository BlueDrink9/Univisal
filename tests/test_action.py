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
from univisal import Keys
from univisal import Motion
from tests.mock_setup import init_univisal
from tests.translate_output import translate_keys

@pytest.fixture(autouse=True)
def setUp():
    init_univisal()


@pytest.mark.parametrize("motion, expected, error_msg", [
    ("l",
        # getAdapterMap(motion.goRight.name),
        (Motion.right),
        "l returns wrong thing"),
    ])
def test_basic_motions(motion, expected, error_msg):
    result = handleInput(motion)
    assert result == expected, error_msg

# @pytest.mark.xfail
def test_f():
    translate_keys("fw")
    assert Keys.requestSelectedText in translate_keys("fw")
    result = translate_keys("<clipboard>end of this is w and text")
    # TODO Account for deselect, then movement.
    assert result == "<right>" * 16

# TODO: F, t, T.
