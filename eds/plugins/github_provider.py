import os
from typing import List, Dict, Optional

from github3 import login, enterprise_login
from github3.github import GitHub, GitHubEnterprise
from github3.orgs import Organization
from github3.repos.repo import Repository
from github3.repos.contents import Contents
# from github3.repos.branch import Branch
# from github3.git import CommitTree, Commit, Tree, Hash, Reference
# from github3.repos.comparison import Comparison
# from github3.users import User
# from github3.exceptions import NotFoundError, ForbiddenError

from eds.interfaces.vcs_provider import VcsProvider
from eds.interfaces.plugin import Plugin


class GithubProvider(VcsProvider):
    """Github Provider implementation."""

    def __init__(self, token_env_var: str = None, github_enterprise_url: str = None):
        """Login to Github or Github Enterprise."""
        token: str = os.environ.get(token_env_var)
        if token == '' or token is None:
            raise RuntimeError(
                f'ERROR: You must export the {token_env_var} environment variable.'
            )
        if github_enterprise_url is None:
            self._g: GitHub = login(token=token)
        else:
            self._g: GitHubEnterprise = enterprise_login(url=github_enterprise_url, token=token)

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

    def get_files(self, owner: str, repo_name: str, path: str = '/', ref: str = 'master') -> Dict[str, str]:
        """Get project files.

        Return the contents of the repository's specified ``ref``, under the
        specified path, as a dict of string key to string file contents.

        :param owner: owner of the repo
        :param repo_name: name of the repo
        :param path: path under the repo to get
        :param ref: ref to get contents at
        :return: repository contents
        """
        result: Dict[str, str] = {}

        try:
            repo: Repository = self._g.repository(owner, repo_name)
            content: Dict[str, Contents] = repo.directory_contents(path, ref=ref, return_as=dict)

            for fname in content.keys():
                if content[fname].type == 'dir':
                    for k, v in self.directory_contents(
                        content[fname].path, ref=ref
                    ).items():
                        result[os.path.join(fname, k).lstrip('/')] = v
                else:
                    content[fname].refresh()
                    result[fname] = content[fname].decoded.decode('utf-8')

        except Exception as ex:
            print(f"Exception in get_files: {ex}")

        return result

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
