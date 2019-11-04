#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import sys, os
import json
import logging
import logging.config
from tempfile import gettempdir
try:
    from .library import *
except ImportError:
    from library import *

class myLogHandler(logging.handlers.RotatingFileHandler):
    def __init__(self,filename,maxBytes,backupCount,encoding):
        path = os.path.join(gettempdir(), "univisal_logs")
        if not os.path.isdir(path):
            os.mkdir(path)
        super(myLogHandler,self).__init__(os.path.join(path,filename),'a',maxBytes,backupCount,encoding)

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

# setup_logging(os.path.join(get_script_path(), 'logging_py.json'), logging.DEBUG)
setup_logging(os.path.join(get_script_path(), '..', '..', 'logging_py.json'), logging.DEBUG)
logger = logging.getLogger(__name__)

# Any unhandled exceptions will be logged.
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    """Handler for unhandled exceptions that will write to the logs"""
    if issubclass(exc_type, KeyboardInterrupt):
        # call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_unhandled_exception

# logger = logging.getLogger(__name__)
# logger.config.filename(
