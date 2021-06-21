from eds.interfaces.plugin_interface import PluginInterface


class Tags(PluginInterface):
    """eds.tags interface."""

    interface_name = "eds.tags"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.tags",
        "title": "Tags",
        "type": "object",
        "properties": {}
    }


PluginInterface.register(Tags)
assert issubclass(Tags, PluginInterface)
assert isinstance(Tags(), PluginInterface)
