import json
import pathlib
import statistics



def generate_dataset_table(repos):
    def generate_table_head():
        print(r"")

    def number_split(num):
        num = str(num)
        if len(num) > 3:
            num = num[:-3] + "," + num[-3:]
        return num

    for each in repos:
        repo_name = each
        if "_cr" in each:
            repo_name = repo_name.split("_cr")[0]
        print(r"\repository{" + repo_name + "} & " + number_split(repos[each]["commit_count"]) + r"\\")


def load_data(path):
    with open(path) as f:
        data = json.load(f)
    return data


def generate_type_rank_table_seperate():
    def build_table_NGR(data):
        print(r"\begin{center}")
        print(r"\begin{table}")
        print(r"\centering")
        print(r"\begin{tabular}{l" + "r" * 1 + "}")
        print(r"\hline")
        print(r"rank & granularity level 1 \\")
        print(r"\hline")
        for type_index in range(10):
            print(str(type_index + 1), end="")
            for granularity in range(1, 2):
                print(" & " + data[str(granularity)][type_index][0], end="")
            print(r" \\")
        print(r"\hline")
        print(r"\end{tabular}")
        print(r"\caption{NGR type rank}\label{t:type_rank_NGR}")
        print(r"\end{table}")
        print(r"\end{center}")

    def build_table_CGR(data):
        print(r"\begin{center}")
        print(r"\begin{table}")
        print(r"\centering")
        print(r"\begin{tabular}{l" + "r" * 2 + "}")
        print(r"\hline")
        print(r"rank & granularity level 2 & granularity level 3\\")
        print(r"\hline")
        for type_index in range(10):
            print(str(type_index + 1), end="")
            for granularity in range(2, 4):
                print(" & " + data[str(granularity)][type_index][0], end="")
            print(r" \\")
        print(r"\hline")
        print(r" \\")
        print(r" \\")
        print(r" \\")
        print(r"\end{tabular}")
        print(r"\begin{tabular}{l" + "r" * 2 + "}")
        print(r"\hline")
        print(r"rank & granularity level 4 & granularity level 5\\")
        print(r"\hline")
        for type_index in range(10):
            print(str(type_index + 1), end="")
            for granularity in range(4, 6):
                print(" & " + data[str(granularity)][type_index][0], end="")
            print(r" \\")
        print(r"\hline")
        print(r"\end{tabular}")
        # print(r"\caption{CGR type rank}\label{t:type_rank_CGR}")
        print(r"\caption{FGR type rank}\label{t:type_rank_FGR}")
        print(r"\end{table}")
        print(r"\end{center}")

    # GIR
    # data = load_data("./RQ3_ratio.json")
    # build_table_NGR(data)
    # CGR
    # build_table_CGR(data)

    # FGR
    data = load_data("./RQ2_ratio.json")
    build_table_CGR(data)


def generate_type_rank_table():
    def build_table(data):
        print(r"\begin{center}")
        print(r"\begin{table}")
        print(r"\centering")
        print(r"\rotatebox{90}{")
        print(r"\begin{tabular}{l" + "rr" * 4 + "}")
        print(r"\hline")
        print(r"rank & granularity level 1 & 2 & 3 & 4 & 5 \\")
        print(r"\hline")
        for type_index in range(10):
            print(str(type_index + 1), end="")
            for granularity in range(1, 6):
                print(" & " + data[str(granularity)][type_index][0], end="")
            print(r" \\")
        print(r"\hline")
        print(r"\end{tabular}")
        print(r"}")
        # print(r"\caption{CGR type rank}\label{t:type_rank}")
        print(r"\caption{FGR type rank}\label{t:type_rank_FGR}")
        print(r"\end{table}")
        print(r"\end{center}")

    def build_table_4_columns(data):
        print(r"\begin{center}")
        print(r"\begin{table}")
        print(r"\centering")
        print(r"\rotatebox{90}{")
        print(r"\begin{tabular}{l" + "rr" * 3 + "}")
        print(r"\hline")
        print(r"rank & granularity level 2 & 3 & 4 & 5 \\")
        print(r"\hline")
        for type_index in range(10):
            print(str(type_index + 1), end="")
            for granularity in range(2, 6):
                print(" & " + data[str(granularity)][type_index][0], end="")
            print(r" \\")
        print(r"\hline")
        print(r"\end{tabular}")
        print(r"}")
        print(r"\caption{CGR type rank}\label{t:type_rank}")
        # print(r"\caption{FGR type rank}\label{t:type_rank_FGR}")
        print(r"\end{table}")
        print(r"\end{center}")

    data = load_data("./RQ3_ratio.json")
    print(data)
    # build_table(data)
    build_table_4_columns(data)


