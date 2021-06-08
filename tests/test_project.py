from eds.event import Event
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

        }
    ]
}


def _get_eds_yaml(self):
    if self._url == '/child':
        return eds_yml_child
    elif self._url == '/parent':
        return eds_yml_parent
    elif self._url == '/grandparent':
        return eds_yml_grandparent


def test_includes(monkeypatch):
    monkeypatch.setattr(Event, '_get_eds_yaml', _get_eds_yaml)
    monkeypatch.setattr(project, 'get_plugin', lambda group, name: Plugin)
    event = Event(True, True, '/child', 'project', 'project==1.0')
    p = Project(event)
    assert len(p.plugins) == 3


def test_overridden(monkeypatch):
    monkeypatch.setattr(Event, '_get_eds_yaml', _get_eds_yaml)
    monkeypatch.setattr(project, 'get_plugin', lambda group, name: Plugin)
    event = Event(True, True, '/child', 'project', 'project==1.0')
    p = Project(event)
    assert len([plugin for plugin in p.plugins if plugin.overridden]) == 2


def test_property_inheritance(monkeypatch):
    monkeypatch.setattr(Event, '_get_eds_yaml', _get_eds_yaml)
    monkeypatch.setattr(project, 'get_plugin', lambda group, name: Plugin)
    event = Event(True, True, '/child', 'project', 'project==1.0')
    p = Project(event)
    assert len(p.plugins) == 3
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
