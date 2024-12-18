import argparse
import json
import pathlib
import re
import subprocess
from pathlib import Path
from utils import load_commit_pairs_all
from line_trace import BlameRes
from refactoring_operation.refactoring import Refactoring


class CommitRef:
    def __init__(self, file, coarse_granularity):
        self.file: str = file
        self.sha1: str = ""
        self.coarse_granularity: int = coarse_granularity
        self.refs: list[Refactoring] = []
        self._load_ref_file()

    def _load_ref_file(self):
        with open(self.file) as f:
            c = json.load(f)
            if len(c["commits"]):  # exclude the most initial commit
                self.sha1 = c["commits"][0]["sha1"]
                self._load_refs(c)

    def _load_refs(self, c):
        for ref in c["commits"][0]["refactorings"]:
            if ref[
                "type"] == "Move Source Folder":  # exclude Move Source Folder because it contains neither leftSideLocation nor rightSideLocation
                continue
            self.refs.append(Refactoring(ref))


def get_blame_res(line_numbers: tuple[int, int], blame_at_commit: str, blamed_file_path: str,
                  ignore_commits: list[str], repo_git_path) -> list[BlameRes]:
    """
    use git-blame to trace the line number when code of line_numbers are firstly introduced
    :param blame_at_commit: commit sha1 where blame starts (the parent commit of the target commit)
    :param ignore_commits:
    :param blamed_file_path: file path where code change lies
    :param line_numbers: a tuple (start_line, end_line)
    :param ignore_commits: the commits should be ignore when tracing in git blame api --ignore-rev
    :return:
    """

    def is_commit_sha1(s: str) -> bool:
        if len(s) != 40:
            return False
        return bool(re.compile("[0-9a-f]{40}").match(s))

    def is_file_line(s: str) -> bool:
        # to find the line that indicates the file path of the blame result
        if "filename " in s and s.endswith(
                ".java"):  # ensure that the line is in the form of filename src/.../StepGraph.java
            return True
        return False

    def parse(output) -> list[BlameRes]:
        # print("--------------------start-----------------------")
        # print("output", output)
        blameRes_list = []
        properties = [each for each in output.split("\n") if
                      is_file_line(each.strip()) or is_commit_sha1(each.split(" ")[0].strip())]
        # print("properties", properties)
        for i in range(0, len(properties), 2):
            sha1, oline = properties[i].split(" ")[:2]
            try:
                file_name = properties[i + 1].split("filename ")[1]
            except IndexError:
                print("IndexError")
                print("properties", properties)
            blameRes_list.append(BlameRes(sha1, oline, file_name))
        return blameRes_list

    def generate_command(file_path, git_path, blame_at_commit) -> str:
        command = f"git --git-dir={git_path} blame --line-porcelain {blame_at_commit} "
        for ignore_commit in ignore_commits:
            command = command + f"--ignore-rev {ignore_commit} "
        command = command + f"-L {line_numbers[0]},{line_numbers[1]} {file_path}"
        return command

    blamed_file_path = Path(blamed_file_path) if not isinstance(blamed_file_path, Path) else blamed_file_path
    res = subprocess.getoutput(generate_command(blamed_file_path, repo_git_path, blame_at_commit))
    return parse(res)


def get_parent_sha1(git_path, sha1) -> str:
    command = f'git --git-dir={git_path} log --pretty=format:"%H" -n 1 {sha1}^'
    return subprocess.getoutput(command)


def trace(commit: CommitRef, parent_commit_sha1, ignored_commits: list[str], git_path):
    for ref in commit.refs:
        res = get_blame_res(
            line_numbers=(ref.refactored_location.startLine, ref.refactored_location.startLine),
            blame_at_commit=parent_commit_sha1,
            blamed_file_path=ref.refactored_location.file_path,
            ignore_commits=ignored_commits,
            repo_git_path=git_path)[0].to_dict()
        ref.traced_location[len(ignored_commits)] = res


def load_commitRefs(path: str):
    granularity_commit = {}
    for i in range(1, 6):
        granularity_commit[i] = []
        folder_granularity = Path(path).joinpath(str(i), "refs")
        for cr_file in folder_granularity.iterdir():
            cr = CommitRef(cr_file, i)
            if cr.sha1:  # RM result of the initial commit does not contain any information
                granularity_commit[i].append(cr)
    return granularity_commit


