# -*- coding: utf-8 -*-

# .FileName:file_operations.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/6/30 20:23
# .Finish time:

import os
import maya.cmds as cmds

try:
    FileNotFoundError
except NameError:
    class FileNotFoundError(IOError):
        pass


def normalize_path(path):
    if not path:
        return path
    path = path.replace("\\", "/")
    while path.endswith("/") and len(path) > 1:
        path = path[:-1]
    return path


def get_maya_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".ma":
        return "mayaAscii"
    elif ext == ".mb":
        return "mayaBinary"
    return None


def clear_scene():
    cmds.file(new=True, force=True)


def _validate_file(file_path):
    file_path = normalize_path(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found: {}".format(file_path))

    return file_path


def _maya_file_operation(file_path, mode="open", **kwargs):
    """
    mode:
        open
        import
        reference
    """
    file_path = _validate_file(file_path)

    file_type = get_maya_file_type(file_path)

    args = {
        "type": file_type,
        "options": "v=0;"
    }

    args.update(kwargs)

    if mode == "open":
        args["open"] = True
        args["force"] = True

    elif mode == "import":
        args["i"] = True

    elif mode == "reference":
        args["r"] = True
        args.setdefault("ignoreVersion", True)

    else:
        raise RuntimeError("Unknown mode: {}".format(mode))

    cmds.file(file_path, **args)
    return True


def open_file(file_path, force_new=True):
    if force_new:
        clear_scene()

    return _maya_file_operation(file_path, mode="open")


def import_file(file_path,
                namespace=None,
                preserve_references=True,
                group=False):
    kwargs = {
        "preserveReferences": preserve_references,
        "groupReference": group
    }

    if namespace:
        kwargs["namespace"] = namespace

    return _maya_file_operation(file_path, mode="import", **kwargs)


def reference_file(file_path,
                   namespace=None,
                   group_locator=True,
                   merge_namespaces=False,
                   shared=False):
    kwargs = {
        "gl": group_locator,
        "mergeNamespacesOnClash": merge_namespaces
    }

    if namespace:
        kwargs["namespace"] = namespace

    if shared:
        kwargs["sharedReference"] = True

    return _maya_file_operation(file_path, mode="reference", **kwargs)


def save_scene_as(file_path):
    file_path = normalize_path(file_path)
    file_type = get_maya_file_type(file_path)

    cmds.file(rename=file_path)
    cmds.file(save=True, type=file_type)
    return True


def save_workshop(file_path=None, notes=None,
                  pm=None,
                  asset_type=None,
                  asset=None,
                  subtype=None):
    if pm and asset_type and asset and subtype:
        return pm.save_version(
            asset_type,
            asset,
            subtype,
            notes=notes
        )

    if not file_path:
        raise RuntimeError("file_path required")

    return save_scene_as(file_path)


def save_master(file_path=None,
                pm=None,
                asset_type=None,
                asset=None,
                subtype=None):
    if pm and asset_type and asset and subtype:
        return pm.save_master(asset_type, asset, subtype)

    if not file_path:
        raise RuntimeError("file_path required")

    return save_scene_as(file_path)


def set_master_from_version(pm, asset_type, asset, subtype, version_filename):
    return pm.set_master(asset_type, asset, subtype, version_filename)


def _get_workshop_file(pm, asset_type, asset, subtype, version_filename):
    asset_dir = pm.get_asset_dir(asset_type, asset)
    workshop_dir = os.path.join(
        asset_dir,
        "components",
        subtype,
        "workshop"
    )

    file_path = os.path.join(workshop_dir, version_filename)
    file_path = normalize_path(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    return file_path


def open_latest_or_selected_version(pm,
                                    asset_type,
                                    asset,
                                    subtype,
                                    version_filename=None):
    if version_filename:
        path = _get_workshop_file(
            pm, asset_type, asset, subtype, version_filename
        )
    else:
        path = pm.get_latest_workshop(
            asset_type,
            asset,
            subtype
        )

        if not path:
            raise RuntimeError("No version found")

    return open_file(path)


def open_master_file(pm, asset_type, asset, subtype):
    mf = pm.get_master_file(asset_type, asset, subtype)

    if not mf or not os.path.exists(mf):
        raise FileNotFoundError("Master file not found")

    return open_file(mf)


def import_master_file(pm, asset_type, asset, subtype, namespace=None):
    mf = pm.get_master_file(asset_type, asset, subtype)

    if not mf:
        raise FileNotFoundError("Master file not found")

    return import_file(mf, namespace=namespace)


def reference_master_file(pm, asset_type, asset, subtype, namespace=None):
    mf = pm.get_master_file(asset_type, asset, subtype)

    if not mf:
        raise FileNotFoundError("Master file not found")

    return reference_file(mf, namespace=namespace)


def write_note_info(pm, task_dir, version_filename, info="", workshop=True):
        pm.write_note_info(task_dir, version_filename, info, workshop=workshop)