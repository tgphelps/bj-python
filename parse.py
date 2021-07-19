
from typing import Set, Tuple, List

import constants as c

strategy: Set[Tuple[str, int, int]] = set()


def do_hit(s: str, f: List[str]) -> None:
    counts = f[2].split(',')
    upcards = f[4].split(',')

    for ct in counts:
        for u in upcards:
            key = (s, int(ct), int(u))
            assert key not in strategy
            strategy.add(key)


def do_split(f: List[str]) -> None:
    counts = f[1].split(',')
    upcards = f[3].split(',')

    for ct in counts:
        for u in upcards:
            key = (c.SPLIT, int(ct), int(u))
            assert key not in strategy
            strategy.add(key)


def do_double(s: str, f: List[str]) -> None:
    counts = f[2].split(',')
    upcards = f[4].split(',')

    for ct in counts:
        for u in upcards:
            key = (s, int(ct), int(u))
            assert key not in strategy
            strategy.add(key)


def do_surrender(f: List[str]) -> None:
    counts = f[1].split(',')
    upcards = f[3].split(',')

    for ct in counts:
        for u in upcards:
            key = (c.SURRENDER, int(ct), int(u))
            assert key not in strategy
            strategy.add(key)


def parse_strategy(fname: str) -> Set[Tuple[str, int, int]]:
    with open(fname, 'rt') as fd:
        for line in fd:
            line = line.rstrip()
            # print(line)
            if line.startswith('#'):
                continue
            if len(line) == 0:
                continue
            f = line.split()

            if f[0] == 'hit':
                if f[1] == 'hard':
                    do_hit(c.HIT_HARD, f)
                elif f[1] == 'soft':
                    do_hit(c.HIT_SOFT, f)
                else:
                    print('error:', line)
            elif f[0] == 'double':
                if f[1] == 'hard':
                    do_double(c.DBL_HARD, f)
                elif f[1] == 'soft':
                    do_double(c.DBL_SOFT, f)
                else:
                    print('error:', line)
            elif f[0] == 'split':
                do_split(f)
            elif f[0] == 'surrender':
                do_surrender(f)
            else:
                print('error:', line)
    return strategy


if __name__ == '__main__':

    s = parse_strategy('data/never-bust.txt')
    print(s)
    print()
    last = ''
    for key in s:
        code = key[0]
        if code != last:
            print('--->', code)
            last = code
        print(key)
