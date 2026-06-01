"""
Influence mapping process creates a "source->destination" list for two influence lists,
describing how based on influence metadata (name, position) and mapping requirements
(mirror mode, left/right side name prefixes, etc) a mapping is created,
where "source->destination" in, say, weight transfer/mirror situation, describes that weights
currently associated with source influence, should be transfered  to destination influence.

for mirror mode, same influence can map to itself, which would generally mean "copy influence weights
on one side to be the same on the other side".

mapping is returned as "logical index"->"logical index" map.

For usage details, see unit test examples.
"""
from __future__ import division

import itertools
import json
import re

from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.python_compatibility import Object, is_string

log = getLogger("influenceMapping")


def regexpMatchAny(fragments):
    return '(' + '|'.join(fragments) + ')'


illegalCharactersRegexp = re.compile(r"[^\w_\*]")


def validate_glob(glob):
    match = illegalCharactersRegexp.search(glob)
    if match is not None:
        raise Exception("invalid pattern '{}': character {} not allowed".format(glob, match.group(0)))


def convertGlobToRegexp(glob):
    """
    :type glob: str
    """
    glob = illegalCharactersRegexp.sub("", glob)
    if "*" not in glob:  # if no stars added, just add them on both sides, e.g. "_L_" is the same as "*_L_*"
        glob = "*" + glob + "*"
    return "^" + glob.replace("*", "(.*)") + "$"


class InfluenceInfo(Object):
    """
    Metadata about an influence in a skin cluster
    """

    SIDE_LEFT = "left"
    SIDE_RIGHT = "right"
    SIDE_CENTER = "center"
    SIDE_MAP = {
        0: SIDE_CENTER,
        1: SIDE_LEFT,
        2: SIDE_RIGHT,
    }

    oppositeSides = {SIDE_LEFT: SIDE_RIGHT, SIDE_RIGHT: SIDE_LEFT}

    def __init__(self, pivot=None, path=None, name=None, logicalIndex=None, labelSide=None, labelText=None):
        self.pivot = pivot  #: influence pivot in world-space coordinates
        self.path = path  #: influence node path
        self.name = name  #: influence node name (if influence is not a DAG node, like )
        self.logicalIndex = logicalIndex  #: influence logical index in the skin cluster.
        self.labelSide = labelSide  #: joint label "side" attribute
        self.labelText = labelText  #: joint label text

    def path_name(self):
        """
        returns path if it's not None, otherwise returns name
        :return:
        """
        if self.path is not None:
            return self.path
        if self.name is None:
            raise Exception("both path and name is empty for InfluenceInfo")
        return self.name

    def __repr__(self):
        return "[InflInfo %r %r %r]" % (self.logicalIndex, self.path, self.pivot)

    def as_json(self):
        return {
            "pivot": self.pivot,
            "path": self.path,
            "name": self.name,
            "logicalIndex": self.logicalIndex,
            "labelSide": self.labelSide,
            "labelText": self.labelText,
        }

    def from_json(self, json):
        self.pivot = json["pivot"]
        self.path = json.get("path", "")
        self.name = json.get("name", "")
        self.logicalIndex = json["logicalIndex"]
        self.labelSide = json["labelSide"]
        self.labelText = json["labelText"]
        return self


def calcShortestUniqueName(influences):
    """
    calculates "uniquePath" for each influence - in a similar manner as Maya does, only in the context of single
    skincluster instead of the whole scene.
    :type influences: list[InfluenceInfo]
    """

    def commonOffset(original, sibling):
        i = 0
        for o, s in zip(original, sibling):
            if o != s:
                break
            i += 1

        # extend to full name
        while i < len(original) and original[i] != '|':
            i += 1

        return i

    for infl in influences:
        if infl.path is None:
            infl.shortestPath = infl.name

    reversedPaths = [{"path": infl.path[::-1], "infl": infl} for infl in influences if infl.path]

    # sort by line ending
    reversedPaths = sorted(reversedPaths, key=lambda item: item["path"])

    # compare path to siblings, find a shortest subpath that is different from nearest similar names
    for prev, curr, next in zip([None] + reversedPaths[:-1], reversedPaths, reversedPaths[1:] + [None]):
        minLength = curr['path'].find("|")
        if minLength < 0:
            minLength = len(curr['path'])

        prevOffset = minLength if prev is None else commonOffset(curr['path'], prev['path'])
        nextOffset = minLength if next is None else commonOffset(curr['path'], next['path'])

        curr['infl'].shortestPath = curr['path'][: max(prevOffset, nextOffset)][::-1]


