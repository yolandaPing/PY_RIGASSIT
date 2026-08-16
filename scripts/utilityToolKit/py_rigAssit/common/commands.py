# -*- coding: utf-8 -*-

# .FileName:commands.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/12 17:09
# .Finish time:

import json
import os
import maya.cmds as cmds
import maya.mel as mel

from py_rigAssit.dialogs import base_dir, decorator, mayaPrint
from py_rigAssit.common.command_dispatcher import CommandDispatcher

# lazy helpers
_RecordLocation = __import__(
    'JointEdit.JointEditFun',
    fromlist=['RecordLocation']
).RecordLocation()

def _edit_jnt():
    return __import__('JointEdit.JointEditFun', fromlist=['EditJnt']).EditJnt()

def _quick_functions():
    return __import__('QuickTools.QuickFunction', fromlist=['QuickFunctions']).QuickFunctions()

def _make_group_pivot():
    return __import__('QuickTools.QuickFunction', fromlist=['MakeGroupPivot']).MakeGroupPivot()

def _set_attr_tool():
    return __import__('GeneralTools.AttributeSetting', fromlist=['SetAttrTool']).SetAttrTool()

def _mesh_edit():
    return __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit()

def _add_attr():
    return __import__('ControllerTool.Addattr', fromlist=['AddattrFunc']).AddattrFunc()


@CommandDispatcher.register("Show Axis")
@decorator.undo
def show_axis(ui):
    _edit_jnt().DisplayJntAxis(1)


@CommandDispatcher.register("Hide Axis")
@decorator.undo
def hide_axis(ui):
    _edit_jnt().DisplayJntAxis(0)


@CommandDispatcher.register("Zero Axis")
@decorator.undo
def zero_axis(ui):
    _edit_jnt().zero_jointAxisOrient()


@CommandDispatcher.register("Show Joint")
@decorator.undo
def show_joint(ui):
    _edit_jnt().showJoints()


@CommandDispatcher.register("Hide Joint")
@decorator.undo
def hide_joint(ui):
    _edit_jnt().hideJoints()


@CommandDispatcher.register("Quick Orient")
@decorator.undo
def quick_orient(ui):
    _edit_jnt().OrientJnts()


@CommandDispatcher.register("World")
@decorator.undo
def obj_world(ui):
    _RecordLocation.object_to_world()


@CommandDispatcher.register("Return")
@decorator.undo
def obj_return(ui):
    _RecordLocation.object_to_return()


@CommandDispatcher.register("Orient")
@decorator.undo
def orient(ui):
    from JointEdit.JointOrentTool import JointOrentUI
    jointOrentUI = JointOrentUI()
    jointOrentUI.JointOrientTool()


@CommandDispatcher.register("Resrt Skined Pose")
@decorator.undo
def resetSelectSkinPose(ui):
    _edit_jnt().resetSelectSkinPose()


@CommandDispatcher.register("Remove unInfluences")
@decorator.undo
def remove_sence_unusedInfluence(ui):
    _edit_jnt().removeSkinClusterUnusedInfluence()


@CommandDispatcher.register("Select Child joints")
@decorator.undo
def selectChilds(ui):
    _edit_jnt().selectChilds()


@CommandDispatcher.register("Select Skin joints")
@decorator.undo
def selectSkinJoint(ui):
    _edit_jnt().selectSkinJoint()


@CommandDispatcher.register("Inherits Transform")
@decorator.undo
def setInheritsTransform(ui):
    _edit_jnt().setInheritsTransform()


@CommandDispatcher.register("Segment Scale Compensate")
@decorator.undo
def segment_scale_compensate(ui):
    _edit_jnt().setJointSegmentScale()


@CommandDispatcher.register("Split skin")
@decorator.undo
def split_skin_ui(ui):
    from py_rigAssit.dialogs import split_skin_dlg as split_skin_dlg
    split_skin_dlg.main()


@CommandDispatcher.register("Tubes pro")
@decorator.undo
def tubes_create_joints(ui):
    from py_rigAssit.dialogs import curves_from_tubesPro as curves_from_tubes
    curves_from_tubes.show()


@CommandDispatcher.register("Soft add ctrl")
@decorator.undo
def soft_add_ctrl(ui):
    _quick_functions().soft_create_joint()


@CommandDispatcher.register("Auto IK Weight")
@decorator.undo
def auto_ik_weight(ui):
    from JointEdit.AutomaticConversionWeightFun import AutomaticToWeightFun
    meshs = cmds.ls(sl=1)
    if meshs:
        AutomaticToWeightFun().ApplyWireToWeight()


