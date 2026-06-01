# -*- coding: utf-8 -*-

# .FileName:commands.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/12 17:09
# .Finish time:
import json
import os
from py_rigAssit.dialogs import base_dir, decorator, mayaPrint
from py_rigAssit.common.command_dispatcher import CommandDispatcher
from JointEdit.JointEditFun import EditJnt
from JointEdit.JointOrentTool import JointOrentUI
from selectOrRemove import SelectOrremoveObj
from Utils.attr_name import PyAttrUtils
from PyUtils import PyObjectUtils
from Utils import sdk_info
from GeneralTools.AttributeSetting import SetAttrTool
import DefromConvertWeight.auto_nurbs_convert_skinWeight as auto_curve_convert_skinWeight

try:
    import numpy
    import DefromConvertWeight.wire_deltamush_tension_to_weight as defromer_convert_weight
    _num = True
except:
    _num = False

import GeneralTools.zipperRig as zipperRig
from JointEdit.CreateFolliclesFun import FolliclesTools
from ControllerTool.Addattr import AddattrFunc

import maya.cmds as cmds, maya.mel as mel, maya.OpenMaya as om

editJnt = EditJnt()
jointOrentUI = JointOrentUI()
_obj = SelectOrremoveObj()
AttrUtils = PyAttrUtils()
ObjectUtils = PyObjectUtils()
SAT = SetAttrTool()
FRT = FolliclesTools()
AddAttr = AddattrFunc()


@CommandDispatcher.register("Show Axis")
@decorator.undo
def show_axis(ui):
    editJnt.DisplayJntAxis(1)

@CommandDispatcher.register("Hide Axis")
@decorator.undo
def hide_axis(ui):
    editJnt.DisplayJntAxis(0)

@CommandDispatcher.register("Zero Axis")
@decorator.undo
def zero_axis(ui):
    editJnt.zero_jointAxisOrient()

@CommandDispatcher.register("Show Joint")
@decorator.undo
def show_joint(ui):
    editJnt.showJoints()

@CommandDispatcher.register("Hide Joint")
@decorator.undo
def hide_joint(ui):
    editJnt.hideJoints()

@CommandDispatcher.register("Quick Orient")
@decorator.undo
def quick_orient(ui):
    editJnt.OrientJnts()

@CommandDispatcher.register("World")
@decorator.undo
def obj_world(ui):
    editJnt.object_to_world()

@CommandDispatcher.register("Return")
@decorator.undo
def obj_return(ui):
    editJnt.object_to_return()

@CommandDispatcher.register("Orient")
@decorator.undo
def orient(ui):
    jointOrentUI.JointOrientTool()

@CommandDispatcher.register("Resrt Skined Pose")
@decorator.undo
def resetSelectSkinPose(ui):
    editJnt.resetSelectSkinPose()

@CommandDispatcher.register("Remove unInfluences")
@decorator.undo
def remove_sence_unusedInfluence(ui):
    editJnt.removeSkinClusterUnusedInfluence()

@CommandDispatcher.register("Select Child joints")
@decorator.undo
def selectChilds(ui):
    editJnt.selectChilds()

@CommandDispatcher.register("Select Skin joints")
@decorator.undo
def selectSkinJoint(ui):
    editJnt.selectSkinJoint()

@CommandDispatcher.register("Inherits Transform")
@decorator.undo
def setInheritsTransform(ui):
    editJnt.setInheritsTransform()

@CommandDispatcher.register("Segment Scale Compensate")
@decorator.undo
def segment_scale_compensate(ui):
    editJnt.setJointSegmentScale()

@CommandDispatcher.register("Soft to skin")
@decorator.undo
def soft_to_weight(ui):
    from JointEdit.AutomaticConversionWeightFun import AutomaticToWeightFun
    AutomaticToWeightFun().soft_To_weight()

@CommandDispatcher.register("Soft add ctrl")
@decorator.undo
def auto_ik_weight(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['QuickFunctions']).QuickFunctions().soft_create_joint()

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
    editJnt.create_copySkinWeight()

