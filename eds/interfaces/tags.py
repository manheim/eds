from eds.interfaces.plugin import Plugin


class Tags(Plugin):

    interface_name = "eds.tags"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.tags",
        "title": "Tags",
        "type": "object",
        "properties": {}
    }
