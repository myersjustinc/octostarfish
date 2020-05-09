import sys


class Octostarfish(object):
    """Expose all public functionality.

    Use `Octostarfish.run()` to kick things off!
    """
    @classmethod
    def run(cls, user, token, clones_root):
        """Run the Octostarfish job."""
        fish = cls(user, token)
        for repo in fish.stars():
            fish.clone(repo, clones_root)

    def __init__(self, user, token):
        if user is None:
            sys.stderr.write(
                'You must specify a user with --user or the GITHUB_USER '
                'environment variable.\n')
            sys.exit(1)
        if token is None:
            sys.stderr.write(
                'You must specify a token with --token or the '
                'GITHUB_API_TOKEN environment variable.\n')
            sys.exit(1)
        self.user = user
        self.token = token

    def clone(self, repo, clones_root):
        """Manage a clone of a given repository.

        Positional arguments:
        repo - An octostarfish.repo.Repo.
        clones_root - A path-like object one level representing the parent
            directory of the clone.
        """
        repo.clone(clones_root / repo.gh_path)

    def stars(self):
        """Retrieve the user's starred repositories.

        Returns a sequence of octostarfish.repo.Repos.
        """
        return ()  # TODO: Add this.
