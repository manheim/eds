from eds.event import Event


def test_eds_built_property():
    e = Event(True, False, 'url', 'project_name', 'project_version')
    assert e.eds_built
    e = Event(False, True, 'url', 'project_name', 'project_version')
    assert not e.eds_built


def test_eds_plugins_built_property():
    e = Event(False, True, 'url', 'project_name', 'project_version')
    assert e.eds_plugins_built
    e = Event(True, False, 'url', 'project_name', 'project_version')
    assert not e.eds_plugins_built


def test_url_property():
    e = Event(False, True, 'url', 'project_name', 'project_version')
    assert e.url == 'url'


def test_project_name_property():
    e = Event(False, True, 'url', 'project_name', 'project_version')
    assert e.project_name == 'project_name'


def test_project_version_property():
    e = Event(False, True, 'url', 'project_name', 'project_version')
    assert e.project_version == 'project_version'
