"""Parse PDF that contains triathlon race result"""

import sys
import re
import codecs
from datetime import timedelta
import argparse

import numpy
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'
from matplotlib import pyplot


def main():
    args = get_args()
    race = build_race_results(open(args.filepath, encoding='utf8'))

    print(len(race.results))
    # TODO: add logging
    # TODO: automate test

    # Analyze
    swim_laps = [r.swim_lap.total_seconds() for r in race.results.values()]
    # TODO: parametrize bin count
    bin_count = 50
    n, bins, patches = pyplot.hist(swim_laps, bin_count, cumulative=True, normed=1)

    # TODO: format time on X axis

    ref_result = race.get_result(args.aid)
    pyplot.axvline(ref_result.swim_lap.total_seconds(), color='red', linestyle='dashed', linewidth=2)

    pyplot.show()

    # TODO: bike, run and total
    # TODO: stat within division


class Race:
    def __init__(self):
        self.results = {}

    def add_result(self, result):
        self.results[result.id] = result

    def get_result(self, aid):
        return self.results.get(aid)


class Result:
    def __init__(self, id_, swim_lap, bike_lap, run_lap, division):
        self.id = id_
        self.swim_lap = swim_lap
        self.bike_lap = bike_lap
        self.run_lap = run_lap
        # TODO: make division enum
        self.division = division

    def __str__(self):
        return '<Result id={}>'.format(self.id)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='Path to result file')
    parser.add_argument('aid', help='Athelete ID')
    result = parser.parse_args()
    return result


def build_race_results(textfile):
    race = Race()
    for result in result_reader(textfile):
        race.add_result(result)
    return race


def result_reader(textfile):
    """Iterate over results

    textfile is sequence of single line texts that contain athete results
    """
    for line in textfile:

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

        result = Result(aid, swim_lap, bike_lap, run_lap, div)

        yield result


def parse_lap(lap_str):
    """Parse string H:MM:SS and return timedelta"""
    pattern = r'(\d):(\d{2}):(\d{2})'
    hours, minutes, seconds = map(int, re.match(pattern, lap_str).groups())
    result = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    return result


if __name__ == '__main__':
    main()
