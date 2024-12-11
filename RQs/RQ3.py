"""
Which types of refactorings tend to be CGR & FGR
1.Find CGRs/FGRs, count the number of them in terms of types
2.Also the count the number of original refactoring in terms of types.
"""
import glob

from match import *
from collections import defaultdict
from RQs.RQ1_seperate import revert_dict_key_value, search_sub_commit_combination, search_list_index
import json

from utils import load_commit_pairs_all


def count_by_type(refs: list[Refactoring]) -> dict[str, int]:
    d = defaultdict(int)
    for ref in refs:
        d[ref.type] += 1
    return d


def load_data(type_file):
    with open(type_file) as f:
        data = json.load(f)
    return data


def type_rank_all_repos(type_file):
    data = load_data(type_file)
    res = {}
    for repo in data.keys():
        for coarse_granularity in data[repo].keys():
            if coarse_granularity not in res.keys():
                res[coarse_granularity] = {}
            for each in data[repo][coarse_granularity]:
                res[coarse_granularity][each] = res[coarse_granularity].get(each, 0) + \
                                                data[repo][coarse_granularity][each]

    sorted_res = {}

    # rank
    for coarse_granularity in res.keys():
        sorted_result = sorted(res[coarse_granularity].items(), key=lambda x: x[1], reverse=True)
        sorted_res[coarse_granularity] = sorted_result
        print("granularity level ", coarse_granularity)
        print(sorted_result)

    return sorted_res


def type_rank_each_repo(type_file):
    data = load_data(type_file)
    for repo in data.keys():
        print(repo)
        for coarse_granularity in data[repo].keys():
            sorted_result = sorted(data[repo][coarse_granularity].items(), key=lambda x: x[1], reverse=True)
            print(coarse_granularity + ": ", end="")
            print(sorted_result)


def collect_type(repo_path):
    d = load_commit_pairs_all(repo_path)
    reverted_d = revert_dict_key_value(d)

    ref_types = {}

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

            for combination in sub_commit_combinations:
                cgc_sub = reverted_d[str(combination)]
                ref_cgc_sub += get_retraced_commit_refdict2(squash_log_p,
                                                            cgc_sub,
                                                            search_list_index(normal_grained_commits,
                                                                              str(combination[-1])), len(combination))

        CGRs = extract_coarse_grained_refs_oline_as_supportive(coarser_grained_refs, normal_grained_refs + ref_cgc_sub)
        for CGR in CGRs:
            if coarse_granularity not in ref_types.keys():
                ref_types[coarse_granularity] = {}
            ref_types[coarse_granularity][CGR.type] = ref_types[coarse_granularity].get(CGR.type, 0) + 1

    # collect normal-grained refs
    ref_types["1"] = {}
    for each in glob.glob(repo_path + "/1/refs/*.json"):
        refs = load_dictref_no_source(each)
        for ref in refs:
            ref_types["1"][ref.type] = ref_types["1"].get(ref.type, 0) + 1

    return ref_types


def get_effective_squash_unit(repo_path):
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

        CGRs = extract_coarse_grained_refs_oline_as_supportive(coarser_grained_refs, normal_grained_refs + ref_cgc_sub)

        if len(CGRs):
            effective_squash_units[coarse_granularity - 2] = effective_squash_units[coarse_granularity - 2] + 1
            all_CGR.append(CGRs)
    return effective_squash_units


def get_effective_squash_unit_count(repos):
    root_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"
    res = {}
    file = "RQ3_effective_units.json"
    for repo in repos:
        res[repo] = get_effective_squash_unit(root_path + repo)
    with open(file, "w") as f:
        json.dump(res, f)
    return res


def calculate_ratio():
    def load_effective_unit_count_dict():
        with open("RQ3_effective_units.json") as f:
            data = json.load(f)
        return data

    def load_type_data():
        with open("./RQ3_type.json") as f:
            data = json.load(f)
        return data

    def count_type_per_granularity(data):
        res = {}
        for granularity in range(1, 6):
            res[granularity] = {}
            for repo in data:
                if str(granularity) in data[repo].keys():
                    for type in data[repo][str(granularity)]:
                        res[granularity][type] = res[granularity].get(type, 0) + data[repo][str(granularity)][type]
        return res

    def count_effective_unit_per_granularity(data):
        res = {}
        for granularity in range(1, 6):
            for each in data:
                res[granularity] = res.get(granularity, 0) + data[each][granularity - 2]
        return res

    data = load_type_data()
    type_per_granularity = count_type_per_granularity(data)
    # for each in type_per_granularity:
    #     res = sorted(type_per_granularity[each].items(), key=lambda x: x[1], reverse=True)
    #     print(res)

    effective_squash_unit_count_dict = load_effective_unit_count_dict()
    effective_unit_per_granularity = count_effective_unit_per_granularity(effective_squash_unit_count_dict)

    ratio = {}
    for granularity in type_per_granularity:
        ratio[granularity] = {}
        for each in type_per_granularity[granularity]:
            ratio[granularity][each] = type_per_granularity[granularity][each] / effective_unit_per_granularity[
                granularity]

    sorted_ratio = {}
    # sort
    for granularity in ratio:
        sorted_ratio[granularity] = sorted(ratio[granularity].items(), key=lambda x: x[1], reverse=True)

    for granularity in sorted_ratio:
        print(granularity)
        print(sorted_ratio[granularity])

    with open("./RQ3_ratio.json", "w") as f:
        json.dump(sorted_ratio, f)

    return sorted_ratio


