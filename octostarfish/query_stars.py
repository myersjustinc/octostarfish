import logging
from textwrap import dedent

import requests

from .repo import Repo


logger = logging.getLogger(__name__)


def _build_query(user, cursor=None):
    """Generate a GraphQL query for a user's stars.

    Positional arguments:
    user - A string username for a GitHub user.
    cursor - An optional string cursor ID for a page of API results.

    Returns a string.
    """
    return dedent(
        """
        {{
          user(login: "{user}") {{
            starredRepositories(after: {cursor}) {{
              totalCount
              edges {{
                node {{
                  nameWithOwner
                  url
                  defaultBranchRef {{
                    name
                  }}
                }}
                cursor
              }}
              pageInfo {{
                endCursor
                hasNextPage
              }}
            }}
          }}
        }}
        """.format(
            user=user,
            cursor=('null' if cursor is None else '"{0}"'.format(cursor))))


def _run_query(query, token):
    """Run a query against the GitHub GraphQL API.

    Positional arguments:
    query - A string query to run.
    token - A string GitHub API token (personal access token).

    Returns a dict.
    """
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    r = requests.post(url, headers=headers, json={'query': query})
    return r.json()


def _build_repo(edge):
    """Generate a Repo object for a given project.

    Positional arguments:
    edge - A dict of GraphQL results data.

    Returns an octostarfish.repo.Repo.
    """
    return Repo(
        edge['node']['nameWithOwner'],
        edge['node']['url'] + '.git',
        edge['node']['defaultBranchRef']['name'])


def query_stars(user, token):
    """Query GitHub's GraphQL API for a user's stars.

    Positional arguments:
    user - A string username for a GitHub user.
    token - A string GitHub API token (personal access token).

    Returns a generator of octostarfish.repo.Repos.
    """
    cursor = None
    has_next_page = True
    page_num = 0
    repos_so_far = 0
    while has_next_page:
        page_num += 1
        query = _build_query(user, cursor)
        response = _run_query(query, token)
        raw_repos = response['data']['user']['starredRepositories']
        edges = raw_repos['edges']
        repos_so_far += len(edges)
        logger.info('Retrieved page {0} ({1}/{2})'.format(
            page_num, repos_so_far, raw_repos['totalCount']))
        cursor = raw_repos['pageInfo']['endCursor']
        has_next_page = raw_repos['pageInfo']['hasNextPage']
        for edge in edges:
            yield _build_repo(edge)
