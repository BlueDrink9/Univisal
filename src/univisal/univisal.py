#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import sys
import logging
# Available since 3.1
# import importlib

try:
    from .message_interface import init_message_interface
    from .library import *
    from .adapter_maps import *
    from .handleKey import *
    from .library import *
    from . import model
    from . import config
    from . import logging_
except ImportError:
    from message_interface import init_message_interface
    from library import *
    from adapter_maps import *
    from handleKey import *
    import model
    import config
    import logging_
logger = logging.getLogger(__name__)

if len(sys.argv) != 2:
    print("Usage: univisal.py adapter")
    print("""'adapter' is a string corresponding to a folder in ../adapters
    that contains a json 'mappings.json'."
    """)
    sys.exit(1)

logger.info("Starting univisal")

load_adapter_maps(sys.argv[1])

config.init_config()
init_model()
init_message_interface()
