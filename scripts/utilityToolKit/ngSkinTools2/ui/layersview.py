from ngSkinTools2 import api, signal
from ngSkinTools2.api import python_compatibility
from ngSkinTools2.api.log import getLogger
from ngSkinTools2.api.pyside import QtCore, QtWidgets
from ngSkinTools2.api.session import session
from ngSkinTools2.ui import qt
from ngSkinTools2.ui.layout import scale_multiplier

if python_compatibility.PY3:
    from typing import Union


log = getLogger("layersView")


def build_view(parent, actions):
    from ngSkinTools2.operations import layers

    layer_icon_size = 20
    visibility_icon_size = 13

    icon_layer = qt.scaled_icon(":/layeredTexture.svg", layer_icon_size, layer_icon_size)
    icon_layer_disabled = qt.scaled_icon(":/layerEditor.png", layer_icon_size, layer_icon_size)
    icon_visible = qt.scaled_icon("eye-fill.svg", visibility_icon_size, visibility_icon_size)
    icon_hidden = qt.scaled_icon("eye-slash-fill.svg", visibility_icon_size, visibility_icon_size)

    layer_data_role = QtCore.Qt.UserRole + 1

    def item_to_layer(item):
        # type: (QtWidgets.QTreeWidgetItem) -> Union[api.Layer, None]
        if item is None:
            return None
        return item.data(0, layer_data_role)

    # noinspection PyShadowingNames
    def sync_layer_parents_to_widget_items(view):
        """
        after drag/drop tree reordering, just brute-force check
        that rearranged items match layers parents
        :return:
        """

        def sync_item(tree_item, parent_layer_id):
            for i in range(tree_item.childCount()):
                child = tree_item.child(i)
                rebuild_buttons(child)

                child_layer = item_to_layer(child)

                if child_layer.parent_id != parent_layer_id:
                    log.info("changing layer parent: %r->%r (was %r)", parent_layer_id, child_layer, child_layer.parent_id)
                    child_layer.parent = parent_layer_id

                new_index = tree_item.childCount() - i - 1
                if child_layer.index != new_index:
                    log.info("changing layer index: %r->%r (was %r)", child_layer, new_index, child_layer.index)
                    child_layer.index = new_index

                sync_item(child, child_layer.id)

        with qt.signals_blocked(view):
            sync_item(view.invisibleRootItem(), None)

    # noinspection PyPep8Naming
    class LayersWidget(QtWidgets.QTreeWidget):
        def dropEvent(self, event):
            QtWidgets.QTreeWidget.dropEvent(self, event)
            sync_layer_parents_to_widget_items(self)

    view = LayersWidget(parent)
    view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
    view.setUniformRowHeights(True)
    view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    # enable drag/drop
    view.setDragEnabled(True)
    view.viewport().setAcceptDrops(True)
    view.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
    view.setDropIndicatorShown(True)

    # add context menu
    view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
    actions.addLayersActions(view)

    view.setHeaderLabels(["Layers", ""])
    # view.setHeaderHidden(True)
    view.header().setMinimumSectionSize(1)
    view.header().setStretchLastSection(False)
    view.header().swapSections(0, 1)
    view.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    view.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
    view.setColumnWidth(1, 25 * scale_multiplier)
    view.setIndentation(15 * scale_multiplier)
    view.setIconSize(QtCore.QSize(layer_icon_size * scale_multiplier, layer_icon_size * scale_multiplier))

    tree_items = {}

    def rebuild_buttons(item):
        layer = item_to_layer(item)
        bar = QtWidgets.QToolBar(parent=parent)
        bar.setMovable(False)
        bar.setIconSize(QtCore.QSize(visibility_icon_size * scale_multiplier, visibility_icon_size * scale_multiplier))
        a = bar.addAction(icon_visible if layer is None or layer.enabled else icon_hidden, "Toggle enabled/disabled")

        @qt.on(a.triggered)
        def handler():
            layer.enabled = not layer.enabled
            session.events.layerListChanged.emitIfChanged()

        view.setItemWidget(item, 1, bar)

    def build_items(layer_infos):
        """
        sync items in view with provided layer values, trying to delete as little items on the view as possible
        :type layer_infos: list[api.Layer]
        """

        # build map "parent id->list of children "

        log.info("syncing items...")

        # save selected layers IDs to restore item selection later
        selected_layer_ids = {item_to_layer(item).id for item in view.selectedItems()}
        log.info("selected layer IDs: %r", selected_layer_ids)
        current_item_id = None if view.currentItem() is None else item_to_layer(view.currentItem()).id

        hierarchy = {}
        for child in layer_infos:
            if child.parent_id not in hierarchy:
                hierarchy[child.parent_id] = []
            hierarchy[child.parent_id].append(child)

        def sync(parent_tree_item, children_list):
            while parent_tree_item.childCount() > len(children_list):
                parent_tree_item.removeChild(parent_tree_item.child(len(children_list)))

            for index, child in enumerate(reversed(children_list)):
                if index >= parent_tree_item.childCount():
                    item = QtWidgets.QTreeWidgetItem()
                    item.setSizeHint(1, QtCore.QSize(1 * scale_multiplier, 25 * scale_multiplier))
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    parent_tree_item.addChild(item)
                else:
                    item = parent_tree_item.child(index)

                tree_items[child.id] = item

                item.setData(0, layer_data_role, child)
                item.setText(0, child.name)
                item.setIcon(0, icon_layer if child.enabled else icon_layer_disabled)
                rebuild_buttons(item)

                sync(item, hierarchy.get(child.id, []))

        with qt.signals_blocked(view):
            tree_items.clear()
            sync(view.invisibleRootItem(), hierarchy.get(None, []))

            current_item = tree_items.get(current_item_id, None)
            if current_item is not None:
                view.setCurrentItem(current_item, 0, QtCore.QItemSelectionModel.NoUpdate)

            for i in selected_layer_ids:
                item = tree_items.get(i, None)
                if item is not None:
                    item.setSelected(True)

    @signal.on(session.events.layerListChanged, qtParent=view)
    def refresh_layer_list():
        log.info("event handler for layer list changed")
        if not session.state.layersAvailable:
            build_items([])
        else:
            build_items(session.state.all_layers)

        update_selected_items()

    @signal.on(session.events.currentLayerChanged, qtParent=view)
    def current_layer_changed():
        log.info("event handler for currentLayerChanged")
        layer = session.state.currentLayer.layer
        current_item = view.currentItem()
        if layer is None:
            view.setCurrentItem(None)
            return

        prev_layer = None if current_item is None else item_to_layer(current_item)

        if prev_layer is None or prev_layer.id != layer.id:
            item = tree_items.get(layer.id, None)
            if item is not None:
                log.info("setting current item to " + item.text(0))
                view.setCurrentItem(item, 0, QtCore.QItemSelectionModel.SelectCurrent | QtCore.QItemSelectionModel.ClearAndSelect)

                item.setSelected(True)

    @qt.on(view.currentItemChanged)
    def current_item_changed(curr, _):
        log.info("current item changed")
        if curr is None:
            return

        selected_layer = item_to_layer(curr)

        if layers.getCurrentLayer() == selected_layer:
            return

        layers.setCurrentLayer(selected_layer)

    @qt.on(view.itemChanged)
    def item_changed(item, column):
        log.info("item changed")
        layers.renameLayer(item_to_layer(item), item.text(column))

    @qt.on(view.itemSelectionChanged)
    def update_selected_items():
        selection = [item_to_layer(item) for item in view.selectedItems()]

        if selection != session.context.selected_layers(default=[]):
            log.info("new selected layers: %r", selection)
            session.context.selected_layers.set(selection)

    refresh_layer_list()

    return view
