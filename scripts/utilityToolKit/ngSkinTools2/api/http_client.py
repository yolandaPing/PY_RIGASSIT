import json
import threading

import maya.utils

from .python_compatibility import PY2

# HTTP library might not be available in batch mode
available = True

try:
    # different ways to import urlopen
    if PY2:
        from urllib import urlencode

        # noinspection PyUnresolvedReferences
        from urllib2 import HTTPError, Request, urlopen
    else:
        from urllib.error import HTTPError
        from urllib.parse import urlencode
        from urllib.request import Request, urlopen

    _ = urlencode
    _ = urlopen
    _ = Request
    _ = HTTPError
except:
    available = False


def encode_url(base_url, args):
    return base_url + "?" + urlencode(args)


def get_async(url, success_callback, failure_callback):
    def runnerFunc():
        defer_func = maya.utils.executeDeferred
        try:
            result = urlopen(url).read()
            defer_func(success_callback, json.loads(result))
        except Exception as err:
            defer_func(failure_callback, str(err))

    t = threading.Thread(target=runnerFunc)
    t.start()
    return t
