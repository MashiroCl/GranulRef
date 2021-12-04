import sys
sys.path.append('../')
from RefactoringOperation.RMcommit import RMcommit
import glob


def _getROSet(filePath:str):
    '''
    use json file of commit to extract refactoring operation set
    :param filePath: path for a Refactoirng Miner result
    :return: refactoring operation set
    '''
    rMcommit = RMcommit(filePath)
    ROset = set()
    for ro in rMcommit.refactorings:
        ROset.add(ro)
    return ROset

def _getRMResultsFile(repoPath:str):
    filePaths = glob.glob(repoPath+"*.json")
    return filePaths

def getSet(repoPath:str):
    '''
    return refactoring operation set
    :param repoPath: repoName +'xbyx'
    :return: refatoring operation set
    '''
    setTemp = set()
    filePaths = _getRMResultsFile(repoPath)
    for filePath in filePaths:
        setTemp=setTemp.union(_getROSet(filePath))
    return setTemp


if __name__ =="__main__":
    temp = "refactoring-toy-example"
    experimentPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"
    set1by1 = getSet(experimentPath + temp + "/1/")
    set2by2 = getSet(experimentPath + temp + "/2/")
    set3by3 = getSet(experimentPath + temp + "/3/")
    set4by4 = getSet(experimentPath + temp + "/4/")
    # print(len(set1by1))
    # print(len(set2by2.union(set3by3.union(set4by4))))
    squashedSets = set2by2.union(set3by3.union(set4by4))
    disappear = len(set1by1-squashedSets)/len(set1by1)
    print(disappear)
    # for each in set1by1:
    #     print(each)cd .
    # print("--------------------------------------------------------------------------------------")
    # for each in squashedSets:
    #     print(each)
    # print("--------------------------------------------------------------------------------------")
    # for each in (set1by1-squashedSets):
    #     print(each)