@CommandDispatcher.register("center > joint")
@decorator.undo
def center_mesh_joint(ui):
    editJnt.createobjJntorSkin()

@CommandDispatcher.register("mesh > Bind")
@decorator.undo
def create_bindSkin(ui):
    editJnt.createbindSkin(True)

@CommandDispatcher.register("point > joint")
@decorator.undo
def create_PointJoint(ui):
    editJnt.createPointJoint()

@CommandDispatcher.register("curve > joint")
@decorator.undo
def curve_create_joints(ui):
    cur = cmds.ls(sl=1)
    if len(cur) < 1:
        om.MGlobal.displayError("Please select a curve.")
        return
    mel_file = os.path.join(base_dir, "scripts", "mel", "great_curvejoint.mel")
    mel.eval('source ' + json.dumps(mel_file))

@CommandDispatcher.register("joints > curve")
@decorator.undo
def joint_for_curve(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "joint_for_curve.mel")
    mel.eval('source ' + json.dumps(mel_file))

@CommandDispatcher.register("InsertJoints")
@decorator.undo
def InsertJoints(ui):
    mel_file = os.path.join(base_dir, "scripts", "mel", "Insertjoint_selected.mel")
    mel.eval('source ' + json.dumps(mel_file) + '; pyFitResampleUI;')

@CommandDispatcher.register("To Parent")
@decorator.undo
def Toparent(ui):
    editJnt.Toparent()

@CommandDispatcher.register("Group Clearing")
@decorator.undo
def group_Clearing(ui):
    editJnt.createLocgrp()

@CommandDispatcher.register("Add Chain Loc")
@decorator.undo
def add_jointLoc_system(ui):
    editJnt.add_jointLoc_system()

@CommandDispatcher.register("snape center")
@decorator.undo
def snape_seleted_to_manip(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['QuickFunctions']).QuickFunctions().snape_seleted_to_manip()

@CommandDispatcher.register("Make Group")
@decorator.undo
def make_Group(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['MakeGroupPivot']).MakeGroupPivot().make_group_multi()

@CommandDispatcher.register("Make Global")
@decorator.undo
def group_Clearing(ui):
    __import__('GeneralTools.AttributeSetting',
               fromlist=['SetAttrTool']).SetAttrTool().add_follow_attr()

@CommandDispatcher.register("Make Pivot")
@decorator.undo
def add_jointLoc_system(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['MakeGroupPivot']).MakeGroupPivot().make_pivot()

@CommandDispatcher.register("IK Weight")
@decorator.undo
def run_wire_convert_weight(ui):
    if _num == True:
        defromer_convert_weight.run_wire_convert_weight()

@CommandDispatcher.register("Split Weight")
@decorator.undo
def run_wire_split_weight(ui):
    if _num == True:
        defromer_convert_weight.run_wire_split_weight()

@CommandDispatcher.register("DeltaMush Weight")
@decorator.undo
def run_defrom_convert_weight(ui):
    if _num == True:
        defromer_convert_weight.run_defrom_convert_weight()

@CommandDispatcher.register("Divisions Weight")
@decorator.undo
def smooth_convert_weight(ui):
    if _num == True:
        defromer_convert_weight.smooth_convert_weight()

@CommandDispatcher.register("Curve Split")
@decorator.undo
def curve_split_weight(ui, types):
    Type = types[0]
    degree = types[1]

    sels = cmds.ls(sl=1)
    if sels:
        for mesh in sels:
            mesh_shape = mesh.listRelatives(mesh, s=True)[0]
            if mesh.objectType(mesh_shape) != 'mesh':
                mayaPrint.warning(u"{} is not mesh.".format(mesh))
                continue

            skin_node = AttrUtils.get_skinClusterNode(mesh)

            if skin_node == None:
                om.MGlobal.displayWarning(u"{} is not add skin.".format(mesh))
                continue

            skin_joints_list = cmds.skinCluster(skin_node, q=True, inf=True)
            if Type == 1:
                curve = ObjectUtils.createCurveforObj(skin_joints_list)
                auto_curve_convert_skinWeight.main(skin_joints_list, curve, mesh, degree)

            else:
                curve = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=len(skin_joints_list), ch=0,name="temp_cur")[0]

                jnt = skin_joints_list[1::]
                jnt.append(skin_joints_list[0])

                for i, c in zip(skin_joints_list, cmds.ls("{}.cv[0:]".format(curve), fl=1)):
                    pos = cmds.xform(i, query=1, a=1, translation=1, worldSpace=1)
                    cmds.xform(c, t=pos)

                auto_curve_convert_skinWeight.main(jnt, curve, mesh, degree)

            cmds.delete(curve)

            om.MGlobal.displayInfo(u"{} is complete.".format(mesh))

