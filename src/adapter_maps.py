#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import json
from library import *

def load_adapter_maps(adapter):
    # Can dump a dict in python with `json.dumps(dict, sort_keys=True, indent=2)`
    try:
        adapter_maps_f=open(get_script_path() + \
                           "/../adapter/{}/mappings.json".format(adapter), "r")
        adapter_maps = json.load(adapter_maps_f)
        adapter_maps_f.close()
    except IOError as e:
        print(e)
        adapter_maps = {}
    except JSONDecodeError as e:
        print(e)
        adapter_maps = {}
    return adapter_maps

def getAdapterMap(key):
    if key in script_maps:
        return script_maps[key]
    else:
        return key

