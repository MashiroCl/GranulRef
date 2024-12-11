from match import load_commit_pairs, get_commit_refdict


def collect_types(refs) -> set:
    res = set()
    for each in refs:
        for each_ref in each:
            res.add(each_ref.type)
    return res

def load_commits(squash_log_p):
    d = load_commit_pairs(squash_log_p)
    for coarse_grained_commit in d.keys():
        normal_grained_commits = d[coarse_grained_commit]
        normal_grained_refs = get_commit_refdict(squash_log_p, list(normal_grained_commits), coarse_grained_commit)
        coarse_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)
        ref_diffs = get_ref_diffs(coarse_grained_refs, normal_grained_refs)
        if len(ref_diffs)>0:
            print_coarse_grained_refs(ref_diffs, coarse_grained_commit, normal_grained_commits)


def get_ref_diffs(coarse_grained_refs, normal_grained_refs) -> set:
    types_ngc = collect_types(normal_grained_refs)
    types_cgc = collect_types(coarse_grained_refs)
    refs_diff = types_cgc - types_ngc

    return refs_diff


def print_coarse_grained_refs(ref_diffs, coarse_grained_commits, normal_grained_commits):
    print(f"Coarse-grained refs are {ref_diffs}, CGC: {coarse_grained_commits}, NGC{normal_grained_commits}")


if __name__ == "__main__":
    squash_log_p = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/JGroups_cr/2/log2.txt"
    load_commits(squash_log_p)