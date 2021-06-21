from abc import abstractmethod
from eds.interfaces.plugin_interface import PluginInterface


class PipelineProvider(PluginInterface):
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
        pass

    @abstractmethod
    def update_pipeline(self) -> None:
        """Update a pipeline."""
        pass

    @abstractmethod
    def delete_pipeline(self) -> None:
        """Delete a pipeline."""
        pass


PluginInterface.register(PipelineProvider)
assert issubclass(PipelineProvider, PluginInterface)
assert isinstance(PipelineProvider(), PluginInterface)
