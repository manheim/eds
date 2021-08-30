from typing import Dict
import pytest
import json
from github3.github import GitHub, GitHubEnterprise
from github3.repos.contents import Contents
from github3.repos.repo import Repository
from unittest.mock import Mock, patch, call, PropertyMock

from eds.plugins.vcs_provider_github import GithubProviderPlugin

pbm = 'eds.plugins.vcs_provider_github'
pb = f'{pbm}.GithubProviderPlugin'

class GithubProviderPluginTester(object):

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

class TestParseEvent(GithubProviderPluginTester):

    def test_parse_event(self):
        mock_event_json = '''
        {
            "action": "completed",
            "check_suite": {
                "id": 118578147,
                "node_id": "MDEwOkNoZWNrU3VpdGUxMTg1NzgxNDc=",
                "head_branch": "changes",
                "head_sha": "ec26c3e57ca3a959ca5aad62de7213c562f8c821",
                "status": "completed",
                "conclusion": "success",
                "url": "https://api.github.com/repos/Codertocat/Hello-World/check-suites/118578147",
                "before": "6113728f27ae82c7b1a177c8d03f9e96e0adf246",
                "after": "ec26c3e57ca3a959ca5aad62de7213c562f8c821",
                "pull_requests": [
                    {
                        "url": "https://api.github.com/repos/Codertocat/Hello-World/pulls/2",
                        "id": 279147437,
                        "number": 2,
                        "head": {
                            "ref": "changes",
                            "sha": "ec26c3e57ca3a959ca5aad62de7213c562f8c821",
                            "repo": {
                                "id": 186853002,
                                "url": "https://api.github.com/repos/Codertocat/Hello-World",
                                "name": "Hello-World"
                            }
                        },
                        "base": {
                            "ref": "master",
                            "sha": "f95f852bd8fca8fcc58a9a2d6c842781e32a215e",
                            "repo": {
                                "id": 186853002,
                                "url": "https://api.github.com/repos/Codertocat/Hello-World",
                                "name": "Hello-World"
                            }
                        }
                    }
                ],
                "app": {
                    "id": 29310,
                    "node_id": "MDM6QXBwMjkzMTA=",
                    "owner": {
                        "login": "Octocoders",
                        "id": 38302899,
                        "node_id": "MDEyOk9yZ2FuaXphdGlvbjM4MzAyODk5",
                        "avatar_url": "https://avatars1.githubusercontent.com/u/38302899?v=4",
                        "gravatar_id": "",
                        "url": "https://api.github.com/users/Octocoders",
                        "html_url": "https://github.com/Octocoders",
                        "followers_url": "https://api.github.com/users/Octocoders/followers",
                        "following_url": "https://api.github.com/users/Octocoders/following{/other_user}",
                        "gists_url": "https://api.github.com/users/Octocoders/gists{/gist_id}",
                        "starred_url": "https://api.github.com/users/Octocoders/starred{/owner}{/repo}",
                        "subscriptions_url": "https://api.github.com/users/Octocoders/subscriptions",
                        "organizations_url": "https://api.github.com/users/Octocoders/orgs",
                        "repos_url": "https://api.github.com/users/Octocoders/repos",
                        "events_url": "https://api.github.com/users/Octocoders/events{/privacy}",
                        "received_events_url": "https://api.github.com/users/Octocoders/received_events",
                        "type": "Organization",
                        "site_admin": false
                    },
                    "name": "octocoders-linter",
                    "description": "",
                    "external_url": "https://octocoders.io",
                    "html_url": "https://github.com/apps/octocoders-linter",
                    "created_at": "2019-04-19T19:36:24Z",
                    "updated_at": "2019-04-19T19:36:56Z",
                    "permissions": {
                        "administration": "write",
                        "checks": "write",
                        "contents": "write",
                        "deployments": "write",
                        "issues": "write",
                        "members": "write",
                        "metadata": "read",
                        "organization_administration": "write",
                        "organization_hooks": "write",
                        "organization_plan": "read",
                        "organization_projects": "write",
                        "organization_user_blocking": "write",
                        "pages": "write",
                        "pull_requests": "write",
                        "repository_hooks": "write",
                        "repository_projects": "write",
                        "statuses": "write",
                        "team_discussions": "write",
                        "vulnerability_alerts": "read"
                    },
                    "events": []
                },
                "created_at": "2019-05-15T15:20:31Z",
                "updated_at": "2019-05-15T15:21:14Z",
                "latest_check_runs_count": 1,
                "check_runs_url": "https://api.github.com/repos/Codertocat/Hello-World/check-suites/118578147/check-runs",
                "head_commit": {
                    "id": "ec26c3e57ca3a959ca5aad62de7213c562f8c821",
                    "tree_id": "31b122c26a97cf9af023e9ddab94a82c6e77b0ea",
                    "message": "Update README.md",
                    "timestamp": "2019-05-15T15:20:30Z",
                    "author": {
                        "name": "Codertocat",
                        "email": "21031067+Codertocat@users.noreply.github.com"
                    },
                    "committer": {
                        "name": "Codertocat",
                        "email": "21031067+Codertocat@users.noreply.github.com"
                    }
                }
            },
            "repository": {
                "id": 186853002,
                "node_id": "MDEwOlJlcG9zaXRvcnkxODY4NTMwMDI=",
                "name": "Hello-World",
                "full_name": "Codertocat/Hello-World",
                "private": false,
                "owner": {
                    "login": "Codertocat",
                    "id": 21031067,
                    "node_id": "MDQ6VXNlcjIxMDMxMDY3",
                    "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/Codertocat",
                    "html_url": "https://github.com/Codertocat",
                    "followers_url": "https://api.github.com/users/Codertocat/followers",
                    "following_url": "https://api.github.com/users/Codertocat/following{/other_user}",
                    "gists_url": "https://api.github.com/users/Codertocat/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/Codertocat/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/Codertocat/subscriptions",
                    "organizations_url": "https://api.github.com/users/Codertocat/orgs",
                    "repos_url": "https://api.github.com/users/Codertocat/repos",
                    "events_url": "https://api.github.com/users/Codertocat/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/Codertocat/received_events",
                    "type": "User",
                    "site_admin": false
                },
                "html_url": "https://github.com/Codertocat/Hello-World",
                "description": null,
                "fork": false,
                "url": "https://api.github.com/repos/Codertocat/Hello-World",
                "forks_url": "https://api.github.com/repos/Codertocat/Hello-World/forks",
                "keys_url": "https://api.github.com/repos/Codertocat/Hello-World/keys{/key_id}",
                "collaborators_url": "https://api.github.com/repos/Codertocat/Hello-World/collaborators{/collaborator}",
                "teams_url": "https://api.github.com/repos/Codertocat/Hello-World/teams",
                "hooks_url": "https://api.github.com/repos/Codertocat/Hello-World/hooks",
                "issue_events_url": "https://api.github.com/repos/Codertocat/Hello-World/issues/events{/number}",
                "events_url": "https://api.github.com/repos/Codertocat/Hello-World/events",
                "assignees_url": "https://api.github.com/repos/Codertocat/Hello-World/assignees{/user}",
                "branches_url": "https://api.github.com/repos/Codertocat/Hello-World/branches{/branch}",
                "tags_url": "https://api.github.com/repos/Codertocat/Hello-World/tags",
                "blobs_url": "https://api.github.com/repos/Codertocat/Hello-World/git/blobs{/sha}",
                "git_tags_url": "https://api.github.com/repos/Codertocat/Hello-World/git/tags{/sha}",
                "git_refs_url": "https://api.github.com/repos/Codertocat/Hello-World/git/refs{/sha}",
                "trees_url": "https://api.github.com/repos/Codertocat/Hello-World/git/trees{/sha}",
                "statuses_url": "https://api.github.com/repos/Codertocat/Hello-World/statuses/{sha}",
                "languages_url": "https://api.github.com/repos/Codertocat/Hello-World/languages",
                "stargazers_url": "https://api.github.com/repos/Codertocat/Hello-World/stargazers",
                "contributors_url": "https://api.github.com/repos/Codertocat/Hello-World/contributors",
                "subscribers_url": "https://api.github.com/repos/Codertocat/Hello-World/subscribers",
                "subscription_url": "https://api.github.com/repos/Codertocat/Hello-World/subscription",
                "commits_url": "https://api.github.com/repos/Codertocat/Hello-World/commits{/sha}",
                "git_commits_url": "https://api.github.com/repos/Codertocat/Hello-World/git/commits{/sha}",
                "comments_url": "https://api.github.com/repos/Codertocat/Hello-World/comments{/number}",
                "issue_comment_url": "https://api.github.com/repos/Codertocat/Hello-World/issues/comments{/number}",
                "contents_url": "https://api.github.com/repos/Codertocat/Hello-World/contents/{+path}",
                "compare_url": "https://api.github.com/repos/Codertocat/Hello-World/compare/{base}...{head}",
                "merges_url": "https://api.github.com/repos/Codertocat/Hello-World/merges",
                "archive_url": "https://api.github.com/repos/Codertocat/Hello-World/{archive_format}{/ref}",
                "downloads_url": "https://api.github.com/repos/Codertocat/Hello-World/downloads",
                "issues_url": "https://api.github.com/repos/Codertocat/Hello-World/issues{/number}",
                "pulls_url": "https://api.github.com/repos/Codertocat/Hello-World/pulls{/number}",
                "milestones_url": "https://api.github.com/repos/Codertocat/Hello-World/milestones{/number}",
                "notifications_url": "https://api.github.com/repos/Codertocat/Hello-World/notifications{?since,all,participating}",
                "labels_url": "https://api.github.com/repos/Codertocat/Hello-World/labels{/name}",
                "releases_url": "https://api.github.com/repos/Codertocat/Hello-World/releases{/id}",
                "deployments_url": "https://api.github.com/repos/Codertocat/Hello-World/deployments",
                "created_at": "2019-05-15T15:19:25Z",
                "updated_at": "2019-05-15T15:21:14Z",
                "pushed_at": "2019-05-15T15:20:57Z",
                "git_url": "git://github.com/Codertocat/Hello-World.git",
                "ssh_url": "git@github.com:Codertocat/Hello-World.git",
                "clone_url": "https://github.com/Codertocat/Hello-World.git",
                "svn_url": "https://github.com/Codertocat/Hello-World",
                "homepage": null,
                "size": 0,
                "stargazers_count": 0,
                "watchers_count": 0,
                "language": "Ruby",
                "has_issues": true,
                "has_projects": true,
                "has_downloads": true,
                "has_wiki": true,
                "has_pages": true,
                "forks_count": 0,
                "mirror_url": null,
                "archived": false,
                "disabled": false,
                "open_issues_count": 2,
                "license": null,
                "forks": 0,
                "open_issues": 2,
                "watchers": 0,
                "default_branch": "master"
            },
            "sender": {
                "login": "Codertocat",
                "id": 21031067,
                "node_id": "MDQ6VXNlcjIxMDMxMDY3",
                "avatar_url": "https://avatars1.githubusercontent.com/u/21031067?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/Codertocat",
                "html_url": "https://github.com/Codertocat",
                "followers_url": "https://api.github.com/users/Codertocat/followers",
                "following_url": "https://api.github.com/users/Codertocat/following{/other_user}",
                "gists_url": "https://api.github.com/users/Codertocat/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/Codertocat/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/Codertocat/subscriptions",
                "organizations_url": "https://api.github.com/users/Codertocat/orgs",
                "repos_url": "https://api.github.com/users/Codertocat/repos",
                "events_url": "https://api.github.com/users/Codertocat/events{/privacy}",
                "received_events_url": "https://api.github.com/users/Codertocat/received_events",
                "type": "User",
                "site_admin": false
            }
        }'''

        res = self.cls.parse_event(mock_event_json)

        assert res is not None
        assert isinstance(res, Dict)
        assert res['url'] == 'https://api.github.com/repos/Codertocat/Hello-World'
        assert res['ref'] == 'ec26c3e57ca3a959ca5aad62de7213c562f8c821'

class TestGetFiles(GithubProviderPluginTester):

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

class TestCreateProject(GithubProviderPluginTester):

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

class TestDeleteProject(GithubProviderPluginTester):

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
    
class TestUpdateProject(GithubProviderPluginTester):

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
