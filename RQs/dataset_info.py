"""
Extract the detail info for dataset
"""
import json
import pathlib
import statistics

from ROExtract.extractRO import extract_commits
from commitProcess.CommitGraph import CommitGraph
from jsonUtils import JsonUtils

# number of straight commit sequnces
# the average length of straight commit sequences
# extract again and count

# number of refactorings detected
# from the original repo
# from converted repos with each strategy (how to express this?)


# number of CGRs and FGRs
# reuse the code in frequency

# etc what else?
#

EXPERIMENT_RESULT_PATH = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result"
REPOS_PATH = "/home/salab/chenlei/CGR/dataset"


def collect_logs():
    experiment_result_path = pathlib.Path(EXPERIMENT_RESULT_PATH)
    logpaths = experiment_result_path.glob("**/[2-5]/log[2-5].txt")
    return list(logpaths)


class Recipe():
    def __init__(self, log_path):
        self.log_path = log_path
        self.repo_name = log_path.parent.parent.name
        self.granularity_level = log_path.parent.name
        self.squash_units = []


def load_log(log_path) -> Recipe:
    recipe = Recipe(log_path)
    print(f"loading recipe for {recipe.repo_name} at granularity level {recipe.granularity_level}")
    with open(str(log_path)) as f:
        lines = f.readlines()
    for line in lines:
        if "squash units list " in line:
            # 2d list
            squash_units = eval(line.split("squash units list ")[1])
            recipe.squash_units.append(squash_units)
    return recipe


def count_squashed_units():
    log_paths = collect_logs()
    res = {}
    for log_path in log_paths:
        recipe = load_log(log_path)
        if recipe.repo_name not in res:
            res[recipe.repo_name] = {}
        if recipe.granularity_level not in res[recipe.repo_name]:
            res[recipe.repo_name][recipe.granularity_level] = 0
        for each_strategy_squash_unit in recipe.squash_units:
            res[recipe.repo_name][recipe.granularity_level] += len(each_strategy_squash_unit)
    print(res)
    return res


class SimpleCommit:
    def __init__(self, sha1):
        self.sha1 = sha1
        self.refs = []


def load_commit_file(commit_file) -> SimpleCommit:
    with open(commit_file) as f:
        data = json.loads("[" + f.read() + "]")[0]
    if not len(data["commits"])>0:
        return None
    commit = SimpleCommit(data["commits"][0]['sha1'])
    if 'refactorings' in data["commits"][0]:
        commit.refs += data["commits"][0]['refactorings']
    return commit


def collect_repo_commits(repo_path):
    commits = {}
    for i in range(1, 6):
        commits[str(i)] = []
        commit_files = repo_path.joinpath(str(i)).joinpath("refs").glob("*.json")
        for commit_file in commit_files:
            commit = load_commit_file(commit_file)
            if commit:
                commits[str(i)].append(commit)
    return commits


def count_refactoring_number(repos):
    experiment_result_path = pathlib.Path(EXPERIMENT_RESULT_PATH)
    res = {}
    for repo in repos:
        res[repo] = {}
        repo_path = experiment_result_path.joinpath(repo)
        commits = collect_repo_commits(repo_path)
        for each in commits:
            res[repo][each] = sum([len(commit.refs) for commit in commits[each]])
    print(res)
    return res


def extract_straight_commit_sequence_repo(repo_path):
    jU = JsonUtils()
    jU.setRepoPath(repo_path)
    jU.gitJson()
    commits = jU.jsonToCommit()
    # create commit graph
    cG = CommitGraph(commits)
    head = cG.buildGraph()
    # Extract sc_lists
    sc_lists = cG.getSClist()
    sc_lists_str = cG.getSCListStr(sc_lists)
    return sc_lists_str


def count_straight_commit_sequence_repos(repos):
    repo_path = pathlib.Path(REPOS_PATH)
    res = {}
    for repo in repos:
        res[repo] = [len(each) for each in extract_straight_commit_sequence_repo(str(repo_path.joinpath(repo)))]
    return res


def run_count_straight_commit_sequence_repos():
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
    repos = [repo + "_cr" for repo in repos if "_cr" not in repo]

    res = count_straight_commit_sequence_repos(repos)
    print(res)
    with open("./straight_commit_sequence.json", "w") as f:
        json.dump(res, f)


def load_straight_commit_sequence_repos_count():
    data_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/dataset_info/straight_commit_sequence.json"
    with open(data_path) as f:
        data = json.load(f)
    return data


def straight_commit_sequence_repos_info():
    data = load_straight_commit_sequence_repos_count()
    # exclude length 1 SCS
    for each in data:
        for i, v in reversed(list(enumerate(data[each]))):
            if v == 1:
                data[each].pop(i)
    print(data)
    print("# of SCS ", [len(data[each]) for each in data])
    print("average SCS length ", [sum(data[each]) / len(data[each]) for each in data])
    print("median SCS length ", [statistics.median(data[each]) for each in data])
    return data

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
    repos = [repo+"_cr" for repo in repos]

    # squashed_units = count_squashed_units()
    # with open("/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/dataset_info"
    #           "/squash_units.json", "w") as f:
    #     json.dump(squashed_units, f)

    # refactoring_number = count_refactoring_number(repos)
    # with open("/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/dataset_info"
    #           "/refactoring_number.json", "w") as f:
    #     json.dump(refactoring_number, f)

    straight_commit_sequences = straight_commit_sequence_repos_info()
    # with open("/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/dataset_info"
    #           "/straight_commit_sequence_exclude_length1.json", "w") as f:
    #     json.dump(straight_commit_sequences, f)
