import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--full', dest='full', action='store_true'
    )
    parser.add_argument(
        '-p', '--prepare', dest='prepare', action='store_true'
    )
    parser.add_argument(
        '-i', '--initial', dest='initial', action='store_true'
    )
    parser.add_argument(
        '-m', '--map', dest='map', action='store_true'
    )
    return parser
