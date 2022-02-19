import glob
import json
import csv
from RefactoringOperation.RefactoringOperation import RefactoringOperation
from RefactoringOperation.RMcommit import RMcommit
import os

def fine_grained_line(refactoring, repository_name, commit_id):
    a_line = list()
    a_line.append(repository_name)
    a_line.append(commit_id)
    a_line.append(refactoring["type"])
    a_line.append(refactoring["description"])
    a_line.append(refactoring["leftSideLocations"])
    a_line.append(refactoring["rightSideLocations"])
    return a_line

def coarse_grained_line(refactoring, repository_name,fine_commit_ids):
    a_line = list()
    a_line.append(repository_name)
    a_line.append(fine_commit_ids)
    a_line.append(refactoring["type"])
    a_line.append(refactoring["description"])
    a_line.append(refactoring["leftSideLocations"])
    a_line.append(refactoring["rightSideLocations"])
    return a_line

def load_json(file_path):
    # print(file_path)
    with open(file_path) as f:
        data = f.read()
    data = data.replace("\'", " ")
    return json.loads(data)

def write_2_csv(path, head,info):
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(head)
        for each in info:
            writer.writerow(each)

def get_b_a_commit_dict(log_path):
    res = dict()
    with open(log_path) as f:
        lines = f.readlines()
    squashable_commit_lists = list()
    squashed_commit_lists = list()
    for line in lines:
        if "squashable commit list" in line:
            squashable_commit_lists.append(eval(line.split("squashable commit list ")[1]))
        if "squashed commit list" in line:
            squashed_commit_lists.append(eval(line.split("squashed commit list ")[1]))
    for i in range(len(squashed_commit_lists)):
        for j in range(len(squashed_commit_lists[i])):
            res[squashed_commit_lists[i][j]] = squashable_commit_lists[i][j]
    return res

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

def isEffectiveSquash(dict1):
    for each in dict1:
        'Move Source Folder cannot be used to judge if a squash is effective or not'
        if each == "Move Source Folder":
            continue
        if dict1[each] >0:
            return True
    return False

def is_effective(squashed_commit, squashable_commits, experiment_result_path):
    squashed_ro_type = get_ROType(squashed_commit, experiment_result_path, len(squashable_commits))
    squashable_ro_type = get_ROType(squashable_commits, experiment_result_path, 1)
    # print(squashed_ro_type)
    # print(squashable_ro_type)
    ro_type_difference = dict_minus(squashable_ro_type,squashed_ro_type)

    # print(ro_type_difference)
    return isEffectiveSquash(ro_type_difference)

def fine_grained_process(repo, root_path, csv_path):
    repo_path = root_path+repo

    "fine grained"
    f_commits = glob.glob(repo_path+"/1/*.json")
    res = list()
    for f_commit in f_commits:
        single_commit = load_json(f_commit)
        if not len(single_commit["commits"])==0:
            single_commit = single_commit["commits"][0]
            repository_name = single_commit["repository"]
            refactoirngs = single_commit["refactorings"]
            commit_id = single_commit["sha1"]

            for refactoring in refactoirngs:
                a_line = fine_grained_line(refactoring,repo,commit_id)
                a_line.append(" ")
                a_line.append(1)
                res.append(a_line)

    return res



def coarse_grained_process(repo, root_path, csv_path):
    repo_path = root_path+repo

    nums = ["2", "3", "4"]
    res = list()
    for num in nums:
        f_commits = glob.glob(repo_path+"/"+num+"/*.json")
        b_a_dict = get_b_a_commit_dict(repo_path+"/log"+num+".txt")
        for f_commit in f_commits:
            single_commit = load_json(f_commit)
            if not len(single_commit["commits"])==0:
                single_commit = single_commit["commits"][0]
                repository_name = single_commit["repository"]
                refactoirngs = single_commit["refactorings"]
                commit_id = single_commit["sha1"]
                fine_grained_commit_ids = b_a_dict[commit_id]
                for refactoring in refactoirngs:
                    a_line = coarse_grained_line(refactoring, repo, fine_grained_commit_ids)
                    a_line.append(str(is_effective(commit_id, fine_grained_commit_ids, repo_path)))
                    a_line.append(num)
                    res.append(a_line)
    return res


if __name__ =="__main__":
    repoNames = ["jfinal", "mbassador", "javapoet", "jeromq", "seyren", "retrolambda","baasbox","sshj",
                 "xabber-android", "android-async-http", "giraph", "spring-data-rest","blueflood", "HikariCP",
                 "redisson","goclipse", "atomix", "morphia", "PocketHub"]

    root_path = "/home/chenlei/RA/setversion/experimentResult/"
    # root_path = "/Users/leichen/Desktop/"
    csv_path = "/home/chenlei/RA/setversion/csv"
    # csv_path = "/Users/leichen/Desktop/csv/"

    # res = get_b_a_commit_dict("/Users/leichen/Desktop/mbassador/log2.txt")
    # print(res)
    csv_head = ["repository", "commit(s)", "detected_refactoring_type", "description", "leftSideLocations",
                "rightSideLocations", "is_effective", "granularity"]

    for repo in repoNames:
        fine_grained = fine_grained_process(repo, root_path, csv_path)
        coarse_grained = coarse_grained_process(repo, root_path, csv_path)
        res = fine_grained + coarse_grained
        write_2_csv(csv_path + repo + ".csv", csv_head, res)

    # sum =0
    # for each in res:
    #     sum+=1 if is_effective(each,res[each],root_path+repoNames[0]) else 0
    # print(sum)
    # print(is_effective("4c0ee6d3a8c905d9eba25954d8288988cab3d908",res["4c0ee6d3a8c905d9eba25954d8288988cab3d908"],root_path+repoNames[0]))