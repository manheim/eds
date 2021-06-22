import os
from typing import List, Dict, Optional
from github3 import login
from github3 import enterprise_login
from github3.github import GitHub
from github3.github import GitHubEnterprise
from github3.repos.repo import Repository
from github3.orgs import Organization
from github3.repos.contents import Contents

from eds.interfaces.vcs_provider import VcsProvider
from eds.interfaces.plugin import Plugin


class GithubProvider(VcsProvider):
    """Github Provider implementation."""

    def __init__(
        self,        
        gh_username: str = None,
        gh_password: str = None,
        token_var: str = None,
        github_enterprise_url: str = None, 
    ):
        """Login to Github or Github Enterprise"""
        if github_enterprise_url is None:
            print(f"Logging in to github.com...")
            self._g: GitHub = login(
                username=gh_username,
                password=gh_password,
                token=os.environ[token_var]
            )
        else:
            print(f"Logging in to {github_enterprise_url}...")
            self._g: GitHubEnterprise = enterprise_login(
                url=github_enterprise_url,
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

    def get_files(self, owner: str, repo_name: str) -> Dict:
        """Get project files."""
        try:
            repo: Repository = self._g.repository(owner, repo_name)
            contents = repo.directory_contents('path/to/dir/', return_as=dict)
        except Exception as ex:
            print(f"Exception in get_files: {ex}")
            return None

        return contents

    def create_project(self, org_name: str, project_name: str) -> Repository:
        """Create a Project."""
        try:
            org: Organization = self._g.organization(org_name)
            new_project_repo: Repository = org.create_repository(
                name=project_name,
                descritption=f"EDS project for {project_name}"
            )
        except Exception as ex:
            print(f"Exception in create_project: {ex}")
            return None

        return new_project_repo

    def delete_project(self, owner: str, repo_name: str) -> bool:
        """Delete a Project."""
        try:
            repo: Repository = self._g.repository(owner, repo_name)
            repo_deleted = repo.delete()
        except Exception as ex:
            print(f"Exception in delete_project: {ex}")

        if repo_deleted:
            print(f"Repo {repo_name} deleted successfully!")
        else:
            print(f"Failure to delete {repo_name}")

        return repo_deleted

    def update_project(
        self, owner: str, repo_name: str,
        file_name: str, new_contents: str,
        commit_message: str = "Updating EDS project",
        branch_name: Optional[str] = None
    ) -> bool:
        """Update a Project."""
        try:
            repo: Repository = self._g.repository(owner, repo_name)
            file_contents: Contents = repo.contents(file_name)
            file_contents.update(
                message=commit_message,
                content=new_contents.encode('utf-8'),
                branch=branch_name
            )
        except Exception as ex:
            print(f"Exception in update_project: {ex}")
            return False

        return True


VcsProvider.register(GithubProvider)
