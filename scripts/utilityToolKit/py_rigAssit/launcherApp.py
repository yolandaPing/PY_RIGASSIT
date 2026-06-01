# -*- coding: utf-8 -*-

# .FileName:launcherApp.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2025/7/24 22:35
# .Finish time:
# launcherApp_lazy.py
from QuickTools.QuickFunction import QuickFunctions
import saveRootPath as Root
from Utils import sdk_info
import Utils.Decorator as _decorator

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om


path = Root.ParentPath
user_path = path.replace("\\", "/")
Quick = QuickFunctions()

# ===================== UI / tool函数封装 =====================

def run_mel_tool(tool_path, command):
    mel.eval('source "{}{}"; {}'.format(user_path, tool_path, command))


def Joint_orent():
    from JointEdit.JointOrentTool import JointOrentUI
    JointOrentUI().JointOrientTool()


def separate_Head():
    run_mel_tool("scripts/mel/separate_Head.mel", "separateHeadUI")


def Insertjoint_selected():
    run_mel_tool("scripts/mel/Insertjoint_selected.mel", "pyFitResampleUI")


def combine_SDK_Dirve():
    try:
        from ConstrainEdit.combine_SDK_Tool import Combine_SDK_UI
        combine_SDK = Combine_SDK_UI()
        combine_SDK.showWindow()
    except:
        raise Exception(u"请先安装 PY_RIGASSIT 工具箱!")


def skinner():
    import skinner.window as skinWin
    skinWin.App()


def animat_data_tool():
    try:
        import ani_data_tool
        ani_data_tool.main()
    except:
        om.MGlobal.displayWarning(u"此工具未加载进box")


def Arrt_shif_up():
    from GeneralTools.AttributeSetting import SetAttrTool
    SetAttrTool().apply_MoveAttr(False)


def Arrt_shif_dn():
    from GeneralTools.AttributeSetting import SetAttrTool
    SetAttrTool().apply_MoveAttr(True)


# ============== command (用于按钮绑定) ===================

@_decorator.undo
def Mirror_ctrl():
    from ControllerTool.CurveEdit import CurvesEdit
    CurvesEdit().mirror_ctrl()


@_decorator.undo
def Master_ctrl():
    from GeneralTools.ControllerVisFun import ControllerVisTool
    ControllerVisTool().createGlobalCtrl()


@_decorator.undo
def Vis_ctrl():
    from QuickTools.QuickFunction import MakeGroupPivot
    MakeGroupPivot().addVisNameCtrl()


@_decorator.undo
def Connect_mesh():
    from QuickTools.QuickFunction import QuickFunctions
    QuickFunctions().connectMeshDisplay()


# ===================== 图标配置区 =====================

tool_info = {
    'Joint_orent.png': Joint_orent,
    'Joints_Chain_IKFK.png': lambda: __import__('ControllerTool.Joint_Chain_IKFK_System', fromlist=['main']).main(),
    'IKFK_complex_system.png': lambda: __import__('ControllerTool.IKFK_Ribbon_System', fromlist=['main']).main(),
    'Target_Correct.png': lambda: __import__('GeneralTools.blendshape_target_Correct', fromlist=['mian']).mian(),
    'Mirror_SDK.png': lambda: __import__('ConstrainEdit.mirror_copy_sdk', fromlist=['main']).main(),
    'separate_Head.png': separate_Head,
    'combine_SDK.png': lambda: __import__('py_rigAssit.general_mod.combine_sdk_ui', fromlist=['main']).main(),
    'skinner.png': skinner,
    'animat_tool.png': animat_data_tool,
    'Deform_Weight_Edit.png': lambda: __import__('py_rigAssit.deform_edit.copy_deform_weight', fromlist=['main']).main(),
    'Double_FK_tool.png': lambda: __import__('JointEdit.ForwardReverseFKUI', fromlist=['main']).main(),
    'Dynamic_curve_rig.png': lambda: __import__('JointEdit.DynamicCoexistToolUI', fromlist=['main']).main(),
    'Zipper_rig_tool.png': lambda: __import__('GeneralTools.ZipperUI', fromlist=['main']).main(),
    'make_follow.png': lambda: __import__('QuickTools.follow_tool', fromlist=['main']).main(),
    'material_tool.png': lambda: __import__('py_rigAssit.model_mod.shaderTool',
                                            fromlist=['show_material_tool']).show_material_tool(),
    'soft_Deform.png': lambda: __import__('QuickTools.CreateSoftMode', fromlist=['showWindow']).showWindow(),
    'add_attributes.png': lambda: __import__('ControllerTool.AddAttributeUI', fromlist=['main']).main(),
    'target_split_tool.png': lambda: __import__('GeneralTools.blendDivider_split', fromlist=['main']).main(),
    'molde_uv_shader.png': lambda: __import__('py_rigAssit.model_mod.model_transfer_uv_shader',
                                              fromlist=['main']).main(),
    'slide_FK.png': lambda: __import__('JointEdit.variable_FK_tool', fromlist=['main']).main(),
}

