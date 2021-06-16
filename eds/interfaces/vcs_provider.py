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
        pass

    def get_files(self) -> Dict:
        """Get project files."""
        pass

    def create_project(self) -> None:
        """Create a Project."""
        pass

    def delete_project(self) -> None:
        """Delete a Project."""
        pass

    def update_project(self) -> None:
        """Update a Project."""
        pass
