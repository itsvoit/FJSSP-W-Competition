from argparse import ArgumentParser

from .deterministic import deterministic_parser
from .uncertainty import uncertainty_parser


def parse_args():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    
    deterministic_parser(subparsers)
    uncertainty_parser(subparsers)
    
    return parser.parse_args()
    
    
def main():
    args = parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    exit(main())