command_info = {
    '1_arrt_shif_dn.png': Arrt_shif_dn,
    '0_arrt_shif_up.png': Arrt_shif_up,
    'Mirror_ctrl.png': Mirror_ctrl,
    'Mater_ctrl.png': Master_ctrl,
    'Vis_ctrl.png': Vis_ctrl,
    'VIS_Connect_mesh.png': Connect_mesh,
    'make_follow.png': lambda: __import__('QuickTools.follow_tool', fromlist=['main']).main(),
    'ctrl_move_drv.png': lambda: __import__('QuickTools.QuickFunction',
                                            fromlist=['QuickFunctions']).QuickFunctions().ctrlValueMoveDrv(),
    '4_delete_ani_key.png': lambda: __import__('QuickTools.QuickFunction',
                                               fromlist=['QuickFunctions']).QuickFunctions().deleteAnimation(),
    'make_group.png': lambda: __import__('QuickTools.QuickFunction',
                                         fromlist=['MakeGroupPivot']).MakeGroupPivot().make_group_multi(),
    'make_pivot.png': lambda: __import__('QuickTools.QuickFunction',
                                         fromlist=['MakeGroupPivot']).MakeGroupPivot().make_pivot(),
    'rename_bs_node.png': lambda: __import__('QuickTools.QuickFunction',
                                             fromlist=['QuickFunctions']).QuickFunctions().renameBlendShape(),
    'rename_skin_node.png': lambda: __import__('QuickTools.QuickFunction',
                                               fromlist=['QuickFunctions']).QuickFunctions().renameSkinCluster(),
    'Remove_DoubleSkin.png': lambda: __import__('JointEdit.JointEditFun',
                                                fromlist=['EditJnt']).EditJnt().remove_DoubleSkin(),
    'snape_center.png': lambda: __import__('QuickTools.QuickFunction',
                                           fromlist=['QuickFunctions']).QuickFunctions().snape_seleted_to_manip(),
    'target_invert.png': lambda: __import__('QuickTools.QuickFunction',
                                            fromlist=['QuickFunctions']).QuickFunctions().correctshape(),
    'target_mirror.png': lambda: __import__('QuickTools.QuickFunction',
                                            fromlist=['QuickFunctions']).QuickFunctions().mirror_targets(),
    'target_split.png': lambda: __import__('GeneralTools.meshTool', fromlist=['MeshEdit']).MeshEdit().split_target(),
    'soft_create_joint.png': lambda: __import__('QuickTools.QuickFunction',
                                                fromlist=['QuickFunctions']).QuickFunctions().soft_create_joint(),
    'soft_select_vertxs.png': lambda: __import__('QuickTools.QuickFunction',
                                                 fromlist=['QuickFunctions']).QuickFunctions().soft_select_vertices(),
    '2_objects_to_world.png': Quick.object_to_world,

    '3_objects_to_world_return.png': Quick.object_to_return,

    'export_curve_points.png': lambda: __import__('QuickTools.object_postion_info',
                                                  fromlist=['curve_vetx_save']).curve_vetx_save(),
    'export_position.png': lambda: __import__('QuickTools.object_postion_info',
                                              fromlist=['objects_position_save']).objects_position_save(),
    'export_sdk_info.png': sdk_info.store_sdk_info,
    'import_curve_points.png': lambda: __import__('QuickTools.object_postion_info',
                                                  fromlist=['load_curve_info']).load_curve_info(),
    'import_position.png': lambda: __import__('QuickTools.object_postion_info',
                                              fromlist=['load_objects_position']).load_objects_position(),
    'import_sdk_info.png': sdk_info.import_sdk_data,
    'mesh_distance_create_jnt.png': lambda: __import__('QuickTools.QuickFunction', fromlist=[
        'QuickFunctions']).QuickFunctions().createJntByMeshFarthest_point(),
    'copy_attributes.png': lambda: __import__('GeneralTools.AttributeSetting',
                                              fromlist=['SetAttrTool']).SetAttrTool().copy_attrs(),
    'insert_joints.png': Insertjoint_selected,
    'delete_namespace.png': lambda: __import__('OptimizeSceneFun',
                                               fromlist=['OptimizeScene']).OptimizeScene().removeNameSpase(),
    'delete_unused_influences_Joints.png': lambda: __import__('JointEdit.JointEditFun', fromlist=[
        'EditJnt']).EditJnt().remove_seleted_unskin_joint(),
    'delete_unused_node.png': lambda: __import__('OptimizeSceneFun',
                                                 fromlist=['OptimizeScene']).OptimizeScene().deleteunUsedNodes(),
}


