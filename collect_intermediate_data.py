"""
Collect the intermediate data from experiment log and dump into csv files
"""
import csv
import pathlib

from coarse_fine_ref_extractor import extract_CGR_contained_CGC, extract_FGR_contained_NGC, \
    collect_cgr_according_to_granularity, collect_fgr_according_to_granularity, extract_NGR
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
           'Number of NGR': sum(count_normal_grained_refs(repo_path).values())}
    for granularity in range(2, 6):
        res[f"Number of squash units(granularity={granularity})"] = inter_d[granularity]['Number of squash units list']
        res[f"Number of commits involved in squash units list(granularity={granularity})"] = inter_d[granularity][
            'Number of commits involved in squash units list']
    return res


def extract_CGR_FGR_contained_commits(repo_path):
    cgrs = extract_CGR_contained_CGC(repo_path)
    fgrs = extract_FGR_contained_NGC(repo_path)
    return cgrs, fgrs


def get_CGR_FGR_data(cgrs, fgrs):
    cgr_nums = collect_cgr_according_to_granularity(cgrs)
    fgr_nums = collect_fgr_according_to_granularity(fgrs)
    num = {}
    # number of CGRs, FGRs
    for granularity in range(2, 6):
        num[f"CGR({granularity})"] = len(cgr_nums.get(granularity, []))
    for granularity in range(2, 6):
        num[f"FGR({granularity})"] = len(fgr_nums.get(granularity, []))
    return num


def get_CGR_FGR_types(cgrs, fgrs):
    cgr_types = {}  # {type:{granularity: #}}
    for cgc in cgrs:
        granularity = cgrs[cgc]['granularity']
        for cgr in cgrs[cgc]['CGRs']:
            if cgr.type not in cgr_types:
                cgr_types[cgr.type] = {}
            cgr_types[cgr.type][granularity] = cgr_types[cgr.type].get(granularity, 0) + 1

    fgr_types = {}  # {type:{granularity: #}}
    for ngc in fgrs:
        for granularity in fgrs[ngc]:
            for commit_tuple, fgr in fgrs[ngc][granularity]:
                if fgr.type not in fgr_types:
                    fgr_types[fgr.type] = {}
                fgr_types[fgr.type][granularity] = fgr_types[fgr.type].get(granularity, 0) + 1
    return cgr_types, fgr_types


def build_count_csv(repo_name, repo_path: pathlib.Path, cgrs, fgrs, csv_path):
    date_row = parse(repo_path)
    date_row["Repository"] = repo_name
    cgr_fgr_data = get_CGR_FGR_data(cgrs, fgrs)
    date_row.update(cgr_fgr_data)

    with open(csv_path, 'a') as csv_file:
        is_empty = csv_file.tell() == 0
        writer = csv.DictWriter(csv_file, fieldnames=date_row.keys())

        if is_empty:
            writer.writeheader()

        writer.writerow(date_row)


def build_type_csv(cgr_types, fgr_types, ngr_types):
    def build_csv(types, csv_path):
        rows = []
        for key, value_map in types.items():
            row = [key]
            for i in range(2, 6):
                row.append(value_map.get(i, 0))
            rows.append(row)
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_row)  # Write the first header row
            for row in rows:
                writer.writerow(row)

    def build_ngr_csv(ngr_types, csv_path):
        rows = [[type, value] for type, value in ngr_types.items()]
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["type", "number"])  # Write the first header row
            for row in rows:
                writer.writerow(row)

    header_row = ["type\\granularit level", 2, 3, 4, 5]
    build_csv(cgr_types, "./cgr_types.csv")
    build_csv(fgr_types, "./fgr_types.csv")
    build_ngr_csv(ngr_types, "./ngr_types.csv")


def collect_CGR_FGR_types(total_cgr_types, total_fgr_types, cgrs, fgrs):
    def collect_types(total_types, types):
        for key in types:
            if key not in total_types:
                total_types[key] = {}
            for granularity in types[key]:
                total_types[key][granularity] = total_types[key].get(granularity, 0) + types[key][granularity]
        return total_types

    cgr_types, fgr_types = get_CGR_FGR_types(cgrs, fgrs)
    total_cgr_types = collect_types(total_cgr_types, cgr_types)
    total_fgr_types = collect_types(total_fgr_types, fgr_types)
    return total_cgr_types, total_fgr_types


def collect_NGR_types(output_path, total_ngr_types):
    refs = extract_NGR(output_path.joinpath("o1"))
    for i, v in enumerate(refs):
        for ref in v:
            total_ngr_types[ref.type] = total_ngr_types.get(ref.type, 0) + 1
    return total_ngr_types


if __name__ == "__main__":
    # repo = "mbassador_cr"
    # repo_path = f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/{repo}"
    # repo_path = pathlib.Path(repo_path)
    # cgrs, fgrs = extract_CGR_FGR_contained_commits(repo_path)

    # build_count_csv(repo_name="mbassador", repo_path=repo_path, cgrs=cgrs, fgrs=fgrs, csv_path="./test.csv")

    # cgr_types, fgr_types = get_CGR_FGR_types(cgrs, fgrs)
    # build_type_csv(cgr_types, fgr_types)

    temp = """javapoet
                mbassador
                seyren
                jeromq
                jfinal
                retrolambda
                helios
                android-async-http
                baasbox
                RoboBinding
                sshj
                zuul
                giraph
                truth
                spring-data-rest
                blueflood
                goclipse
                rest-assured
                cascading
                HikariCP
                hydra
                PocketHub
                rest.li
                morphia
                xabber-android
                redisson
                processing
                JGroups
                infinispan
                libgdx
                cgeo
                checkstyle
                Activiti
                crate
                """
    repos = temp.split()
    titan_path = pathlib.Path("/home/salab/chenlei/CGR/experiment/output/")
    total_cgr_types = {}
    total_fgr_types = {}
    total_ngr_types = {}
    for repo in repos:
        cgrs, fgrs = extract_CGR_FGR_contained_commits(titan_path.joinpath(repo + "_cr"))
        total_cgr_types, total_fgr_types = collect_CGR_FGR_types(total_cgr_types, total_fgr_types, cgrs, fgrs)
        total_ngr_types = collect_NGR_types(titan_path.joinpath(repo + "_cr"), total_ngr_types)
        build_count_csv(repo_name=repo, repo_path=titan_path.joinpath(repo + "_cr"), cgrs=cgrs, fgrs=fgrs,
                        csv_path="./intermediate.csv")
        print("Processed ref count: " + repo)

    print("Building type csv")
    build_type_csv(total_cgr_types, total_fgr_types, total_ngr_types)
    print("Built type csv")
