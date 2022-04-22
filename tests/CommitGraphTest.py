import unittest
import json
from commitProcess.Commit import Commit
from commitProcess.CommitGraph import CommitGraph

class CommitGraphTest(unittest.TestCase):
    def test_getSCList_refactoring_toy_example_should_return_list_length_31(self):
        path = "gitLog.json"
        with open(path) as f:
            data = json.loads("[" + f.read() + "]")
        commits = []
        for each in data:
            commits.append(Commit(each))
        sc_lists = []
        cG = CommitGraph(commits)
        head = cG.buildGraph()
        sc_lists = cG.getSClist()
        print(sc_lists)
        self.assertEqual(len(sc_lists), 31)

    def test_clusterList_cluster_length_5_list_2by2(self):
        cG = CommitGraph([])
        test = [1, 2, 3, 4, 5]
        result, num = cG.clusterList(test, 2)
        self.assertEqual(result, [[[1, 2], [3, 4], [5]], [[1], [2, 3], [4, 5]]])