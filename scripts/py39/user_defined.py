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
