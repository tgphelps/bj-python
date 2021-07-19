
from log import log
from Hand import Hand
from Shoe import Shoe


class Dealer:
    def __init__(self, shoe: Shoe, hit_s17=True, verbose=False) -> None:
        self.shoe = shoe
        self.verbose = verbose
        self.hit_s17 = hit_s17
        self.hand: Hand
        self.value: int

    def get_hand(self) -> None:
        "Deal yourself a hand."
        self.hand = Hand(self.shoe)
        log(f"dealer hand: {self.hand}")
        assert self.hand.busted is False

    def play_hand(self) -> None:
        "Play dealer hand."
        log(f"   hand: {self.hand}")
        if self.verbose:
            print(f"Dealer: {self.hand}")
        while self.hand.value < 17 \
                or (self.hand.value == 17 and self.hand.is_soft()
                    and self.hit_s17):
            self.hand.hit()
            log(f"   hand: {self.hand}")
            if self.verbose:
                print(f"hit...{self.hand}")
            if self.hand.value > 21 and self.hand.is_soft():
                self.hand.harden()

    def up_card(self) -> int:
        "Return the dealer up-card."
        # Catchy: If dealer was dealt 2 aces, one of them has been
        # changed from 11 to 1. Return 11 in that case.
        card = self.hand.cards[0]
        return 11 if card == 1 else card
