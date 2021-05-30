from eds.interfaces.plugin import Plugin


class Worker(Plugin):

    interface_name = "eds.worker"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.tags",
        "title": "Tags",
        "type": "object",
        "properties": {}
    }

    def build_eds(self, eds_version, plugin_versions):
        pass
