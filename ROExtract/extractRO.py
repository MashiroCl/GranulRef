'''
extract commits, squash commits and detect refactoring operations on both fine-grained and coarse-grained commits
'''

from jsonUtils import JsonUtils
from commitProcess.CommitGraph import CommitGraph
from repository import Repository, create_folder
from refactoring_mining.miner import RefactoringMiner
import os
from logger import logger_config

from utils import squashWithRecipe, getConfig
from typing import List


def set_repository(repoPath: str):
    '''
    create folder /RMoutput and /compare under target repository path
    :param reopPath: target repository path
    :return: repo:Repository
    '''
    repo = Repository(repoPath)
    # repo.createWorkSpace()
    return repo


def extract_commits(repo: Repository):
    '''
    extract commit:Commit from repository
    :param repo: 
    :return: commits:List[Commit]
    '''
    jU = JsonUtils()
    jU.setRepoPath(repo.repoPath)
    jU.gitJson()
    return jU.jsonToCommit()


def remove_file(path):
    '''
    remove file of path
    :return:
    '''
    if os.path.exists(path):
        command = "rm -rf " + path
        os.system(command)


def list3dto2d(l: List[List[List[str]]]) -> List[List[str]]:
    res = []
    for each in l:
        res += each
    return res


def get_recipe_candidates(sc_possible_squashes: List[List[List[List[str]]]], cluster_num: int) -> List[
    List[List[List[str]]]]:
    candidates = []
    for bias in range(cluster_num):
        # extract the squashable sequence for each bias from the straight commit sequences
        bias_candidate = []
        for sc_possible_squash in sc_possible_squashes:
            if len(sc_possible_squash) > bias:
                bias_candidate.append(
                    [squash_l for squash_l in sc_possible_squash[bias] if len(squash_l) == cluster_num])
        candidates.append(bias_candidate)
    return candidates


def extractRO(RMPath: str, repoPath: str, recipe: str, git_stein: str, squashedOutput: str, clusterNum: int,
              jsonOutputDirectory: str, logger, steinOuput):
    '''
    extract commits, squash commits and detect refactoring operations on both fine-grained and coarse-grained commits
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
    # set Repository
    repo = set_repository(repoPath)

    '''extract commits from repository'''
    commits = extract_commits(repo)

    # create commit graph
    cG = CommitGraph(commits)
    head = cG.buildGraph()

    # Extract sc_lists
    sc_lists = cG.getSClist()
    sc_lists_str = cG.getSCListStr(sc_lists)

    # get RefactoringMiner entity
    rm = RefactoringMiner(RMPath)

    commitNumBefore, commitNumAfter = 0, 0

    create_folder(jsonOutputDirectory)

    if clusterNum == 1:
        # no squash needed, detect refactoring operations in origin commits
        origin_commits = list()
        for each1 in sc_lists_str:
            if len(each1) == 1:
                # the commits between two merges has no possibility to be squashed, so they needn't to be considered
                continue
            for eachCommit in each1:
                origin_commits.append(eachCommit)
        'RM detect commits without squash'
        RMDetectWithOutput(rm, origin_commits, repo, jsonOutputDirectory)
    else:
        sc_possible_squashes = []
        for each in sc_lists_str:
            commitNumBefore += len(each)

            # According to cluster num (x) to divide a sequence of commits into 'squash x by x' form
            # For a length 5 sequence commit, squash 2 by 2 has 2 possible squashe way,{{1,2}{3,4},{5} & {{1}{2,3}{4,5}}}
            # possibleSquashes are 3d lists
            possibleSquashes, commitNumAfterSquash = cG.clusterList(each, clusterNum)

            if commitNumAfterSquash == len(each):
                # no squash occurs
                commitNumAfter += len(each)
            else:
                # commitNumAfterSquash < len(each) means squash occurs
                commitNumAfter += commitNumAfterSquash
                sc_possible_squashes.append(possibleSquashes)

        candidates = get_recipe_candidates(sc_possible_squashes, clusterNum)

        for bias_candidate in candidates:
            squash_units = list3dto2d(bias_candidate)
            if len(squash_units) == 0:
                break
            logger.info(f"squash units list {squash_units}")

            # if squash output .git file is already exist, delete it to prohibit .git from becoming too big
            remove_file(squashedOutput)

            afterSquashed = squashWithRecipe(repo, squash_units, recipe, git_stein, squashedOutput, steinOuput)

            logger.info("coarse-grained commit list %s" % afterSquashed)

            repoNew = set_repository(squashedOutput)
            repoNew.addRemote(repoNew.repoPath)

            'RM detect commits after squash'
            RMDetectWithOutput(rm, afterSquashed, repoNew, jsonOutputDirectory)


if __name__ == "__main__":
    data = getConfig()
    RMSupportedREF = data["local"]["RMSupportedREF"]
    RMPath = data["local"]["RMPath"]
    git_stein = data["local"]["git_stein"]
    recipe = data["local"]["recipe"]

    clusterNum = [1, 5]

    temp = "refactoring-toy-example"
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + temp
    squashedOutput = "/Users/leichen/Desktop/RTEnew"

    outputRepoDirectory = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/" + temp
    create_folder(outputRepoDirectory)

    for num in range(clusterNum[0], clusterNum[1]):
        jsonOutputDirectory = outputRepoDirectory + "/" + str(num)
        create_folder(jsonOutputDirectory)
        logger = logger_config(log_path=outputRepoDirectory + '/log' + str(num) + '.txt',
                               logging_name=temp + " " + str(num) + "by" + str(num))

        logger.info("start squash " + str(num) + "by" + str(num))
        extractRO(RMPath=RMPath,
                  repoPath=repoPath,
                  recipe=recipe, git_stein=git_stein,
                  squashedOutput=squashedOutput,
                  clusterNum=num, jsonOutputDirectory=jsonOutputDirectory, logger=logger,
                  steinOuput=outputRepoDirectory)
        logger.info("finish squash " + str(num) + "by" + str(num))


def RMDetectWithOutput(rm, commits: list, repo, output: str):
    '''

    :param rm: RefactoringMiner entity
    :param commits: straight commit sequences
    :param repo: Repository entity
    :param output:
    :return:
    '''
    for each in commits:
        rm.detect(repo.repoPath, output, each)
