"""
1.create a json file read json file
2.find cc_lists and p_lists
3.RM on current all commits (merge excluded)
4.squash
5.RM on remaining all commits (merge excluded)
"""
from jsonUtils import JsonUtils
from CommitGraph import CommitGraph
from CommitGraph import printCClists
from MyRepository import MyRepository
from MyRepository import create_folder
from RefactoringMiner import RefactoringMiner
import os
import json

def git_log(path,file_name="git_log.txt")->str:
    os.system('git -C '+path+'/.git log>'+path+"/"+file_name)
    return path+"/"+file_name

def extract_commit(file_path)->list:
    with open(file_path) as f1:
        lines=f1.readlines()
    commits=[]
    length=len(lines)
    for i,line in enumerate(lines):
        if "commit" in line:
            if i<length-1 and ("Merge: " in lines[i+1] or "Author: " in lines[i+1]):
                temp=line.split("commit ")[1]
                temp=temp.split("\n")[0]
                commits.append(temp)
    return commits

def count_commit(file_path):
    with open(file_path) as f:
        lines = f.readlines()
    length = len(lines)
    num=0

    # #Merge not excluded
    # for i, line in enumerate(lines):
    #     if "commit" in line:
    #         if i < length - 1 and ("Merge: " in lines[i + 1] or "Author: " in lines[i + 1]):
    #             num=num+1
    # return num

    #Merge excluded
    for i, line in enumerate(lines):
        if "commit" in line:
            if i < length - 1 and ("Author: " in lines[i + 1]):
                num=num+1
    return num

def RM_supported_type():
    RMSupportedREF = "RMSupportedREF.txt"
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
    for each1 in dictS:
        for each2 in dict2:
            if each1.lower() == each2.lower():
                dictS[each1] += dict2[each2]
    return dictS

def dictCompare(dict1,dict2)->list:
    dictAdd=RM_supported_type()
    dictDecrease=RM_supported_type()
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

# def step_discarded():
#     '''Initialize workspace'''
#     #set Repository
#     repo = MyRepository(repoPath)
#     repo.createWorkSpace()
#
#     '''Obtain git commit info in Json form'''
#     #create a json file read json file
#     jF=JsonUtils()
#     jF.setRepoPath(repo.repoPath)
#     jF.gitJson()
#     commits=jF.jsonToCommit()
#
#     #create commit graph
#     cG = CommitGraph(commits)
#     head = cG.formGraph()
#
#     #Extract cc_lists
#     cc_lists = cG.getCClist()
#     # initialCommit=cc_lists[-1][-1]
#     # print("initial commit is ",initialCommit.commitID)
#
#     # #Process cc_lists
#     # pcc_lists=cG.processCClist(cc_lists)
#     # printCClists(cc_lists)
#
#     # #parent commit used in git rebase -i
#     # p_lists=[]
#     # for each in cc_lists:
#     #     #The most initial commit
#     #     if len(each[-1].parent)==0:
#     #         p_lists.append(each[-1])
#     #         each.remove(each[-1])
#     #     else:
#     #         p_lists.append(each[-1].parent[0])
#
#     #RM on all commits before squash
#     rm=RefactoringMiner(RMPath)
#
#     ftemp=git_log(repo.repoPath)
#     commits_before=extract_commit(ftemp)
#     num_before=len(commits_before)
#
#     for each in commits_before:
#         rm.detect(repo.repoPath,repo.outputPath,each)
#     f1=repo.combine("/RM_before_squashed.json")
#
#     ref_num_before = 0
#     ref_num_after = 0
#     dict_before = RM_supported_type()
#     dict_after = RM_supported_type()
#
#     #static analysis
#     ref_num_before,dict_temp=stat_analysis(f1)
#     #sort result
#     dictAdd(dict_before,dict_temp)
#
#     '''SQUASH'''
#     # # copy auto_seq_editor.txt to the repository
#     # repo.copy_auto_seq_editor()
#     # # write cc_cluster_info with commits
#     # for i in range(len(cc_lists)):
#     #     #Bug here, why commits will disappear
#     #     #Manually do the squash in the same way and have a check
#     #     if len(cc_lists[i])>1:
#     #         ccCommits=repo.cc_cluster_info(cc_lists[i])
#     #         repo.squashCommits(p_lists[i])
#
#     # copy auto_seq_editor.txt to the repository
#     repo.copy_auto_seq_editor()
#     # write cc_cluster_info with commits
#     pcc_list_temp=[]
#     for each1 in pcc_lists:
#         for each2 in each1:
#             pcc_list_temp.append(each2)
#     repo.cc_cluster_info(pcc_list_temp)
#     repo.squashCommits(initialCommit)
#
#     '''Detect with RM after squash'''
#     #obtain commit(Merge excluded) after squash
#     f2=git_log(repo.repoPath)
#     commits2=extract_commit(f2)
#     num_after=len(commits2)
#
#     #Use RM to detect all commits after squashed(Merge excluded)
#     create_folder(repo.outputPath)
#     for each in commits2:
#         rm.detect(repo.repoPath, repo.outputPath, each)
#
#     f2=repo.combine("/RM_after_squashed.json")
#
#     #static analysis
#     ref_num_after,dict_temp2=stat_analysis(f2)
#     #sort result
#     dictAdd(dict_after,dict_temp2)
#
#     result_before="Fine grained "+str(num_before)+ " commits in total: "+"Total "+str(ref_num_before)+" detected, "+str(exclude_0_in_dict(dict_before))
#     result_after="Coarese-grained "+str(num_after)+ " commits in total: "+ "Total "+str(ref_num_after)+ " detected, "+str(exclude_0_in_dict(dict_after))
#
#     print(result_before)
#     print(result_after)
#
#     with open(CompareResult,"w") as f:
#         f.writelines(result_before+"\n")
#         f.writelines(result_after)


