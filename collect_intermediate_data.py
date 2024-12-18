"""
Collect the intermediate data from experiment log and dump into csv files
"""
import csv
import pathlib

from trace import load_commitRefs


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


def count_normal_grained_refs(repo_path: pathlib.Path) -> dict:
    commitRefs = load_commitRefs(str(repo_path))
    normal_grained_refs = {}
    for commitRef in commitRefs[1]:
        for ref in commitRef.refs:
            if ref.type not in normal_grained_refs:
                normal_grained_refs[ref.type] = 0
            normal_grained_refs[ref.type] += 1
    return normal_grained_refs


def parse(repo_path: pathlib.Path) -> dict:
    inter_d = {}
    for i in range(1, 6):
        parse_from_log_file(repo_path, i, inter_d)

    res = {"Repository": repo_path,
           'Number of commits to be processed': inter_d[1]['Number of commits to be processed'],
           'Number of straight sequences': inter_d[1]['Number of straight sequences'],
           'Number of commits involved in straight sequences': inter_d[1][
               'Number of commits involved in straight sequences'],
           'Number of NGR': 0}
    for granularity in range(2, 6):
        res[f"Number of squash units(granularity={granularity})"] = inter_d[granularity]['Number of squash units list']
        res[f"Number of commits involved in squash units list(granularity={granularity})"] = inter_d[granularity][
            'Number of commits involved in squash units list']
        res[f"CGR({granularity})"] = 0
        res[f"FGR({granularity})"] = 0
    return res


def get_CGR_FGR_date():
    pass


def build_csv(repo_name, repo_path: pathlib.Path, csv_path):
    date_row = parse(repo_path)
    date_row["Repository"] = repo_name

    # TODO: get other data
    with open(csv_path, "a") as csv_file:
        is_empty = csv_file.tell() == 0
        writer = csv.DictWriter(csv_file, fieldnames=date_row.keys())

        if is_empty:
            writer.writeheader()

        writer.writerow(date_row)


if __name__ == "__main__":
    repo = "mbassador_cr"
    repo_path = f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/{repo}"
    repo_path = pathlib.Path(repo_path)
    intermediate_date = parse(repo_path)
    print(intermediate_date)
    normal_grained_refs = count_normal_grained_refs(repo_path)
    print(sum(normal_grained_refs.values()))
