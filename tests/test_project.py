from eds.event import Event
from eds.project import Project

eds_yml_grandparent = {
    'include': [],
    'plugins': [
        {
            'id': 'yo',
            'type': 'Yo',
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
            'type': 'Yo',
            'version': 'yo==1.0',
            'parent': {
                'url': '/grandparent',
                'plugin_id': 'yo'
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
            'type': 'Yo',
            'version': 'yo==1.0',
            'parent': {
                'url': '/parent',
                'plugin_id': 'yo'
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
    event = Event(True, True, '/child', 'project', 'project==1.0')
    p = Project(event)
    assert len(p._get_plugins()) == 3


def test_overridden(monkeypatch):
    monkeypatch.setattr(Event, '_get_eds_yaml', _get_eds_yaml)
    event = Event(True, True, '/child', 'project', 'project==1.0')
    p = Project(event)
    p._get_plugins()
    assert len([plugin for plugin in p.plugins if plugin.overridden]) == 2


def test_property_inheritance(monkeypatch):
    monkeypatch.setattr(Event, '_get_eds_yaml', _get_eds_yaml)
    event = Event(True, True, '/child', 'project', 'project==1.0')
    p = Project(event)
    assert len(p._get_plugins()) == 3
    assert p._get_plugins()[0].yaml['properties'] == {
        'p1': 'grandparent',
        'p2': 'grandparent'
    }
    assert p._get_plugins()[1].yaml['properties'] == {
        'p1': 'parent',
        'p2': 'grandparent',
        'p4': 'parent',
        'p5': 'parent'
    }
    assert p._get_plugins()[2].yaml['properties'] == {
        'p1': 'child',
        'p2': 'grandparent',
        'p4': 'child',
        'p5': 'parent',
        'p6': 'child'
    }
