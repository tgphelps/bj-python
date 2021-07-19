#!/bin/env python3


def main() -> None:
    take = False
    with open('trace.txt', 'rt') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('playing'):
                print(line)
                take = True
            elif line.startswith('end play'):
                print(line)
                print()
                take = False
            elif take:
                print(line)
                continue


if __name__ == '__main__':
    main()
