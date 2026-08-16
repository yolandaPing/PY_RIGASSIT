# -*- coding: utf-8 -*-

# .FileName:dir_pose_solver.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/7/19 00:46
# .Finish time:

import math
import maya.cmds as cmds
import pymel.core as pm
from DrivePose.direction_dirve_pose import driver_core
import mayaPrint as mayaPrint


class DIRPoseTempSolver(object):
    def __init__(self):
        self.info_node = None
        self.input_pose = None
        self.drive_joint = None
        self.drive_ctrl = None
        self.temp_joint = None
        self.temp_info = None
        self.system = None

    def load_driver(self, info_node, input_pose):
        self.clear()
        self.info_node = info_node
        self.input_pose = input_pose
        if not cmds.objExists(input_pose):
            return False
        if cmds.objExists(input_pose + ".drive_joint"):
            self.drive_joint = cmds.getAttr(input_pose + ".drive_joint")
        self.drive_ctrl = cmds.getAttr(input_pose + ".drive_ctrl")
        if isinstance(self.drive_ctrl, list):
            self.drive_ctrl = self.drive_ctrl[0]
        if not self.drive_joint:
            mayaPrint.warning("No drive_joint")
            return False
        return True

    def create_temp_joint(self):
        self.clear_temp()
        self.temp_joint = cmds.createNode("joint", n="DIRPose_temp_joint")
        pat = cmds.listRelatives(self.info_node, parent=True)[0]
        self.temp_info = cmds.createNode("joint", n="DIRPose_temp_PoseInfo", parent=pat)
        cmds.matchTransform(self.temp_info, self.info_node)
        cmds.parent(self.temp_joint, self.temp_info)
        matrix = cmds.xform(self.input_pose, q=True, ws=True, matrix=True)
        cmds.xform(self.temp_joint, ws=True, matrix=matrix)
        cmds.setAttr(self.temp_joint + ".rotate", 0,0,0, type="double3")
        cmds.setAttr(self.temp_joint + ".jointOrient", 0,0,0, type="double3")
        cmds.setAttr(self.temp_info + ".visibility", 0)
        return self.temp_joint

    def build_driver_network(self):
        if not self.temp_joint:
            return False
        try:
            self.system = driver_core.DIRDrivePoseSystem()
            self.system.aixs = cmds.getAttr(self.info_node + ".init_axis")
            if isinstance(self.system.aixs, tuple):
                self.system.aixs = self.system.aixs[0]
            self.system.update_angle_direction(self.temp_joint)
            cmds.select(cl=1)
            return True
        except Exception as e:
            print("Temp DIR network error:", e)
            return False

    def matrix_set_position(self, angle, direction):
        if not self.temp_joint:
            return
        d = math.radians(direction)
        a = math.radians(angle)
        direction_matrix = pm.datatypes.Matrix([
            [1,0,0,0],
            [0,math.cos(d),math.sin(d),0],
            [0,-math.sin(d),math.cos(d),0],
            [0,0,0,1]
        ])
        angle_matrix = pm.datatypes.Matrix([
            [math.cos(a),math.sin(a),0,0],
            [-math.sin(a),math.cos(a),0,0],
            [0,0,1,0],
            [0,0,0,1]
        ])
        result = direction_matrix.inverse() * angle_matrix * direction_matrix
        euler = pm.datatypes.EulerRotation(result)
        cmds.setAttr(self.temp_joint + ".rotate",
                     math.degrees(euler.x), math.degrees(euler.y), math.degrees(euler.z), type="double3")
        cmds.dgdirty(self.temp_joint)

    def get_rotate(self):
        if not self.temp_joint or not cmds.objExists(self.temp_joint):
            return None
        cmds.matchTransform(self.drive_ctrl, self.temp_joint, pos=False, rot=True)
        return cmds.getAttr(self.drive_ctrl+".rotate")[0]

    def clear_temp(self):
        for node in [self.temp_joint, self.temp_info]:
            if node and cmds.objExists(node):
                cmds.delete(node)
        self.temp_joint = None
        self.temp_info = None
        self.system = None

    def clear(self):
        self.clear_temp()
        self.info_node = None
        self.input_pose = None
        self.drive_joint = None
        self.drive_ctrl = None