@CommandDispatcher.register("Copy Skin")
@decorator.undo
def copy_skin(ui):
    _edit_jnt().create_copySkinWeight()


@CommandDispatcher.register("center > joint")
@decorator.undo
def center_mesh_joint(ui):
    _edit_jnt().createobjJntorSkin()


@CommandDispatcher.register("mesh > Bind")
@decorator.undo
def create_bindSkin(ui):
    _edit_jnt().createbindSkin(True)


@CommandDispatcher.register("point > joint")
@decorator.undo
def create_PointJoint(ui):
    _edit_jnt().createPointJoint()


@CommandDispatcher.register("curve > joint")
@decorator.undo
def curve_create_joints(ui):
    cur = cmds.ls(sl=1)
    if len(cur) < 1:
        mayaPrint.error("Please select a curve.")
        return
    mel_file = os.path.join(base_dir, "scripts", "mel", "great_curvejoint.mel")
    mel.eval('source ' + json.dumps(mel_file))


@CommandDispatcher.register("joints > curve")
@decorator.undo
def joint_for_curve(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "joint_for_curve.mel")
    mel.eval('source ' + json.dumps(mel_file))


@CommandDispatcher.register("InsertJoints")
def InsertJoints(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "Insertjoint_selected.mel")
    mel.eval('source ' + json.dumps(mel_file) + '; pyFitResampleUI;')


@CommandDispatcher.register("To Parent")
@decorator.undo
def Toparent(ui):
    _edit_jnt().Toparent()


@CommandDispatcher.register("Group Clearing")
@decorator.undo
def group_Clearing(ui):
    _edit_jnt().createLocgrp()


@CommandDispatcher.register("Add Chain Loc")
@decorator.undo
def add_jointLoc_system(ui):
    _edit_jnt().add_jointLoc_system()


@CommandDispatcher.register("snape center")
@decorator.undo
def snape_seleted_to_manip(ui):
    _quick_functions().snape_seleted_to_manip()


@CommandDispatcher.register("Make Group")
@decorator.undo
def make_Group(ui):
    _make_group_pivot().make_group_multi()


@CommandDispatcher.register("Make Global")
@decorator.undo
def group_Clearing(ui):
    _set_attr_tool().add_follow_attr()


@CommandDispatcher.register("Make Pivot")
@decorator.undo
def add_jointLoc_system(ui):
    _make_group_pivot().make_pivot()


@CommandDispatcher.register("IK Weight")
@decorator.undo
def run_wire_convert_weight(ui):
    try:
        import numpy
        import DefromConvertWeight.wire_deltamush_tension_to_weight as defromer_convert_weight
        defromer_convert_weight.run_wire_convert_weight()
    except ImportError as e:
        mayaPrint.warning(
            "Import failed: {}".format(e)
        )


@CommandDispatcher.register("Split Weight")
@decorator.undo
def run_wire_split_weight(ui):
    try:
        import numpy
        import DefromConvertWeight.wire_deltamush_tension_to_weight as defromer_convert_weight
        defromer_convert_weight.run_wire_split_weight()
    except ImportError as e:
        mayaPrint.warning(
            "Import failed: {}".format(e)
        )


@CommandDispatcher.register("DeltaMush Weight")
@decorator.undo
def run_defrom_convert_weight(ui):
    try:
        import numpy
        import DefromConvertWeight.wire_deltamush_tension_to_weight as defromer_convert_weight
        defromer_convert_weight.run_defrom_convert_weight()
    except ImportError as e:
        mayaPrint.warning(
            "Import failed: {}".format(e)
        )


@CommandDispatcher.register("Divisions Weight")
@decorator.undo
def smooth_convert_weight(ui):
    try:
        import numpy
        import DefromConvertWeight.wire_deltamush_tension_to_weight as defromer_convert_weight
        defromer_convert_weight.smooth_convert_weight()
    except ImportError as e:
        mayaPrint.warning(
            "Import failed: {}".format(e)
        )


