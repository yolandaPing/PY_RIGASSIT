# -*- coding: utf-8 -*-

# .FileName:mel_translate_py.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/4/23 19:42
# .Finish time:
from functools import partial

from py_rigAssit import QtWidgets, QtCore, QtGui, Widgets, PyouPersistentWindow
import pymel.core as pm

PY_WIDGEAT = Widgets()


class TranslateMELtoPythonUI(PyouPersistentWindow):


    def __init__(self, parent=None):
        super(TranslateMELtoPythonUI, self).__init__("TranslateMELtoPythonUI", "TranslateMELtoPythonUI", parent)
        self.setWindowTitle("Translate MEL to Python")
        self.setMinimumSize(600, 460)
        self.loadWindowSettings()

        main = QtWidgets.QVBoxLayout(self)
        main.setContentsMargins(4, 4, 4, 4)
        main.setSpacing(4)

        main.addWidget(PY_WIDGEAT.create_title("translate mel to python", 16, None))

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setContentsMargins(0, 0, 0, 0)

        cld_widget = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(cld_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(4)

        scroll.setWidget(cld_widget)
        main.addWidget(scroll)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(4, 2, 2, 4)
        main_layout.setSpacing(8)

        main_layout.addWidget(PY_WIDGEAT.create_text(">>> MEL转换时不要有中文 !!!"))

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        mel_group = QtWidgets.QGroupBox("MEL:")
        mel_layout = QtWidgets.QVBoxLayout(mel_group)
        self.mel_text_edit = QtWidgets.QPlainTextEdit()
        self.mel_text_edit.setPlaceholderText("在此输入MEL代码...")
        mel_layout.addWidget(self.mel_text_edit)
        splitter.addWidget(mel_group)

        python_group = QtWidgets.QGroupBox("PYTHON:")
        python_layout = QtWidgets.QVBoxLayout(python_group)
        self.python_text_edit = QtWidgets.QPlainTextEdit()
        self.python_text_edit.setReadOnly(True)
        python_layout.addWidget(self.python_text_edit)
        splitter.addWidget(python_group)

        main_layout.addWidget(splitter, 1)

        apply_button = QtWidgets.QPushButton("Apply")
        apply_button.clicked.connect(self.mel_to_python)
        main_layout.addWidget(apply_button)

        scroll_layout.addLayout(main_layout)

        scroll_layout.addLayout(main_layout)
        PY_WIDGEAT.create_copyrightText(main, "2024-2026")


    def mel_to_python(self):
        import pymel.tools.mel2py as mel2py

        mel_text = self.mel_text_edit.toPlainText()
        if not mel_text.strip():
            QtWidgets.QMessageBox.warning(self, "警告", "MEL输入框为空，请先输入MEL代码。")
            return

        try:
            py_text = mel2py.mel2pyStr(mel_text, pymelNamespace='pm')
            py_fixed = py_text.replace("pymel.all", "pymel.core")
            py_fixed = py_fixed.replace("pm.pm.cmds.", "mc.")
            final_text = "import maya.cmds as mc\n" + py_fixed
            self.python_text_edit.setPlainText(final_text)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "转换错误",
                "转换过程中发生错误：\n{}".format(e)
            )


def show():

    global _mel_py_instance
    try:
        _mel_py_instance.close()  # pylint: disable=E0601
        _mel_py_instance.deleteLater()
    except:
        pass
    _mel_py_instance = TranslateMELtoPythonUI()
    _mel_py_instance.show()

    return _mel_py_instance


if __name__ == '__main__':

    show()
