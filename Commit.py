import json

class Commit:
    def __init__(self,info:str):
        self.commitID=info["commit"]
        self.parentID=info["parent"].split(" ")
        self.suject=None
        self.commit_notes=info["commit_notes"]
        self.commiter=info["commiter"]
        self.isMerge=True if len(self.parentID)>1 else False
        self.parent=[]
        self.child=[]
        self.added=False
        self.head=False

    def setParent(self,pCommit)->None:
        self.parent.append(pCommit)

    def setChild(self,cCommit)->None:
        self.child.append(cCommit)

    def getConnections(self):
        return self.connectedTo

    def getAdded(self):
        return self.added

    def setAdded(self):
        self.added=True

    def getHead(self):
        return self.head
    def setHead(self):
        self.head=True

if __name__ =="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal/test.json"
    with open(path) as f:
        data=json.loads("["+f.read()+"]")
    data=data[0]
    commits=[]
    num=0
    for each in data:
        num=num+1
        commits.append(Commit(each))
    print(len(commits))
    print(num)
