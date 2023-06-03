"""
remove comments in java files with tool preform
https://github.com/xecua/preform/blob/main/README_ja.md
"""
import subprocess
from line_trace import checkout_latest
from repository import Repository
import argparse

PREFORM = "preform-0.0.1-all.jar"


def remove_comment(target_repo_path, output_path):
    print(f"removing comment for {target_repo_path} to the path {output_path}")
    command = ["java", "-jar", PREFORM, target_repo_path, output_path, "CommentRemover"]
    subprocess.run(command)


def preprocess(target_repo_path, output_path):
    remove_comment(target_repo_path, output_path)
    repository = Repository(output_path)
    checkout_latest(repository)
    repository.addRemote(repository.repoPath)


def command():
    parser = argparse.ArgumentParser(description="remove the comments in code in each commit")
    parser.add_argument("-s", help="source repository")
    parser.add_argument("-t", help="output repository")
    return parser


if __name__ == "__main__":
    args = command().parse_args()
    preprocess(args.s, args.t)