def collect_detail_dataset(dataset_detail: dict):
    dataset_info_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/dataset_info/"
    SCS_info = dataset_info_path + "straight_commit_sequence_exclude_length1.json"
    ref_info = dataset_info_path + "refactoring_number.json"

    with open(SCS_info) as f:
        SCS_data = json.load(f)
    for repo in SCS_data.keys():
        # number of SCS
        dataset_detail[repo.replace("_cr", "")]["number of SCS"] = len(SCS_data[repo])

        # average length of SCS
        dataset_detail[repo.replace("_cr", "")]["average length of SCS"] = sum(SCS_data[repo]) / len(SCS_data[repo])

        # median length of SCS
        dataset_detail[repo.replace("_cr", "")]["median length of SCS"] = statistics.median(SCS_data[repo])

    with open(ref_info) as f:
        ref_data = json.load(f)
    for repo in ref_data.keys():
        dataset_detail[repo.replace("_cr", "")]["number of refs"] = ref_data[repo]["1"]

    print(dataset_detail)
    return dataset_detail


def generate_detail_dataset_table(data):
    print(r"\begin{table}[tb]\centering")
    print(r"\caption{Dataset}\label{t:dataset_detail}")
    print(r"{\scriptsize\begin{tabular}{lrrrrl}")
    print(r"\hline")
    print(r"org/repo & $\#$ commit & $\#$ refs & ave $|\mathrm{SCS}|$ & med $|\mathrm{SCS}|$ & domain \\")
    print(r"\hline")
    for repo in data:
        print(repo + " & ", end="")
        print(str(data[repo]['commit_count']) + " & ", end="")
        print(str(data[repo]['number of refs']) + " & ", end="")
        print(str("{:.1f}".format(round(data[repo]['average length of SCS'], 1))) + " & ", end="")
        print(str("{:.1f}".format(data[repo]['median length of SCS'], 1)) + " & ", end="")
        print(data[repo]['domain'], end=r" \\")
        print("")

    print(r"\hline")
    print(r"\end{tabular}}")
    print(r"\end{table}")


