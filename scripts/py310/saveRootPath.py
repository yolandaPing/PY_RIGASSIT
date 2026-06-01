# -*- coding: utf-8 -*-

# .FileName:saveRootPath
# .Date....:2023-01-09 : 16 :37
# .@Author:You P
# .
# .Finish time:


import os


ParentPath = os.path.split(__file__)[0].split('scripts')[0]
ScriptsPath = os.path.split(__file__)[0].split(' ')[0]
IconsPath = ParentPath+"icons"
CurveDataPath = ParentPath+"files/CurveData"

# print(os.path.dirname(__file__).split('scripts')[0], '')
# print(os.path.join(os.path.dirname(__file__), ''))

# print(ParentPath,ScriptsPath,IconsPath,CurveDataPath)