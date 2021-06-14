import json
from Commit import Commit

class CommitGraph():
    def __init__(self,commits:list):
        self.commits=commits
        self.num=len(commits)

    def whichCommit(self,commitID:str)->Commit:
        for each in self.commits:
            if each.commitID==commitID:
                return each

    def formGraph(self)->Commit:
        head=None
        tail=None
        for each in self.commits:
            if head==None:
                head=each
            for eachID in each.parentID:
                if len(eachID)>3:
                    each.setParent(self.whichCommit(eachID))
                    (self.whichCommit(eachID)).setChild(each)
                else :
                    tail=each
        return head

    def isConnected(self,c1,c2)->bool:
        flag=False
        for each in c1.parent:
            if  each==c2:
                flag=True
        for each in c1.child:
            if each==c2:
                flag=True
        return flag

    def add(self,commit,cc_list)->list:
        if not commit.getAdded():
            cc_list.append(commit)
            commit.setAdded()
        return cc_list

    def addToCCLIST(self,commit:Commit,cc_list,cc_lists):
        if len(commit.parent) == 2:
            if len(cc_list) != 0:
                cc_lists.append(cc_list)
                cc_list = []
        elif len(commit.child) > 1:
            if len(cc_list) != 0:
                cc_lists.append(cc_list)
                cc_list = []
            self.add(commit,cc_list)
        else:
            self.add(commit,cc_list)
        return cc_list,cc_lists

    def DFSUtil(self,node:Commit,visited:set,cc_list:list,cc_lists:list):
        visited.add(node)
        temp1_list=cc_list
        c_list, c_lists = self.addToCCLIST(node, cc_list, cc_lists)
        for each in self.whichCommit(node.commitID).parent:
            if each not in visited:
                self.DFSUtil(each,visited,c_list,c_lists)

    def DFS(self,node,cc_lists):
        cc_list=[]
        visited=set()
        self.DFSUtil(node,visited,cc_list,cc_lists)


    def getCClist(self):
        temp=[]
        for each in self.commits:
            temp.append(each)
        # temp.append(each for each in self.commits)
        #Remove merge
        for each in temp:
            if len(each.parent)==2:
                temp.remove(each)

        #find head
        for i in range(len(temp)):
            if len(temp[i].child)==0:
                temp[i].setHead()

            elif len(temp[i].child)==1:
                #child is merge
                if len(temp[i].child[0].parent)==2:
                    temp[i].setHead()

            elif len(temp[i].child)>1:
                temp[i].setHead()

        cc_lists=list()
        #for each head find connected commit sequence
        for i in range(len(temp)):
            if temp[i].getHead():
                cc_list=[temp[i]]
                p=temp[i].parent[0]
                while not (p.getHead()):
                    if len(p.parent)==1:
                        cc_list.append(p)
                    if len(p.parent)==0:
                        cc_list.append(p)
                        break
                    else:
                        p=p.parent[0]
                cc_lists.append(cc_list)

        return cc_lists

def printCClists(cc_lists):
    num=0
    for each1 in cc_lists:
        print("_________________________")
        for each2 in each1:
            num=num+1
            print(each2.commitID)
    print("_________________________")
    print("in total",num,"commits")

def listSet(l):
    temp=[]
    for each in l:
        temp.append(list(set(each)))
    return temp



if __name__=="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal/test.json"
    with open(path) as f:
        data=json.loads("["+f.read()+"]")

    commits=[]
    data=data[0]
    for each in data:
        commits.append(Commit(each))

    cc_lists = []

    cG = CommitGraph(commits)
    head = cG.formGraph()
    cc_lists=cG.getCClist()
    printCClists(cc_lists)
