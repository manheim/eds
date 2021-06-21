from abc import abstractmethod
from eds.interfaces.plugin_interface import PluginInterface


class Worker(PluginInterface):
    """eds.worker interface."""

    interface_name = "eds.worker"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.tags",
        "title": "Tags",
        "type": "object",
        "properties": {}
    }

    @abstractmethod
    def build_eds(self, eds_version: bool, plugin_versions: bool) -> None:
        """Build EDS.

        Args:
            eds_version (bool): EDS version as pip install requirement.
            plugin_versions (bool): List of EDS plugin versions as pip install requirements.
        """
        pass

PluginInterface.register(Worker)
assert issubclass(Worker, PluginInterface)
assert isinstance(Worker(), PluginInterface)
