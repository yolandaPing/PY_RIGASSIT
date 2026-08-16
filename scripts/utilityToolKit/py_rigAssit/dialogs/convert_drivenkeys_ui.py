# -*- coding: utf-8 -*-

# .FileName:convert_drivenkeys_ui.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/6/3 20:04
# .Finish time:
from functools import partial

from CommonUse.winUse import GetUIuse
import HelpImageUI as Help

import maya.cmds as cmds


class PYConvertDrivenkeysUI(GetUIuse):

    def __init__(self):
        self.WINDOW_NAME = 'Animkeys Convert Drivenkeys'
        self.windowT = 'PYConvertDrivenkeysWindow'
        self.timeStamp = ' 2026'

        self.withHight = (350, 220)

    def _build_ui(self):
        if (cmds.window(self.windowT, q=True, ex=True)):
            cmds.deleteUI(self.windowT)

        window_object = cmds.window(self.windowT, bgc=self.window_bgc, t=self.WINDOW_NAME, wh=self.withHight, s=0)
        self.menuBar_wigets_layout()
        cmds.columnLayout(adj=True)
        self.gui_creation()
        self.create_iconTextButton(self.timeStamp, 'gui')
        cmds.setFocus(window_object)
        cmds.showWindow(window_object)

    def menuBar_wigets_layout(self):
        cmds.menuBarLayout()
        cmds.menu(l=" Help ")
        cmds.menuItem(c=lambda *args: self.helpWebs('gui'), l="About using")

    def gui_creation(self):
        cmds.columnLayout(adj=True)
        self.create_title(self.WINDOW_NAME, self.withHight[0], 20)
        cmds.textFieldButtonGrp('pyconvert_driver_attr_field',
                                label='driver attr: ',
                                text='',
                                editable=False,
                                buttonLabel='  <<<  ',
                                ann='Add driver attributes',
                                cw3=(80, 120, 110),
                                adj=2,
                                buttonCommand=partial(self.load_driver_attr))

        cmds.separator(st='none', h=10)
        cmds.floatFieldGrp('pyconvert_driver_attr_value', label='driver min/max value: ', v1=0.0, v2=10.0, en=1, nf=2,
                           cw3=(120, 65, 65))
        cmds.separator(st='none', h=10)
        cmds.text(l=u'选择k动画对象,channelbox选择属性', font="smallObliqueLabelFont")

        cmds.rowColumnLayout(nc=2, adj=1, cw=[(1, 320), (2, 20)])
        cmds.button(label='Apply', bgc=self.button_bgc, h=30, command=partial(self.apply))
        Help.symbolHelpImageButton(file="", name="convert_drivenkeys", With=26)
        cmds.setParent('..')
        cmds.separator(st='none', h=10)


    def load_driver_attr(self, *args):
        from AttrNameUtils import PyAttrUtils
        attr_utils = PyAttrUtils()
        obj_attrs = attr_utils.getSelectedAttr()
        if obj_attrs:
            cmds.textFieldButtonGrp('pyconvert_driver_attr_field', edit=True, text=obj_attrs[-1])

    def apply(self, *args):
        from ConstrainEdit import convert_drivenkeys
        driver_attr_field = cmds.textFieldButtonGrp('pyconvert_driver_attr_field', q=True, text=True)
        driverMin = float(cmds.floatFieldGrp('pyconvert_driver_attr_value', q=1, v1=1))
        driverMax = float(cmds.floatFieldGrp('pyconvert_driver_attr_value', q=1, v2=1))

        if not driver_attr_field:
            cmds.error("Please load the driver properties first.")

        convert_drivenkeys.animkeys_to_drivenkeys(driver_attr_field, driverMin, driverMax)

    def showWindow(self):
        self._build_ui()


def main():
    convert_drivenkeys_ui = PYConvertDrivenkeysUI()
    convert_drivenkeys_ui.showWindow()

if __name__ == '__main__':
    main()