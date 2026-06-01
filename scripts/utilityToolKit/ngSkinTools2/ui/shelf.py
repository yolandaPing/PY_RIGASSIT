from maya import cmds, mel


def install_shelf():
    """
    checks if there's ngSkintTools shelf installed, and if not, creates one.

    this runs each time Maya starts (via Autoloader's ngSkinTools_load.mel) - avoid duplication, like creating things
    that already exist.
    """

    # don't do anything if we're in batch mode. UI commands are not available
    if cmds.about(batch=True) == 1:
        return

    maya_shelf = mel.eval("$tempngSkinTools2Var=$gShelfTopLevel")
    existing_shelves = cmds.shelfTabLayout(maya_shelf, q=True, tabLabel=True)

    parent_shelf = 'ngSkinTools2'

    if parent_shelf in existing_shelves:
        return

    mel.eval('addNewShelfTab ' + parent_shelf)
    cmds.shelfButton(
        parent=parent_shelf,
        enable=1,
        visible=1,
        preventOverride=0,
        label="ngst",
        annotation="opens ngSkinTools2 UI",
        image="ngSkinTools2ShelfIcon.png",
        style="iconOnly",
        noBackground=1,
        align="center",
        marginWidth=1,
        marginHeight=1,
        command="import ngSkinTools2; ngSkinTools2.open_ui()",
        sourceType="python",
        commandRepeatable=0,
    )
