from jsonUtils import JsonUtils
from commitProcess.CommitGraph import CommitGraph
from MyRepository import MyRepository, create_folder
from refactoringMiner.RefactoringMiner import RefactoringMiner
import os
from myLog import logger_config

from utils import squashWithRecipe, RMDetectWithOutput, getConfig

def extractRO(RMPath:str,repoPath:str,recipe:str,git_stein:str,squashedOutput:str,clusterNum:int,jsonOutputDirectory:str,logger):
    '''
    :param RMPath: path for refactoring miner
    :param repoPath: path for repo being squashed
    :param recipe: path for recipe
    :param git_stein: path for git-stin
    :param squashedOutput: path for squashed repository output
    :param clusterNum: number of each cluster
    :param compareResult: path for txt file storing compare result
    :param RMSupportedREF: path for RMSupportedREF.txt
    :return:
    '''

    '''Initialize workspace'''
    #set Repository
    repo = MyRepository(repoPath)
    repo.createWorkSpace()

    '''Obtain git commit info in Json form'''
    #create a json file read json file
    jU=JsonUtils()
    jU.setRepoPath(repo.repoPath)
    jU.gitJson()
    commits=jU.jsonToCommit()

    #create commit graph
    cG = CommitGraph(commits)
    head = cG.formGraph()

    #Extract cc_lists
    cc_lists = cG.getCClist()
    cc_lists_str=cG.getCCListStr(cc_lists)


    rm = RefactoringMiner(RMPath)

    commitNumBefore,commitNumAfter=0,0
    squashedCommitNum=0

    create_folder(jsonOutputDirectory)
    for each in cc_lists_str:
        commitNumBefore+=len(each)
        "According to cluster num (x) to divide a sequence of commits into 'squash x by x' form"
        "For a length 5 sequence commit, squash 2 by 2 has 2 possible squashe way,{{1,2}{3,4},{5} & {{1}{2,3}{4,5}}}"
        'possibleSquashes are 3d lists'
        possibleSquashes,commitNumAfterSquash=cG.clusterList(each,clusterNum)
        'commitNumAfterSquash < len(each) means the squash occurs'
        if commitNumAfterSquash!=len(each):
            squashedCommitNumTemp=0
            commitNumAfter+=commitNumAfterSquash
            'For each possible squash way, if length of squashableCandidate(1d list) bigger than 1,' \
            'it will be added into squashableCommitList (2d list) '
            for possibleSquash in possibleSquashes:
                squashableCommitList=[]
                for squashableCandidate in possibleSquash:
                    if len(squashableCandidate) > 1:
                        squashedCommitNumTemp += len(squashableCandidate)
                        squashableCommitList.append(squashableCandidate)

                'if squash output .git file is already exist, delete it to prohibit .git from becoming too big'
                if os.path.exists(squashedOutput):
                    command="rm -rf "+squashedOutput
                    os.system(command)

                logger.info("squashable commit list %s"%squashableCommitList)

                afterSquashed = squashWithRecipe(jU, repo, squashableCommitList, recipe, git_stein, squashedOutput)

                logger.info("squashed commit list %s" % afterSquashed)

                repoNew = MyRepository(squashedOutput)
                repoNew.createWorkSpace()
                repoNew.addRemote(repoNew.repoPath)

                'RM detect commits after squash'
                RMDetectWithOutput(rm, afterSquashed, repoNew,jsonOutputDirectory)

        else:
            commitNumAfter+=len(each)

if __name__ =="__main__":
    data = getConfig()
    RMSupportedREF = data["local"]["RMSupportedREF"]
    RMPath = data["local"]["RMPath"]
    git_stein = data["local"]["git_stein"]
    recipe = data["local"]["recipe"]

    clusterNum = [2, 5]

    temp="refactoring-toy-example"
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + temp
    squashedOutput = "/Users/leichen/Desktop/RTEnew"

    outputRepoDirectory = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/" + temp
    create_folder(outputRepoDirectory)

    for num in range(clusterNum[0], clusterNum[1]):
        jsonOutputDirectory =outputRepoDirectory+ "/" + str(num)
        create_folder(jsonOutputDirectory)
        logger = logger_config(log_path=outputRepoDirectory+'/log'+str(num)+'.txt', logging_name=temp+" "+str(num)+"by"+str(num))

        logger.info("start squash " +str(num)+"by"+str(num))
        extractRO(RMPath=RMPath,
             repoPath=repoPath,
             recipe=recipe, git_stein=git_stein,
             squashedOutput=squashedOutput,
             clusterNum=num,jsonOutputDirectory=jsonOutputDirectory,logger=logger)
        logger.info("finish squash " + str(num) + "by" + str(num))