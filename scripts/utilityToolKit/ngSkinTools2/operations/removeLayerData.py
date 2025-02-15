import itertools

from maya import cmds

from ngSkinTools2.api import PaintTool, target_info
from ngSkinTools2.api.session import Session
from ngSkinTools2.decorators import undoable


def as_list(arg):
    return [] if arg is None else arg


customNodeTypes = ['ngst2MeshDisplay', 'ngst2SkinLayerData']


def list_custom_nodes():
    """
    list all custom nodes in the scene
    """

    result = []
    for nodeType in customNodeTypes:
        result.extend(as_list(cmds.ls(type=nodeType)))
    return result


def list_custom_nodes_for_mesh(mesh=None):
    """
    list custom nodes only related to provided mesh. None means current selection
    """

    skin_cluster = target_info.get_related_skin_cluster(mesh)
    if skin_cluster is None:
        return []

    # delete any ngSkinTools deformers from the history, and find upstream stuff from given skinCluster.
    hist = as_list(cmds.listHistory(skin_cluster, future=True, levels=1))
    return [i for i in hist if cmds.nodeType(i) in customNodeTypes]


def list_custom_nodes_for_meshes(meshes):
    return list(itertools.chain.from_iterable([list_custom_nodes_for_mesh(i) for i in meshes]))


message_scene_noCustomNodes = 'Scene does not contain any custom ngSkinTools nodes.'
message_selection_noCustomNodes = 'Selection does not contain any custom ngSkinTools nodes.'
message_scene_warning = (
    'This command deletes all custom ngSkinTools nodes. Skin weights ' 'will be preserved, but all layer data will be lost. Do you want to continue?'
)
message_selection_warning = (
    'This command deletes custom ngSkinTools nodes for selection. Skin weights '
    'will be preserved, but all layer data will be lost. Do you want to continue?'
)


@undoable
def remove_custom_nodes(interactive=False, session=None, meshes=None):
    """
    Removes custom ngSkinTools2 nodes from the scene or selection.

    :type meshes: list[str]
    :param meshes: list of node names; if empty, operation will be scene-wide.
    :type session: Session
    :param session: optional; if specified, will fire events for current session about changed status of selected mesh
    :type interactive: bool
    :param interactive: if True, user warnings will be emited
    """
    from ngSkinTools2.ui import dialogs

    if meshes is None:
        meshes = []

    is_selection_mode = len(meshes) > 0

    custom_nodes = list_custom_nodes() if not is_selection_mode else list_custom_nodes_for_meshes(meshes)

    if not custom_nodes:
        if interactive:
            dialogs.info(message_selection_noCustomNodes if is_selection_mode else message_scene_noCustomNodes)
        return

    delete_confirmed = True
    if interactive:
        delete_confirmed = dialogs.yesNo(message_selection_warning if is_selection_mode else message_scene_warning)

    if delete_confirmed:
        cmds.delete(custom_nodes)

    if PaintTool.is_painting():
        # make sure that painting is canceled to restore mesh display etc
        cmds.setToolTo("Move")

    if session is not None:
        session.events.targetChanged.emitIfChanged()


@undoable
def remove_custom_nodes_from_selection(interactive=False, session=None):
    selection = cmds.ls(sl=True)
    remove_custom_nodes(interactive=interactive, session=session, meshes=as_list(selection))