def nameMatches(globs, influences, destination_influences=None, mirror_mode=False):
    """
    for each name pair, calculates a match score, and keeps matches that have highest score.

    score calculation rules:
    * each name is broken down into sections, e.g. |root|L_shoulder|L_elbow -> root, L_shoulder, L_elbow
    * for each section, find glob match, e.g. L_elbow becomes : {withoutGlob: elbow, matchedRule=L_*, oppositeRule=R_*}
    * two names are matched from the end, section by section:
        * it is assumed that a section matches if "withoutGlob" part is identical, and section1.matchedRule==section2.oppositeRule


    matching of the name happens by finding highest score

    returns map of source->destination matches
    :type globs: list[(string, string)]
    :type influences: list[InfluenceInfo]
    """

    if destination_influences is None:
        destination_influences = influences

    # 1 each path element is calculated as glob value

    globRegexps = [[re.compile(convertGlobToRegexp(i)) for i in g] for g in globs]

    # join with reversed logic
    globRegexps = globRegexps + [tuple(reversed(ge)) for ge in globRegexps]

    class GlobInfo(Object):
        def __init__(self):
            self.withoutGlob = ""
            self.matchedRule = None
            self.oppositeRule = None

    def convertPathElementToGlobInfo(pathElement):
        result = GlobInfo()
        result.withoutGlob = pathElement

        for expr, opposite in globRegexps:
            match = expr.match(pathElement)
            if match is not None:
                result.matchedRule = expr
                result.oppositeRule = opposite
                result.withoutGlob = "".join(match.groups())
                break

        return result

    def calcMatchScore(info1, info2):
        """

        :type info1: list[GlobInfo]
        :type info2: list[GlobInfo]
        """

        # optimization - if there's no chance these two paths match,
        # cut away loop logic
        if info1[0].withoutGlob != info2[0].withoutGlob:
            return 0

        score = 0

        rules_matched = False

        for e1, e2 in zip(info1, info2):
            if e1.withoutGlob != e2.withoutGlob or e1.matchedRule != e2.oppositeRule:
                break

            if e1.matchedRule is not None:
                score += 10
                rules_matched = True

            score += 1

        # in mirror mode, it's important that at least rule is matched (e.g. L->R or similar)
        if mirror_mode and not rules_matched:
            score = 0

        return score

    class MatchData(Object):
        path_split = re.compile("[\\|\\:]")

        def __init__(self, infl):
            """
            :type infl: InfluenceInfo
            """
            reversedPath = list(reversed(self.path_split.split(infl.path))) if infl.path else [infl.name]
            self.infl = infl
            self.score = 0
            self.match = None
            self.globInfo = [convertPathElementToGlobInfo(e) for e in reversedPath]

    destination_matches = [MatchData(infl) for infl in destination_influences]
    if destination_influences == influences:
        source_data = destination_matches
    else:
        source_data = [MatchData(infl) for infl in influences]

    # encapsulating for profiler
    def findBestMatches():
        for source in source_data:
            for destination in destination_matches:
                if source == destination:
                    continue

                score = calcMatchScore(source.globInfo, destination.globInfo)

                if (not mirror_mode or score > source.score) and score > destination.score:
                    destination.match = source
                    destination.score = score
                    if mirror_mode:
                        source.match = destination
                        source.score = score

    findBestMatches()

    return {md.match.infl: md.infl for md in destination_matches if md.match is not None}


