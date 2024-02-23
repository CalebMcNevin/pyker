from __future__ import annotations
from functools import total_ordering
from collections import Counter

from .enums import Rank, Suit, HandType
from .utils import sort_cards_by_rank


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
        return False

    def __lt__(self, other):
        if self.hand_type.value < other.hand_type.value:
            return True
        if self.hand_type.value > other.hand_type.value:
            return False
        for s, o in zip(self.kickers, other.kickers):
            if s < o:
                return True
            if s > o:
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
        self.cards = sort_cards_by_rank(cards=self.cards, aces_high=aces_high)

    def score_hand(self):
        self.sort()
        self.hand_type = None
        self.kickers = []

        if self.is_flush and self.is_straight:
            self._score_straight_flush()
        elif self.is_flush:
            self._score_flush()
        elif self.is_straight:
            self._score_straight()
        else:
            self._score_rank_match()

    def _score_straight_flush(self):
        if Rank.ACE in self.ranks and Rank.KING in self.ranks:
            self.hand_type = HandType.ROYAL_FLUSH
        else:
            self.hand_type = HandType.STRAIGHT_FLUSH
            self.kickers.append(self.cards[0].rank)

    def _score_flush(self):
        self.hand_type = HandType.FLUSH
        self.kickers = [c.rank for c in self.cards]

    def _score_straight(self):
        self.hand_type = HandType.STRAIGHT
        self.kickers.append(self.cards[0].rank)

    def _score_rank_match(self):
        counter = Counter([card.rank.name for card in self.cards])
        most_common = counter.most_common()
        counts = [x[1] for x in most_common]
        self.kickers += [Rank[name] for name, _ in most_common]

        if counts[0] == 4:
            self.hand_type = HandType.FOUR_OF_A_KIND
        elif counts[0] == 3:
            if counts[1] == 2:
                self.hand_type = HandType.FULL_HOUSE
            else:
                self.hand_type = HandType.THREE_OF_A_KIND
        elif counts[0] == 2:
            if counts[1] == 2:
                self.hand_type = HandType.TWO_PAIR
            else:
                self.hand_type = HandType.PAIR
        else:
            self.hand_type = HandType.HIGH_CARD

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
