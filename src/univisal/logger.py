#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import sys, os
import json
import logging
import logging.config
from tempfile import gettempdir

from . import library
# Usage:
# logger = __import__("univisal.logger").logger.get_logger(__name__)


def init():
    logConfigPath=os.path.join(library.get_script_path(), '..', '..', 'logging_py.json')
    setup_logging(logConfigPath, logging.DEBUG)

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
        config = loadDictFromJson(path)
        logHandlerConcreteClass = myLogHandler.__module__ + ".myLogHandler"
        config = replaceClassValuesWithClass(config, logHandlerConcreteClass)
        print(config)
        logging.config.dictConfig(config)
    else:
        logging.error("Couldn't find logging config json at path '" + path + "'")
        logging.basicConfig(level=default_level)

    # logging.config.filename

def loadDictFromJson(path):
    with open(path, 'rt') as f:
        return json.load(f)

def replaceClassValuesWithClass(dict_, new_class):
    for handlerName, handler in dict_['handlers'].items():
        handler['class'] = new_class
    return dict_

# Any unhandled exceptions will be logged.
def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    """Handler for unhandled exceptions that will write to the logs"""
    # logger = get_logger(__name__)
    if issubclass(exc_type, KeyboardInterrupt):
        # call the default excepthook saved at __excepthook__
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical("Unhandled exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_unhandled_exception

def get_logger(moduleName):
    return logging.getLogger(moduleName)

init()
