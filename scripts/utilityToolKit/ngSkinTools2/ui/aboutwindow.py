import os
from xml.sax.saxutils import escape as escape

from ngSkinTools2 import cleanup, version
from ngSkinTools2.api.pyside import Qt, QtWidgets
from ngSkinTools2.api.session import session
from ngSkinTools2.ui import qt
from ngSkinTools2.ui.layout import scale_multiplier


def show(parent):
    """
    :type parent: QWidget
    """

    def header():
        # noinspection PyShadowingNames
        def leftSide():
            layout = QtWidgets.QVBoxLayout()
            layout.addStretch()
            layout.addWidget(QtWidgets.QLabel("<h1>ngSkinTools</h1>"))
            layout.addWidget(QtWidgets.QLabel("Version {0}".format(version.pluginVersion())))
            layout.addWidget(QtWidgets.QLabel(version.COPYRIGHT))

            url = QtWidgets.QLabel('<a href="{0}" style="color: #007bff;">{0}</a>'.format(version.PRODUCT_URL))
            url.setTextInteractionFlags(Qt.TextBrowserInteraction)
            url.setOpenExternalLinks(True)
            layout.addWidget(url)
            layout.addStretch()
            return layout

        def logo():
            from ngSkinTools2.api.pyside import QSvgWidget

            w = QSvgWidget(os.path.join(os.path.dirname(__file__), "images", "logo.svg"))

            w.setFixedSize(*((70 * scale_multiplier,) * 2))
            layout.addWidget(w)
            return w

        result = QtWidgets.QWidget()
        result.setPalette(qt.alternative_palette_light())
        result.setAutoFillBackground(True)

        hSplit = QtWidgets.QHBoxLayout()
        hSplit.setContentsMargins(30, 30, 30, 30)
        result.setLayout(hSplit)

        hSplit.addLayout(leftSide())
        hSplit.addStretch()
        hSplit.addWidget(logo())

        return result

    # noinspection PyShadowingNames
    def body():
        result = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        result.setLayout(layout)
        layout.setContentsMargins(30, 30, 30, 30)

        status = session.licenseClient.current_status()
        if status.licensed_to != "":
            layout.addWidget(QtWidgets.QLabel("This product is licensed to:"))
            layout.addWidget(QtWidgets.QLabel("<strong>" + escape(status.licensed_to) + "</strong>"))
        return result

    # noinspection PyShadowingNames
    def buttonsRow(window):
        layout = QtWidgets.QHBoxLayout()
        layout.addStretch()
        btnClose = QtWidgets.QPushButton("Close")
        btnClose.setMinimumWidth(100 * scale_multiplier)
        layout.addWidget(btnClose)
        layout.setContentsMargins(20 * scale_multiplier, 15 * scale_multiplier, 20 * scale_multiplier, 15 * scale_multiplier)

        btnClose.clicked.connect(lambda: window.close())
        return layout

    window = QtWidgets.QWidget(parent, Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
    window.resize(600 * scale_multiplier, 500 * scale_multiplier)
    window.setAttribute(Qt.WA_DeleteOnClose)
    window.setWindowTitle("About ngSkinTools")
    layout = QtWidgets.QVBoxLayout()
    window.setLayout(layout)
    layout.setContentsMargins(0, 0, 0, 0)

    layout.addWidget(header())
    layout.addWidget(body())
    layout.addStretch(2)
    layout.addLayout(buttonsRow(window))

    window.show()

    cleanup.registerCleanupHandler(window.close)
