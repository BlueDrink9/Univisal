#!/usr/bin/env python
import pytest
import unittest.mock
import logging

import univisal
import univisal.model as model
from univisal.model import increaseRepeatCount
from univisal.model import Mode, getMode, setMode
from univisal.keys import Keys

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


@pytest.mark.parametrize("count", [1, 5])
def test_repeatOutputKeys(count):
    model.__repeat_count = count
    key = "<esc>"
    model.__outputKeys = [key]
    model.repeatOutputKeys()
    assert model.__outputKeys == [key] * count, \
        "repeatOutputKeys doesn't change outputKey count correctly"

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

def test_checkValidMode(caplog):
    caplog.set_level(logging.ERROR)
    model.checkValidMode(Mode.normal)
    model.checkValidMode(Keys.esc)
    errors = [record for record in caplog.records if record.levelno >= logging.ERROR]
    assert errors[0].msg == "Not a valid mode: 'Keys.esc'"


def test_init_model():
    model.init_model()
    assert model.__outputKeys == []
    assert getMode() == Mode.normal
    # Just one test to make sure clear_pending was called.
    assert not model.expecting_search_letter

@pytest.mark.xfail(reason="Not implemented yet, test unfinished")
def test_init_registers():
    registers = {
    }
    assert model._registers == registers

def test_clear_pending():
    model.expecting_clipboard = True
    model.expecting_search_letter = True
    model._pending_motion = ""
    model._captured_clipboard = ""
    model._search_letter = ""

    model.clear_pending()

    assert not model.expecting_clipboard
    assert not model.expecting_search_letter
    assert model._pending_motion is None
    assert model._captured_clipboard is None
    assert model._search_letter is None
    assert model.pending_operator is None


def test_popOuputKeys():
    test = ["key1", "key2"]
    model.__outputKeys = test.copy()
    assert model.popOutputKeys() == test, "popOutputKeys doesn't output keys"
    assert model.__outputKeys == [], "popOutputKeys doesn't reset keys"

extendOutputKeysTests = [
    ["key1", "key2"],
    ["key"],
    "key",
    [Keys.esc, Keys.space],
    Keys.esc,
    "l",
]
@pytest.mark.parametrize("keys", extendOutputKeysTests)
def test_extendOutputKeysSingleCall(keys):
    model.extendOutputKeys(keys)
    errmsg = "extendOutputKeys fails with keys '{}'".format(keys)
    if not isinstance(keys, list):
        keys = [keys]
    else:
        keys = keys
    assert model.popOutputKeys() == keys, errmsg

@pytest.mark.parametrize("keys", extendOutputKeysTests)
def test_extendOutputKeysMultipleCall(keys):
    count = 5
    for _ in range(count):
        model.extendOutputKeys(keys)
    errmsg = "extendOutputKeys fails with {} times keys '{}'".format(count, keys)
    if not isinstance(keys, list):
        keys = [keys]
    else:
        keys = keys
    keys = keys * count
    assert model.popOutputKeys() == keys, errmsg

@pytest.mark.parametrize("keys", [
    ["key1", "key2"],
    [Keys.esc, Keys.space],
])
def test_extendOutputKeysSingleCallMultiArg(keys):
    model.extendOutputKeys(*keys)
    errmsg = "extendOutputKeys fails with keys '{}'".format(keys)
    if not isinstance(keys, list):
        keys = [keys]
    else:
        keys = keys
    assert model.popOutputKeys() == keys, errmsg

@pytest.mark.parametrize("keys", [
    ["key1", "key2"],
    [Keys.esc, Keys.space],
])
def test_extendOutputKeysMultipleCallMultiArgs(keys):
    count = 5
    for _ in range(count):
        model.extendOutputKeys(*keys)
    errmsg = "extendOutputKeys fails with {} times keys '{}'".format(count, keys)
    if not isinstance(keys, list):
        keys = [keys]
    else:
        keys = keys
    keys = keys * count
    assert model.popOutputKeys() == keys, errmsg
