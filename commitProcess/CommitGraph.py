"""
commit graph class, contains commits extracted from a repository
"""

from commitProcess.Commit import Commit


class CommitGraph:
    def __init__(self, commits: list):
        self.commits = commits
        self.num = len(commits)

    def whichCommit(self, commitID: str) -> Commit:
        """
        search a Commit entity using commit id
        :param commitID:
        :return:
        """
        for each in self.commits:
            if each.commitID == commitID:
                return each

    def buildGraph(self) -> Commit:
        """
        build commits into a graph using parent/child commit relationship
        :return: head of commit graph(the latest commit)
        """
        head = None
        tail = None
        for each in self.commits:
            if head == None:
                head = each
            for eachID in each.parentID:
                if len(eachID) > 3:
                    each.setParent(self.whichCommit(eachID))
                    (self.whichCommit(eachID)).setChild(each)
                else:
                    tail = each
        return head

    # def add(self,commit,cc_list)->list:
    #     if not commit.getAdded():
    #         cc_list.append(commit)
    #         commit.setAdded()
    #     return cc_list

    def getSClist(self) -> list:
        '''
        search straight commit sequences in commit history
        :return: 2d array of straight commit sequences
        '''
        temp = []
        for each in self.commits:
            temp.append(each)

        # Remove merge commit
        for each in temp:
            if len(each.parent) == 2:
                temp.remove(each)

        # find head
        for i in range(len(temp)):
            if len(temp[i].child) == 0:
                temp[i].setHead()

            elif len(temp[i].child) == 1:
                # child is merge
                if len(temp[i].child[0].parent) == 2:
                    temp[i].setHead()

            elif len(temp[i].child) > 1:
                temp[i].setHead()

        sc_lists = list()
        # for each head find connected commit sequence
        for i in range(len(temp)):
            if temp[i].isHead():
                sc_list = [temp[i]]
                # Initial commit has two child commit
                if (len(temp[i].parent) == 0):
                    continue
                p = temp[i].parent[0]
                while not (p.isHead()):
                    if len(p.parent) == 1:
                        sc_list.append(p)
                    if len(p.parent) == 0:
                        sc_list.append(p)
                        break
                    else:
                        p = p.parent[0]
                sc_lists.append(sc_list)

        return sc_lists

    def getSCListStr(self, sc_lists) -> str:
        sc_lists_str = []
        for each1 in sc_lists:
            temp = []
            for each2 in each1:
                temp.append(each2.commitID)
            sc_lists_str.append(temp)
        return sc_lists_str

    def clusterList(self, l: list, num: int):
        res = list()
        if (len(l) < num):
            temp = []
            for x in l:
                temp.append([x])
            res.append(temp)
        elif (len(l) == num):
            res.append(l)
        else:
            for i in range(num):
                if i + num > len(l):
                    break
                temp = []
                for each in l[:i]:
                    temp.append([each])
                n = len(l[i:]) // num
                if len(l[i:]) >= num:
                    for j in range(n):
                        temp.append(l[i + j * num:i + (j + 1) * num])
                for each in l[i + n * num:]:
                    temp.append([each])
                res.append(temp)

        return res, len(res[0])


    def printSClists(self, sc_lists):
        num = 0
        for each1 in sc_lists:
            print("_________________________")
            for each2 in each1:
                num = num + 1
                print(each2.commitID)
        print("_________________________")
        print("in total", num, "commits")