from __future__ import annotations
from typing import Tuple
from random import shuffle
from itertools import product, combinations
from functools import cached_property

from .enums import Rank, Suit
from .card import Card
from .scored_hand import ScoredHand


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
        self._best_hand_updated = False
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
        if self._best_hand_updated:
            del self.best_hand
        return Deck(dealt_cards)

    def add_cards(self, cards):
        self.cards += cards
        if self._best_hand_updated:
            del self.best_hand

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

    @cached_property
    def best_hand(self):
        self.best_hand_updated = True
        possible_hands = combinations(self.cards, 5)
        best_hand = max(ScoredHand(list(h)) for h in possible_hands)
        return best_hand