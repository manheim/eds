from eds.interfaces.plugin import PluginInterface


class Pipeline(PluginInterface):
    """eds.pipeline interface."""

    interface_name = "eds.pipeline"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.pipeline",
        "title": "Pipeline",
        "type": "object",
        "properties": {}
    }

    def build(self) -> None:
        """Build the pipeline configuration."""
        pass
