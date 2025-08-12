"""
How frequently do FGRs appear because of granularity change
1. For each squash unit, find FGR exists or not
2. Calculate frequency
squash unit is a pair of coarse-grained commit and fine-grained commits which squashed into the coarse one
frequency is the ratio of the number of squash units that can generate at least one FGR
"""
from match import get_commit_refdict, extract_fine_grained_refs, extract_fine_grained_refs_through_type, \
    get_retraced_commit_refdict2
import pathlib
from line_trace import load_commit_pairs
from RQs.RQ1_seperate import revert_dict_key_value, \
    search_sub_commit_combination, search_list_index, \
    extract_coarse_grained_refs_oline_as_supportive, cal_effective_squash_units, print_refs
from utils import load_commit_pairs_all
from RQs.RQ3 import load_dictref_no_source
import json
import glob


def collect_FGR_type(repo_path):
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

        FGRs = extract_coarse_grained_refs_oline_as_supportive(normal_grained_refs, ref_cgc_sub + coarser_grained_refs)
        for FGR in FGRs:
            if coarse_granularity not in ref_types.keys():
                ref_types[coarse_granularity] = {}
            ref_types[coarse_granularity][FGR.type] = ref_types[coarse_granularity].get(FGR.type, 0) + 1

    # collect normal-grained refs
    ref_types["1"] = {}
    for each in glob.glob(repo_path + "/1/refs/*.json"):
        refs = load_dictref_no_source(each)
        for ref in refs:
            ref_types["1"][ref.type] = ref_types["1"].get(ref.type, 0) + 1

    return ref_types


def count_type(repos, output="./RQ2_type.json"):
    root_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"
    res = {}
    for each in repos:
        res[each] = collect_FGR_type(root_path + each)
        print("FGR type collected for repo", each)
    with open(output, "w") as f:
        json.dump(res, f)


def FGRfrequency(repo_path):
    d = load_commit_pairs_all(repo_path)
    reverted_d = revert_dict_key_value(d)
    squash_units = [0] * 4
    effective_squash_units = [0] * 4

    all_FGR = list()
    FGR_count = dict()

    for coarse_grained_commit in d.keys():
        normal_grained_commits = d[coarse_grained_commit]
        coarse_granularity = len(normal_grained_commits)
        squash_units[coarse_granularity - 2] = squash_units[coarse_granularity - 2] + 1
        if coarse_granularity not in FGR_count.keys():
            FGR_count[coarse_granularity] = []

        squash_log_p = str(
            pathlib.Path(repo_path).joinpath(str(coarse_granularity)).joinpath(f"log{coarse_granularity}.txt"))

        # get normal grained refs
        normal_grained_refs = get_commit_refdict(squash_log_p, list(normal_grained_commits), coarse_grained_commit)

        # get refs detected in coarser granularity level commits
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

        FGRs = extract_coarse_grained_refs_oline_as_supportive(normal_grained_refs, ref_cgc_sub + coarser_grained_refs)

        if len(FGRs):
            effective_squash_units[coarse_granularity - 2] = effective_squash_units[coarse_granularity - 2] + 1
            FGR_count[coarse_granularity] += FGRs
            # print_refs(coarse_grained_commit, normal_grained_commits,FGRs)
            all_FGR.append(FGRs)

    for coarse_granularity in FGR_count.keys():
        FGR_count[coarse_granularity] = set(str(each) for each in FGR_count[coarse_granularity])

    return all_FGR, cal_effective_squash_units(repo_path.split("/")[-1].replace("_cr", ""), squash_units,
                                               effective_squash_units), effective_squash_units, squash_units, FGR_count


def top_x_type_per_granularity():
    with open("./RQ2_ratio.json") as f:
        data = json.load(f)

    res_top = {}
    for granularity in range(1, 6):
        res_top[granularity] = [each[0] for each in data[str(granularity)][:10]]
    print("Top 10 ratio refactoring types")
    for each in res_top:
        print(each)
        print(res_top[each])

    print("#" * 100)
    print("rank according to alphabet")
    for each in res_top:
        print(each)
        print(sorted(res_top[each]))

    print("common in all granularity")
    print(set(res_top[1])
          .intersection(set(res_top[2]))
          .intersection(set(res_top[3]))
          .intersection(set(res_top[4]))
          .intersection(set(res_top[5])))

    print("common only in coarse granularity")
    print(set(res_top[2])
          .intersection(set(res_top[3]))
          .intersection(set(res_top[4]))
          .intersection(set(res_top[5])))


