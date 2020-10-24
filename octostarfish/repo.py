import logging

import git

from .exceptions import InvalidRepoError


logger = logging.getLogger(__name__)


class Repo(object):
    """Manage the state of a local GitHub repo's clone."""
    def __init__(self, gh_path, clone_url, default_branch):
        self.gh_path = gh_path
        self.clone_url = clone_url
        self.default_branch = default_branch

    def clone(self, clone_path):
        """Create or update a clone.

        Positional arguments:
        clone_path - A path-like object to the clone's local directory.
        """
        try:
            repo = git.Repo(clone_path)
            remote = repo.remotes['origin']
            logger.info('Found {0} clone at {1}'.format(
                self.gh_path, clone_path))
            repo.git.config('core.filemode', 'false')
            repo.head.reset(index=True, working_tree=True)
            logger.debug('Ensured {0} is reset'.format(clone_path))
        except git.exc.NoSuchPathError:
            logger.debug('Cloning {0} to {1}'.format(self.gh_path, clone_path))
            repo = git.Repo.init(clone_path)
            remote = repo.create_remote('origin', self.clone_url)
            remote.fetch()
            remote_ref = getattr(remote.refs, self.default_branch)
            branch = repo.create_head(self.default_branch, remote_ref)
            branch.set_tracking_branch(remote_ref)
            branch.checkout()
            logger.info('Cloned {0} to {1}'.format(self.gh_path, clone_path))
        except git.exc.InvalidGitRepositoryError:
            raise InvalidRepoError('{0} is not a valid Git repository'.format(
                clone_path))
        remote.pull(force=True)
        logger.info('Pulled {0}'.format(self.gh_path))
