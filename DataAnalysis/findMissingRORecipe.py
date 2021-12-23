import glob
import os

def searchRecipe(commitID:str,experimentResultPath:str):
    '''
    Get recipe lists contains commitID
    :param commitID:
    :param experimentResultPath:
    :return:
    '''
    files = glob.glob(os.path.join(experimentResultPath,"log[2-4].txt"))

    result = list()
    for eachFile in files:
        with open(eachFile) as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if commitID in lines[i]:
                    squashedList = eval(lines[i].split("squashed commit list ")[1])
                    recipeLists = eval(lines[i - 1].split("squashable commit list ")[1])
                    num=-1
                    for j in range(len(squashedList)):
                            if commitID in squashedList[j]:
                                num=j
                                break
                    result = recipeLists[num]

    return result



if __name__ =="__main__":
    repoName = "mbassador"
    experimentResultPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"+repoName
    commitID = "b49639ab74870701a510ba201c13c5fdf487536b"
    result = searchRecipe(commitID,experimentResultPath)
    print(str(result).replace("\'",""))
    print(commitID)
