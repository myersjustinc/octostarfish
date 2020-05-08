import sys


class Octostarfish(object):
    """Expose all public functionality.

    Use `Octostarfish.run()` to kick things off!
    """
    @classmethod
    def run(cls, user, token):
        """Run the Octostarfish job."""
        fish = cls(user, token)
        # TODO: Keep going.

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
