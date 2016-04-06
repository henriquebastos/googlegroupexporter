import argparse
import logging

import sys
from tqdm import tqdm


def command_line(args=None):
    parser = argparse.ArgumentParser(description='Export all googlegroups messages.')
    parser.add_argument('group', help='Group name on the url.')
    parser.add_argument('mode', choices=['csv', 'mbox'], help='Export topic list to csv or all messages to mbox.')
    parser.add_argument('-c', '--cookies', type=argparse.FileType(), help='Cookie file.', required=True)
    parser.add_argument('-d', '--cachedir', default='webcache', dest='cache_dir')
    parser.add_argument('-t', '--cachedays', type=int, default=7, dest='cache_days')
    parser.add_argument('-f', '--cacheforever', action='store_true', default=False, dest='cache_forever')
    parser.add_argument('-w', '--workers', type=int, default=10)
    parser.add_argument('-v', '--verbose', type=int, choices=[1, 2], default=1)

    return parser.parse_args(args)


def verbosity(level):
    if level < 2:
        return

    root = logging.getLogger()
    console = logging.StreamHandler(sys.stdout)
    root.addHandler(console)
    root.setLevel(logging.DEBUG)


class ProgressBar(tqdm):
    def update(self, progress=0, total=None):
        if self.disable:
            return

        if total and total != self.total:
            self.total = total

        assert progress >= self.n
        offset = progress - self.n
        if offset > 0:
            super().update(offset)


def progressbar():
    return ProgressBar(leave=True, bar_format='[{elapsed}] {n_fmt} downloads from {total_fmt} requests')