@CommandDispatcher.register("Curve Split")
@decorator.undo
def curve_split_weight(ui, types):
    from Utils.attr_name import PyAttrUtils
    from PyUtils import PyObjectUtils
    import DefromConvertWeight.auto_nurbs_convert_skinWeight as auto_curve_convert_skinWeight

    AttrUtils = PyAttrUtils()
    ObjectUtils = PyObjectUtils()

    Type = types[0]
    degree = types[1]

    sels = cmds.ls(sl=1)
    if sels:
        for mesh in sels:
            mesh_shape = cmds.listRelatives(mesh, s=True)[0]
            if cmds.objectType(mesh_shape) != 'mesh':
                mayaPrint.warning(u"{} is not mesh.".format(mesh))
                continue

            skin_node = AttrUtils.get_skinClusterNode(mesh)

            if skin_node is None:
                mayaPrint.warning(u"{} is not add skin.".format(mesh))
                continue

            skin_joints_list = cmds.skinCluster(skin_node, q=True, inf=True)
            if Type == 1:
                curve = ObjectUtils.createCurveforObj(skin_joints_list)
                auto_curve_convert_skinWeight.main(skin_joints_list, curve, mesh, degree)
            else:
                curve = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=len(skin_joints_list), ch=0, name="temp_cur")[0]
                jnt = skin_joints_list[1::]
                jnt.append(skin_joints_list[0])
                for i, c in zip(skin_joints_list, cmds.ls("{}.cv[0:]".format(curve), fl=1)):
                    pos = cmds.xform(i, query=1, a=1, translation=1, worldSpace=1)
                    cmds.xform(c, t=pos)
                auto_curve_convert_skinWeight.main(jnt, curve, mesh, degree)

            cmds.delete(curve)
            mayaPrint.log(u"{} is complete.".format(mesh))


@CommandDispatcher.register("Menu Select All")
@decorator.undo
def select_all_menu(ui, LIST):
    from selectOrRemove import SelectOrremoveObj
    _obj = SelectOrremoveObj()
    objs = _obj.get_list_widget_items(LIST)
    cmds.select(objs, r=True)


@CommandDispatcher.register("Attr Store")
@decorator.undo
def store_attr(ui):
    _set_attr_tool().ApplyStore()


@CommandDispatcher.register("Attr Return")
@decorator.undo
def return_attr(ui):
    _set_attr_tool().setReturnStoreValue()


@CommandDispatcher.register("Copy Attr")
@decorator.undo
def copy_attributes(ui):
    _set_attr_tool().copy_attrs()


@CommandDispatcher.register("Shift Up")
@decorator.undo
def arrt_shif_up(ui):
    _set_attr_tool().apply_MoveAttr(False)


@CommandDispatcher.register("Shift Down")
@decorator.undo
def arrt_shif_dn(ui):
    _set_attr_tool().apply_MoveAttr(True)


@CommandDispatcher.register("Lock/Hide Ctrls Vis")
@decorator.undo
def lock_hide_vis(ui):
    _set_attr_tool().ctrls_lock_hide()


@CommandDispatcher.register("Move value")
@decorator.undo
def ctrl_move_drv(ui):
    _quick_functions().ctrlValueMoveDrv()


@CommandDispatcher.register("Fip Shape")
@decorator.undo
def fip_shapes(ui):
    _quick_functions().mirror_targets()


@CommandDispatcher.register("Correct Shape")
@decorator.undo
def correct_shape(ui):
    _quick_functions().correctshape()


@CommandDispatcher.register("Split Shape")
@decorator.undo
def split_shape(ui):
    _mesh_edit().split_target()


@CommandDispatcher.register("Move local")
@decorator.undo
def shape_move_to_local(ui):
    _mesh_edit().moveVertexTo('local')


@CommandDispatcher.register("Move world")
@decorator.undo
def shape_move_to_world(ui):
    _mesh_edit().moveVertexTo('world')


@CommandDispatcher.register("UV move Shape")
@decorator.undo
def uv_move_shape(ui):
    _mesh_edit().mesh_UV_transfer()


@CommandDispatcher.register("Copy BS Targets")
@decorator.undo
def copy_bs_targets(ui):
    _mesh_edit().copyDeformObjs()


@CommandDispatcher.register("Export Mesh Data")
@decorator.undo
def uv_move_shape(ui, is_uv):
    _mesh_edit().export_selected(is_uv)


@CommandDispatcher.register("Import Mesh Data")
@decorator.undo
def copy_bs_targets(ui):
    _mesh_edit().import_from_file()

@CommandDispatcher.register("Create Cut Plan")
@decorator.undo
def createCutPlane(ui):
    global cut_obj_plan
    cut_obj_plan = cmds.ls(sl=True)
    mel_cmd = 'source ' + json.dumps(
        base_dir + "scripts/mel/cutTool.mel") + ";js_cutPlane_create();"
    if cut_obj_plan:
        mel.eval(mel_cmd)

