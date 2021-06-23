import os
from eds.plugins.github_provider import GithubProvider


def test_github():
    g = GithubProvider(token_env_var='GITHUB_PAT')


def test_github_enterprise():
    g = GithubProvider(token_env_var='GHE_PAT', github_enterprise_url=os.getenv('GHE_URL'))

