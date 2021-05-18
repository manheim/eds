
import pkg_resources
import pytest

from eds.plugin import _get_plugins, get_plugins, get_plugin
from eds.exception import (PluginNameNotFoundError, NoPluginsFoundError,
                           DuplicatePluginError, PluginNameMismatchError,
                           PluginNoNameAttributeError)


class PluginClass(object):
    plugin_name = 'testname'


class PluginClassMismatch(object):
    plugin_name = 'mismatch'


class PluginClassNoName(object):
    pass


def patch_working_set(monkeypatch, plugin_class, no_ep=False, dupe=False):
    dist = pkg_resources.get_distribution('eds')
    if no_ep:
        monkeypatch.setattr(dist, 'get_entry_map', lambda group: {})
    else:
        ep = pkg_resources.EntryPoint.parse("testname = tests.test_plugin:%s" % plugin_class, dist=dist)
        monkeypatch.setattr(dist, 'get_entry_map', lambda group: {'testname': ep})
    if dupe:
        dists = [dist, dist]
    else:
        dists = [dist]
    monkeypatch.setattr('eds.plugin.pkg_resources.WorkingSet.__iter__', lambda self: iter(dists))


def test_get_plugin(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClass')
    p = get_plugin('foo', 'testname')
    assert p.plugin_name == 'testname'


def test_get_plugins(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClass')
    plugins = get_plugins('foo')
    assert len(plugins) == 1
    assert 'testname' in plugins
    assert plugins['testname'].plugin_name == 'testname'


def test_get_plugins_matching_project(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClass')
    plugins = get_plugins('foo', project='eds')
    assert len(plugins) == 1
    assert 'testname' in plugins
    assert plugins['testname'].plugin_name == 'testname'


def test_get_plugins_non_matching_project(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClass')
    with pytest.raises(NoPluginsFoundError):
        get_plugins('foo', project='foo')


def test__get_plugins_mismatch(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClassMismatch')
    with pytest.raises(PluginNameMismatchError):
        _get_plugins('foo', name='testname')


def test__get_plugins_no_name_attr(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClassNoName')
    with pytest.raises(PluginNoNameAttributeError):
        _get_plugins('foo', name='testname')


def test__get_plugins_name_not_found(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClass', no_ep=True)
    with pytest.raises(PluginNameNotFoundError):
        _get_plugins('foo', name='testname')


def test__get_plugins_duplicates(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClass', dupe=True)
    with pytest.raises(DuplicatePluginError):
        _get_plugins('foo', name='testname')


def test__get_plugins_no_plugins(monkeypatch):
    patch_working_set(monkeypatch, 'PluginClass', no_ep=True)
    with pytest.raises(NoPluginsFoundError):
        _get_plugins('foo')
