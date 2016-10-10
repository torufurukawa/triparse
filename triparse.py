"""Parse PDF that contains triathlon race result"""

import sys
import re
import codecs
from datetime import timedelta


def main():
    # TODO: use argparse
    fin = open(sys.argv[1], encoding='utf8')
    for line in fin:

        # TODO: make parser plaggable
        # TODO: fix style
        pattern = r'\d+ (\d+).*?\d:\d{2}:\d{2} (\d:\d{2}:\d{2}) \d+ (\d:\d{2}:\d{2}) \d+ \d:\d{2}:\d{2} \d+ (\d:\d{2}:\d{2}) \d+(\S+)'
        m = re.match(pattern, line)
        if m is None:
            continue
        aid, swim_str, bike_str, run_str, div = m.groups()

        swim_lap = parse_lap(swim_str)
        bike_lap = parse_lap(bike_str)
        run_lap = parse_lap(run_str)

        print(aid, swim_lap, bike_lap, run_lap, div)

    # TODO: automate test
    # TODO: define data structure to represent athlete activity
    # TODO: analyze and visualize


def parse_lap(lap_str):
    """Parse string H:MM:SS and return timedelta"""
    pattern = r'(\d):(\d{2}):(\d{2})'
    hours, minutes, seconds = map(int, re.match(pattern, lap_str).groups())
    result = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return result


if __name__ == '__main__':
    main()