def step(repoPath,recipe,git_stein,squashedOutput):
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
    cc_lists_str=[]
    for each1 in cc_lists:
        temp=[]
        for each2 in each1:
            temp.append(each2.commitID)
        cc_lists_str.append(temp)

    'Squash'
    'Write recipe'
    jU.writeRecipe(cc_lists_str,recipe)
    'Squash according to recipe'
    repo.squashCommits(recipe,git_stein,squashedOutput,repo.repoPath)

    repoNew=MyRepository(squashedOutput)
    repoNew.createWorkSpace()
    repoNew.addRemote(repoNew.repoPath)
    'RM and data analysis'
    'obtain squashed commit'
    steinLog="./stein.log"
    with open(steinLog,"r") as f:
        lines=f.readlines()
    oldlists=[]
    newlists=[]

    rm = RefactoringMiner(RMPath)

    for each in lines:
        if " Rewrite commit: " in each:
            temp=each.split("Rewrite commit: ")[1].split(" -> ")
            'Attention: merge not excluded'
            oldlists.append(temp[0].strip())
            newlists.append(temp[1].strip())

    print(cc_lists_str)
    print("oldlists",oldlists)
    print("newlists",newlists)

    dictBeforeS=RM_supported_type()
    dictAfterS=RM_supported_type()
    disappearRO=RM_supported_type()
    genereatRO=RM_supported_type()

    refNumBefore=0
    refNumAfter=0

    commitNumBefore=0
    commitNumAfter=0
    for i in range(len(cc_lists_str)):
        for j in range(len(oldlists)):
            'commits in cc_lists_str[i] is squashed into newlists[j]'
            if cc_lists_str[i][0] in oldlists[j]:
                create_folder(repo.comparePath)
                create_folder(repo.RMoutputPath)
                'RM on being squashed old commit'
                print("__________________________________________________")
                for each in cc_lists_str[i]:
                    print(each)
                    rm.detect(repo.repoPath,repo.RMoutputPath,each)
                commitNumBefore +=len(cc_lists_str[i])
                commitNumAfter+=1
                jsonFBefore=repo.combine("/squashed.json")

                'RM on squashed new commit'

                jsonFAfter=rm.detect(repoNew.repoPath,repo.comparePath,newlists[j])

                'compare RO detected before and after squash for each cluster, find ROs disappear and generated'
                dictTemp1=RM_supported_type()
                dictTemp2 = RM_supported_type()
                refNum1, dictTemp1 = stat_analysis(jsonFBefore,dictTemp1)
                refNum2, dictTemp2 = stat_analysis(jsonFAfter, dictTemp2)
                dictIncrease,dictDecrease=dictCompare(dictTemp1,dictTemp2)
                dictAdd(genereatRO,dictIncrease)
                dictAdd(disappearRO,dictDecrease)
                dictAdd(dictBeforeS,dictTemp1)
                dictAdd(dictAfterS,dictTemp2)
                refNumBefore+=refNum1
                refNumAfter+=refNum2

    result_before="Fine grained (Merge excluded) "+str(commitNumBefore)+ " commits in total: "+"Total "+str(refNumBefore)+" detected, "+str(exclude_0_in_dict(dictBeforeS))
    result_after="Coarse-grained (Merge excluded)  "+str(commitNumAfter)+ " commits in total: "+ "Total "+str(refNumAfter)+ " detected, "+str(exclude_0_in_dict(dictAfterS))
    increaseRO="Number of RO generated because of squash is "+str(dictCount(genereatRO))+", they are"+str(exclude_0_in_dict(genereatRO))
    decreaseRO="Number of RO disappear because of squash is "+str(dictCount(disappearRO))+", they are"+str(exclude_0_in_dict(disappearRO))


    print(result_before)
    print(result_after)
    print(increaseRO)
    print(decreaseRO)

    with open(CompareResult,"w") as f:
        f.writelines(result_before+"\n")
        f.writelines(result_after+"\n")
        f.writelines(increaseRO+"\n")
        f.writelines(decreaseRO+"\n")

if __name__=="__main__":
    RMSupportedREF = "RMSupportedREF.txt"
    RMPath = "/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"
    CompareResult = "./CompareResult.txt"

    repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal"
    # repoPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/refactoring-toy-example"
    # repoPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/mbassador"
   #  repoPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/test/refactoring-toy-example"
   # repoPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/jeromq"

    git_stein = "/Users/leichen/Code/git-stein/build/libs/git-stein-all.jar"
    recipe="./recipe.json"
    # squashedOutput="/Users/leichen/ResearchAssistant/InteractiveRebase/data/experimentResult/mbassador"
    # squashedOutput = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/experimentResult/refactoring-toy-example"
    squashedOutput = "/Users/leichen/ResearchAssistant/InteractiveRebase/data/experimentResult/jfinal"


    CompareResult = squashedOutput+"/compareResult.txt"

    step(repoPath,recipe,git_stein,squashedOutput)



