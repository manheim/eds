from abc import abstractmethod
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

    @abstractmethod
    def create_pipeline(self) -> None:
        """Create a pipeline."""
        raise NotImplementedError()

    @abstractmethod
    def update_pipeline(self) -> None:
        """Update a pipeline."""
        raise NotImplementedError()

    @abstractmethod
    def delete_pipeline(self) -> None:
        """Delete a pipeline."""
        raise NotImplementedError()
