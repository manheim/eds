from __future__ import annotations
from typing import List, Dict
from abc import ABCMeta, abstractmethod
from eds.plugin import Plugin


class PluginInterface(metaclass=ABCMeta):
    """general plugin interface."""

    schema: Dict = {}
    """json schema for plugin properties"""

    @property
    @abstractmethod
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        pass

    @abstractmethod
    def validate(self) -> None:
        """Validate the plugin."""
        pass