@CommandDispatcher.register("Cut Mesh")
@decorator.undo
def cutPlane(ui):
    global cut_obj_plan
    mel_cmd = 'source ' + json.dumps(
        base_dir + "scripts/mel/cutTool.mel") + ";js_cutPlane_cut (1);"
    if cut_obj_plan:
        mel.eval(mel_cmd)
        cut_obj_plan = None
        mayaPrint.log('Cutting successfully.')


@CommandDispatcher.register("Remove Double")
@decorator.undo
def remove_DoubleSkin(ui):
    from JointEdit.JointEditFun import EditJnt
    EditJnt().remove_DoubleSkin()


@CommandDispatcher.register("Rename SkinNode")
@decorator.undo
def rename_skinCluster_name(ui):
    _quick_functions().renameSkinCluster()


@CommandDispatcher.register("Rename BsNode")
@decorator.undo
def rename_blendShape_name(ui):
    _quick_functions().renameBlendShape()


@CommandDispatcher.register("Export curve")
def export_curve_data(ui):
    __import__('QuickTools.object_postion_info',
               fromlist=['curve_vetx_save']).curve_vetx_save()


@CommandDispatcher.register("Import curve")
@decorator.undo
def import_curve_data(ui):
    __import__('QuickTools.object_postion_info',
               fromlist=['load_curve_info']).load_curve_info()


@CommandDispatcher.register("Export Pos")
def export_Position(ui):
    __import__('QuickTools.object_postion_info',
               fromlist=['objects_position_save']).objects_position_save()


@CommandDispatcher.register("Import Pos")
@decorator.undo
def import_Position(ui):
    __import__('QuickTools.object_postion_info',
               fromlist=['load_objects_position']).load_objects_position()


@CommandDispatcher.register("Export SDK")
def export_SDK_Info(ui):
    from Utils import sdk_info
    sdk_info.store_sdk_info()


@CommandDispatcher.register("Import SDK")
@decorator.undo
def import_curve_data(ui):
    from Utils import sdk_info
    sdk_info.import_sdk_data()


@CommandDispatcher.register("Global ctrl")
@decorator.undo
def global_ctrl(ui):
    from GeneralTools.ControllerVisFun import ControllerVisTool
    ControllerVisTool().createGlobalCtrl()


@CommandDispatcher.register("Create visibility")
@decorator.undo
def create_visibility(ui):
    from QuickTools.QuickFunction import MakeGroupPivot
    MakeGroupPivot().addVisNameCtrl()


@CommandDispatcher.register("Connect Mesh")
@decorator.undo
def connect_mesh(ui):
    from QuickTools.QuickFunction import QuickFunctions
    QuickFunctions().connectMeshDisplay()


@CommandDispatcher.register("zipper Rig")
@decorator.undo
def zipper_rig(ui, datas):
    import GeneralTools.zipperRig as zipperRig
    Joint_M, Joint_Left, Joint_Right, Name, zipper, mode_Exp = datas["Joint_Middle"], datas["Joint_Left"], datas["Joint_Right"], datas["Name"], datas["zipper"], datas["mode_Exp"]
    axial = datas["axial"]
    ctrlType = datas["ctrlType"]
    ctrlCount = datas["ctrlCount"]
    GlobalScale = datas["Root"]
    scale_attr = {1: ".sx", 2: ".sy", 3: ".sz"}

    con_list_M, con_list_L, con_list_R = zipperRig.zipper_rig(Joint_M, Joint_Left,
                                                              Joint_Right, Name, zipper,
                                                              mode_Exp, GlobalScale)

    if not GlobalScale:
        GlobalScale = cmds.createNode("transform", n="global_scale", parent="notMove")

    if con_list_M and not cmds.objExists("{}_spRig_grp".format(con_list_M[0])):
        zipperRig.spineIK_rig([con_list_M[0]], GlobalScale, ctrlCount, ctrlType, scale_attr[axial])

    for dr, dn in zip([con_list_L, con_list_R], [Joint_Left, Joint_Right]):
        if dr and not cmds.objExists("{}_spRig_grp".format(dr[0])):
            zipperRig.spineIK_rig([dr[0]], GlobalScale, ctrlCount, ctrlType, scale_attr[axial])

        if dn:
            cmds.select(dn, hi=True)
            dns = cmds.ls(sl=True, type="joint")
            for ii in range(len(dns)):
                cmds.scaleConstraint(dr[ii], dns[ii], mo=1)

    try:
        cmds.hide("ZIP_RigSystem_grp")
    except:
        pass

    return True


