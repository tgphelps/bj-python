#!/usr/bin/env python

"""
bj.py: Blackjack simulator, for studying the game.

Usage:
    bj.py [-d <flags>] [-v] [-r] [-l] [-n <rounds>] [-s <seats>] [ -b bet_spread ] \
    [ --ins <tc> ] HOUSE-RULES STRATEGY

Options:
    -h  --help           Show this screen, and exit.
    --version            Show version, and exit.
    -v                   Be verbose.
    -l                   Write log file entries.
    -r                   Generate repeatable deals.
    -d <flags>           Set debug flags.
    -n <rounds>          Number of rounds to play.
    -s <seats>           Number of players to play.
    -b <bet_spread>      What max bet spread to use.
    --ins <tc>           True count at which to take insurance. 0 => never.
"""

from typing import Dict, Any

import docopt  # type:ignore

import config
import Game
import log
import parse
# import constants as const


# Global parameters

VERSION = '0.3'
LOG_FILE = 'trace.txt'
STATS_FILE = 'stats.txt'


class Globals:
    verbose: bool
    log: bool
    repeatable: bool
    debug: str
    num_rounds: int
    num_players: int
    bet_spread: int
    ins_count: int

    rules: Dict[str, int]

# Global variables


g = Globals()

# Set from command line flags
g.verbose = False
g.log = False
g.repeatable = False
g.debug = ''
g.num_rounds = 1
g.num_players = 1
g.bet_spread = 1
g.ins_count = 0  # 0 => Never take insurance.

g.rules = {}

# ---------------------------


def save_cmd_line(args: Dict[str, Any]) -> None:
    "Store command line args into global variables."

    if args['-v']:
        g.verbose = True
    if args['-l']:
        g.log = True
    if args['-r']:
        g.repeatable = True
    flags = args['-d']
    if flags:
        g.debug = flags
    n = args['-n']
    if n:
        g.num_rounds = int(n)
    n = args['-s']
    if n:
        g.num_players = int(n)
    b = args['-b']
    if args['-b']:
        g.bet_spread = int(b)
    ins = args['--ins']
    if ins:
        g.ins_count = int(ins)


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
    if g.log:
        log.log_open(LOG_FILE)

    log.log(f"bet spread: {g.bet_spread}")
    if g.verbose:
        print("bet_spread:", g.bet_spread)
    read_config(args['HOUSE-RULES'])
    strategy = parse.parse_strategy(args['STRATEGY'])

    # ----------- The interesting stuff goes here.

    game = Game.Game(strategy=strategy,
                     players=g.num_players,
                     repeatable=g.repeatable,
                     rules=g.rules,
                     bet_spread=g.bet_spread,
                     ins_count=g.ins_count,
                     verbose=g.verbose)

    for i in range(g.num_rounds):
        log.log(f"round: {i + 1}")
        if g.verbose:
            print("\nround:", i + 1)
            print("round start count:", game.shoe.running_count)
        game.play_round()
        if g.verbose:
            print("running count", game.shoe.running_count)
            print("true count:", game.shoe.true_count())
            _ = input("...")

    game.write_stats(STATS_FILE, args['STRATEGY'])

    # -----------

    if g.log:
        log.log_close()


count = 0  # static


if __name__ == '__main__':
    # import cProfile
    # cProfile.run('main()')
    main()
