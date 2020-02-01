import json
import logging
import os
import pathlib
try:
    from .library import *
    from . import model
    from .model import Mode
    from . import remap
except ImportError:
    from library import *
    import model
    from model import Mode
    import remap
logger = __import__("univisal.logger").logger.get_logger(__name__)

# All valid options must have a default.
# An error will be raised if a user sets an option not in defaults.
defaults = {
    "load_configs" : [],
    "log_level": "warning",
    "swallow_unused_normal_keys": "false",
    "imaps" : {},
    "nmaps" : {},
    "cmaps" : {},
    "vmaps" : {},
}

configStore = {}

def getConfigOption(opt):
    try:
        return configStore[opt]
    except KeyError:
        # Try to load a default if custom not set.
        logger.info("Loading default for option '{}'".format(opt))
        try:
            return defaults[opt]
        except KeyError:
            logger.error("No default config option detected for '{}'. Option is not valid".format(opt),
                        exc_info=1)
        return None


def loadConfig(path = None):
    if path is None:
        path = pathlib.Path(getConfigPath())
    else:
        path = pathlib.Path(path)
    path = path.expanduser()
    with open(path, 'r') as infile:
        readInConfig(path, infile)

def readInConfig(path, infile):
    global configStore
    try:
        logger.info("Loading config file at '{}'".format(path))
        configStore = json.load(infile)
    except (IOError, json.JSONDecodeError) as e:
        logConfigLoadError(e, path)
        configStore = defaults

def logConfigLoadError(e, path):
    if isinstance(e, IOError):
        errorAction = "loading"
    else:
        errorAction = "decoding"
    logger.warning("Error {} config filemap: '{}'. \
                   Using defaults.".format(errorAction, path),
                   exc_info=True)


def getConfigDir():
    # Not using appdirs (https://pypi.org/project/appdirs/), because we want
    # OSX to be treated ike unix.
    if os.name == "nt":
        # Windows
        config_dir = pathlib.Path(os.getenv("APPDATA") / "univisal")
    else:
        config_dir = pathlib.Path(os.getenv("XDG_CONFIG_HOME", "~/.config")) / "univisal"
    return config_dir

def getConfigPath():
    config_path = getConfigDir() / "config.json"
    return config_path


def makeDefaults():
    path = getConfigPath()
    # only PurePath has .parent, only Path has .exists()
    dir_ = pathlib.Path(pathlib.PurePath(path).parent)
    if not dir_.exists():
        dir_.mkdir(parents=True)
    with open(path, 'w') as outfile:
        logger.info("Making default config file at '{}'".format(path))
        json.dump(defaults, outfile, indent=2, ensure_ascii=False)


def init_config():
    """ Initialise all user configurations. """
    init_base_config()
    for conf in getConfigOption("load_configs"):
        loadConfig(conf)
    removeInvalidOptions(configStore)
    applyOptions()

def init_base_config():
    path = getConfigPath()
    if path.exists():
        loadConfig()
    else:
        makeDefaults()

def removeInvalidOptions(options):
    toRemove = []
    for opt in options:
        if opt not in defaults:
            logger.error("Not a valid option: '{}'".format(opt))
            toRemove.append(opt)
        if isinstance(opt, dict):
            removeInvalidOptions(opt)
    for opt in toRemove:
        del options[opt]


def applyOptions():
    setLogLevel()
    setMaps()

def setLogLevel():
    levelStr = getConfigOption("log_level")
    if levelStr == "debug":
        level = logging.DEBUG
    elif levelStr == "info":
        level = logging.INFO
    elif levelStr == "error":
        level = logging.ERROR
    elif levelStr == "warning":
        level = logging.WARNING
    elif levelStr == "critical":
        level = logging.CRITICAL
    logging.getLogger().setLevel(level)

def setMaps():
    for maps in ["imaps", "nmaps", "cmaps", "vmaps"]:
        mode = getMapMode(maps)
        remap.addMapsFromDict(mode, getConfigOption(maps))

def getMapMode(mapstype):
    if mapstype == "imaps":
        return Mode.insert
    elif mapstype == "nmaps":
        return Mode.normal
    elif mapstype == "cmaps":
        return Mode.command
    elif mapstype == "vmaps":
        return Mode.visual
    else:
        # Should only ever raise if someone modifies the above function, not if
        # a user enters a strange config.
        raise KeyError