def collect_dataset_each_granularity(data):
    data = collect_detail_dataset(data)
    with open(
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/dataset_info/CGR_count.json") as f:
        CGR_count = json.load(f)
    with open(
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/dataset_info/FGR_count.json") as f:
        FGR_count = json.load(f)
    for repo in data.keys():
        data[repo]["CGR"] = CGR_count[repo + "_cr"]
        data[repo]["FGR"] = FGR_count[repo + "_cr"]
    print(data)
    return data


def generate_dataset_each_granularity(data):
    print(r"\begin{table}[tb]\centering")
    print(r"\caption{Detected CGR and FGR}\label{t:dataset_granularity}")
    print(r"{\scriptsize\begin{tabular}{lccccccccc}\hline")
    print(
        r"\multirow{2}{4em}{org/repo} & \multirow{2}{4em}{ $\#$ GIR} & \multicolumn{4}{c}{$\#$ CGR}  & \multicolumn{4}{c}{$\#$ FGR} \\")
    print(r"& & 2 & 3 & 4 & 5 & 2 & 3 & 4 & 5\\")
    print(r"\hline")
    for repo in data:
        print(repo + " & ", end="")
        print(str(data[repo]['number of refs'] - sum(data[repo]['FGR'][str(each)] for each in range(2, 6))) + " & ",
              end="")
        for granularity in range(2, 6):
            print(str(data[repo]['CGR'][str(granularity)]) + " & ", end="")
        for granularity in range(2, 5):
            print(str(data[repo]['FGR'][str(granularity)]) + " & ", end="")
        print(str(data[repo]['FGR'][str(5)]) + r" \\")
    print(r"\hline")
    print(r"\end{tabular}}")
    print(r"\end{table}")


def commit_count_per_repo(repos):
    root_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result"
    log2paths = pathlib.Path(root_path).glob("*/2/log2.txt")
    for repo_log2 in log2paths:
        repo_log2 = str(repo_log2)
        with open(repo_log2) as f:
            data = f.readlines()
        for line in data:
            if "2by2 - INFO - squash units list " in line:
                commit_num = len(eval(line.split("2by2 - INFO - squash units list ")[1])) * 2
                break
        for each in repos.keys():
            if each in repo_log2:
                repos[each]["commit_count"] = commit_num
                break
    with open("dataset_info/commit_count.json", "w") as f:
        json.dump(repos, f)

    return repos


if __name__ == "__main__":
    repos = {"jfinal": {"commit_count": 510, "star_count": 3200, "domain": "web framework"},
             "mbassador": {"commit_count": 342, "star_count": 939, "domain": "event bus"},
             "javapoet": {"commit_count": 897, "star_count": 10400, "domain": "source file generator"},
             "jeromq": {"commit_count": 1347, "star_count": 2200, "domain": "messaging library"},
             "seyren": {"commit_count": 640, "star_count": 865, "domain": "dashboard"},
             "retrolambda": {"commit_count": 530, "star_count": 3500, "domain": "backport lambda expression"},
             "baasbox": {"commit_count": 1706, "star_count": 795, "domain": "backend server"},
             "sshj": {"commit_count": 1011, "star_count": 2300, "domain": "ssh library"},
             "xabber-android": {"commit_count": 4264, "star_count": 1800, "domain": "XMPP client for Android"},
             "android-async-http": {"commit_count": 899, "star_count": 10600, "domain": "HTTP client"},
             "giraph": {"commit_count": 1138, "star_count": 611, "domain": "graph processing system"},
             "spring-data-rest": {"commit_count": 1650, "star_count": 867, "domain": "restful data access"},
             "blueflood": {"commit_count": 3152, "star_count": 592, "domain": "data processing"},
             "HikariCP": {"commit_count": 2835, "star_count": 18500, "domain": "JDBC connection"},
             "redisson": {"commit_count": 8187, "star_count": 21600, "domain": "redis client"},
             "goclipse": {"commit_count": 2925, "star_count": 837, "domain": "IDE for go language"},
             # "atomix": {"commit_count": 1245, "star_count": 2300},
             "morphia": {"commit_count": 3377, "star_count": 1600, "domain": "Java MongoDB ORM"},
             "PocketHub": {"commit_count": 3512, "star_count": 9400, "domain": "Android app"},
             "hydra": {"commit_count": 2958, "star_count": 437, "domain": "distributed data processing"},
             "cascading": {"commit_count": 2524, "star_count": 337, "domain": "data processing"},
             # "robovm": {"commit_count": 2823, "star_count": 1600},
             "helios": {"commit_count": 2457, "star_count": 2100, "domain": "container orchestration framework"},
             "RoboBinding": {"commit_count": 1088, "star_count": 1300, "domain": "data binding framework"},
             "truth": {"commit_count": 1843, "star_count": 2600, "domain": "Java assertions"},
             "rest.li": {"commit_count": 1843, "star_count": 2600, "domain": "REST framework"},
             "rest-assured": {"commit_count": 2842, "star_count": 2300, "domain": "REST service testing"},
             "JGroups": {"commit_count": 1843, "star_count": 2600, "domain": "messaging library"},
             "processing": {"commit_count": 19934, "star_count": 979, "domain": "code learning platform"},
             "zuul": {"commit_count": 1517, "star_count": 12900, "domain": "gateway service"}
             }

    generate_type_rank_table_seperate()

    # count non-brnch commit number
    repos = commit_count_per_repo(repos)

    sorted_repos = sorted(repos.items(), key=lambda x: x[1]["commit_count"])
    temp = {}
    for each in sorted_repos:
        temp[each[0]] = each[1]

    # Depreaceted
    # generate_dataset_table(repos)
    # print(len(repos))

    # Deprecated
    # generate_type_rank_table()

    # dataset info including commit #, # of refs, average |SCS| and domain
    # data = collect_detail_dataset(temp)
    # generate_detail_dataset_table(data)

    # count median SCS length < 5.0
    # lessThan5Count = 0
    # for med in [data[each]['median length of SCS'] for each in data]:
    #     if med<5.0:
    #         lessThan5Count+=1
    # print(f"# of median SCS length repos is {lessThan5Count}, count for {lessThan5Count/len(data)}")

    # of CGR & FGR at each granularity
    # data = collect_dataset_each_granularity(temp)
    # generate_dataset_each_granularity(data)
