from __future__ import annotations

from functools import cached_property
from itertools import combinations, product
from random import shuffle
from typing import Tuple

from .card import Card
from .enums import Rank, Suit
from .scored_hand import ScoredHand


class Deck():
    _id: int = 0

    def __init__(
        self: Deck,
        card_def: str | list[Card] | Tuple[list[Rank], list[Suit]]
        | 'Deck' | None = None,
    ):
        match card_def:
            case str():
                self.cards: list[Card] = Deck.parse_cards(card_def)
            case list():
                self.cards: list[Card] = card_def
            case tuple():
                ranks: list[Rank] = card_def[0]
                suits: list[Rank] = card_def[1]
                self.cards: list[Card] = [
                    Card((r, s)) for (r, s) in product(ranks, suits)
                ]
            case Deck():
                self.cards: list[Rank] = card_def.cards
            case None:
                self.cards: list[Rank] = [
                    Card((r, s)) for (r, s) in product(Rank, Suit)
                ]
            case _:
                raise ValueError
        Deck._id += 1
        self._id: int = Deck._id
        self._original_cardset: list[Card] = self.cards
        self._best_hand_updated: bool = False
        self.sort()

    def __str__(self: Deck) -> str:
        return "  ".join(str(card) for card in self.cards)

    def __repr__(self: Deck) -> str:
        class_name = type(self).__name__
        cards_list = '  '.join(str(card) for card in self.cards[:8])
        result = f'<{class_name} id={self._id} num_cards={len(self.cards)}'
        result += f' cards=[{cards_list} {"..." if len(self.cards)>8 else ""}]>'
        return result

    def __iter__(self: Deck) -> iter:
        return iter(self.cards)

    def __getitem__(self: Deck, index: int) -> Card:
        return self.cards[index]

    def __eq__(self: Deck, other: Deck) -> bool:
        return self.cards == other.cards

    def __add__(self: Deck, other: Deck) -> None:
        return Deck(self.cards + other.cards)

    @property
    def original_cardset(self: Deck) -> list[Card]:
        return list(self._original_cardset)

    @staticmethod
    def parse_cards(card_def: str = '') -> Tuple[Rank, Suit]:
        card_strings = card_def.split(' ')
        cards = [Card(cs) for cs in card_strings]
        return cards

    def retrieve_cards(self: Deck) -> None:
        """Reset cards list to original. Equivalent to 'retrieving' all dealt cards."""
        self.cards = self._original_cardset

    def shuffle(self: Deck) -> None:
        shuffle(self.cards)

    def deal(self: Deck, n_cards: int = 1) -> Deck:
        self.cards, dealt_cards = self.cards[n_cards:], self.cards[:n_cards]
        if self._best_hand_updated:
            del self.best_hand
        return Deck(dealt_cards)

    def add_cards(self: Deck, cards: list[Card]) -> None:
        self.cards += cards
        if self._best_hand_updated:
            del self.best_hand

    def sort_by_rank(self: Deck, aces_high: bool = True) -> None:
        self.cards = sorted(self.cards,
                            reverse=True,
                            key=lambda card: card.rank.number
                            if not aces_high else
                            (card.rank.number
                             if card.rank != Rank.ACE else 14))

    def sort_by_suit(self: Deck) -> None:
        self.cards = sorted(self.cards, key=lambda card: card.suit.index)

    def sort(self: Deck) -> None:
        self.sort_by_suit()
        self.sort_by_rank()

    @cached_property
    def best_hand(self: Deck) -> ScoredHand:
        self.best_hand_updated = True
        possible_hands = combinations(self.cards, 5)
        best_hand = max(ScoredHand(list(h)) for h in possible_hands)
        return best_hand
