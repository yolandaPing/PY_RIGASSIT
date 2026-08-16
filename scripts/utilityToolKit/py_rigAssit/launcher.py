# -*- coding: utf-8 -*-

from py_rigAssit.dialogs.manager import show


def _reload(mod):
    try:
        import importlib
        importlib.reload(mod)
    except Exception:
        reload(mod)


def launch():

    from py_rigAssit.dialogs.joint_mod_layout import PYJointEditLayout
    from py_rigAssit.dialogs.batch_copys_dlg import PYCopyToolsLayout
    from py_rigAssit.dialogs.controller_editor_dlg import PYControllerEditorLayout
    from py_rigAssit.dialogs.optional_driver_dlg import PYOptionalDriveLayout
    from py_rigAssit.dialogs.general_mod import PYGeneralLayout
    from py_rigAssit.dialogs.custom_mod import PYCustomLayout

    copy_instance = PYCopyToolsLayout()
    joint_instance = PYJointEditLayout()
    ctrl_instance = PYControllerEditorLayout()
    drive_instance = PYOptionalDriveLayout()
    general_instance = PYGeneralLayout()
    custom_instance = PYCustomLayout()

    tabs = ('Rigging', 'Ctrl', 'Copy', 'Driver', 'General', 'Custom')

    instances_ui = {
        "Rigging": joint_instance.init_ui,
        "Ctrl": ctrl_instance.init_ui,
        "Copy": copy_instance.init_ui,
        "Driver": drive_instance.init_ui,
        "General": general_instance.init_ui,
        "Custom": custom_instance.init_ui,
    }

    dialog_data = {
        'UI_NAME': "PY_RIGASSIT",
        'WITHHIGHT': [380, 800],
        'INIT_UI': instances_ui,
        'TABS': tabs,
        'TIME_STAMP': "2022-2026"
    }

    return show(dialog_data)


if __name__ == '__main__':
    launch()