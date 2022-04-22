import unittest
import json
from commitProcess.Commit import Commit

class CommitTest(unittest.TestCase):
    def test_init_refactoring_toy_example_gitLog_as_Commit_length_should_be_474(self):
        path = "gitLog.json"
        with open(path) as f:
            data = json.loads("[" + f.read() + "]")
        commits = []
        for each in data:
            commits.append(Commit(each))
        self.assertEqual(len(commits), 65)
