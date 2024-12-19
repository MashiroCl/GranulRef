"""
Extract coarse-grained refactorings & fine-grained refactorings from ]
1) the refactorings detected from granularity 1~5
2) the traced result
3) the retraced result
"""
import pathlib
import json
from collections import defaultdict

from match import extract_coarse_grained_refs_oline_as_supportive, load_coarse_grained_refs, load_normal_grained_refs, \
    load_retraced_commit_refdict, load_traced_refs, RefactoringSetOperation, match_with_traced_location
from utils import load_commit_pairs_all


def search_sub_commit_combination(l: list) -> list[str]:
    """
    search consecutive substring (exclude itself)
    :param l:
    :return:
    """
    res = []
    for length in range(1, len(l)):
        for offset in range(len(l) + 1 - length):
            res.append(l[offset:offset + length])
    return res


def search_list_index(ll, sl):
    """
    ll = (A,B,C,...), where B is the parent commit of A, and C is the parent commit of B.
    :param ll: the fine-grained commits
    :param sl: the target commit
    :return: the number of parent commits of the target commit in ll
    e.g. ll=(A,B,C), sl = C, the index of C is 2
    the return should be 3-1-2 = 0
    """
    return len(ll) - 1 - ll.index(sl)


def revert_dict_key_value(d):
    new_d = dict()
    for each in d:
        new_d[str(d[each])] = each
    return new_d


def load_lower_granularity_refs(repo_path: str, normal_grained_commits: list[str],
                                normal_coarse_commit_map: dict) -> dict:
    """
    load refs: load refactorings for normal_grained_commits & coarse_grained_commits whose granularity<len(normal_grained_commits)
    :param repo_path: folder path for the traced ref
    :param normal_grained_commits: all normal grained commits squashed into a coarse grained commit
    :param normal_coarse_commit_map:
    :return: a dictionary with num of ignore commit as key and refs as value, e.g. {0:[refs], 1:[refs]}
    """
    refs = {}
    for i in range(len(normal_grained_commits)):
        refs[i] = []
    for length in range(1, len(normal_grained_commits)):
        for offset in range(len(normal_grained_commits) + 1 - length):
            candidate = normal_grained_commits[offset:offset + length]
            # the time order for commits in normal_grained_commits from left to right is from latest to oldest
            # so the num_of_ignored_commits should be len(normal_grained_commits) - (offset + length)
            if len(candidate) == 1:
                refs[len(normal_grained_commits) - offset - length] += load_traced_refs(
                    f"{repo_path}/o{len(candidate)}/{candidate[0]}.json")
            else:
                refs[len(normal_grained_commits) - offset - length] += load_traced_refs(
                    f"{repo_path}/o{len(candidate)}/{normal_coarse_commit_map.get(str(candidate))}.json")
    return refs


def load_higher_granularity_refs(repo_path: str, normal_grained_commit: str,
                                 straight_commit_sequence: list[str], normal_coarse_commit_map: dict) -> dict:
    """
    load refactorings for coarser_grained commits which contains the normal grained commit
    e.g. for normal grained commit sequence:
    c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 for normal grained commit c5,
    load the refs in coarse grained commits ranges
    from a length of [2, min(5, len(commits before), len(commits after)]
    from an offset of [1-length, 0]
    i.e.
    {c4,c5}, {c5,c6},
    {c3, c4, c5}, {c4, c5, c6}, {c5, c6, c7}
    {c2, c3, c4, c5}, {c3, c4, c5, c6}, {c4, c5, c6, c7}, {c5, c6, c7, c8}
    {c1, c2, c3, c4, c5}, {c2, c3, c4, c5, c6}, {c3, c4, c5, c6, c7}, {c4, c5, c6, c7, c8}, {c5, c6, c7, c8, c9}

    :param straight_commit_sequence:
    :param normal_grained_commit:
    :param repo_path: folder path for the traced ref
    :param normal_coarse_commit_map:
    :return: a dictionary with tuple of normal_grained_commits as key and refs as value, e.g. {(commit1, commit2):[ref0], (commit3, commit4):[ref1, ref2]}
    """

    refs = {}
    index = straight_commit_sequence.index(normal_grained_commit)
    for length in range(2, 6):
        for offset in range(max(-index, 1 - length), 1):
            if index + offset + length >= len(straight_commit_sequence):
                continue
            ngc_sequence = straight_commit_sequence[index + offset:index + offset + length]
            higher_granularity_refs = load_traced_refs(
                f"{repo_path}/o{len(ngc_sequence)}/{normal_coarse_commit_map[str(ngc_sequence)]}.json")
            refs[tuple(ngc_sequence)] = higher_granularity_refs
    return refs


