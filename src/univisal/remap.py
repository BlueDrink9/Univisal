from json import loads as json_load
import logging
try:
    from .library import *
    from . import logging_
    from .model import *
except ImportError:
    from library import *
    import logging_
    from model import *
logger = logging.getLogger(__name__)

# This is going to want a better algorithm. Figure it out later, TODO.
# How to efficiently map gradual input onto a list of sequences

imaps = {}
nmaps = {}

current_mode = None
current_maps = None
current_sequence = []
# Map of sequence : index, where index is the current part of the sequence we
# are up to.
maps_in_progress = {}

def remap(maps, sequence, result=None):
    # if sequence in imaps or a subsequence of a current map:
    # raise Error "imap already exists for sequence {}
    #
    if result:
        maps[sequence] = result
        logger.info("Mapping {} to {}".format(sequence, result))
    else:
        del maps[sequence]
        logger.info("removing map for {}}".format(sequence))

def imap(sequence, result=None):
    remap(imaps, sequence, result)
def nmap(sequence, result=None):
    remap(nmaps, sequence, result)


def set_current_maps():
    global current_mode, current_maps
    # If we switch modes, discard progress.
    if current_mode != getMode():
        maps_in_progress = {}
        current_mode = getMode()

    if isMode(Mode.insert):
        current_maps = imaps
    elif isMode(Mode.normal):
        current_maps = nmaps
    else:
        logger.warning("Unknown mode for mapping: {}. \
                        No mappings exist for this mode".format(getMode()))
        current_maps = {}


def check_starts_map(key):
    global maps_in_progress
    for map_ in current_maps:
        # logger.debug("map {} in maps_in_progress {}: {}".format(map_,
            # maps_in_progress, (map_ in maps_in_progress)))
        if map_[0] == key and map_ not in maps_in_progress:
            logger.debug("Key {} starts map {}, added to maps_in_progress".format(key, map_))
            maps_in_progress[map_] = 0


def resolve_map(key):
    global maps_in_progress
    logger.debug("checking {} for maps".format(key))

    set_current_maps()
    check_starts_map(key)

    # What if there are other maps that fit the sequence, but are longer? Need
    # to wait to see what next key is. If it isn't part of a map, expand. But
    # what about timing? What if there is no next key? Probably best to not
    # allow maps inside maps.
    expired_maps = []
    for map_ in maps_in_progress:
        index = maps_in_progress[map_]
        logger.debug("map index {}; map[index] {}; key {}".format(
            index, map_[index], key))
        if map_[index] == key:
            maps_in_progress[map_] += 1
        else:
            # Broken sequence
            expired_maps.append(map_)
        if maps_in_progress[map_] == len(map_):
            # Full sequence has been matched
            maps_in_progress = {}
            logger.info("Expanding map '{}' as '{}'".format(map_, current_maps[map_]))
            # return appropriate number of backspaces.
            return ["<bs>"] * (len(map_) - 1) + [current_maps[map_]]
    for k in expired_maps:
        del maps_in_progress[k]
    return key


