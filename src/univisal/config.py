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
        logger.info("Loading default for option '{}'".format(opt))
        try:
            return defaults[opt]
        except KeyError:
            logger.warning("No config option detected for '{}'".format(opt),
                        exc_info=1)
        return None

def getConfigDir():
    # Not using appdirs (https://pypi.org/project/appdirs/), because we want
    # OSX to be treated ike unix.
    # Windows
    if os.name == "nt":
        config_dir = pathlib.Path(os.getenv("APPDATA") / "univisal")
    else:
        config_dir = pathlib.Path(os.getenv("XDG_CONFIG_HOME", "~/.config"))
    return config_dir

def getConfigPath():
    config_path = getConfigDir() / "config.json"
    return config_path


def makeDefaults():
    path = getConfigPath()
    dir_ = pathlib.Path(pathlib.PurePath(path).parent)
    if not dir_.exists():
        dir_.mkdir(parents=True)
    with open(path, 'w') as outfile:
        logger.info("Making default config file at '{}'".format(path))
        json.dump(defaults, outfile, indent=2, ensure_ascii=False)


def loadConfig(path = None):
    global config
    if path is None:
        path = pathlib.Path(getConfigPath())
    else:
        path = pathlib.Path(path)
    with open(path.expanduser(), 'r') as infile:
        try:
            logger.info("Loading config file at '{}'".format(path))
            config = json.load(infile)
        except IOError as e:
            logger.warning("Error loading config filemap: '{}'. \
                           Using defaults.".format(path), exc_info=True)
            config = defaults
        except JSONDecodeError as e:
            logger.warning("Error decoding config file '{}'. \
                           Using defaults.".format(path), exc_info=True)
            config = defaults


def validate_config():
    for opt in config:
        if opt not in defaults:
            raise ValueError("Not a valid option: '{}'".format(opt))


def init_config():
    path = getConfigPath()
    if path.exists():
        loadConfig()
    else:
        makeDefaults()

    model.imaps = getConfigOption("imaps")
    model.nmaps = getConfigOption("nmaps")
    model.cmaps = getConfigOption("cmaps")
    model.vmaps = getConfigOption("vmaps")
    for conf in getConfigOption("load_configs"):
        loadConfig(conf)
    validate_config()


