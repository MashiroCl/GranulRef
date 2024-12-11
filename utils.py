"""
1.create a json file read json file
2.find cc_lists and p_lists
3.RM on current all commits (merge excluded)
4.squash
5.RM on remaining all commits (merge excluded)
"""
import pathlib

from jsonUtils import JsonUtils
import json
import time


def RM_supported_type(RMSupportedREF):
    dict = {}
    with open(RMSupportedREF) as f:
        lines = f.readlines()
    for each in lines:
        dict[each.lower().strip()] = 0
    return dict

def dictAdd(dictS, dict2) -> dict:
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


def dictAverage(d, num) -> dict:
    for each in d:
        d[each] = d[each] / num


def dictCompare(dict1, dict2, RMSupportedREF) -> list:
    dictAdd = RM_supported_type(RMSupportedREF)
    dictDecrease = RM_supported_type(RMSupportedREF)
    for each1 in dict1:
        difference = dict2[each1] - dict1[each1]
        if difference > 0:
            dictAdd[each1] = difference
        if difference < 0:
            dictDecrease[each1] = -1 * difference
    return dictAdd, dictDecrease


def dictCount(dict) -> int:
    num = 0
    for each in dict:
        num += dict[each]
    return num


def exclude_0_in_dict(dict):
    dict2 = {}
    for each in dict:
        if dict[each] != 0:
            dict2[each] = dict[each]
    return dict2


def squashWithRecipe(repo, cc_lists_str, recipe, git_stein, squashedOutput, steinOuput, coarse_normal_commit_map) -> str:
    '''
    squash commits according to recipe.json using git_stein
    :param jU: jsonUtil instance
    :param repo: Reository instance
    :param cc_lists_str: commit lists
    :param recipe: path for recipe.json
    :param git_stein: path for git_stein
    :param squashedOutput: output json file path
    :return: list of newly generated commit sha1 because of squash
    '''
    'Write recipe'
    JsonUtils().writeRecipe(cc_lists_str, recipe)
    'Squash according to recipe'
    repo.squashCommits(recipe, git_stein, squashedOutput, repo.repoPath, steinOuput)
    'Find newly generated commit No.'
    steinLog = steinOuput + "/stein.log"
    with open(steinLog, "r") as f:
        lines = f.readlines()
    result = []
    for eachList in cc_lists_str:
        for eachLine in lines:
            if " Rewrite commit: " in eachLine:
                temp = eachLine.split("Rewrite commit: ")[1].split(" -> ")
                'Attention: merge not excluded'
                if temp[0].strip() == eachList[0].strip():
                    result.append(temp[1].strip())
                    coarse_normal_commit_map[temp[1].strip()] = eachList
    return result


def getConfig():
    with open("../config.json") as f:
        data = json.load(f)
    return data

def get_config():
    with open("config.json") as f:
        data = json.load(f)
    return data

def outputTime(t) -> str:
    h = t // 3600
    m = (t - h * 3600) // 60
    s = t - h * 3600 - m * 60
    tResult = 'time cost:  {:.0f}h {:.0f}min {:.0f}s'.format(h, m, s)
    return tResult


def timeRecord():
    return time.time()


def load_coarse_normal_commit_map(path)->dict:
    if not path.exists():
        return {}
    with open(str(path)) as f:
        data = json.load(f)
    return dict(data)


def load_commit_pairs_all(repo_path):
    res = dict()
    for i in range(2, 6):
        squash_log_ps = pathlib.Path(repo_path).joinpath(str(i)).joinpath(f"coarse_normal_commit_map.json")
        res.update(load_coarse_normal_commit_map(squash_log_ps))
    return res
