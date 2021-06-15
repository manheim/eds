
from __future__ import annotations
import pkg_resources
from typing import Dict, Iterator

from eds.exception import (PluginNameNotFoundError, NoPluginsFoundError,
                           DuplicatePluginError, PluginNameMismatchError,
                           PluginNoNameAttributeError)
from eds.interfaces.plugin import Plugin


def _iter_entry_points(group: str, name: str = None, project: str = None) -> Iterator[Plugin]:
    """Yield entry point objects from `group` matching `name`, and `project`.

    Args:
        group (str): [description]
        name (str, optional): [description]. Defaults to None.
        project (str, optional): [description]. Defaults to None.

    Yields:
        Iterator[Plugin]: Iterator of plugins.
    """
    for dist in pkg_resources.working_set:
        if project and dist.project_name != project:
            continue
        entries = dist.get_entry_map(group)
        if name is None:
            for ep in entries.values():
                yield ep
        elif name in entries:
            yield entries[name]


def _get_plugins(group: str, name: str = None, project: str = None) -> Dict:
    """Return a dict of plugins.

    By name from a certain `group`, filtered by `name` and/or `project` if given.

    Args:
        group (str): Plugin group.
        name (str, optional): Plugin name. Defaults to None.
        project (str, optional): Project. Defaults to None.

    Raises:
        PluginNameMismatchError: When name doesn't match.
        PluginNoNameAttributeError: When there is no name attribute.
        DuplicatePluginError: When there are duplicate plugins.
        PluginNameNotFoundError: When no plugin with that name is found.
        NoPluginsFoundError: When no plugins are found.

    Returns:
        Dict: A dict of plugins by name.
    """
    plugins = {}
    for entry_point in _iter_entry_points(group, name=name, project=project):
        plugin = entry_point.load()
        if hasattr(plugin, 'plugin_name') and entry_point.name != plugin.plugin_name:
            raise PluginNameMismatchError(
                "name '%s' does not match plugin name '%s'" % (entry_point.name, plugin.plugin_name))
        elif not hasattr(plugin, 'plugin_name'):
            raise PluginNoNameAttributeError(
                "plugin %s has no 'plugin_name' attribute" % (entry_point.name))
        if plugin.plugin_name in plugins:
            raise DuplicatePluginError(
                "duplicate plugin '%s' found" % plugin.plugin_name)
        plugins[plugin.plugin_name] = plugin
    if name and not plugins:
        raise PluginNameNotFoundError(
            "no %s plugin found with name '%s'" % (group, name))
    elif not plugins:
        raise NoPluginsFoundError("no '%s' plugins found" % group)
    return plugins


def get_plugin(group: str, name: str) -> Plugin:
    """Return a single plugin by `group` and `name`.

    Args:
        group (str): Plugin group.
        name (str): Plugin name

    Returns:
        Plugin: The discovered plugin.
    """
    return _get_plugins(group, name)[name]


def get_plugins(group: str, project: str = None) -> Dict:
    """Return a dict of plugins by `group`, and optionally filtered by `project`.

    Args:
        group (str): Plugin group.
        project (str, optional): Project. Defaults to None.

    Returns:
        Dict: Dict of plugins.
    """
    return _get_plugins(group, project=project)