def count_type(repos, output="./RQ3_type.json"):
    root_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"
    res = {}
    for each in repos:
        res[each] = collect_type(root_path + each)
        print("type collected for repo", each)
    with open(output, "a") as f:
        json.dump(res, f)


def top_x_type_per_reqposiotry(granularity=2):
    with open("./RQ3_type.json") as f:
        data = json.load(f)

    for repo in data:
        print(repo)
        print(sorted(data[repo][str(granularity)].items(), key=lambda x: x[1], reverse=True))


def top_x_type_per_granularity_in_repository():
    with open("./RQ3_type.json") as f:
        data = json.load(f)

    for repo in data:
        print(repo)
        for granularity in range(1, 6):
            print(sorted(data[repo][str(granularity)].items(), key=lambda x: x[1], reverse=True))


def top_x_type_per_granularity():
    with open("./RQ3_ratio.json") as f:
        data = json.load(f)

    res_top = {}
    for granularity in range(1, 6):
        res_top[granularity] = [each[0] for each in data[str(granularity)][:10]]
    print("Top 10 ratio refactoring types")
    for each in res_top:
        print(each)
        print(res_top[each])

    common = set(res_top[1])
    for each in res_top:
        common = common.intersection(set(res_top[each]))
    print("common refactoring types in top 10 in all granularity ", common)

    common = set(res_top[4])
    for i in range(4, 6):
        common = common.intersection(set(res_top[i]))
    print("common refactoring types in top 10 in coarse-grained granularity ", common)

    # sorted according to refactoring type name
    # for each in res_top:
    #     print(sorted(res_top[each]))

    res = {}
    # ref appears only in granularity 1 & only in granularity>1
    for granularity in range(1, 6):
        res[granularity] = [each[0] for each in data[str(granularity)]]
    coarse_grained_ref_types = set()
    coarse_grained_ref_types_each_granularity = []
    for granularity in range(2, 6):
        coarse_grained_ref_types_each_granularity.append((res[granularity]))
        coarse_grained_ref_types = coarse_grained_ref_types.union(set(res[granularity]))
    print("type only in granularity 1: ", set(res[1]).difference(coarse_grained_ref_types))
    print("type only in granularity larger than 1: ", set(coarse_grained_ref_types).difference(res[1]))

    # ref types comparison between each granularity
    print("refactoring types detected in granularity level 1 ", len(set(res[1])))
    print("refactoring type differnce between granularity 1 & 2", set(res[1]) - set(res[2]))
    print("refactoring type differnce between granularity 1 & 3", set(res[1]) - set(res[3]))
    print("refactoring type differnce between granularity 1 & 4", set(res[1]) - set(res[4]))
    print("refactoring type differnce between granularity 1 & 5", set(res[1]) - set(res[5]))
    print("refactoring type differnce between granularity 2 & 1", set(res[2]) - set(res[1]))
    print("refactoring type differnce between granularity 3 & 2", set(res[3]) - set(res[2]))
    print("refactoring type differnce between granularity 4 & 3", set(res[4]) - set(res[3]))
    print("refactoring type differnce between granularity 5 & 4", set(res[5]) - set(res[4]))
    print("refactoring type differnce between granularity 1 & 2", set(res[1]) - set(res[2]))
    print("refactoring type differnce between granularity 2 & 3", set(res[2]) - set(res[3]))
    print("refactoring type differnce between granularity 3 & 4", set(res[3]) - set(res[4]))
    print("refactoring type differnce between granularity 4 & 5", set(res[4]) - set(res[5]))

    print("refactoring types detected in each granularity", [len(each) for each in coarse_grained_ref_types_each_granularity])


    print("rank of the top 10 ref types in granularity level 1 in other granularities: ")
    for each in res[1][:10]:
        for granularity in range(2,6):
            print(f"{each} ranked {res[granularity].index(each)} in granularity {granularity}")


if __name__ == "__main__":
    repos = ["jfinal",
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

    # count_type([each + "_cr" if "_cr" not in each else each for each in repos])

    # type_rank_all_repos(type_file="./RQ3_type.json")
    # type_rank_each_repo(type_file="./RQ3_type.json")

    # get_effective_squash_unit_count([each + "_cr" if "_cr" not in each else each for each in repos])

    # calculate_ratio()

    top_x_type_per_granularity()

    # top_x_type_per_reqposiotry()

    # top_x_type_per_granularity_in_repository()

