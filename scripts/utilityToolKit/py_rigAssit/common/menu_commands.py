# -*- coding: utf-8 -*-

# .FileName:clear_commands.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/22 23:21
# .Finish time:

import os
import json
import maya.cmds as cmds
import maya.mel as mel
from py_rigAssit.dialogs import base_dir, decorator, mayaPrint
from py_rigAssit.common.command_dispatcher import CommandDispatcher


@CommandDispatcher.register("Clean NameSpace")
@decorator.undo
def removeNameSpase(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().removeNameSpase()


@CommandDispatcher.register("Optimize Scene")
@decorator.undo
def optimizeScene(ui):
    mel.eval('OptimizeScene;')


@CommandDispatcher.register("Check Scene Name")
@decorator.undo
def checkSceneName(ui):
    mel.eval('source ' + json.dumps(base_dir + "scripts/mel/checkSceneName.mel"))


@CommandDispatcher.register("Delete Unused Nodes")
@decorator.undo
def DeleteunUsedNodes(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().deleteunUsedNodes()


@CommandDispatcher.register("Delete unknown Node")
@decorator.undo
def DeleteunknownNode_unknow(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().deleteunKnowNodes()


@CommandDispatcher.register("Delete unUsedOrig")
@decorator.undo
def DeleteunUsedOrig(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().deleteUnuseOrig()


@CommandDispatcher.register("Delete unDisplayPoint")
@decorator.undo
def DeleteunDisplayPoint(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().Clean_invalid_displayPoints()


@CommandDispatcher.register("Delete unUsedPlug")
@decorator.undo
def DeleteunUsedPlug(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().clean_unknown_plugins()


@CommandDispatcher.register("Delete unUsedDagPose")
@decorator.undo
def DeleteunUsedDagPose(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().delete_unused_dagpose_nodes()


@CommandDispatcher.register("UnLockNode Selected")
@decorator.undo
def UnLockNodeSelected(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().CleanUNLockNode(False)


@CommandDispatcher.register("UnLockNode Scene")
@decorator.undo
def unLockNodeScene(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().CleanUNLockNode(True)


@CommandDispatcher.register("UnLock initialShading")
@decorator.undo
def unLockinitialShading(ui):
    mel.eval('lockNode -l 0 -lu 0 initialShadingGroup;')


@CommandDispatcher.register("setIsHistoricallyInteresting")
@decorator.undo
def setIsHistoricallyInteresting(ui):
    __import__(
        'OptimizeSceneFun',
        fromlist=['OptimizeScene']
    ).OptimizeScene().setIsHistoricallyInteresting()


@CommandDispatcher.register("Maya Script Editor")
def charcoalEditor(ui):
    mel.eval("ScriptEditor;")
    __import__(
        'syntax_jd',
        fromlist=['wrap']
    ).wrap()


@CommandDispatcher.register("CharcoalEditor2")
def charcoalEditor2(ui):
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
            mel.eval('deleteAllIntermediates("{}");'.format(i))


@CommandDispatcher.register("Select Input Node")
@decorator.undo
def select_attr_input_node(ui):
    __import__(
        'Popumenus',
        fromlist=['GUIPopupMenu']
    ).GUIPopupMenu()._select_attr_input_node()


@CommandDispatcher.register("Combine Skinweight")
@decorator.undo
def combine_skinweight(ui):
    __import__(
        'Popumenus',
        fromlist=['GUIPopupMenu']
    ).GUIPopupMenu()._combine_skinweight()


@CommandDispatcher.register("Linked Surface")
@decorator.undo
def linked_surface(ui):
    __import__(
        'Popumenus',
        fromlist=['GUIPopupMenu']
    ).GUIPopupMenu().linked_surface()


@CommandDispatcher.register("Curve Keep Linked")
@decorator.undo
def keep_linked(ui, keep=False):
    popup = __import__(
        'Popumenus',
        fromlist=['GUIPopupMenu']
    ).GUIPopupMenu()

    if keep:
        popup.keep_linked()
    else:
        popup.run_locked()


@CommandDispatcher.register("Mirror Skin")
@decorator.undo
def mirror_skin(ui, lr=True):
    popup = __import__(
        'Popumenus',
        fromlist=['GUIPopupMenu']
    ).GUIPopupMenu()

    if lr:
        popup._mirror_skin()
    else:
        popup._open_mirror_skin_tool()


@CommandDispatcher.register("Create Joints")
@decorator.undo
def create_joint(ui):
    __import__(
        'Popumenus',
        fromlist=['GUIPopupMenu']
    ).GUIPopupMenu()._create_joint()


@CommandDispatcher.register("Joints Add Shape")
@decorator.undo
def joints_add_shape(ui):
    __import__(
        'Popumenus',
        fromlist=['GUIPopupMenu']
    ).GUIPopupMenu()._joint_add_shape()


@CommandDispatcher.register("Curve Create Joint")
@decorator.undo
def curve_create_joints(ui):
    cur = cmds.ls(sl=1)
    if not cur:
        mayaPrint.error("Please select a curve.")

    mel.eval('source "{}"'.format(
        base_dir + "scripts/mel/great_curvejoint.mel"
    ))


#---------------------------ui-------------------------------------
@CommandDispatcher.register("Attribute Edit")
def attribute_tool(ui):
    __import__(
        'ControllerTool.AttributeEditUI',
        fromlist=['AttributeEditUI']
    ).AttributeEditUI().window_creation()


@CommandDispatcher.register("OLD PY_RIGASSIT")
def py_rigassit_gui(ui):
    __import__(
        'BatchGUI',
        fromlist=['BatchGUI']
    ).BatchGUI().showWindow()


@CommandDispatcher.register("Rename")
def rename_tool(ui):
    from py_rigAssit.dialogs import rename_dialog as rename_dialog
    rename_dialog.main()


@CommandDispatcher.register("Joint Orient")
def joints_orient_tool(ui):
    __import__(
        'JointEdit.JointOrentTool',
        fromlist=['JointOrentUI']
    ).JointOrentUI().JointOrientTool()


@CommandDispatcher.register("IKFK Rigging")
def ikfk_rigging_tool(ui):
    __import__(
        'py_rigAssit.dialogs.ikfk_system_layout',
        fromlist=['main']
    ).main()


@CommandDispatcher.register("Follow World")
def follow_tool(ui):
    __import__(
        'QuickTools.follow_tool',
        fromlist=['main']
    ).main()


@CommandDispatcher.register("InsertJoints")
def InsertJoints(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "Insertjoint_selected.mel")
    mel.eval('source ' + json.dumps(mel_file) + '; pyFitResampleUI;')


@CommandDispatcher.register("Convert Drivenkeys")
def animkeys_to_drivenkeys(ui):
    __import__(
        'py_rigAssit.dialogs.convert_drivenkeys_ui',
        fromlist=['main']
    ).main()


@CommandDispatcher.register("BlendShape Exp/Imp")
def exp_imp_data_tool(ui):
    from py_rigAssit.driver_pose.exp_imp_data_ui import show_ui
    show_ui()


@CommandDispatcher.register("Curve Snape")
def snape_curve_tool(ui):
    from py_rigAssit.general_mod.snape_curve import show
    show()


@CommandDispatcher.register("Compare Groups")
def compare_groups(ui):
    from py_rigAssit.model_mod.compare_groups import show_ui
    show_ui()