#!/usr/bin/env python3

"""
This reads a log file and verifies that all the 'action' entries are
corrent. And action entry looks like:
    act: key value up-card action
"""

act_line = ''


def main():
    global act_line
    with open('trace.txt', 'rt') as fd:
        for line in fd:
            line = line.rstrip()
            act_line = line
            if line.startswith('act:'):
                f = line.split()
                assert len(f) == 5
                if f[1] == 'hh':
                    verify_hh(int(f[2]), int(f[3]), f[4])
                elif f[1] == 'hs':
                    verify_hs(int(f[2]), int(f[3]), f[4])
                elif f[1] == 'dh':
                    verify_dh(int(f[2]), int(f[3]), f[4])
                elif f[1] == 'ds':
                    verify_ds(int(f[2]), int(f[3]), f[4])
                elif f[1] == 'sp':
                    verify_sp(int(f[2]), int(f[3]), f[4])
                elif f[1] == 'su':
                    verify_su(f[2], int(f[3]), f[4])
                else:
                    print("ERROR", line)


def error(key: str, val: int, up: int, act: str) -> None:
    # print("ERROR", key, val, up, act)
    print("ERROR", act_line)


def verify_hh(val: int, up: int, act: str) -> None:
    if (val >= 17 and act == 'stand') \
      or (val in (13, 14, 15, 16) and up >= 7 and act == 'hit') \
      or (val in (13, 14, 15, 16) and up <= 6 and act == 'stand') \
      or (val == 12 and up in (4, 5, 6) and act == 'stand') \
      or (val == 12 and up in (2, 3, 7, 8, 9, 10, 11) and act == 'hit') \
      or (val <= 11 and act == 'hit'):
        pass
    else:
        error('hh', val, up, act)


def verify_hs(val: int, up: int, act: str) -> None:
    if (val >= 19 and act == 'stand') \
      or (val == 18 and up >= 9 and act == 'hit') \
      or (val == 18 and up <= 8 and act == 'stand') \
      or (val <= 17 and act == 'hit'):
        pass
    else:
        error('hs', val, up, act)


def verify_dh(val: int, up: int, act: str) -> None:
    if (val == 11 and act == 'double') \
      or (val > 11 and act == 'no-double') \
      or (val < 9 and act == 'no-double') \
      or (val == 9 and up in (3, 4, 5, 6) and act == 'double') \
      or (val == 9 and up not in (3, 4, 5, 6) and act == 'no-double') \
      or (val == 10 and up < 10 and act == 'double') \
      or (val == 10 and up >= 10 and act == 'no-double'):
        pass
    else:
        error('dh', val, up, act)


def verify_ds(val: int, up: int, act: str) -> None:
    if (val in (13, 14) and up in (5, 6) and act == 'double') \
      or (val in (13, 14) and up not in (5, 6) and act == 'no-double') \
      or (val in (15, 16) and up in (4, 5, 6) and act == 'double') \
      or (val in (15, 16) and up not in (4, 5, 6) and act == 'no-double') \
      or (val == 19 and up == 6 and act == 'double') \
      or (val == 19 and up != 6 and act == 'no-double') \
      or (val == 17 and up in (3, 4, 5, 6) and act == 'double') \
      or (val == 17 and up not in (3, 4, 5, 6) and act == 'no-double') \
      or (val == 18 and up in (2, 3, 4, 5, 6) and act == 'double') \
      or (val == 18 and up not in (2, 3, 4, 5, 6) and act == 'no-double') \
      or (val >= 20 and act == 'no-double') \
      or (val >= 12 and act == 'no-double'):
        pass
    else:
        error('ds', val, up, act)


def verify_sp(val: int, up: int, act: str) -> None:
    if (val in (8, 11) and act == 'split') \
      or (val in (5, 10) and act == 'no-split') \
      or (val in (2, 3) and up <= 7 and act == 'split') \
      or (val in (2, 3) and up > 7 and act == 'no-split') \
      or (val == 4 and up in (5, 6) and act == 'split') \
      or (val == 4 and up not in (5, 6) and act == 'no-split') \
      or (val == 6 and up in (2, 3, 4, 5, 6) and act == 'split') \
      or (val == 6 and up not in (2, 3, 4, 5, 6) and act == 'no-split') \
      or (val == 7 and up in (2, 3, 4, 5, 6, 7) and act == 'split') \
      or (val == 7 and up not in (2, 3, 4, 5, 6, 7) and act == 'no-split') \
      or (val == 9 and up in (2, 3, 4, 5, 6, 8, 9) and act == 'split') \
      or (val == 9 and up not in (2, 3, 4, 5, 6, 8, 9) and act == 'no-split'):
        pass
    else:
        error('sp', val, up, act)


def verify_su(val: str, up: int, act: str) -> None:
    if (val == 'soft' and act == 'no-surrender') \
      or (val not in ('15', '16', '17') and act == 'no-surrender') \
      or (val == '17' and up == 11 and act == 'surrender') \
      or (val == '17' and up < 11 and act == 'no-surrender') \
      or (val == '15' and up >= 10 and act == 'surrender') \
      or (val == '15' and up < 10 and act == 'no-surrender') \
      or (val == '16' and up >= 9 and act == 'surrender') \
      or (val == '16' and up < 9 and act == 'no-surrender'):
        pass
    else:
        error('su', int(val), up, act)


if __name__ == '__main__':
    main()
