from unittest import TestCase

from extract_refs import get_json_files_under_directory
from repository import Repository
from refactoring_operation.commit import RMCommit, Commit
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

    def test_get_parent_commit2(self):
        repo = Repository(
            "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/hydra_cr")
        res = get_parent_commit("5db5b7f2b903fbac1dc9484ddf5945ea1475d396", repo)
        print(res)


    def test_load_commit_pairs(self):
        squash_log_p="/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/hydra_cr/4/log4.txt"
        pairs = load_commit_pairs(str(squash_log_p))
        print(pairs)

    def test_load_ref(self):
        squash_res_d = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/hydra_cr"
        squash_res_d = pathlib.Path(squash_res_d)
        normal_grained_commit = [Commit(file) for file in get_json_files_under_directory(
            squash_res_d.joinpath(str(1)).joinpath(f"log{1}.txt").parent.joinpath("refs")
        )]
        for each in normal_grained_commit:
            if each.sha1=="5db5b7f2b903fbac1dc9484ddf5945ea1475d396":
                print(each.refs)

    def test_get_blame_res(self):
        repo = Repository("/Users/leichen/JAVA/gradle_test")
        checkout(repo, "bf2d40ceb705f2d7486768c69b1c2bbadff0e455")
        line_numbers = (15, 17)
        file_path = "/Users/leichen/JAVA/gradle_test/app/src/main/java/animal/WhiteRabbit.java"
        res = get_blame_res(line_numbers, file_path)
        print(res)
        checkout_latest(repo)


    def test_get_blame_res2(self):
        file_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador/src/main/java/net/engio/mbassy/bus/common/Properties.java"
        repo = Repository("/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador")
        commit = "c5715acdd65c9be3cc4313579f027e2b55b37cd6"
        checkout(repo, get_parent_commit(commit, repo))
        line_numbers = (3, 25)
        res = get_blame_res(line_numbers, file_path)
        print(res)
        checkout_latest(repo)


    def test_get_blame_res3(self):
        file_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador/src/main/java/org/mbassy/listener/MessageFilter.java"
        repo = Repository("/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador")
        commit = "1eb8b8bb46dcfb2c132e6576c40445554be64124"
        squash_log = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/mbassador/2/log2.txt"
        fine_grained_commits = load_commit_pairs(squash_log)[commit]
        parent_commit = get_parent_commit(fine_grained_commits[-1], repo)
        print(f"fine grained commits: {fine_grained_commits}\n parent commit: {parent_commit}")
        checkout(repo, parent_commit)
        line_numbers = (23, 29)
        res = get_blame_res(line_numbers, file_path)
        print(res)
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

    def test_trace3(self):
        commit = "c5715acdd65c9be3cc4313579f027e2b55b37cd6"
        line_numbers = (3, 25)
        file_path = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador/src/main/java/net/engio/mbassy/bus/common/Properties.java"
        repo = Repository("/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador")
        print("parent commit:",get_parent_commit(commit, repo))
        res = trace(line_numbers, get_parent_commit(commit, repo) , file_path, repo)
        for each in res:
            print(each.__dict__)
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
                par_c_sha1 = get_parent_commit(pairs[c][-1], repo)
                refs = RMCommit(refs_dir.joinpath(c+".json")).get_refs()
                if refs:
                    for ref in refs:
                        ref.set_oline(trace((ref.refactored_location.startLine, ref.refactored_location.endLine),
                                            par_c_sha1,
                                            repo_path+"/"+ref.refactored_location.file_path,
                                            repo))
                        ref.get_dict_format()

    def test_blame_on_repo_hydra(self):
        output = """f23c0319364ca2e6941508e2e4cd8b2e6480b6c1 76 76 1
                author Michael Spiegel
                author-mail <spiegel@addthis.com>
                author-time 1425666900
                author-tz -0500
                committer Michael Spiegel
                committer-mail <spiegel@addthis.com>
                committer-time 1425666900
                committer-tz -0500
                summary Add 'csv2' query output format.
                previous 4639568738fda8333cb39222881ea1d35b91f5a5 hydra-main/src/main/java/com/addthis/hydra/query/web/DelimitedBundleEncoder.java
                filename hydra-main/src/main/java/com/addthis/hydra/query/web/DelimitedBundleEncoder.java
                public static void buildRow(Bundle row, String delimiter, String quoteReplacement, StringBuilder stringBuilder) {"""
        properties = [each for each in output.split("\n") if
                      "filename " in each or is_commit_sha1(each.split(" ")[0].strip())]
        for i in range(0, len(properties), 2):
            sha1, oline = properties[i].split(" ")[:2]
            print("properties:", properties)

            file_name = properties[i + 1].split("filename ")[1]
            print(sha1)
            print(file_name)

def is_commit_sha1(s: str) -> bool:
    if len(s) != 40:
        return False
    return bool(re.compile("[0-9a-f]{40}").match(s))
