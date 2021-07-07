from __future__ import annotations
from typing import List, Dict
from abc import ABC, abstractmethod


class Plugin(ABC):
    """general plugin interface."""

    schema: Dict = {}
    """json schema for plugin properties"""

    @property
    @abstractmethod
    def id(self) -> str:
        """The plugin id.

        Returns:
            str: The plugin id.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def yaml(self) -> Dict:
        """The plugin yaml.

        Returns:
            Dict: The plugin yaml.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def descendants(self) -> List[Plugin]:
        """The list of descendant plugins.

        Returns:
            List[Plugin]: The list of descendant plugins.
        """
        raise NotImplementedError()

    @abstractmethod
    def validate(self) -> None:
        """Validate the plugin."""
        raise NotImplementedError()
