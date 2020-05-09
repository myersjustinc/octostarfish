import git


class InvalidRepoError(git.exc.InvalidGitRepositoryError):
    pass