def exactNameMatches(influences, destination_influences=None):
    """
    match influences by exact name
    :type influences: list[InfluenceInfo]
    """

    pass


def labelMatches(source_influences, destination_influences, mirror_mode=False):
    """
    :type source_influences: list[InfluenceInfo]
    """

    def infl_key(i):
        if i.labelText is None:
            return ("", "")

        return (i.labelText, i.labelSide)

    def group_by_label_and_side(infl_list):
        return {k: list(v) for k, v in itertools.groupby(list(sorted(infl_list, key=infl_key)), key=infl_key)}

    def as_unique_entries(l):
        return {k: v[0] for k, v in l.items() if len(v) == 1}

    result = {}

    # group by labelText+labelSide keys
    # it is essential that only unique keys are used; skip repeats of text+side on either list, as they are ambiguous
    grouped_sources = group_by_label_and_side(source_influences)
    unique_sources = as_unique_entries(grouped_sources)
    unique_destinations = unique_sources if mirror_mode else as_unique_entries(group_by_label_and_side(destination_influences))

    # "center" treatment in mirror mode: sometimes users might not set left/right sides, and "center" is actually just an untouched default;
    # in that case, just favour other influences if there are multiple "center" with the same label
    if mirror_mode:
        for (label, side), src in grouped_sources.items():
            if label == "" or side != InfluenceInfo.SIDE_CENTER:
                continue

            # only the cases of len==1 and len==2 are supported
            if len(src) == 1:
                result[src[0]] = src[0]
            else:
                result[src[0]] = src[1]
                result[src[1]] = src[0]

    # find matching label+side pairs for all destinations; flip side for mirror mode
    for (label, side), src in unique_sources.items():
        if label == "":
            continue
        if mirror_mode:
            if side == InfluenceInfo.SIDE_CENTER:
                continue
            side = InfluenceInfo.oppositeSides[side]

        dest = unique_destinations.get((label, side), None)
        if dest is not None:
            result[src] = dest

    return result


