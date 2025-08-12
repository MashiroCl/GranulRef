from match import get_commit_refdict, extract_fine_grained_refs, extract_fine_grained_refs_through_type
import pathlib
from line_trace import load_commit_pairs
from RQs.RQ1_seperate import revert_dict_key_value, \
    search_sub_commit_combination, get_retraced_commit_refdict2, search_list_index, \
    extract_coarse_grained_refs_oline_as_supportive, cal_effective_squash_units, print_refs
from utils import load_commit_pairs_all
from RQs.RQ3 import load_dictref_no_source
import json
import glob


def extract_FGR(repo_path):
    """
    Extract granulrity level 2 to 5 FGRs from repository
    :param repo_path:
    :return:
    """
    d = load_commit_pairs_all(repo_path)
    reverted_d = revert_dict_key_value(d)
    squash_units = [0] * 4
    effective_squash_units = [0] * 4

    all_CGR = list()

    for coarse_grained_commit in d.keys():
        normal_grained_commits = d[coarse_grained_commit]
        coarse_granularity = len(normal_grained_commits)
        squash_units[coarse_granularity - 2] = squash_units[coarse_granularity - 2] + 1

        squash_log_p = str(
            pathlib.Path(repo_path).joinpath(str(coarse_granularity)).joinpath(f"log{coarse_granularity}.txt"))

        # get normal grained refs
        normal_grained_refs = get_commit_refdict(squash_log_p, list(normal_grained_commits), coarse_grained_commit)

        # get coarse grained refs
        coarser_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)

        ref_cgc_sub = []

        # coarse granularity 2 CGRs only compare with normal grained refactorings
        if coarse_granularity > 2:  # coarse granularity larger than 2 CGRs compare with normal & smaller coarse
            # granularity CGRs
            sub_commit_combinations = search_sub_commit_combination(normal_grained_commits)

            for combination in sub_commit_combinations:
                cgc_sub = reverted_d[str(combination)]
                ref_cgc_sub += get_retraced_commit_refdict2(squash_log_p,
                                                            cgc_sub,
                                                            search_list_index(normal_grained_commits,
                                                                              str(combination[-1])), len(combination))

        FGRs = extract_coarse_grained_refs_oline_as_supportive(normal_grained_refs, coarser_grained_refs + ref_cgc_sub)

        if len(FGRs):
            effective_squash_units[coarse_granularity - 2] = effective_squash_units[coarse_granularity - 2] + 1
            all_CGR.append(FGRs)
            print_refs(coarse_grained_commit, normal_grained_commits, FGRs)

    # print(squash_units)
    # print(effective_squash_units)
    # print([effective_squash_units[i] / squash_units[i] for i in range(0, 4)])

    return all_CGR, cal_effective_squash_units(repo_path.split("/")[-1].replace("_cr", ""), squash_units,
                                               effective_squash_units)



if __name__ == "__main__":
    root_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"
    repo = "zuul_cr"
    extract_FGR(root_path+repo)