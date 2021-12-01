"""
1.create a json file read json file
2.find cc_lists and p_lists
3.RM on current all commits (merge excluded)
4.squash
5.RM on remaining all commits (merge excluded)
"""
from jsonUtils import JsonUtils
from commitProcess.CommitGraph import CommitGraph
from MyRepository import MyRepository
from refactoringMiner.RefactoringMiner import RefactoringMiner
import os
import json
import argparse
import time

STEINLOG="./stein.log"


def RM_supported_type(RMSupportedREF):
    dict={}
    with open(RMSupportedREF) as f:
       lines=f.readlines()
    for each in lines:
        dict[each.lower().strip()]=0
    return dict

def stat_analysis(f_json,dictS):
    with open(f_json,"r") as f1:
        list1=json.load(f1)
    #ref_num, num_of_each_type
    ref_num=0
    if isinstance(list1,list):
        pass
    else:
        list1=[list1]

    for each in list1:
        if len(each["commits"])!=0:
            for each_r in each["commits"][0]["refactorings"]:
                for eachD in dictS:
                    if eachD.lower() == each_r['type'].lower():
                        ref_num = ref_num + 1
                        dictS[eachD] = dictS[eachD] + 1
    return ref_num,dictS

def dictAdd(dictS,dict2)->dict:
    '''
    add all value from dict2 to dict1
    :param dictS:
    :param dict2:
    :return:
    '''
    for each1 in dictS:
        for each2 in dict2:
            if each1.lower() == each2.lower():
                dictS[each1] += dict2[each2]
    return dictS

def dictAverage(d,num)->dict:
    for each in d:
        d[each]=d[each]/num


def dictCompare(dict1,dict2,RMSupportedREF)->list:
    dictAdd=RM_supported_type(RMSupportedREF)
    dictDecrease=RM_supported_type(RMSupportedREF)
    for each1 in dict1:
        difference=dict2[each1]-dict1[each1]
        if difference>0:
            dictAdd[each1]=difference
        if difference<0:
            dictDecrease[each1]=-1*difference
    return dictAdd,dictDecrease

def dictCount(dict)->int:
    num=0
    for each in dict:
        num+=dict[each]
    return num

def exclude_0_in_dict(dict):
    dict2={}
    for each in dict:
        if dict[each]!=0:
            dict2[each]=dict[each]
    return dict2

def squashWithRecipe(jU,repo,cc_lists_str,recipe,git_stein,squashedOutput)->str:
    'Squash'
    'Write recipe'
    jU.writeRecipe(cc_lists_str, recipe)
    'Squash according to recipe'
    repo.squashCommits(recipe, git_stein, squashedOutput, repo.repoPath)
    'Find newly generated commit No.'
    steinLog=STEINLOG
    with open(steinLog,"r") as f:
        lines=f.readlines()
    result=[]
    for eachList in cc_lists_str:
        for eachLine in lines:
            if " Rewrite commit: " in eachLine:
                temp = eachLine.split("Rewrite commit: ")[1].split(" -> ")
                'Attention: merge not excluded'
                if temp[0].strip() == eachList[0].strip():
                    result.append(temp[1].strip())
    return result
def RMDetect(rm,commits:list,repo):
    print("_____________________RM Detect commits__________________________________")
    for each in commits:
        jsonF = rm.detect(repo.repoPath, repo.RMoutputPath, each)
    print("________________________________________________________________________")
    return jsonF

