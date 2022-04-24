import argparse


def read_args():
    parser=argparse.ArgumentParser(description="squash commits and detect refactoring operations")
    parser.add_argument('repoPath', help='path for repository to be squashed and detected')
    parser.add_argument('o',help='path for experiment output')
    parser.add_argument('-mi', help='minimum coarse granularity, default 1', default=1)
    parser.add_argument('-ma', help='maximum coarse granularity, default 4', default=4)
    parsed=parser.parse_args()
    repoPath=parsed.repoPath
    output=parsed.o
    mi = parsed.mi
    ma = parsed.ma
    return repoPath, output, mi, ma
