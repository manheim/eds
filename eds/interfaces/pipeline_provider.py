from eds.interfaces.plugin import Plugin


class PipelineProvider(Plugin):

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.pipeline_provider",
        "title": "Pipeline Provider",
        "type": "object",
        "properties": {}
    }

    def create_pipeline(self):
        pass

    def delete_pipeline(self):
        pass
