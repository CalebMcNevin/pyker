from __future__ import annotations
from functools import total_ordering
from collections import Counter

from .enums import Rank, Suit, HandType


@total_ordering
class ScoredHand():

    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError
        self.cards = cards
        self.hand_type = None
        self.kickers = []
        self.is_flush = self.check_flush()
        self.is_straight = self.check_straight()
        self.score_hand()

    def __eq__(self, other):
        if self.hand_type == other.hand_type:
            return self.kickers == other.kickers
        else:
            return False

    def __lt__(self, other):
        if self.hand_type.value < other.hand_type.value:
            return True
        elif self.hand_type.value > other.hand_type.value:
            return False
        else:
            for s, o in zip(self.kickers, other.kickers):
                if s < o:
                    return True
                elif s > o:
                    return False
            return False

    def __str__(self):
        hand_name = self.hand_type.name.title().replace('_', ' ')
        hand_string = ", ".join(str(card) for card in self.cards)
        return f"{hand_name} - {hand_string}"

    @property
    def suits(self):
        suits = []
        for suit in Suit:
            if any(card.suit == suit for card in self.cards):
                suits.append(suit)
        return suits

    @property
    def ranks(self):
        ranks = []
        for rank in Rank:
            if any(card.rank == rank for card in self.cards):
                ranks.append(rank)
        return ranks

    def sort(self, aces_high: bool = True):
        self.cards = sorted(self.cards,
                            reverse=True,
                            key=lambda card: card.rank.number
                            if not aces_high else
                            (card.rank.number
                             if card.rank != Rank.ACE else 14))

    def score_hand(self):
        self.sort()
        self.hand_type = None
        self.kickers = []

        # Look for straight and flush based hands
        if self.is_flush and self.is_straight:
            if Rank.ACE in self.ranks and Rank.KING in self.ranks:
                self.hand_type = HandType.ROYAL_FLUSH
                return
            else:
                self.hand_type = HandType.STRAIGHT_FLUSH
                self.kickers.append(self.cards[0].rank)
                return
        if self.is_flush:
            self.hand_type = HandType.FLUSH
            self.kickers = [c.rank for c in self.cards]
            return
        if self.is_straight:
            self.hand_type = HandType.STRAIGHT
            self.kickers.append(self.cards[0].rank)
            return

        # Look for rank-match based hands
        counter = Counter([card.rank.name for card in self.cards])
        most_common = counter.most_common()
        counts = [x[1] for x in most_common]
        self.kickers += [Rank[name] for name, _ in most_common]
        if counts[0] == 4:
            self.hand_type = HandType.FOUR_OF_A_KIND
            return
        elif counts[0] == 3:
            if counts[1] == 2:
                self.hand_type = HandType.FULL_HOUSE
                return
            else:
                self.hand_type = HandType.THREE_OF_A_KIND
                return
        elif counts[0] == 2:
            if counts[1] == 2:
                self.hand_type = HandType.TWO_PAIR
                return
            else:
                self.hand_type = HandType.PAIR
                return
        else:
            self.hand_type = HandType.HIGH_CARD
            return
        raise Exception(f'''Failed to find hand type for {self.__repr__()}:
            {[str(card) for card in self.cards]}''')

    def check_straight(self):
        self.sort(aces_high=True)
        if all(self.cards[i] >> self.cards[i + 1] for i in range(4)):
            return True
        self.sort(aces_high=False)
        if all(self.cards[i] >> self.cards[i + 1] for i in range(4)):
            return True
        return False

    def check_flush(self):
        suit = self.cards[0].suit
        if all((card.suit == suit for card in self.cards)):
            return True
        return False
