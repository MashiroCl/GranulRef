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

    for each in result:
        print(each)

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

def refactoringMining():
    pass

def squashAndGetAfterSquashId(repoName,commitID):
    output = "/Users/leichen/Desktop/RTEnew/test"
    if os.path.exists(output):
        command = "rm -rf " + output
        os.system(command)
    stein_output = "."
    git_stein = "/Users/leichen/Code/git-stein/build/libs/git-stein-all.jar"
    recipe = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/run/recipe.json"
    repository = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + repoName

    list = ['12b11bf39cb4800e3fa57fb1112c5fbda26de3df', 'b2c7be7001d4833d14d7fee8c7c989279b4ad039']
    writeRecipe(list, recipe)
    # squash(recipe,git_stein,output,repository,stein_output)
    squash(recipe=recipe, git_stein=git_stein, output=output, repository=repository, steinOutput=stein_output)
    afterSquash = findAfterSquash(
        "/Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/DataAnalysis/stein.log", commitID)
    print("Before squash {}\nAfter squash {}".format(list, afterSquash))

if __name__ == "__main__":
    repoName = "retrolambda"
    commitID = "7aec89a28410bf3f981069eb3d89fad4354000a0"

    experimentResultPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"+repoName
    'Analyse disappear commit reason'
    '1. get recipe about how disappeared commit is squashed'
    # searchRecipe(commitID,experimentResultPath)

    '2.squash according to the recipe and get after squashed commit id'
    squashAndGetAfterSquashId(repoName, commitID)