def get_ignored_commits(normal_grained_commit_sha1: str, granularity, commit_parent_map):
    parent_commits = commit_parent_map.get(normal_grained_commit_sha1, [])
    # for a commit with granularity g, the number of commits should be ignored N = [0, min(num_pCommit_in_SCS, (5-g))]
    # in parent_commits, higher index commits are proposed earlier (nearer parent commits for the target commit)
    # range for ignorable commit in parent_commits should be [-N:]
    return parent_commits[:min(len(parent_commits), 5 - granularity)] if granularity != 5 else []


def trace_for_repository(straight_commit_sequences: list[list[str]], commitRef_path: str, git_path: str) -> None:
    # get parent commits in each straight commit sequence
    commit_parent_map = get_commit_parent_map(straight_commit_sequences)

    coarse_normal_commit_map = load_commit_pairs_all(commitRef_path)

    # for commit_ref in repo/{granularity}/refs trace for each ref
    granularity_commitRef = load_commitRefs(commitRef_path)

    for granularity in range(1, 6):
        Path(commitRef_path).joinpath("o" + str(granularity)).mkdir(parents=True, exist_ok=True)
        for commitRef in granularity_commitRef[granularity]:
            if not commitRef.refs:  # skip commits that haven't commits
                continue

            traced_commit = {"sha1": commitRef.sha1}
            # e.g. {c6: c1 c2 c3 c4 c5}  ignorable_commits = {c2 c3 c4 c5}
            # e.g. {c6: c5} ignorable_commits = {c5}
            ignorable_commits = get_ignored_commits(
                commitRef.sha1 if commitRef.coarse_granularity == 1 else coarse_normal_commit_map.get(commitRef.sha1)[
                    -1], granularity, commit_parent_map)
            parent_commit_sha1 = get_parent_sha1(git_path, commitRef.sha1 if commitRef.coarse_granularity == 1 else
            coarse_normal_commit_map.get(commitRef.sha1)[-1])

            for l in range(0, len(ignorable_commits) + 1):  # ignored commit range [0: min(4, len(ignorable_commits)]
                ignored_commits = ignorable_commits[:l] if l != 0 else []  # 0 ignored commit
                trace(commit=commitRef, parent_commit_sha1=parent_commit_sha1, ignored_commits=ignored_commits,
                      git_path=git_path)

            traced_commit["refactorings"] = [each.to_traced_dict() for each in commitRef.refs]
            with open(Path(commitRef_path).joinpath("o" + str(granularity)).joinpath(commitRef.sha1 + ".json"),
                      "w") as outfile:
                json.dump(traced_commit, outfile)


def load_straight_commit_sequences(path: str) -> list[list[str]]:
    straight_commit_sequences = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        if "Straight commit sequences: " in line:
            return eval(line.split("Straight commit sequences: ")[1])
    return straight_commit_sequences


def get_commit_parent_map(commit_sequences: list[list[str]]):
    parent_map = {}
    for commit_sequence in commit_sequences:
        for i, commit in enumerate(commit_sequence):
            parent_map[commit] = commit_sequence[i + 1:] if i < len(commit_sequence) - 1 else []
    return parent_map


def commands():
    # example
    # python3 trace.py -f /Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador_cr -r /Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador_cr/.git

    parser = argparse.ArgumentParser(description="Trace the last-modified locations for the refactorings")
    parser.add_argument("-f", help="Refactoring folder path")
    parser.add_argument("-r", help="Repository .git path")
    return parser


if __name__ == "__main__":
    args = commands().parse_args()
    commitRef_path = args.f
    repo_path = args.r
    straight_commit_sequence_path = Path(commitRef_path).joinpath("1").joinpath("log1.txt")
    trace_for_repository(load_straight_commit_sequences(str(straight_commit_sequence_path)), commitRef_path, repo_path)

    # mbassador_straight_commit_sequence_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador_cr/1/log1.txt"
    # commitRef_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador_cr/"
    # repo_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador_cr/.git"
    #
    # straight_commit_sequences = load_straight_commit_sequences(mbassador_straight_commit_sequence_path)
    # commit_parent_map = get_commit_parent_map(straight_commit_sequences)
    #
    # trace_for_repository(straight_commit_sequences, commitRef_path, repo_path)

    # refactoring_toy_example_commit_sequence_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/refactoring-toy-example_cr/1/log1.txt"
    # refactoring_toy_example_commitRef_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/refactoring-toy-example_cr/"
    # refactoring_toy_example_repo_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/refactoring-toy-example_cr/.git"
    #
    # straight_commit_sequences = load_straight_commit_sequences(refactoring_toy_example_commit_sequence_path)
    # commit_parent_map = get_commit_parent_map(straight_commit_sequences)
    #
    # trace_for_repository(straight_commit_sequences, refactoring_toy_example_commitRef_path,
    #                      refactoring_toy_example_repo_path)