def calculate_ratio():
    def load_effective_unit_count_dict():
        with open("RQ2_effective_units.json") as f:
            data = json.load(f)
        return data

    def load_type_data():
        with open("./RQ2_type.json") as f:
            data = json.load(f)
        return data

    def count_type_per_granularity(data):
        res = {}
        for granularity in range(1, 6):
            res[granularity] = {}
            for repo in data:
                if str(granularity) not in data[repo]:
                    continue
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
    print("effective unit per granularity", effective_unit_per_granularity)

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

    with open("./RQ2_ratio.json", "w") as f:
        json.dump(sorted_ratio, f)

    return sorted_ratio


def count_FGR(FGR_each_granularity):
    res = {}
    for granularity in FGR_each_granularity.keys():
        res[granularity] = len(set([str(each) for each in FGR_each_granularity[granularity]]))
    return res

def remove_duplicate_in_FGR(FGRs):
    """
    the same FGR maybe detected duplicate times
    e.g. commits c1,c2,c3.      c1,c2 are squashed into a CGC cs1,   c2,c3 are squashed into a CGC cs2
        one FGR might be detected from both cs1 and cs2, because it is the code change consisted in c2 cause the FGR,
        but the code change in either c1 or c3 will spoil the refactoring.

    Remove the duplicate FGRs using the refactoring type+startLine, endLine
    :return:
    """
    return set([each for ref in FGRs for each in ref])


def FGR_frequency_per_commit():
    """
    use # of CGR/ # of commits
    :return:
    """
    total_FGR_count = 0
    total_commits_coumt = 0
    with open("dataset_info/FGR_count.json", "r") as f:
        data = json.load(f)
        total_FGR_count = sum([data[repo]["2"] + data[repo]["3"] + data[repo]["4"] + data[repo]["5"] for repo in data])
        print("Total FGR count", total_FGR_count)

    with open("dataset_info/commit_count.json", "r") as f:
        data = json.load(f)
        total_commits_coumt = sum([data[repo]["commit_count"] for repo in data])
        print("Total commits count", total_commits_coumt)

    print("FGR frequency per commit", total_FGR_count/total_commits_coumt)

if __name__ == "__main__":
    root_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/"
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
             # "atomix",
             "morphia",
             "PocketHub",
             "hydra",
             "cascading",
             # "robovm",
             "helios",
             "RoboBinding",
             "truth",
             # "assertj",
             "rest.li",
             "rest-assured",
             "JGroups",
             "processing",
             # "spring-framework",
             "zuul"
             ]

    # repos = ["RoboBinding"]

    print(len(repos))
    print(len(set(repos)))

    # calculate FGR frequencies and effective_squash_units
    # res = dict()
    # effective_squash_units = dict()
    # FGR_count = {}
    # for repo in repos:
    #     if "_cr" not in repo:
    #         repo = repo + "_cr"
    #     repo_path = root_path + repo
    #
    #     FGRs, frequency, effective_su, squash_su, FGR_each_granularity = FGRfrequency(repo_path)
    #     print("before removing duplicate: ", len([each for ref in FGRs for each in ref]))
    #     print("after removing duplicate: ", len(remove_duplicate_in_FGR(FGRs)))
    #     res.update(frequency)
    #     effective_squash_units[repo] = effective_su
    #     FGR_count[repo] = count_FGR(FGR_each_granularity)
    #
    #     print(repo, end=" ")
    # print(res)

    # with open("./RQ2_FGR_frequency.json", "w") as f:
    #     json.dump(res, f)
    #
    # with open("./RQ2_effective_units.json", "w") as f:
    #     json.dump(effective_squash_units, f)
    #
    # collect types and write into json
    # count_type([each + "_cr" if "_cr" not in each else each for each in repos])

    # calculate_ratio()
    # top_x_type_per_granularity()

    # with open("dataset_info/FGR_count.json","w") as f:
    #     json.dump(FGR_count, f)

    # print(FGR_count)

    FGR_frequency_per_commit()