"""
Collect the intermediate data from experiment log and dump into csv files
"""
import pathlib


def parse_from_log_file(repo_path: pathlib.Path, coarse_granularity, d):
    d[coarse_granularity] = {}
    inter_d = d[coarse_granularity]
    with open(repo_path.joinpath(str(coarse_granularity), f"log{coarse_granularity}.txt")) as f:
        for line in f.readlines():
            if "Number of commits to be processed: " in line:
                inter_d["Number of commits to be processed"] = int(
                    line.split("Number of commits to be processed:")[1].strip())
            if "Number of straight sequences: " in line:
                inter_d["Number of straight sequences"] = int(line.split("Number of straight sequences: ")[1].strip())
            if "Number of commits involved in straight sequences: " in line:
                inter_d["Number of commits involved in straight sequences"] = int(
                    line.split("Number of commits involved in straight sequences: ")[1].strip())

            if "Number of squash units list " in line:
                if "Number of squash units list" not in inter_d.keys():
                    inter_d["Number of squash units list"] = []
                inter_d["Number of squash units list"].append(int(line.split("Number of squash units list")[1].strip()))

            if "Number of commits involved in squash units list " in line:
                if "Number of commits involved in squash units list" not in inter_d.keys():
                    inter_d["Number of commits involved in squash units list"] = []
                inter_d["Number of commits involved in squash units list"].append(
                    int(line.split("Number of commits involved in squash units list")[1].strip()))


def parse(repo_path: pathlib.Path) -> dict:
    inter_d = {}
    for i in range(1, 6):
        parse_from_log_file(repo_path, i, inter_d)

    with open(repo_path.joinpath("1", "reflog.txt")) as f:
        for line in f.readlines():
            if "Number of normal-grained-refactorings: " in line:
                inter_d["Number of normal-grained-refactorings"] = int(
                    line.split("Number of normal-grained-refactorings: ")[1].strip())

    return inter_d


if __name__ == "__main__":
    repo = "mbassador_cr"
    repo_path = f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/{repo}"
    repo_path = pathlib.Path(repo_path)
    res = parse(repo_path)
    print(res)
