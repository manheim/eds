from typing import Dict
import pytest
from github3.github import GitHub, GitHubEnterprise
from github3.repos.contents import Contents
from github3.repos.repo import Repository
from unittest.mock import Mock, patch, call, PropertyMock

from eds.plugin import BasePlugin
from eds.plugins.vcs_provider_github import GithubProvider

pbm = 'eds.plugins.vcs_provider_github'
pb = f'{pbm}.GithubProvider'

class GithubProviderPlugin(BasePlugin, GithubProvider):

    def generate(self) -> None:
        pass

class GithubProviderTester(object):

    """Tests for eds.plugins.vcs_provider_github module."""

    def setup(self):
        self.mock_g = Mock(spec_set=GitHub)
        self.mock_org = Mock(login='foo')
        self.mock_g.organization.return_value = self.mock_org
        self.mock_repo = Mock(full_name='foo/bar', id=12345)
        self.mock_repo2 = Mock(full_name='foo/bar2', id=6789)
        self.mock_g.repository.return_value = self.mock_repo
        with patch(f'{pb}.__init__') as m_init:
            m_init.return_value = None
            self.cls = GithubProviderPlugin({'token_env_var': 'GITHUB_TOKEN'})
        self.cls._g = self.mock_g

class TestInit:

    @patch.dict(
        'os.environ',
        {
            'GITHUB_TOKEN': 'myToken'
        },
        clear=True
    )
    def test_public_github(self):
        mock_g = Mock(spec_set=GitHub)

        with patch(f'{pbm}.login', autospec=True) as m_login:
            m_login.return_value = mock_g
            cls = GithubProviderPlugin({'token_env_var': 'GITHUB_TOKEN'})
        assert m_login.mock_calls == [
            call(token='myToken')
        ]
        assert cls._g == mock_g

    @patch.dict(
        'os.environ',
        {
            'GHE_TOKEN': 'myEnterpriseToken'
        },
        clear=True
    )
    def test_github_enterprise(self):
        mock_ghe = Mock(spec_set=GitHubEnterprise)
        with patch(f'{pbm}.enterprise_login', autospec=True) as m_el:
            m_el.return_value = mock_ghe
            cls = GithubProviderPlugin({"token_env_var": "GHE_TOKEN", "github_enterprise_url": "https://url.com/"})
        assert m_el.mock_calls == [
            call(url='https://url.com/', token='myEnterpriseToken')
        ]
        assert cls._g == mock_ghe
    
    @patch.dict('os.environ', {}, clear=True)
    def test_no_token(self):
        mock_g = Mock(spec_set=GitHub)
        mock_repo = Mock()
        with patch(f'{pbm}.login', autospec=True) as m_login:
            m_login.return_value = mock_g
            with pytest.raises(RuntimeError):
                GithubProviderPlugin({"token_env_var": "GITHUB_TOKEN"})
        assert m_login.mock_calls == []
        assert mock_g.mock_calls == []

    @patch.dict('os.environ', {}, clear=True)  
    def test_no_token_enterprise(self):
        mock_ghe = Mock(spec_set=GitHubEnterprise)
        mock_repo = Mock()
        with patch(f'{pbm}.enterprise_login', autospec=True) as m_el:
            m_el.return_value = mock_ghe
            with pytest.raises(RuntimeError):
                GithubProviderPlugin({"token_env_var": "GITHUB_TOKEN", "github_enterprise_url": "https://url.com/"})
        assert m_el.mock_calls == []
        assert mock_ghe.mock_calls == []
    
class TestGetFiles(GithubProviderTester):

    def test_get_files(self):
        def se_contents(path, **kwargs):
            return {
                'baz': Mock(spec_set=Contents),
                'blarg': Mock(spec_set=Contents)
            }

        self.mock_repo.directory_contents.side_effect = se_contents
        res = self.cls.get_files(owner='foo', repo_name='bar')
        assert res is not None
        assert isinstance(res, Dict)
        assert isinstance(res['baz'], Contents)
        assert isinstance(res['blarg'], Contents)
        assert self.mock_repo.mock_calls == [
            call.directory_contents('/', ref='master', return_as=dict)
        ]

    def test_get_files_with_path(self):
        def se_contents(path, **kwargs):
            return {
                'bar': Mock(spec_set=Contents),
                'foo': Mock(spec_set=Contents)
            }

        self.mock_repo.directory_contents.side_effect = se_contents
        res = self.cls.get_files(owner='foo', repo_name='bar', path='subdir')

        assert res is not None
        assert isinstance(res, Dict)
        assert isinstance(res['bar'], Contents)
        assert isinstance(res['foo'], Contents)
        assert self.mock_repo.mock_calls == [
            call.directory_contents('subdir', ref='master', return_as=dict)
        ]

class TestCreateProject(GithubProviderTester):

    def test_create_project(self):
        self.mock_org.create_repository.return_value = self.mock_repo2
        res = self.cls.create_project(org_name='myorg', project_name='new_proj')

        assert res is not None
        assert self.mock_org.mock_calls == [
            call.create_repository(name="new_proj", descritption="EDS project for new_proj")
        ]

    def test_create_project_exception(self):
        self.mock_repo.create_repository.return_value = self.mock_repo2

        with pytest.raises(Exception):
            res = self.cls.create_project(owner='foo', repo_name='bar')

        assert self.mock_org.mock_calls == []
        assert self.mock_repo.mock_calls == []

class TestDeleteProject(GithubProviderTester):

    def test_delete_project(self):
        self.mock_repo.delete.return_value = True
        res = self.cls.delete_project(owner='foo', repo_name='bar')

        assert res is True
        assert self.mock_repo.mock_calls == [
            call.delete()
        ]

    def test_delete_project_failure(self):
        self.mock_repo.delete.return_value = False
        res = self.cls.delete_project(owner='foo', repo_name='bar')

        assert res is False
        assert self.mock_repo.mock_calls == [
            call.delete()
        ]
    
class TestUpdateProject(GithubProviderTester):

    def test_update_project(self):
        def se_contents(path, **kwargs):
            return {
                'myfile.txt': Mock(spec_set=Contents)
            }

        self.mock_repo.contents('myfile.txt').side_effect = se_contents
        res = self.cls.update_project(owner='foo', repo_name='bar2', file_name='myfile.txt', new_contents='updated content')

        assert res is True
        assert self.mock_repo.mock_calls == [
            call.contents('myfile.txt'),
            call.contents('myfile.txt'),
            call.contents().update(message='Updating EDS project', content=b'updated content', branch=None)
        ]
    
    def test_update_project_with_branch(self):
        def se_contents(path, **kwargs):
            return {
                'myfile.txt': Mock(spec_set=Contents)
            }

        self.mock_repo.contents('myfile.txt').side_effect = se_contents
        res = self.cls.update_project(owner='foo', repo_name='bar2', file_name='myfile.txt', new_contents='updated content', branch_name="develop_br")

        assert res is True
        assert self.mock_repo.mock_calls == [
            call.contents('myfile.txt'),
            call.contents('myfile.txt'),
            call.contents().update(message='Updating EDS project', content=b'updated content', branch="develop_br")
        ]
