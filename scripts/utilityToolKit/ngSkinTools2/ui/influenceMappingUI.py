from ngSkinTools2 import cleanup, signal
from ngSkinTools2.api import influenceMapping, mirror
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.pyside import QtCore, QtGui, QtWidgets
from ngSkinTools2.signal import Signal
from ngSkinTools2.ui import dialogs, qt, widgets
from ngSkinTools2.ui.dialogs import yesNo
from ngSkinTools2.ui.layout import scale_multiplier
from ngSkinTools2.ui.options import config
from ngSkinTools2.ui.widgets import NumberSliderGroup

log = getLogger("influence mapping UI")


def open_ui_for_mesh(ui_parent, mesh):
    m = mirror.Mirror(mesh)
    mapper = m.build_influences_mapper()

    def do_apply(mapping):
        m.set_influences_mapping(mapping)
        m.save_influences_mapper(mapper)

    return open_as_dialog(ui_parent, mapper, do_apply)


def open_as_dialog(parent, matcher, result_callback):
    """

    :type matcher: ngSkinTools2.api.influenceMapping.InfluenceMapping
    """
    main_layout, reload_ui, recalc_matches = build_ui(parent, matcher)

    def button_row(window):
        def apply():
            result_callback(matcher.asIntIntMapping(matcher.calculatedMapping))
            window.close()

        def save_defaults():
            if not yesNo("Save current settings as default?"):
                return
            config.mirrorInfluencesDefaults = matcher.config.as_json()

        def load_defaults():
            matcher.config.load_json(config.mirrorInfluencesDefaults)
            reload_ui()
            recalc_matches()

        return widgets.button_row(
            [
                ("Apply", apply),
                ("Cancel", window.close),
            ],
            side_menu=[
                ("Save As Default", save_defaults),
                ("Load Defaults", load_defaults),
            ],
        )

    window = QtWidgets.QDialog(parent)
    cleanup.registerCleanupHandler(window.close)
    window.setWindowTitle("Influence Mirror Mapping")
    window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    window.resize(720 * scale_multiplier, 500 * scale_multiplier)
    window.setLayout(QtWidgets.QVBoxLayout())
    window.layout().addWidget(main_layout)
    window.layout().addLayout(button_row(window))

    window.show()

    recalc_matches()

    return window


