import argparse
from extract_refs import run


def commands():
    parser = argparse.ArgumentParser(description="Extract refactorings from commits in a repository")
    parser.add_argument("-r", help="target repository path")
    parser.add_argument("-c", help="number of commits in a cluster")
    parser.add_argument("-o", help="output path")
    parser.add_argument("-p", help="platform")
    return parser


if __name__ == "__main__":
    args = commands().parse_args()
    run(args.r, args.o, int(args.c), args.p)
