try:
    from .library import *
    from . import logging_
    from .pipes_windows import *
except ImportError:
    from library import *
    from pipes_windows import *
    import logging_


data = inpt_read()
logger.debug("data :'{}'".format(data))
