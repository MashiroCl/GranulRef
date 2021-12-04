from MyRepository import MyRepository
from commitProcess.CommitGraph import CommitGraph
from jsonUtils import JsonUtils
from refactoringMiner.RefactoringMiner import RefactoringMiner
from utils import RM_supported_type, RMDetect, stat_analysis, getConfig


def extractRO(repoPath:str,RMPath:str,RMSupportedREF:str,output:str):
    '''
    Extract refactoring operations from all commits contained in file
    :param
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

    dictRO = RM_supported_type(RMSupportedREF)


    for each in cc_lists_str:
        RMDetect(rm,each,repo)
    jsonFBefore = repo.combine("/squashed.json")
    refNum, dictRO = stat_analysis(jsonFBefore, dictRO)

    with open(output+"/RefactoringOperation.txt","w") as f:
        f.write(str(dictRO))
    with open(output+"/number.txt","w") as f:
        f.write(str(refNum))
    print(refNum,dictRO)

if __name__ =="__main__":
    data = getConfig()
    RMSupportedREF = data["local"]["RMSupportedREF"]
    RMPath = data["local"]["RMPath"]
    temp = "RoboBinding"
    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/" + temp
    output = "/Users/leichen/Code/pythonProject/pythonProject/pythonProject" \
             "/SCRMDetection/DataAnalysis/data/"+temp+"All"
    extractRO(repoPath,RMPath,RMSupportedREF,output)