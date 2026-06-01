MAYA_2018 = 20180000
MAYA_2019 = 20190000
MAYA_2020 = 20200000
MAYA_2021 = 20210000


def at_least(version):
    from maya import cmds

    return cmds.about(api=True) >= version
