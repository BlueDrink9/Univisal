#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import os
import sys
from tempfile import gettempdir
import logging

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
logPath = gettempdir() + "univisal.log"
handler = logging.FileHandler(logPath)
handler.setLevel(logging.WARNING)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the file handler to the logger
logger.addHandler(handler)
