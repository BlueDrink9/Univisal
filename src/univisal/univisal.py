#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
# Available since 3.1
# import importlib

try:
    from .message_interface import readMessagesLoop
    from .library import *
    from .adapter_maps import load_adapter_maps
    from . import model
    from . import config
except ImportError:
    from message_interface import readMessagesLoop
    from library import *
    from adapter_maps import load_adapter_maps
    import model
    import config
logger = __import__("univisal.logger").logger.get_logger(__name__)

def main(args=sys.argv):
    checkArgs(args)
    logger.info("Starting univisal")
    adapter = args[1]
    univisal_init(adapter)

def checkArgs(args):
    if len(args) != 2:
        print(
            """Usage: univisal.py adapter
                'adapter' is a string corresponding to a folder name in
                Univisal/adapters, where the folder contains a json
                'mappings.json'. """
        )
        sys.exit(1)


def univisal_init(adapter):
    config.init_config()
    load_adapter_maps(adapter)
    model.init_model()
    readMessagesLoop()

main()