@CommandDispatcher.register("Menu Select All")
@decorator.undo
def select_all_menu(ui, LIST):
    objs = _obj.get_list_widget_items(LIST)
    cmds.select(objs, r=True)

@CommandDispatcher.register("Attr Store")
@decorator.undo
def store_attr(ui):
    SAT.ApplyStore()

@CommandDispatcher.register("Attr Return")
@decorator.undo
def return_attr(ui):
    SAT.setReturnStoreValue()

@CommandDispatcher.register("Copy Attr")
@decorator.undo
def copy_attributes(ui):
    __import__('GeneralTools.AttributeSetting',
               fromlist=['SetAttrTool']).SetAttrTool().copy_attrs()

@CommandDispatcher.register("Shift Up")
@decorator.undo
def arrt_shif_up(ui):
    SAT.apply_MoveAttr(False)

@CommandDispatcher.register("Shift Down")
@decorator.undo
def arrt_shif_dn(ui):
    SAT.apply_MoveAttr(True)

@CommandDispatcher.register("Lock/Hide Ctrls Vis")
@decorator.undo
def lock_hide_vis(ui):
    SAT.ctrls_lock_hide()

@CommandDispatcher.register("Move value")
@decorator.undo
def ctrl_move_drv(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['QuickFunctions']).QuickFunctions().ctrlValueMoveDrv()

@CommandDispatcher.register("Fip Shape")
@decorator.undo
def fip_shapes(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['QuickFunctions']).QuickFunctions().mirror_targets()

@CommandDispatcher.register("Correct Shape")
@decorator.undo
def correct_shape(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['QuickFunctions']).QuickFunctions().correctshape()

@CommandDispatcher.register("Split Shape")
@decorator.undo
def split_shape(ui):
    __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().split_target()

@CommandDispatcher.register("Move local")
@decorator.undo
def shape_move_to_local(ui):
    __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().moveVertexTo('local')

@CommandDispatcher.register("Move world")
@decorator.undo
def shape_move_to_world(ui):
    __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().moveVertexTo('world')

@CommandDispatcher.register("UV move Shape")
@decorator.undo
def uv_move_shape(ui):
    __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().mesh_UV_transfer()

@CommandDispatcher.register("Copy BS Targets")
@decorator.undo
def copy_bs_targets(ui):
    __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().copyDeformObjs()

@CommandDispatcher.register("Export Mesh Data")
@decorator.undo
def uv_move_shape(ui, is_uv):
    __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().export_selected(is_uv)

@CommandDispatcher.register("Import Mesh Data")
@decorator.undo
def copy_bs_targets(ui):
    __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().import_from_file()

@CommandDispatcher.register("Remove Double")
@decorator.undo
def remove_DoubleSkin(ui):
    __import__('JointEdit.JointEditFun',
               fromlist=['EditJnt']).EditJnt().remove_DoubleSkin()

@CommandDispatcher.register("Rename SkinNode")
@decorator.undo
def rename_skinCluster_name(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['QuickFunctions']).QuickFunctions().renameSkinCluster()

@CommandDispatcher.register("Rename BsNode")
@decorator.undo
def rename_blendShape_name(ui):
    __import__('QuickTools.QuickFunction',
               fromlist=['QuickFunctions']).QuickFunctions().renameBlendShape()



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
    sdk_info.store_sdk_info()

