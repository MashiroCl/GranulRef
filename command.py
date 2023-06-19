import argparse
from extract_refs import run, attach_source_locations


def commands():
    parser = argparse.ArgumentParser(description="Extract refactorings from commits in a repository")
    parser.add_argument("-r", help="target repository path")
    parser.add_argument("-c", help="number of commits in a cluster")
    parser.add_argument("-o", help="output path")
    parser.add_argument("-p", help="platform")

    parser.add_argument("-m", help ="mode selection, 'extract' for extracting refactorings from commits in a repository"
                                    "trace for tracing source locations for refactorings")
    parser.add_argument("-d", help = "squash result directory")
    parser.add_argument("--start", help="start squash num")
    parser.add_argument("--end", help="end squash num")
    return parser


if __name__ == "__main__":
    args = commands().parse_args()
    if args.m == "trace":
        attach_source_locations(args.r, args.d, int(args.start), int(args.end))
    else:
        run(args.r, args.o, int(args.c), args.p)

