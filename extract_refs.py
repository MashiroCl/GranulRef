import os
from ROExtract.extractRO import extractRO
from logger import logger_config
from utils import get_config


def make_directories(output: str, repo_name, cluster_num):
    """
    -repo_name/
    ----cluster_num/
    ----------squashed_git/
    ----------refs/
    ----------recipe.json
    ----------stein.log
    ----------log<cluster_num>.txt
    ----------time.txt
    :param output:
    :param repo_name:
    :param cluster_num:
    :return:
    """
    snapshot_folder = os.path.join(output, repo_name, str(cluster_num))
    os.makedirs(snapshot_folder, exist_ok=True)
    squashed_git_p = os.path.join(snapshot_folder, "squashed_git")
    os.mkdir(squashed_git_p)
    refs = os.path.join(snapshot_folder, "refs")
    os.mkdir(refs)
    return snapshot_folder, squashed_git_p, refs


def run(repo_path, output, cluster_num, platform):
    data = get_config()
    RMPath = data[platform]["RMPath"]
    git_stein = data[platform]["git_stein"]

    repo_name = repo_path.split("/")[-1]

    snapshot_folder, squashed_git_p, refs = make_directories(output, repo_name, cluster_num)

    recipe = os.path.join(snapshot_folder, "recipe.json")

    logger = logger_config(log_path=snapshot_folder + '/log' + str(cluster_num) + '.txt',
                           logging_name=repo_name + " " + str(cluster_num) + "by" + str(cluster_num))

    logger.info("start squash " + str(cluster_num) + "by" + str(cluster_num))
    extractRO(RMPath=RMPath,
              repoPath=repo_path,
              recipe=recipe, git_stein=git_stein,
              squashedOutput=squashed_git_p,
              clusterNum=cluster_num, jsonOutputDirectory=refs, logger=logger,
              steinOuput=snapshot_folder)
    logger.info("finish squash " + str(cluster_num) + "by" + str(cluster_num))

    os.system("rm -rf " + squashed_git_p)
