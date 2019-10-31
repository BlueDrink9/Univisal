#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import json
import logging
from library import *
import logging_
logger = logging.getLogger(__name__)

adapter_maps = None

def load_adapter_maps(adapter):
    global adapter_maps
    # Can dump a dict in python with `json.dumps(dict, sort_keys=True, indent=2)`
    try:
        adapter_maps_p=get_script_path() + \
                           "/../adapter/{}/mappings.json".format(adapter)
        adapter_maps_f=open(adapter_maps_p, "r")
        adapter_maps = json.load(adapter_maps_f)
        adapter_maps_f.close()
    except IOError as e:
        logger.error("Error loading adapter map: {}".format(adapter_maps_p), exc_info=(exc_type, exc_value, exc_traceback))
        adapter_maps = {}
    except JSONDecodeError as e:
        logger.error("Error decoding adapter map {}".format(adapter_maps_p), exc_info=(exc_type, exc_value, exc_traceback))
        adapter_maps = {}
    return adapter_maps

def getAdapterMap(key):
    global adapter_maps
    if key in adapter_maps:
        return adapter_maps[key]
    else:
        return key

