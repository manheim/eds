

class Plugin():

    eds_schema = {}
    properties_schema = {}

    def __init__(self, yaml):
        self._yaml = yaml
        self._validate()
        self.overridden = False

    def _validate(self):
        # jsonschema(eds_schema)
        # jsonschema(properties_schema)
        self.validate()

    def validate(self):
        pass

    def get_child_plugins(self):
        return []

    @property
    def id(self):
        return self._yaml['id']

    @property
    def yaml(self):
        return self._yaml

    @property
    def child_plugins(self):
        plugins = []
        for plugin in self.get_child_plugins():
            plugins += plugin.get_child_plugins()
            plugins.append(plugin)
        return plugins
