# -*- coding: utf-8 -*-

# .FileName:clear_commands.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/22 23:21
# .Finish time:
import json
from py_rigAssit.dialogs import base_dir, decorator, mayaPrint
from py_rigAssit.common.command_dispatcher import CommandDispatcher
from OptimizeSceneFun import OptimizeScene
from Popumenus import GUIPopupMenu

import maya.cmds as cmds, maya.mel as mel

optimized = OptimizeScene()
popupMenu = GUIPopupMenu()

@CommandDispatcher.register("Clean NameSpace")
@decorator.undo
def removeNameSpase(ui):
    optimized.removeNameSpase()


@CommandDispatcher.register("Optimize Scene")
@decorator.undo
def optimizeScene(ui):
    mel.eval('OptimizeScene;')


@CommandDispatcher.register("Check Scene Name")
@decorator.undo
def checkSceneName(ui):
    mel.eval('source ' + json.dumps(base_dir + "scripts/mel/checkSceneName.mel"))


@CommandDispatcher.register("Delete unknown Node")
@decorator.undo
def DeleteunknownNode(ui):
    optimized.deleteunUsedNodes()


@CommandDispatcher.register("Delete unknown Node")
@decorator.undo
def DeleteunknownNode(ui):
    optimized.deleteunKnowNodes()


@CommandDispatcher.register("Delete unUsedOrig")
@decorator.undo
def DeleteunUsedOrig(ui):
    optimized.deleteUnuseOrig()


@CommandDispatcher.register("Delete unDisplayPoint")
@decorator.undo
def DeleteunDisplayPoint(ui):
    optimized.Clean_invalid_displayPoints()


@CommandDispatcher.register("Delete unUsedPlug")
@decorator.undo
def DeleteunUsedPlug(ui):
    optimized.clean_unknown_plugins()


@CommandDispatcher.register("Delete unUsedDagPose")
@decorator.undo
def DeleteunUsedDagPose(ui):
    optimized.delete_unused_dagpose_nodes()


@CommandDispatcher.register("UnLockNode Selected")
@decorator.undo
def UnLockNodeSelected(ui):
    optimized.CleanUNLockNode(False)


@CommandDispatcher.register("UnLockNode Scene")
@decorator.undo
def unLockNodeScene(ui):
    optimized.CleanUNLockNode(True)


@CommandDispatcher.register("UnLock initialShading")
@decorator.undo
def unLockinitialShading(ui):
    mel.eval('lockNode -l 0 -lu 0 initialShadingGroup;')


@CommandDispatcher.register("setIsHistoricallyInteresting")
@decorator.undo
def setIsHistoricallyInteresting(ui):
    optimized.setIsHistoricallyInteresting()


@CommandDispatcher.register("Maya Script Editor")
def charcoalEditor(ui):
    import maya.mel as mel
    import syntax_jd as syntax_jd
    mel.eval("ScriptEditor;")
    syntax_jd.wrap()


@CommandDispatcher.register("CharcoalEditor2")
def charcoalEditor(ui):
    import maya.cmds as cmds
    if not cmds.pluginInfo('CharcoalEditor2', q=True, l=True):
        cmds.loadPlugin('CharcoalEditor2')
    mel.eval("charcoalEditor2;")


@CommandDispatcher.register("Delete Orig Nodes")
@decorator.undo
def delete_orig_node(ui):
    mel.eval('source ' + json.dumps(base_dir + "scripts/mel/deleteAllIntermediates.mel"))

    objs = cmds.ls(sl=1)
    if objs:
        for i in objs:
            mel.eval('deleteAllIntermediates( "{}" );'.format(i))


@CommandDispatcher.register("Select Input Node")
@decorator.undo
def select_attr_input_node(ui):
    popupMenu._select_attr_input_node()


@CommandDispatcher.register("Combine Skinweight")
@decorator.undo
def combine_skinweight(ui):
    popupMenu._combine_skinweight()


@CommandDispatcher.register("Linked Surface")
@decorator.undo
def linked_surface(ui):
    popupMenu.linked_surface()


@CommandDispatcher.register("Curve Keep Linked")
@decorator.undo
def keep_linked(ui, keep=False):
    if keep:
        popupMenu.keep_linked()
    else:
        popupMenu.run_locked()


@CommandDispatcher.register("Mirror Skin")
@decorator.undo
def mirror_skin(ui, lr=True):
    if lr:
        popupMenu._mirror_skin()
    else:
        popupMenu._open_mirror_skin_tool()


@CommandDispatcher.register("Create Joints")
@decorator.undo
def create_joint(ui):
    popupMenu._create_joint()


@CommandDispatcher.register("Joints Add Shape")
@decorator.undo
def create_joint(ui):
    popupMenu._joint_add_shape()










