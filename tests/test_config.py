#!/usr/bin/env python
import os
import pytest
import unittest.mock
import sys
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from univisal.remap import *
from univisal import config
from univisal.config import *


@pytest.fixture(scope="function", autouse=True)
def clear_config():
    config.configStore = {}


@pytest.mark.parametrize("test_opt, expected, error_msg", [
    ("imaps", {}, "loads dict option incorrectly"),
    ("load_configs", [], "loads list option incorrectly"),
    ("trash option", None, "Fails loading non-existant option")
])
def test_defaults(caplog, tmpdir, test_opt, expected, error_msg):
    caplog.set_level(logging.DEBUG)
    with unittest.mock.patch('univisal.config.getConfigPath',
                             return_value=tmpdir / "univisal" / "config.json"):
        makeDefaults()
        loadConfig()
    assert getConfigOption(test_opt) == expected, error_msg

@pytest.mark.parametrize("conf, test_opt, expected, error_msg", [
    ({"imaps": {"jk": "<esc>"}}, "imaps", {"jk": "<esc>"},
     "imaps dict not loaded properly with one entry"),
    ({"imaps": {"jk": "<esc>", "~": "/home/user"}},
     "imaps", {"jk": "<esc>", "~": "/home/user"},
     "imaps dict not loaded properly with two entries"),
    ({"imaps": {"jk": "<esc>", "~": "/home/user"},
      "load_configs": ["trash", "path"]},
     "imaps", {"jk": "<esc>", "~": "/home/user"},
     "imaps dict not loaded properly with two entries and multiple options"),
    ({"imaps": {"jk": "<esc>", "~": "/home/user"},
      "load_configs": ["trash", "path"]},
     "load_configs", ["trash", "path"],
     "load_configs dict not loaded properly with two entries and multiple options"),
])
def test_config(caplog, tmpdir, conf, test_opt, expected, error_msg):
    caplog.set_level(logging.DEBUG)
    with unittest.mock.patch('univisal.config.getConfigPath',
                             return_value=tmpdir / "univisal" / "config.json"):
        init_config()
    config.configStore = conf
    assert getConfigOption(test_opt) == expected, error_msg

def test_additional_config(caplog, tmpdir):
    import json
    caplog.set_level(logging.DEBUG)
    with unittest.mock.patch('univisal.config.getConfigPath',
                             return_value=tmpdir / "univisal" / "config.json"):
        path = tmpdir / "config2.json"
        config.defaults["load_configs"] = [str(path)]
        makeDefaults()
        test = {"imaps": {"vk": "<esc>"}}
        expected = {"vk": "<esc>"}
        error_msg = "Additional config not loaded properly"
        with open(path, 'w') as outfile:
            json.dump(test, outfile, indent=2, ensure_ascii=False)
        init_config()
    assert getConfigOption("imaps") == expected, error_msg

@pytest.mark.parametrize("level, expected", [
    ("debug", logging.DEBUG),
    ("info", logging.INFO),
    ("error", logging.ERROR),
    ("warning", logging.WARNING),
    ("info", logging.INFO),
])
def test_log_level(level, expected):
    import logging
    config.configStore={"log_level": level}
    setLogLevel()
    result = logging.getLogger().getEffectiveLevel()
    assert result == expected, \
        "Setting log level '{}' doesn't change effective level (is {})".format(
            level, result)



@pytest.mark.parametrize("opt, expected, msg", [
    (False, "m", "Unused normal keys are swallowed when they should not be"),
    (True, "", "Unused normal keys are not swallowed when they should be"),
    ])
def test_swallow_unused_normal(opt, expected, msg):
    from tests.mock_setup import init_univisal
    from univisal.handleInput import handleInput
    from univisal.handleKey import handleSingleInputKey

    init_univisal()
    config.configStore={"swallow_unused_normal_keys": opt}
    setMode(Mode.normal)
    # Test handling the single key, then the whole input to confirm.
    result = handleSingleInputKey("m")
    assert result == expected, msg + " after handleSingleInputKey"
    result = handleInput("m")
    assert result == expected, msg + " after handleInput"
