
from __future__ import annotations
from typing import List


class Plugin():
    """general plugin interface."""

    @property
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        return []

    def validate(self) -> None:
        """Validate the plugin."""
        pass