# CGR
def extract_CGR_contained_CGC(repo_path):
    """
    Extract the coarse-grained commits that contains CGR
    The CGRs are determined by comparing and matching with lower-granularity CGR & normal-grained refactorings
    :param repo_path:
    :return: {coarse_grained_commit: {granularity:x, cgrs:[CGRs]}}
    """
    coarse_normal_commit_map = load_commit_pairs_all(repo_path)
    normal_coarse_commit_map = revert_dict_key_value(coarse_normal_commit_map)
    CGRmap = {}

    for coarse_grained_commit in coarse_normal_commit_map.keys():
        normal_grained_commits = coarse_normal_commit_map[coarse_grained_commit]
        coarse_granularity = len(normal_grained_commits)

        cgr_candidates = load_traced_refs(f"{repo_path}/o{coarse_granularity}/{coarse_grained_commit}.json")

        lower_granularity_refs = load_lower_granularity_refs(repo_path, normal_grained_commits,
                                                             normal_coarse_commit_map)

        # Extract the coarse grained refs
        # Match ref in cgr_candidates with lower_g_refs, the not matched ones are cgrs
        cgrs = []
        for candidate in cgr_candidates:
            is_cgr = True
            for num_of_ignored_commit in lower_granularity_refs.keys():
                if any([match_with_traced_location(candidate, 0, ref, num_of_ignored_commit) for ref in
                        lower_granularity_refs[num_of_ignored_commit]]):
                    is_cgr = False
                    break
            if is_cgr:
                cgrs.append(candidate)

        if len(cgrs):
            CGRmap[coarse_grained_commit] = {"granularity": coarse_granularity, "CGRs": cgrs}
    return CGRmap


def extract_FGR_contained_NGC(repo_path):
    """
    Extract the FGR which are refs that only exists in NGC but not in any CGC
    :param repo_path:
    :return: dict {normal_grained_commit: granularity: [FGRs]}
    """

    def load_straight_commit_sequences():
        res = []
        with open(f"{repo_path}/1/log1.txt") as f:
            for each in f.readlines():
                if "Straight commit sequences: " in each:
                    res = eval(each.strip().split("Straight commit sequences: ")[1])
        if len(res) == 0:
            raise Exception(f"No straight commit sequences found in {repo_path}/1/log1.txt")
        return res

    coarse_normal_commit_map = load_commit_pairs_all(repo_path)
    normal_coarse_commit_map = revert_dict_key_value(coarse_normal_commit_map)
    straight_commit_sequences = load_straight_commit_sequences()
    # {normal_grained_commit:granularity:[(tuple),ref] }
    FGRmap = {}
    visited_fgr = set()
    for straight_commit_sequence in straight_commit_sequences:
        for normal_grained_commit in straight_commit_sequence:
            fgr_candidates = load_traced_refs(f"{repo_path}/o1/{normal_grained_commit}.json")
            if not fgr_candidates:
                continue
            higher_granularity_refs = load_higher_granularity_refs(repo_path, normal_grained_commit,
                                                                   straight_commit_sequence, normal_coarse_commit_map)
            # convert to {granularity:{tuple():[refs]}}  {2:{(c1,c2):[refs]}, {(c2,c3):[refs]}}
            granularity_refs = {}
            for commit_tuple in higher_granularity_refs:
                if len(commit_tuple) not in granularity_refs:
                    granularity_refs[len(commit_tuple)] = {}
                granularity_refs[len(commit_tuple)][commit_tuple] = higher_granularity_refs[commit_tuple]

            granularities = sorted(granularity_refs.keys())
            # extract FGR by comparing refs detected from NGC with the refs detected in CGC on each granularity
            for fgr_candidate in fgr_candidates:
                for granularity in granularities:
                    if fgr_candidate in visited_fgr:
                        break
                    # FGR at granularity g refers to ref disappears in any coarse-grained commit at granularity g
                    # e.g. c1,c2,c3   r in c2 disappear in {c2,c3}, appears in {c1,c2}, is a FGR
                    for commit_tuple in granularity_refs[granularity]:
                        if not any(
                                [match_with_traced_location(fgr_candidate, len(commit_tuple) - list(commit_tuple).index(
                                    normal_grained_commit) - 1, ref, 0) for ref in
                                 granularity_refs[granularity][commit_tuple]]):
                            visited_fgr.add(fgr_candidate)

                            if normal_grained_commit not in FGRmap:
                                FGRmap[normal_grained_commit] = {}
                            if granularity not in FGRmap[normal_grained_commit]:
                                FGRmap[normal_grained_commit][granularity] = []
                            FGRmap[normal_grained_commit][granularity].append((commit_tuple, fgr_candidate))

                            break
    return FGRmap


