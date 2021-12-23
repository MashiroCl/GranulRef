from commitProcess.Commit import Commit
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

    def add(self,commit,cc_list)->list:
        if not commit.getAdded():
            cc_list.append(commit)
            commit.setAdded()
        return cc_list


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
                '''Initial commit has two child commit'''
                if(len(temp[i].parent)==0):
                    continue
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

    # def clusterList(self,l:list,num:int):
    #     if num<1:
    #         print("cluster structured according to commit history")
    #         return
    #     result=[]
    #     candidateNum=len(l)%num+1
    #     for i in range(candidateNum):
    #         temp=[]
    #         j=i
    #         for each in l[:j]:
    #             temp.append([each])
    #         while j+num<=len(l):
    #             temp.append(l[j:j+num])
    #             j=j+num
    #         for each in l[j:]:
    #             temp.append([each])
    #         result.append(temp)
    #     numAfterSquash=len(result[0])
    #     return result,numAfterSquash

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

def printCClists(cc_lists):
    num=0
    for each1 in cc_lists:
        print("_________________________")
        for each2 in each1:
            num=num+1
            print(each2.commitID)
    print("_________________________")
    print("in total",num,"commits")

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

    test=[1,2,3,4]
    result,num=cG.clusterList(test,2)
    print(result)
