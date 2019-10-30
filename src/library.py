#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import os
import sys
import json
import logging
import logging.config
from tempfile import gettempdir

# LOG_CFG=path is an env variable, uses `path` as config.
def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.error("Couldn't find logging config json at path '" + path + "'")
        logging.basicConfig(level=default_level)

    # logging.config.filename

# setup_logging(os.path.join(get_script_path(), '..', 'logging_py.json'), logging.DEBUG)
# logPath = os.path.join(gettempdir(), "univisal.log")

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

setup_logging(os.path.join(get_script_path(), '..', 'logging_py.json'), logging.DEBUG)

# logger = logging.getLogger(__name__)
# logger.config.filename(
logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')
