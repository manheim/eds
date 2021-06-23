import os
from typing import Dict
from unittest.mock import patch, call, Mock, mock_open
from github3.repos.contents import Contents

from eds.plugins.github_provider import GithubProvider


class TestGithubProvider(object):

    # Github.com Tests
    def test_get_files(self):
        cls = GithubProvider(token_env_var='GITHUB_PAT')
        root_dir_contents = cls.get_files(owner="manheim", repo_name="eds")

        assert root_dir_contents is not None
        assert root_dir_contents['README.md'] is not None
        assert isinstance(root_dir_contents, Dict)
        assert isinstance(root_dir_contents['README.md'], Contents)

    def test_get_files_with_dir(self):
        cls = GithubProvider(token_env_var='GITHUB_PAT')
        test_dir_contents = cls.get_files(owner="manheim", repo_name="eds", directory_path="tests")

        assert test_dir_contents is not None
        assert test_dir_contents['test_plugin.py'] is not None
        assert isinstance(test_dir_contents, Dict)
        assert isinstance(test_dir_contents['test_plugin.py'], Contents)

    # Github Enterprise Tests
    def test_enterprise_get_files(self):
        cls = GithubProvider(token_env_var='GHE_PAT', github_enterprise_url=os.getenv('GHE_URL', None))
        root_dir_contents = cls.get_files(owner="James-Leopold", repo_name="jleopold-pipeworks-example")

        assert root_dir_contents is not None
        assert root_dir_contents['README.md'] is not None
        assert isinstance(root_dir_contents, Dict)
        assert isinstance(root_dir_contents['README.md'], Contents)

    def test_enterprise_get_files_with_dir(self):
        cls = GithubProvider(token_env_var='GHE_PAT', github_enterprise_url=os.getenv('GHE_URL', None))
        config_dir_contents = cls.get_files(owner="James-Leopold", repo_name="jleopold-pipeworks-example",  directory_path="config")

        assert config_dir_contents is not None
        assert config_dir_contents['pipeline.groovy'] is not None
        assert isinstance(config_dir_contents, Dict)
        assert isinstance(config_dir_contents['pipeline.groovy'], Contents)

