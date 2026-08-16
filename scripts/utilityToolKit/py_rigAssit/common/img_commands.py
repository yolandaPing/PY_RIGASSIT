# -*- coding: utf-8 -*-

# .FileName:img_commands.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/13 22:52
# .Finish time:
from py_rigAssit.dialogs import Help
from py_rigAssit.common.command_dispatcher import CommandDispatcher


@CommandDispatcher.register("Show Help")
def show_img(ui, btn_id):
    maps = {1: "seleted_joints_create_ctrl",
            2: "Joint_Chain_IKFK_System",
            3: "IKFK_System",
            5: "editJoint_spineIK_ribbon",
            6: "reverse_fk_Tool",
            7: "dynamic_coexist",
            8: "Zipper_Tool",
            9: "variable_Fk_tool",
            10: "copyTool3",
            11: "copy_skinWeight",
            12: "copy_blendshape",
            13: "copy_ffd",
            14: "copy_UV",
            15: "add_attr_Tool",
            16: "ribbon_rigging",
            17: "lock_curve_visibility",
            18: "mel_script_manager",
            19: "split_skin_weight",
            20: "split_skin_weight_ng2",
            21: "split_skin_weight_soft"
            }

    try:
        Help.HelpImage("", maps[btn_id])
    except:
        pass