@CommandDispatcher.register("ribbon rig build")
@decorator.undo
def ribbon_rig_build(ui, datas):
    from JointEdit.CreateFolliclesFun import FolliclesTools
    FRT = FolliclesTools()
    cons = datas["cons"]
    if FRT.ribbon_rigging(datas["name_filed"], datas["joint_filed"], datas["rig_block"], datas["direction_block"], cons, datas["animation_block"], datas["ctrl_block"], datas["ctrl_count"]):
        if cons == 1:
            mayaPrint.log(' Rivets Ribbon Nurbs successfully !')
        else:
            mayaPrint.log(' Follice Ribbon Nurbs successfully !')


@CommandDispatcher.register("follicle rivet Rig")
@decorator.undo
def follicle_rivet_constrain(ui, datas):
    rivet_cons = datas["cons_block"]
    rig_block = datas["rig_block"]
    constrain_block = datas["constrain_block"]

    if rivet_cons == 1:
        run_ages = "{},{}".format(rig_block, constrain_block)
        mel_cmd = 'source ' + json.dumps(base_dir + "scripts/mel/RivetandFollicle_Func.mel") + ";CreateobjFollicles(" + run_ages + ");"
        mel.eval(mel_cmd)
        mayaPrint.log("Follice constrain successfully.")
    elif rivet_cons == 2:
        run_ages = "{},{},{}".format(rig_block, constrain_block, str(1))
        mel_cmd = 'source ' + json.dumps(base_dir + "scripts/mel/RivetandFollicle_Func.mel") + ";CreateRivet(" + run_ages + ");"
        mel.eval(mel_cmd)
        mayaPrint.log("Rivets constrain successfully.")
    elif rivet_cons == 3:
        import GeneralTools.uv_pin as uv_pin
        sels = cmds.ls(sl=True)

        if len(sels) < 2:
            mayaPrint.warning("Select objects then Mesh/Surface.")
            return
        objs = sels[:-1]
        driver = sels[-1]
        uv_pin.apply_uvPin(objs=objs, driver=driver, cons_type=rig_block, cons=constrain_block)
    else:
        import GeneralTools.point_skinWeight_constrant as pointsc
        pointsc.create_point_skin_constrant()

    return True


@CommandDispatcher.register("mirror constraints")
@decorator.undo
def mirror_constraints(ui, datas):

    mapping = datas["mapping"]
    replace_type = datas["replace_type"]

    selected = cmds.ls(sl=True)

    if not selected:
        cmds.warning("Please select constraint nodes.")
        return

    import ConstrainEdit.mirror_constraints as mirror_con
    mirror_con.mirror_constraints(selected, mapping, replace_type)
    mayaPrint.log('constraint mirror successfully!')


@CommandDispatcher.register("create separator")
@decorator.undo
def create_separator(ui, name):
    AddAttr = _add_attr()
    objs = cmds.ls(sl=1)
    if not objs:
        mayaPrint.warning(u"没有选中的对象")
    for obj in objs:
        if not cmds.listAttr(obj, m=True, st='{}Sep'.format(name)):
            AddAttr.addAttribute(objects=[obj], longName=['{}Sep'.format(name)], niceName=['________________'], at="enum",
                                 en=name, lock=True, k=True)


@CommandDispatcher.register("create attrs")
@decorator.undo
def create_attrs(ui, datas):
    AddAttr = _add_attr()
    attr_id = datas["attr_id"]
    names_str = datas["names_str"]
    min_value = datas["min_value"]
    max_value = datas["max_value"]
    def_value = datas["def_value"]
    proxy = datas["proxy"]

    if len(names_str) == 0:
        mayaPrint.warning('write at least one name !')

    names = names_str.split(" ")
    selection = cmds.ls(sl=True)

    for obj in selection:
        if attr_id == 1:
            Attrname = names[0]
            enumname_list = []
            strenum = ''
            for name in names[1:]:
                if len(name) == 0:
                    continue
                enumname_list.append(name)
            for i in enumname_list:
                strenum += i + ":"
            AddAttr.create_enumAttr(obj, Attrname, strenum, usedAsProxy=proxy)
        else:
            for name in names:
                if len(name) == 0:
                    continue
                else:
                    if attr_id == 2:
                        AddAttr.create_floatAttr(obj, name, min_value, max_value, def_value, usedAsProxy=proxy)
                    elif attr_id == 3:
                        AddAttr.create_intAttr(obj, name, min_value, max_value, def_value, usedAsProxy=proxy)
                    elif attr_id == 4:
                        AddAttr.create_boolAttr(obj, name, usedAsProxy=proxy)
                    elif attr_id == 5:
                        AddAttr.create_stringAttr(obj, name)

    mayaPrint.log("Custom attribute {} has been added to selected objects.".format(names))


