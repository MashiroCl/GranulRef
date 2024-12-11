'''
extract commits, squash commits and detect refactoring operations on both fine-grained and coarse-grained commits
'''
import json
from jsonUtils import JsonUtils
from commitProcess.CommitGraph import CommitGraph
from repository import Repository, create_folder
from refactoring_mining.miner import RefactoringMiner, RefDiff, remove_redundant_git_files
import os

from utils import squashWithRecipe, getConfig
from multiprocessing import Process


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


def list3dto2d(l: list[list[list[str]]]) -> list[list[str]]:
    res = []
    for each in l:
        res += each
    return res


def get_recipe_candidates(sc_possible_squashes: list[list[list[list[str]]]], cluster_num: int) -> list[
    list[list[list[str]]]]:
    """
    from the straight commit sequence generate the list of squash units list under different offset
    :param sc_possible_squashes:
    :param cluster_num:
    :return:
    """
    candidates = []
    for offset in range(cluster_num):
        # extract the squashable sequence for each offset from the straight commit sequences
        offset_candidate = []
        for sc_possible_squash in sc_possible_squashes:
            if len(sc_possible_squash) > offset:
                offset_candidate.append(
                    [squash_l for squash_l in sc_possible_squash[offset] if len(squash_l) == cluster_num])
        candidates.append(offset_candidate)
    return candidates


def extractRO(RMPath: str, repoPath: str, recipe: str, git_stein: str, squashedOutput: str, clusterNum: int,
              jsonOutputDirectory: str, logger, stein_output):
    '''
    extract commits, squash commits and detect refactoring operations on both fine-grained and coarse-grained commits
    :param jsonOutputDirectory:
    :param RMPath: path for refactoring miner
    :param repoPath: path for repo being squashed
    :param recipe: path for recipe
    :param git_stein: path for git-stin
    :param squashedOutput: path for squashed repository output
    :param clusterNum: number of each cluster
    :param jsonOutputDirectory:
    :param logger: logger
    :param stein_output:
    :return:
    '''
    '''Initialize workspace'''
    # set Repository
    repo = set_repository(repoPath)

    '''extract commits from repository'''
    commits = extract_commits(repo)

    logger.info(f"Number of commits to be processed: {len(commits)}")

    # create commit graph
    cG = CommitGraph(commits)
    head = cG.buildGraph()

    # Extract sc_lists
    sc_lists = cG.getSClist()
    sc_lists_str = cG.getSCListStr(sc_lists)

    logger.info(f"Straight commit sequences: {sc_lists_str}")
    logger.info(f"Number of straight sequences: {len(sc_lists)}")
    logger.info(f"Number of commits involved in straight sequences: {sum([len(i) for i in sc_lists])}")

    # get RefactoringMiner entity
    rm = RefactoringMiner(RMPath)
    # rm = RefDiff(RMPath)

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
        RMDetectWithOutput_multiprocess(rm, origin_commits, repo, jsonOutputDirectory)
        remove_redundant_git_files(os.path.dirname(repo.repoPath))

        # RMDetectWithOutput(rm, origin_commits, repo, jsonOutputDirectory)
    else:
        sc_possible_squashes = []

        for each in sc_lists_str:
            commitNumBefore += len(each)

            # According to cluster num (x) to divide a sequence of commits into 'squash x by x' form
            # For a length 5 sequence commit, squash 2 by 2 has 2 possible squashe ways (offset=0 and offset=1),{{1,2}{3,4},{5} & {{1}{2,3}{4,5}}}
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
        logger.info(f"Candidates are : {candidates}")

        coarse_normal_commit_map = {}
        for bias_candidate in candidates:
            squash_units = list3dto2d(bias_candidate)
            if len(squash_units) == 0:
                break
            logger.info(f"squash units list {squash_units}")
            logger.info(f"Number of squash units list {len(squash_units)}")
            logger.info(f"Number of commits involved in squash units list {sum(len(each) for each in squash_units)}")


            # if squash output .git file is already exist, delete it to prohibit .git from becoming too big
            remove_file(squashedOutput)

            afterSquashed = squashWithRecipe(repo, squash_units, recipe, git_stein, squashedOutput, stein_output, coarse_normal_commit_map)

            logger.info("coarse-grained commit list %s" % afterSquashed)

            repoNew = set_repository(squashedOutput)
            repoNew.addRemote(repoNew.repoPath)

            'RM detect commits after squash'
            # RMDetectWithOutput(rm, afterSquashed, repoNew, jsonOutputDirectory)
            RMDetectWithOutput_multiprocess(rm, afterSquashed, repoNew, jsonOutputDirectory)
    with open(stein_output+"/coarse_normal_commit_map.json", "w") as f:
        json.dump(coarse_normal_commit_map, f)
    # RefDiff will generate .git-xxx folders, remove them if exist
    remove_redundant_git_files(os.path.dirname(jsonOutputDirectory))

def RMDetectWithOutput(rm, commits: list, repo, output: str):
    '''
    detect refactorings with RM for a list of commits
    :param rm: RefactoringMiner entity
    :param commits: straight commit sequences
    :param repo: Repository entity
    :param output:
    :return:
    '''
    for each in commits:
        rm.detect(repo.repoPath, output, each)


def RMDetectWithOutput_multiprocess(rm, commits: list, repo, output: str):
    """
    Detect Refs with multi process
    :param rm:
    :param commits:
    :param repo:
    :param output:
    :return:
    """
    process_num = int(os.cpu_count()/4*3)
    step = int(len(commits) / process_num)+1
    processes = []
    for i in range(0, len(commits), step):
        processes.append(Process(target=RMDetectWithOutput, args=(
            rm, commits[i:i+step], repo, output)))
    for p in processes:
        p.start()
    for p in processes:
        p.join()
