#!/usr/bin/env python3

import os
import re

import pandas as pd

import click
from github import Github

"""
Given text contains GitHub urls, fetch their star and order desc
"""


def get_repos(text):
    exp = re.compile('https:\/\/github\.com\/([a-z\-_0-9]*)\/([a-z\-_0-9]*)')
    res = exp.findall(text)
    return [c[0] + '/' + c[1] for c in res]

@click.command(help='given text contains GitHub urls, fetch their star and order desc')
@click.argument('file')
def star(file):
    with open('token', 'r') as f:
        access_token = f.read().rstrip()
    g = Github(access_token)
    with open(file, 'r') as f:
        repo_names = get_repos(f.read())
    repos = []
    # FIXME: it seems progress bar is not working
    with click.progressbar(length=len(repo_names)) as bar:
        for repo_name in repo_names:
            print(repo_name)
            repo = g.get_repo(repo_name)
            repos.append({
                'name': repo.full_name,
                'url': repo.html_url,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'watchers': repo.watchers_count,
                'issues': repo.open_issues_count,
                'created_at': repo.created_at,
                'pushed_at': repo.pushed_at,
                'updated_at': repo.updated_at
            })
            # bar.update(1)
    df = pd.DataFrame(repos)
    saved_file = file + '.csv'
    df.to_csv(saved_file, index=False)
    print('saved to', saved_file)


if __name__ == '__main__':
    star()
