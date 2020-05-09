#!/usr/bin/env python
import argparse
import logging
import os
import pathlib

from octostarfish import Octostarfish


parser = argparse.ArgumentParser(description=(
    'Clone GitHub repositories that have been starred by a given user.'))
parser.add_argument(
    '-u', '--user', default=os.getenv('GITHUB_USER'),
    help='GitHub user whose stars should be cloned')
parser.add_argument(
    '-t', '--token', default=os.getenv('GITHUB_API_TOKEN'),
    help='GitHub API token')
parser.add_argument(
    'clones_root', type=pathlib.Path,
    help='Base directory under which clones will be created')


logger = logging.getLogger('octostarfish')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__':
    args = parser.parse_args()
    Octostarfish.run(args.user, args.token, args.clones_root)
