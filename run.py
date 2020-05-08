#!/usr/bin/env python
import argparse
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
args = parser.parse_args()


Octostarfish.run(args.user, args.token, args.clones_root)
