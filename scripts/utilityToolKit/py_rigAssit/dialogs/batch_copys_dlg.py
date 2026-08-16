# -*- coding: utf-8 -*-
# .FileName:CopyToolsDialog
# .Date....:2024-07-06 : 15 :27
# .@Author:You P
# .
# .Finish time:
from functools import partial

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
from selectOrRemove import SelectOrremoveObj
from CopyEdit.copy_blendShape_info import BlendShapeInfo
import CopyEdit.copy_skinCluster_info as copy_skinCluster_info

# from py_rigAssit.dialogs import decorator
from py_rigAssit.common.command_dispatcher import CommandDispatcher
import py_rigAssit.common.img_commands
from py_rigAssit.dialogs import mayaPrint

import  maya.cmds as cmds

_obj = SelectOrremoveObj()
_widgest = Widgets()
_bsInfo = BlendShapeInfo()


class PYCopyToolsLayout(QtWidgets.QWidget):

    WINDOW_TITLE = "Batch Copys "
    TimeStamp = "2022-2026"
    mayaMajorVersion = int(cmds.about(version=True)[0:4])
    txts = ('', u"默认一对一或一对多拷贝", u"识别组里对应的名字进行拷贝权重", u"合并源组的所有对象权重，拷贝给新对象组",
                 u"在当前的skinNode基础上额外添加新的skinNode", u"将多个模型skin节点拷贝给新模型")

    def __init__(self, parent=None):
        super(PYCopyToolsLayout, self).__init__(parent)

        if self.mayaMajorVersion < 2024:
            self.skin_radio_en = False
        else:
            self.skin_radio_en = True

    def init_ui(self, copyright=False):
        container_main = QtWidgets.QWidget()
        container_main.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        main_layout = QtWidgets.QVBoxLayout(container_main)
        main_layout.setSpacing(4)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(_widgest.create_title("Batch Copy Tools", 15, ""))

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        scroll_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(1)

        self.scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(self.scroll_area)

        v_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        v_splitter.setChildrenCollapsible(True)
        top_frame = QtWidgets.QFrame()
        self.create_textScrollList_lay(top_frame)

        bottom_frame = QtWidgets.QFrame()
        bottom_layout = QtWidgets.QVBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(1)
        _widgest.separator(bottom_layout)
        self.create_type_widgets(bottom_layout)
        # bottom_layout.addStretch()
        v_splitter.addWidget(top_frame)
        v_splitter.addWidget(bottom_frame)
        v_splitter.setStretchFactor(0, 1)
        v_splitter.setStretchFactor(1, 0)
        v_splitter.setSizes([3, 1])

        scroll_layout.addWidget(v_splitter)

        self.create_connections()
        return container_main

    def source_widgets(self, frame):
        self.main_layout_source = QtWidgets.QVBoxLayout(frame)
        self.main_layout_source.setContentsMargins(8, 0, 4, 4)
        self.main_layout_source.setSpacing(0)

        btn_layout_source = QtWidgets.QHBoxLayout()
        source_label = QtWidgets.QLabel("source:")
        source_label.setAlignment(QtCore.Qt.AlignCenter)

        self.source_list = QtWidgets.QListWidget()
        self.source_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.load_source_btn = QtWidgets.QPushButton("load")
        self.load_source_btn.setProperty("green", True)

        self.remove_source_btn = QtWidgets.QPushButton("remove")
        self.remove_source_btn.setProperty("danger", True)

        self.main_layout_source.addWidget(source_label)
        self.main_layout_source.addWidget(self.source_list)
        self.main_layout_source.addLayout(btn_layout_source)
        btn_layout_source.addWidget(self.load_source_btn)
        btn_layout_source.addWidget(self.remove_source_btn)

    def target_widgets(self, frame):
        self.main_layout_target = QtWidgets.QVBoxLayout(frame)
        self.main_layout_target .setContentsMargins(4, 0, 8, 4)
        self.main_layout_target.setSpacing(0)
        btn_layout_target = QtWidgets.QHBoxLayout()
        target_label = QtWidgets.QLabel("target:")
        target_label.setAlignment(QtCore.Qt.AlignCenter)
        self.target_list = QtWidgets.QListWidget()
        self.target_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.load_target_btn = QtWidgets.QPushButton("load")
        self.load_target_btn.setProperty("green", True)
        self.remove_target_btn = QtWidgets.QPushButton("remove")
        self.remove_target_btn.setProperty("danger", True)

        self.main_layout_target.addWidget(target_label)
        self.main_layout_target.addWidget(self.target_list)
        self.main_layout_target.addLayout(btn_layout_target)
        btn_layout_target.addWidget(self.load_target_btn)
        btn_layout_target.addWidget(self.remove_target_btn)

    def create_textScrollList_lay(self, parent_layout):
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.setHandleWidth(1)
        splitter.setChildrenCollapsible(True)
        frame1 = QtWidgets.QFrame()
        frame2 = QtWidgets.QFrame()
        splitter.addWidget(frame1)
        splitter.addWidget(frame2)
        splitter.setSizes([100, 100])
        self.source_widgets(frame1)
        self.target_widgets(frame2)

        main_layout = QtWidgets.QVBoxLayout(parent_layout)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(splitter)

    def create_type_widgets(self, parent_layout):
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Raised)
        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.setContentsMargins(2, 2, 2, 2)
        group = QtWidgets.QGroupBox(u"批量拷贝:")
        layout = QtWidgets.QVBoxLayout(group)
        self.copy_block = _widgest.create_radiogroup(
            "Copy Mode",
            [
                ("one/multis", 1, self.txts[1]),
                ("skin grp name", 2, self.txts[2]),
                ("skin grp com", 3, self.txts[3]),
            ],
            default_id=1
        )

        self.skin_block = _widgest.create_radiogroup(
            "Skin Mode",
            [
                ("default", 1, None),
                ("add mult skinNode", 2, self.txts[4]),
                ("multis to one", 3, self.txts[5]),
            ],
            default_id=1,
            enabled_map={2: self.skin_radio_en, 3: self.skin_radio_en}
        )

        self.type_block = _widgest.create_radiogroup(
            "Type",
            [
                ("skinWeight", 1, None),
                ("blendshape", 2, None),
                ("ffd", 3, None),
                ("uv", 4, None),
            ],
            default_id=1
        )
        bs_op_layout = QtWidgets.QHBoxLayout()
        self.clean_invild_cbx = QtWidgets.QCheckBox(u'Cleaning targets 清理无效的target')
        self.clean_invild_cbx.setChecked(True)
        self.clean_invild_cbx.setEnabled(False)
        self.cvWarp_cbx = QtWidgets.QCheckBox(u'cvWarp')
        self.cvWarp_cbx.setChecked(False)
        self.cvWarp_cbx.setEnabled(False)

        bs_op_layout.addWidget(self.clean_invild_cbx)
        bs_op_layout.addWidget(self.cvWarp_cbx)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(2)

        self.apply_btn = QtWidgets.QPushButton("Apply")
        self.apply_btn.setProperty("main", True)

        self.help_btn = QtWidgets.QPushButton()
        self.help_btn.setIcon(QtGui.QIcon(":\help.png"))
        self.help_btn.setProperty("help", True)
        btn_layout.addWidget(self.apply_btn,60)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.help_btn,1)

        self.hit_txt = _widgest.create_text(u'{}'.format(self.txts[1]))
        layout.addWidget(self.hit_txt)
        layout.addWidget(self.copy_block)
        _widgest.separator(layout)
        layout.addWidget(self.skin_block)
        layout.addWidget(_widgest.create_text(u'>> Please select the under type of copy first !!!'))
        # layout.addWidget(self.clean_invild_cbx)
        layout.addLayout(bs_op_layout)
        layout.addWidget(self.type_block)
        layout.addLayout(btn_layout)
        frame_layout.addWidget(group)
        parent_layout.addWidget(frame)

    def create_connections(self):
        self.dispatcher = CommandDispatcher()
        # source mod
        self.source_list.itemSelectionChanged.connect(self._on_seleted_source)
        self.load_source_btn.clicked.connect(self._on_load_source)
        self.remove_source_btn.clicked.connect(self._on_remove_source )
        #target mod
        self.target_list.itemSelectionChanged.connect(self._on_seleted_target)
        self.load_target_btn.clicked.connect(self._on_load_target)
        self.remove_target_btn.clicked.connect(self._on_remove_target)
        self.copy_block.idClicked.connect(self._on_copy_type_toggled)
        self.skin_block.idClicked.connect(self._on_skin_radio_toggled)
        self.type_block.idClicked.connect(self._on_type_Toggled)
        self.apply_btn.clicked.connect(self._on_apply_clicked)
        self.help_btn.clicked.connect(self.showHHelpImage)

    def showHHelpImage(self):
        self.dispatcher.execute("Show Help", (self.type_block.checkedId()+9))

    def _on_load_source(self):
        _obj.load_list_widget_items(self.source_list, True)

    def _on_load_target(self):
        _obj.load_list_widget_items(self.target_list,True)

    def _on_seleted_source(self):
        _obj.list_widget_seleted_item(self.source_list)

    def _on_seleted_target(self):
        _obj.list_widget_seleted_item(self.target_list)

    def _on_remove_source(self):
        _obj.remove_seleted_items(self.source_list)

    def _on_remove_target(self):
        _obj.remove_seleted_items(self.target_list)

    def _on_apply_clicked(self):
        mode = self.copy_block.checkedId()

        if mode == 1:
            self.run_copy()
        else:
            self.grp_to_copy(mode)

    def _on_copy_type_toggled(self, btn_id):
        self.hit_txt.setText(self.txts[btn_id])

        if btn_id == 1:
            self.type_block.setEnabledByIds([2, 3, 4], True)
        else:
            self.type_block.setEnabledByIds([2, 3, 4], False)

    def _on_skin_radio_toggled(self, btn_id):
        if btn_id == 1:
            self.type_block.setEnabledByIds([2, 3, 4], True)
        else:
            self.type_block.setEnabledByIds([2, 3, 4], False)

    def _on_type_Toggled(self, btn_id):

        if btn_id != 1:
            self.copy_block.setEnabledByIds([2, 3], False)
            self.skin_block.setEnabledByIds([1, 2, 3], False)
        else:
            self.copy_block.setEnabledByIds([2, 3], True)
            self.skin_block.setEnabledByIds([2, 3], self.skin_radio_en)
            self.skin_block.setEnabledByIds([1], True)

        if btn_id == 2:
            self.clean_invild_cbx.setEnabled(True)
        else:
            self.clean_invild_cbx.setEnabled(False)

    def _get_src_tgt(self):
        return (
            _obj.get_list_widget_items(self.source_list),
            _obj.get_list_widget_items(self.target_list)
        )

    def _pair_iter(self, oldMod, newMod):
        if len(oldMod) == 1:
            for tgt in newMod:
                yield oldMod[0], tgt
        elif len(oldMod) == len(newMod):
            for src, tgt in zip(oldMod, newMod):
                yield src, tgt
        else:
            mayaPrint.error("Mismatch source/target count")
            return

    def run_copy(self):
        copy_type = self.type_block.checkedId()

        if copy_type == 1:
            self.run_skin_copy()
        elif copy_type == 2:
            self.copy_blendshape()
        elif copy_type == 3:
            self.copy_ffd()
        elif copy_type == 4:
            self.copy_uv()

    def run_skin_copy(self):
        mode = self.copy_block.checkedId()

        if mode == 1:
            self.copy_skin_default()
        elif mode == 2:
            self.copy_skin_add_node()
        elif mode == 3:
            self.copy_skin_multi_to_one()

    # @decorator.undo
    def copy_skin_default(self):
        oldMod, newMod = self._get_src_tgt()
        cmds.undoInfo(openChunk=True)
        try: 
            for src, tgt in self._pair_iter(oldMod, newMod):
                copy_skinCluster_info.copy_skin_type([src, tgt], if_add=False)
                mayaPrint.log(" {} >>> {} .".format(src, tgt))
        finally:
            cmds.undoInfo(closeChunk=True)

    # @decorator.undo
    def copy_skin_add_node(self):
        oldMod, newMod = self._get_src_tgt()
        cmds.undoInfo(openChunk=True)
        try: 
            for src, tgt in self._pair_iter(oldMod, newMod):
                copy_skinCluster_info.copy_skin_type([src, tgt], if_add=True)
                mayaPrint.log(" {} >>> {} .".format(src, tgt))
        finally:
            cmds.undoInfo(closeChunk=True)

    # @decorator.undo
    def copy_skin_multi_to_one(self):
        oldMod, newMod = self._get_src_tgt()
        cmds.undoInfo(openChunk=True)
        try: 
            copy_skinCluster_info.copy_multi_mesh_skins_to_one(oldMod, newMod)
            mayaPrint.log(" copy Successfully.")
        finally:
            cmds.undoInfo(closeChunk=True)

    # @decorator.undo
    def copy_blendshape(self):
        clean = self.clean_invild_cbx.isChecked()
        oldMod, newMod = self._get_src_tgt()
        cmds.undoInfo(openChunk=True)
        try: 
            for src, tgt in self._pair_iter(oldMod, newMod):
                _bsInfo.apply_copy_blendShape_Drefrom(Source=src, Object=tgt)
                if clean:
                    _bsInfo.CleanUpBS([tgt])

                mayaPrint.log("copy blendShape: {} >>> {} .".format(src, tgt))
        finally:
            cmds.undoInfo(closeChunk=True)

    # @decorator.undo
    def copy_uv(self):
        import CopyEdit.copy_FFD_UV as copy_FFD_UV
        oldMod, newMod = self._get_src_tgt()
        cmds.undoInfo(openChunk=True)
        try: 
            for src, tgt in self._pair_iter(oldMod, newMod):
                copy_FFD_UV.transferUV(src, tgt)
                mayaPrint.log("transferUV: {} >>> {} .".format(src, tgt))
        finally:
            cmds.undoInfo(closeChunk=True)

    def copy_ffd(self):
        import CopyEdit.copy_FFD_UV as copy_FFD_UV
        oldMod, newMod = self._get_src_tgt()
        cmds.undoInfo(openChunk=True)
        try:   
            for src, tgt in self._pair_iter(oldMod, newMod):
                copy_FFD_UV.ADDFFD(src, tgt)
                mayaPrint.log("transferFFD: {} >>> {} .".format(src, tgt))
        finally:
            cmds.undoInfo(closeChunk=True)

    # @decorator.undo
    def grp_to_copy(self, Type):
        oldMod, newMod = self._get_src_tgt()
        cmds.undoInfo(openChunk=True)
        try:    
            for src, tgt in self._pair_iter(oldMod, newMod):
                if Type == 2:
                    copy_skinCluster_info.grp_object_name_copy(src, tgt)
                elif Type == 3:
                    copy_skinCluster_info.grp_combine_copy_skin(src, tgt)

            cmds.select(cl=1)
            mayaPrint.log(' group object copy Successfully.')
        finally:
            cmds.undoInfo(closeChunk=True)


class PYCopyToolsDialog(PyouPersistentWindow):
    WINDOW_TITLE = "Batch Copys "
    TimeStamp = "2022-2026"

    def __init__(self, parent=None):
        super(PYCopyToolsDialog, self).__init__("PYCopyToolsDialog", "PYCopyToolsDialog", parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setObjectName('pyCopyToolsDialog')
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self._build_ui()
        self.loadWindowSettings()


    def _build_ui(self):
        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(4)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)

        self.widget = PYCopyToolsLayout(parent=self)

        scroll_layout.addWidget(self.widget.init_ui())

        _widgest.create_copyrightText(main, self.TimeStamp)


def main():
    global Copy_Dialog

    try:
        Copy_Dialog.close() # pylint: disable=E0601
        Copy_Dialog.deleteLater()
    except:
        pass

    Copy_Dialog = PYCopyToolsDialog()
    Copy_Dialog.show()


if __name__ == '__main__':

    main()
