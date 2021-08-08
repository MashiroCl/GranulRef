import json
from Commit import Commit
from jsonUtils import JsonUtils

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


    def getCClist(self)->list:
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

    def getCCListStr(self,cc_lists)->str:
        cc_lists_str = []
        for each1 in cc_lists:
            temp = []
            for each2 in each1:
                temp.append(each2.commitID)
            cc_lists_str.append(temp)
        return cc_lists_str

    'As the squash method changed to git-stein, this method is discarded'
    # def processCClist(self,cclist):
    #     for i in range(len(cclist)):
    #         if i!=len(cclist)-1:
    #             for each2 in cclist[i]:
    #                 if each2.parent[0] not in cclist[i]:
    #                     # print("being removed",each2.commitID," parent id:",each2.parent[0].commitID)
    #                     cclist[i].remove(each2)
    #         else:
    #             for each3 in cclist[i]:
    #                 if len(each3.parent)==0:
    #                     cclist[i].remove(each3.child[0])
    #                     cclist[i].remove(each3)
    #     return cclist

    'cluster list of lists according to num input'
    def clusterList(self,lists:list,num:int):
        if num<1:
            print("cluster structured according to commit history")
            return
        result=[]
        for each1 in lists:
            if len(each1)>num:
                cluster=len(each1)//num
                remain=len(each1)-cluster*num
                for i in range(cluster):
                    temp=[]
                    for j in range(num):
                        temp.append(each1[i*num+j])
                    result.append(temp)
                if remain!=0:
                    temp=each1[-1*remain:]
                    result.append(temp)
            else:
                result.append(each1)
        return result

    def clusterProcess(self,l:list,num:int):
        result=[]
        cluster = len(l) // num
        remain = len(l) - cluster * num
        for i in range(cluster):
            temp = []
            for j in range(num):
                temp.append(l[i * num + j])
            result.append(temp)
        if remain != 0:
            temp = l[-1 * remain:]
            for each in temp:
                result.append([each])
        return result

    'cluster list of lists according to num input'
    'considering different cluster method'
    def clusterList2(self,l:list,num:int):
        if num<1:
            print("cluster structured according to commit history")
            return
        result=[]
        numAfterSquash=0
        if len(l)>num:
            for i in range(num):
                if (i+num)<=len(l):
                    temp = []
                    for each in l[:i]:
                        temp.append([each])
                        numAfterSquash += 1
                    for each in self.clusterProcess(l[i:],num):
                        temp.append(each)
                        numAfterSquash+=1
                    result.append(temp)
        else:
            numAfterSquash+=len(l)
        return result,numAfterSquash

    def clusterList3(self,l:list,num:int):
        if num<1:
            print("cluster structured according to commit history")
            return
        result=[]
        candidateNum=len(l)%num+1
        for i in range(candidateNum):
            temp=[]
            j=i
            for each in l[:j]:
                temp.append([each])
            while j+num<=len(l):
                temp.append(l[j:j+num])
                j=j+num
            for each in l[j:]:
                temp.append([each])
            result.append(temp)
        numAfterSquash=len(result[0])
        return result,numAfterSquash


def printCClists(cc_lists):
    num=0
    for each1 in cc_lists:
        print("_________________________")
        for each2 in each1:
            num=num+1
            print(each2.commitID)
    print("_________________________")
    print("in total",num,"commits")
    # for i in range(6):
    #     print("_________________________")
    #     for each in cc_lists[i]:
    #         print(each.commitID)
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

def listSet(l):
    temp=[]
    for each in l:
        temp.append(list(set(each)))
    return temp



if __name__=="__main__":
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal/test.json"
    path="/Users/leichen/ResearchAssistant/InteractiveRebase/data/refactoring-toy-example"

    js=JsonUtils()
    js.setRepoPath(path)
    js.gitJson()
    commits=js.jsonToCommit()
    cc_lists = []

    cG = CommitGraph(commits)
    head = cG.formGraph()
    cc_lists=cG.getCClist()
    max=0
    a=0
    for each in range(len(cc_lists)):
        if len(cc_lists[each])>max:
            max=len(cc_lists[each])
            a=each
    print(max)
    result=cG.clusterList2(cc_lists[a],3)
    print(len(result))
    for each in result:
        print(each)

    test=[1,2,3,4,5,6,7,8,9,10]
    result=cG.clusterList2(test,5)
    for each in result:
        print(each)

    test=[1,2,3,4]
    result,num=cG.clusterList3(test,2)
    print(num)
    print(result)