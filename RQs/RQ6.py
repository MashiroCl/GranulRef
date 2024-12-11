"""
Does commit messages have a relationship with CGR/ FGR?
1. Collect csv contains the commit messages for fine-grained commits which squshed into the coarse one where the CGRs are
csv HEAD:
coarse-grained commit sha1->fine-grained commit sha1s, CGR 1, CGR 2, CGR 3, fine-grained commit msg1, fine-grained commit msg2
2. Manually check, try to extract some keywords for automated analysis
"""
from refactoring_operation.refactoring import Refactoring
from line_trace import load_commit_pairs
from repository import Repository
from match import get_commit_refdict, extract_coarse_grained_refs
from dataclasses import dataclass
import csv
import subprocess


def extract_msg(repo: Repository, commit: str) -> str:
    return subprocess.getoutput(f"cd {repo.repoPath} && git show -s --format=%B {commit}")


@dataclass
class CommitPairMsg:
    commit_pair: tuple
    CGRs: list[Refactoring]
    # FGRs: list[str]
    msgs: list[str]

    def csv_format(self):
        return [f"{self.commit_pair[0]}->{self.commit_pair[1]}",
                ','.join([each.type for each in self.CGRs]),
                ','.join([each for each in self.msgs])]
        # return f"{self.commit_pair[0]}->{self.commit_pair[1]}, {','.join([each.type for each in self.CGRs])}, " \
        #        f"{','.join([each for each in self.msgs])}"


class RefMsgMapper:
    @staticmethod
    def ref_msg_map(repo, squash_log_p):
        d = load_commit_pairs(squash_log_p)
        commit_pair_msgs = []
        for coarse_grained_commit in d.keys():
            fine_grained_commits = d[coarse_grained_commit]
            fine_grained_refs = get_commit_refdict(squash_log_p, list(fine_grained_commits))
            coarse_grained_refs = get_commit_refdict(squash_log_p, coarse_grained_commit)
            cgrs = extract_coarse_grained_refs(coarse_grained_refs, fine_grained_refs)
            if len(cgrs) > 0:
                commit_pair_msgs.append(
                    CommitPairMsg((coarse_grained_commit, fine_grained_commits),
                                  cgrs,
                                  [extract_msg(repo, each) for each in fine_grained_commits]
                                  ))
        return commit_pair_msgs

    @staticmethod
    def to_csv(commit_pair_msgs: list[CommitPairMsg], fileobj):
        writer = csv.writer(fileobj)
        for each in commit_pair_msgs:
            writer.writerow(each.csv_format())


if __name__ == "__main__":
    repo = Repository(
        "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador")
    squash_log_p = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador/2/log2.txt"
    commit_pair_msgs\
        = RefMsgMapper.ref_msg_map(repo, squash_log_p)
    csv_file = "refmsg.csv"
    with open(csv_file, "w") as f:
        RefMsgMapper.to_csv(commit_pair_msgs, f)