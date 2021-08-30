
from __future__ import annotations
from copy import deepcopy
from typing import Dict, List

from eds.event import Event
from eds.extend import get_plugin, is_installed
from eds.exception import DuplicateIncludeError
from eds.interfaces.plugin import Plugin
from eds.interfaces.pipeline import Pipeline
from eds.plugin import BasePlugin


EDS_YML_FILE: str = 'eds.yml'


class Project:
    """A project containing an 'eds.yml' file."""

    schema: Dict = {}
    """json schema for eds.yml"""

    def __init__(self, event: Event, lookup: Dict = None):
        """Project constructor.

        Args:
            event (Event): Commit event for the project.
            lookup (Dict, optional): Lookup dict for discovered plugins. Defaults to None.

        Raises:
            DuplicateIncludeError: If an 'eds.yml' file is included more than once.
        """
        self._event = event
        self._yaml = event.eds_yaml
        self._plugins = []
        self._lookup = lookup if lookup is not None else {}
        self._validate_schema()
        if self._event.url in self._lookup:
            raise DuplicateIncludeError("%s has already been included" % self._event.url)
        self._lookup[self._event.url] = {}
        self._discover_plugins()
        [self._apply_inheritance(p) for p in self._plugins]

    def _validate_schema(self) -> None:
        """Validate 'self._yaml' using schema in `Project.schema`."""
        pass

    def _get_includes(self) -> List[Project]:
        """Recursively discover the included 'eds.yml' projects.

        Returns:
            List[Project]: The list of discovered projects.
        """
        includes: List[Project] = []
        for include in self._yaml['include']:
            self._lookup[self._event.url] = {}
            event = Event.init_from_include(include, self._event)
            includes.append(Project(event, self._lookup))
        return includes

    def _discover_plugins(self) -> List[Plugin]:
        """Recursively discover all the plugins.

        Returns:
            List[Plugin]: The list of discovered plugins.
        """
        for include in self._get_includes():
            self._plugins += include.plugins
        for plugin_yaml in self._yaml['plugins']:
            # If plugin is builtin or already installed, then it can be
            # instantiated. Otherwise, we will use the BasePlugin, and the
            # actual plugin will be instantiated in a future discovery after
            # worker performs the installation.
            if 'version' not in plugin_yaml or is_installed(plugin_yaml['version']):
                plugin = get_plugin(plugin_yaml['type'], plugin_yaml['name'])(plugin_yaml)
            else:
                plugin = BasePlugin(plugin_yaml)
            self._lookup[self._event.url][plugin.id] = plugin
            for descendant in plugin.descendants:
                self._lookup[self._event.url][descendant.id] = descendant
                self._plugins.append(descendant)
            self._plugins.append(plugin)

    def _apply_inheritance(self, plugin: Plugin) -> None:
        """Gather parent properties recursively.  Mark parent plugins as overridden.

        Args:
            plugin (Plugin): The plugin to apply.
        """
        parent_ref = plugin.yaml.get('parent')
        if parent_ref:
            parent_plugin = self._lookup[parent_ref.get('url', self._event.url)][parent_ref['id']]
            parent_plugin.overridden = True
            self._apply_inheritance(parent_plugin)
            new_properties = deepcopy(parent_plugin.yaml['properties'])
            new_properties.update(plugin.yaml['properties'])
            plugin.yaml['properties'] = new_properties

    @property
    def plugins(self) -> List[Plugin]:
        """The list of discovered plugins.

        Returns:
            List[Plugin]: The list of discovered plugins
        """
        return self._plugins

    @property
    def plugin_versions(self) -> List[str]:
        """The list of plugin pip install requirements.

        Returns:
            List[str]: The list of plugin pip install requirments.
        """
        return [p.yaml['version'] for p in self._plugins if 'version' in p.yaml and not p.overridden]

    @property
    def pipelines(self) -> List[Pipeline]:
        """The list of discovered pipelines, excluding overridden.

        Returns:
            List[Plugin]: The list of discovered pipelines, excluding overridden.
        """
        return [p for p in self._plugins if not p.overridden and p.yaml['type'] == 'eds.pipeline']
