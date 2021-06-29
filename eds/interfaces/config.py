from abc import abstractmethod
from eds.interfaces.plugin import Plugin


class Config(Plugin):
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
