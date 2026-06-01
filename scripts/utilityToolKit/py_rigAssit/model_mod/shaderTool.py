# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from PySide2.QtWidgets import *


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major == 2:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)
    if sys.version_info.major == 3:
     return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

    
    
class CustomColorButton(QtWidgets.QLabel):
    
    def __init__(self, color = QtCore.Qt.white, parent=None):
        super(CustomColorButton, self).__init__(parent)
        
        self._color = QtGui.QColor()
        
        self.set_size(40,18)
        self.set_color(color)
        
    def set_size(self, width, height):
        self.setFixedSize(width, height)
        
    def set_color(self, color):
        color = QtGui.QColor(color)
        
        self._color = color
        
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(self._color)
        self.setPixmap(pixmap)
        
    def get_color(self):
        return self._color

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor(self.get_color(), self, option = QtWidgets.QColorDialog.DontUseNativeDialog)
        if color.isValid():
            self.set_color(color)
            
    def mouseReleaseEvent(self, mouse_event):
        self.select_color()
        
    

class MaterialTool(QtWidgets.QDialog):
    
    def __init__(self,parent=maya_main_window()):
        super(MaterialTool,self).__init__(parent)

        self.setWindowTitle("Material Shader Tool")
        self.setMinimumWidth(260)

        self.create_widgets()
        self.create_layout()
        
        # self.selected_color = None
        self.material_type = "Lambert"
    

    def create_widgets(self):
        # self.color_button = QPushButton("Set color")
        # self.color_button.clicked.connect(self.set_material_color)
        self.color_button = CustomColorButton(QtCore.Qt.white)
        
        self.material_type_label = QLabel("Select shader:")
        self.material_type_combo = QComboBox()
        self.material_type_combo.addItems(["Lambert","Blinn"])
        self.material_type_combo.currentIndexChanged.connect(self.set_material_type)

        self.apply_button = QPushButton("Create")
        self.apply_button.clicked.connect(self.apply_material)

    def create_layout(self):
        layout = QVBoxLayout()

        # Horizontal layout for material type and color selection
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.material_type_label)
        hbox_layout.addWidget(self.material_type_combo)
        hbox_layout.addWidget(self.color_button)

        layout.addLayout(hbox_layout)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)


    def set_material_color(self):
        # color = QColorDialog.getColor()
        color = self.color_button.get_color()
        if color.isValid():
            self.selected_color = color

    def set_material_type(self):
        self.material_type = self.material_type_combo.currentText()
        
    def Is_seleted_type(self,obj):
        node_type = cmds.nodeType(obj)
        if cmds.filterExpand(obj, selectionMask=12):  
            return ("mesh")
        elif cmds.filterExpand(obj, selectionMask=34):  
            return("meshFace")
        else:
            return None
            

    def apply_material(self):
        
        self.set_material_color()
        
        if not self.selected_color:
            QMessageBox.warning(self, "warning:", "Pick a color, please !")
            return

        selection = cmds.ls(selection=True, flatten=True)
        if not selection:
            # QMessageBox.warning(self, "warning", "Please select an object to apply the material ")
            cmds.warning("Please select an object to apply the material.")
            return
        
        obj_type = self.Is_seleted_type(selection[0])
        if obj_type == "meshFace":

            if self.material_type == "Blinn":
                material = cmds.shadingNode('blinn', asShader=True, name="{}_Mat#".format(selection[0].split(".")[0]))
            elif self.material_type == "Lambert":
                material = cmds.shadingNode('lambert', asShader=True, name="{}_Mat#".format(selection[0].split(".")[0]))
            else:
                cmds.warning("Invalid shader type")
                return

                
            cmds.setAttr(material + '.color', self.selected_color.redF(), self.selected_color.greenF(), self.selected_color.blueF(), type='double3')
            # shading group
            sg_name = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=material + "SG")
            cmds.connectAttr(material + ".outColor", sg_name + ".surfaceShader", force=True)
            cmds.select(selection)
            cmds.sets(forceElement=material + "SG", e=1)
                        
        
        else:

            for obj in selection:
                
                if self.material_type == "Blinn":
                    material = cmds.shadingNode('blinn', asShader=True, name="{}_Mat#".format(obj))
                elif self.material_type == "Lambert":
                    material = cmds.shadingNode('lambert', asShader=True, name="{}_Mat#".format(obj))
                else:
                    cmds.warning("Invalid shader type")
                    return
                
                cmds.setAttr(material + '.color', self.selected_color.redF(), self.selected_color.greenF(), self.selected_color.blueF(), type='double3')
                shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
                cmds.connectAttr(material + '.outColor', shading_group + '.surfaceShader', force=True)
                cmds.sets(obj, edit=True, forceElement=shading_group)


def show_material_tool():
    global material_tool
    try:
        material_tool.close() # Close the tool if it's already open
    except:
        pass
    material_tool = MaterialTool()
    material_tool.show()


if __name__ == '__main__':
    show_material_tool()
    
