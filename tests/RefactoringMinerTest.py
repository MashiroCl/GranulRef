import unittest
from refactoring_mining.miner import RefactoringMiner, RefDiff


class RefactoringMinerTest(unittest.TestCase):
    def test_detect_(self):
        RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
        rm = RefactoringMiner(RMPath)
        repository = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/retrolambda"
        output = "/Users/leichen/Desktop"
        commitID = "bc99e75c2fa4b56325910e445283d1b24cb2618d"
        rm.detect(repository, output, commitID)


    def test_RefDiff_detect_mbassador(self):
        RDPath = "/Users/leichen/Desktop/RefDiff.jar"
        rd = RefDiff(RDPath)
        repository = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
        output = "/Users/leichen/Desktop/output/mbassador"
        commitID = "0a7ed2e651b04756ff210eacb68671d5cd0c2f2b"
        commitID = "12a3e778e99564b1c7031516a26786a9a96362db"
        rd.detect(repository,output,commitID)


    def test_RM_detect(self):
        RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
        rm = RefactoringMiner(RMPath)
        repository = "/Users/leichen/JAVA/gradle_test"
        repository = "/Users/leichen/JAVA/gradle_test_refs/squashed_git"
        output = "/Users/leichen/JAVA/gradle_test_refs/coarse-grained/"
        # commitID = "106b9450f986e5e9b570a023be930ff2615e5d1b"
        # commitID = "bf2d40ceb705f2d7486768c69b1c2bbadff0e455"
        # commitID = "1e660ff932b0c74173bbe95b0a9f060e1f28c6d8"
        # commitID = "b06a8273f44c1b46770e6e6f32d80d4fc2644250"
        commitID = "f77d38d9cdb006eaaabcf0703c1b006c89b5388c"
        rm.detect(repository, output, commitID)


    def test_detect2(self):
        RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
        rm = RefactoringMiner(RMPath)
        repository = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/RQs/squashed_output"
        output = "./temp/"
        commitID = "0362c92af77db27be425b3a0365309e17d043059"
        rm.detect(repository, output, commitID)