def step(RMPath:str,repoPath:str,recipe:str,git_stein:str,squashedOutput:str,clusterNum:int,compareResult:str,RMSupportedREF:str):
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

    'write recipe and Squash'
    dictBeforeS=RM_supported_type(RMSupportedREF)
    dictAfterS=RM_supported_type(RMSupportedREF)
    disappearRO=RM_supported_type(RMSupportedREF)
    genereatRO=RM_supported_type(RMSupportedREF)
    commitNumBefore,commitNumAfter=0,0
    squashedCommitNum=0

    for each in cc_lists_str:
        commitNumBefore+=len(each)
        possibleSquashes,commitNumAfterSquash=cG.clusterList(each,clusterNum)
        'commitNumAfterSquash < len(each) means the squash occurs'
        if commitNumAfterSquash!=len(each):
            print("commitNumAfterSquash",commitNumAfterSquash)
            dictTemp1 = RM_supported_type(RMSupportedREF)
            dictTemp2 = RM_supported_type(RMSupportedREF)
            squashedCommitNumTemp=0
            commitNumAfter+=commitNumAfterSquash
            for possibleSquash in possibleSquashes:
                squashableCommitList=[]
                for each2 in possibleSquash:
                    if len(each2) > 1:
                        squashedCommitNumTemp += len(each2)
                        squashableCommitList.append(each2)

                'if squash output .git file is already exist, delete it to prohibit .git from becoming too big'
                if os.path.exists(squashedOutput):
                    command="rm -rf "+squashedOutput
                    os.system(command)

                afterSquashed = squashWithRecipe(jU, repo, squashableCommitList, recipe, git_stein, squashedOutput)
                repoNew = MyRepository(squashedOutput)
                repoNew.createWorkSpace()
                repoNew.addRemote(repoNew.repoPath)
                'Using git gc to pack new generated .git'
                # repoNew.gitGc(repoNew.repoPath)

                'RM detect commits after squash'
                RMDetect(rm, afterSquashed, repoNew)
                'combine detected results and combined them into a json file'
                jsonFAfter=repoNew.combine("/squashed.json")

                'RM detect commits before squash'
                'clean old RMoutput file'
                repo.createWorkSpace()
                for eachList in squashableCommitList:
                    RMDetect(rm,eachList,repo)
                jsonFBefore=repo.combine("/squashed.json")
                refNum1, dictTemp1 = stat_analysis(jsonFBefore, dictTemp1)
                refNum2, dictTemp2 = stat_analysis(jsonFAfter, dictTemp2)

            dictAverage(dictTemp1,len(possibleSquashes))
            dictAverage(dictTemp2,len(possibleSquashes))
            squashedCommitNum+=squashedCommitNumTemp/len(possibleSquashes)
            dictIncrease, dictDecrease = dictCompare(dictTemp1, dictTemp2,RMSupportedREF)
            dictAdd(genereatRO, dictIncrease)
            dictAdd(disappearRO, dictDecrease)
            dictAdd(dictBeforeS, dictTemp1)
            dictAdd(dictAfterS, dictTemp2)
        else:
            commitNumAfter+=len(each)

    #result_before="Fine grained (Merge excluded) "+str(commitNumBefore)+ " commits in total: "+"Total "+str(refNumBefore)+" detected, "+str(exclude_0_in_dict(dictBeforeS))
    result_before="Fine grained (Merge excluded) "+str(commitNumBefore)+ " commits in total: "
    result_after="Coarse-grained (Merge excluded)  "+str(commitNumAfter)+ " commits in total: "
    realSquashedCommit="Number of commits being squashed is "+str(squashedCommitNum)
    increaseRO="Number of RO generated because of squash is "+str(dictCount(genereatRO))+", they are"+str(exclude_0_in_dict(genereatRO))
    decreaseRO="Number of RO disappear because of squash is "+str(dictCount(disappearRO))+", they are"+str(exclude_0_in_dict(disappearRO))



    print(result_before)
    print(result_after)
    print(realSquashedCommit)
    print(increaseRO)
    print(decreaseRO)


    with open(compareResult,"w") as f:
        f.writelines(result_before+"\n")
        f.writelines(result_after+"\n")
        f.writelines(realSquashedCommit+"\n")
        f.writelines(increaseRO+"\n")
        f.writelines(decreaseRO+"\n")

def start():
    parser=argparse.ArgumentParser(description="squash commits and detect refactoring operations")
    parser.add_argument('RMpath',help='path for refactoring miner')
    parser.add_argument('git_stein',help='path for git-stein')
    parser.add_argument('squashedOutput',help='path for experiment output')
 #   parser.add_argument('repoPath',help='path for repository to be squashed and detected')
    parsed=parser.parse_args()
    RMPath=parsed.RMpath
    git_stein=parsed.git_stein
    squashedOutput=parsed.squashedOutput

def getConfig():
    with open("../config.json") as f:
        data=json.load(f)
    return data

def outputTime(t)->str:
    h=t // 3600
    m=(t-h*3600)//60
    s=t-h*3600-m*60
    tResult = 'time cost:  {:.0f}h {:.0f}min {:.0f}s'.format(h,m,s)
    return tResult

def timeRecord():
    return time.time()