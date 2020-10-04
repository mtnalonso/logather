import argparse

from logather import Logather


def main():
    args = load_args()
    logather = Logather(
        min_potential_sources=args.min_log_results
    )
    valid_sources = logather.gather()

    if args.output_file:
        save_sources_to_file(args.output_file, valid_sources)

    return 0


def load_args():
    parser = argparse.ArgumentParser(prog='logather')
    parser.add_argument(
        '--min-log-results',
        type=int,
        default=50,
        help="minimum number of potential log results to search"
    )
    parser.add_argument(
        '-o',
        '--output-file',
        type=str,
        help="output file"
    )
    return parser.parse_args()


def save_sources_to_file(filename, sources):
    with open(filename, 'w') as output_file:
        for source in sources:
            output_file.write(source + '\n')
    return
