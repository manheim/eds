import pytest
from eds.event import Event
from eds.exception import DuplicateIncludeError
from eds import project
from eds.plugin import Plugin
from eds.project import Project


eds_yml_grandparent = {
    'include': [],
    'plugins': [
        {
            'id': 'yo',
            'name': 'Foo',
            'type': 'Bar',
            'version': 'yo==1.0',
            'properties': {
                'p1': 'grandparent',
                'p2': 'grandparent'
            }

        }
    ]
}

eds_yml_parent = {
    'include': [
        '/grandparent'
    ],
    'plugins': [
        {
            'id': 'yo',
            'name': 'Foo',
            'type': 'Bar',
            'version': 'yo==1.0',
            'parent': {
                'url': '/grandparent',
                'id': 'yo'
            },
            'properties': {
                'p1': 'parent',
                'p4': 'parent',
                'p5': 'parent'
            }

        }
    ]
}

eds_yml_child = {
    'include': [
        '/parent'
    ],
    'plugins': [
        {
            'id': 'yo',
            'name': 'Foo',
            'type': 'Bar',
            'version': 'yo==1.0',
            'parent': {
                'url': '/parent',
                'id': 'yo'
            },
            'properties': {
                'p1': 'child',
                'p4': 'child',
                'p6': 'child',
            }

        },
        {
            'id': 'go',
            'name': 'Too',
            'type': 'eds.pipeline',
            'version': 'go==1.0',
            'properties': {}
        }
    ]
}


def _setup(monkeypatch):
    monkeypatch.setattr(Event, '_get_eds_yaml', _get_eds_yaml)
    monkeypatch.setattr(project, 'get_plugin', lambda group, name: Plugin)
    event = Event(True, True, '/child', 'project', 'project==1.0')
    return Project(event)


def _get_eds_yaml(self):
    if self._url == '/child':
        return eds_yml_child
    elif self._url == '/parent':
        return eds_yml_parent
    elif self._url == '/grandparent':
        return eds_yml_grandparent


def test_includes(monkeypatch):
    p = _setup(monkeypatch)
    assert len(p.plugins) == 4


def test_overridden(monkeypatch):
    p = _setup(monkeypatch)
    assert len([plugin for plugin in p.plugins if plugin.overridden]) == 2


def test_property_inheritance(monkeypatch):
    p = _setup(monkeypatch)
    assert len(p.plugins) == 4
    assert p.plugins[0].yaml['properties'] == {
        'p1': 'grandparent',
        'p2': 'grandparent'
    }
    assert p.plugins[1].yaml['properties'] == {
        'p1': 'parent',
        'p2': 'grandparent',
        'p4': 'parent',
        'p5': 'parent'
    }
    assert p.plugins[2].yaml['properties'] == {
        'p1': 'child',
        'p2': 'grandparent',
        'p4': 'child',
        'p5': 'parent',
        'p6': 'child'
    }


def test_plugins_property(monkeypatch):
    p = _setup(monkeypatch)
    for plugin in p.plugins:
        assert type(plugin).__name__ == 'Plugin'


def test_plugin_versions_property(monkeypatch):
    p = _setup(monkeypatch)
    assert p.plugin_versions == ['yo==1.0', 'go==1.0']


def test_pipelines_property(monkeypatch):
    p = _setup(monkeypatch)
    assert len(p.pipelines) == 1
    assert p.pipelines[0].yaml['name'] == 'Too'


def test_duplicate_include():
    event = Event(True, True, '/child', 'project', 'project==1.0')
    with pytest.raises(DuplicateIncludeError):
        return Project(event, {'/child': ''})
