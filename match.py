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


def get_commit_refdict(squash_log_p: str, commits: Union[str, list[str]], coarse_grained_commit: str = "") -> list[
    list[Refactoring]]:
    refs_d = pathlib.Path(squash_log_p).parent.parent
    squash_num = pathlib.Path(squash_log_p).name.split(".txt")[0].split("log")[1]
    refs = []
    if isinstance(commits, list):  # normal grained commits
        if len(coarse_grained_commit) == 0:
            raise Exception("Coarse grained commit miss, directory for normal grained commits not set")
        fine_grained_path = refs_d.joinpath(f"o{squash_num}").joinpath(coarse_grained_commit)
        for commit in commits:
            refs.append(load_dictref(fine_grained_path.joinpath(commit + ".json")))
    else:  # coarse grained commits
        coarse_grained_path = refs_d.joinpath(f"o{squash_num}")
        refs.append(load_dictref(coarse_grained_path.joinpath(commits + ".json")))
    return refs


def extract_coarse_grained_refs(coarse_grained_refs: list[list[Refactoring]],
                                normal_grained_refs: list[list[Refactoring]]) -> list[Refactoring]:
    return list(set(coarse_grained_refs[0]) - set([ref for each in normal_grained_refs for ref in each]))


def extract_coarse_grained_refs_by_squashlog(squash_log_p: str) -> list[Refactoring]:
    d = load_commit_pairs(squash_log_p)
    res = list()
    for coarse_grained_commit in d.keys():
        fine_grained_commits = d[coarse_grained_commit]
        normal_grained_refs = get_commit_refdict(squash_log_p, list(fine_grained_commits))
        coarse_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)
        cgr = extract_coarse_grained_refs(coarse_grained_refs, normal_grained_refs)
        if len(cgr) > 0:
            res += cgr
    return res


def extract_fine_grained_refs_by_squashlog(squash_log_p: str) -> list[Refactoring]:
    d = load_commit_pairs(squash_log_p)
    res = list()
    for coarse_grained_commit in d.keys():
        fine_grained_commits = d[coarse_grained_commit]
        normal_grained_refs = get_commit_refdict(squash_log_p, list(fine_grained_commits))
        coarse_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)
        fgr = extract_fine_grained_refs(coarse_grained_refs, normal_grained_refs)
        if len(fgr) > 0:
            res += fgr
    return res


def extract_regular_refs_by_squashlog(squash_log_p: str) -> list[Refactoring]:
    squash_log_p = pathlib.Path(squash_log_p)
    refs_d = pathlib.Path(squash_log_p).parent.parent
    if not squash_log_p.name == "log1.txt":
        raise RuntimeError(f"squash log is {squash_log_p}, use log1.txt as the squash log")
    refs = []
    fine_grained_path = refs_d.joinpath("o1")
    for path in fine_grained_path.iterdir():
        refs += load_dictref(path)
    return refs


def get_coarse_grained_refs(squash_log_p: str) -> list[Refactoring]:
    d = load_commit_pairs(squash_log_p)
    CGRs = list()
    for coarse_grained_commit in d.keys():
        fine_grained_commits = d[coarse_grained_commit]
        normal_grained_refs = get_commit_refdict(squash_log_p, list(fine_grained_commits))
        coarse_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)
        CGRs += extract_coarse_grained_refs(coarse_grained_refs, normal_grained_refs)

    return CGRs


def extract_fine_grained_refs(coarse_grained_refs: list[list[Refactoring]],
                              normal_grained_refs: list[list[Refactoring]]) -> list[Refactoring]:
    return list(set([ref for each in normal_grained_refs for ref in each]) - set(coarse_grained_refs[0]))


def extract_fine_grained_refs_through_type(coarse_grained_refs: list[list[Refactoring]],
                                           normal_grained_refs: list[list[Refactoring]]) -> list[Refactoring]:
    """
    Obtain Fine Grained Refs by using Normal Grained Refs to substract Coarse Grained Refs
    :param coarse_grained_refs: list[list[squashed coarse grained refs]]
    :param normal_grained_refs: list[list[non-squashed normal grained refs],list[non-squashed normal grained refs]],
    each list[non-squashed normal grained refs] is squashed to the corresponding index coarse grained refs in coarse_grained_refs
    :return: list of Fine Grained Refs
    """
    CGRtypes = set([ref.type for ref in coarse_grained_refs[0]])
    NGRtypes = set([ref.type for each in normal_grained_refs for ref in each])
    return list(NGRtypes - CGRtypes)


def match_oline_as_supportive(coarse_grained_ref: Refactoring, normal_grained_ref: Refactoring,
                              normal_grained_commit_sha1s: list[str]) -> bool:
    """
    :param normal_grained_commit_sha1s:
    :param coarse_grained_ref: squashed coarse-grained ref, which is squashed by normal_grained_refs
    :param normal_grained_ref: one non-squashed normal-grained-ref
    :return: it is matched or not

    match mechanism for determine whether a refactoring detected from coarse-grained commit is the same as the
    normal-grained ref (match if yes)

    mechanism:
        ref detected in coarse-grained commit Co: r'
        normal-grained commit {C1, C2}, which squashed into Co.
        refs detected in {C1, C2}: R
        r ∈ R
          r==r'<=> r.type==r'type ^ r.oline==r'.oline
    """
    if coarse_grained_ref.type == normal_grained_ref.type and \
            coarse_grained_ref.refactored_source_location == normal_grained_ref.refactored_source_location:
        return True
    return False


def extract_coarse_grained_refs_oline_as_supportive(coarse_grained_refs: list[list[Refactoring]],
                                                    normal_grained_refs: list[list[Refactoring]],
                                                    normal_grained_commit_sha1s: list[str]) -> list[Refactoring]:
    """
    Extract coarse grained refs through match mechanism
    :param normal_grained_commit_sha1s:
    :param coarse_grained_refs:
    :param normal_grained_refs:
    :return:
    """
    res = []
    CGR_candidates = coarse_grained_refs[0]
    NGRs = [ref for each in normal_grained_refs for ref in each]
    for CGR_candidate in CGR_candidates:
        if not any([match_oline_as_supportive(CGR_candidate, NGR, normal_grained_commit_sha1s) for NGR in NGRs]):
            res.append(CGR_candidate)
    return res
