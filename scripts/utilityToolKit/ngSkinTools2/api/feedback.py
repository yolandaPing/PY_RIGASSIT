def display_error(message):
    from ngSkinTools2 import BATCH_MODE

    if BATCH_MODE:
        import sys

        sys.stdout.write(message + "\n")
    else:
        from ngSkinTools2.ui import dialogs

        dialogs.displayError(message)
