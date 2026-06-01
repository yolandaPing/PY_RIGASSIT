import sys

PY2 = sys.version_info[0] == 2
PY3 = not PY2


def is_string(obj):
    if PY2:
        # noinspection PyUnresolvedReferences
        return isinstance(obj, basestring)

    return isinstance(obj, str)


# need to use a new-style class in case of python2, or "normal" class otherwise
if PY2:

    class Object(object):
        pass

else:

    class Object:
        pass
