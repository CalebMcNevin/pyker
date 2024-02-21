from itertools import product, groupby, combinations
from random import shuffle, seed
from functools import total_ordering
from collections import Counter
from typing import Tuple

from .enums import Suit, Rank, HandType
from .card import Card

seed(0)


class Deck(object):

    def __init__(
        self,
        card_def: str | list[Card] | Tuple[list[Rank], list[Suit]]
        | 'Deck' | None = None,
    ):
        match card_def:
            case str():
                self.cards = Deck.parse_cards(card_def)
            case list():
                self.cards = card_def
            case tuple():
                ranks, suits = card_def
                self.cards = [Card((r, s)) for (r, s) in product(ranks, suits)]
            case Deck():
                self.cards = card_def.cards
            case None:
                self.cards = [Card((r, s)) for (r, s) in product(Rank, Suit)]
            case _:
                raise ValueError
        self.sort()

    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __eq__(self, other):
        return self.cards == other.cards

    def __add__(self, other):
        return Deck(self.cards + other.cards)

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

    @staticmethod
    def parse_cards(card_def: str = ''):
        card_strings = card_def.split(' ')
        cards = [Card(cs) for cs in card_strings]
        print(cards)
        return cards

    def shuffle(self):
        shuffle(self.cards)

    def deal(self, n_cards: int = 1):
        self.cards, dealt_cards = self.cards[n_cards:], self.cards[:n_cards]
        return Deck(dealt_cards)

    def add_cards(self, cards):
        self.cards += cards

    def get_suits(self, suits: list[Suit]):
        cards = Deck(list(filter(lambda card: card.suit in suits, self.cards)))
        cards.sort()
        return cards

    def get_ranks(self, ranks: list[Rank]):
        cards = Deck(list(filter(lambda card: card.rank in ranks, self.cards)))
        cards.sort()
        return cards

    def sort_by_rank(self, aces_high: bool = True):
        self.cards = sorted(self.cards,
                            reverse=True,
                            key=lambda card: card.rank.number
                            if not aces_high else
                            (card.rank.number
                             if card.rank != Rank.ACE else 14))

    def sort_by_suit(self):
        self.cards = sorted(self.cards, key=lambda card: card.suit.index)

    def sort(self):
        self.sort_by_suit()
        self.sort_by_rank()

    def scored(self):
        possible_hands = combinations(self.cards, 5)
        best_hand = max(ScoredHand(list(h)) for h in possible_hands)
        return best_hand


@total_ordering
class ScoredHand(Deck):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.cards) != 5:
            raise ValueError
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
        return f"{self.hand_type.name.title().replace('_',' ')} - {super().__str__()}"

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
        self.sort_by_rank(aces_high=True)
        if all(self[i] >> self[i + 1] for i in range(4)):
            return True
        self.sort_by_rank(aces_high=False)
        if all(self[i] >> self[i + 1] for i in range(4)):
            return True
        return False

    def check_flush(self):
        suit = self[0].suit
        if all((card.suit == suit for card in self.cards)):
            return True
        return False
