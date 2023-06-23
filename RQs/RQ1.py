"""
How frequently do CGRs appear because of granularity change?
1. For each squash unit, find CGR exists or not
2. Calculate frequency
squash unit is a pair of coarse-grained commit and fine-grained commits which squashed into the coarse one
frequency is the ratio of the number of squash units that can generate at least one CGR
"""
from match import get_commit_refdict, extract_coarse_grained_refs
import pathlib
from line_trace import load_commit_pairs


def frequency(repo_path: str):
    """

    :param repo_path: path of the extracting refs output of the repo
    :return:
    """

    def get_squash_units(squash_log_p: str) -> tuple[int, int]:
        d = load_commit_pairs(squash_log_p)
        effective_squash_units_count = 0
        squash_units_count = len(d)
        for coarse_grained_commit in d.keys():
            fine_grained_commits = d[coarse_grained_commit]
            fine_grained_refs = get_commit_refdict(squash_log_p, list(fine_grained_commits))
            coarse_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)
            CGRs = extract_coarse_grained_refs(coarse_grained_refs, fine_grained_refs)
            if len(CGRs) > 0:
                print("*" * 30)
                print(f"coarse grained commits {coarse_grained_commit}")
                print(f"fine grained commits {fine_grained_commits}")
                print(f"CGRS {[each.type for each in CGRs]}")
                print("*" * 30)
                effective_squash_units_count += 1
        return effective_squash_units_count, squash_units_count

    squash_units = 0
    effective_squash_units = 0
    for i in range(1, 3):
        squash_log_ps = pathlib.Path(repo_path).joinpath(str(i)).joinpath(f"log{i}.txt")
        e_su, su = get_squash_units(squash_log_ps)
        effective_squash_units += e_su
        squash_units += su
    return effective_squash_units / squash_units

if __name__ == "__main__":
    repo_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador"
    res = frequency(repo_path)
    print(res)
