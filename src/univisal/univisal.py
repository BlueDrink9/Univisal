#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import logging
# Available since 3.1
# import importlib

try:
    from .message_interface import init_message_interface
    from .library import *
    from .adapter_maps import load_adapter_maps
    from . import model
    from . import config
    from . import logging_
except ImportError:
    from message_interface import init_message_interface
    from library import *
    from adapter_maps import load_adapter_maps
    import model
    import config
    import logging_
logger = logging.getLogger(__name__)

def main(args=sys.argv):
    if len(args) != 2:
        print("Usage: univisal.py adapter")
        print("""'adapter' is a string corresponding to a folder in ../adapters
        that contains a json 'mappings.json'."
        """)
        sys.exit(1)

    logger.info("Starting univisal")
    univisal_init(args[1])


def univisal_init(adapter):
    load_adapter_maps(adapter)
    config.init_config()
    model.init_model()
    init_message_interface()

main()
