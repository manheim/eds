from typing import Dict
from abc import abstractmethod

from eds.interfaces.plugin import Plugin


class VcsProvider(Plugin):
    """eds.vcs_provider interface."""

    interface_name = "eds.vcs_provider"

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.vcs_provider",
        "title": "VCS Provider",
        "type": "object",
        "properties": {}
    }

    @property
    @abstractmethod
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        return []

    @abstractmethod
    def validate(self) -> None:
        """Validate the plugin."""
        pass

    @abstractmethod
    def parse_event(self) -> Dict:
        """Parse webhook event for project url and ref."""
        pass

    @abstractmethod
    def get_files(self) -> Dict:
        """Get project files."""
        pass

    @abstractmethod
    def create_project(self) -> None:
        """Create a Project."""
        pass

    @abstractmethod
    def delete_project(self) -> None:
        """Delete a Project."""
        pass

    @abstractmethod
    def update_project(self) -> None:
        """Update a Project."""
        pass

class GithubProvider(VcsProvider):
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
    def parse_event(self) -> Dict:
        return super().parse_event()

    def get_files(self) -> Dict:
        return super().get_files()

    def create_project(self) -> None:
        return super().create_project()

    def delete_project(self) -> None:
        return super().delete_project()

    def update_project(self) -> None:
        return super().update_project()

class GithubEnterpriseProvider(VcsProvider):
    
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

    def parse_event(self) -> Dict:
        return super().parse_event()

    def get_files(self) -> Dict:
        return super().get_files()

    def create_project(self) -> None:
        return super().create_project()

    def delete_project(self) -> None:
        return super().delete_project()

    def update_project(self) -> None:
        return super().update_project()

VcsProvider.register(GithubProvider)
VcsProvider.register(GithubEnterpriseProvider)
