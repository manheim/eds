from eds.interfaces.plugin_interface import PluginInterface


class Tags(PlugPluginInterfacein):
    """eds.tags interface."""

    interface_name = "eds.tags"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.tags",
        "title": "Tags",
        "type": "object",
        "properties": {}
    }
