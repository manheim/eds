
from __future__ import annotations
from typing import Dict, List
from eds.interfaces.plugin_interface import PluginInterface


class Plugin(PluginInterface):
    """Base class for EDS plugins."""

    schema: Dict = {}
    """json schema for plugin properties.

    An abstract attribute implemented by specific plugin classes.
    """

    def __init__(self, yaml: Dict):
        """Plugin Consructor.

        Args:
            yaml (Dict): Plugin yaml dict.
        """
        self._yaml = yaml
        self._validate_schema()
        self.validate()
        self.overridden = False

    def _validate_schema(self) -> None:
        """Validate against the schema in `Plugin.schema`."""
        pass

    def validate(self) -> None:
        """Abstract method implemented in plugin classes for custom validation."""
        pass

    @property
    def id(self) -> str:
        """The plugin id.

        Returns:
            str: The plugin id.
        """
        return self._yaml['id']

    @property
    def yaml(self) -> Dict:
        """The plugin yaml.

        Returns:
            Dict: The plugin yaml.
        """
        return self._yaml

    @property
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        return []

    @property
    def descendants(self) -> List[Plugin]:
        """The list of descendant plugins.

        Returns:
            List[Plugin]: The list of descendant plugins.
        """
        plugins = []
        for plugin in self.children:
            plugins += plugin.children
            plugins.append(plugin)
        return plugins


PluginInterface.register(Plugin)
assert issubclass(Plugin, PluginInterface)
assert isinstance(Plugin({}), PluginInterface)
