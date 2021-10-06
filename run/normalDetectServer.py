import sys
sys.path.append('../')

from MyRepository import MyRepository, create_folder,delete_foler
from refactoringMiner.RefactoringMiner import RefactoringMiner
from jsonUtils import JsonUtils
from utils import outputTime,RMDetect,timeRecord


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
    RMPath="/home/chenlei/RA/RefactoringMiner/build/distributions/RefactoringMiner-2.1.0/bin/RefactoringMiner"

    args=sys.argv
    repoPath=args[1]
    output=args[2]
    normal_detect(RMPath=RMPath,repoPath=repoPath,output=output)