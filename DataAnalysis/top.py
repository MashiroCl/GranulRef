import sys
sys.path.append('../')
import pandas as pd
from DataAnalysis.setAnalysis import getSet
from DataAnalysis.typeAnalysis import buildRODict, setDivision

def dictAdd(dict1,dict2):
    for each in dict2:
        dict1[each] = dict1.get(each,0)+dict2[each]
    return dict1

def disappearDict(repo:str):
    set1by1 = getSet(repo + "/1/")
    set2by2 = getSet(repo + "/2/")
    set3by3 = getSet(repo + "/3/")
    set4by4 = getSet(repo + "/4/")
    squashedSets = set2by2.union(set3by3.union(set4by4))
    return buildRODict(set1by1),buildRODict(set1by1 - squashedSets)

def disappearRatio(repos:list, topNum:int):
    dict1by1s = dict()
    disappearDicts = dict()
    for repo in repos:
        dict1by1Temp,disappearDictTemp = disappearDict(repo)
        dictAdd(dict1by1s, dict1by1Temp)
        dictAdd(disappearDicts, disappearDictTemp)
    resDict = setDivision(disappearDicts, dict1by1s)

    print("top {} disappear RO          : {}".format(topNum, sorted(disappearDicts.items(), key=lambda x: x[1], reverse=True)[:topNum]))
    print("top {} 1by1 detected RO      : {}".format(topNum, sorted(dict1by1s.items(), key=lambda x: x[1], reverse=True)[:topNum]))
    print("top {} disappearance Ratio RO: {}".format(topNum, sorted(resDict.items(), key=lambda x: x[1], reverse=True)[:topNum]))


def top(num:int):
    # repoNames = ["retrolambda", "sshj", "mbassador"]
    repoNames = ["jfinal", "mbassador", "javapoet", "jeromq", "seyren", "retrolambda", "truth",
                 "sshj", "xabber-android", "android-async-http", "redisson", "giraph", "spring-data-rest",
                 "blue-flood", "byte-buddy", "HikariCP", "goclipse", "atomix", "morphia", "PocketHub"]
    # experimentPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"
    experimentPath = "/home/chenlei/RA/setversion/experimentResult/"
    # resDict = dict()
    # for repoName in repoNames:
    #     resDict = dictAdd(resDict,disappearDict(experimentPath+repoName))
    repos = [experimentPath+x for x in repoNames]
    resDict = disappearRatio(repos,num)

    # return sorted(resDict.items(),key=lambda x:x[1],reverse=True)[:num]

if __name__ =="__main__":
    args = sys.argv
    top(int(args[1]))