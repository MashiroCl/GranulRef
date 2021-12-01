from jsonUtils import JsonUtils
from commitProcess.CommitGraph import CommitGraph
from MyRepository import MyRepository
from refactoringMiner.RefactoringMiner import RefactoringMiner
import os
import json
import argparse
import time


def extractCCList(repoPath:str):
    '''
    extract refactoring operations through git commit of repository
    :param repoPath: file path for repository
    :return: json file directory
    '''

    '''Initialize workspace'''
    #set Repository
    repo = MyRepository(repoPath)
    repo.createWorkSpace()

    '''Obtain git commit info in Json form'''
    jU=JsonUtils()
    jU.setRepoPath(repo.repoPath)
    jU.gitJson()

    '''json form to Commit'''
    commits=jU.jsonToCommit()

    #create commit graph
    cG = CommitGraph(commits)
    cG.formGraph()

    #Extract cc_lists
    cc_lists = cG.getCClist()
    cc_lists_str=cG.getCCListStr(cc_lists)

    return cc_lists_str,repo

def clusterCCList(clusterNum:int,cclist:list):
    '''
    cluster cclist according to squashNum
    :param clusterNum: int, number of commits being clustered
    :param cclist: being squashed commit list
    :return: clustered commit list
    '''