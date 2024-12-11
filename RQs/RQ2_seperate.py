"""

Deprecated, the contents of RQ2 refers to RQ2.py


"""

import pathlib
from RQ1_seperate import revert_dict_key_value, write_refs2file, print_refs, search_sub_commit_combination, search_list_index
from match import get_commit_refdict, extract_coarse_grained_refs_oline_as_supportive, get_retraced_commit_refdict2
from utils import load_commit_pairs_all


def extract_FGR(repo_path):
    d = load_commit_pairs_all(repo_path)
    reverted_d = revert_dict_key_value(d)

    all_FGR = list()

    for coarse_grained_commit in d.keys():
        normal_grained_commits = d[coarse_grained_commit]
        coarse_granularity = len(normal_grained_commits)
        squash_log_p = str(pathlib.Path(repo_path).joinpath(str(coarse_granularity)).joinpath(
            f"log{coarse_granularity}.txt"))

        FGR = None

        if coarse_granularity == 2:
            ref_ngc = get_commit_refdict(squash_log_p, list(normal_grained_commits), coarse_grained_commit)
            ref_cgc = get_commit_refdict(squash_log_p, coarse_grained_commit)
            FGR = extract_coarse_grained_refs_oline_as_supportive(ref_ngc, ref_cgc)
        elif coarse_granularity == 3:
            """
            FGR(a,b,c) = Rab+Rbc-Rb-Rabc
            """
            ref_cgc_ab = get_commit_refdict(str(pathlib.Path(repo_path).joinpath("2").joinpath(f"log2.txt")),
                                            reverted_d[str(normal_grained_commits[:-1])])
            ref_cgc_bc = get_commit_refdict(str(pathlib.Path(repo_path).joinpath("2").joinpath(f"log2.txt")),
                                            reverted_d[str(normal_grained_commits[1:])])
            ref_cgc_abc = get_commit_refdict(squash_log_p, coarse_grained_commit)
            ref_ngc_b = get_commit_refdict(squash_log_p, list(normal_grained_commits)[1:2], coarse_grained_commit)
            FGR = extract_coarse_grained_refs_oline_as_supportive(ref_cgc_ab + ref_cgc_bc, ref_cgc_abc + ref_ngc_b)
        elif coarse_granularity == 4:
            ref_cgc_abc = get_commit_refdict(str(pathlib.Path(repo_path).joinpath("3").joinpath(f"log3.txt")),
                                            reverted_d[str(normal_grained_commits[:-1])])
            ref_cgc_bcd =get_commit_refdict(str(pathlib.Path(repo_path).joinpath("3").joinpath(f"log3.txt")),
                                            reverted_d[str(normal_grained_commits[1:])])
            ref_cgc_abcd = get_commit_refdict(squash_log_p, coarse_grained_commit)
            ref_cgc_bc = get_commit_refdict(squash_log_p, list(normal_grained_commits)[1:-1], coarse_grained_commit)
            FGR = extract_coarse_grained_refs_oline_as_supportive(ref_cgc_abc + ref_cgc_bcd, ref_cgc_abcd + ref_cgc_bc)
        elif coarse_granularity == 5:
            ref_cgc_abcd = get_commit_refdict(str(pathlib.Path(repo_path).joinpath("4").joinpath(f"log4.txt")),
                                            reverted_d[str(normal_grained_commits[:-1])])
            ref_cgc_bcde = get_commit_refdict(str(pathlib.Path(repo_path).joinpath("4").joinpath(f"log4.txt")),
                                            reverted_d[str(normal_grained_commits[1:])])
            ref_cgc_abcde = get_commit_refdict(squash_log_p, coarse_grained_commit)
            ref_cgc_bcd = get_commit_refdict(squash_log_p, list(normal_grained_commits)[1:-1], coarse_grained_commit)
            FGR = extract_coarse_grained_refs_oline_as_supportive(ref_cgc_abcd + ref_cgc_bcde,
                                                                  ref_cgc_abcde + ref_cgc_bcd)

        if len(FGR):
            all_FGR.append(FGR)
            write_refs2file(coarse_grained_commit, normal_grained_commits, FGR, "./FGR_RoboBindg.txt")
            print_refs(coarse_grained_commit, normal_grained_commits, FGR)
    return all_FGR


def extract_FGR_2(repo_path):
    d = load_commit_pairs_all(repo_path)
    reverted_d = revert_dict_key_value(d)

    all_FGR = list()

    for coarse_grained_commit in d.keys():
        normal_grained_commits = d[coarse_grained_commit]
        coarse_granularity = len(normal_grained_commits)
        squash_log_p = str(pathlib.Path(repo_path).joinpath(str(coarse_granularity)).joinpath(
            f"log{coarse_granularity}.txt"))
        normal_grained_refs = get_commit_refdict(squash_log_p, list(normal_grained_commits), coarse_grained_commit)
        coarser_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)

        FGRs = None
        ref_cgc_sub = []

        if coarse_granularity == 2:
            FGRs = extract_coarse_grained_refs_oline_as_supportive(normal_grained_refs, coarser_grained_refs)
        else:       # coarse granularity>2 FGR(a,b,c) = Ra + Rb + Rc - Rabc -Rab - Rbc -Rcd
            sub_commit_combinations = search_sub_commit_combination(normal_grained_commits)

            for combination in sub_commit_combinations:
                cgc_sub = reverted_d[str(combination)]
                ref_cgc_sub += get_retraced_commit_refdict2(squash_log_p,
                                                            cgc_sub,
                                                            search_list_index(normal_grained_commits,
                                                                              str(combination[-1])), len(combination))

        FGRs = extract_coarse_grained_refs_oline_as_supportive(normal_grained_refs, coarser_grained_refs + ref_cgc_sub)

        if len(FGRs):
            all_FGR.append(FGRs)
            print_refs(coarse_grained_commit, normal_grained_commits, FGRs)
    return all_FGR


if __name__ == "__main__":
    repo_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador_cr"
    refs = extract_FGR_2(repo_path)
    # calculate(repo_path)


    all_refs = [each for ref in refs for each in ref]
    print(all_refs)
    all_refs_signature = [str(each) for each in all_refs]
    print(len(all_refs))
    print(len(set(all_refs)))
    print(len(set(all_refs_signature)))