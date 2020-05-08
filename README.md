# Octostarfish #

Clones all repos that have been starred by a given GitHub user and keeps those
clones up to date.

## Usage ##

```sh
$ poetry install
$ export GITHUB_API_TOKEN='TOKEN_GOES_HERE'
$ export GITHUB_USER='USERNAME_WHOSE_STARS_GET_CLONED'
$ poetry run ./run.py
```
