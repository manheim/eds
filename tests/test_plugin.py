from eds.plugin import BasePlugin


class PluginChild(BasePlugin):
    pass


class PluginParent(BasePlugin):

    @property
    def children(self):
        return [PluginChild({})]


class PluginGrandParent(BasePlugin):

    @property
    def children(self):
        return [PluginParent({})]


def test_get_child_plugins():
    p = PluginGrandParent({})
    assert len(p.descendants) == 2
    assert type(p.descendants[0]).__name__ == 'PluginChild'
    assert type(p.descendants[1]).__name__ == 'PluginParent'


def test_id_property():
    p = PluginChild({'id': 'my_id'})
    assert p.id == 'my_id'


def test_yaml_property():
    p = PluginChild({'some': 'yaml'})
    assert p.yaml == {'some': 'yaml'}
