import sys
sys.path.append('../')
from RefactoringOperation.RMcommit import RMcommit
import glob

def getROType(repoPath):
    filePaths = glob.glob(repoPath+"*.json")
    RTdict = dict()
    for eachFile in filePaths:
        rMcommit = RMcommit(eachFile)
        for ro in rMcommit.refactorings:
            RTdict[ro.type] = RTdict.get(ro.type,0)+1
    return RTdict

def dictAdd(dict1,dict2):
    for each in dict2:
        dict1[each] = dict1.get(each,0)+dict2[each]
    return dict1

def dictDivide(dict1,dict2,dict2Is0):
    resDict = dict()
    for each in dict1:
        resDict[each] = dict1[each]/(dict2.get(each,1)*3)
        if dict2.get(each) ==None:
            dict2Is0.append(each)
    return resDict

if __name__ =="__main__":
    # repoName = ["mbassador"]
    repoNames = ["jfinal", "mbassador", "javapoet", "jeromq", "seyren", "retrolambda", "truth",
                 "sshj", "xabber-android", "android-async-http", "redisson", "giraph", "spring-data-rest",
                 "blue-flood", "byte-buddy", "HikariCP", "goclipse", "atomix", "morphia", "PocketHub"]
    roSquashDict = dict()
    roNoSquashDict = dict()
    onlyInSquash = list()
    for each in repoName:
        # repo = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"+each+"/"
        repo = "/home/chenlei/RA/setversion/experimentResult/"+each+"/"
        roNoSquashDict = dictAdd(roNoSquashDict,getROType(repo+"1"+"/"))
        for i in range(2,5):
            roSquashDict = dictAdd(roSquashDict,getROType(repo+str(i)+"/"))
    res = dictDivide(roSquashDict,roNoSquashDict,onlyInSquash)
    print(sorted(res.items(),key=lambda x:x[1],reverse=True))
    print(onlyInSquash)
    "'Change Type Declaration Kind', 'Extract Subclass', 'Push Down Method', 'Push Down Attribute'"