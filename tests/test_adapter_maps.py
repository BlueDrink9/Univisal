#!/usr/bin/env python
import pytest
import unittest.mock
import json

from univisal.keys import Keys
from univisal import adapter_maps


@pytest.fixture(scope="function", autouse=True)
def setup(caplog, tmpdir):
    pass
    # caplog.set_level(logging.DEBUG)
    # with unittest.mock.patch('univisal.config.getConfigPath',
    #                          return_value=tmpdir / "univisal" / "config.json"):
    #     init_config()

def dumpDictToFile(dict_, path):
    with open(path, 'w') as outfile:
        json.dump(dict_, outfile, indent=2, ensure_ascii=False)

@pytest.fixture(scope='function', autouse=True)
def mapPath(tmpdir):
    with unittest.mock.patch(
        'univisal.adapter_maps.getMappingPath',
        return_value=tmpdir / "univisal" / "mappings.json"
    ) as path:
        yield path

@pytest.mark.parametrize("mock_maps, key, expected, error_msg", [
    ({Keys.esc.value: "escape"}, Keys.esc.value, "escape",
     "adapter map isn't returned correctly"),
    ({"not a valid key": "non-valid"}, "unmapped key", "unmapped key",
     "unmapped adapter key isn't returned as original key"),
])
def test_getMap(caplog, mock_maps, key, expected, error_msg):
    # caplog.set_level(logging.DEBUG)
    adapter_maps.adapter_maps = mock_maps
    assert adapter_maps.getAdapterMap(key) == expected, error_msg


# @pytest.mark.parametrize("test_opt, expected, error_msg", [
#     ("imaps", {}, "loads dict option incorrectly"),
# ])
# def test_load_adapter_maps(caplog, tmpdir, test_opt, expected, error_msg):
#     caplog.set_level(logging.DEBUG)
#     with unittest.mock.patch('univisal.config.getConfigPath',
#                              return_value=tmpdir / "univisal" / "config.json"):
#         makeDefaults()
#         loadConfig()
#     assert getConfigOption(test_opt) == expected, error_msg

# @pytest.mark.parametrize("conf, test_opt, expected, error_msg", [
#     ({"imaps": {"jk": "<esc>"}}, "imaps", {"jk": "<esc>"},
#      "imaps dict not loaded properly with one entry"),
#     ({"imaps": {"jk": "<esc>", "~": "/home/user"}},
#      "imaps", {"jk": "<esc>", "~": "/home/user"},
#      "imaps dict not loaded properly with two entries"),
#     ({"imaps": {"jk": "<esc>", "~": "/home/user"},
#       "load_configs": ["trash", "path"]},
#      "imaps", {"jk": "<esc>", "~": "/home/user"},
#      "imaps dict not loaded properly with two entries and multiple options"),
#     ({"imaps": {"jk": "<esc>", "~": "/home/user"},
#       "load_configs": ["trash", "path"]},
#      "load_configs", ["trash", "path"],
#      "load_configs dict not loaded properly with two entries and multiple options"),
# ])
# def test_config(caplog, tmpdir, conf, test_opt, expected, error_msg):
#     caplog.set_level(logging.DEBUG)
#     config.configStore = conf
#     assert getConfigOption(test_opt) == expected, error_msg

# def test_additional_config(caplog, tmpdir):
#     import json
#     caplog.set_level(logging.DEBUG)
#     with unittest.mock.patch('univisal.adapter_maps.getMappingPath',
#                              return_value=tmpdir / "univisal" /
#                              "mappings.json"):
#         test = {"imaps": {"vk": "<esc>"}}
#         expected = {"vk": "<esc>"}
#         error_msg = "Additional config not loaded properly"
#         init_config()
#     assert getConfigOption("imaps") == expected, error_msg

# @pytest.mark.parametrize("mapConfEntry, error_msg", [
#     ({"imaps": {"jk": "<esc>"}}, "configured imaps did not expand"),
#     ({"nmaps": {"j": "<left>"}}, "configured nmaps did not expand"),
#     ({"nmaps": {"j": "<left>", "k": "<right>"}},
#     "configured nmaps did not expand when multiple are configured"),
# ])
# def test_config_setMaps(mapConfEntry, error_msg):
#     config.configStore = mapConfEntry
#     config.setMaps()
#     for mapModeType, maps in mapConfEntry.items():
#         setCorrectModeForMap(mapModeType)
#         assertMapsExpandCorrectly(maps, error_msg)

# def setCorrectModeForMap(mapModeType):
#     mode = getMapMode(mapModeType)
#     model.setMode(mode)

# def assertMapsExpandCorrectly(maps, error_msg):
#     for sequence, expansion in maps.items():
#         result = expandMap(sequence)
#         assert result == [expansion], error_msg

# def expandMap(sequence):
#     for char in sequence:
#         # Deliberately overwrite, we only want the last result (the
#         # expansion).
#         result = remap.resolve_map(char)
#     removeBackspaces(result)
#     return result

# def removeBackspaces(lst):
#     bs = Keys.backspace.value
#     lst.remove(bs) if (bs in lst) else ''


# @pytest.mark.parametrize("level, expected", [
#     ("debug", logging.DEBUG),
#     ("info", logging.INFO),
#     ("error", logging.ERROR),
#     ("warning", logging.WARNING),
#     ("critical", logging.CRITICAL),
# ])
# def test_log_level(level, expected):
#     import logging
#     config.configStore={"log_level": level}
#     setLogLevel()
#     result = logging.getLogger().getEffectiveLevel()
#     assert result == expected, \
#         "Setting log level '{}' doesn't change effective level (is {})".format(
#             level, result)



# @pytest.mark.parametrize("opt, expected, msg", [
#     (False, "m", "Unused normal keys are swallowed when they should not be"),
#     (True, "", "Unused normal keys are not swallowed when they should be"),
#     ])
# def test_swallow_unused_normal(opt, expected, msg):
#     from tests.mock_setup import init_univisal
#     from univisal.handleInput import handleInput
#     from univisal.handleKey import handleVimInputKey

#     init_univisal()
#     config.configStore={"swallow_unused_normal_keys": opt}
#     setMode(Mode.normal)
#     # Test handling the single key, then the whole input to confirm.
#     result = handleVimInputKey("m")
#     assert result == expected, msg + " after handleSingleInputKey"
#     result = handleInput("m")
#     assert result == expected, msg + " after handleInput"
