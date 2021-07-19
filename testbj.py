#!/usr/bin/env python

"""Test random BJ hands and build a database of results.

Usage: testbj.py

This program deals and plays rounds of heads-up blackjack, displays the
results, and asks the user to say yes/no to the play and results. If
the answer is 'no', it stops, and the user can fix the bug. If it's 'yes',
it will save this deal (a ordered list of cards dealt) in a database,
and in the future, this deal will never be shown again.

Thus, over time, the user accumulates an ever-growing database of
correct results, which is one way (maybe a good way) of testing this
simulator.

The user must be careful to always use the same strategy with the same
results database, for consistency.
"""

from typing import Set, Tuple
from sqlitedict import SqliteDict  # type: ignore
import config
import parse
import Game


STRATEGY_FILE = 'data/basic-double-split.txt'
CONFIG_FILE = 'data/house.cfg'
DB_FILE = 'results.db'
MAX_ROUNDS = 20
COMMIT_INTERVAL = 5


def main() -> None:
    house_rules = config.load_config(CONFIG_FILE)
    strategy = parse.parse_strategy(STRATEGY_FILE)
    db = SqliteDict(DB_FILE)

    play_bj(db, strategy, house_rules)
    db.commit()
    db.close()


def play_bj(db, strategy: Set[Tuple[str, int, int]], house_rules: dict):
    game = Game.Game(strategy=strategy,
                     players=1,
                     verbose=True,
                     rules=house_rules)
    game.shoe.enable_tracking(True)

    hands = 0
    duplicates = 0
    for i in range(MAX_ROUNDS):
        print(f"round: {i}\n\n\n")
        game.shoe.start_round()
        game.play_round()
        hands += 1
        cards_used = game.shoe.end_round()
        key = ','.join(map(str, cards_used))
        print(cards_used)
        if key in db:
            print('\n\nDUPLICATE\n\n')
            duplicates += 1
        else:
            ans = input('Another? >')
            if ans.startswith('n'):
                break
            add_to_db(db, key)
        if (i + 1) % COMMIT_INTERVAL == 0:
            print('commit')
            db.commit()
    print(f'\nHands played = {hands}')
    print(f'Duplicates = {duplicates}')
    print(f'Total tests = {count_keys(db)}')


def add_to_db(db, key: str):
    print(f'key = {key}')
    db[key] = 1


def count_keys(db):
    n = 0
    for key in db:
        n += 1
    return n


if __name__ == '__main__':
    main()
