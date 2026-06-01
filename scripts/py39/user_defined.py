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