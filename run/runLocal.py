import time
from utils2 import step
from utils import outputTime
def runLocal():
    RMSupportedREF = "../RMSupportedREF.txt"
    RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"

    temp = "refactoring-toy-example"
    temp="mbassador"
    # temp="spring-boot"
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/"+temp
    git_stein = "/Users/leichen/Code/git-stein/build/libs/git-stein-all.jar"
    # git_stein = "/home/chenlei/RA/git-stein/build/libs/git-stein-all.jar"
    recipe = "./recipe.json"
    squashedOutput = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/experimentResult/"+temp


    time_start = time.time()
    for clusterNum in range(2, 3):
        miaomiao = squashedOutput
        miaomiao += str(clusterNum)
        CompareResult = miaomiao + "/compareResult.txt"
        step(RMPath=RMPath,repoPath=repoPath, recipe=recipe, git_stein=git_stein, squashedOutput=miaomiao, clusterNum=clusterNum,
             compareResult=CompareResult,RMSupportedREF=RMSupportedREF)

    time_end = time.time()
    t = time_end - time_start
    tResult = outputTime(t)
    print(tResult)
    with open("./time.txt", "w") as f:
        f.writelines(tResult)

if __name__ =="__main__":
    runLocal()