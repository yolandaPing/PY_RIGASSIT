# -*- coding: utf-8 -*-

# .FileName:translator.py
# .@Author : Yolanda Ping (You P)
# .@Email : yolandaping1224@gmail.com
# .Date....: 2026/3/26 23:41
# .Finish time:

import os
import json

_data = {}
_current_lang = "en"

BASE_DIR = os.path.dirname(__file__)
I18N_DIR = os.path.join(BASE_DIR, "i18n")


def load_language(lang):
    global _data, _current_lang

    path = os.path.join(I18N_DIR, "{}.json".format(lang))

    if not os.path.exists(path):
        _data = {}
        return

    with open(path, "r") as f:
        try:
            _data = json.load(f)
        except:
            _data = {}

    _current_lang = lang


def set_language(lang):
    load_language(lang)


def tr(key):
    return _data.get(key, key)