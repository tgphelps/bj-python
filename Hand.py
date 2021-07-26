
from log import log
from Shoe import Shoe


class Hand:
    def __init__(self, shoe: Shoe, split_card=0) -> None:
        self.value: int

        self.blackjack = False
        self.doubled = False
        self.busted = False
        self.is_split = False
        self.no_hit = False  # True => Hit not allowed
        self.obsolete = False  # Set true when a pair is split into new hands.
        self.surrendered = False

        self.shoe = shoe

        if not split_card:
            self.cards = [shoe.deal(), shoe.deal()]
        else:
            # This is a pair split. Deal one additional card.
            self.cards = [split_card, shoe.deal()]
            self.is_split = True

        self.update_value()
        if self.value == 21:
            self.blackjack = True
            # But wait...
            if self.is_split and split_card == 11:
                log("NOT blackjack")
                self.blackjack = False
        if self.big_aces == 2:
            self.harden()

    def harden(self) -> None:
        "Convert one of the aces from 11 to 1"
        first_ace = self.cards.index(11)
        self.cards[first_ace] = 1
        self.update_value()

    def update_value(self) -> None:
        self.value = sum(self.cards)
        self.big_aces = self.cards.count(11)

    def is_soft(self) -> bool:
        "Return True if one of the aces is counted as 11."
        return self.big_aces > 0

    def is_pair(self) -> bool:
        "Return True if the initial hand is a pair."
        assert len(self.cards) == 2
        if self.cards[0] == self.cards[1]:
            return True
        if self.cards == [1, 11] or self.cards == [11, 1]:
            return True
        return False

    def __str__(self) -> str:
        return f"{str(self.cards)}: {self.value}"

    def double(self) -> None:
        "Double the bet, and take ONE card."
        self.doubled = True
        self.hit()

    def hit(self) -> None:
        """
        Hit the hand. If it puts the total over 21, try to count an ace
        as 1, instead of 11. Set 'busted' if we can't get the total under 21.
        """
        assert not self.obsolete
        c = self.shoe.deal()
        self.cards.append(c)
        self.update_value()
        if c == 11:
            self.big_aces += 1
        if self.value > 21:
            if self.big_aces:
                self.harden()
            else:
                self.busted = True

    def surrender(self) -> None:
        "Mark the hand as surrendered."
        self.surrendered = True
