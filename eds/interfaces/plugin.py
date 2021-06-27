
from __future__ import annotations
from typing import List, Dict


class Plugin():
    """general plugin interface."""

    schema: Dict = {}
    """json schema for plugin properties"""

    @property
    def id(self) -> str:
        """The plugin id.

        Returns:
            str: The plugin id.
        """
        pass

    @property
    def yaml(self) -> Dict:
        """The plugin yaml.

        Returns:
            Dict: The plugin yaml.
        """
        pass

    @property
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        pass

    @property
    def descendants(self) -> List[Plugin]:
        """The list of descendant plugins.

        Returns:
            List[Plugin]: The list of descendant plugins.
        """
        pass

    def validate(self) -> None:
        """Validate the plugin."""
        pass
