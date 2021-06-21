from eds.interfaces.plugin import Plugin


class PipelineProvider(Plugin):
    """eds.pipeline_provider interface."""

    interface_name = "eds.pipeline_provider"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.pipeline_provider",
        "title": "Pipeline Provider",
        "type": "object",
        "properties": {}
    }

    def create_pipeline(self) -> None:
        """Create a pipeline."""
        pass

    def update_pipeline(self) -> None:
        """Update a pipeline."""
        pass

    def delete_pipeline(self) -> None:
        """Delete a pipeline."""
        pass
