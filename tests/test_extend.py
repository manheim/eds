
import pkg_resources
import pytest

from eds.extend import _get_plugins, get_plugins, get_plugin
from eds.exception import (PluginNameNotFoundError, NoPluginsFoundError,
                           DuplicatePluginError, PluginNameMismatchError,
                           PluginNoNameAttributeError, PluginInterfaceNotImplementedError,
                           UnknownPluginIntefaceError)
from eds.interfaces.config import Config
from eds.interfaces.pipeline import Pipeline


class ConfigPlugin(Config):
    plugin_name = 'testname'


class PipelinePlugin(Pipeline):
    plugin_name = 'testname'


class ConfigPluginMismatch(Config):
    plugin_name = 'mismatch'


class ConfigPluginNoName(Config):
    pass


def patch_working_set(monkeypatch, plugin_class, no_ep=False, dupe=False):
    dist = pkg_resources.get_distribution('eds')
    if no_ep:
        monkeypatch.setattr(dist, 'get_entry_map', lambda group: {})
    else:
        ep = pkg_resources.EntryPoint.parse("testname = tests.test_extend:%s" % plugin_class, dist=dist)
        monkeypatch.setattr(dist, 'get_entry_map', lambda group: {'testname': ep})
    if dupe:
        dists = [dist, dist]
    else:
        dists = [dist]
    monkeypatch.setattr('eds.extend.pkg_resources.WorkingSet.__iter__', lambda self: iter(dists))


def test_get_plugin(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin')
    p = get_plugin('eds.config', 'testname')
    assert p.plugin_name == 'testname'


def test_get_plugins(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin')
    plugins = get_plugins('eds.config')
    assert len(plugins) == 1
    assert 'testname' in plugins
    assert plugins['testname'].plugin_name == 'testname'


def test_get_plugins_matching_project(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin')
    plugins = get_plugins('eds.config', project='eds')
    assert len(plugins) == 1
    assert 'testname' in plugins
    assert plugins['testname'].plugin_name == 'testname'


def test_get_plugins_non_matching_project(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin')
    with pytest.raises(NoPluginsFoundError):
        get_plugins('eds.config', project='foo')


def test__get_plugins_mismatch(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPluginMismatch')
    with pytest.raises(PluginNameMismatchError):
        _get_plugins('eds.config', name='testname')


def test__get_plugins_no_name_attr(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPluginNoName')
    with pytest.raises(PluginNoNameAttributeError):
        _get_plugins('eds.config', name='testname')


def test__get_plugins_name_not_found(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin', no_ep=True)
    with pytest.raises(PluginNameNotFoundError):
        _get_plugins('eds.config', name='testname')


def test__get_plugins_duplicates(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin', dupe=True)
    with pytest.raises(DuplicatePluginError):
        _get_plugins('eds.config', name='testname')


def test__get_plugins_no_plugins(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin', no_ep=True)
    with pytest.raises(NoPluginsFoundError):
        _get_plugins('eds.config')


def test__get_plugins_unknown_interface(monkeypatch):
    patch_working_set(monkeypatch, 'ConfigPlugin')
    with pytest.raises(UnknownPluginIntefaceError):
        _get_plugins('eds.unknown')


def test__get_plugins_interface_not_implemented(monkeypatch):
    patch_working_set(monkeypatch, 'PipelinePlugin')
    with pytest.raises(PluginInterfaceNotImplementedError):
        _get_plugins('eds.config')
