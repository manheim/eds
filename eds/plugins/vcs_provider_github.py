import os
import json
from typing import Dict, Optional

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

from eds.plugin import BasePlugin
from eds.interfaces.vcs_provider import VcsProvider


class GithubProviderPlugin(BasePlugin, VcsProvider):
    """eds.plugins.vcs_provider_github Plugin."""

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "eds.plugins.vcs_provider_github",
        "title": "Github Provider Plugin",
        "type": "object",
        "properties": {
            "token_env_var": "",
            "github_enterprise_url": ""
        }
    }

    def __init__(self, yaml: Dict):
        """Github Provider Plugin Consructor.

        Args:
            yaml (Dict): Plugin yaml dict.
        """
        self._yaml = yaml
        self._validate_schema()
        self.validate()
        self.overridden = False

        token_env_var = self._yaml.get('token_env_var', 'GITHUB_TOKEN')
        github_enterprise_url = self._yaml.get('github_enterprise_url', '')

        # Login to Github or Github Enterprise.
        token: str = os.environ.get(token_env_var)
        if token is None or token == '':
            raise RuntimeError(
                f"ERROR: You must export the {token_env_var} environment variable."
            )
        if github_enterprise_url is None or github_enterprise_url == '':
            self._g: GitHub = login(token=token)
        else:
            self._g: GitHubEnterprise = enterprise_login(url=github_enterprise_url, token=token)

    def parse_event(self, payload: str) -> Dict:
        """Parse webhook event for project url and ref."""
        # parse project url and sha from the webhook payload.
        json_data = json.loads(payload)
        project_url = json_data['repository']['url']
        head_sha = json_data['check_suite']['head_sha']
        return {"url": project_url, "ref": head_sha}

    def get_files(self, owner: str, repo_name: str, path: str = '/', ref: str = 'master') -> Dict[str, Contents]:
        """Get project files.

        Return the contents of the repository's specified ``ref``, under the
        specified path, as a dict of string key to string file contents.

        :param owner: owner of the repo
        :param repo_name: name of the repo
        :param path: path under the repo to get
        :param ref: ref to get contents at
        :return: repository contents
        """
        try:
            repo: Repository = self._g.repository(owner, repo_name)
            contents: Dict[str, Contents] = repo.directory_contents(path, ref=ref, return_as=dict)
        except Exception as ex:
            print(f"Exception in get_files: {ex}")
            return None

        return contents

    def create_project(self, org_name: str, project_name: str) -> Repository:
        """Create a Project.

        :param org_name: Organization to create repo in
        :param project_name: name of the repo to create
        :return: newly created Repository object
        """
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
        """Delete a Project.

        :param owner: owner of repo
        :param repo_name: name of the repo to delete
        :return: True if succefully deleted repo, False otherwise
        """
        repo_deleted = False
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
        """Update a Project.

        :param owner: owner of repo
        :param repo_name: name of the repo to delete
        :param file_name: file name to update
        :param new_contents: new contents for the file
        :param commit_message: github commit message
        :param branch_name: Name of branch to update file in
        :return: True if succefully updated repo, False otherwise
        """
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
