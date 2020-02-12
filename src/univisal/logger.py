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

MAX_LOG_SIZE = 5 * 2**20  # 5 megabytes
MAX_LOG_COUNT = 3
LOG_FORMAT = '%(asctime)s %(levelname)8s - %(name)22s | %(message)s'
LOG_FILE = os.path.join(gettempdir(), "univisal_logs")

handlers = {
        "debug_file_handler": {
            "level": "DEBUG",
            "filename": "debug.log",
            "backupCount": 2,
            },
        "info_file_handler": {
            "level": "INFO",
            "filename": "info.log",
            "backupCount": 5,
            },
        "error_file_handler": {
            "level": "ERROR",
            "filename": "errors.log",
            "backupCount": 10,
            },
        "critical_file_handler": {
            "level": "CRITICAL",
            "filename": "CRITICAL.log",
            "backupCount": 10,
            },
        }


def init():
    # Log root to console as well.
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.DEBUG,
            format=LOG_FORMAT,
            handlers=[logging.StreamHandler()])


def make_logger(moduleName):
    """Setup logging configuration"""
    logger = logging.getLogger(moduleName)
    logger.setLevel(logging.DEBUG)
    for _, handler in handlers.items():
        logger.addHandler(makeHandler(handler))
    # logging.basicConfig(level=logging.DEBUG)
    return logger


def makeHandler(handler):
    filename = handler["filename"]
    level = handler["level"]
    backupCount = handler["backupCount"]
    handler = myLogHandler(filename, MAX_LOG_SIZE, backupCount)
    handler.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)

    return handler


class myLogHandler(logging.handlers.RotatingFileHandler):
    def __init__(self,filename,maxBytes,backupCount):
        path = LOG_FILE
        if not os.path.isdir(path):
            os.mkdir(path)
        super(myLogHandler,self).__init__(os.path.join(path,filename),'a',maxBytes,backupCount)


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
    return make_logger(moduleName)

init()
