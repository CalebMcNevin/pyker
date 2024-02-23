from __future__ import annotations
from typing import Tuple
from random import shuffle
from itertools import product, combinations
from functools import cached_property

from .enums import Rank, Suit
from .card import Card
from .scored_hand import ScoredHand


class Deck(object):
    _id = 0

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
        Deck._id += 1
        self._id = Deck._id
        self._original_cardset = self.cards
        self._best_hand_updated = False
        self.sort()

    def __str__(self):
        return "  ".join(str(card) for card in self.cards)

    def __repr__(self):
        class_name = type(self).__name__
        cards_list = '  '.join(str(card) for card in self.cards[:8])
        return f'<{class_name} id={self._id} num_cards={len(self.cards)} cards=[{cards_list} {"..." if len(self.cards)>8 else ""}]>'

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

    def __eq__(self, other):
        return self.cards == other.cards

    def __add__(self, other):
        return Deck(self.cards + other.cards)

    @property
    def original_cardset(self):
        return list(self._original_cardset)

    @staticmethod
    def parse_cards(card_def: str = ''):
        card_strings = card_def.split(' ')
        cards = [Card(cs) for cs in card_strings]
        print(cards)
        return cards

    def retrieve_cards(self):
        """Retrieve all cards that have been dealt or removed from the cards list"""
        self.cards = self._original_cardset

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
