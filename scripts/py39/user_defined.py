<<<<<<< HEAD
# -*- coding: utf-8 -*-

# .FileName:user_defined.py
# .Date....:2024-04-25 : 22 :43
# .@Author:You P
# .
# .Finish time:
import inspect,os,json

def get_current_dir():
    return os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )


# THIS_DIR = os.path.dirname(os.path.abspath(__file__))
THIS_DIR = get_current_dir()
ROOT_DIR = os.path.dirname(THIS_DIR)

JSON_FILE = os.path.join(ROOT_DIR, "user_defined.json")
USER_SETUP = os.path.join(ROOT_DIR, "userSetup.py")

HOTKEY_LINE = 'cmds.evalDeferred("import CommonUse.yolanda_p_setHotKey as YHK\\nYHK.setHotkey()")'
HOTKEY_OFF = '#PY_RIGASSIT hotkey are not enabled'


def load_json():
    if not os.path.exists(JSON_FILE):
        return {}

    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_json(data):
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except:
        return False


def update_userSetup_hotkey(enable=True):

    if not os.path.exists(USER_SETUP):
        return

    try:
        with open(USER_SETUP, "r") as f:
            txt = f.read()

        if enable:
            txt = txt.replace(HOTKEY_OFF, HOTKEY_LINE)
        else:
            txt = txt.replace(HOTKEY_LINE, HOTKEY_OFF)

        with open(USER_SETUP, "w") as f:
            f.write(txt)

    except Exception as e:
        print(e)


def set_value(key, value):

    data = load_json()
    data[key] = value
    save_json(data)

    if key == "hotkey":
        update_userSetup_hotkey(value)


_data = load_json()

# 配置读取
# -------------------
hotkey = _data.get("hotkey", True)
hotBox = _data.get("hotBox", False)

shelfButton_New = _data.get("shelfButton_New", True)

Allow_users = _data.get("Allow_users", True)
Allow_smooth = _data.get("Allow_smooth", True)

Grp_prisec = _data.get("Grp_prisec", False)

suffix = _data.get("suffix", "bind")

Chinese = _data.get("Chinese", True)

MotionPath_Enable = _data.get("MotionPath_Enable", False)

prefix_map = _data.get("prefix_map", {})
suffix_map = _data.get("suffix_map", {})
infix_map = _data.get("infix_map", {})
=======
# -*- coding: utf-8 -*-

# .FileName:user-defined
# .Date....:2024-04-25 : 22 :43
# .@Author:You P
# .
# .Finish time:
import sys
import saveRootPath as Root

Path = sys.path.append(Root.ParentPath)
if Path not in sys.path:
    sys.path.append(Path)

import scripts.user_defined as user

# import hotKey
hotkey = user.hotkey

# Allow_users: enable smooth copy weight
Allow_users = user.Allow_users

# Allow_users: enable smooth copy weight
Allow_smooth = user.Allow_smooth

# Grp_prisec: add ctrl sec and pri group
Grp_prisec = user.Grp_prisec

#rename tool suffix
suffix = user.suffix

# enable Chinese
Chinese = user.Chinese

# copy tool ui
CopyTools_UI_new = user.CopyTools_UI_new

# optional drive tool ui
Optional_Drive_UI_new = user.Optional_Drive_UI_new

# blendshape Editor designated users use blendshape
Blendshape_Editor_User = user.Blendshape_Editor_User

# dirve pose tool: enable mirror
Dirve_Pose_Mirror = user.Dirve_Pose_Mirror
>>>>>>> 8215c5ba5fbffb8c5cc2357c9b7672c93ec3dee5
