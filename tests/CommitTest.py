import unittest
import json
from commitProcess.Commit import Commit

class CommitTest(unittest.TestCase):
    def test_init_jfinal_gitLog_as_Commit_length_should_be_474(self):
        path = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal/gitLog.json"
        with open(path) as f:
            data = json.loads("[" + f.read() + "]")
        commits = []
        for each in data:
            commits.append(Commit(each))
        self.assertEqual(len(commits), 474)
