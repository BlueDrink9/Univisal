from json import loads as json_load
try:
    from .library import *
    from .model import *
except ImportError:
    from library import *
    from model import *
logger = __import__("univisal.logger").logger.get_logger(__name__)

# This is going to want a better algorithm. Figure it out later, TODO.
# How to efficiently map gradual input onto a list of sequences

maps = None
current_mode = None
current_maps = None
# Map of sequence : index, where index is the current part of the sequence we
# are up to.
maps_in_progress = {}

def resetMapData():
    global current_mode, current_maps
    init_maps()

    current_mode = None
    current_maps = None
    resetMapsInProgress()

def init_maps():
    global maps
    maps = {
        Mode.insert: {},
        Mode.normal: {},
        Mode.visual: {},
        Mode.command: {},
    }

def resetMapsInProgress():
    global maps_in_progress
    maps_in_progress = {}

resetMapData()

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
    remap(maps[Mode.insert], sequence, result)
def nmap(sequence, result=None):
    remap(maps[Mode.normal], sequence, result)
def vmap(sequence, result=None):
    remap(maps[Mode.visual], sequence, result)
def cmap(sequence, result=None):
    remap(maps[Mode.command], sequence, result)

def addMapsFromDict(mode, newmaps):
    for sequence, result in newmaps.items():
       remap(maps[mode], sequence, result)


def set_current_maps_for_mode():
    global current_maps
    # If we switch modes, discard progress.
    updateCurrentMode()

    try:
        current_maps = maps[current_mode]
    except KeyError:
        if isMode(Mode.operator_pending):
            current_maps = maps[Mode.normal]
        else:
            logger.warning("Unknown mode for mapping: {}. \
                            No mappings exist for this mode".format(getMode()))
            current_maps = {}

def updateCurrentMode():
    global current_mode
    # If we switch modes, discard progress.
    if current_mode != getMode():
        current_mode = getMode()
        resetMapsInProgress()
        logger.debug("Mode changed, discarding maps_in_progress")


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
            return getOutputMapExpansion(map_)

    for m in maps_no_longer_in_progress:
        del maps_in_progress[m]
    return [key]

def getEnoughBackspacesToErase(map_):
    backspaces = []
    if modeIsInsertLike():
        # return appropriate number of backspaces.
        backspaces = ["<bs>"] * (len(map_) - 1)
    return backspaces

def getOutputMapExpansion(map_):
    backspaces = getEnoughBackspacesToErase(map_)
    remappedKeys = backspaces + [current_maps[map_]]
    logger.info("Expanded map '{}' as '{}'".format(map_,
                                                   remappedKeys))
    return remappedKeys

def isCompleteMatch(map_):
    return maps_in_progress[map_] == len(map_)

def incrementMapProgress(map_):
    maps_in_progress[map_] += 1


