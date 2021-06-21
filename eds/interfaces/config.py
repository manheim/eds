
from eds.interfaces.plugin import PluginInterface


class Config(PluginInterface):
    """eds.config interface."""

    interface_name = "eds.config"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.application",
        "title": "Configuration",
        "type": "object",
        "properties": {}
    }

    def generate(self) -> None:
        """Generate the config."""
        pass
