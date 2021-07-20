
from typing import List, Set, Dict, Tuple

import constants as c
from log import log
from Shoe import Shoe
from Hand import Hand


class Player:
    def __init__(self, shoe: Shoe,
                 strategy: Set[Tuple[str, int, int]],
                 rules: Dict[str, int],
                 verbose: bool,
                 bet_amount=0, seat=0) -> None:
        self.strategy = strategy
        self.max_splits = rules['max_split_hands'] - 1
        self.max_split_aces = rules['max_split_aces'] - 1
        self.can_hit_split_aces = rules['can_hit_split_aces']
        self.das_allowed = rules['das_allowed']
        self.surrender_allowed = rules['surrender']
        self.verbose = verbose

        self.splits_done = 0
        self.shoe = shoe
        self.seat = seat
        self.bet_amount = bet_amount
        self.hands: List[Hand] = []

    def log_hands(self):
        "Log all hand contents."
        log("All hands:")
        for h in self.hands:
            log(f"   hand: {h}")

    def get_hand(self, split_card=0) -> None:
        "Get a new hand, either with 2 new cards, or 1 new card to a split."
        if split_card == 0:
            self.hands.append(Hand(self.shoe, bet_amount=self.bet_amount))
        else:
            h = (Hand(self.shoe, split_card=split_card,
                 bet_amount=self.bet_amount))
            if split_card == 11 and not self.can_hit_split_aces:
                h.no_hit = True
            self.hands.append(h)

    def play_hands(self, up_card: int) -> None:
        "Play each hands. Split pairs generate new hands."
        i = 0
        for h in self.hands:
            i += 1
            log(f"hand {i}")
            if self.verbose:
                s = "soft" if h.is_soft() else ""
                print(f"hand: {s} {h} vs {up_card}")
            if h.no_hit:
                log("cannot hit split ace")
            else:
                if not self.maybe_surrender(h, up_card):
                    if not self.maybe_split(h, up_card):
                        if not self.maybe_double_down(h, up_card):
                            self.play_normal(h, up_card)

    def end_round(self) -> None:
        "Throw away all hands, to get ready for the next round."
        self.hands = []
        self.splits_done = 0

    def maybe_surrender(self, hand: Hand, up_card: int) -> bool:
        "Surrender this hand if strategy says to do so."
        key = (c.SURRENDER, hand.value, up_card)
        if key in self.strategy:
            hand.surrender()
            return True
        else:
            return False

    def maybe_split(self, hand: Hand, up_card: int) -> bool:
        """Split this hand if it's a pair, and stategy dictates it.

        To split, create 2 more hands, and append them to the list.
        Return True if we split, else False.
        """
        if hand.is_pair():
            # Catchy: A pair of aces will show as [1, 11] or [11, 1]
            sp_card = 11 if hand.cards[0] == 1 else hand.cards[0]
            key = (c.SPLIT, sp_card, up_card)
            if key in self.strategy:
                log(f"act: {key[0]} {key[1]} {key[2]} split")
                if (sp_card == 11 and self.splits_done < self.max_split_aces) \
                   or (sp_card != 11 and self.splits_done < self.max_splits):
                    self.splits_done += 1
                    hand.obsolete = True
                    self.get_hand(split_card=sp_card)
                    self.get_hand(split_card=sp_card)
                    if self.verbose:
                        print("SPLIT")
                    self.log_hands()
                    return True
                else:
                    log("already at max splits")
                    return False
            else:  # Did not split
                log(f"act: {key[0]} {key[1]} {key[2]} no-split")
                return False
        else:
            return False

    def maybe_double_down(self, hand: Hand, up_card: int) -> bool:
        """Double down if the strategy dictates it.

        Return True if we doubled, else False.
        """
        if hand.is_split and not self.das_allowed:
            log("das not allowed")
            return False
        if not hand.is_soft():
            key = (c.DBL_HARD, hand.value, up_card)
            if key in self.strategy:
                log(f"act: {key[0]} {key[1]} {key[2]} double")
                hand.double()
                log(f"hand: {hand}")
                if self.verbose:
                    print(f"DOUBLE...{hand}")
                log("")
                return True
            else:
                log(f"act: {key[0]} {key[1]} {key[2]} no-double")
                return False
        else:
            key = (c.DBL_SOFT, hand.value, up_card)
            if key in self.strategy:
                log(f"act: {key[0]} {key[1]} {key[2]} double")
                hand.double()
                log(f"hand: {hand}")
                if self.verbose:
                    print(f"DOUBLE...{hand}")
                log("")
                return True
            else:
                log(f"act: {key[0]} {key[1]} {key[2]} no-double")
                return False

    def play_normal(self, hand: Hand, up_card: int) -> None:
        """Use the normal hit/stand strategy."""
        log("hit/stand")
        while True:
            # Loop till we stand
            if hand.is_soft():
                log(f"soft: {hand}")
                key = (c.HIT_SOFT, hand.value, up_card)
                if not self.play_strategy(key, hand):
                    break
            else:
                log(f"hard: {hand}")
                key = (c.HIT_HARD, hand.value, up_card)
                if not self.play_strategy(key, hand):
                    break

    def play_strategy(self, key: Tuple[str, int, int], hand: Hand) -> bool:
        "Return True if we hit and didn't bust, else False."
        if key in self.strategy:
            log(f"act: {key[0]} {key[1]} {key[2]} hit")
            hand.hit()
            if self.verbose:
                s = "soft" if hand.is_soft() else ""
                print(f"hit...{s} {hand}")
            if hand.busted:
                log(f"BUST: {hand}")
                ret = False
            else:
                ret = True
        else:
            log(f"act: {key[0]} {key[1]} {key[2]} stand")
            ret = False
        if not ret:
            log("")
        return ret
