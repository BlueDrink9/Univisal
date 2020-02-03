#!/usr/bin/env python
import pytest
import unittest.mock
import json

from univisal.keys import Keys
from univisal import adapter_maps


def dumpDictToFile(dict_, path):
    with open(path, 'w') as outfile:
        json.dump(dict_, outfile, indent=2, ensure_ascii=False)


@pytest.fixture(scope="function", autouse=True)
def setup(caplog, tmpdir):
    adapter_maps.adapter_maps = {}

@pytest.fixture(scope='session', autouse=True)
def mapPath(tmpdir_factory):
    """
    :type request: _pytest.python.SubRequest
   :return:
    """
    tmpdir = tmpdir_factory.mktemp("mappings")
    patched = unittest.mock.patch(
        'univisal.adapter_maps.getMappingPath',
        return_value=tmpdir / "mappings.json"
    )
    patched.__enter__()

    def unpatch():
        patched.__exit__()
        log.info("Patching complete. Unpatching")
        request.addfinalizer(unpatch)

@pytest.mark.parametrize("mock_maps, key, expected, error_msg", [
    ({Keys.esc.value: "escape"}, Keys.esc.value, "escape",
     "adapter map isn't returned correctly"),
    ({Keys.esc.value: "escape"}, Keys.esc, "escape",
     "adapter map using enum isn't returned correctly"),
    ({"not a valid key": "non-valid"}, "unmapped key", "unmapped key",
     "unmapped adapter key isn't returned as original key"),
])
def test_getAdapterMap(caplog, mock_maps, key, expected, error_msg):
    # caplog.set_level(logging.DEBUG)
    adapter_maps.adapter_maps = mock_maps
    assert adapter_maps.getAdapterMap(key) == expected, error_msg

@pytest.mark.parametrize("mock_maps, key, expected, error_msg", [
    ({Keys.multikey_join_char.value: "{+}"}, "", "{+}",
     "getJoinChar returns wrong value"),
    ({}, "", "",
     "getJoinChar doesn't return blank when no multikey_join_char map exists"),
])
def test_getJoinChar(caplog, mock_maps, key, expected, error_msg):
    # caplog.set_level(logging.DEBUG)
    adapter_maps.adapter_maps = mock_maps
    assert adapter_maps.getJoinChar() == expected, error_msg

# def test_getMappingPath():

def test_loadAdapterMaps(mapPath):
    key = Keys.space.value
    value = "{space}"
    mock_maps = {key: value}
    dumpDictToFile(mock_maps, adapter_maps.getMappingPath(""))

    adapter_maps.loadAdapterMaps("")

    assert adapter_maps.adapter_maps == mock_maps, \
        "Adapter maps don't load correctly"
    assert adapter_maps.getAdapterMap(key) == value, \
        "Loaded adapter maps don't provide values for lookup"
