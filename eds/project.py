from copy import deepcopy

from eds.event import Event
from eds.extend import get_plugin
from eds.exception import CircularIncludeError


EDS_YML_FILE = 'eds.yml'


class Project:

    def __init__(self, event, lookup=None):
        self._event = event
        self._yaml = self._validate(event.eds_yaml)
        if lookup is None:
            self._lookup = {}
            self._plugins = self._get_plugins()
            [self._apply_inheritance(p) for p in self._plugins]
        elif event.url in lookup:
            raise CircularIncludeError()
        else:
            self._lookup = lookup

    def _validate(self, eds_yaml):
        return eds_yaml

    def _get_includes(self):
        includes = []
        for include in self._yaml['include']:
            event = Event.init_from_include(include, self._event)
            includes.append(Project(event, self._lookup))
        return includes

    def _get_plugins(self):
        plugins = []
        for include in self._get_includes():
            plugins += include._get_plugins()
        for plugin_yaml in self._yaml['plugins']:
            plugin = get_plugin(plugin_yaml['type'], plugin_yaml['name'])(plugin_yaml)
            self._lookup[self._event.url + plugin.id] = plugin
            for descendant in plugin.descendants:
                self._lookup[self._event.url + descendant.id] = descendant
                plugins.append(descendant)
            plugins.append(plugin)
        return plugins

    def _apply_inheritance(self, plugin):
        parent_ref = plugin.yaml.get('parent')
        if parent_ref:
            parent_plugin = self._lookup[parent_ref.get('url', self._event.url) + parent_ref['id']]
            parent_plugin.overridden = True
            self._apply_inheritance(parent_plugin)
            new_properties = deepcopy(parent_plugin.yaml['properties'])
            new_properties.update(plugin.yaml['properties'])
            plugin.yaml['properties'] = new_properties

    @property
    def plugins(self):
        return self._plugins

    @property
    def plugin_versions(self):
        return [p.yaml['version'] for p in self._plugins if not p.overridden]

    @property
    def pipelines(self):
        return [p for p in self._plugins if not p.overridden and p.yaml['type'] == 'eds.pipeline']
