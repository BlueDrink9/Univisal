#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import json
import logging
import os
try:
    from .library import *
    from . import logging_
except ImportError:
    from library import *
    import logging_
logger = logging.getLogger(__name__)

adapter_maps = None

def load_adapter_maps(adapter):
    global adapter_maps
    # Can dump a dict in python with `json.dumps(dict, sort_keys=True, indent=2)`
    try:
        adapter_maps_p=os.path.join(get_script_path(),
                "..", "..", "adapters", adapter, "mappings.json")
        adapter_maps_f=open(adapter_maps_p, "r")
        adapter_maps = json.load(adapter_maps_f)
        adapter_maps_f.close()
        logger.info("Loaded adapter map file {}".format(adapter_maps_p))
    except IOError as e:
        logger.error("Error loading adapter map: {}".format(adapter_maps_p), exc_info=True)
        adapter_maps = {}
    except JSONDecodeError as e:
        logger.error("Error decoding adapter map {}".format(adapter_maps_p), exc_info=True)
        adapter_maps = {}
    return adapter_maps

def getAdapterMap(key):
    global adapter_maps
    if adapter_maps is None:
        return key
    if key in adapter_maps:
        logger.debug("Mapping {} to adapter key {}".format(key, adapter_maps[key]))
        return adapter_maps[key]
    else:
        return key

