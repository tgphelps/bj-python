#!/usr/bin/env python

"""
bj.py: Blackjack simulator, for studying the game.

Usage:
    bj.py [-d <flags>] [-v] [-t] [-n <rounds>] [-s <seats>] [--test] \
HOUSE-RULES STRATEGY

Options:
    -h  --help           Show this screen, and exit.
    --version            Show version, and exit.
    -v                   Be verbose.
    -t                   Trace all plays to log file.
    -d <flags>           Set debug flags.
    -n <rounds>          Number of rounds to play.
    -s <seats>           Number of players to play.
    --test               Use repeatable card sequence.
"""

from typing import Dict, Any

import docopt  # type:ignore

import config
import Game
import log
import parse


# Global parameters

VERSION = '0.10'
LOG_FILE = 'trace.txt'
STATS_FILE = 'stats.txt'


class Globals:
    verbose: bool
    trace: bool
    test: bool
    debug: str
    num_rounds: int
    num_players: int

    rules: Dict[str, int]

# Global variables


g = Globals()

# Set from command line flags
g.verbose = False
g.trace = False
g.test = False
g.debug = ''
g.num_rounds = 1
g.num_players = 1

g.rules = {}

# ---------------------------


def save_cmd_line(args: Dict[str, Any]) -> None:
    "Store command line args into global variables."

    if args['-v']:
        g.verbose = True
    if args['-t']:
        g.trace = True
    if args['--test']:
        g.test = True
    flags = args['-d']
    if flags:
        g.debug = flags
    n = args['-n']
    if n:
        g.num_rounds = int(n)
    n = args['-s']
    if n:
        g.num_players = int(n)


def read_config(cfg_file: str) -> None:
    "Read a config file, and store info in global variables."
    g.rules = config.load_config(cfg_file)
    log.log(f"config: {g.rules}")


def main() -> None:
    args = docopt.docopt(__doc__, version=VERSION)
    save_cmd_line(args)
    if g.verbose:
        print("Version:", VERSION)
        print(args)
    if g.trace:
        log.log_open(LOG_FILE)

    read_config(args['HOUSE-RULES'])
    strategy = parse.parse_strategy(args['STRATEGY'])

    # ----------- The interesting stuff goes here.

    game = Game.Game(strategy=strategy,
                     players=g.num_players,
                     repeatable=g.test,
                     rules=g.rules,
                     verbose=g.verbose)

    for i in range(g.num_rounds):
        log.log(f"round: {i + 1}")
        game.play_round()

    game.write_stats(STATS_FILE, args['STRATEGY'])

    # -----------

    if g.trace:
        log.log_close()


if __name__ == '__main__':
    main()
