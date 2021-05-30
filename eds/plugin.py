

class Plugin():

    eds_schema = {}
    properties_schema = {}

    def __init__(self, plugin_yml):
        self._yml = self._validate(plugin_yml)
        self.overridden = False

    def _validate(self, yaml):
        # jsonschema(eds_schema)
        # jsonschema(properties_schema)
        self.validate()

    def validate(self):
        pass

    def get_plugins(self):
        pass

    @property
    def id(self):
        return self._yml['id']

    @property
    def plugins(self):
        plugins = []
        for plugin in self.get_plugins():
            plugins += plugin.get_plugins()
            plugins.append(plugin)
        return plugins
