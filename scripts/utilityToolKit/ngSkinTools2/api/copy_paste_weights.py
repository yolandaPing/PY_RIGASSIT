from ngSkinTools2.api import plugin


def __clipboard_operation__(layer, influences, operation):
    influences = "" if influences is None else ','.join([str(i) for i in influences])
    plugin.ngst2Layers(layer.mesh, e=True, id=layer.id, clipboard=operation, paintTarget=influences)


def copy_weights(layer, influences):
    """
    :type layer: ngSkinTools2.api.layers.Layer
    :type influences: list
    """
    __clipboard_operation__(layer, influences, 'copy')


def cut_weights(layer, influences):
    """
    :type layer: ngSkinTools2.api.layers.Layer
    :type influences: list
    """
    __clipboard_operation__(layer, influences, 'cut')


class PasteOperation:
    replace = 'pasteReplace'
    add = 'pasteAdd'
    subtract = 'pasteSubtract'


def paste_weights(layer, operation=PasteOperation.replace, influences=None):
    """
    :type layer: ngSkinTools2.api.layers.Layer
    :param operation: one of paste_* constants
    :param influences: list of target influences
    """
    __clipboard_operation__(layer, influences, operation)
