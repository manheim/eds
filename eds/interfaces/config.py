from eds.interfaces.plugin import Plugin


class Config(Plugin):

    interface_name = "eds.config"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.application",
        "title": "Configuration",
        "type": "object",
        "properties": {}
    }
