"""Parse PDF that contains triathlon race result"""

import sys
import re
import codecs


def main():
    # TODO: use argparse
    fin = open(sys.argv[1], encoding='utf8')
    for line in fin:

        # TODO:DOING parse
        pattern = r'\d+ (\d+).*?\d:\d{2}:\d{2} (\d:\d{2}:\d{2}) \d+ (\d:\d{2}:\d{2}) \d+ \d:\d{2}:\d{2} \d+ (\d:\d{2}:\d{2}) \d+(\S+)'
        m = re.match(pattern, line)
        if m is None:
            continue
        aid, swim_str, bike_str, run_str, div = m.groups()

        # TODO: print
        pass

    # TODO: analyze and visualize


if __name__ == '__main__':
    main()