toolTip = {
    'IKFK_complex_system.png': u"高级ikfk绑定",
    'Mirror_skin.png': u"特殊镜像权重: 镜像一些难以镜像的权重和在有pose的情况也可以镜像",
    'Joint_orent.png': u"关节定向工具",
    'Mirror_ctrl.png': u"镜像控制器形态",
    'Mater_ctrl.png': u"导入Global_ctrl",
    'Vis_ctrl.png': u"创建/修正 VIS ctrl",
    'Copy_skin_tool.png': u"特殊拷贝权重工具：拷贝一些关节位置过于贴合拷贝不上",
    'Joints_Chain_IKFK.png': u"批量选择关节链创建ikfk系统",
    'VIS_Connect_mesh.png': u"Visibility链接模型的显示状态",
    'Target_Correct.png': u"修正blendShape目标体",
    'Mirror_SDK.png': u"镜像 animCurve node info (SDK)",
    'BS_Split_tool.png': u"拆分blendshape目标体",
    'separate_Head.png': u"工具body拆分head模型",
    'combine_SDK.png': u"组合驱动工具",
    'skinner.png':u"skinner 权重导出导入工具（需要安装numpy和scip)",
    'sqr.png':u"头部挤压",
    'find_Edge_UpDown.png':u"拆分循环边上下，创建曲线",
    'animat_tool.png':u"动画数据导入导出工具",
    'Split_Skin_Tool.png':u"拆分权重工具",
    'Animat_Ribbon.png': u"surface 绑定工具\n内置生长动画效果和拉伸动画",
    'Deform_Weight_Edit.png': u"变形器权重拷贝编辑工具",
    'Double_FK_tool.png': u"双向FK绑定系统",
    'Dynamic_curve_rig.png': u"大理学曲线绑定工具",
    'Zipper_rig_tool.png': u"拉链绑定工具",
    'ctrl_move_drv.png': u"将控制器_ctrl的位置信息移动到它的_drv组\n* 只适用与PY_RIGASSIT工具创建的控制器系统或group有_ctrl, _drv 规范命名的控制器",
    '4_delete_ani_key.png': u"删除场景里所k的动画帧",
    'make_follow.png': u"创建Worldspace Group\n* 只适用与PY_RIGASSIT工具创建的控制器系统或group有_ofs, _con 规范命名的控制器",
    'make_group.png': u"批量添加组",
    'make_pivot.png': u"批量添加控制器的轴心移动\n选择需要添加轴心移动的对象直接运行",
    'rename_bs_node.png': u"批量一键重命名对象的skinCluster节点\n选择对象直接运行即可",
    'rename_skin_node.png': u"批量一键重命名对象的blendShape节点\n选择对象直接运行即可",
    'snape_center.png': u"将对象吸附到所选的 点，线，面 的中心\n选择定位的点/线/面 + 被吸附的对象",
    'target_invert.png': u"反算目标体\n选择权重模型 + 雕刻好的pose对象",
    'target_mirror.png': u"左右镜像目标体\n选择需要镜像的目标体 + 默认状态的源对象",
    'target_split.png': u"权重拆分目标pose\n选择目标pose mesh + 权重mesh",
    '1_arrt_shif_dn.png': u"选择属性向下移",
    '0_arrt_shif_up.png': u"选择属性向上移",
    'Remove_DoubleSkin.png': u"blendshape双倍位移\n权重逆矩阵去双倍位移:选择模型直接运行（此处控制器和组的命名需要是此工具添加的）",
    'soft_select_vertxs.png': u"软选择范围选择点",
    'soft_create_joint.png': u"软选择创建权重关节\n关节朝向 会弹窗是否朝对象法线方向",
    '2_objects_to_world.png': u"选择需要临时移出对象在大纲（层级）当前位置, 移出到世界",
    '3_objects_to_world_return.png': u"将之前运行objects to world时, 移出层级的所有对象重新回到原始位置",
    'export_curve_points.png': u'选择需要导出曲线的点位置信息',
    'export_position.png': u'选择需要导出位置信息的对象',
    'export_sdk_info.png': u'选择需要导出信息的sdk',
    'import_curve_points.png':u'导入曲线的点位置信息,无需选择对象',
    'import_position.png': u'导入对象的位置信息,无需选择对象',
    'import_sdk_info.png': u'导入已有sdk信息,无需选择对象',
    'material_tool.png': u'material tool',
    'soft_Deform.png': u'soft Deform',
    'mesh_distance_create_jnt.png': u"根据所选mesh的最远的两个点创建关节",
    'copy_attributes.png':u"拷贝属性名称\n选择需要拷贝的对象，加选拷贝源对象，然后选择源对象属性通道里的属性名称 运行即可",
    'add_attributes.png':u"批量添加属性工具",
    'target_split_tool.png': u"平面拆分bs target",
    'insert_joints.png': u"批量插入关节\n选择关节的开始端运行即可",
    'molde_uv_shader.png': u"传递模型uv和材质球工具",
    'delete_namespace.png': u"delete namespace",
    'delete_unused_influences_Joints.png': u"移除对象里没有权重影响的关节",
    'delete_unused_node.png': u"删除未使用的节点",
    'slide_FK.png': lambda: u"活动的FK",
           }