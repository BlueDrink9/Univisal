#!/usr/bin/env python
import os
import pytest
import unittest.mock
import sys
# Add src dir to the python path so we can import.
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")
from univisal.remap import *
import univisal.config
from univisal.config import *


@pytest.fixture(scope="function", autouse=True)
def clear_config():
    univisal.config.config = {}


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
    univisal.config.config = conf
    assert getConfigOption(test_opt) == expected, error_msg

def test_additional_config(caplog, tmpdir):
    import json
    caplog.set_level(logging.DEBUG)
    with unittest.mock.patch('univisal.config.getConfigPath',
                             return_value=tmpdir / "univisal" / "config.json"):
        path = tmpdir / "config2.json"
        univisal.config.defaults["load_configs"] = [str(path)]
        makeDefaults()
        test = {"imaps": {"vk": "<esc>"}}
        expected = {"vk": "<esc>"}
        error_msg = "Additional config not loaded properly"
        with open(path, 'w') as outfile:
            json.dump(test, outfile, indent=2, ensure_ascii=False)
        init_config()
    assert getConfigOption("imaps") == expected, error_msg

