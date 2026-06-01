from ngSkinTools2.api import plugin
from ngSkinTools2.api.python_compatibility import Object

COPYRIGHT = "<span>&copy; Viktoras Makauskas, 2012-2021</span>"
PRODUCT_URL = "https://www.ngskintools.com"


def pluginVersion():
    """
    Unique version of plugin, e.g. "1.0beta.680". Also represents
    required version of mll plugin. Automatically set at build time
    """
    pluginVersion_doNotEdit = "2.1.6"
    return pluginVersion_doNotEdit


def buildWatermark():
    """
    returns a unique ID of this build.
    will be set by a build system and stored in the plugin binary
    """

    return plugin.ngst2License(q=True, watermark=True)


def uniqueClientId():
    """
    returns a unique ID for this installation. randomly generated at first run.
    """
    from ngSkinTools2.ui.options import config

    if config.unique_client_id.get() is None:
        config.unique_client_id.set(generate_unique_client_id())
    return config.unique_client_id.get()


# returns random hexadecimal 40-long string
def generate_unique_client_id():
    import random

    result = ""
    for i in range(10):
        result += "%0.4x" % random.randrange(0xFFFF)

    return result


class SemanticVersion(Object):
    def __init__(self, stringVersion):
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.preRelease = None
        self.parse(stringVersion)

    def parse(self, stringVersion):
        import re

        pattern = re.compile(r"(\d+)(\.(\d+)((\.)(\d+))?)?(-([a-zA-Z0-9]+))?")

        def toInt(s):
            try:
                return int(s)
            except:
                return 0

        result = pattern.match(stringVersion)
        if result is None:
            raise Exception("Invalid version string: '{0}'".format(stringVersion))

        self.major = toInt(result.group(1))
        self.minor = toInt(result.group(3))
        self.patch = toInt(result.group(6))
        self.preRelease = result.group(8)


def compare_semver(currentVersion, candidateVersion):
    """
    returns negative if current version is bigger, 0 if versions are equal and positive if candidateVersion is higher.

    e.g.

    1.0, 1.1 -> 1
    1.0, 1.0-beta -> -1

    """
    currentVersion = SemanticVersion(currentVersion)
    candidateVersion = SemanticVersion(candidateVersion)

    if currentVersion.major != candidateVersion.major:
        return candidateVersion.major - currentVersion.major
    if currentVersion.minor != candidateVersion.minor:
        return candidateVersion.minor - currentVersion.minor
    if currentVersion.patch != candidateVersion.patch:
        return candidateVersion.patch - currentVersion.patch
    if currentVersion.preRelease != candidateVersion.preRelease:
        if currentVersion.preRelease is None:
            return -1
        if candidateVersion.preRelease is None:
            return 1
        return 1 if candidateVersion.preRelease > currentVersion.preRelease else -1

    return 0
