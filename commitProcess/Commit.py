"""
git commit class
"""


class Commit:
    """
    turn json formatgir commit info into Commit Class
    """
    def __init__(self, info: str):
        self.commitID = info["commit"]
        self.parentID = info["parent"].split(" ")
        self.suject = None
        self.commit_notes = info["commit_notes"]
        self.commiter = info["commiter"]
        self.isMerge = True if len(self.parentID) > 1 else False
        self.parent = []
        self.child = []
        # self.added=False
        self.head = False

    def setParent(self, pCommit) -> None:
        """
        set pCommit as the parent commit of the current one
        :param pCommit:
        :return:
        """
        self.parent.append(pCommit)

    def setChild(self, cCommit) -> None:
        """
        set cCommit as the child commit of thecurrent one
        :param cCommit:
        :return:
        """
        self.child.append(cCommit)

    # def getConnections(self):
    #     """
    #
    #     :return:
    #     """
    #     return self.connectedTo

    # def getAdded(self):
    #     return self.added
    #
    # def setAdded(self):
    #     self.added=True

    def getHead(self):
        return self.head

    def setHead(self):
        """
        set commit as the head(1st) commit of a sequence of commit
        :return:
        """
        self.head = True
