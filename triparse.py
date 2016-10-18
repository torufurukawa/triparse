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

# TODO: parametrize bin count
BIN_COUNT = 20

# TODO: add logging
# TODO: automate test


def main():
    args = get_args()
    race = build_race_results(open(args.filepath, encoding='utf8'))
    plot_histograms(race, args.aid)


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


def plot_histograms(race, aid):
    bin_count = BIN_COUNT
    ref_result = race.get_result(aid)

    for i, attr in enumerate(['swim_lap', 'bike_lap', 'run_lap']):
        pyplot.subplot(2, 2, i+1)
        times = [getattr(r, attr).total_seconds() for r in race.results.values()]
        ref_time = getattr(ref_result, attr).total_seconds()
        plot_histogram(times, bin_count, ref_time)

    #pyplot.savefig('swim.png')
    pyplot.show()

    # TODO: run and total
    # TODO: stat within division


def plot_histogram(times, bin_count, ref_time):
    pyplot.hist(times, bin_count, cumulative=True, normed=1)
    pyplot.axvline(ref_time, color='red', linestyle='dashed', linewidth=2)
    # TODO: format time on X axis
    # TODO: format Y axis as %
    # TODO: draw horizontal line
    # TODO: render figure title
    # TODO: align x and y max


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
