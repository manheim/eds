from typing import Dict
import pytest

from github3.github import GitHub, GitHubEnterprise
from unittest.mock import Mock, patch, call, PropertyMock

from eds.plugins.github_provider import GithubProvider

pbm = 'eds.plugins.github_provider'
pb = f'{pbm}.GithubProvider'

class GithubProviderTester(object):

    """Tests for eds.plugins.github_provider module."""

    def setup(self):
        self.mock_g = Mock(spec_set=GitHub)
        self.mock_org = Mock(login='foo')
        self.mock_g.organization.return_value = self.mock_org
        self.mock_repo = Mock(full_name='foo/bar', id=12345)
        self.mock_g.repository.return_value = self.mock_repo
        with patch(f'{pb}.__init__') as m_init:
            m_init.return_value = None
            self.cls = GithubProvider(token_env_var='foo')
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
            cls = GithubProvider(token_env_var='GITHUB_TOKEN')
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
            cls = GithubProvider(token_env_var='GHE_TOKEN', github_enterprise_url='https://url.com/')
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
                GithubProvider(token_env_var='GITHUB_TOKEN')
        assert m_login.mock_calls == []
        assert mock_g.mock_calls == []

    @patch.dict('os.environ', {}, clear=True)  
    def test_no_token_enterprise(self):
        mock_ghe = Mock(spec_set=GitHubEnterprise)
        mock_repo = Mock()
        with patch(f'{pbm}.enterprise_login', autospec=True) as m_el:
            m_el.return_value = mock_ghe
            with pytest.raises(RuntimeError):
                GithubProvider(token_env_var='GITHUB_TOKEN', github_enterprise_url='https://url.com/')
        assert m_el.mock_calls == []
        assert mock_ghe.mock_calls == []
    
class TestGetFiles(GithubProviderTester):

    def test_get_files(self):
        def se_contents(path, **kwargs):
            return {
                'baz': Mock(
                    decoded='bazContent'.encode('utf-8'), type='file'
                ),
                'blarg': Mock(
                    decoded='blargContent'.encode('utf-8'), type='file'
                ),
            }

        self.mock_repo.directory_contents.side_effect = se_contents
        res = self.cls.get_files(owner='foo', repo_name='bar')
        assert res == {
            'baz': 'bazContent',
            'blarg': 'blargContent'
        }
        assert self.mock_repo.mock_calls == [
            call.directory_contents('/', ref='master', return_as=dict)
        ]

