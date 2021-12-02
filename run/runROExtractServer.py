import sys
sys.path.append('../')
from MyRepository import create_folder
from myLog import logger_config
from utils import getConfig, outputTime
import time


from ROExtract.extractRO import extractRO


def runServer(repoPath, squashedOutput,outputRepoDirectory, clusterNum):
    data = getConfig()
    RMPath = data["titan"]["RMPath"]
    git_stein = data["titan"]["git_stein"]
    recipe = data["titan"]["recipe"]

    repoName = repoPath.split("/")[-1]

    outputRepoDirectory = outputRepoDirectory + "/" + repoName
    create_folder(outputRepoDirectory)

    for num in range(clusterNum[0], clusterNum[1]):
        jsonOutputDirectory = outputRepoDirectory + "/" + str(num)
        create_folder(jsonOutputDirectory)
        logger = logger_config(log_path=outputRepoDirectory + '/log' + str(num) + '.txt',
                               logging_name=repoName + " " + str(num) + "by" + str(num))

        logger.info("start squash " + str(num) + "by" + str(num))
        extractRO(RMPath=RMPath,
                  repoPath=repoPath,
                  recipe=recipe, git_stein=git_stein,
                  squashedOutput=squashedOutput,
                  clusterNum=num, jsonOutputDirectory=jsonOutputDirectory, logger=logger)
        logger.info("finish squash " + str(num) + "by" + str(num))


if __name__ == "__main__":
    clusterNum = [1, 5]
    rootPath = "/home/chenlei/RA/data/"
    repoName = ["refactoring-toy-example"]
    outputRepoDirectory = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"
    output = "/Users/leichen/Desktop/RTEnew"


    for each in repoName:
        time_start = time.time()
        repoPath = rootPath + each
        runServer(repoPath, output,outputRepoDirectory,clusterNum)

        time_end = time.time()
        t = time_end - time_start
        tResult = outputTime(t)
        with open((outputRepoDirectory+each+"/time.txt"),"w") as f:
            f.write(tResult)