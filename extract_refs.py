import json
import pathlib
import os
import glob
import shutil
from typing import Union
from ROExtract.extractRO import extractRO
from logger import logger_config
from utils import get_config
from repository import Repository
from refactoring_operation.commit import Commit
from line_trace import load_commit_pairs, get_parent_commit
from multiprocessing import Process


def make_directories(output: str, repo_name: str, cluster_num: int):
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


def trace_and_dump(cs: list[Commit], process_idx, repo_temp_p: pathlib.Path, repo: Repository, dump_des) -> None:
    """
    1. copy .git of the target file
    2. trace in the copied .git
    3. dump the ref traced commits into files
    4. remove the copied file
    :param repo:
    :param process_idx:
    :param repo_temp_p:
    :param cs:
    :return:
    """
    process_p = repo_temp_p.joinpath(process_idx)
    process_p.mkdir()
    shutil.copytree(pathlib.Path(repo.repoPath).joinpath(".git"), process_p.joinpath(".git"))
    temp_repo = Repository(str(process_p))
    for c in cs:
        c_parent = get_parent_commit(c.sha1, temp_repo)
        if c_parent:
            c.trace_refs_source_locations(
                parent_commit_sha1=c_parent,
                repo=temp_repo
            )
            c.dump_refs(dump_des)
    shutil.rmtree(process_p)


def trace_and_dump_n(cs: list[Commit], process_idx, repo_temp_p: pathlib.Path, repo: Repository, dump_des,
                     pairs) -> None:
    """
    Similar with trace_and_dum() with only an additional parameter for obtaining parent commit
    :param cs:
    :param process_idx:
    :param repo_temp_p:
    :param repo:
    :param dump_des:
    :param pairs:
    :return:
    """
    process_p = repo_temp_p.joinpath(process_idx)
    process_p.mkdir()
    shutil.copytree(pathlib.Path(repo.repoPath).joinpath(".git"), process_p.joinpath(".git"))
    temp_repo = Repository(str(process_p))
    for coarse_grained_commit in cs:
        coarse_c_parent = get_parent_commit(pairs[coarse_grained_commit.sha1][-1], temp_repo)
        if coarse_c_parent:
            coarse_grained_commit.trace_refs_source_locations(
                parent_commit_sha1=coarse_c_parent,
                repo=temp_repo
            )
            coarse_grained_commit.dump_refs(dump_des)
    shutil.rmtree(process_p)

def attach_source_locations(repo_path: str, squash_log_d: str, squash_num_start=2, squash_num_end=5) -> None:
    '''
    trace source locations for refs in commits in squash_log_d and dump the refs into json files
    Note that only commits contains refactorings will be traced and write into json file.
    :param repo_path: repository where commits belong
    :param squash_log_d: squash result directory
    :param squash_num_start: start squash num
    :param squash_num_end: end squash num
    :return: None
    '''

    def build_directory():
        """
        build a temporary directory to store the copied .git of the target repository
        :return:
        """
        repo_name = pathlib.Path(repo.repoPath).name
        repo_temp_d = pathlib.Path(squash_log_d).parent.parent.joinpath("repo_temp")
        repo_temp_d.mkdir(exist_ok=True)
        p = repo_temp_d.joinpath(repo_name)
        p.mkdir(exist_ok=True)
        return p

    def commits_trace_1(commits: list[Commit]) -> None:
        """
        trace for non-squash commits, trace from their parent commits
        :param commits:
        :return:
        """
        cpu_num = os.cpu_count() / 2
        processes = []
        step = int(len(commits) / cpu_num) + 1
        for i in range(0, len(commits), step):
            processes.append(Process(target=trace_and_dump,
                                     args=(commits[i:i + step], f"1_{i}", repo_temp_p, repo, output_directory)))
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def commits_trace_n(commits: list[Commit], pairs: dict[str, list[str]]):
        """
        trace for squashed commits (coarse-granied commits). For each coarse-grained commit, in the fine-grained commits
        which squashed into it, find the most early fine-grained one in terms of chronological order. Trace is conduct
        on the fine-grained commit's parent commit.
        :param commits: coarse-grained commits list
        :param paris: dict where key is the coarse-grained commits and value is the fine-grained commits which squashed into the coarse-grained one
        :return:
        """
        cpu_num = os.cpu_count() / 2
        processes = []
        step = int(len(commits) / cpu_num) + 1
        for k in pairs.keys():
            squash_num = len(pairs[k])
            break
        for i in range(0, len(commits), step):
            processes.append(Process(target=trace_and_dump_n,
                                     args=(commits[i:i + step], f"{squash_num}_{i}", repo_temp_p, repo, output_directory,pairs)))
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def commits_dump(commits: list[Commit], directory: str) -> None:
        for c in commits:
            c.dump_refs(directory)

    squash_log_d = pathlib.Path(squash_log_d)
    repo = Repository(repo_path)

    repo_temp_p = build_directory()

    for squash_num in range(squash_num_start, squash_num_end + 1):
        squash_log_p = squash_log_d.joinpath(str(squash_num)).joinpath(f"log{squash_num}.txt")
        refs_dir = squash_log_p.parent.joinpath("refs")
        output_directory = squash_log_d.joinpath(f"o{squash_num}").__str__()

        if squash_num == 1:
            cs = [Commit(file) for file in get_json_files_under_directory(refs_dir)]
            commits_trace_1(cs)
        else:
            pairs = load_commit_pairs(squash_log_p.__str__())
            coarse_grained_commits = [Commit(refs_dir.joinpath(c + ".json")) for c in pairs.keys()]
            commits_trace_n(coarse_grained_commits, pairs)


def get_json_files_under_directory(directory: Union[str, pathlib.Path]) -> list[str]:
    directory = directory if isinstance(directory, pathlib.Path) else pathlib.Path(directory)
    return glob.glob(directory.joinpath("*.json").__str__())
