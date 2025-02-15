"""
The purpose of the module is mostly for testing: close everything and prepare for source reload
"""
from __future__ import print_function

from ngSkinTools2.api.log import getLogger

handlers = []

log = getLogger("cleanup")


def registerCleanupHandler(handler):
    handlers.append(handler)


def cleanup():
    while len(handlers) > 0:
        handler = handlers.pop()
        try:
            handler()
        except Exception as err:
            log.error(err)
