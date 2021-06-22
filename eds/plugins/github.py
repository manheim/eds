import os
from typing import List, Dict
from github3 import login
from github3.github import GitHub

from eds.interfaces.vcs_provider import VcsProvider
from eds.interfaces.plugin import Plugin


class GithubProvider(VcsProvider):
    """Github Provider implementation."""

    def __init__(
        self,
        gh_username: str = None,
        gh_password: str = None,
        token_var: str = None
    ):
        """Login to public Github using username/password or token."""
        self._g: GitHub = login(
            username=gh_username,
            password=gh_password,
            tokan=os.environ[token_var]
        )

    @property
    def children(self) -> List[Plugin]:
        """The list of child plugins.

        Returns:
            List[Plugin]: The list of child plugins.
        """
        return []

    def validate(self) -> None:
        """Validate the plugin."""
        return super().validate()

    def parse_event(self) -> Dict:
        """Parse webhook event for project url and ref."""
        return super().parse_event()

    def get_files(self) -> Dict:
        """Get project files."""
        return super().get_files()

    def create_project(self) -> None:
        """Create a Project."""
        return super().create_project()

    def delete_project(self) -> None:
        """Delete a Project."""
        return super().delete_project()

    def update_project(self) -> None:
        """Update a Project."""
        return super().update_project()


VcsProvider.register(GithubProvider)
