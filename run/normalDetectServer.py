import sys
sys.path.append('../')

from MyRepository import MyRepository, create_folder
from RefactoringMiner import RefactoringMiner
from jsonUtils import JsonUtils
from utils import outputTime,RMDetect,timeRecord


def normal_detect(RMPath:str,repoPath:str,output:str):

    '''Initialize workspace'''
    #set Repository
    repo = MyRepository(repoPath)
    repo.createWorkSpace()

    # create_folder(squashedOutput)
    '''Obtain git commit info in Json form'''
    #create a json file read json file
    jU=JsonUtils()
    jU.setRepoPath(repo.repoPath)
    jU.gitJson()
    commits=jU.jsonToCommit()

    rm = RefactoringMiner(RMPath)


    create_folder(output)
    'RM detect commits after squash'
    repo.setRMoutputPath(output)
    time_start = timeRecord()
    temp = []
    for each in commits:
        temp.append(each.commitID)
    RMDetect(rm,temp, repo)

    time_end = timeRecord()
    t = time_end - time_start
    tResult = outputTime(t)
    print(tResult)
    with open(output+"./time.txt", "w") as f:
        f.writelines(tResult)

if __name__ =="__main__":
    'server'
    RMPath="/home/chenlei/RA/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner"

    args=sys.argv
    repoPath=args[1]
    output=args[2]
    normal_detect(RMPath=RMPath,repoPath=repoPath,output=output)