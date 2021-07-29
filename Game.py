
import time
from typing import Set, Tuple, List, Dict

from log import log
from Shoe import Shoe
from Dealer import Dealer
from Player import Player
import constants as const

# This should be even, so all wins and losses are integers.
BET_UNIT = 2

default_rules = {
    'num_decks': 6,
    'cut_card_pct': 25,
    'hit_s17': 1,
    'das_allowed': 1,
    'max_split_hands': 4,
    'max_split_aces': 2,
    'can_hit_split_aces': 0,
    'surrender_allowed': 0
    }


class Game:
    def __init__(self,
                 players=1,
                 rules=default_rules,
                 strategy={},
                 # cut_card_pct=0.25,
                 repeatable=False,
                 bet_spread=1,
                 verbose=False) -> None:
        self.verbose = verbose
        self.num_players = players
        self.players: List[Player] = []
        self.strategy: Set[Tuple[str, int, int]] = strategy
        self.rules = rules
        self.num_decks = rules['num_decks']
        self.shuffle_point = int(self.num_decks * 52 * rules['cut_card_pct'] // 100)
        # print("shuffle point:", self.shuffle_point)
        self.shoe = Shoe(self.num_decks, repeatable=repeatable)
        self.bet_amount = BET_UNIT
        self.bet_spread = bet_spread
        self.true_count = 0

        self.by_count: Dict[int, Statistics] = {}
        for n in range(-const.MAX_TRUE_COUNT, const.MAX_TRUE_COUNT + 1):
            self.by_count[n] = Statistics()

        log(f"house rules: {rules}")
        self.hit_s17 = rules['hit_s17']

        log("shuffle")
        self.shoe.shuffle()
        log("new dealer")
        self.dealer = Dealer(self.shoe, hit_s17=self.hit_s17,
                             verbose=self.verbose)
        for i in range(self.num_players):
            log(f"new player: {i + 1}")
            p = Player(self.shoe, self.strategy, self.rules, self.verbose,
                       seat=i + 1)
            self.players.append(p)

    def adjust_bet_amount(self) -> None:
        "Set bet_amount as determined by true count and config."
        # WARNING: self.set_true_count must have just been called!
        if self.true_count <= 0:
            new_bet = BET_UNIT
            # log(f"BET: {new_bet}  COUNT: {self.true_count}")
        else:
            bet_factor = self.true_count
            if bet_factor > self.bet_spread:
                bet_factor = self.bet_spread
            new_bet = bet_factor * BET_UNIT
            # log(f"BET: {new_bet}  COUNT: {self.true_count}")
        if new_bet != self.bet_amount:
            # log(f"CHANGE: {new_bet}  COUNT: {self.true_count}")
            self.bet_amount = new_bet

    def set_true_count(self) -> None:
        c = self.shoe.true_count()
        if c < -const.MAX_TRUE_COUNT:
            c = -const.MAX_TRUE_COUNT
        elif c > const.MAX_TRUE_COUNT:
            c = const.MAX_TRUE_COUNT
        self.true_count = c

    def play_round(self) -> None:
        """
        Deal hands to each player and the dealer.
        If the dealer has a BJ, settle all hands now.
        Otherwise, play each player hand, and then the dealer hand.
        Collect data on win/loss/push.
        """
        if self.shoe.remaining() < self.shuffle_point:
            log("shuffle")
            self.shoe.shuffle()
        self.shoe.start_round()
        self.set_true_count()
        self.adjust_bet_amount()

        # Deal player hands
        for p in self.players:
            self.by_count[self.true_count].hands_played += 1
            p.get_hand()
            log(f"player {p.seat}  hand: {p.hands[0]}")
            if self.verbose:
                print(f"Player: {p.hands[0]}")
            if p.hands[0].blackjack:
                log("player blackjack")
                if self.verbose:
                    print("Player BJ")

        self.dealer.get_hand()
        if self.dealer.hand.blackjack:
            log("dealer blackjack")
            if self.verbose:
                print("Dealer BJ")
            # No need to play the players' hands. They will all lose
            # unless they have a blackjack also.
        else:
            for p in self.players:
                log(f"player {p.seat}")
                p.play_hands(self.dealer.up_card())

            log(f"dealer: {self.dealer.hand}")
            # log("play dealer hand")
            self.dealer.play_hand()

        self.update_stats()

        for p in self.players:
            # This clears out hands just played.
            p.end_round()
        self.by_count[self.true_count].rounds_played += 1

    def update_stats(self) -> None:
        "Determine the result of each player hand. Compute wins and losses."
        log("update stats HERE --------------")
        dlr = self.dealer.hand.value
        dbj = self.dealer.hand.blackjack
        dbust = self.dealer.hand.busted
        log(f"dealer has {dlr}")
        if self.verbose:
            print('\nRESULTS')

        tc = self.true_count
        for pnum, p in enumerate(self.players):
            if self.verbose:
                print("player:", pnum + 1)
            for n, h in enumerate(p.hands):
                log(f"p{p.seat} hand {n + 1}: {h.value}")
                if self.verbose:
                    print(f"hand {n + 1}: {h.value}")
                if h.obsolete:
                    if self.verbose:
                        print('obsolete')
                    log("hand is obsolete")
                    # Hand has been split into two. Nothing to do.
                    continue

                if h.doubled:
                    this_bet = self.bet_amount * 2
                else:
                    this_bet = self.bet_amount
                self.by_count[tc].total_bet += this_bet

                if h.blackjack:
                    if not dbj:
                        win = this_bet * 3 // 2
                        log(f"WIN: blackjack: {win}")
                        if self.verbose:
                            print(f'BJ: WIN {win}')
                        self.by_count[tc].total_won += win
                        self.by_count[tc].total_bj_bonus += this_bet // 2
                        continue

                if dbj:
                    if h.blackjack:
                        log("PUSH: blackjacks")
                        if self.verbose:
                            print('BJ: PUSH')
                        self.by_count[tc].total_push += this_bet
                    else:
                        log(f"LOSS. Dealer BJ: {this_bet}")
                        if self.verbose:
                            print(f'LOSE to dealer BJ. LOSE {this_bet}.')
                        self.by_count[tc].total_lost += this_bet
                else:  # NO BJs
                    if h.busted:
                        log(f"LOSS - busted: {this_bet}")
                        if self.verbose:
                            print(f'BUST: LOSE {this_bet}')
                        self.by_count[tc].total_lost += this_bet
                    elif h.surrendered:
                        loss = this_bet // 2
                        log(f"SURRENDER: LOSE {loss}")
                        if self.verbose:
                            print(f'SURRENDER: LOSE {loss}')
                        self.by_count[tc].total_lost += loss
                        self.by_count[tc].total_surrendered += loss
                    elif dbust:
                        log(f"WIN - dealer bust: {this_bet}")
                        if self.verbose:
                            print(f'Dealer bust: WIN {this_bet}')
                        self.by_count[tc].total_won += this_bet
                    elif dlr > h.value:
                        log(f"LOSS: {this_bet}")
                        if self.verbose:
                            print(f'LOSE {this_bet}')
                        self.by_count[tc].total_lost += this_bet
                    elif h.value > dlr:
                        log(f"WIN: {this_bet}")
                        if self.verbose:
                            print(f'WIN {this_bet}')
                        self.by_count[tc].total_won += this_bet
                    else:
                        log("PUSH")
                        if self.verbose:
                            print('PUSH result 0')
                        self.by_count[tc].total_push += this_bet
        log("                  --------------")

    def write_stats(self, fname: str, strategy_name: str) -> None:
        "Append stats to the stats file"
        log("writing stats")
        with open(fname, 'at') as f:
            print("time", time.asctime(), file=f)
            print("strategy", strategy_name, file=f)

            total_bet = 0
            total_won = 0
            total_lost = 0
            for tc in range(-const.MAX_TRUE_COUNT, const.MAX_TRUE_COUNT + 1):
                r = self.by_count[tc].rounds_played
                h = self.by_count[tc].hands_played
                b = self.by_count[tc].total_bet
                w = self.by_count[tc].total_won
                ls = self.by_count[tc].total_lost
                p = self.by_count[tc].total_push
                bj = self.by_count[tc].total_bj_bonus
                s = self.by_count[tc].total_surrendered
                if b > 0:
                    gain = 100 * (w - ls) / b
                else:
                    gain = 0.0
                print(f"tc {tc} {r} {h} {b} {w} {ls} {p} {bj} {s} {gain:5.4}", file=f)
                assert w + ls + p - bj + s == b
                total_bet += b
                total_won += w
                total_lost += ls
            g = 100 * (total_won - total_lost) / total_bet
            msg = f"session gain: {g:5.4}"
            print(msg, file=f)
            print(msg)


class Statistics():
    "Just a struct to hold the data we want to accumulate."
    def __init__(self) -> None:
        self.rounds_played = 0
        self.hands_played = 0
        self.total_bet = 0
        self.total_won = 0
        self.total_lost = 0
        self.total_push = 0
        self.total_bj_bonus = 0
        self.total_surrendered = 0
