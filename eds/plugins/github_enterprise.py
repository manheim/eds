import os
from typing import List, Dict
from github3 import enterprise_login
from github3.github import GitHubEnterprise

from eds.interfaces.vcs_provider import VcsProvider
from eds.interfaces.plugin import Plugin


class GithubEnterpriseProvider(VcsProvider):
    """Github Enterprise Provider implementation."""


    def __init__ (self, github_url: str, token_var: str):
        """
        Login to Github Enterprise using access token
        """
        self._ghe: GitHubEnterprise = enterprise_login(
            url=github_url,
            token=os.environ[token_var]
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

    def get_files(self, org_name: str, repo_name: str) -> Dict:
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


VcsProvider.register(GithubEnterpriseProvider)
