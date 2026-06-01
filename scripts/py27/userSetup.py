# -*- coding: utf-8 -*-
import inspect,os
import sys
import json
import traceback
import maya.cmds as cmds

def get_current_dir():
    return os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )

def get_script_path():
    try:
        return os.path.abspath(__file__)
    except:
        pass
    try:
        return os.path.abspath(sys.modules[__name__].__file__)
    except:
        pass
    return cmds.internalVar(userScriptDir=True)


THIS_DIR = get_current_dir()
ROOT_DIR = os.path.dirname(THIS_DIR)
CONFIG_FILE = os.path.join(ROOT_DIR, "user_defined.json")


def log(msg):
    try:
        print("[PY_RIGASSIT] {}".format(msg))
    except:
        pass


def default_config():
    return {
        "hotkey": False,
        "hotBox": False,
        "shelfButton_New": True,    
        "Allow_users": True,
        "Allow_smooth": True,
        "Grp_prisec": False,

        "suffix": "bind",

        "Chinese": True,

        "CopyTools_UI_new": True,
        "Optional_Drive_UI_new": True,

        "Blendshape_Editor_User": False,
        "Dirve_Pose_Mirror": False,
        "MotionPath_Enable": False,

        "prefix_map": {
            "l_": "r_",
            "r_": "l_",
            "L_": "R_",
            "R_": "L_"
        },

        "suffix_map": {
            "_L": "_R",
            "_R": "_L"
        },

        "infix_map": {
            "_l_": "_r_",
            "_r_": "_l_",
            "_L_": "_R_",
            "_R_": "_L_"
        }
    }


def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except:
        log("Save config failed")


def load_config():

    defaults = default_config()

    if not os.path.exists(CONFIG_FILE):
        save_config(defaults)
        return defaults

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        # 自动补字段
        changed = False

        for k, v in defaults.items():
            if k not in data:
                data[k] = v
                changed = True

        if changed:
            save_config(data)

        return data

    except:
        log("Config broken, rebuild default")
        save_config(defaults)
        return defaults


def run_deferred(code):
    try:
        cmds.evalDeferred(code)
    except:
        log("evalDeferred failed")


def load_shelf():
    try:
        run_deferred("import ShelfButton")
        log("Shelf loaded")
    except:
        traceback.print_exc()


def load_hotkey():
    try:
        run_deferred(
            'import CommonUse.yolanda_p_setHotKey as YHK\n'
            'YHK.setHotkey()'
        )
        log("Hotkey loaded")
    except:
        traceback.print_exc()


def load_hotbox():
    try:
        run_deferred(
            'import CommonUse.yolanda_p_setHotKey.hotBox as HB\n'
            'HB.start()'
        )
        log("HotBox loaded")
    except:
        traceback.print_exc()


def startup():

    cfg = load_config()

    print("CONFIG FILE =", CONFIG_FILE)
    print("CONFIG DATA =", cfg)

    load_shelf()

    if bool(cfg.get("hotkey", False)) is True:
        print("LOAD HOTKEY")
        load_hotkey()
    else:
        print("HOTKEY OFF")

    if bool(cfg.get("hotBox", False)) is True:
        load_hotbox()


startup()

# cmds.evalDeferred('import ShelfButton')
# cmds.evalDeferred("import CommonUse.yolanda_p_setHotKey as YHK\nYHK.setHotkey()")