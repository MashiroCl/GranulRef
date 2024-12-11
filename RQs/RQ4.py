"""
RQ4: what's the cause for CGR

for coarse granularity leve 2 CGRs, iterate the refactroings in FGCs which squashed into those CGCs,
by comparing the source location info, if the CGR source location info can be found in both commits, then
it is a COMBINATION type, if only one can be found, it is a MUTATION type, and if non can be found, it is a GENERATION

COMBINATION: combined by two refactorings
MUTATION: combined by one refactoring with a non-refactoring
GENERATION: combined by two non-refactoring operations
"""
import csv
import pathlib
import random

from match import load_dictref, match_oline_as_supportive, get_commit_refdict, \
    get_retraced_commit_refdict2, extract_coarse_grained_refs_oline_as_supportive
from utils import load_commit_pairs_all
from RQs.RQ1_seperate import extract_CGR_contained_CGC, revert_dict_key_value, search_sub_commit_combination, \
    search_list_index

REF_PATH = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"


def analyse_type(CGR, FGRs):
    type_record = [0, 0]  # 0 referred to non ref found
    for i in range(len(FGRs)):
        for FGR in FGRs[i]:
            if match_oline_as_supportive(FGR, CGR):
                type_record[i] = 1
                break
    return which_cause_type(type_record)


def which_cause_type(type_record):
    if type_record[0] == type_record[1] == 1:
        return "Combination"
    elif type_record[0] == type_record[1] == 0:
        return "Generation"
    else:
        return "Mutation"


def print_refs_with_cause(coarse_grained_commit, normal_grained_commits, CGRs, FGRs):
    print("*" * 30)
    print(f"coarse grained commits {coarse_grained_commit}")
    print(f"fine grained commits {normal_grained_commits}")
    for each in CGRs:
        print(analyse_type(each, FGRs))
        print(each)
    print("*" * 30)


def print_refs2txt_with_cause(coarse_grained_commit, normal_grained_commits, CGRs, FGRs, file_path):
    with open(file_path, "a") as f:
        f.write("*" * 30 + "\n")
        f.write(f"coarse grained commits {coarse_grained_commit}\n")
        f.write(f"fine grained commits {normal_grained_commits}\n")
        for each in CGRs:
            f.write(analyse_type(each, FGRs) + "\n")
            f.write(str(each) + "\n")
        f.write("*" * 30 + "\n")


def extract_CGR_filter_sub(repo_name, csv_path):
    repo_path = REF_PATH + repo_name + "_cr"
    d = load_commit_pairs_all(repo_path)
    reverted_d = revert_dict_key_value(d)

    all_CGR = list()

    for coarse_grained_commit in d.keys():
        normal_grained_commits = d[coarse_grained_commit]
        coarse_granularity = len(normal_grained_commits)

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
            # if coarse_grained_commit=="53f3d0bec1e4f003623e084930e8364106f4ebfd":
            #     print(sub_commit_combinations)
            #     print("reverted_d", reverted_d["('1af8b5ba996cc01d62cfac8ea347d067ca45d1f1', '78752573e5495f74a76bee5a302d952b93de5630')"])
            #     print("search list index",  search_list_index(normal_grained_commits,
            #                                                                   "78752573e5495f74a76bee5a302d952b93de5630"))
            #     print("squash_log_p", squash_log_p)
            #     squash_num = pathlib.Path(squash_log_p).name.split(".txt")[0].split("log")[1]
            #     print("squash num", squash_num)
            #     print("refs_p", pathlib.Path(squash_log_p).parent.parent.joinpath("o" + "2").joinpath(reverted_d["('1af8b5ba996cc01d62cfac8ea347d067ca45d1f1', '78752573e5495f74a76bee5a302d952b93de5630')"] + ".json"))
            #     refs = get_retraced_commit_refdict2(squash_log_p,
            #                                                 reverted_d["('1af8b5ba996cc01d62cfac8ea347d067ca45d1f1', '78752573e5495f74a76bee5a302d952b93de5630')"],
            #                                                 search_list_index(normal_grained_commits,
            #                                                                   "78752573e5495f74a76bee5a302d952b93de5630"), 2)
            #     for ref in refs:
            #         print(ref)


            for combination in sub_commit_combinations:
                cgc_sub = reverted_d[str(combination)]
                ref_cgc_sub += get_retraced_commit_refdict2(squash_log_p,
                                                            cgc_sub,
                                                            search_list_index(normal_grained_commits,
                                                                              str(combination[-1])), len(combination))
        CGRs = extract_coarse_grained_refs_oline_as_supportive(coarser_grained_refs, normal_grained_refs + ref_cgc_sub)

        csv_file_path=f"./cause_analysis/{repo_name}.txt"
        if len(CGRs):
            all_CGR.append(CGRs)
            to_csv(repo_name, coarse_grained_commit, normal_grained_commits, CGRs, csv_path)
        #     # print_refs_with_cause(coarse_grained_commit, normal_grained_commits, CGRs, normal_grained_refs)
            print_refs2txt_with_cause(coarse_grained_commit, normal_grained_commits, CGRs, normal_grained_refs, csv_file_path)

    return all_CGR


def to_csv(repository, CGC, FGC, CGRs, csv_path):
    def create_csv(csv_path):

        with open(csv_path, "w") as f:
            writer = csv.writer(f, delimiter=",")
            CSV_HEADER = ["Repository", "Granularity level", "fine-grained commits", "CGR type", "CGR left",
                          "CGR right",
                          "CGR traced location", "Cause"]
            writer.writerow(CSV_HEADER)

    if not pathlib.Path(csv_path).exists():
        create_csv(csv_path)

    with open(csv_path, "a") as f:
        writer = csv.writer(f)
        for each in CGRs:
            writer.writerow([repository,
                             len(FGC),
                             FGC,
                             each.type,
                             each.left,
                             each.right,
                             each.refactored_source_location
                             ]
                            )


if __name__ == "__main__":
    # analyse_type(repo_path)
    repos = [
            "jfinal",
             "mbassador",
             "javapoet",
             "jeromq",
             "seyren",
             "retrolambda",
             "baasbox",
             "sshj",
             "xabber-android",
             "android-async-http",
             "giraph",
             "spring-data-rest",
             "blueflood",
             "HikariCP",
             "redisson",
             "goclipse",
             "morphia",
             "PocketHub",
             "hydra",
             "cascading",
             "helios",
             "RoboBinding",
             "truth",
             "rest.li",
             "rest-assured",
             "JGroups",
             "processing",
             "zuul"
             ]
    # repo_name = "goclipse"
    # repo_name = "jfinal"
    for repo_name in repos:
        csv_path = "./cause_analysis/" + repo_name + ".csv"
        extract_CGR_filter_sub(repo_name, csv_path)


    # C for combination
    # G for generation
    # X for misidentification