def distanceMatches(source_influences, destination_influences, threshold, mirror_axis):
    """
    :type source_influences: list[InfluenceInfo]
    :type destination_influences: list[InfluenceInfo]
    :type threshold: float
    :type mirror_axis: union(int, None)
    """

    def distance_squared(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2

    threshold_squared = threshold * threshold

    mirror_mode = mirror_axis is not None

    result = {}
    for source in source_influences:
        # if we're in mirror mode and near mirror axis, match self instead of other influence
        if mirror_mode and abs(source.pivot[mirror_axis]) < (threshold / 2.0):
            result[source] = source
            continue

        source_pivot = list(source.pivot[:])
        if mirror_mode:
            source_pivot[mirror_axis] = -source_pivot[mirror_axis]

        best_distance = None
        for destination in destination_influences:
            d = distance_squared(source_pivot, destination.pivot)
            if threshold_squared < d:
                continue

            if best_distance is None or d < best_distance:
                best_distance = d
                result[source] = destination
                if mirror_mode:
                    result[destination] = source

    return result


def dg_matches(source_influences, destination_influences, link_resolver):
    """
    :type source_influences: list[InfluenceInfo]
    :type destination_influences: list[InfluenceInfo]
    :type link_resolver:
    """

    result = {}

    dest_by_path = {i.path: i for i in destination_influences}
    for i in source_influences:
        dest = link_resolver(i.path)
        dest = None if dest is None else dest_by_path.get(dest, None)
        if dest is not None:
            result[i] = dest

    return result


class InfluenceMappingConfig(Object):
    """
    This class represents a configuration for how influences are matched for weights mirroring or transfering
    between meshes.
    """

    globs = [
        ("L_*", "R_*"),
        ("l_*", "r_*"),
        ("lf_*", "rt_*"),
        ("*_lf", "*_rt"),
    ]  #: For mirrored influences matching, this specifies the globs that will be used for name substitution

    use_dg_link_matching = True  #: turn on to use dependency graph links
    use_name_matching = True  #: should matching by name be used?
    use_label_matching = True  #: should matching by label be used?
    use_distance_matching = True  #: should matching by influence X,Y,Z coordinates be used?
    distance_threshold = 0.001  #: When matching by distance, if distance between two positions is greater than this threshold, that pair of influences is not considered as potential match.

    __mirror_axis = None
    dg_destination_attribute = "oppositeInfluence"  #: default attribute name

    @property
    def mirror_axis(self):
        """
        int: Mirror axis (0 - X, 1 - Y, 2 - Z)

        When mirror axis is not None, matching is done in "mirror" mode:

        * left/right side .globs are used;
        * matching by position uses mirrorAxis to invert positions first;

        """
        return self.__mirror_axis

    @mirror_axis.setter
    def mirror_axis(self, axis):
        if is_string(axis):
            self.__mirror_axis = ['x', 'y', 'z'].index(axis)
            return

        if axis is not None and not isinstance(axis, int):
            raise Exception("invalid axis type, need int")

        self.__mirror_axis = axis

    @classmethod
    def transfer_defaults(cls):
        """
        Builds  a mapping configuration that is suitable as default for transferring between meshes (or importing)

        Returns:
            InfluenceMappingConfig: default transfer configuration
        """
        result = InfluenceMappingConfig()
        result.mirror_axis = None
        result.globs = []
        return result

    def as_json(self):
        """
        serializes config as JSON string
        """
        return json.dumps(self.__dict__)

    def load_json(self, json_string):
        """
        loads configuration from previously saved `as_json` output
        """
        try:
            self.__dict__ = json.loads(json_string)
        except:
            pass


def default_dg_resolver(dg_attribute):
    from maya import cmds

    def resolver(input_path):
        try:
            sources = cmds.listConnections(input_path + "." + dg_attribute, source=True)
            if sources:
                return cmds.ls(sources[0], long=True)[0]
        except:
            pass
        return None

    return resolver


class InfluenceMapping(Object):
    """
    this class serves as a hub to calculate influences mapping, given a mapping config and source/destination influences
    """

    def __init__(self):
        self.config = InfluenceMappingConfig()  # type:InfluenceMappingConfig
        "assigned config"

        self.influences = []  # type: list[InfluenceInfo]
        "Source influences list. Can be assigned to result of :py:meth:`Layers.list_influences`"

        self.destinationInfluences = None
        self.calculatedMapping = None
        self.dg_resolver = lambda: default_dg_resolver(self.config.dg_destination_attribute)

    def calculate(self):
        mirror_mode = self.config.mirror_axis is not None
        log.info("calculate influence mapping, mirror mode: %s", mirror_mode)
        if self.destinationInfluences is None:
            self.destinationInfluences = self.influences

        results = []

        if mirror_mode:
            results.append(({infl: infl for infl in self.destinationInfluences}, "fallback to self"))

        if self.config.use_distance_matching:
            matches = distanceMatches(
                self.influences, self.destinationInfluences, self.config.distance_threshold, mirror_axis=self.config.mirror_axis
            )
            results.append((matches, "distance"))

        if self.config.use_name_matching:
            results.append((nameMatches(self.config.globs, self.influences, self.destinationInfluences, mirror_mode=mirror_mode), "name"))

        if self.config.use_label_matching:
            results.append((labelMatches(self.influences, self.destinationInfluences, mirror_mode=mirror_mode), "label"))

        if self.config.use_dg_link_matching:
            matches = dg_matches(self.influences, self.destinationInfluences, self.dg_resolver())
            results.append((matches, "DG link"))

        result = {}
        for mapping, matchedRule in results:
            for k, v in mapping.items():
                result[k] = {
                    "matchedRule": matchedRule,
                    "infl": v,
                }

        self.calculatedMapping = result

        return result

    @staticmethod
    def asIntIntMapping(mapping):
        """


        :meta private:
        """
        return {k.logicalIndex: v['infl'].logicalIndex for k, v in mapping.items()}
