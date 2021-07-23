

import random
from typing import List

SUIT = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
DECK = 4 * SUIT
assert len(DECK) == 52

SEED = 'Blackjack might be a winnable game.'


class Shoe:
    def __init__(self, decks: int, repeatable=False) -> None:
        self.decks = decks
        self.shoe = DECK * decks
        self.shoe_size = len(DECK) * decks
        self.next = 0
        self.running_count = 0
        self.starting_count = 0  # running_count at start of round
        self.this_round: List[int] = []
        self.track_rounds = False
        # print("shoe contains:", len(self.shoe))
        if repeatable:
            random.seed(SEED)
        else:
            random.seed()  # Use current date/time as seed.

    def enable_tracking(self, yesno: bool) -> None:
        self.track_rounds = yesno

    def shuffle(self) -> None:
        "Shuffle the deck."
        random.shuffle(self.shoe)
        self.next = 0
        self.running_count = 0
        # print("shuffle...")

    def deal(self) -> int:
        "Return the next card from the shoe."
        assert self.next < self.shoe_size
        c = self.shoe[self.next]
        self.next += 1
        if c <= 6:
            self.running_count += 1
        elif c >= 10:
            self.running_count -= 1
        if self.track_rounds:
            self.this_round.append(c)
        # XXX debug
        # print("DEAL:", c, "count:", self.running_count)
        return c

    def remaining(self) -> int:
        "Return the number of cards still in the shoe."
        return self.shoe_size - self.next

    def start_round(self) -> None:
        self.this_round = []
        self.starting_count = self.running_count

    def end_round(self) -> List[int]:
        cards = self.this_round
        self.this_round = []
        return cards
