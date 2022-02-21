import sys
sys.path.append('../')
from RefactoringOperation.RMcommit import RMcommit
import glob
import json

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
        resDict[each] = dict1[each]/(dict2.get(each,1))
        if dict2.get(each) ==None:
            dict2Is0[each]=dict2Is0.get(each,0)+1
    return resDict

if __name__ =="__main__":
    # repoNames = ["retrolambda","mbassador"]
    repoNames = ["jfinal", "mbassador", "javapoet", "jeromq", "seyren", "retrolambda", "truth",
                 "sshj", "xabber-android", "android-async-http", "redisson", "giraph", "spring-data-rest",
                 "blueflood", "byte-buddy", "HikariCP", "goclipse", "atomix", "morphia", "PocketHub"]

    sumRoSquashDict = dict()
    sumRONoSquashDict = dict()
    sumOnlyInSquash = dict()
    for each in repoNames:
        roSquashDict = dict()
        roNoSquashDict = dict()
        onlyInSquash = dict()
        # repo = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"+each+"/"
        repo = "/home/chenlei/RA/setversion/experimentResult/"+each+"/"
        roNoSquashDict = dictAdd(roNoSquashDict,getROType(repo+"1"+"/"))
        sumRONoSquashDict = dictAdd(sumRONoSquashDict, roNoSquashDict)
        for i in range(2,5):
            dictSquashI = getROType(repo+str(i)+"/")
            roSquashDict = dictAdd(roSquashDict,dictSquashI)
        sumRoSquashDict = dictAdd(sumRoSquashDict,roSquashDict)
        res = dictDivide(roSquashDict,roNoSquashDict,onlyInSquash)
        print("repoName: {}, only in squash number: {}".format(each,len(onlyInSquash)))
        print(onlyInSquash)
    res = dictDivide(sumRoSquashDict,sumRONoSquashDict,sumOnlyInSquash)
    print("RO in squash/RO in no squash:{}".format(sorted(res.items(),key=lambda x:x[1],reverse=True)))
    print(sumOnlyInSquash)
