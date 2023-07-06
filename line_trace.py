import glob
import pathlib
import re
import subprocess
from repository import Repository
from dataclasses import dataclass


def load_commits(directory: str):
    """

    :param directory: a directory contain json files whose names are fine-grained commit sha1
    :return:
    """
    json_files = glob.glob(pathlib.Path(directory).joinpath("*.json").__str__())
    for f in json_files:
        pass


def load_commit_pairs(squash_log_path: str) -> dict[str:tuple]:
    """
    For corase-grained commits in the squash log, find the corresponding fine-grained commits for them
    :param squash_log_path: squash log
    :return:a dict where key is the coarse-grained commit sha1,
    values is the fine-grained commits which squashed into the key
    """

    def match(key_commits: list[str], value_commits: list[str]) -> None:
        if not len(key_commits) == len(value_commits):
            raise RuntimeError(
                f"length of fine grained commits is not equal with coarse grained commits in\n file: {squash_log_path}\n line: {line}")
        for i, v in enumerate(key_commits):
            pairs[v] = tuple(value_commits[i])

    pairs = dict()
    with open(squash_log_path) as f:
        data = f.readlines()[1:-1]  # remove the start squash & finish squash notice line
    for i, line in enumerate(data):
        if i % 2 == 0 and "squash units list " in line:  # fine_grained commit line
            fine_grained_commits = eval(line.split("squash units list")[1])
            coarse_grained_commits = eval(data[i + 1].split("coarse-grained commit list ")[1])
            match(coarse_grained_commits, fine_grained_commits)
    return pairs

def get_normal_grained_ref_map()->dict:
    """
    For load each group of normal grained refs in the squash log, and build a hashmap where the key is one of the normal
    grained ref in the group, the values are the group
    e.g. [[C1,C2],[C2,C3]] -> {C1:[C1,C2], C2:[C1,C2], C3:[C2,C3]}
    :return:
    """

def get_parent_commit(commit: str, repo: Repository) -> str:
    """
    get parent commmit sha1
    :param commit: sha1
    :param repo: target repository
    :return: parent commmt sha1
    """

    def parse(output: str):
        if "parent " not in output:  # Initial commit doesn't have parent commit
            return ""
        return [line.split("parent ") for line in output.split("\n") if "parent " in line][0][1]

    commit_info = subprocess.getoutput(f"cd {repo.repoPath} && git cat-file -p {commit}")
    return parse(commit_info)


def checkout(repo: Repository, commit):
    """
    git checkout to certain commit
    :param repo:
    :param commit:
    :return:
    """
    res = subprocess.getoutput(f"cd {repo.repoPath} && git checkout {commit}")
    if "fatal:" in res:
        raise RuntimeWarning(f"Error occurs when git checkout to {commit}")


def checkout_latest(repo: Repository):
    """
    git checkout to the most recent commit
    :param repo:
    :return:
    """
    print(f"checkout to the latest commit for {repo.repoPath}")
    res = subprocess.getoutput(f'cd {repo.repoPath} && git checkout $(git log --branches -1 --pretty=format:"%H")')
    if "fatal:" in res:
        raise RuntimeWarning(f"Error occurs when git checkout to the latest commit")


@dataclass
class BlameRes:
    """
    result of git blame
    https://git-scm.com/docs/git-blame#_the_porcelain_format
    """
    sha1: str  # 40-byte SHA-1 of the commit the line is attributed to
    oline: str  # the line number of the line in the original file;
    file_name: str  # the filename in the commit that the line is attributed to.


def get_blame_res(line_numbers: tuple[str, str], file_path: str, ignore_commits: list[str]) -> list[BlameRes]:
    """
    use git-blame to trace the line number when code of line_numbers are firstly introduced
    :param ignore_commits:
    :param file_path: file path where code change lies
    :param line_numbers: a tuple (start_line, end_line)
    :param ignore_commits: the commits should be ignore when tracing in git blame api --ignore-rev
    :return:
    """

    def is_commit_sha1(s: str) -> bool:
        if len(s) != 40:
            return False
        return bool(re.compile("[0-9a-f]{40}").match(s))

    def parse(output) -> list[BlameRes]:
        blameRes_list = []
        properties = [each for each in output.split("\n") if
                      "filename " in each or is_commit_sha1(each.split(" ")[0].strip())]
        for i in range(0, len(properties), 2):
            sha1, oline = properties[i].split(" ")[:2]
            file_name = properties[i + 1].split("filename ")[1]
            blameRes_list.append(BlameRes(sha1, oline, file_name))
        return blameRes_list

    def generate_command(path) -> str:
        command = f"cd {path.parent} && git blame --line-porcelain "
        for ignore_commit in ignore_commits:
            command = command + f"--ignore-rev {ignore_commit} "
        command = command + f"-L {line_numbers[0]},{line_numbers[1]} {path}"
        print(command)
        return command

    file_path = pathlib.Path(file_path) if not isinstance(file_path, pathlib.Path) else file_path
    res = subprocess.getoutput(generate_command(file_path))
    return parse(res)


def trace(line_numbers: tuple[str, str], commit: str, file_path: str, repo: Repository, ignore_commits:'list[Commit]'=None) -> list[
    BlameRes]:
    """
    trace when code of certain lines is initially introduced into repo under certain commit
    :param ignore_commits:
    :param line_numbers: start & end line numbers of the target trace lines
    :param commit: sha1 of a commit, trace under this parameter (git checkout to this commit   then trace)
    :param file_path: traced file
    :param repo: traced repo
    :param ignore_commits: the commits should be ignore when tracing in git blame api --ignore-rev
    :return:
    """
    if ignore_commits is None:
        ignore_commits = []
    checkout(repo, commit)
    blameRes_ls = get_blame_res(line_numbers, file_path, [each.sha1 for each in ignore_commits])
    checkout_latest(repo)
    return blameRes_ls
