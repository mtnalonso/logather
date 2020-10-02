import argparse

from logather import Logather


def main():
    args = load_args()
    logather = Logather(
        min_potential_sources=args.min_log_results
    )
    logather.gather()
    return 0


def load_args():
    parser = argparse.ArgumentParser(prog='logather')
    parser.add_argument(
        '--min-log-results',
        type=int,
        default=50,
        help="minimum number of potential log results to search"
    )
    return parser.parse_args()

