from ngSkinTools2.api.python_compatibility import Object


def website_base_url():
    import ngSkinTools2

    if ngSkinTools2.DEBUG_MODE:
        return "http://localhost:1313"

    return "https://www.ngskintools.com"


class WebsiteLinksActions(Object):
    def __init__(self, parent):
        self.api_root = make_documentation_action(parent, "API Documentation", "/v2/api")
        self.user_guide = make_documentation_action(parent, "User Guide", "/v2/")
        self.changelog = make_documentation_action(parent, "Change Log", "/v2/changelog", icon=None)
        self.contact = make_documentation_action(parent, "Contact", "/contact/", icon=None)


def make_documentation_action(parent, title, url, icon=":/help.png"):
    from ngSkinTools2.ui import actions

    def handler():
        import webbrowser

        webbrowser.open_new(website_base_url() + url)

    result = actions.define_action(parent, title, callback=handler, icon=icon)
    result.setToolTip("opens {0} in a browser".format(url))
    return result
