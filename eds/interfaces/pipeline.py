from eds.interfaces.plugin import Plugin


class Pipeline(Plugin):

    interface_name = "eds.pipeline"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.pipeline",
        "title": "Pipeline",
        "type": "object",
        "properties": {}
    }
