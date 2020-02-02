#!/usr/bin/env python
import pytest
import unittest.mock

import univisal
from univisal.model import Mode, isMode, getMode, setMode
from univisal.handleInput import handleInput
from univisal.keys import Keys
from univisal.vim_operator import Operator
from univisal.motion import Motion
from tests.mock_setup import init_univisal
from tests.translate_output import translate_keys

@pytest.fixture(autouse=True)
def setUp():
    init_univisal()


def handleSequence(keys):
    for key in keys:
        result = handleInput(key)
    return result


def test_escape():
    setMode(Mode.insert)
    assert getMode() == Mode.insert
    result = handleInput(Keys.esc.value)
    assert getMode() == Mode.normal
    assert result == Keys.nop.value


@pytest.mark.parametrize("motion, expected", [
    ("l", Motion.right),
    ("h", Motion.left),
    ("j", Motion.down),
    ("k", Motion.up),
    ("w", Motion.goWordNext),
    ("b", Motion.goWordPrevious),
    ("$", Motion.goLineEnd),
    ("0", Motion.goLineStart),
    ("G", Motion.goFileEnd),
    pytest.param("gg", Motion.goFileStart,
                 marks=pytest.mark.xfail(reason = 'g not implemented')),
    ])
def test_basic_motions(motion, expected):
    setMode(Mode.normal)
    result = handleInput(motion)
    assert result == expected.value, "{} returns wrong thing".format(motion)


# Handles 1, single digit, double digit with 0, double digit without 0.
@pytest.mark.parametrize("count", [1, 10, 12, 26])
def test_basic_motion_with_count(count):
    motion='l'
    motionVal=Motion.right.value
    inpt = str(count) + motion
    expected=motionVal * count
    setMode(Mode.normal)
    result = translate_keys(inpt)
    print("number of repeats in result: {}".format(result.count(motionVal)))
    print("current repeat count: {}".format(univisal.model.getRepeatCount()))
    assert result == expected, "motion with count {} returns wrong thing".format(count)

# @pytest.mark.xfail(reason = 'unfinished implementation')
def test_basic_delete_motion():
    setMode(Mode.normal)
    result = handleSequence("dw")
    expected = [Operator.visualStart, Motion.goWordNext, \
        Operator.visualPause, Operator.delete]
    assert result == expected, "basic delete with motion fails (dw)"


@pytest.mark.xfail(reason = 'unfinished implementation')
def test_repeat_delete_motion():
    setMode(Mode.normal)
    result = handleSequence("3dw")
    expected = 3 * ([Operator.visualStart, Motion.goWordNext, \
        Operator.visualPause, Operator.delete])
    assert result == expected, "repeated delete with motion fails (3dw)"

@pytest.mark.xfail(reason = 'unfinished implementation')
def test_delete_repeat_motion():
    setMode(Mode.normal)
    result = handleSequence("d3w")
    expected = 3 * ([Operator.visualStart, Motion.goWordNext, \
        Operator.visualPause, Operator.delete])
    assert result == expected, "delete with repeated motion fails (d3w)"

@pytest.mark.xfail(reason = 'unfinished implementation')
def test_repeat_delete_repeat_motion():
    setMode(Mode.normal)
    result = handleSequence("3d3w")
    expected = 9 * ([Operator.visualStart, Motion.goWordNext, \
        Operator.visualPause, Operator.delete])
    assert result == expected, "repeated delete with repeated motion fails (3d3w)"


@pytest.mark.xfail(reason = 'unfinished test implementation')
def test_f():
    assert Keys.requestSelectedText.value in translate_keys("fm")
    result = translate_keys("<clipboard>end of this is m and text")
    # TODO Account for deselect, then movement.
    assert result == "<left>" + "<right>" * 16

# TODO: F, t, T.
