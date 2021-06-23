import os
from eds.plugins.github_provider import GithubProvider


def test_github():
    g = GithubProvider(token_env_var='GITHUB_PAT')
    dir_contents = g.get_files(owner="manheim", repo_name="eds")
    print(f'{dir_contents}')
    assert dir_contents is not None



def test_github_enterprise():
    ghe = GithubProvider(token_env_var='GHE_PAT', github_enterprise_url=os.getenv('GHE_URL', None))
    dir_contents = ghe.get_files(owner="CAIS-Accounts", repo_name="awsmanretnp")
    print(f'{dir_contents}')
    assert dir_contents is not None

