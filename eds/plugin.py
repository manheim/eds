

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

    @property
    def id(self):
        return self._yaml['id']

    @property
    def yaml(self):
        return self._yaml

    @property
    def children(self):
        return []

    @property
    def descendants(self):
        plugins = []
        for plugin in self.children:
            plugins += plugin.children
            plugins.append(plugin)
        return plugins
