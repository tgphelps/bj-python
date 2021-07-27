#!/usr/bin/env python

"""
Read the stats.txt file, and suumarize its contents. If there are
stats from different strategies in the file, ignore all that are not
the same as the first one found.
"""

import sys
from typing import Dict, List
import constants as const

STATS_FILE = 'stats.txt'


class Stats():
    "Just a struct to hold the data we want to accumulate."
    def __init__(self) -> None:
        self.tc = 0
        self.r = 0
        self.h = 0
        self.b = 0
        self.w = 0
        self.ls = 0
        self.p = 0
        self.bj = 0
        self.s = 0
        self.g = 0.0


stats: Dict[int, Stats] = {}


def process_tc_data(f: List[str]):
    tc = int(f[1])
    st = stats[tc]
    st.tc = tc
    st.r += int(f[2])
    st.h += int(f[3])
    st.b += int(f[4])
    st.w += int(f[5])
    st.ls += int(f[6])
    st.p += int(f[7])
    st.bj += int(f[8])
    st.s += int(f[9])
    st.g += float(f[10])
    # print(f)


def print_summary():
    r = 0
    h = 0
    b = 0
    w = 0
    ls = 0
    p = 0
    print(" TC  rounds   hands    bet      won      lost     push     edge")
    print("==== ======== ======== ======== ======== ======== ======== =====")
    for tc in range(-const.MAX_TRUE_COUNT, const.MAX_TRUE_COUNT + 1):
        st = stats[tc]
        r += st.r
        h += st.h
        b += st.b
        w += st.w
        ls += st.ls
        p += st.p
        if st.b > 0:
            g = 100 * (st.w - st.ls) / st.b
        else:
            g = 0.0
        print(f"{st.tc:4} {st.r:8} {st.h:8} {st.b:8} {st.w:8} {st.ls:8} {st.p:8} {g:+5.3}")
    g = 100 * (w - ls) / b
    print(f"     {r:8} {h:8} {b:8} {w:8} {ls:8} {p:8} {g:+5.3}")


def main() -> None:
    for tc in range(-const.MAX_TRUE_COUNT, const.MAX_TRUE_COUNT + 1):
        stats[tc] = Stats()

    strategy = ''
    with open(STATS_FILE, 'rt') as fstats:
        for line in fstats:
            line = line.rstrip()
            f = line.split()
            if f[0] == 'strategy':
                if strategy == '':
                    strategy = f[1]
                    print(line)
                elif strategy != f[1]:
                    print('ERROR: strategy:', f[1], file=sys.stderr)
            elif f[0] == 'time':
                pass
            elif f[0] == 'session':
                pass
            elif f[0] == 'tc':
                process_tc_data(f)
    print_summary()


if __name__ == '__main__':
    main()
