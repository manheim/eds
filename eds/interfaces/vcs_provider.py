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

    def parse_webhook_event(self) -> None:
        """Parse webhook event data."""
        pass

    def create_project(self) -> None:
        """Create Project."""
        pass

    def delete_project(self) -> None:
        """Delete Project."""
        pass

    def get_project(self) -> None:
        """Get Project."""
        pass
