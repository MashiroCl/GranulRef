import sys
sys.path.append('../')
import time
from MyRepository import MyRepository, create_folder,delete_foler
from RefactoringMiner import RefactoringMiner
from jsonUtils import JsonUtils
from utils import outputTime,RMDetect,timeRecord


# def normal_detect(RMPath:str,repoPath:str,output:str):
#
#     '''Initialize workspace'''
#     #set Repository
#     repo = MyRepository(repoPath)
#     repo.createWorkSpace()
#
#     # create_folder(squashedOutput)
#     '''Obtain git commit info in Json form'''
#     #create a json file read json file
#     jU=JsonUtils()
#     jU.setRepoPath(repo.repoPath)
#     jU.gitJson()
#     commits=jU.jsonToCommit()
#
#     rm = RefactoringMiner(RMPath)
#
#
#     create_folder(output)
#     'RM detect commits after squash'
#     repo.setRMoutputPath(output)
#     time_start = time.time()
#     temp = []
#     for each in commits:
#         temp.append(each.commitID)
#     RMDetect(rm,temp, repo)
#     time_end = time.time()
#     t = time_end - time_start
#     tResult = outputTime(t)
#     print(tResult)
#     with open("./time.txt", "w") as f:
#         f.writelines(tResult)

def normal_detect(RMPath:str,repoPath:str,output:str):

    '''Initialize workspace'''
    #set Repository
    repo = MyRepository(repoPath)
    repo.createWorkSpace()

    repoName = repo.repoPath.split("/")[-1]
    outputPath=output+"/"+repoName
    create_folder(outputPath)

    # create_folder(squashedOutput)
    '''Obtain git commit info in Json form'''
    #create a json file read json file
    jU=JsonUtils()
    jU.setRepoPath(repo.repoPath)
    jU.gitJson()
    commits=jU.jsonToCommit()

    rm = RefactoringMiner(RMPath)
    'RM detect commits after squash'
    time_start = timeRecord()
    temp = []
    for each in commits:
        temp.append(each.commitID)
    outputJson=outputPath+"/temp"
    create_folder(outputJson)
    repo.setRMoutputPath(outputJson)
    RMDetect(rm,temp, repo)


    time_end = timeRecord()
    t = time_end - time_start
    tResult = outputTime(t)
    print(tResult)
    with open(outputPath+"/time.txt", "w") as f:
        f.writelines(tResult)

    delete_foler(outputJson)

if __name__ =="__main__":
    'server'
    # RMPath="/home/chenlei/RA/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner"
    'local'
    RMPath="/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"

    # repoPath = "/home/chenlei/RA/data/RoboBinding"
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/refactoring-toy-example"
    # repoPath = "/home/chenlei/RA/data/jbpm"
    output = repoPath+"/normal_detect"

    args=sys.argv
    repoPath=args[1]
    output=args[2]

    normal_detect(RMPath=RMPath,repoPath=repoPath,output=output)