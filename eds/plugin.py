import pkg_resources

from eds.exception import (PluginNameNotFoundError, NoPluginsFoundError,
                           DuplicatePluginError, PluginNameMismatchError,
                           PluginNoNameAttributeError)


def _iter_entry_points(group, name=None, project=None):
    """Yield entry point objects from `group` matching `name`, and `project`"""
    for dist in pkg_resources.working_set:
        if project and dist.project_name != project:
            continue
        entries = dist.get_entry_map(group)
        if name is None:
            for ep in entries.values():
                yield ep
        elif name in entries:
            yield entries[name]


def _get_plugins(group, name=None, project=None):
    """Return a dict of plugins by name from a certain `group`, filtered by `name`
    and/or `project` if given.

    :param group: plugin group
    :param name: plugin name
    :param project: project name

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


def get_plugin(group, name):
    """Return a single plugin by `group` and `name`

    :param group: plugin group
    :param name: plugin name
    """
    return _get_plugins(group, name)[name]


def get_plugins(group, project=None):
    """Return a dict of plugins by `group`, and optionally filtered by `project`

    :param group: plugin group
    :param project: project name
    """
    return _get_plugins(group, project=project)
