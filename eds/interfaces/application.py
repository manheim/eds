from eds.interfaces.plugin import Plugin


class Application(Plugin):

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.application",
        "title": "Application",
        "type": "object",
        "properties": {}
    }