def collect_cgr_according_to_granularity(cgcs):
    res = {}
    for i in range(2, 6):
        res[i] = []
    for id, commit in cgcs.items():
        res[commit['granularity']] += set(commit['CGRs'])
    return res


# [(2, 18), (3, 22), (4, 19), (5, 17)]


def collect_fgr_according_to_granularity(fgrs):
    res = {}
    for i in range(2, 6):
        res[i] = []
    for each in fgrs:
        for granularity in fgrs[each]:
            for commits, ref in fgrs[each][granularity]:
                res[granularity].append(ref)
    return res


if __name__ == '__main__':
    root_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"

    coarse_normal_commit_map = load_commit_pairs_all(root_path + "mbassador_cr")
    # coarse_normal_commit_map = load_commit_pairs_all(root_path + "refactoring-toy-example_cr")

    cgr = extract_CGR_contained_CGC(root_path + "mbassador_cr")
    fgr = extract_FGR_contained_NGC(root_path + "mbassador_cr")
    # cgr = extract_CGR_contained_CGC(root_path + "refactoring-toy-example_cr")
    # fgr = extract_FGR_contained_NGC(root_path + "refactoring-toy-example_cr")

    res = collect_cgr_according_to_granularity(cgr)
    print([(each[0], len(each[1])) for each in res.items()])

    # cgrmap = {2: [], 3: [], 4: [], 5: []}
    # print("cgrs are: ")
    # cgr_num = 0
    # for each in cgr:
    #     # print(each)
    #     # print(coarse_normal_commit_map.get(each))
    #     cgrmap[len(coarse_normal_commit_map.get(each))] += cgr[each]
    #     cgr_num += len(cgr[each])
    #     for ref in cgr[each]:
    #         print(ref)
    # print("In total cgr num: " + str(cgr_num))
    # print("cgrmap: ", cgrmap)

    # print("fgrs are: ")
    # fgr_num = 0
    # for each in fgr:
    #     print(each)
    #     for granularity in fgr[each]:
    #         print(granularity)
    #         fgr_num += len(fgr[each][granularity])
    #         for commits, ref in fgr[each][granularity]:
    #             print(commits)
    #             print(ref)
    # print("In total fgr num: " + str(fgr_num))

    # granulrity_fgr = collect_fgr_according_to_granularity(fgr)
    # print([(each[0], len(set(each[1]))) for each in granulrity_fgr.items()])

    # fgr = extract_FGR_contained_NGC(root_path + "mbassador_cr")
    # print(f"find grained refs:\n {fgr}")
