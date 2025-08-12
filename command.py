import argparse
from extract_refs import run


def commands():
    # example
    # python3 command.py -r /Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/data/refactoring-toy-example_cr -c 2 -o /Users/leichen/Code/pythonProject/pythonProject/pythonProject/SCRMDetection/experiment/output/result/
    parser = argparse.ArgumentParser(description="Extract refactorings from commits in a repository")
    parser.add_argument("-r", help="target repository path")
    parser.add_argument("-c", help="number of commits in a cluster")
    parser.add_argument("-o", help="output path")
    return parser


if __name__ == "__main__":
    args = commands().parse_args()
    run(args.r, args.o, int(args.c))

