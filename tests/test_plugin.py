from eds.plugin import Plugin


class PluginChild(Plugin):
    pass


class PluginParent(Plugin):

    def get_child_plugins(self):
        return [PluginChild({})]


class PluginGrandParent(Plugin):

    def get_child_plugins(self):
        return [PluginParent({})]


def test_get_child_plugins():
    p = PluginGrandParent({})
    assert len(p.child_plugins) == 2
    assert type(p.child_plugins[0]).__name__ == 'PluginChild'
    assert type(p.child_plugins[1]).__name__ == 'PluginParent'
