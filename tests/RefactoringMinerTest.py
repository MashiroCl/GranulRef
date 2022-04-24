import unittest
from refactoringMiner.RefactoringMiner import RefactoringMiner


class RefactoringMinerTest(unittest.TestCase):
    def test_detect_(self):
        RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner-2.2.0/bin/RefactoringMiner"
        rm = RefactoringMiner(RMPath)
        repository = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/retrolambda"
        output = "/Users/leichen/Desktop"
        commitID = "bc99e75c2fa4b56325910e445283d1b24cb2618d"
        rm.detect(repository, output, commitID)



