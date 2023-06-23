import argparse
import RQs.RQ1 as RQ1
import RQs.RQ2 as RQ2

def run_rqs():
    pass


def rq_selector(rq_index, *args):
    if rq_index == 1:
        res = RQ1.frequency(*args)
        print(res)
    elif rq_index == 2:
        res = RQ2.frequency(*args)
        print(res)
    else:
        print("Invalid rq index:", rq_index)


def arg_parser():
    parser = argparse.ArgumentParser(description="run rqs")
    parser.add_argument("-i", help="rq index, from 1 to 7")
    parser.add_argument("-p", help="repo path")
    return parser


if __name__ == "__main__":
    args = arg_parser().parse_args()
    rq_selector(args.i, args.p)
