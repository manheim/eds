from eds.interfaces.plugin import Plugin


class PipelineProvider(Plugin):

    interface_name = "eds.pipeline_provider"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.pipeline_provider",
        "title": "Pipeline Provider",
        "type": "object",
        "properties": {}
    }

    def create_pipeline(self):
        pass

    def update_pipeline(self):
        pass

    def delete_pipeline(self):
        pass