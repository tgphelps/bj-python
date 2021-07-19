#!/usr/bin/env python

"""
Read the stats.txt file, and suumarize its contents. If there are
stats from different strategies in the file, ignore all that are not
the same as the first one found.
"""

import sys
from typing import Dict

STATS = 'stats.txt'


def print_stats(d: Dict[str, int], strategy: str):
    print("strategy", strategy)
    for k in d:
        print(k, d[k])
    gain = 100 * (d['total_won'] - d['total_lost']) / d['total_bet']
    print(f"%win: {gain:5.4}")


def main() -> None:
    strategy = ''
    d: Dict[str, int] = {}
    with open(STATS, 'rt') as fstats:
        for line in fstats:
            f = line.split()
            if len(f) != 2:
                continue
            if f[0] == 'strategy':
                if strategy == '':
                    strategy = f[1]
                elif strategy != f[1]:
                    print('ERROR: strategy:', f[1], file=sys.stderr)
            elif not f[0].startswith('%'):
                if f[0] not in d:
                    d[f[0]] = 0
                d[f[0]] += int(f[1])
    print_stats(d, strategy)


if __name__ == '__main__':
    main()
