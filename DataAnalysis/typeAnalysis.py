import sys
import pandas as pd
sys.path.append('../')
from DataAnalysis.setAnalysis import getSet
from MyRepository import create_folder

def buildRODict(roSet):
    resDict = dict()
    for each in roSet:
        roType = each.type
        resDict[roType] = resDict.get(roType, 0) + 1
    return resDict
    # print("Disappearance:", disappear)
def setDivision(seta, setb):
    '''
    seta intersect setb = seta, if element e exists in seta, division = seta[e]/setb[e]
    :param seta:
    :param setb:
    :return: a float number
    '''
    resDict = dict()
    for a in seta:
        resDict[a] = seta.get(a) / setb.get(a, 1)
    return resDict

def ROTypeAnalysis():
    # args = sys.argv
    # repoName = args[1]
    repoName = "refactoring-toy-example"
    # repoName = "retrolambda"

    # experimentPath = "/home/chenlei/RA/setversion/experimentResult/"
    experimentPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"

    set1by1 = getSet(experimentPath + repoName + "/1/")
    set2by2 = getSet(experimentPath + repoName + "/2/")
    set3by3 = getSet(experimentPath + repoName + "/3/")
    set4by4 = getSet(experimentPath + repoName + "/4/")

    squashedSets = set2by2.union(set3by3.union(set4by4))
    # print("squashedSets", buildRODict(squashedSets))
    disappearRODict = buildRODict(set1by1 - squashedSets)
    set1by1RODict = buildRODict(set1by1)
    # print("disappearRODict", disappearRODict)
    # print("set1by1RODict", set1by1RODict)

    'Calculate the number of disappeared RO in squashed set divide the number of Ro of same type in no squash set'
    "Example result: {'Pull Up Method': 1.0, 'Move Class': 0.5} means "
    "100% of the Pull Up Method which is detected when no squash disappeared because of squash,"
    "50% of the Move Class which is detected when no squash disappeared because of squash"

    disappearDictRatio = setDivision(disappearRODict, set1by1RODict)
    # disappear = len(set1by1-squashedSets)/len(set1by1)

    print("Disappear Ratio: {}".format(disappearDictRatio))

    all = set1by1.union(set2by2.union(set3by3.union(set4by4)))
    missingRatio = setDivision(buildRODict((all-set1by1)),buildRODict(all))
    print("Missing Ratio: {}".format(missingRatio))

    belongedCommits = list()
    types = list()
    descriptions = list()
    for each in set1by1 - squashedSets:
        belongedCommits.append(each.belongedCommit)
        types.append(each.type)
        descriptions.append(each.description)
        print("commitID:{}, type: {}, description: {}".format(each.belongedCommit,each.type,each.description))
        dataFrame = pd.DataFrame({"commitID":belongedCommits,"type":types,"description":descriptions})

    # import os
    # csv_path = os.path.join("/Users/leichen/ResearchAssistant/csv/",repoName)
    # create_folder(csv_path)
    # dataFrame.to_csv(os.path.join(csv_path,"disappear.csv"),index=False,sep=",")
if __name__ == "__main__":
    ROTypeAnalysis()