@CommandDispatcher.register("apply attr vis lock")
@decorator.undo
def apply_attr_vis_lock(ui, datas):
    t_key = datas["t_info"][0]
    t_lock = datas["t_info"][1]
    r_key = datas["r_info"][0]
    r_lock = datas["r_info"][1]
    s_key = datas["s_info"][0]
    s_lock = datas["s_info"][1]
    v_key = datas["v_info"][0]
    v_lock = datas["v_info"][1]

    objs = cmds.ls(selection=True)
    if not objs:
        mayaPrint.error(">>> Please select object(s) !")
        return
    attrs = [
        ('t', t_key, t_lock, 'xyz'),
        ('r', r_key, r_lock, 'xyz'),
        ('s', s_key, s_lock, 'xyz'),
        ('v', v_key, v_lock, '')
    ]
    for obj in objs:
        if cmds.nodeType(obj) in ('joint', 'transform', 'ikHandle'):
            for attr, key, lock, axes in attrs:
                if axes:
                    for axis in axes:
                        cmds.setAttr("{}.{}{}".format(obj, attr, axis), keyable=key, lock=lock)
                else:
                    cmds.setAttr("{}.{}".format(obj, attr), keyable=key, lock=lock)
    mayaPrint.log("Applied attribute changes to {} object(s).".format(len(objs)))

@CommandDispatcher.register("Vector Driver System")
@decorator.undo
def vector_driver_system(ui, info):
    try:
        from ConstrainEdit.vector_system import create_angle_system
        create_angle_system(info[0], info[1], info[2], mapping=info[3], replace_type=info[4])
    except Exception as e:
        mayaPrint.warning(e)

# ========== 以下为独立的外部工具导入 ==========
@CommandDispatcher.register("QuadRemesher")
def QuadRemesher(ui):
    try:
        import ArtistTools.QuadRemesher.QuadRemesher_ch as QuadRemesher
        QuadRemesher.QuadRemesher()
    except:
        mayaPrint.warning("Higher versions are not supported at the moment.")


@CommandDispatcher.register("intersecSolver")
def intersectionSolver(ui):
    import ArtistTools.intersectionSolver as intersectionSolver
    intersectionSolver.intersectionSolver()


@CommandDispatcher.register("muscleTool")
def muscleTool(ui):
    import ArtistTools.muscleTool as muscleTool
    muscleTool.muscleTool()


@CommandDispatcher.register("CopySDK")
def CopySDK(ui):
    from CopyEdit import copySDK as copySDK
    copySDK.runUI()


@CommandDispatcher.register("UKDPEyelidRig")
def UKDP_EyelidRig(ui):
    from ArtistTools.UKDP_AE_eyelid import AER
    AER().UI()


@CommandDispatcher.register("EyelidRig")
def EyelidRig(ui):
    import ArtistTools.eyeLidSetupTool as eyeLidSetupTool
    eyeLidSetupTool.mayaRun()


@CommandDispatcher.register("CurveFromTubes")
def Curve_From_Tubes(ui):
    if (int(cmds.about(version=True))) < 2023:
        import ArtistTools.CurvesFromTubes as CTFT
        CTFT.showWindow()
    else:
        mayaPrint.warning("This version is not available.")


@CommandDispatcher.register("Curve_Rigger")
def Curve_Rigger(ui):
    import ArtistTools.Curve_Rigger.RigNet_RUN as RigNet_Curve_RiggerLaunch
    RigNet_Curve_RiggerLaunch.run()


@CommandDispatcher.register("Ribbon_Nacho")
def Ribbon_Nacho(ui):
    from ArtistTools.Ribbon_Nacho import Ribbon_NachoUI as Ribbon_NachoUI
    Ribbon_NachoUI.UI()


@CommandDispatcher.register("Create Ctrls")
def create_ctrls(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "createFKctrls.mel")
    mel.eval('source ' + json.dumps(mel_file))


@CommandDispatcher.register("abSymMesh")
def abSymMesh(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "abSymMesh.mel")
    mel.eval('source ' + json.dumps(mel_file))


@CommandDispatcher.register("Quick rename")
def quick_rename(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "Quick_rename_tool.mel")
    mel.eval('source ' + json.dumps(mel_file))

