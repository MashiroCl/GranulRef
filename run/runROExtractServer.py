import sys
sys.path.append('../')
from repository import create_folder
from logger import logger_config
from utils import getConfig, outputTime
import time,os


from ROExtract.extractRO import extractRO


def runServer(repoPath, squashedOutput,outputRepoDirectory, clusterNum):
    data = getConfig()
    RMPath = data["titan"]["RMPath"]
    git_stein = data["titan"]["git_stein"]


    repoName = repoPath.split("/")[-1]

    outputRepoDirectory = os.path.join(outputRepoDirectory, repoName)
    create_folder(outputRepoDirectory)
    recipe = os.path.join(outputRepoDirectory, "recipe.json")
    squashedOutput = os.path.join(squashedOutput, repoName)

    for num in range(clusterNum[0], clusterNum[1]):
        jsonOutputDirectory = os.path.join(outputRepoDirectory, str(num))
        create_folder(jsonOutputDirectory)
        logger = logger_config(log_path=outputRepoDirectory + '/log' + str(num) + '.txt',
                               logging_name=repoName + " " + str(num) + "by" + str(num))

        logger.info("start squash " + str(num) + "by" + str(num))
        extractRO(RMPath=RMPath,
                  repoPath=repoPath,
                  recipe=recipe, git_stein=git_stein,
                  squashedOutput=squashedOutput,
                  clusterNum=num, jsonOutputDirectory=jsonOutputDirectory, logger=logger,
                  steinOuput=outputRepoDirectory)
        logger.info("finish squash " + str(num) + "by" + str(num))

    os.system("rm -rf " + squashedOutput)

if __name__ == "__main__":
    clusterNum = [1, 5]
    rootPath = "/home/chenlei/RA/data/"
    args = sys.argv
    repoNameTemp = args[1]
    repoName = [repoNameTemp]
    outputRepoDirectory = "/home/chenlei/RA/setversion/experimentResult/"
    output = "/home/chenlei/RA/setversion/gitOutput"


    for each in repoName:
        time_start = time.time()
        repoPath = rootPath + each
        runServer(repoPath, output,outputRepoDirectory,clusterNum)

        time_end = time.time()
        t = time_end - time_start
        tResult = outputTime(t)
        with open((outputRepoDirectory+each+"/time.txt"),"w") as f:
            f.write(tResult)