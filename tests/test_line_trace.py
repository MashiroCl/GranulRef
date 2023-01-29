from unittest import TestCase
from repository import Repository
from refactoring_operation.commit import RMCommit
import pathlib
from line_trace import *


class Test(TestCase):
    def test_load_commit_pairs(self):
        file_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/refactoring-toy-example/2/log2.txt"
        pairs = load_commit_pairs(file_path)
        self.assertEqual(pairs['f60f68a15a96f0eafcfa2f83586c7f99f62c1de9'],
                         ('d4bce13a443cf12da40a77c16c1e591f4f985b47', '9a5c33b16d07d62651ea80552e8782974c96bb8a'))
        self.assertEqual(pairs['8fa0b5ee04c8cfd7144c2a45cdbf57c061167437'],
                         ('cd61fd2a70828030ccb3cf46d8719f8b204c52ed', '819b202bfb09d4142dece04d4039f1708735019b'))

    def test_get_parent_commit(self):
        repo = Repository(
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/refactoring-toy-example")
        self.assertEqual(get_parent_commit("d4bce13a443cf12da40a77c16c1e591f4f985b47", repo),
                         "9a5c33b16d07d62651ea80552e8782974c96bb8a")
        self.assertEqual(get_parent_commit("32bf625304762aaad475fa817150634038f07af5", repo),
                         "92b201345f730110445d83f4fefe8ae88bc4872b")

    def test_get_blame_res(self):
        repo = Repository("/Users/leichen/JAVA/gradle_test")
        checkout(repo, "bf2d40ceb705f2d7486768c69b1c2bbadff0e455")
        line_numbers = (15, 17)
        file_path = "/Users/leichen/JAVA/gradle_test/app/src/main/java/animal/WhiteRabbit.java"
        get_blame_res(line_numbers, file_path)
        checkout_latest(repo)

    def test_checkout(self):
        repo = Repository("/Users/leichen/JAVA/gradle_test")
        checkout(repo, "e2673e1c0b500300d25a198f8af0da42746c97cc")
        import subprocess
        self.assertEqual(subprocess.getoutput(f'cd {repo.repoPath} && git log -1 --pretty=format:"%H"'),
                         "e2673e1c0b500300d25a198f8af0da42746c97cc")
        checkout_latest(repo)

    def test_checkout_latest(self):
        repo = Repository("/Users/leichen/JAVA/gradle_test")
        checkout(repo, "e2673e1c0b500300d25a198f8af0da42746c97cc")
        checkout_latest(repo)
        import subprocess
        self.assertEqual(subprocess.getoutput(f'cd {repo.repoPath} && git log -1 --pretty=format:"%H"'),
                         "b06a8273f44c1b46770e6e6f32d80d4fc2644250")

    def test_trace(self):
        commit = "bf2d40ceb705f2d7486768c69b1c2bbadff0e455"
        line_numbers = (15, 17)
        file_path = "/Users/leichen/JAVA/gradle_test/app/src/main/java/animal/WhiteRabbit.java"
        repo = Repository("/Users/leichen/JAVA/gradle_test")
        res = trace(line_numbers, commit, file_path, repo)
        print(res)

    def test_trace2(self):
        commit = "ae49bdb9f7244e1d7e92114eccf0b8169ef9e37d"
        line_numbers = (11, 13)
        file_path = "/Users/leichen/JAVA/gradle_test/app/src/main/java/animal/WhiteRabbit.java"
        repo = Repository("/Users/leichen/JAVA/gradle_test")
        res = trace(line_numbers, commit, file_path, repo)
        print(res)

    def test_process(self):
        repo_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador"
        repo = Repository(repo_path)
        for squash_num in range(2,5):
            squash_log_p = f"/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador/{squash_num}/log{squash_num}.txt"
            squash_log_p =pathlib.Path(squash_log_p)
            refs_dir = squash_log_p.parent.joinpath("refs")
            pairs = load_commit_pairs(squash_log_p)
            for c in pairs:
                par_c_sha1 = get_parent_commit(pairs[c][0], repo)
                refs = RMCommit(refs_dir.joinpath(c+".json")).get_refs()
                if refs:
                    for ref in refs:
                        ref.set_oline(trace((ref.refactored_location.startLine, ref.refactored_location.endLine),
                                            par_c_sha1,
                                            repo_path+"/"+ref.refactored_location.file_path,
                                            repo))

