import time
import unittest
from ROExtract.extractRO import RMDetectWithOutput, set_repository, extract_commits
from commitProcess.CommitGraph import CommitGraph
from repository import  create_folder
from refactoring_mining.miner import RefactoringMiner
from threading import Thread
from multiprocessing import  Process


class MyTestCase(unittest.TestCase):
    def get_repo(self):
        # repoPath = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/refactoring-toy-example"
        repoPath = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/mbassador"
        repo = set_repository(repoPath)
        return repo

    def get_commit_list(self):
        repo = self.get_repo()
        commits = extract_commits(repo)
        cG = CommitGraph(commits)
        head = cG.buildGraph()
        sc_lists = cG.getSClist()
        sc_lists_str = cG.getSCListStr(sc_lists)
        origin_commits = list()
        for each1 in sc_lists_str:
            if len(each1) == 1:
                continue
            for eachCommit in each1:
                origin_commits.append(eachCommit)
        return origin_commits

    def extract_no_squashed_commit_single_thread(self):
        repo = self.get_repo()
        origin_commits  = self.get_commit_list()
        RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
        rm = RefactoringMiner(RMPath)
        jsonOutputDirectory = "./test_RM_speed/"
        create_folder(jsonOutputDirectory)
        RMDetectWithOutput(rm, origin_commits, repo, jsonOutputDirectory)

    def extract_no_squashed_commit_multiple_threads(self):
        repo = self.get_repo()
        origin_commits  = self.get_commit_list()
        RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
        rm = RefactoringMiner(RMPath)
        jsonOutputDirectory = "./test_RM_speed/"
        create_folder(jsonOutputDirectory)

        thread_num = 10
        sub_c_num = int(len(origin_commits)/thread_num)

        threads = []
        for i in range(1,thread_num+1):
            threads.append(Thread(target=RMDetectWithOutput, args=(rm, origin_commits[(i-1)*sub_c_num:min(i*sub_c_num,len(origin_commits))], repo, jsonOutputDirectory)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    def extract_no_squashed_commit_multiple_processes(self):
        repo = self.get_repo()
        origin_commits  = self.get_commit_list()
        RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
        rm = RefactoringMiner(RMPath)
        jsonOutputDirectory = "./test_RM_speed/"
        create_folder(jsonOutputDirectory)
        import os
        process_num = os.cpu_count()
        sub_c_num = int(len(origin_commits)/process_num)

        processes = []
        for i in range(1,process_num+1):
            processes.append(Process(target=RMDetectWithOutput, args=(rm, origin_commits[(i-1)*sub_c_num:min(i*sub_c_num,len(origin_commits))], repo, jsonOutputDirectory)))
        for p in processes:
            p.start()
        for p in processes:
            p.join()


    def test_extract_no_squahsed_commit_refactoring_toy_example_single_thread(self):
        start = time.time()
        self.extract_no_squashed_commit_single_thread()
        end = time.time()
        print(f"Time: {end-start}")   # 9.706s

    def test_extract_no_squahsed_commit_refactoring_toy_example_5_threads(self):
        start = time.time()
        self.extract_no_squashed_commit_multiple_threads()
        end = time.time()
        print(f"Time: {end-start}")  #  7.618

    def test_extract_no_squahsed_commit_mbassador_single_thread(self):
        start = time.time()
        self.extract_no_squashed_commit_single_thread()
        end = time.time()
        print(f"Time: {end-start}")  # 145.250s

    def test_extract_no_squahsed_commit_mbassador_10_threads(self):
        start = time.time()
        self.extract_no_squashed_commit_multiple_threads()
        end = time.time()
        print(f"Time: {end-start}")   # 154.420s

    def test_extract_no_squahsed_commit_mbassador_multiple_process(self):
        start = time.time()
        self.extract_no_squashed_commit_multiple_processes()
        end = time.time()
        print(f"Time: {end-start}")   # 46.974s


if __name__ == '__main__':
    unittest.main()
