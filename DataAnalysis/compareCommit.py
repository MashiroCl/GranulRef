import glob
import os
import json
def writeRecipe(list,output):
    recipe = {}
    recipe["forcedClusters"] = []
    recipe["forcedClusters"].append(list)
    with open(output, 'w') as f:
        json.dump(recipe, f)

def squash(recipe,git_stein,output,repository,steinOutput):
    command = "java -jar " + git_stein + " Clusterer " + "--recipe=" + recipe + " -v -o " + output + " " + repository + ">" + steinOutput + "/stein.log"
    print(command)

    os.system(command)
    # 'add remote'
    # command = "(cd " + output + " && git remote add origin https://example.jp/dummy_url.git)"
    # os.system(command)

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
                    recipeLists = eval(lines[i].split("squashable commit list ")[1])
                    for recipeList in recipeLists:
                        if commitID in recipeList:
                            result.append(recipeList)

    # for each in result:
    #     print("squashable candidate: {}".format(each))
    return result

def findAfterSquash(steinLog:str,commit):
    with open(steinLog,"r") as f:
        lines=f.readlines()
    result=[]
    for eachLine in lines:
        if " Rewrite commit: " in eachLine:
            temp = eachLine.split("Rewrite commit: ")[1].split(" -> ")
            if temp[0].strip() == commit.strip():
                result.append(temp[1].strip())
    return result

def squashAndGetAfterSquashId(repoName,commitID,list):
    output = "/Users/leichen/Desktop/RTEnew/test"
    if os.path.exists(output):
        command = "rm -rf " + output
        os.system(command)
    stein_output = "."
    git_stein = "/Users/leichen/Code/git-stein/build/libs/git-stein-all.jar"
    recipe = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/DataAnalysis/recipe.json"
    repository = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName

    writeRecipe(list, recipe)
    # squash(recipe,git_stein,output,repository,stein_output)
    squash(recipe=recipe, git_stein=git_stein, output=output, repository=repository, steinOutput=stein_output)
    afterSquash = findAfterSquash(
        "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/DataAnalysis/stein.log", commitID)
    print("Before squash {}\nAfter squash {}".format(list, afterSquash))


def findAfterSquashLog(logFile,list):
    '''
    find squashed git commit id in logx.txt according to list
    :param logFile: file path for logx.txt
    :param list: being squashed commit list
    :return: squashed commit ID
    '''
    with open(logFile) as f:
        lines = f. readlines()
    for i in range(len(lines)):
        if str(list) in lines[i]:
            squashable_commit_list = lines[i]
            squashed_commit_list = lines[i+1]
            break
    countTemp = squashable_commit_list.split("squashable commit list ")[1].split("], ")
    for i in range(len(countTemp)):
        if str(list[-1]) in countTemp[i]:
            squashed_commit = squashed_commit_list.split("squashed commit list ")[1].split(",")[i]
            break
    print("squashed commit is: {}".format(squashed_commit))

if __name__ == "__main__":
    repoName = "retrolambda"
    disappearROCommitID = "281aa17f7e8a0b14d332fc903f9a0d67a0b6fd52"

    experimentResultPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"+repoName
    'Analyse disappear commit reason'
    '1. get recipe about how disappeared commit is squashed'
    squashable_commits = searchRecipe(disappearROCommitID,experimentResultPath)

    'compare git diff: recipe[0]^..recipe[-1] with commitID'

    list = sorted(squashable_commits,key = lambda x:len(x))[0]
    print(list)
    # list = ['bc99e75c2fa4b56325910e445283d1b24cb2618d', 'a4bdd6f054c3e3a119c0b8df3d8b5fde5ca5f61d']
    logFile = experimentResultPath+"/log"+str(len(list))+".txt"
    'find Squashed commit ID according to logx.txt to get the refactoring miner result'
    findAfterSquashLog(logFile,list)
