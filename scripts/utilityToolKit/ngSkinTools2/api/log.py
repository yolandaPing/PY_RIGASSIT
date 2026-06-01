import logging
import sys

from ngSkinTools2.api.python_compatibility import Object


class DummyLogger(Object):
    def __getattr__(self, name):
        return self.doNothing

    def doNothing(self, *args, **kwargs):
        pass

    def isEnabledFor(self, *args):
        return False

    def getLogger(self, name):
        return self


class LogLineCountFilter(logging.Filter):
    def __init__(self):
        self.count = 1

    def filter(self, record):
        record.count = self.count
        self.count = (self.count + 1) % 1000
        return True


class SimpleLoggerFactory(Object):
    ROOT_LOGGER_NAME = "ngSkinTools2"

    def __init__(self, level=logging.DEBUG):
        self.level = level
        self.log = self.configureRootLogger()

    def configureRootLogger(self):
        logger = logging.getLogger(self.ROOT_LOGGER_NAME)
        logger.setLevel(self.level)
        logger.addFilter(LogLineCountFilter())
        # logger.handlers = []

        formatter = logging.Formatter("%(count)3d: [UI %(levelname)s %(filename)s:%(lineno)d] %(message)s")
        formatter.datefmt = '%H:%M:%S'

        for i in logger.handlers[:]:
            logger.removeHandler(i)

        ch = logging.StreamHandler(sys.__stdout__)
        ch.setLevel(self.level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False

        return logger

    def getLogger(self, name):
        return self.log

        self.log.debug("creating logger '%s'" % name)

        result = logging.getLogger(self.ROOT_LOGGER_NAME + "." + name)
        result.setLevel(self.level)

        result.info("alive check")
        return result


import ngSkinTools2

currentLoggerFactory = DummyLogger() if not ngSkinTools2.DEBUG_MODE else SimpleLoggerFactory(level=logging.DEBUG)


def getLogger(name):
    return currentLoggerFactory.getLogger(name)
