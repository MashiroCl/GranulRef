"""
retrace: for matching the CGRs in different coarse granularities,
e.g. for a coarse granularity 3 coarse grained commit (3by3), the refs detected
are required to match the refs detected from coarse granularity 2 coarse grained commit (2by2),
            commits: 0-1-2-3
            squash 1,2,3 into c
            1,2 was squahsed into coarse-grained commit c1, 2,3 was squashed into c2
            refs detected from s required to match refs detected from c1 and refs detected from c2
            retrace the locations of refs in c1 and c2, for example for a ref in c2, we checkout to commit 1 and apply
            git blame with --ignore-rev of commit 1 to trace the source location of the first line of the being
            refactored element.


Retrace target granularity ranged from 2 to 4 (because the maximum coarse granularity is 5, and coarse-granularity-5
don't need retrace)
"""
import subprocess
import json
import pathlib
from refactoring_operation.refactoring import Refactoring
from match import load_commit_pairs_all
from line_trace import BlameRes
import re
import argparse


class CommitHistory:
    def __init__(self, repo):
        self.repo = repo
        self.commits = []

class RetracedCommitHistory:
    def __init__(self, repo):
        self.repo = repo
        self.retraced_commits = []


def get_parent_sha1(git_path, sha1) -> str:
    command = f'git --git-dir={git_path} log --pretty=format:"%H" -n 1 {sha1}^'
    return subprocess.getoutput(command)


class CoarseGrainedCommit:
    def __init__(self, file, coarse_granularity=1):
        self.file = file
        self.sha1 = ""
        self.coarse_granularity = coarse_granularity
        self.refs = []
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

    def get_parents(self, git_path, squash_log, length):
        try:
            earliest_commit = squash_log[self.sha1][-1]
        except KeyError:
            print("Errored key is ", self.sha1)
        parents = []
        cur_commit = earliest_commit
        for i in range(length):
            cur_commit = get_parent_sha1(git_path, cur_commit)
            parents.append(cur_commit)
        return parents


class RetraceCommit:
    def __init__(self, cgc: CoarseGrainedCommit):
        self.cgc = cgc
        self.sha1 = cgc.sha1
        self.coarse_granularity = cgc.coarse_granularity
        self.retraced_refs = dict()

    def retrace(self, git_path, squash_log):
        for i in range(1, 5 - self.coarse_granularity + 1):
            ignored_commits = self.cgc.get_parents(git_path, squash_log, i)
            traced_refs = []
            for ref in self.cgc.refs:
                # if isValidRef(traced_ref):
                ref.refactored_source_location = trace(ref, git_path, ignored_commits[0], ignored_commits)
                traced_refs.append(ref)
            if len(traced_refs):
                retraced_refs = RetracedRefs(ignored_commits, traced_refs)
                self.retraced_refs[len(ignored_commits)] = retraced_refs.__dict__()
        return self


class Ref:
    def __init__(self):
        self.type = None
        self.location = None


class RetracedRefs:
    def __init__(self, ignored_commits, traced_refs):
        self.ignored_commits = ignored_commits
        self.refs = traced_refs

    def __dict__(self):
        return {
            "ignored_commits": self.ignored_commits,
            "refs": [each.get_dict_format() for each in self.refs]
        }


def get_blame_res(git_path, line_numbers: tuple[str, str], file_path: str, checkout_commit,
                  ignore_commits: list[str]) -> list[BlameRes]:
    """
    use git-blame to trace the line number when code of line_numbers are last modified
    :param ignore_commits:
    :param git_path: path/to/repo/.git
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

    def generate_command(git_path, checkout_commit, path) -> str:
        command = f"git --git-dir={git_path} blame --line-porcelain {checkout_commit} "
        for ignore_commit in ignore_commits:
            command = command + f"--ignore-rev {ignore_commit} "
        command = command + f"-L {line_numbers[0]},{line_numbers[1]} {path}"
        return command

    file_path = pathlib.Path(file_path) if not isinstance(file_path, pathlib.Path) else file_path
    file_path.joinpath(".git")
    res = subprocess.getoutput(generate_command(git_path, checkout_commit, file_path))
    return parse(res)


def trace(ref, git_path, checkout_commit, ignored_commits):
    res = get_blame_res(git_path,
                        (ref.refactored_location.startLine, ref.refactored_location.startLine),
                        ref.refactored_location.file_path,
                        checkout_commit,
                        ignored_commits)
    return res


def load_CGCs(path: str):
    cgcs = {}
    for i in range(2, 5):
        cgcs[i] = []
        folder_coarse = pathlib.Path(path).joinpath(str(i), "refs")
        for cgc_file in folder_coarse.iterdir():
            cgc = CoarseGrainedCommit(cgc_file, i)
            if cgc.sha1:  # RM result of the initial commit does not contain any information
                cgcs[i].append(cgc)
    return cgcs

def command():
    parser = argparse.ArgumentParser(description="retrace the last modified locations for refs in coarse-grained commits")
    parser.add_argument("-t", help="retrace target path")
    parser.add_argument("-r", help="repository path")
    return parser


if __name__ == "__main__":
    args = command().parse_args()
    path = args.t
    cgcs = load_CGCs(args.t)
    squash_log = load_commit_pairs_all(path)
    repo = args.r
    git_path = repo + "/.git"
    res_p = pathlib.Path(path).joinpath("retrace")
    res_p.mkdir(parents=True, exist_ok=True)

    for key in cgcs.keys():
        for cgc in cgcs[key]:
            rc = RetraceCommit(cgc)
            rc.retrace(git_path, squash_log)

            # create json file
            p = res_p.joinpath(str(rc.coarse_granularity))
            p.mkdir(exist_ok=True)
            if not len(rc.retraced_refs):   # skip no ref commits
                continue
            with open(p.joinpath(rc.sha1 + ".json"), "w") as f:
                json.dump(rc.retraced_refs, f)
