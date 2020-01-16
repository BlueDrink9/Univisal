import json
import logging
import os
import pathlib
try:
    from .library import *
    from . import logging_
    from . import model
except ImportError:
    from library import *
    import logging_
    import model
logger = logging.getLogger(__name__)

# All valid options must have a default.
# An error will be raised if a user sets an option not in defaults.
defaults = {
    "load_configs" : [],
    "imaps" : {},
    "nmaps" : {},
    "cmaps" : {},
    "vmaps" : {},
}

config = {}

def getConfigOption(opt):
    try:
        return config[opt]
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
    global config
    try:
        logger.info("Loading config file at '{}'".format(path))
        config = json.load(infile)
    except (IOError, json.JSONDecodeError) as e:
        logConfigLoadError(e, path)
        config = defaults

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


def remove_invalid_config_options(subkey=None):
    if subkey:
        options = subkey
    else:
        options = config
    removeInvalidOptions(options)

def removeInvalidOptions(options):
    toRemove = []
    for opt in options:
        if opt not in defaults:
            logger.error("Not a valid option: '{}'".format(opt))
            toRemove.append(opt)
        if isinstance(opt, dict):
            remove_invalid_config_options(opt)
    for opt in toRemove:
        del options[opt]


def init_config():
    """ Initialise all user configurations. """
    init_base_config()
    for conf in getConfigOption("load_configs"):
        loadConfig(conf)
    remove_invalid_config_options()
    setMapsFromConfig()

def init_base_config():
    path = getConfigPath()
    if path.exists():
        loadConfig()
    else:
        makeDefaults()

def setMapsFromConfig():
    model.imaps = getConfigOption("imaps")
    model.nmaps = getConfigOption("nmaps")
    model.cmaps = getConfigOption("cmaps")
    model.vmaps = getConfigOption("vmaps")


