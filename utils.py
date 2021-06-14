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

RMSupportedREF="RMSupportedREF.txt"
RMPath="/Users/leichen/ResearchAssistant/RefactoringMiner_commandline/RefactoringMiner-2.1.0/bin/RefactoringMiner"



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
    dict={}
    with open(RMSupportedREF) as f:
       lines=f.readlines()
    for each in lines:
        dict[each.strip()]=0
    return dict

def stat_analysis(f_json):
    with open(f_json,"r") as f1:
        list1=json.load(f1)
    dictS = RM_supported_type()
    #ref_num, num_of_each_type
    ref_num=0
    if isinstance(list1,list):
        pass
    else:
        list1=[list1]

    for each in list1:
        if len(each["commits"])!=0:
            for each_r in each["commits"][0]["refactorings"]:
                ref_num=ref_num+1
                for eachD in dictS:
                    if eachD.lower() == each_r['type'].lower():
                        dictS[eachD] = dictS[eachD] + 1
    return ref_num,dictS

def dictAdd(dictS,dict2)->dict:
    for each1 in dictS:
        for each2 in dict2:
            if each1.lower() == each2.lower():
                dictS[each1] += dict2[each2]
    return dictS

def exclude_0_in_dict(dict):
    dict2={}
    for each in dict:
        if dict[each]!=0:
            dict2[each]=dict[each]
    return dict2

# repoPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/jfinal"
# repoPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/refactoring-toy-example"
repoPath="/Users/leichen/ResearchAssistant/InteractiveRebase/data/test/refactoring-toy-example"
if __name__=="__main__":
    #set Repository
    repo = MyRepository(repoPath)
    repo.createWorkSpace()

    #create a json file read json file
    jF=JsonUtils()
    jF.setRepoPath(repoPath)
    jF.createJson()
    commits=jF.jsonToCommit()

    #create commit graph
    cG = CommitGraph(commits)
    head = cG.formGraph()

    #Extract cc_lists
    cc_lists = cG.getCClist()
    printCClists(cc_lists)

    #parent commit used in git rebase -i
    p_lists=[]
    for each in cc_lists:
        #The most initial commit
        if len(each[-1].parent)==0:
            p_lists.append(each[-1])
            each.remove(each[-1])
        else:
            p_lists.append(each[-1].parent[0])

    num_before=len(commits)

    #RM on all commits in cc_lists
    rm=RefactoringMiner(RMPath)

    for each1 in cc_lists:
        for each2 in each1:
             rm.detect(repo.repoPath,repo.outputPath,each2.commitID)
    f1=repo.combine("/RM_before_squashed.json")

    ref_num_before = 0
    ref_num_after = 0
    dict_before = RM_supported_type()
    dict_after = RM_supported_type()

    #static analysis
    ref_num_before,dict_temp=stat_analysis(f1)
    #sort result
    dictAdd(dict_before,dict_temp)

    '''SQUASH'''
    # copy auto_seq_editor.txt to the repository
    repo.copy_auto_seq_editor()
    # write cc_cluster_info with commits
    for i in range(0,2):
        ccCommits=repo.cc_cluster_info(cc_lists[i])
        repo.squashCommits(p_lists[i])

    #obtain commit(Merge excluded) after squash
    f2=git_log(repo.repoPath)
    commits2=extract_commit(f2)
    num_after=len(commits2)

    #Use RM to detect all commits after squashed(Merge excluded)
    create_folder(repo.outputPath)
    for each in commits2:
        rm.detect(repo.repoPath, repo.outputPath, each)

    f2=repo.combine("/RM_after_squashed.json")

    #static analysis
    ref_num_after,dict_temp2=stat_analysis(f2)
    #sort result
    dictAdd(dict_after,dict_temp2)

    print("Fine grained", num_before, "commits in total: ", "Total ", ref_num_before, " detected, ",
          exclude_0_in_dict(dict_before))
    print("Coarese-grained", num_after, "commits in total: ", "Total ", ref_num_after, " detected, ",
          exclude_0_in_dict(dict_after))




