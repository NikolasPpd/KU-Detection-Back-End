import git
from core.utils import is_file_accepted


def get_commit_count(repo: git.Repo, branch_name: str = None) -> int:
    """Gets the total number of commits in the given branch of the given repository.
    Ignore the branch_name parameter to get the number of commits in the active branch.

    :param repo: The repository to get the commit count from.
    :param branch_name: The name of the branch to get the commit count from.
    :return: The total number of commits in the given branch of the given repository."""
    branch_name = branch_name or repo.active_branch.name
    return repo.git.rev_list("--count", branch_name, no_merges=True)


def get_author_commit_counts(repo: git.Repo, branch_name: str = None) -> dict:
    """Gets the number of commits per author in the given branch of the given repository.
    Ignore the branch_name parameter to get the number of commits in the active branch.

    :param repo: The repository to get the commit count from.
    :param branch_name: The name of the branch to get the commit count from.
    :return: A dictionary mapping authors to the number of commits they have made
    in the given branch of the given repository."""
    authors = {}
    for commit in repo.iter_commits(branch_name, no_merges=True):
        author_name = commit.author.name
        author_email = commit.author.email
        identifier = f"{author_name} <{author_email}>"

        if identifier not in authors:
            authors[identifier] = {
                "name": author_name,
                "email": author_email,
                "number_of_commits": 1
            }
        else:
            authors[identifier]["number_of_commits"] += 1

    return authors


def get_commits_by_author(repo: git.Repo, author: dict, branch_name: str = None) -> list:
    """Gets a list of commit hashes for the given author in the given branch of the given repository.
    Ignore the branch_name parameter to get the number of commits in the active branch.

    :param repo: The repository to get the commit count from.
    :param author: A dictionary containing the name and email of the author.
    :param branch_name: The name of the branch to get the commit count from.
    :return: A list of commit hashes for the given author in the given branch of the given repository.
    Sorted from newest to oldest.
    """
    author_name = author["name"]
    author_email = author["email"]
    branch_name = branch_name or repo.active_branch.name

    commits = []
    for commit in repo.iter_commits(branch_name, no_merges=True):
        if commit.author.name == author_name and commit.author.email == author_email:
            commits.append(commit.hexsha)

    return commits


def get_changed_files(repo: git.Repo, commit_hashes: list, accepted_file_types: list = None) -> dict:
    """Given a path to a git repository and a list of commit hashes, return a dictionary containing
    files changed in that commit.

    :param repo: The repository that contains the commits.
    :param commit_hashes: A list of commit hashes.
    :param accepted_file_types: A list of file types to include in the results. All other file types will be excluded.
    Ignore this parameter to include all file types.
    :return: A dictionary where 'keys' are commit hashes and 'values' are lists of paths to files
    changed in that commit.
    """
    commit_files = {}
    for hexsha in commit_hashes:
        commit = repo.commit(hexsha)
        files_changed = []

        # Check if the commit has a parent
        if commit.parents:
            diffs = commit.diff(commit.parents[0])

            # Getting a list of files changed for the commit
            for diff in diffs:
                # If the file type is not in the accepted file types list, skip it
                # if accepted_file_types and get_file_extension(diff.a_path) not in accepted_file_types:
                if not is_file_accepted(diff.a_path, accepted_file_types):
                    continue
                files_changed.append(diff.a_path)
        else:
            # If it's the root commit, list all files added in that commit
            files_changed = [item.a_path for item in commit.tree.traverse()]

        if files_changed:
            commit_files[hexsha] = files_changed

    return commit_files
