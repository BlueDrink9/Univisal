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

def ret_arg(arg):
    return arg


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


@pytest.mark.parametrize("sequence, count, errmsg", [
    ("dw", 1, "basic delete with motion fails"),
    ("3dw", 3, "repeated delete with motion fails"),
    ("d3w", 3, "delete with repeated motion fails"),
    pytest.param("3d3w", 9, "repeated delete with repeated motion fails", marks=pytest.mark.xfail),
])
@unittest.mock.patch("univisal.handleKey.formatOutputForAdapter",
                     side_effect=ret_arg)
def test_delete_motion(mock, sequence, count, errmsg):
    setMode(Mode.normal)
    result = handleSequence(sequence)
    # Left as plus to make it easier to move the count.
    expected = count * ([Operator.visualStart] + [Motion.goWordNext] + \
        [Operator.visualPause]) + [Operator.change]
    assert result == expected, errmsg + " ({})".format(sequence)
    assert isMode(Mode.insert)


@pytest.mark.xfail(reason="change not implemented")
@pytest.mark.parametrize("sequence, count, errmsg", [
    ("cw", 1, "basic change with motion fails"),
    ("3cw", 3, "repeated change with motion fails"),
    ("c3w", 3, "change with repeated motion fails"),
    pytest.param("3c3w", 9, "repeated change with repeated motion fails", marks=pytest.mark.xfail),
])
@unittest.mock.patch("univisal.handleKey.formatOutputForAdapter",
                     side_effect=ret_arg)
def test_delete_motion(mock, sequence, count, errmsg):
    setMode(Mode.normal)
    result = handleSequence(sequence)
    # Left as plus to make it easier to move the count.
    expected = count * ([Operator.visualStart] + [Motion.goWordNext] + \
        [Operator.visualPause]) + [Operator.delete]
    assert result == expected, errmsg + " ({})".format(sequence)




@pytest.mark.parametrize("key, operator", [
    ("y", Operator.yank),
    ("d", Operator.delete),
    pytest.param("c", Operator.change, marks=pytest.mark.xfail),
])
@unittest.mock.patch("univisal.handleKey.formatOutputForAdapter",
                     side_effect=ret_arg)
def test_double_operator(mock, key, operator):
    setMode(Mode.normal)
    result = handleSequence(key*2)
    expected = [Motion.goLineStart,
                Operator.visualStart,
                Motion.goLineEnd,
                Operator.visualPause] + [operator]
    assert result == expected, "double {} fails".format(key)
    # TODO test and handle dd yy cc with a count


@pytest.mark.xfail(reason = 'unfinished test implementation')
def test_f():
    assert Keys.requestSelectedText.value in translate_keys("fm")
    result = translate_keys("<clipboard>end of this is m and text")
    # TODO Account for deselect, then movement.
    assert result == "<left>" + "<right>" * 16

# TODO: F, t, T.
