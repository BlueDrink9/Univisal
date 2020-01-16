#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import json
import logging
import enum
import os
try:
    from .library import *
    from . import logging_
    from .keys import Keys
except ImportError:
    from library import *
    import logging_
    from keys import Keys
logger = logging.getLogger(__name__)

adapter_maps = None

def load_adapter_maps(adapter):
    global adapter_maps
    # Can dump a dict in python with `json.dumps(dict, sort_keys=True, indent=2)`
    try:
        adapter_maps_path = getMappingPath(adapter)
        with open(adapter_maps_path, "r") as adapter_maps_file:
            adapter_maps = json.load(adapter_maps_file)

        logger.info("Loaded adapter map file {}".format(adapter_maps_path))

    except (IOError, json.JSONDecodeError) as e:
        logAdapterError(e, adapter_maps_path)
        adapter_maps = {}
    return adapter_maps

def getMappingPath(adapter):
    adapter_maps_path=os.path.join(get_script_path(),
            "..", "..", "adapters", adapter, "mappings.json")
    return adapter_maps_path

def logAdapterError(e, path):
    if isinstance(e, IOError):
        errorAction = "loading"
    else:
        errorAction = "decoding"
    logger.error("Error {} adapter map: {}".format(errorAction, path),
                 exc_info=True)


def getAdapterMap(key):
    global adapter_maps
    if adapter_maps is None:
        return key
    if isinstance(key, enum.Enum):
        lookup = key.value
    else:
        lookup = key

    if lookup in adapter_maps:
        result = adapter_maps[lookup]
        logger.debug("Mapping {} to adapter key {}".format(lookup, result))
        return result
    else:
        return key


def getJoinChar():
    lookup = Keys.multikey_join_char
    joinChar = getAdapterMap(lookup)
    # This happens if the adapter doesn't have a map for this.
    if joinChar == lookup:
        return ""
    return joinChar
