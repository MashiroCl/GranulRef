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
    repoName = "retrolambda"

    # experimentPath = "/home/chenlei/RA/setversion/experimentResult/"
    experimentPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"

    set1by1 = getSet(experimentPath + repoName + "/1/")
    set2by2 = getSet(experimentPath + repoName + "/2/")
    set3by3 = getSet(experimentPath + repoName + "/3/")
    set4by4 = getSet(experimentPath + repoName + "/4/")

    squashedSets = set2by2.union(set3by3.union(set4by4))
    print("squashedSets", buildRODict(squashedSets))
    disappearRODict = buildRODict(set1by1 - squashedSets)
    set1by1RODict = buildRODict(set1by1)
    print("disappearRODict", disappearRODict)
    print("set1by1RODict", set1by1RODict)

    'Calculate the number of disappeared RO in squashed set divide the number of Ro of same type in no squash set'
    "Example result: {'Pull Up Method': 1.0, 'Move Class': 0.5} means "
    "100% of the Pull Up Method which is detected when no squash disappeared because of squash,"
    "50% of the Move Class which is detected when no squash disappeared because of squash"

    disappearDictRatio = setDivision(disappearRODict, set1by1RODict)
    # disappear = len(set1by1-squashedSets)/len(set1by1)

    print("Disappear Ratio: {}".format(disappearDictRatio))

    # for each in squashedSets:
    #     if each.type == "Move Class":
    #         print("in squashedSets: ",each.description)
    # for each in set1by1:
    #     if each.type == "Move Class":
    #         # print(each.type)
    #         print("in set1by1: ",each.description)

    all = set1by1.union(set2by2.union(set3by3.union(set4by4)))
    missingRatio = setDivision(buildRODict((all-set1by1)),buildRODict(all))
    print("Missing Ratio: {}".format(disappearDictRatio))


if __name__ == "__main__":
    ROTypeAnalysis()
