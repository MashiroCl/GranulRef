import sys
sys.path.append('../')
from RefactoringOperation.RMcommit import RMcommit
import os

def containsRO(ROtype,dict1):
    if dict1.get(ROtype,0) >0:
        return True
    return False

def get_commit_id_from_log(log_path):
    with open(log_path) as f:
        lines = f.readlines()
    squasable_commit_lists = list()
    squashed_commit_lists = list()
    for line in lines:
        if "squashable commit list" in line:
            squasable_commit_lists.append(eval(line.split("squashable commit list ")[1]))
        if "squashed commit list" in line:
            squashed_commit_lists.append(eval(line.split("squashed commit list ")[1]))
    return squasable_commit_lists, squashed_commit_lists

def get_ROType(commit, experimentResultPath, squashNum):
    RTdict = dict()
    if isinstance(commit,list):
        for each in commit:
            path = os.path.join(experimentResultPath,str(squashNum),str(each)+".json")
            rMcommit = RMcommit(path)
            for ro in rMcommit.refactorings:
                RTdict[ro.type] = RTdict.get(ro.type, 0) + 1
    elif isinstance(commit,str):
        path = os.path.join(experimentResultPath, str(squashNum), commit+".json")
        rMcommit = RMcommit(path)
        for ro in rMcommit.refactorings:
            RTdict[ro.type] = RTdict.get(ro.type, 0) + 1
    else:
        print("ERROR: commit input not correct")

    return RTdict

def dict_minus(dict1,dict2):
    for each in dict2:
        dict1[each] = dict1.get(each,0) - dict2[each]
    return dict1

def dict_add(dict1, dict2):
    for each in dict2:
        dict1[each] = dict1.get(each,0) + dict2[each]
    return dict1

def dict_add_ignore_negative(dict1, dict2):
    for each in dict2:
        if dict2[each]<0:
            continue
        dict1[each] = dict1.get(each,0) + dict2[each]

def isEffectiveSquash(dict1):
    for each in dict1:
        if dict1[each] >0:
            return True
    return False

def compare_before_after_squash(squashable_commit_lists, squashed_commit_lists, experimentResultPath):
    sum_before_squash_ROtype_Dict = dict()
    sum_after_squash_ROtype_Dict = dict()
    generate_ROtype = dict()
    'a effective squash means squash generates new type of RO'
    effectiveSquash = 0
    squashNum = 0
    'according to logx.txt'
    'find before squash commit ID'
    'find after squash commit ID'
    'compare result type'
    'next squash'
    for i in range(len(squashable_commit_lists)):
        for j in range(len(squashable_commit_lists[i])):
            squashNum += 1
            before_squash_ROtype_Dict = get_ROType(squashable_commit_lists[i][j], experimentResultPath,1)
            after_squash_ROtype_Dict = get_ROType(squashed_commit_lists[i][j], experimentResultPath,len(squashable_commit_lists[i][j]))
            ROtype_difference = dict_minus(after_squash_ROtype_Dict, before_squash_ROtype_Dict)
            if isEffectiveSquash(ROtype_difference):
                effectiveSquash += 1
                if containsRO('Move And Rename Class',ROtype_difference):
                    print(squashable_commit_lists[i][j])
                    print(squashed_commit_lists[i][j])
                # print(sorted(ROtype_difference.items(), key=lambda x: x[1], reverse=True))
            generate_ROtype = dict_add(generate_ROtype,ROtype_difference)

    print("Effective squash ratio: {}, effective squash num: {}, squash num: {}".format(effectiveSquash/squashNum,effectiveSquash,squashNum))
    return generate_ROtype



if __name__ == "__main__":
    repoNames = ["retrolambda"]

    experimentResultPath = "/Users/leichen/ResearchAssistant/InteractiveRebase/experimentResult/"
    for repoName in repoNames:
        repoPath = os.path.join(experimentResultPath,repoName)
        squasable_commit_lists, squashed_commit_lists = get_commit_id_from_log(repoPath+"/log4.txt")
        generate_ROtype = compare_before_after_squash(squasable_commit_lists, squashed_commit_lists, repoPath)
        generate_ROtype = sorted(generate_ROtype.items(),key=lambda x:x[1],reverse=True)
        print(generate_ROtype)