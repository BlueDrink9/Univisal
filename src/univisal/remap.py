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
vmaps = {}
cmaps = {}

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
        logger.info("removing map for {}".format(sequence))

def imap(sequence, result=None):
    remap(imaps, sequence, result)
def nmap(sequence, result=None):
    remap(nmaps, sequence, result)


def set_current_maps_for_mode():
    global current_mode, current_maps, maps_in_progress
    # If we switch modes, discard progress.
    if current_mode != getMode():
        maps_in_progress = {}
        current_mode = getMode()
        logger.debug("Mode changed, discarding maps_in_progress")

    if isMode(Mode.insert):
        current_maps = imaps
    elif isMode(Mode.normal):
        current_maps = nmaps
    elif isMode(Mode.visual):
        current_maps = vmaps
    elif isMode(Mode.command):
        current_maps = cmaps
    elif isMode(Mode.operator_pending):
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
            # logger.debug("Key {} starts map {}, added to maps_in_progress".format(key, map_))
            maps_in_progress[map_] = 0


def resolve_map(key):
    global maps_in_progress
    # logger.debug("checking {} for maps".format(key))

    set_current_maps_for_mode()
    check_starts_map(key)

    # What if there are other maps that fit the sequence, but are longer? Need
    # to wait to see what next key is. If it isn't part of a map, expand. But
    # what about timing? What if there is no next key? Probably best to not
    # allow maps inside maps.
    maps_no_longer_in_progress = []
    for map_, progress in maps_in_progress.items():
        thisKeyIsNextInMap = map_[progress] == key

        if thisKeyIsNextInMap:
            incrementMapProgress(map_)
            logger.debug("Key '{}' is member {} of mapped sequence '{}'".format(key, progress+1, map_))
        else:  # Broken sequence
            maps_no_longer_in_progress.append(map_)

        if isCompleteMatch(map_):
            resetMapsInProgress()
            return getRemappedKeys(map_)

    for m in maps_no_longer_in_progress:
        del maps_in_progress[m]
    return [key]

def getEnoughBackspacesToErase(map_):
    backspaces = []
    if modeIsInsertLike():
        # return appropriate number of backspaces.
        backspaces = ["<bs>"] * (len(map_) - 1)
    return backspaces

def getRemappedKeys(map_):
    backspaces = getEnoughBackspacesToErase(map_)
    remappedKeys = backspaces + [current_maps[map_]]
    logger.info("Expanded map '{}' as '{}'".format(map_,
                                                   remappedKeys))
    return remappedKeys

def isCompleteMatch(map_):
    return maps_in_progress[map_] == len(map_)

def incrementMapProgress(map_):
    maps_in_progress[map_] += 1


def resetMapData():
    global imaps, nmaps, vmaps, cmaps, current_mode, current_maps
    imaps = {}
    nmaps = {}
    vmaps = {}
    cmaps = {}

    current_mode = None
    current_maps = None
    resetMapsInProgress()

def resetMapsInProgress():
    global current_sequence, maps_in_progress
    current_sequence = []
    maps_in_progress = {}