@CommandDispatcher.register("Import SDK")
@decorator.undo
def import_curve_data(ui):
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
def zipper_rig(ui,datas):
    Joint_M, Joint_Left, Joint_Right, Name, zipper, mode_Exp= datas["Joint_Middle"], datas["Joint_Left"], datas["Joint_Right"], datas["Name"], datas["zipper"], datas["mode_Exp"]
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
        TypeALL = "{},{}".format(rig_block, constrain_block)
        mel_cmd = 'source ' + json.dumps( base_dir + "scripts/mel/RivetandFollicle_Func.mel") + ";CreateobjFollicles(" + TypeALL + ");"
        print(mel_cmd)
        mel.eval(mel_cmd)
        mayaPrint.log("Follice constrain successfully.")
    elif rivet_cons == 2:
        TypeALL = "{},{},{}".format(rig_block, constrain_block, str(1))
        mel_cmd = 'source ' + json.dumps(
            base_dir + "scripts/mel/RivetandFollicle_Func.mel") + ";CreateRivet(" + TypeALL + ");"
        print(mel_cmd)
        mel.eval(mel_cmd)
        mayaPrint.log("Rivets constrain successfully.")
    else:
        import GeneralTools.point_skinWeight_constrant as pointsc
        pointsc.create_point_skin_constrant()

    return True

@CommandDispatcher.register("create separator")
@decorator.undo
def create_separator(ui, name):

    objs = cmds.ls(sl=1)
    if not objs:
        mayaPrint.warning(u"没有选中的对象")
    for obj in objs:
        if not cmds.listAttr(obj, m=True, st='{}Sep'.format(name)):
            AddAttr.addAttribute(objects=[obj], longName=['{}Sep'.format(name)], niceName=['________________'], at="enum",
                                  en=name,
                                  lock=True, k=True)

@CommandDispatcher.register("create attrs")
@decorator.undo
def create_attrs(ui, datas):

    attr_id =datas["attr_id"]
    names_str = datas["names_str"]
    min_value = datas["min_value"]
    max_value = datas["max_value"]
    def_value = datas["def_value"]
    proxy = datas["proxy"]

    if len(names_str) == 0:
        mayaPrint.warning('write at least one name !')

    names = names_str.split(" ")

    selection = cmds.ls(sl=True)

    for object in selection:
        if attr_id == 1:
            Attrname = names[0]
            enumname_list = []
            strenum = ''
            for name in names[1:]:
                if len(name) == 0:
                    continue
                enumname_list.append(name)
            for i in enumname_list:
                strenum += i+":"

            print (strenum)
            AddAttr.create_enumAttr(object,Attrname,strenum, usedAsProxy=proxy)
        else:
            for name in names:
                if len(name) == 0:
                    continue

                else:
                    if attr_id == 2:
                        AddAttr.create_floatAttr(object, name, min_value, max_value, def_value, usedAsProxy=proxy)

                    elif attr_id == 3:
                        AddAttr.create_intAttr(object, name, min_value, max_value, def_value, usedAsProxy=proxy)

                    elif attr_id == 4:
                        AddAttr.create_boolAttr(object, name, usedAsProxy=proxy)

                    elif attr_id == 5:
                        AddAttr.create_stringAttr(object, name)


            mayaPrint.log("Custom attribute {} has been added to selected objects.".format(names))

@CommandDispatcher.register("apply attr vis lock")
@decorator.undo
def apply_attr_vis_lock(ui, datas):
    t_key = datas["t_info"][0]
    t_lock = datas["t_info"][1]
    r_key =  datas["r_info"][0]
    r_lock =  datas["r_info"][1]
    s_key =  datas["s_info"][0]
    s_lock =  datas["s_info"][1]
    v_key =  datas["v_info"][0]
    v_lock =  datas["v_info"][1]

    objs = cmds.ls(selection=True)
    if not objs:
        mayaPrint.error(">>> Please select object(s) !")
        return
    attrs = [
        ('t', t_key, t_lock, 'xyz'),
        ('r', r_key, r_lock, 'xyz'),
        ('s', s_key, s_lock, 'xyz'),
        ('v', v_key, v_lock, '')  # 无轴
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


#=================================================================================
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
        om.MGlobal.displayWarning("This version is not available.")

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