def build_ui(parent, matcher):
    """

    :param parent: parent qt widget
    :type matcher: influenceMapping.InfluenceMapping
    """

    influence_data = matcher.influences

    influenceMapping.calcShortestUniqueName(matcher.influences)
    if matcher.destinationInfluences is not None and matcher.destinationInfluences != matcher.influences:
        influenceMapping.calcShortestUniqueName(matcher.destinationInfluences)

    update_globs = Signal("need recalc")
    reload_ui = Signal("reload_ui")

    mirror_mode = matcher.config.mirror_axis is not None

    def build_tree_hierarchy(tree_view):
        tree_items = {}  # mapping of path->treeItem
        influence_items = {}  # same as above, only includes non-intermediate items

        def find_item(path, is_intermediate):
            result = tree_items.get(path, None)
            if result is not None:
                return result

            split_path = path.rsplit("|", 1)
            parent_path, name = split_path if len(split_path) == 2 else ["", split_path[0]]

            item = QtWidgets.QTreeWidgetItem([name, '-', '(not in skin cluster)' if is_intermediate else '?'])
            tree_items[path] = item

            parent_item = None if parent_path is "" else find_item(parent_path, True)

            if parent_item is not None:
                parent_item.addChild(item)
            else:
                tree_view.addTopLevelItem(item)

            item.setExpanded(True)

            return item

        for i in influence_data:
            influence_items[i.path_name()] = find_item(i.path_name(), False)

        return influence_items

    def tolerance():
        result = NumberSliderGroup(min_value=0.001, max_value=10)
        result.spinner.setDecimals(3)

        @signal.on(reload_ui)
        def reload():
            with qt.signals_blocked(result):
                result.set_value(matcher.config.distance_threshold)

        @signal.on(result.valueChanged)
        def changed():
            matcher.config.distance_threshold = result.value()
            recalcMatches()

        reload()

        return result

    def pattern():
        result = QtWidgets.QTableWidget()
        result.setColumnCount(2)
        result.setHorizontalHeaderLabels(["Pattern", "Opposite"] if mirror_mode else ["Source", "Destination"])
        result.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)

        result.verticalHeader().setVisible(False)
        result.verticalHeader().setDefaultSectionSize(20)

        item_font = QtGui.QFont("Courier New", 12)
        item_font.setStyleHint(QtGui.QFont.Monospace)

        @signal.on(reload_ui)
        def reload_patterns():
            with qt.signals_blocked(result):
                result.setRowCount(len(matcher.config.globs) + 1)
                for rowIndex, patterns in enumerate(matcher.config.globs + [('', '')]):
                    for colIndex, p in enumerate(patterns):
                        item = QtWidgets.QTableWidgetItem(p)
                        item.setFont(item_font)
                        result.setItem(rowIndex, colIndex, item)

        reload_patterns()

        @signal.on(update_globs)
        def update_matcher_globs():
            globs = []

            def text(r, c):
                item = result.item(r, c)
                if item is None:
                    return ""
                return item.text().strip()

            for row in range(result.rowCount()):
                v1 = text(row, 0)
                v2 = text(row, 1)
                if v1 != "" and v2 != "":
                    globs.append((v1, v2))

            matcher.config.globs = globs
            recalcMatches()

        @qt.on(result.itemChanged)
        def item_changed(item):
            log.debug("item changed")
            item.setText(item.text().strip())

            try:
                influenceMapping.validate_glob(item.text().strip())
            except Exception as err:
                dialogs.displayError(str(err))
                item.setText(influenceMapping.illegalCharactersRegexp.sub("", item.text()))

            if item.row() != result.rowCount() - 1:
                if item.text().strip() == "":
                    result.removeRow(item.row())

            # ensure one empty line at the end
            rows = result.rowCount()
            last_item = result.item(rows - 1, 0)
            if last_item and last_item.text() != "":
                result.setRowCount(rows + 1)

            update_matcher_globs()

        return result

    def automaticRules():
        form = QtWidgets.QFormLayout()
        use_joint_names = QtWidgets.QCheckBox("Match by joint name")
        naming_patterns = pattern()
        use_position = QtWidgets.QCheckBox("Match by position")
        tolerance_scroll = tolerance()
        use_joint_labels = QtWidgets.QCheckBox("Match by joint label")
        use_dg_links = QtWidgets.QCheckBox("Match by dependency graph links")

        def update_enabled_disabled():
            def enable_form_row(form_item, e):
                form_item.setEnabled(e)
                form.labelForField(form_item).setEnabled(e)

            checked = use_joint_names.isChecked()
            enable_form_row(naming_patterns, checked)

            checked = use_position.isChecked()
            tolerance_scroll.set_enabled(checked)
            form.labelForField(tolerance_scroll.layout()).setEnabled(checked)

            enable_form_row(dg_attribute, use_dg_links.isChecked())

        @qt.on(use_joint_names.toggled, use_position.toggled, use_joint_labels.toggled, use_dg_links.toggled)
        def use_joint_names_toggled():
            update_enabled_disabled()
            matcher.config.use_name_matching = use_joint_names.isChecked()
            matcher.config.use_distance_matching = use_position.isChecked()
            matcher.config.use_label_matching = use_joint_labels.isChecked()
            matcher.config.use_dg_link_matching = use_dg_links.isChecked()
            recalcMatches()

        dg_attribute = QtWidgets.QLineEdit()

        @qt.on(dg_attribute.editingFinished)
        def use_joint_names_toggled():
            matcher.config.dg_destination_attribute = str(dg_attribute.text()).strip()
            recalcMatches()

        @signal.on(reload_ui)
        def update_values():
            with qt.signals_blocked(dg_attribute):
                dg_attribute.setText(matcher.config.dg_destination_attribute)
            with qt.signals_blocked(use_joint_names):
                use_joint_names.setChecked(matcher.config.use_name_matching)
            with qt.signals_blocked(use_position):
                use_position.setChecked(matcher.config.use_distance_matching)
            with qt.signals_blocked(use_joint_labels):
                use_joint_labels.setChecked(matcher.config.use_label_matching)
            with qt.signals_blocked(use_dg_links):
                use_dg_links.setChecked(matcher.config.use_dg_link_matching)
            update_enabled_disabled()

        g = QtWidgets.QGroupBox("Rules")
        g.setLayout(form)
        form.addRow(use_dg_links)
        form.addRow("Attribute name:", dg_attribute)
        form.addRow(use_joint_labels)
        form.addRow(use_joint_names)
        form.addRow("Naming scheme:", naming_patterns)
        form.addRow(use_position)
        form.addRow("Position tolerance:", tolerance_scroll.layout())

        update_values()
        return g

    def scriptedRules():
        g = QtWidgets.QGroupBox("Scripted rules")
        g.setLayout(QtWidgets.QVBoxLayout())
        g.layout().addWidget(QtWidgets.QLabel("TODO"))
        return g

    def manualRules():
        g = QtWidgets.QGroupBox("Manual overrides")
        g.setLayout(QtWidgets.QVBoxLayout())
        g.layout().addWidget(QtWidgets.QLabel("TODO"))
        return g

    leftSide = QtWidgets.QScrollArea()
    leftSide.setFrameShape(QtWidgets.QFrame.NoFrame)
    leftSide.setFocusPolicy(QtCore.Qt.NoFocus)
    leftSide.setWidgetResizable(True)

    l = QtWidgets.QVBoxLayout()
    l.setContentsMargins(0, 0, 0, 0)
    l.addWidget(automaticRules())
    # l.addWidget(scriptedRules())
    # l.addWidget(manualRules())
    # l.addStretch()

    leftSide.setWidget(qt.wrap_layout_into_widget(l))

    def createMappingView():
        view = QtWidgets.QTreeWidget()
        view.setColumnCount(3)
        view.setHeaderLabels(["Source", "Destination", "Matched by rule"])
        view.setIndentation(7)
        view.setExpandsOnDoubleClick(False)

        usedItems = build_tree_hierarchy(view)

        linkedItemRole = QtCore.Qt.UserRole + 1

        def previewMapping(mapping):
            """

            :type mapping: dict[InfluenceInfo, InfluenceInfo]
            """
            for treeItem in list(usedItems.values()):
                treeItem.setText(1, "(not matched)")
                treeItem.setText(2, "")

            for k, v in list(mapping.items()):
                treeItem = usedItems.get(k.path_name(), None)
                if treeItem is None:
                    continue
                treeItem.setText(1, "(self)" if k == v['infl'] else v["infl"].shortestPath)
                treeItem.setText(2, v["matchedRule"])
                treeItem.setData(1, linkedItemRole, v["infl"].path)

        @qt.on(view.itemDoubleClicked)
        def itemDoubleClicked(item, column):
            item.setExpanded(True)

            linkedItemPath = item.data(1, linkedItemRole)
            item = usedItems.get(linkedItemPath, None)
            if item is not None:
                item.setSelected(True)
                view.scrollToItem(item)

        return view, previewMapping

    def recalcMatches():
        matches = matcher.calculate()
        mappingView_updateMatches(matches)

    g = QtWidgets.QGroupBox("Calculated mapping")
    g.setLayout(QtWidgets.QVBoxLayout())
    mappingView, mappingView_updateMatches = createMappingView()
    g.layout().addWidget(mappingView)

    mainLayout = QtWidgets.QSplitter(orientation=QtCore.Qt.Horizontal, parent=parent)
    mainLayout.addWidget(leftSide)
    mainLayout.addWidget(g)

    mainLayout.setStretchFactor(0, 10)
    mainLayout.setStretchFactor(1, 10)
    mainLayout.setCollapsible(0, True)
    mainLayout.setSizes([200] * 2)

    return mainLayout, reload_ui.emit, recalcMatches
