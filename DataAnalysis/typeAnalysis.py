import sys
sys.path.append('../')
import pandas as pd
from DataAnalysis.setAnalysis import getSet
from MyRepository import create_folder
import os


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


def writeSet2CSV(repoName,writtenSet,path,csvName=" "):
    belongedCommits = list()
    types = list()
    descriptions = list()
    for each in writtenSet:
        belongedCommits.append(each.belongedCommit)
        types.append(each.type)
        descriptions.append(each.description)
        print("commitID:{}, type: {}, description: {}".format(each.belongedCommit,each.type,each.description))
        dataFrame = pd.DataFrame({"commitID":belongedCommits,"type":types,"description":descriptions})

    csvFolder = os.path.join(path,repoName)
    csvPath = os.path.join(csvFolder,csvName)
    if not os.path.exists(csvFolder):
        create_folder(csvFolder)
    if os.path.exists(csvPath):
        print("file {} exists, stop writing csv".format(csvPath))
        return
    dataFrame.to_csv(csvPath,index=False,sep=",")

def ROTypeAnalysis(repoName,csvPath):
    # args = sys.argv
    # repoName = args[1]


    # experimentPath = "/home/chenlei/RA/setversion/experimentResult/"
    experimentPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"

    set1by1 = getSet(experimentPath + repoName + "/1/")
    set2by2 = getSet(experimentPath + repoName + "/2/")
    set3by3 = getSet(experimentPath + repoName + "/3/")
    set4by4 = getSet(experimentPath + repoName + "/4/")

    squashedSets = set2by2.union(set3by3.union(set4by4))
    all = set1by1.union(set4by4.union(set3by3.union(set2by2)))

    disappearRODict = buildRODict(set1by1 - squashedSets)
    set1by1RODict = buildRODict(set1by1)


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

    writeSet2CSV(repoName, set1by1-squashedSets, path,"disappear.csv")
    writeSet2CSV(repoName, all-set1by1, path, "missing.csv")

if __name__ == "__main__":
    path = "/Users/leichen/Desktop"
    ROTypeAnalysis(repoName = "mbassador",csvPath=path)

