from utils import JsonUtils,CommitGraph
from MyRepository import MyRepository
import json

def obtainRecipe(repoPath, clusterNum, recipePath, git_stein, squashedOutput):
    """
    Obtain recipe used in git-stein to squash

    :param repoPath:
    :param clusterNum: 2-4
    :param recipePath: path for output
    :param git_stein: path for git-stein/build/libs/git-stein-all.jar
    :param squashedOutput:
    :return:
    """
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
    cG.formGraph()

    #Extract cc_lists
    cc_lists = cG.getCClist()
    cc_lists_str=cG.getCCListStr(cc_lists)

    recipe = {}
    recipe["forcedClusters"]=[]
    for each in cc_lists_str:
        possibleSquashes, commitNumAfterSquash = cG.clusterList(each, clusterNum)
        for each2 in possibleSquashes[0]:
            if len(each2)>1:
                recipe["forcedClusters"].append(each2)
    with open(recipePath,"w") as f:
        json.dump(recipe,f)
    print(recipe)

    # repo.squashCommits(recipePath,git_stein,squashedOutput,repo.repoPath)