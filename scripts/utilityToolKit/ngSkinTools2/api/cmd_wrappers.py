from maya import cmds


def as_comma_separated_list(l):
    return ",".join((str(i) for i in l))


def get_source(plug, **kwargs):
    for i in cmds.listConnections(plug, source=True, **kwargs) or []:
        return i
    return None


def get_source_node(plug):
    return get_source(plug, plugs=False)


def get_source_plug(plug):
    return get_source(plug, plugs=True)
