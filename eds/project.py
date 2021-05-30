from copy import deepcopy

from eds.event import Event
from eds.exception import CircularIncludeError
from eds.plugin import Plugin


EDS_YML_FILE = 'eds.yml'


class Project:

    def __init__(self, event, lookup=None):
        if event.url in lookup:
            raise CircularIncludeError()
        self._event = event
        self._yml = self._validate(event.eds_yml)
        if lookup is None:
            self._lookup = {}
            self._plugins = self._get_plugins(self)
            [self._apply_inheritance(p) for p in self._plugins]

    def _validate(self, eds_yml):
        pass

    def _get_includes(self):
        includes = []
        for include in self.yml['include']:
            event = Event.from_include(include['url'], self._event)
            includes.append(Project(event, self._lookup))
        return includes

    def _get_plugins(self):
        plugins = []
        for include in self._get_includes():
            plugins += include._get_plugins()
        for plugin_yml in self._yml['plugins']:
            plugin = Plugin(plugin_yml)
            self._lookup[self._event.url + plugin.id] = plugin
            for child_plugin in plugin.plugins:
                self._lookup[self._event.url + child_plugin.id] = child_plugin
                plugins.append(child_plugin)
            plugins.append(plugin)
        return plugins

    def _apply_inheritance(self, plugin):
        parent_ref = plugin.yml.get('parent')
        if parent_ref:
            parent_plugin = self._lookup[parent_ref.get('url', self._event.url) + parent_ref['plugin_id']]
            parent_plugin.overridden = True
            self._apply_inheritance(parent_plugin)
        plugin.yml['properties'] = deepcopy(self.parent_plugin.yml['properties']).update(plugin.yml['properties'])

    @property
    def plugin_verions(self):
        return [p.yml['version'] for p in self._plugins if not p.overridden]

    @property
    def pipelines(self):
        return [p for p in self._plugins if not p.overridden and p.yml['type'] == 'eds.pipeline']
