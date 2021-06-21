from abc import abstractmethod
from eds.interfaces.plugin_interface import PluginInterface


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

    @abstractmethod
    def generate(self) -> None:
        """Generate the config."""
        pass

Config.register(PluginInterface)
assert issubclass(PluginInterface, Config)