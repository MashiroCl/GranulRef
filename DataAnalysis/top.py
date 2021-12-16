import sys
import pandas as pd
sys.path.append('../')
from DataAnalysis.setAnalysis import getSet
from DataAnalysis.typeAnalysis import buildRODict

def dictAdd(dict1,dict2):
    for each in dict2:
        dict1[each] = dict1.get(each,0)+dict2[each]
    return dict1

def getDisappearDict(repo:str):
    set1by1 = getSet(repo + "/1/")
    set2by2 = getSet(repo + "/2/")
    set3by3 = getSet(repo + "/3/")
    set4by4 = getSet(repo + "/4/")
    squashedSets = set2by2.union(set3by3.union(set4by4))
    return buildRODict(squashedSets)

def top(num:int):
    repoNames = ["refactoring-toy-example","retrolambda"]
    experimentPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"
    resDict = dict()
    for repoName in repoNames:
        resDict = dictAdd(resDict,getDisappearDict(experimentPath+repoName))

    return sorted(resDict.items(),key=lambda x:x[1],reverse=True)[:num]


print(top(5))