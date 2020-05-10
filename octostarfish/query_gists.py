import logging
import re

import requests

from .repo import Repo


logger = logging.getLogger(__name__)


def _get_next_url(link_header):
    """Get the URL for the following page.

    Positional arguments:
    link_header - A string value of the current page's `Link` header.

    Returns a string URL or None.
    """
    try:
        return re.match(r'<(.+?)>; rel="next"', link_header).group(1)
    except AttributeError:
        return None


def _get_page(url, user, token):
    """Get a page of results from GitHub's REST API.

    Positional arguments:
    url - A string URL for a page to request. If None, request the
        default first page of starred gists.

    Returns a tuple with two elements: a sequence of dict results and
        a string URL of the following page, if available (or None
        otherwise).
    """
    if url is None:
        url = 'https://api.github.com/gists/starred'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    r = requests.get(url, headers=headers, auth=(user, token))
    try:
        next_url = _get_next_url(r.headers['Link'])
    except KeyError:
        next_url = None
    return (r.json(), next_url)


def _build_repo(raw_result):
    """Generate a Repo object for a given gist.

    Positional arguments:
    raw_result - A dict of information from the REST API about a given
        gist.

    Returns an octostarfish.repo.Repo.
    """
    gist_id = raw_result['id']
    gist_username = raw_result['owner']['login']
    return Repo(
        '{0}/{1}'.format(gist_username, gist_id),
        raw_result['git_pull_url'],
        'master')


def query_gists(user, token):
    """Query GitHub's REST API for a user's starred gists.

    Positional arguments:
    user - A string username for a GitHub user.
    token - A string GitHub API token (personal access token).

    Returns a generator of octostarfish.repo.Repos.
    """
    page_number = 0
    next_page_url = None
    while True:  # oh no, infinite loop
        page_number += 1
        logger.info('Getting page {0} of starred gists'.format(page_number))
        results, next_page_url = _get_page(next_page_url, user, token)
        for result in results:
            yield _build_repo(result)
        if next_page_url is None:
            break  # whew, loop's not actually infinite
