from typing import Dict

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

    def parse_event(self) -> Dict:
        """Parse webhook event for project url and ref."""
        raise NotImplementedError()

    def get_files(self) -> Dict:
        """Get project files."""
        raise NotImplementedError()

    def create_project(self) -> None:
        """Create a Project."""
        raise NotImplementedError()

    def delete_project(self) -> None:
        """Delete a Project."""
        raise NotImplementedError()

    def update_project(self) -> None:
        """Update a Project."""
        raise NotImplementedError()
