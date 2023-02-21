import json
import pathlib
from typing import Union
from line_trace import load_commit_pairs
from refactoring_operation.refactoring import Refactoring


def load_dictref(file_p: Union[str, pathlib.Path]) -> list[Refactoring]:
    refs = []
    if not pathlib.Path(file_p).exists():
        return refs
    with open(file_p) as f:
        data = json.load(f)
    for ref_d in data:
        refs.append(Refactoring(ref_d).set_source_location(ref_d))
    return refs


def get_commit_refdict(squash_log_p: str, commits: Union[str, list[str]]) -> list[list[Refactoring]]:
    refs_d = pathlib.Path(squash_log_p).parent.parent
    squash_num = pathlib.Path(squash_log_p).name.split(".txt")[0].split("log")[1]
    refs = []
    if isinstance(commits, list):  # fine grained commits
        fine_grained_path = refs_d.joinpath("o1")
        for commit in commits:
            refs.append(load_dictref(fine_grained_path.joinpath(commit+".json")))
    else:       # coarse grained commits
        coarse_grained_path = refs_d.joinpath(f"o{squash_num}")
        refs.append(load_dictref(coarse_grained_path.joinpath(commits+".json")))
    return refs


def extract_coarse_grained_refs(coarse_grained_refs: list[list[Refactoring]],
                                fine_grained_refs: list[list[Refactoring]]) -> list[Refactoring]:
    return list(set(coarse_grained_refs[0]) - set([ref for each in fine_grained_refs for ref in each]))


def get_coarse_grained_refs(squash_log_p: str) -> list[Refactoring]:
    d = load_commit_pairs(squash_log_p)
    CGRs = list()
    for coarse_grained_commit in d.keys():
        fine_grained_commits = d[coarse_grained_commit]
        fine_grained_refs = get_commit_refdict(squash_log_p, list(fine_grained_commits))
        coarse_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)
        CGRs += extract_coarse_grained_refs(coarse_grained_refs, fine_grained_refs)

    return CGRs
