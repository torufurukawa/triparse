"""Parse PDF that contains triathlon race result"""

import sys
import codecs


def main():
    # TODO: use argparse
    fin = open(sys.argv[1], encoding='utf8')
    for line in fin:
        print(line.strip())

    # TODO: parse
    # TODO: print
    pass
    # TODO: analyze and visualize


if __name__ == '__main__':
    main()
